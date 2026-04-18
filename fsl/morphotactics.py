"""
Morphotactics FST: defines which suffixes/prefixes can attach to which stems.

Maps analysis strings (upper tape) to intermediate forms with boundary markers (lower tape).
Example: "walk+V;PST" (upper) -> "walk^ed" (lower)

The boundary marker '^' is later consumed by spelling rules.
"""
import pynini
from lexicon import (
    ALL_REGULAR_NOUNS, REGULAR_VERBS,
    SHORT_ADJECTIVES, E_ADJECTIVES, Y_ADJECTIVES, LONG_ADJECTIVES,
    UN_ADJECTIVES, RE_VERBS, NESS_ADJECTIVES, LY_ADJECTIVES,
)
from irregulars import ALL_IRREGULARS


def _identity_map(stems):
    """Create an identity string map (stem -> stem) for a list of stems."""
    unique = sorted(set(stems))
    return pynini.string_map([(s, s) for s in unique]).optimize()


def build_noun_morphotactics():
    """
    Regular noun inflection:
      stem+N;SG -> stem       (singular = base form)
      stem+N;PL -> stem^s     (plural, spelling rules handle sibilant/y cases)
    """
    noun_stems = _identity_map(ALL_REGULAR_NOUNS)
    suffixes = pynini.union(
        pynini.cross("+N;SG", ""),
        pynini.cross("+N;PL", "^s"),
    )
    return (noun_stems + suffixes).optimize()


def build_verb_morphotactics():
    """
    Regular verb inflection:
      stem+V;NFIN        -> stem         (base / infinitive)
      stem+V;PST         -> stem^ed      (simple past)
      stem+V;PRS;3;SG    -> stem^s       (3rd person singular present)
      stem+V;V.PTCP;PRS  -> stem^ing     (present participle / gerund)
      stem+V;V.PTCP;PST  -> stem^ed      (past participle, regular = past)
    """
    # Filter out verbs that are in the irregulars list (by lemma)
    irregular_lemmas = set()
    for analysis, _ in ALL_IRREGULARS:
        if "+V;" in analysis:
            lemma = analysis.split("+")[0]
            irregular_lemmas.add(lemma)

    regular_stems = [v for v in REGULAR_VERBS if v not in irregular_lemmas]
    verb_stems = _identity_map(regular_stems)

    suffixes = pynini.union(
        pynini.cross("+V;NFIN", ""),
        pynini.cross("+V;PST", "^ed"),
        pynini.cross("+V;PRS;3;SG", "^s"),
        pynini.cross("+V;V.PTCP;PRS", "^ing"),
        pynini.cross("+V;V.PTCP;PST", "^ed"),
    )
    return (verb_stems + suffixes).optimize()


def build_adjective_morphotactics():
    """
    Adjective inflection:
      Short adjectives:  stem+ADJ -> stem, stem+ADJ;CMPR -> stem^er, stem+ADJ;SPRL -> stem^est
      E-ending adjectives: same pattern (e-deletion rule handles hope^er -> hoper)
      Y-ending adjectives: same pattern (y->i rule handles happy^er -> happier)
      Long adjectives: only base form (comparative uses 'more/most' analytically)
    """
    # Filter out adjectives that appear in irregulars
    irregular_lemmas = set()
    for analysis, _ in ALL_IRREGULARS:
        if "+ADJ" in analysis:
            lemma = analysis.split("+")[0]
            irregular_lemmas.add(lemma)

    short_stems = [a for a in SHORT_ADJECTIVES if a not in irregular_lemmas]
    e_stems = [a for a in E_ADJECTIVES if a not in irregular_lemmas]
    y_stems = [a for a in Y_ADJECTIVES if a not in irregular_lemmas]
    long_stems = [a for a in LONG_ADJECTIVES if a not in irregular_lemmas]

    inflecting_stems = _identity_map(short_stems + e_stems + y_stems)
    long_adj_stems = _identity_map(long_stems)

    inflecting_suffixes = pynini.union(
        pynini.cross("+ADJ", ""),
        pynini.cross("+ADJ;CMPR", "^er"),
        pynini.cross("+ADJ;SPRL", "^est"),
    )

    base_only = pynini.cross("+ADJ", "")

    inflecting_fst = (inflecting_stems + inflecting_suffixes).optimize()
    long_fst = (long_adj_stems + base_only).optimize()

    return pynini.union(inflecting_fst, long_fst).optimize()


def build_derivational_morphotactics():
    """
    Derivational morphology (prefixes and suffixes that change POS or meaning):
      un- + ADJ  -> ADJ            (unhappy, unfair)
      re- + V    -> V              (rebuild, redo)
      ADJ + -ness -> N             (happiness, kindness)
      ADJ + -ly   -> ADV           (happily, kindly)
    """
    parts = []

    # --- un- prefix (un + adjective base form) ---
    un_adj_stems = _identity_map(UN_ADJECTIVES)
    un_prefix = pynini.cross("un+", "un")  # upper: "un+" -> lower: "un"
    un_suffix = pynini.cross("+ADJ", "")
    un_fst = (un_prefix + un_adj_stems + un_suffix).optimize()
    parts.append(un_fst)

    # --- re- prefix (re + verb base form) ---
    re_verb_stems = _identity_map(RE_VERBS)
    re_prefix = pynini.cross("re+", "re")
    re_suffix = pynini.cross("+V;NFIN", "")
    re_fst = (re_prefix + re_verb_stems + re_suffix).optimize()
    parts.append(re_fst)

    # --- -ness suffix (adjective -> noun) ---
    ness_stems = _identity_map(NESS_ADJECTIVES)
    ness_tag = pynini.cross("+N;NESS", "^ness")
    ness_fst = (ness_stems + ness_tag).optimize()
    parts.append(ness_fst)

    # --- -ly suffix (adjective -> adverb) ---
    ly_stems = _identity_map(LY_ADJECTIVES)
    ly_tag = pynini.cross("+ADV;LY", "^ly")
    ly_fst = (ly_stems + ly_tag).optimize()
    parts.append(ly_fst)

    return pynini.union(*parts).optimize()


def build_morphotactics():
    """
    Build the complete morphotactics FST by unioning all parts.
    Upper tape: analysis string (e.g., "walk+V;PST")
    Lower tape: intermediate form with boundaries (e.g., "walk^ed")
    """
    nouns = build_noun_morphotactics()
    verbs = build_verb_morphotactics()
    adjectives = build_adjective_morphotactics()
    derivational = build_derivational_morphotactics()

    print("  [morphotactics] Nouns built")
    print("  [morphotactics] Verbs built")
    print("  [morphotactics] Adjectives built")
    print("  [morphotactics] Derivational rules built")

    return pynini.union(nouns, verbs, adjectives, derivational).optimize()
