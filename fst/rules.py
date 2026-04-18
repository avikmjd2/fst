"""
rules.py - Orthographic Rules
Implements the y -> i spelling change using pynini.cdrewrite.
When a root ending in -y is followed by a consonant-initial suffix,
the 'y' changes to 'i'  (e.g. happy + ness -> happiness).
"""

import pynini

# ── Alphabet ────────────────────────────────────────────────────────

LOWER = [chr(c) for c in range(ord('a'), ord('z') + 1)]
BOUNDARY = "+"

# sigma_star covers lowercase letters AND the boundary marker
_all_syms = LOWER + [BOUNDARY]
SIGMA_STAR = pynini.union(
    *[pynini.accep(ch) for ch in _all_syms]
).closure().optimize()

# ── Consonant set (used as right-context trigger) ───────────────────

CONSONANTS = pynini.union(
    *[pynini.accep(c) for c in "bcdfghjklmnpqrstvwxyz"]
)

# ── y → i  rule ────────────────────────────────────────────────────
# Context:  y  →  i  /  _ + C   (before a boundary then a consonant)
#
# tau   = cross("y","i")       — the rewrite
# lam   = ""                   — no left-context restriction
# rho   = BOUNDARY CONSONANT   — boundary followed by consonant
# sigma = SIGMA_STAR

Y_TO_I_RULE = pynini.cdrewrite(
    pynini.cross("y", "i"),       # tau  : mapping
    "",                            # lam  : left context  (any)
    pynini.accep(BOUNDARY) + CONSONANTS,  # rho  : right context
    SIGMA_STAR,                    # sigma: alphabet closure
).optimize()

# ── Boundary deletion rule ──────────────────────────────────────────
# After applying spelling rules, delete every '+' boundary marker.

DELETE_BOUNDARY = pynini.cdrewrite(
    pynini.cross(BOUNDARY, ""),    # delete boundary
    "",                            # left context  (any)
    "",                            # right context (any)
    SIGMA_STAR,                    # alphabet closure
).optimize()

# ── Combined rule pipeline ──────────────────────────────────────────
# First apply y→i, then strip boundaries.

RULES = (Y_TO_I_RULE @ DELETE_BOUNDARY).optimize()
