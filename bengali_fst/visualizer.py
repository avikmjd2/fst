"""
visualizer.py — Bengali FST State Path Visualizer

Shows the REAL pynini state IDs traversed when recognizing a word.

Example output for a lexicon word:

  Morphological analysis: তুমি
  ──────────────────────────────────────────────────
  FST State Traversal (pynini state IDs):
    q0 -[ত]-> q3 -[ু]-> q7 -[ম]-> q12 -[ি]-> ((q15))

  Analysis (from FST output):
    Lemma    : তুমি
    POS      : PRON
    Features : Case=Nom|Number=Sing|Person=2|PronType=Prs
    Source   : [lexicon]

Example for a heuristic word:

  Morphological analysis: খেলেছিল
  ──────────────────────────────────────────────────
  [!] Word not in FST — running heuristic suffix rules
  FST State Traversal (grapheme-cluster simulation):
    q0 -[খে]-> q1 -[লে]-> q2 -[ছি]-> q3 -[ল]-> ((q4))

  Analysis (heuristic):
    Lemma    : খেলেছিল
    POS      : VERB
    Features : Aspect=Perf|VerbForm=Fin
    Source   : [heuristic]
"""
import unicodedata

COMBINING = {
    '\u09BC', '\u09BE', '\u09BF', '\u09C0', '\u09C1', '\u09C2',
    '\u09C3', '\u09C4', '\u09C7', '\u09C8', '\u09CB', '\u09CC',
    '\u09CD', '\u09D7', '\u09E2', '\u09E3',
}


def grapheme_clusters(word):
    """Split Bengali word into grapheme clusters."""
    clusters = []
    i = 0
    chars = list(word)
    while i < len(chars):
        cluster = chars[i]
        i += 1
        while i < len(chars) and chars[i] in COMBINING:
            cluster += chars[i]
            i += 1
            if cluster.endswith('\u09CD') and i < len(chars):
                cluster += chars[i]
                i += 1
        clusters.append(cluster)
    return clusters


def _render_real_path(grapheme_path):
    """
    Render the FST path using pynini state IDs.
    grapheme_path: list of (entry_state, cluster, exit_state)
    """
    parts = []
    for i, (entry, cluster, exit_st) in enumerate(grapheme_path):
        parts.append(f"q{entry} -[{cluster}]->")
    # Final accepting state (double parens)
    last_exit = grapheme_path[-1][2]
    path_str = " ".join(parts) + f" ((q{last_exit}))"
    return path_str


def _render_simulated_path(word):
    """
    For heuristic words (not in FST), simulate state IDs as q0, q1, q2...
    Uses grapheme clusters as arc labels.
    """
    clusters = grapheme_clusters(word)
    parts = []
    for i, cluster in enumerate(clusters):
        parts.append(f"q{i} -[{cluster}]->")
    final = len(clusters)
    return " ".join(parts) + f" ((q{final}))"


def format_analysis(word, lexicon_entry=None, heuristic=False, grapheme_path=None):
    """
    Full formatted output for one Bengali word.

    Parameters:
        word          : surface Bengali word
        lexicon_entry : dict {lemma, upos, feats} if found
        heuristic     : True if resolved by heuristic rules
        grapheme_path : list of (state, cluster, next_state) from pynini
    """
    sep = "\u2500" * 50  # ──────────────────────────────────────────────────

    lines = []
    lines.append(f"\nMorphological analysis: {word}")
    lines.append(sep)

    # --- State traversal ---
    if grapheme_path:
        lines.append("FST State Traversal (pynini state IDs):")
        lines.append("  " + _render_real_path(grapheme_path))
        lines.append("")
        lines.append("  Arc-by-arc breakdown:")
        for entry, cluster, exit_st in grapheme_path:
            lines.append(f"    State q{entry}  --[{cluster}]-->  State q{exit_st}")
        final_st = grapheme_path[-1][2]
        lines.append(f"    State q{final_st} = FINAL (accepting state) ✓")
    else:
        if heuristic:
            lines.append("[!] Word not in FST — running heuristic suffix rules")
        lines.append("FST State Traversal (grapheme-cluster simulation):")
        lines.append("  " + _render_simulated_path(word))

    lines.append("")

    # --- Analysis result ---
    lines.append("Analysis result:")
    if lexicon_entry:
        lemma = lexicon_entry.get("lemma", word)
        upos  = lexicon_entry.get("upos",  "?")
        feats = lexicon_entry.get("feats", "_")
        src   = "[heuristic]" if heuristic else "[lexicon / FST]"
    else:
        lemma, upos, feats, src = word, "?", "_", "[unknown]"

    lines.append(f"  Lemma    : {lemma}")
    lines.append(f"  POS      : {upos}")
    lines.append(f"  Features : {feats}")
    lines.append(f"  Source   : {src}")

    return "\n".join(lines)
