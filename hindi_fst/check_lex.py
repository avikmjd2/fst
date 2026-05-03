import sys
sys.path.insert(0, '.')
from lexicon import VOCABULARY
words = list(VOCABULARY.keys())
print('Total words:', len(words))
print('Sample:', words[:10])
