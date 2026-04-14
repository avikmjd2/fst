"""
English Morphological Analyzer using Finite State Transducers (Pynini)

Usage:
  python main.py                     # Interactive REPL mode
  python main.py analyze walked      # Analyze a single word
  python main.py generate walk+V;PST # Generate surface form
  python main.py batch words.txt     # Analyze all words in a file
  python main.py evaluate            # Run evaluation on UniMorph data
  python main.py demo                # Run demonstration with example words
"""
import sys
import time

from fst_builder import build_fst
from analyzer import MorphAnalyzer


def run_demo(morph):
    """Demonstrate the analyzer with a curated set of examples."""
    print("\n" + "=" * 70)
    print("DEMONSTRATION: English Morphological Analyzer")
    print("=" * 70)

    # --- Analysis examples ---
    print("\n--- ANALYSIS (surface form -> morphological analysis) ---\n")

    test_words = [
        # Regular nouns
        "dogs", "cats", "houses", "watches", "churches", "boxes",
        "cities", "babies", "stories", "boys", "keys", "toys",
        # Regular verbs
        "walked", "walking", "walks", "played", "playing", "plays",
        "hoped", "hoping", "hopes", "liked", "liking", "likes",
        "carried", "carrying", "carries", "studied", "studying", "studies",
        "tried", "trying", "tries",
        # Irregular verbs
        "went", "gone", "going", "goes",
        "said", "saying", "says",
        "took", "taken", "taking", "takes",
        "saw", "seen", "seeing", "sees",
        "ran", "running", "runs",
        "wrote", "written", "writing", "writes",
        "thought", "thinking", "thinks",
        "was", "were", "been", "being",
        "had", "has", "having",
        "did", "does", "done", "doing",
        # Irregular nouns
        "men", "women", "children", "feet", "teeth", "mice",
        "knives", "wives", "lives", "leaves", "wolves",
        "sheep", "deer", "fish",
        # Adjective comparatives/superlatives
        "taller", "tallest", "smaller", "smallest",
        "nicer", "nicest", "larger", "largest",
        "happier", "happiest", "easier", "easiest",
        "better", "best", "worse", "worst",
        "bigger", "biggest", "hotter", "hottest",
        # Derivational
        "unhappy", "unfair", "unkind",
        "darkness", "kindness", "happiness",
        "badly", "kindly", "happily", "quickly",
    ]

    for word in test_words:
        analyses = morph.analyze(word)
        if analyses:
            analyses_str = " | ".join(analyses)
            print(f"  {word:20s} -> {analyses_str}")
        else:
            print(f"  {word:20s} -> [NO ANALYSIS]")

    # --- Generation examples ---
    print("\n--- GENERATION (morphological analysis -> surface form) ---\n")

    test_analyses = [
        "walk+V;PST", "walk+V;V.PTCP;PRS", "walk+V;PRS;3;SG",
        "hope+V;PST", "hope+V;V.PTCP;PRS",
        "carry+V;PST", "carry+V;PRS;3;SG", "carry+V;V.PTCP;PRS",
        "dog+N;PL", "watch+N;PL", "city+N;PL", "boy+N;PL",
        "go+V;PST", "go+V;V.PTCP;PST", "see+V;PST",
        "man+N;PL", "child+N;PL", "knife+N;PL",
        "tall+ADJ;CMPR", "tall+ADJ;SPRL",
        "happy+ADJ;CMPR", "happy+ADJ;SPRL",
        "nice+ADJ;CMPR", "nice+ADJ;SPRL",
        "good+ADJ;CMPR", "good+ADJ;SPRL",
        "big+ADJ;CMPR", "big+ADJ;SPRL",
    ]

    for analysis in test_analyses:
        forms = morph.generate(analysis)
        if forms:
            forms_str = " | ".join(forms)
            print(f"  {analysis:30s} -> {forms_str}")
        else:
            print(f"  {analysis:30s} -> [GENERATION FAILED]")


def run_interactive(morph):
    """Interactive REPL for analysis and generation."""
    print("\n" + "=" * 70)
    print("INTERACTIVE MODE")
    print("=" * 70)
    print("Commands:")
    print("  <word>           Analyze a word (e.g., 'walked')")
    print("  gen <analysis>   Generate a word (e.g., 'gen walk+V;PST')")
    print("  quit / exit      Exit the program")
    print("-" * 70)

    while True:
        try:
            user_input = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if user_input.lower().startswith("gen "):
            # Generation mode
            analysis = user_input[4:].strip()
            forms = morph.generate(analysis)
            if forms:
                print(f"  Generated: {' | '.join(forms)}")
            else:
                print(f"  No surface form found for '{analysis}'")
        else:
            # Analysis mode
            word = user_input.lower()
            analyses = morph.analyze(word)
            if analyses:
                print(f"  Analyses for '{word}':")
                for a in analyses:
                    parts = a.split("+", 1)
                    lemma = parts[0]
                    features = parts[1] if len(parts) > 1 else ""
                    print(f"    {a:35s}  (lemma: {lemma}, features: {features})")
            else:
                print(f"  No analysis found for '{word}'")


def run_batch(morph, filepath):
    """Analyze all words in a file (one word per line)."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            words = [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return

    print(f"Analyzing {len(words)} words from {filepath}...")
    for word in words:
        analyses = morph.analyze(word)
        analyses_str = " | ".join(analyses) if analyses else "[NO ANALYSIS]"
        print(f"{word}\t{analyses_str}")


def run_evaluate(morph):
    """Run evaluation on UniMorph data."""
    from data_loader import download_unimorph, load_unimorph
    from evaluate import evaluate, error_analysis, save_results, generate_report_text

    # Download data if needed
    data_path = download_unimorph("data")
    if data_path is None:
        print("Cannot run evaluation without data.")
        return

    # Load data
    entries = load_unimorph(data_path)
    if not entries:
        print("No data loaded.")
        return

    # Use all data as test data (our FST is rule-based, not trained)
    print(f"\nEvaluating on {len(entries)} entries...")
    results = evaluate(morph, entries)

    if results:
        err_report = error_analysis(results["errors"])
        save_results(results["metrics"], err_report)
        generate_report_text(results["metrics"], err_report)


def main():
    # Build the FST
    start_time = time.time()
    generator, analyzer_fst = build_fst()
    build_time = time.time() - start_time
    print(f"\nBuild time: {build_time:.2f}s")

    morph = MorphAnalyzer(generator, analyzer_fst)

    # Parse command-line arguments
    if len(sys.argv) < 2:
        # Default: run demo then interactive
        run_demo(morph)
        run_interactive(morph)
    elif sys.argv[1] == "demo":
        run_demo(morph)
    elif sys.argv[1] == "analyze" and len(sys.argv) >= 3:
        word = sys.argv[2].lower()
        analyses = morph.analyze(word)
        if analyses:
            for a in analyses:
                print(a)
        else:
            print(f"No analysis for '{word}'")
    elif sys.argv[1] == "generate" and len(sys.argv) >= 3:
        analysis = sys.argv[2]
        forms = morph.generate(analysis)
        if forms:
            for f in forms:
                print(f)
        else:
            print(f"No surface form for '{analysis}'")
    elif sys.argv[1] == "batch" and len(sys.argv) >= 3:
        run_batch(morph, sys.argv[2])
    elif sys.argv[1] == "evaluate":
        run_evaluate(morph)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()