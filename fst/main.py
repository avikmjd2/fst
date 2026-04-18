"""
main.py - English Morphological Analyzer
Entry point that builds the FST analyzer and provides
an interactive prompt for morphological analysis.

Usage:
    python main.py                     # interactive mode
    python main.py unhappiness         # single-word mode
"""

import sys
import random

from fst_builder import build_analyzer
from analyzer import analyze
from visualizer import format_analysis
from lexicon import get_all_surface_words


def _suggest(all_words):
    """Print 4 random words the analyzer knows about."""
    samples = random.sample(all_words, min(4, len(all_words)))
    print("  Word not recognized. Try one of these:")
    print("    " + ",  ".join(samples))


def main():
    print("=" * 60)
    print("  English Morphological Analyzer  (FST / pynini)")
    print("=" * 60)
    print("  Building FST transducers ...")

    analyzer_fst = build_analyzer()
    all_words = get_all_surface_words()

    print("  FST ready.\n")

    # ── Single-word mode (command-line argument) ────────────────
    if len(sys.argv) > 1:
        word = sys.argv[1].strip().lower()
        result = analyze(word, analyzer_fst)
        if result is None:
            _suggest(all_words)
        else:
            print(format_analysis(result))
        return

    # ── Interactive mode ────────────────────────────────────────
    while True:
        try:
            word = input("> Enter a word : ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not word or word in ("q", "quit", "exit"):
            print("Bye!")
            break

        result = analyze(word, analyzer_fst)
        if result is None:
            _suggest(all_words)
        else:
            print(format_analysis(result))
        print()


if __name__ == "__main__":
    main()

