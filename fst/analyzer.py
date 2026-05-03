"""
analyzer.py - Morphological Analysis Engine
Heuristic rule-based analyzer producing MorphoChallenge format output.
Priority: inflectional > base form > derivational > prefix+deriv > compound
"""
from lexicon import STEMS, DERIV_SUFFIXES, PREFIXES, CONSONANTS, VOWELS


class AnalysisResult:
    """Holds the results of a morphological analysis."""
    def __init__(self, surface, lexical, morphemes=None, arc_path=None, y_to_i_index=-1):
        self.surface = surface
        self.lexical = lexical
        self.morphemes = morphemes or []
        self.arc_path = arc_path or []
        self.y_to_i_index = y_to_i_index


def _lookup(word):
    return STEMS.get(word)


def _strip_inflection(word):
    """Try stripping inflectional suffixes. Returns list of (stem, infl_tag)."""
    cands = []
    # Genitive
    if word.endswith("'s"):
        cands.append((word[:-2], "+GEN"))
    if word.endswith("s'"):
        cands.append((word[:-2], "+PL +GEN"))
    if word.endswith("'"):
        w2 = word[:-1]
        if w2.endswith("s"):
            cands.append((w2[:-1], "+PL +GEN"))
            cands.append((w2, "+GEN"))
        else:
            cands.append((w2, "+GEN"))

    # -iest/-ier (y-adj)
    if word.endswith("iest"):
        cands.append((word[:-4] + "y", "+SUP"))
    if word.endswith("ier") and len(word) > 4:
        b = word[:-3] + "y"
        p = _lookup(b)
        if p == 'A':
            cands.append((b, "+CMP"))

    # -est (superlative)
    if word.endswith("est") and len(word) > 4:
        cands.append((word[:-3], "+SUP"))
        cands.append((word[:-2], "+SUP"))  # e-ending
        if len(word) > 5 and word[-4] == word[-5]:  # doubled
            cands.append((word[:-4], "+SUP"))

    # -er: CMP for adjectives, er_s for verbs/nouns
    if word.endswith("er") and len(word) > 3 and not word.endswith("ier"):
        bases_er = [word[:-2], word[:-1]]  # base, e-ending
        if len(word) > 4 and word[-3] == word[-4]:  # doubled
            bases_er.append(word[:-3])
        for b in bases_er:
            p = _lookup(b)
            if p == 'A':
                cands.append((b, "+CMP"))
            elif p in ('V', 'N'):
                pass  # handled as er_s in derivational
            else:
                cands.append((b, "+CMP"))  # default to CMP

    # -ied -> y + PAST
    if word.endswith("ied"):
        cands.append((word[:-3] + "y", "+PAST"))
    # -ies -> y + PL/3SG
    if word.endswith("ies") and len(word) > 4:
        cands.append((word[:-3] + "y", "+PL"))
        cands.append((word[:-3] + "y", "+3SG"))

    # -ying -> y + PCP1
    if word.endswith("ying"):
        cands.append((word[:-3], "+PCP1"))

    # -ing (PCP1)
    if word.endswith("ing") and len(word) > 4 and not word.endswith("ying"):
        base = word[:-3]
        cands.append((base, "+PCP1"))
        cands.append((base + "e", "+PCP1"))
        if len(base) >= 2 and base[-1] == base[-2]:
            cands.append((base[:-1], "+PCP1"))

    # -ed (PAST) - not -ied which is handled above
    if word.endswith("ed") and len(word) > 3 and not word.endswith("ied"):
        base = word[:-2]
        cands.append((base, "+PAST"))
        cands.append((base + "e", "+PAST"))
        if len(base) >= 2 and base[-1] == base[-2]:
            cands.append((base[:-1], "+PAST"))

    # -es (PL/3SG)
    if word.endswith("es") and len(word) > 3 and not word.endswith("ies"):
        base = word[:-2]
        cands.append((base, "+PL"))
        cands.append((base, "+3SG"))
        cands.append((base + "e", "+PL"))
        cands.append((base + "e", "+3SG"))

    # -s (PL/3SG) - not -es, -ss
    if word.endswith("s") and not word.endswith(("es", "ss", "'s", "s'")) and len(word) > 2:
        base = word[:-1]
        cands.append((base, "+PL"))
        cands.append((base, "+3SG"))

    return cands


def _try_prefix(word):
    results = []
    for pfx, tag in PREFIXES:
        if word.startswith(pfx) and len(word) > len(pfx) + 1:
            results.append((word[len(pfx):], tag))
    return results


def _try_deriv_suffix(word):
    results = []
    for surf_end, strip_len, restore, tag in DERIV_SUFFIXES:
        if word.endswith(surf_end) and len(word) > strip_len + 1:
            base = word[:-strip_len] + restore
            if len(base) >= 2:
                results.append((base, tag))
    return results


def _try_compound(word):
    results = []
    for i in range(3, len(word) - 2):
        left, right = word[:i], word[i:]
        lpos = _lookup(left)
        rpos = _lookup(right)
        if lpos and rpos:
            results.append((f"{left}_{lpos} {right}_{rpos}", 50))
    return results


def _fmt(stem, pos):
    return f"{stem}_{pos}"


def analyze(word, analyzer_fst=None):
    word = word.strip().lower()
    if not word:
        return None
    best = _analyze_word(word)
    if best is None:
        return None
    return AnalysisResult(surface=word, lexical=best)


def _analyze_word(word):
    results = []  # (analysis_string, priority) - lower priority = better

    # === PRIORITY 0: Direct lookup (base form) ===
    pos = _lookup(word)
    if pos:
        results.append((_fmt(word, pos), 5))

    # === PRIORITY 1: Inflectional suffixes (HIGHEST for matching) ===
    for stem, infl in _strip_inflection(word):
        p = _lookup(stem)
        if p:
            results.append((f"{_fmt(stem, p)} {infl}", 1))

        # prefix + stem + inflection
        for rest, ptag in _try_prefix(stem):
            rp = _lookup(rest)
            if rp:
                results.append((f"{ptag} {_fmt(rest, rp)} {infl}", 10))

        # stem + deriv_suffix + inflection (the -ed after deriv should be +PAST)
        for dstem, dtag in _try_deriv_suffix(stem):
            dp = _lookup(dstem)
            if dp:
                results.append((f"{_fmt(dstem, dp)} {dtag} {infl}", 8))
            # prefix + deriv + infl
            for rest2, ptag2 in _try_prefix(dstem):
                rp2 = _lookup(rest2)
                if rp2:
                    results.append((f"{ptag2} {_fmt(rest2, rp2)} {dtag} {infl}", 12))
            # nested deriv + infl
            for dstem2, dtag2 in _try_deriv_suffix(dstem):
                dp2 = _lookup(dstem2)
                if dp2:
                    results.append((f"{_fmt(dstem2, dp2)} {dtag2} {dtag} {infl}", 20))

    # === PRIORITY 2: Derivational suffixes only ===
    for dstem, dtag in _try_deriv_suffix(word):
        dp = _lookup(dstem)
        if dp:
            results.append((f"{_fmt(dstem, dp)} {dtag}", 10))
        # prefix + deriv
        for rest, ptag in _try_prefix(dstem):
            rp = _lookup(rest)
            if rp:
                results.append((f"{ptag} {_fmt(rest, rp)} {dtag}", 15))
        # nested deriv
        for dstem2, dtag2 in _try_deriv_suffix(dstem):
            dp2 = _lookup(dstem2)
            if dp2:
                results.append((f"{_fmt(dstem2, dp2)} {dtag2} {dtag}", 15))
            for rest3, ptag3 in _try_prefix(dstem2):
                rp3 = _lookup(rest3)
                if rp3:
                    results.append((f"{ptag3} {_fmt(rest3, rp3)} {dtag2} {dtag}", 20))
            # triple nested deriv
            for dstem3, dtag3 in _try_deriv_suffix(dstem2):
                dp3 = _lookup(dstem3)
                if dp3:
                    results.append((f"{_fmt(dstem3, dp3)} {dtag3} {dtag2} {dtag}", 20))

    # === PRIORITY 3: Prefixes only ===
    for rest, ptag in _try_prefix(word):
        rp = _lookup(rest)
        if rp:
            results.append((f"{ptag} {_fmt(rest, rp)}", 10))
        # prefix + inflection
        for stem2, infl2 in _strip_inflection(rest):
            rp2 = _lookup(stem2)
            if rp2:
                results.append((f"{ptag} {_fmt(stem2, rp2)} {infl2}", 12))
        # prefix + deriv
        for dstem3, dtag3 in _try_deriv_suffix(rest):
            dp3 = _lookup(dstem3)
            if dp3:
                results.append((f"{ptag} {_fmt(dstem3, dp3)} {dtag3}", 15))

    # === PRIORITY 4: Compounds ===
    for comp, score in _try_compound(word):
        results.append((comp, score))
    # compound + inflection
    for stem_c, infl_c in _strip_inflection(word):
        for comp, score in _try_compound(stem_c):
            results.append((f"{comp} {infl_c}", score + 1))

    if not results:
        return None

    # Sort: lower priority number wins, then shorter string
    results.sort(key=lambda x: (x[1], len(x[0])))
    return results[0][0]
