"""
Spelling Rules: context-dependent rewrite rules (cdrewrite) that handle
orthographic changes at morpheme boundaries.

Rules are applied as a cascade (composed in order):
  1. y -> ie  before ^s   (after consonant)   : fly^s  -> flie^s  -> flies
  2. y -> i   before ^V   (after consonant)   : carry^ed -> carri^ed -> carried
  3. e-deletion before ^V (after consonant)   : hope^ing -> hop^ing -> hoping
  4. e-insertion after sibilant before ^s      : watch^s  -> watch^es -> watches
  5. boundary deletion: ^ -> ""               : dog^s -> dogs
"""
import pynini
from alphabet import SIGMA_STAR, VOWEL, CONSONANT, BOUNDARY


def _build_sibilant():
    """Characters/digraphs after which -es is used instead of -s."""
    return pynini.union(
        pynini.accep("s"),
        pynini.accep("x"),
        pynini.accep("z"),
        pynini.accep("s") + pynini.accep("h"),  # sh
        pynini.accep("c") + pynini.accep("h"),  # ch
    )


def build_y_to_ie_rule():
    """
    Rule 1: y -> ie before ^s (after a consonant)
    Handles: fly^s -> flie^s, carry^s -> carrie^s
    Does NOT fire when y is preceded by a vowel: play^s stays play^s
    """
    return pynini.cdrewrite(
        pynini.cross("y", "ie"),
        CONSONANT,                                    # left context: consonant
        pynini.accep(BOUNDARY) + pynini.accep("s"),   # right context: ^s
        SIGMA_STAR,
    ).optimize()


def build_y_to_i_rule():
    """
    Rule 2: y -> i before ^ + non-i-suffix (after a consonant)
    Handles: carry^ed -> carri^ed, happy^er -> happi^er, happy^ly -> happi^ly
    Does NOT fire before -ing (suffix starts with i): carry^ing stays
    Does NOT fire when y preceded by vowel: play^ed stays
    """
    # Right context: boundary followed by any letter except 'i'
    non_i_letters = [c for c in "abcdefghjklmnopqrstuvwxyz"]  # all lowercase except i
    non_i = pynini.union(*non_i_letters)

    return pynini.cdrewrite(
        pynini.cross("y", "i"),
        CONSONANT,                                     # left context: consonant
        pynini.accep(BOUNDARY) + non_i,                # right context: ^ + non-i
        SIGMA_STAR,
    ).optimize()


def build_e_deletion_rule():
    """
    Rule 3: delete silent 'e' before ^ + vowel-initial suffix (after a consonant)
    Handles: hope^ing -> hop^ing, hope^ed -> hop^ed, like^able -> lik^able
    Does NOT fire when e preceded by vowel: see^ing stays (ee preserved)
    """
    return pynini.cdrewrite(
        pynini.cross("e", ""),
        CONSONANT,                                     # left context: consonant
        pynini.accep(BOUNDARY) + VOWEL,                # right context: ^ + vowel
        SIGMA_STAR,
    ).optimize()


def build_e_insertion_rule():
    """
    Rule 4: insert 'e' after sibilant before ^s
    Handles: watch^s -> watch^es, box^s -> box^es, bus^s -> bus^es
    """
    sibilant = _build_sibilant()

    return pynini.cdrewrite(
        pynini.cross("", "e"),
        sibilant + pynini.accep(BOUNDARY),             # left context: sibilant + ^
        pynini.accep("s"),                             # right context: s
        SIGMA_STAR,
    ).optimize()


def build_boundary_deletion_rule():
    """
    Rule 5: delete all remaining boundary markers
    Handles: dog^s -> dogs, walk^ed -> walked
    """
    return pynini.cdrewrite(
        pynini.cross(BOUNDARY, ""),
        "",   # no left context
        "",   # no right context
        SIGMA_STAR,
    ).optimize()


def build_spelling_rules():
    """
    Build the complete spelling rule cascade.
    Rules are composed in order (left to right = first applied to last):
      y->ie | y->i | e-deletion | e-insertion | boundary-deletion
    """
    r1 = build_y_to_ie_rule()
    r2 = build_y_to_i_rule()
    r3 = build_e_deletion_rule()
    r4 = build_e_insertion_rule()
    r5 = build_boundary_deletion_rule()

    print("  [spelling] y->ie rule built")
    print("  [spelling] y->i rule built")
    print("  [spelling] e-deletion rule built")
    print("  [spelling] e-insertion rule built")
    print("  [spelling] boundary deletion rule built")

    # Compose cascade: input flows through r1, then r2, then r3, then r4, then r5
    cascade = (r1 @ r2 @ r3 @ r4 @ r5).optimize()
    print("  [spelling] Cascade composed and optimized")
    return cascade
