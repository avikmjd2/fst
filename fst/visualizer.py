"""
visualizer.py - State-Graph Visualization
Formats the FST arc path into the character-by-character
state graph display with branching for y->i transformations.
"""


def format_analysis(result):
    """
    Format the complete analysis output for a given AnalysisResult.

    Returns a multi-line string containing:
      1. Morphological breakdown with tags
      2. Character-by-character state graph
    """
    if result is None:
        return "  Word not recognized in lexicon.\n"

    lines = []

    # ── 1. Morphological breakdown ──────────────────────────────
    morph_str = " + ".join(m for m, _ in result.morphemes)
    tag_str = " + ".join(t for _, t in result.morphemes)
    lines.append("Morphological analysis:")
    lines.append(f"    {morph_str} ({tag_str})")
    lines.append("")

    # ── 2. State graph ──────────────────────────────────────────
    arc_path = result.arc_path
    yi = result.y_to_i_index  # -1 when no y→i change

    if yi == -1:
        # Simple linear path (no y→i branching)
        lines.append(_linear_path(arc_path))
    else:
        # Branching path: show root line ending at y, then
        # a vertical branch into i + suffix continuation
        lines.append(_branching_path(arc_path, yi))

    return "\n".join(lines)


# ─── helpers ────────────────────────────────────────────────────────

def _state_label(state_id, char, is_final=False):
    """Format a single state+char node:  (n)[x] or ((n))[x]."""
    if is_final:
        return f"(({state_id}))[{char}]"
    return f"({state_id})[{char}]"


def _linear_path(arc_path):
    """Build a simple left-to-right chain of state nodes."""
    # Filter out boundary arcs (where output is '+' or input is empty)
    filtered = [(sid, in_ch) for sid, in_ch, out_ch in arc_path
                if out_ch != "+" and in_ch != ""]
    nodes = []
    for i, (sid, in_ch) in enumerate(filtered):
        is_final = (i == len(filtered) - 1)
        nodes.append(_state_label(sid, in_ch, is_final))
    return " -> ".join(nodes)


def _branching_path(arc_path, yi):
    """
    Build the two-line branching display around the y→i point.

    Line 1 (top):   prefix + root chars ending with the original 'y'
    Branch:         pipe + V dropping down from the node before 'y'
    Line 2 (bottom): 'i' (surface char) followed by the suffix chars

    Example:
    (5)[u] -> (6)[n] -> (1)[h] -> (2)[a] -> (3)[p] -> [p] -> ((4))[y]
                                                     |
                                                     V
                                                (7)[i] -> (8)[n] -> ...
    """
    # ── Collect top-line nodes (prefix + root up through 'y') ──
    top_nodes = []
    for i in range(yi):
        sid, in_ch, out_ch = arc_path[i]
        if out_ch == "+" or in_ch == "":
            continue
        top_nodes.append(_state_label(sid, in_ch))

    # Append the 'y' as a final-state node (the root's logical end)
    yi_sid, _, _ = arc_path[yi]
    top_nodes.append(_state_label(yi_sid, "y", is_final=True))

    top_line = " -> ".join(top_nodes)

    # ── Branch column: pipe drops below the second-to-last node ─
    # Build the string up to (and including) the arrow before the
    # second-to-last node to find the right column.
    if len(top_nodes) >= 2:
        prefix_str = " -> ".join(top_nodes[:-1])
        # The pipe should be under the start of the LAST real node
        # before 'y' — i.e. right after the last " -> "
        branch_col = len(prefix_str) + len(" -> ")
    else:
        branch_col = 0

    # ── Bottom-line nodes ('i' + suffix chars) ──────────────────
    bottom_nodes = []
    bottom_nodes.append(_state_label(yi_sid, "i"))

    for i in range(yi + 1, len(arc_path)):
        sid, in_ch, out_ch = arc_path[i]
        if out_ch == "+" or in_ch == "":
            continue
        is_final = (i == len(arc_path) - 1)
        bottom_nodes.append(_state_label(sid, in_ch, is_final))

    bottom_line = " -> ".join(bottom_nodes)

    # ── Assemble the three visual rows ──────────────────────────
    indent = " " * branch_col
    pipe_line = indent + "|"
    v_line = indent + "V"
    padded_bottom = indent + bottom_line

    return "\n".join([top_line, pipe_line, v_line, padded_bottom])
