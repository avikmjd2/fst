"""
fst_builder.py — Bengali Morphological FST

Builds a TRUE character-level Finite State Transducer using pynini.

Architecture:
    - Each unique path through the FST = one word in the lexicon
    - Each arc = one Unicode codepoint
    - Arc label: input char (surface form)
    - Arc output: morphological tag emitted at that step
    - Final states: emit the analysis (lemma|UPOS|feats)

State traversal example for a word:
    q0 -[ত]-> q1 -[ু]-> q2 -[ম]-> q3 -[ি]-> q4(FINAL)
    Output: তুমি|PRON|Case=Nom|Number=Sing|Person=2|PronType=Prs
"""
import pynini
from pynini.lib import utf8
from lexicon import VOCABULARY


def build_bengali_fsl():
    """
    Builds a character-level Bengali FST.
    
    Maps: surface_word (char by char) -> "lemma|UPOS|feats"
    
    Internally pynini represents this as a WFST where:
      - States are numbered integers
      - Arcs carry (input_label, output_label, next_state)
      - Final states are marked with final weight
    """
    pairs = []
    for word, info in VOCABULARY.items():
        lemma = info["lemma"]
        upos  = info["upos"]
        feats = info["feats"]
        analysis = f"{lemma}|{upos}|{feats}"
        pairs.append((word, analysis))

    # pynini.string_map builds the minimal FST from (surface, analysis) pairs
    # Each character becomes an arc in the transducer
    fsl = pynini.string_map(pairs, input_token_type="utf8", output_token_type="utf8")
    fsl.optimize()  # minimize state count
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
    Returns the analysis string "lemma|UPOS|feats" or None.
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
    
    Returns:
        list of (state_id, input_char, output_char, next_state_id)
        or None if word not accepted.
    
    How it works:
        1. Build a linear FSA for the input word (one arc per codepoint)
        2. Compose with the FST to get the output lattice
        3. Walk arcs of the composed lattice to extract the path
    """
    try:
        # Build character-by-character input acceptor
        inp = pynini.accep(word, token_type="utf8")
        lattice = pynini.compose(inp, fsl)
        if lattice.num_states() == 0:
            return None

        # Get shortest path through the lattice
        path_fst = pynini.shortestpath(lattice)
        path_fst.rmepsilon()

        # Walk arcs from start state
        arcs = []
        # Get the symbol table for decoding
        # We need to map integer labels back to UTF-8 characters
        # pynini uses UTF-8 byte-level or codepoint-level labels
        
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

            arc = arc_list[0]  # shortest path has one arc per state

            # Skip epsilon arcs (ilabel == 0) — these are internal pynini arcs
            if arc.ilabel == 0:
                state = arc.nextstate
                continue

            # Decode input label (UTF-8 codepoint)
            try:
                in_char = chr(arc.ilabel) if arc.ilabel > 0 else "ε"
            except (ValueError, OverflowError):
                in_char = f"[{arc.ilabel}]"

            # Decode output label
            try:
                out_char = chr(arc.olabel) if arc.olabel > 0 else "ε"
            except (ValueError, OverflowError):
                out_char = f"[{arc.olabel}]"

            arcs.append((state, in_char, out_char, arc.nextstate))
            state = arc.nextstate

        return arcs if arcs else None

    except Exception as e:
        return None


def get_grapheme_path(word, fsl):
    """
    Higher-level: returns the traversal as grapheme clusters (not raw codepoints).
    
    Since Bengali characters = multi-byte UTF-8, pynini works at codepoint level.
    This function groups the raw codepoint arcs back into grapheme clusters
    to give a linguistically meaningful path.
    
    Returns:
        list of (entry_state, grapheme_cluster, exit_state)
        or None if word not accepted.
    """
    raw_arcs = get_state_path(word, fsl)
    if raw_arcs is None:
        return None

    # Group consecutive codepoints into grapheme clusters
    # A Bengali grapheme = base letter + optional combining marks
    COMBINING = {
        '\u09BC', '\u09BE', '\u09BF', '\u09C0', '\u09C1', '\u09C2',
        '\u09C3', '\u09C4', '\u09C7', '\u09C8', '\u09CB', '\u09CC',
        '\u09CD', '\u09D7', '\u09E2', '\u09E3',
    }

    clusters = []
    i = 0
    while i < len(raw_arcs):
        entry_state = raw_arcs[i][0]
        cluster_chars = raw_arcs[i][1]
        exit_state = raw_arcs[i][3]
        i += 1
        # Absorb following combining marks and hasanta+next
        while i < len(raw_arcs):
            ch = raw_arcs[i][1]
            if ch in COMBINING:
                cluster_chars += ch
                exit_state = raw_arcs[i][3]
                i += 1
                # After hasanta, absorb next base letter too
                if ch == '\u09CD' and i < len(raw_arcs):
                    cluster_chars += raw_arcs[i][1]
                    exit_state = raw_arcs[i][3]
                    i += 1
            else:
                break
        clusters.append((entry_state, cluster_chars, exit_state))

    return clusters
