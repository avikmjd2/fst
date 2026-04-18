"""
analyzer.py - Morphological Analysis Engine
Uses pynini.shortestpath and arc iteration to extract state-level
paths through the FST for a given surface word.
"""

import pynini

from lexicon import BOUNDARY, PREFIXES, ROOTS, SUFFIXES, get_tag


class AnalysisResult:
    """Holds the results of a morphological analysis."""

    def __init__(self, surface, lexical, morphemes, arc_path, y_to_i_index):
        self.surface = surface          # e.g. "unhappiness"
        self.lexical = lexical          # e.g. "un+happy+ness"
        self.morphemes = morphemes      # [("un","NEG"), ("happy","ROOT"), ("ness","SUFF")]
        self.arc_path = arc_path        # [(state_id, input_char, output_char), ...]
        self.y_to_i_index = y_to_i_index  # index in arc_path where y->i happens (-1 if none)


def analyze(word, analyzer_fst):
    """
    Analyze a surface word using the analyzer FST.

    Steps:
      1. Compose input word with the analyzer FST
      2. Use pynini.shortestpath to get the best path
      3. Iterate through arcs to extract state IDs and labels
      4. Parse the lexical output to identify morphemes

    Returns an AnalysisResult or None if the word is not recognized.
    """
    try:
        input_fst = pynini.accep(word)
        result = pynini.compose(input_fst, analyzer_fst)

        if result.start() == pynini.NO_STATE_ID:
            return None

        path = pynini.shortestpath(result)
        path = path.rmepsilon()

        # ── Extract arc-level path ──────────────────────────────
        arc_path = []
        state = path.start()

        while path.num_arcs(state) > 0:
            aiter = path.arcs(state)
            arc = next(aiter)

            # Decode labels (byte-valued in pynini)
            in_ch = chr(arc.ilabel) if arc.ilabel > 0 else ""
            out_ch = chr(arc.olabel) if arc.olabel > 0 else ""

            arc_path.append((state, in_ch, out_ch))
            state = arc.nextstate

        # Record the final (accepting) state
        final_state = state

        # ── Reconstruct the lexical string from output labels ───
        lexical = "".join(out_ch for _, _, out_ch in arc_path)

        # ── Identify morphemes ──────────────────────────────────
        parts = lexical.split(BOUNDARY)
        morphemes = _tag_morphemes(parts)

        # ── Detect y → i transformation ────────────────────────
        y_to_i_index = -1
        for i, (_, in_ch, out_ch) in enumerate(arc_path):
            if in_ch == "i" and out_ch == "y":
                y_to_i_index = i
                break

        return AnalysisResult(
            surface=word,
            lexical=lexical,
            morphemes=morphemes,
            arc_path=arc_path,
            y_to_i_index=y_to_i_index,
        )

    except pynini.FstOpError:
        return None


def _tag_morphemes(parts):
    """
    Given a list of morpheme strings (split on BOUNDARY),
    assign grammatical tags based on position and lexicon lookup.
    """
    if len(parts) == 1:
        return [(parts[0], "ROOT")]

    morphemes = []
    for i, part in enumerate(parts):
        if i == 0 and part in PREFIXES:
            morphemes.append((part, get_tag(part, "prefix")))
        elif i == len(parts) - 1 and part in SUFFIXES:
            morphemes.append((part, get_tag(part, "suffix")))
        else:
            morphemes.append((part, "ROOT"))
    return morphemes
