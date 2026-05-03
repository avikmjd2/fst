import sys
sys.path.insert(0, '.')
from analyzer import _analyze_word
words = ['walking', 'unhappiness', 'happily', 'unlucky', 'unkindness', 'kindness', 'helpful', 'running', 'talked']
for w in words:
    r = _analyze_word(w)
    print(f"{w:20s} -> {r}")
