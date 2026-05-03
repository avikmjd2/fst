"""
lexicon.py - Morpheme Lexicon for MorphoChallenge format
Loads stems from stems.txt and defines suffix/prefix rules.
"""
import os

BOUNDARY = "+"
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Load stem dictionary from file ─────────────────────────────────
STEMS = {}  # stem -> POS tag (V, N, A, O, Q, P, B)

def _load_stems():
    path = os.path.join(_SCRIPT_DIR, 'stems.txt')
    if not os.path.isfile(path):
        return
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) == 2:
                STEMS[parts[0]] = parts[1]

_load_stems()

# ── Derivational suffixes: surface_suffix -> (strip, add_back, tag) ─
# For stripping: if word ends with surface_suffix, remove it, add add_back
DERIV_SUFFIXES = [
    # (surface ending, chars to strip, chars to restore, MorphoChallenge tag)
    ("fulness", 7, "ful", "ful_s ness_s"),
    ("lessly", 6, "less", "less_s ly_s"),
    ("ization", 7, "ize", "ize_s ation_s"),
    ("isation", 7, "ise", "ise_s ation_s"),
    ("ically", 6, "ic", "ical_s ly_s"),
    ("ically", 6, "", "ical_s ly_s"),
    ("iously", 6, "ious", "ous_s ly_s"),
    ("ously", 5, "ous", "ous_s ly_s"),
    ("iveness", 7, "ive", "ive_s ness_s"),
    ("iveness", 7, "", "ive_s ness_s"),
    ("ization", 7, "", "ize_s ation_s"),
    ("fulness", 7, "", "ful_s ness_s"),
    ("isation", 7, "", "ise_s ation_s"),
    ("lessness", 8, "", "less_s ness_s"),
    ("lessness", 8, "less", "less_s ness_s"),
    ("ness", 4, "", "ness_s"),
    ("ness", 4, "e", "ness_s"),
    ("ment", 4, "", "ment_s"),
    ("ment", 4, "e", "ment_s"),
    ("tion", 4, "te", "ion_s"),
    ("tion", 4, "t", "ion_s"),
    ("tion", 4, "", "ion_s"),
    ("sion", 4, "de", "ion_s"),
    ("sion", 4, "d", "ion_s"),
    ("sion", 4, "", "ion_s"),
    ("ation", 5, "ate", "ion_s"),
    ("ation", 5, "e", "ation_s"),
    ("ation", 5, "", "ation_s"),
    ("ution", 5, "ute", "ution_s"),
    ("ity", 3, "e", "ity_s"),
    ("ity", 3, "", "ity_s"),
    ("ity", 3, "ous", "ity_s"),
    ("able", 4, "e", "able_s"),
    ("able", 4, "", "able_s"),
    ("ible", 4, "e", "ible_s"),
    ("ible", 4, "", "ible_s"),
    ("ful", 3, "", "ful_s"),
    ("ful", 3, "e", "ful_s"),
    ("less", 4, "", "less_s"),
    ("less", 4, "e", "less_s"),
    ("ize", 3, "", "ize_s"),
    ("ize", 3, "e", "ize_s"),
    ("ise", 3, "", "ise_s"),
    ("ify", 3, "", "ify_s"),
    ("ify", 3, "y", "ify_s"),
    ("ist", 3, "", "ist_s"),
    ("ist", 3, "y", "ist_s"),
    ("ism", 3, "", "ism_s"),
    ("ism", 3, "y", "ism_s"),
    ("ous", 3, "", "ous_s"),
    ("ous", 3, "e", "ous_s"),
    ("ive", 3, "e", "ive_s"),
    ("ive", 3, "", "ive_s"),
    ("ent", 3, "", "ent_s"),
    ("ent", 3, "e", "ent_s"),
    ("ant", 3, "", "ant_s"),
    ("ant", 3, "e", "ant_s"),
    ("ence", 4, "ent", "ence_s"),
    ("ence", 4, "", "ence_s"),
    ("ance", 4, "ant", "ance_s"),
    ("ance", 4, "", "ance_s"),
    ("ency", 4, "ent", "ency_s"),
    ("ancy", 4, "ant", "ancy_s"),
    ("al", 2, "", "al_s"),
    ("al", 2, "e", "al_s"),
    ("ial", 3, "", "ial_s"),
    ("ical", 4, "", "ical_s"),
    ("ical", 4, "y", "ical_s"),
    ("ic", 2, "", "ic_s"),
    ("ic", 2, "y", "ic_s"),
    ("ly", 2, "", "ly_s"),
    ("ly", 2, "e", "ly_s"),
    ("ily", 3, "y", "ly_s"),
    ("ally", 4, "al", "ally_s"),
    ("ally", 4, "", "ally_s"),
    ("er", 2, "", "er_s"),
    ("er", 2, "e", "er_s"),
    ("or", 2, "", "or_s"),
    ("or", 2, "e", "or_s"),
    ("ee", 2, "e", "ee_s"),
    ("age", 3, "", "age_s"),
    ("age", 3, "e", "age_s"),
    ("ure", 3, "e", "ure_s"),
    ("ure", 3, "", "ure_s"),
    ("ary", 3, "", "ary_s"),
    ("ary", 3, "e", "ary_s"),
    ("ery", 3, "", "ery_s"),
    ("ory", 3, "e", "ory_s"),
    ("ory", 3, "", "ory_s"),
    ("ish", 3, "", "ish_s"),
    ("ish", 3, "e", "ish_s"),
    ("en", 2, "", "en_s"),
    ("ian", 3, "", "ian_s"),
    ("an", 2, "", "an_s"),
    ("ate", 3, "", "ate_s"),
    ("ate", 3, "e", "ate_s"),
    ("ette", 4, "", "ette_s"),
    ("ette", 4, "e", "ette_s"),
    ("let", 3, "", "let_s"),
    ("dom", 3, "", "dom_s"),
    ("ship", 4, "", "ship_s"),
    ("ward", 4, "", "ward_s"),
    ("some", 4, "", "some_s"),
    ("ster", 4, "", "ster_s"),
    ("y", 1, "", "y_s"),
    ("y", 1, "e", "y_s"),
    ("ed", 2, "", "ed_s"),
    ("ed", 2, "e", "ed_s"),
]

# ── Prefixes: (surface_prefix, MorphoChallenge tag) ─────────────────
PREFIXES = [
    ("anthropo", "anthropo_p"),
    ("over", "over_p"),
    ("under", "under_p"),
    ("inter", "inter_p"),
    ("trans", "trans_p"),
    ("cross", "cross_p"),
    ("photo", "photo_p"),
    ("hydro", "hydro_p"),
    ("turbo", "turbo_p"),
    ("quasi", "quasi_p"),
    ("tele", "tele_p"),
    ("self", "self_p"),
    ("with", "with_p"),
    ("vice", "vice_p"),
    ("anti", "anti_p"),
    ("semi", "semi_p"),
    ("non", "non_p"),
    ("mid", "mid_p"),
    ("out", "out_p"),
    ("mis", "mis_p"),
    ("mal", "mal_p"),
    ("pre", "pre_p"),
    ("dis", "dis_p"),
    ("sub", "sub_p"),
    ("com", "com_p"),
    ("con", "con_p"),
    ("col", "col_p"),
    ("un", "un_p"),
    ("re", "re_p"),
    ("de", "de_p"),
    ("im", "im_p"),
    ("in", "in_p"),
    ("em", "em_p"),
    ("ex", "ex_p"),
    ("be", "be_p"),
    ("bi", "bi_p"),
    ("ab", "ab_p"),
    ("ag", "ag_p"),
    ("an", "an_p"),
    ("co", "co_p"),
    ("a", "a_p"),
]

# ── Consonants ──────────────────────────────────────────────────────
CONSONANTS = set("bcdfghjklmnpqrstvwxyz")
VOWELS = set("aeiou")
SIBILANTS = {"s", "x", "z", "sh", "ch"}


def get_tag(morpheme, position):
    """Return the grammatical tag for a morpheme given its position."""
    if position == "prefix":
        for pfx, tag in PREFIXES:
            if morpheme == pfx:
                return tag
        return "PREFIX"
    elif position == "root":
        return "ROOT"
    elif position == "suffix":
        return "SUFF"
    return "UNK"


def lookup_stem(word):
    """Look up a word in the stem dictionary. Returns POS or None."""
    return STEMS.get(word)
