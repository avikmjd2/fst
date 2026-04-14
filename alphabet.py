"""
Shared alphabet and symbol definitions for the English morphological FST.
"""
import pynini

# Morpheme boundary marker (used in intermediate forms between stem and suffix)
BOUNDARY = "^"

# Character sets
LOWERCASE = [chr(i) for i in range(ord('a'), ord('z') + 1)]
VOWELS = list("aeiou")
CONSONANTS = list("bcdfghjklmnpqrstvwxyz")

# FST building blocks
VOWEL = pynini.union(*VOWELS)
CONSONANT = pynini.union(*CONSONANTS)

# Sigma star for spelling rules (operates on intermediate forms: letters + boundary)
SIGMA_STAR = pynini.union(*LOWERCASE, BOUNDARY).closure().optimize()
