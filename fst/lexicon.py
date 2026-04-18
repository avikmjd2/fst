"""
lexicon.py - Morpheme Lexicon
Defines prefixes, roots, suffixes with their grammatical tags,
and the valid morpheme combinations for the analyzer.
"""

# ── Morpheme Dictionaries ──────────────────────────────────────────

PREFIXES = {
    "un":  "NEG",
    "re":  "REPEAT",
    "dis": "NEG",
    "pre": "BEFORE",
}

ROOTS = {
    "happy": "ADJ",
    "kind":  "ADJ",
    "fair":  "ADJ",
    "play":  "VERB",
    "care":  "VERB",
    "hope":  "VERB",
    "use":   "VERB",
    "do":    "VERB",
    "like":  "VERB",
    "grace": "NOUN",
}

SUFFIXES = {
    "ness":  "SUFF",
    "ly":    "SUFF",
    "er":    "SUFF",
    "est":   "SUFF",
    "ful":   "SUFF",
    "less":  "SUFF",
    "ing":   "SUFF",
    "ed":    "SUFF",
    "able":  "SUFF",
    "ment":  "SUFF",
}

# Morpheme boundary symbol used internally
BOUNDARY = "+"

# ── Valid Combinations ──────────────────────────────────────────────
# Each entry: (prefix_or_None, root, suffix_or_None)

VALID_WORDS = [
    # happy family
    (None,  "happy", None),
    (None,  "happy", "ness"),
    (None,  "happy", "ly"),
    (None,  "happy", "er"),
    (None,  "happy", "est"),
    ("un",  "happy", None),
    ("un",  "happy", "ness"),
    ("un",  "happy", "ly"),

    # kind family
    (None,  "kind",  None),
    (None,  "kind",  "ness"),
    (None,  "kind",  "ly"),
    (None,  "kind",  "er"),
    (None,  "kind",  "est"),
    ("un",  "kind",  None),
    ("un",  "kind",  "ness"),
    ("un",  "kind",  "ly"),

    # fair family
    (None,  "fair",  None),
    (None,  "fair",  "ness"),
    (None,  "fair",  "ly"),
    (None,  "fair",  "er"),
    (None,  "fair",  "est"),
    ("un",  "fair",  None),
    ("un",  "fair",  "ness"),
    ("un",  "fair",  "ly"),

    # play family
    (None,  "play",  None),
    (None,  "play",  "ful"),
    (None,  "play",  "er"),
    (None,  "play",  "ing"),
    (None,  "play",  "ed"),
    ("re",  "play",  None),
    ("re",  "play",  "ing"),
    ("re",  "play",  "ed"),

    # care family
    (None,  "care",  None),
    (None,  "care",  "ful"),
    (None,  "care",  "less"),
    (None,  "care",  "er"),

    # hope family
    (None,  "hope",  None),
    (None,  "hope",  "ful"),
    (None,  "hope",  "less"),

    # use family
    (None,  "use",   None),
    (None,  "use",   "ful"),
    (None,  "use",   "less"),
    (None,  "use",   "able"),
    ("re",  "use",   None),
    ("re",  "use",   "able"),

    # do family
    (None,  "do",    None),
    (None,  "do",    "er"),
    (None,  "do",    "ing"),
    ("un",  "do",    None),
    ("un",  "do",    "ing"),
    ("re",  "do",    None),
    ("re",  "do",    "ing"),

    # like family
    (None,  "like",  None),
    (None,  "like",  "ly"),
    (None,  "like",  "able"),
    ("un",  "like",  "ly"),
    ("dis", "like",  None),

    # grace family
    (None,  "grace", None),
    (None,  "grace", "ful"),
    (None,  "grace", "less"),
    ("dis", "grace", None),
    ("dis", "grace", "ful"),
]


def get_tag(morpheme, position):
    """Return the grammatical tag for a morpheme given its position."""
    if position == "prefix":
        return PREFIXES.get(morpheme, "PREFIX")
    elif position == "root":
        return "ROOT"
    elif position == "suffix":
        return SUFFIXES.get(morpheme, "SUFF")
    return "UNK"


def lexical_form(prefix, root, suffix):
    """Build the boundary-delimited lexical form: e.g. 'un+happy+ness'."""
    parts = []
    if prefix:
        parts.append(prefix)
    parts.append(root)
    if suffix:
        parts.append(suffix)
    return BOUNDARY.join(parts)


# Consonant letters used for the naive y→i surface-form prediction
_CONSONANTS = set("bcdfghjklmnpqrstvwxyz")


def get_all_surface_words():
    """
    Return a sorted list of every valid surface-form word the
    analyzer can recognize (e.g. 'unhappiness', 'kindness', ...).

    Applies the y→i rule naively so the list matches what the
    pynini transducer would accept.
    """
    words = set()
    for prefix, root, suffix in VALID_WORDS:
        # Start with the raw concatenation
        surface_root = root
        if suffix and root.endswith("y") and suffix[0] in _CONSONANTS:
            surface_root = root[:-1] + "i"
        surface = (prefix or "") + surface_root + (suffix or "")
        words.add(surface)
    return sorted(words)
