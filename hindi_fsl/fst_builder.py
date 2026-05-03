"""
Builds the FST/FSL for Hindi Morphological Analysis using Pynini.
"""
import pynini
from lexicon import VOCABULARY

def build_hindi_fsl():
    """
    Builds a finite state lexicon (transducer) that accepts valid Hindi words.
    In this simplified demo, it accepts the words from the vocabulary and 
    maps them to themselves as a validation step.
    """
    mapping = [(word, word) for word in VOCABULARY.keys()]
    
    # Create the transducer from the string map
    # A transducer mapping surface form to surface form just validates it's in the lexicon
    fsl = pynini.string_map(mapping)
    
    # Optimize
    fsl.optimize()
    return fsl

def is_valid_word(word, fsl):
    """
    Checks if a word is in the FSL.
    """
    try:
        # Compose word with FSL. If valid, result is not empty.
        word_fst = pynini.accep(word)
        result = pynini.compose(word_fst, fsl)
        return result.num_states() > 0
    except Exception:
        return False

if __name__ == "__main__":
    fsl = build_hindi_fsl()
    print("Hindi FSL successfully built.")
