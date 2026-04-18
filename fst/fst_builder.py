"""
fst_builder.py - FST Construction
Builds the morphological generator (lexical -> surface) and
the analyzer (surface -> lexical) from the lexicon and rules.
"""

import pynini

from lexicon import VALID_WORDS, BOUNDARY, lexical_form
from rules import RULES


def build_generator():
    """
    Build a transducer that maps every valid lexical form
    (e.g. "un+happy+ness") to its surface form (e.g. "unhappiness").

    The transducer is the union of all valid word acceptors
    composed with the orthographic rule pipeline.
    """
    word_acceptors = []
    for prefix, root, suffix in VALID_WORDS:
        lex = lexical_form(prefix, root, suffix)
        word_acceptors.append(pynini.accep(lex))

    lexicon_fst = pynini.union(*word_acceptors).optimize()

    # Compose lexicon with rules: lexical -> surface
    generator = (lexicon_fst @ RULES).optimize()
    return generator


def build_analyzer():
    """
    Build the analyzer by inverting the generator.
    Maps surface forms (e.g. "unhappiness") -> lexical forms ("un+happy+ness").
    """
    generator = build_generator()
    analyzer = pynini.invert(generator).optimize()
    return analyzer
