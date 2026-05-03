import argparse
import os

from fst_builder import build_analyzer
from analyzer import analyze


def parse_expected_annotations(annotation_text):
    return [alt.strip() for alt in annotation_text.split(',') if alt.strip()]


def load_dataset(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Dataset file not found: {path}")

    with open(path, encoding='utf-8') as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if '\t' in line:
                surface, annotation_text = line.split('\t', 1)
            else:
                parts = line.split(None, 1)
                surface = parts[0]
                annotation_text = parts[1] if len(parts) > 1 else ''

            surface = surface.strip().lower()
            if not surface:
                continue

            alternatives = parse_expected_annotations(annotation_text)
            yield lineno, surface, alternatives


def format_expected(alternatives):
    if not alternatives:
        return ''
    return ' | '.join(alternatives)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_dataset = os.path.join(script_dir, 'test_data.txt')

    parser = argparse.ArgumentParser(description='Evaluate model output against the dataset.')
    parser.add_argument('dataset', nargs='?', default=default_dataset,
                        help='Path to the dataset file. Default: test_data.txt')
    parser.add_argument('--limit', type=int, default=None,
                        help='Optional limit on the number of dataset lines to evaluate.')
    parser.add_argument('--show-wrong-only', action='store_true',
                        help='Show only mismatched examples.')
    args = parser.parse_args()

    analyzer_fst = build_analyzer()
    total = 0
    recognized = 0
    exact_match = 0
    comparable = 0
    mismatches = []

    for lineno, surface, alternatives in load_dataset(args.dataset):
        if args.limit and total >= args.limit:
            break
        total += 1

        result = analyze(surface, analyzer_fst)
        if result is None:
            output = 'Word not recognized'
            recognized_flag = False
        else:
            output = result.lexical
            recognized_flag = True

        if recognized_flag:
            recognized += 1

        expected = format_expected(alternatives)
        correct = False
        if alternatives:
            comparable += 1
            if recognized_flag and output in alternatives:
                exact_match += 1
                correct = True

        if not correct:
            mismatches.append((lineno, surface, output, expected, alternatives))
            if not args.show_wrong_only:
                print(f'word: {surface}')
                print(f'  my output: {output}')
                print(f'  expected: {expected}')
                print('  result: wrong output')
                print()

    if args.show_wrong_only:
        for lineno, surface, output, expected, alternatives in mismatches:
            print(f'word: {surface}')
            print(f'  my output: {output}')
            print(f'  expected: {expected}')
            print('  result: wrong output')
            print()

    recognition_rate = recognized / total * 100 if total else 0.0
    exact_rate = exact_match / comparable * 100 if comparable else 0.0
    print('Dataset:', args.dataset)
    print(f'Total lines evaluated: {total}')
    print(f'Recognized surface words: {recognized} / {total} ({recognition_rate:.2f}%)')
    if comparable:
        print(f'Exact matches: {exact_match} / {comparable} ({exact_rate:.2f}% of comparable lines)')
    else:
        print('Exact lexical match comparison skipped because the dataset contains no expected annotations.')
    print(f'Wrong cases: {len(mismatches)}')


if __name__ == '__main__':
    main()
