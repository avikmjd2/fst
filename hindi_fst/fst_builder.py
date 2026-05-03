"""
fst_builder.py — Hindi Morphological FST

Builds a TRUE character-level Finite State Transducer using pynini.

Maps: surface_word (char by char) -> "lemma|UPOS|feats"
Each arc in the transducer = one Unicode codepoint.
"""
import pynini
from lexicon import VOCABULARY


def build_hindi_fsl():
    """
    Builds a character-level Hindi FST.
    Maps: surface_word -> "lemma|UPOS|feats"
    """
    pairs = []
    for word, info in VOCABULARY.items():
        lemma = info["lemma"]
        upos  = info["upos"]
        feats = info["feats"]
        analysis = f"{lemma}|{upos}|{feats}"
        pairs.append((word, analysis))

    fsl = pynini.string_map(pairs, input_token_type="utf8", output_token_type="utf8")
    fsl.optimize()
    return fsl


def is_valid_word(word, fsl):
    """Returns True if the FST accepts this word."""
    try:
        inp = pynini.accep(word, token_type="utf8")
        lattice = pynini.compose(inp, fsl)
        return lattice.num_states() > 0
    except Exception:
        return False


def analyze_word_fst(word, fsl):
    """
    Run word through the FST character by character.
    Returns "lemma|UPOS|feats" or None.
    """
    try:
        inp = pynini.accep(word, token_type="utf8")
        lattice = pynini.compose(inp, fsl)
        if lattice.num_states() == 0:
            return None
        return pynini.shortestpath(lattice).string(token_type="utf8")
    except Exception:
        return None


def get_state_path(word, fsl):
    """
    Trace the actual pynini states traversed when reading 'word' through the FST.
    Returns list of (state_id, input_char, output_char, next_state_id) or None.
    """
    try:
        inp = pynini.accep(word, token_type="utf8")
        lattice = pynini.compose(inp, fsl)
        if lattice.num_states() == 0:
            return None

        path_fst = pynini.shortestpath(lattice)
        path_fst.rmepsilon()

        arcs = []
        visited = set()
        state = path_fst.start()
        if state == -1:
            return None

        while True:
            if state in visited:
                break
            visited.add(state)

            arc_list = list(path_fst.arcs(state))
            if not arc_list:
                break

            arc = arc_list[0]

            # Skip epsilon arcs
            if arc.ilabel == 0:
                state = arc.nextstate
                continue

            try:
                in_char = chr(arc.ilabel) if arc.ilabel > 0 else "ε"
            except (ValueError, OverflowError):
                in_char = f"[{arc.ilabel}]"

            try:
                out_char = chr(arc.olabel) if arc.olabel > 0 else "ε"
            except (ValueError, OverflowError):
                out_char = f"[{arc.olabel}]"

            arcs.append((state, in_char, out_char, arc.nextstate))
            state = arc.nextstate

        return arcs if arcs else None

    except Exception:
        return None


def get_grapheme_path(word, fsl):
    """
    Groups raw codepoint arcs into Devanagari grapheme clusters.
    Returns list of (entry_state, grapheme_cluster, exit_state) or None.
    """
    raw_arcs = get_state_path(word, fsl)
    if raw_arcs is None:
        return None

    # Devanagari combining marks
    COMBINING = {
        '\u0900', '\u0901', '\u0902', '\u0903',  # anusvara, visarga
        '\u093A', '\u093B', '\u093C',              # nukta
        '\u093E', '\u093F', '\u0940',              # aa, i, ii vowel signs
        '\u0941', '\u0942', '\u0943', '\u0944',    # u, uu, ri, rri
        '\u0945', '\u0946', '\u0947', '\u0948',    # e vowel signs
        '\u0949', '\u094A', '\u094B', '\u094C',    # o vowel signs
        '\u094D',                                   # virama (halant)
        '\u094E', '\u094F',
        '\u0951', '\u0952', '\u0953', '\u0954',    # accent marks
        '\u0962', '\u0963',
    }

    clusters = []
    i = 0
    while i < len(raw_arcs):
        entry_state = raw_arcs[i][0]
        cluster_chars = raw_arcs[i][1]
        exit_state = raw_arcs[i][3]
        i += 1
        # Absorb following combining marks and virama+next consonant
        while i < len(raw_arcs):
            ch = raw_arcs[i][1]
            if ch in COMBINING:
                cluster_chars += ch
                exit_state = raw_arcs[i][3]
                i += 1
                # After virama (halant), absorb next base letter too
                if ch == '\u094D' and i < len(raw_arcs):
                    cluster_chars += raw_arcs[i][1]
                    exit_state = raw_arcs[i][3]
                    i += 1
            else:
                break
        clusters.append((entry_state, cluster_chars, exit_state))

    return clusters


if __name__ == "__main__":
    fsl = build_hindi_fsl()
    print("Hindi FSL successfully built.")
