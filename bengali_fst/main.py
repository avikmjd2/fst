"""
Main CLI for Bengali Morphological Analyzer (FSL)

Usage:
    python main.py                      # interactive mode
    python main.py তুমি                 # single word — FST state path
    python main.py "আমি ভালো আছি"     # sentence — CoNLL-U output
"""
import sys
from fst_builder import build_bengali_fsl, analyze_word_fst, get_grapheme_path
from analyzer import analyze_sentence, generate_conllu_line
from lexicon import VOCABULARY
from visualizer import format_analysis


def analyze_single_word(word, fsl):
    """Show FST state traversal + morphological analysis for one word."""

    if word in VOCABULARY:
        # Word is in lexicon — get real pynini state path
        gpath = get_grapheme_path(word, fsl)
        print(format_analysis(
            word,
            lexicon_entry=VOCABULARY[word],
            heuristic=False,
            grapheme_path=gpath
        ))

    else:
        # Try FST transducer
        fst_result = analyze_word_fst(word, fsl)
        if fst_result:
            parts = fst_result.split("|")
            entry = {
                "lemma": parts[0] if len(parts) > 0 else word,
                "upos":  parts[1] if len(parts) > 1 else "?",
                "feats": parts[2] if len(parts) > 2 else "_",
            }
            gpath = get_grapheme_path(word, fsl)
            print(format_analysis(
                word,
                lexicon_entry=entry,
                heuristic=False,
                grapheme_path=gpath
            ))

        else:
            # Heuristic fallback — no real FST path exists
            conllu = generate_conllu_line(1, word)
            cols = conllu.split("\t")
            entry = {
                "lemma": cols[2] if len(cols) > 2 else word,
                "upos":  cols[3] if len(cols) > 3 else "NOUN",
                "feats": cols[5] if len(cols) > 5 else "_",
            }
            print(format_analysis(
                word,
                lexicon_entry=entry,
                heuristic=True,
                grapheme_path=None   # no FST path — simulated states shown
            ))


def main():
    print("Initializing Bengali FSL...", file=sys.stderr)
    fsl = build_bengali_fsl()
    print("FSL ready.\n", file=sys.stderr)

    import sys as _sys
    import argparse
    parser = argparse.ArgumentParser(description="Bengali FSL Morphological Analyzer")
    parser.add_argument("input_text", nargs="*")
    args = parser.parse_args()

    if args.input_text:
        text = " ".join(args.input_text)
        words = text.split()
        if len(words) == 1:
            analyze_single_word(words[0], fsl)
        else:
            print(analyze_sentence(text, fsl))
    else:
        print("Bengali FSL Interactive Mode.", file=sys.stderr)
        print("  Single word → FST state path + analysis", file=sys.stderr)
        print("  Sentence    → CoNLL-U output", file=sys.stderr)
        print("  Type 'q' to quit\n", file=sys.stderr)

        while True:
            try:
                user_input = input(">> ").strip()
            except (KeyboardInterrupt, EOFError):
                break
            if not user_input:
                continue
            if user_input.lower() in ("q", "quit", "exit"):
                break

            words = user_input.split()
            if len(words) == 1:
                analyze_single_word(words[0], fsl)
            else:
                print(analyze_sentence(user_input, fsl))
            print()


if __name__ == "__main__":
    main()
