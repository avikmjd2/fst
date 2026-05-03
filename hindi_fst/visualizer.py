"""
visualizer.py — Hindi FST State Path Visualizer

Shows real pynini state IDs for lexicon words, simulated states for heuristic words.
"""

# Devanagari combining marks
COMBINING = {
    '\u0900', '\u0901', '\u0902', '\u0903',
    '\u093A', '\u093B', '\u093C',
    '\u093E', '\u093F', '\u0940',
    '\u0941', '\u0942', '\u0943', '\u0944',
    '\u0945', '\u0946', '\u0947', '\u0948',
    '\u0949', '\u094A', '\u094B', '\u094C',
    '\u094D',
    '\u094E', '\u094F',
    '\u0951', '\u0952', '\u0953', '\u0954',
    '\u0962', '\u0963',
}


def grapheme_clusters(word):
    """Split a Devanagari word into grapheme clusters."""
    clusters = []
    i = 0
    chars = list(word)
    while i < len(chars):
        cluster = chars[i]
        i += 1
        while i < len(chars) and chars[i] in COMBINING:
            cluster += chars[i]
            i += 1
            # After virama, absorb next base letter
            if cluster.endswith('\u094D') and i < len(chars):
                cluster += chars[i]
                i += 1
        clusters.append(cluster)
    return clusters


def _render_real_path(grapheme_path):
    """Render FST path using real pynini state IDs."""
    parts = []
    for entry, cluster, exit_st in grapheme_path:
        parts.append(f"q{entry} -[{cluster}]->")
    last_exit = grapheme_path[-1][2]
    return " ".join(parts) + f" ((q{last_exit}))"


def _render_simulated_path(word):
    """Simulate state IDs q0, q1, q2... for heuristic words."""
    clusters = grapheme_clusters(word)
    parts = []
    for i, cluster in enumerate(clusters):
        parts.append(f"q{i} -[{cluster}]->")
    return " ".join(parts) + f" ((q{len(clusters)}))"


def format_analysis(word, lexicon_entry=None, heuristic=False, grapheme_path=None):
    """Full formatted FST state-path output for one Hindi word."""
    sep = "\u2500" * 50

    lines = []
    lines.append(f"\nMorphological analysis: {word}")
    lines.append(sep)

    # State traversal
    if grapheme_path:
        lines.append("FST State Traversal (pynini state IDs):")
        lines.append("  " + _render_real_path(grapheme_path))
        lines.append("")
        lines.append("  Arc-by-arc breakdown:")
        for entry, cluster, exit_st in grapheme_path:
            lines.append(f"    State q{entry}  --[{cluster}]-->  State q{exit_st}")
        final_st = grapheme_path[-1][2]
        lines.append(f"    State q{final_st} = FINAL (accepting state) \u2713")
    else:
        if heuristic:
            lines.append("[!] Word not in FST \u2014 running heuristic suffix rules")
        lines.append("FST State Traversal (grapheme-cluster simulation):")
        lines.append("  " + _render_simulated_path(word))

    lines.append("")

    # Analysis result
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
