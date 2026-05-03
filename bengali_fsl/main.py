"""
Main CLI for Bengali Morphological Analyzer (FSL)
"""
import sys
import argparse
from fst_builder import build_bengali_fsl, is_valid_word
from analyzer import analyze_sentence, generate_conllu_line

def main():
    parser = argparse.ArgumentParser(description="Bengali FSL Morphological Analyzer")
    parser.add_argument("input_text", nargs="*", help="Bengali word or sentence to analyze")
    args = parser.parse_args()
    
    print("Initializing Bengali FSL...", file=sys.stderr)
    fsl = build_bengali_fsl()
    
    if args.input_text:
        text = " ".join(args.input_text)
        if len(text.split()) > 1:
            print(analyze_sentence(text, fsl))
        else:
            print("1\t" + generate_conllu_line(1, text).split("\t", 1)[1])
    else:
        print("Bengali FSL Interactive Mode. Type a word or sentence (or 'q' to quit):", file=sys.stderr)
        while True:
            try:
                user_input = input(">> ").strip()
                if user_input.lower() in ('q', 'quit', 'exit'):
                    break
                if not user_input:
                    continue
                    
                if len(user_input.split()) > 1:
                    print(analyze_sentence(user_input, fsl))
                else:
                    # Strip the ID part to match a 1-based index
                    print(generate_conllu_line(1, user_input))
                        
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    main()
