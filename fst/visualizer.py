"""
visualizer.py - FST State Path Visualizer

Renders the morphological analysis as a character-level state path diagram.

Format for a word with a suffix bend (e.g. y->i or clear prefix+suffix boundary):

  (13)[u] -> (12)[n] -> (10)[h] -> (9)[a] -> (8)[p] -> (7)[p] -> ((6))[y]
                                                                       |
                                                                       V
                                          (6)[i] -> (4)[n] -> (3)[e] -> (2)[s] -> ((1))[s]

For simple words (root + inflectional tag, no deriv suffix split), single row:

  (7)[w] -> (6)[a] -> (5)[l] -> (4)[k] -> (3)[i] -> (2)[n] -> ((1))[g]
"""


# ── Tag label mapping ──────────────────────────────────────────────────────────

_TAG_LABELS = {
    "p": "NEG",    # prefix like un_, re_
    "V": "ROOT",
    "N": "ROOT",
    "A": "ROOT",
    "O": "ROOT",
    "Q": "ROOT",
    "P": "ROOT",
    "B": "ROOT",
    "s": "SUFF",
}

_INFL_TAG_LABELS = {
    "+PCP1": "PRS.PTCP",
    "+PAST": "PST",
    "+PL":   "PL",
    "+3SG":  "3SG",
    "+GEN":  "GEN",
    "+SUP":  "SUP",
    "+CMP":  "CMP",
}


def _parse_lexical(lexical):
    """
    Parse lexical string into a list of (form, label) tuples.
    Handles:
      "walk_V +PCP1"          -> [("walk", "ROOT"), ("+PCP1", "PRS.PTCP")]
      "un_p luck_N y_s"       -> [("un", "NEG"), ("luck", "ROOT"), ("y", "SUFF")]
      "help_V ful_s"          -> [("help", "ROOT"), ("ful", "SUFF")]
      "help_V ful_s +PL"      -> [("help","ROOT"),("ful","SUFF"),("+PL","PL")]
    """
    parts = lexical.split()
    result = []
    for p in parts:
        if p.startswith("+"):
            label = _INFL_TAG_LABELS.get(p, p.lstrip("+"))
            result.append((p, label))
        elif "_" in p:
            form, raw_tag = p.rsplit("_", 1)
            label = _TAG_LABELS.get(raw_tag, raw_tag.upper())
            result.append((form, label))
        else:
            result.append((p, "ROOT"))
    return result


def _header_line(segments):
    """
    Build: un + luck + y  (NEG + ROOT + SUFF)
    Inflectional tags like +PCP1 are shown inline in the tag section.
    """
    forms = [s[0].lstrip("+") if s[0].startswith("+") else s[0] for s in segments]
    labels = [s[1] for s in segments]
    return " + ".join(forms) + "  (" + " + ".join(labels) + ")"


def _surface_from_lexical(word, segments):
    """
    Map the lexical segments back to surface characters.
    
    Strategy:
      1. Concatenate all form strings from segments (ignoring +INFL tags).
      2. Find where the surface `word` diverges (y->i substitution).
      3. Return (top_surface, bottom_surface, bend_char_idx)
         where top_surface is the prefix+root portion of `word`
         and bottom_surface is the suffix portion.
    
    If there's no derivational suffix in segments, there's no split:
    returns (word, None, None).
    """
    # Collect only morpheme forms (not inflectional tags)
    morph_forms = [(f, lbl) for f, lbl in segments if not f.startswith("+")]

    # Determine where root ends and suffix starts
    # Root ends at the last segment labelled ROOT (or NEG before ROOT)
    root_end_idx = -1
    for i, (f, lbl) in enumerate(morph_forms):
        if lbl in ("NEG", "ROOT"):
            root_end_idx = i

    has_suffix = any(lbl == "SUFF" for _, lbl in morph_forms)

    if not has_suffix:
        # No derivational split — single row
        return word, None, None

    # Build the prefix+root lexical string
    prefix_root_lex = "".join(f for f, lbl in morph_forms if lbl in ("NEG", "ROOT"))
    # Build the suffix lexical string
    suffix_lex = "".join(f for f, lbl in morph_forms if lbl == "SUFF")

    # Find where in the word the split happens
    # Case 1: direct split (e.g. help + ful -> helpful, split at 4)
    if word.startswith(prefix_root_lex):
        split_pos = len(prefix_root_lex)
        top_surface = word[:split_pos]
        bottom_surface = word[split_pos:]
        return top_surface, bottom_surface, split_pos - 1

    # Case 2: y->i substitution (e.g. luck + y -> unlucky, luckily)
    if prefix_root_lex.endswith("y"):
        candidate = prefix_root_lex[:-1] + "i"
        if word.startswith(candidate):
            split_pos = len(candidate)
            top_surface = word[:split_pos]       # ends with 'i' (was 'y')
            bottom_surface = word[split_pos:]
            return top_surface, bottom_surface, split_pos - 1

    # Case 3: e-deletion (e.g. like -> liking, drop 'e')
    if not word.startswith(prefix_root_lex):
        # try adding 'e' back
        for extra in ["e", ""]:
            candidate = prefix_root_lex + extra
            rest = word[len(candidate):]
            if word.startswith(prefix_root_lex[: len(prefix_root_lex) - len(extra)]):
                split_pos = len(word) - len(suffix_lex)
                if 0 < split_pos < len(word):
                    top_surface = word[:split_pos]
                    bottom_surface = word[split_pos:]
                    return top_surface, bottom_surface, split_pos - 1

    # Fallback: split by suffix length from end
    split_pos = len(word) - len(suffix_lex)
    if split_pos <= 0:
        return word, None, None
    top_surface = word[:split_pos]
    bottom_surface = word[split_pos:]
    return top_surface, bottom_surface, split_pos - 1


def _fmt_node(state, double=False):
    if double:
        return f"(({state}))"
    return f"({state})"


def _render_chars(chars, start_state, is_top=True, top_end_state=None):
    """
    Render a row of character transitions.
    
    chars: string of characters to render
    start_state: the state number of the FIRST character's entry state
    is_top: if True, the last node uses double parens (bend point)
            if False, the first node uses double parens (coming from bend)
                      and the last node uses double parens (final state)
    top_end_state: for bottom row, the state number to show for double-paren first node
    
    Returns the rendered string.
    """
    n = len(chars)
    tokens = []
    current_state = start_state

    for i, ch in enumerate(chars):
        next_state = current_state - 1
        if next_state < 1:
            next_state = 1

        # Format current (entry) node
        is_first_bottom = (not is_top and i == 0)
        is_last = (i == n - 1)

        if is_first_bottom:
            node_str = _fmt_node(current_state, double=True)
        else:
            node_str = _fmt_node(current_state)

        tokens.append(f"{node_str}[{ch}]")
        current_state = next_state

    # Append final exit node
    if is_top:
        # top row: last exit node is bend (double parens)
        tokens.append(_fmt_node(current_state, double=True))
    else:
        # bottom row: last exit is final state (double parens)
        tokens.append(_fmt_node(current_state, double=True))

    return " -> ".join(tokens)


def format_analysis(result):
    """
    Format the full FST state-path visualization.
    """
    if result is None or not result.lexical:
        return "  No analysis found."

    word = result.surface
    lexical = result.lexical

    segments = _parse_lexical(lexical)
    if not segments:
        return f"  Analysis: {lexical}"

    header = _header_line(segments)
    top_surface, bottom_surface, bend_idx = _surface_from_lexical(word, segments)

    lines = []
    lines.append("Morphological analysis:")
    lines.append(f"    {header}")
    lines.append("")

    total_len = len(word)
    start_state = total_len  # entry state for first character

    if bottom_surface is None:
        # Single row — no suffix split; first node is normal, last is double-paren
        n = len(word)
        tokens = []
        cur = start_state
        for i, ch in enumerate(word):
            nxt = cur - 1
            if nxt < 1:
                nxt = 1
            tokens.append(f"{_fmt_node(cur)}[{ch}]")
            cur = nxt
        tokens.append(_fmt_node(cur, double=True))
        lines.append(" -> ".join(tokens))
    else:
        # Two rows: top (prefix+root ending with double paren),
        # then vertical arrow, then bottom (suffix)

        # Top row starts at state=total_len, goes down
        top_row = _render_chars(top_surface, start_state, is_top=True)
        lines.append(top_row)

        # Compute bend column: position of the last token on top row
        # The last token is "((N))" — we want the arrow centered under it
        tokens = top_row.split(" -> ")
        prefix_width = len(" -> ".join(tokens[:-1]))
        if prefix_width:
            prefix_width += len(" -> ")
        last_token = tokens[-1]
        arrow_col = prefix_width + len(last_token) // 2

        lines.append(" " * arrow_col + "|")
        lines.append(" " * arrow_col + "V")

        # Bottom row — starts from bend_state = total_len - len(top_surface)
        bottom_start = total_len - len(top_surface)
        bottom_row = _render_chars(bottom_surface, bottom_start, is_top=False)

        # Indent bottom row so its first double-paren node is under the arrow
        first_token = bottom_row.split(" -> ")[0]
        indent = max(0, arrow_col - len(first_token) // 2)
        lines.append(" " * indent + bottom_row)

    return "\n".join(lines)
