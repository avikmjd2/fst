"""
Hindi FSL Test Evaluator
Evaluates the morphological analyzer against a CoNLL-U format test file.
"""

import sys
import argparse
from fst_builder import build_hindi_fsl
from analyzer import generate_conllu_line

def main():
    parser = argparse.ArgumentParser(description="Evaluate Hindi FSL against test data")
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_test = os.path.join(script_dir, "test.txt")
    parser.add_argument("--test-file", default=default_test, help="Path to CoNLL-U test file")
    parser.add_argument("--show-wrong-only", action="store_true", help="Only show mismatches")
    args = parser.parse_args()

    print("Initializing Hindi FSL...")
    # build_hindi_fsl() isn't strictly used for the heuristics but let's init it
    fsl = build_hindi_fsl()

    total = 0
    exact_match = 0
    mismatches = []

    print(f"Reading {args.test_file}...")
    try:
        with open(args.test_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split('\t')
                if len(parts) < 10:
                    continue
                
                # Ignore multi-word tokens (e.g., '1-2')
                if '-' in parts[0] or '.' in parts[0]:
                    continue

                surface = parts[1]
                expected_lemma = parts[2]
                expected_upos = parts[3]
                expected_xpos = parts[4]
                expected_feats = parts[5]

                # Run our analyzer (id=1 just to generate the line)
                my_line = generate_conllu_line(1, surface)
                my_parts = my_line.split('\t')
                
                my_lemma = my_parts[2]
                my_upos = my_parts[3]
                my_xpos = my_parts[4]
                my_feats = my_parts[5]

                total += 1
                
                # We check for exact match on core morphological fields
                is_match = (my_lemma == expected_lemma and 
                            my_upos == expected_upos and 
                            my_xpos == expected_xpos and 
                            my_feats == expected_feats)
                
                if is_match:
                    exact_match += 1
                    if not args.show_wrong_only:
                        print(f"word: {surface}")
                        print(f"  my output: {my_lemma} {my_upos} {my_xpos} {my_feats}")
                        print(f"  expected:  {expected_lemma} {expected_upos} {expected_xpos} {expected_feats}")
                        print("  result: match\n")
                else:
                    print(f"word: {surface}")
                    print(f"  my output: {my_lemma} {my_upos} {my_xpos} {my_feats}")
                    print(f"  expected:  {expected_lemma} {expected_upos} {expected_xpos} {expected_feats}")
                    print("  result: wrong output\n")



    except FileNotFoundError:
        print(f"Error: Could not find {args.test_file}")
        sys.exit(1)

    accuracy = (exact_match / total * 100) if total > 0 else 0.0

    print("=" * 40)
    print("EVALUATION RESULTS")
    print("=" * 40)
    print(f"Dataset: {args.test_file}")
    print(f"Total words evaluated: {total}")
    print(f"Exact morphological matches: {exact_match} / {total} ({accuracy:.2f}%)")
    print("=" * 40)

if __name__ == "__main__":
    main()
