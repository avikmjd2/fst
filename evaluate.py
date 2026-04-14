"""
Evaluation: compute coverage, accuracy, and ambiguity metrics.
Also performs detailed error analysis categorized by error type.

Metrics:
  - Coverage: fraction of test words that receive at least one analysis
  - Accuracy: fraction of test words where the correct analysis is among the outputs
  - Ambiguity: average number of analyses per word (lower is better)

Error Categories:
  (a) Missing from dictionary (OOV - out of vocabulary)
  (b) Missing spelling rules
  (c) Irregular forms not covered
  (d) Wrong/spurious analyses
"""
import json
import os
from collections import Counter, defaultdict


def evaluate(morph_analyzer, test_data, verbose=True):
    """
    Evaluate the morphological analyzer on test data.

    Args:
        morph_analyzer: MorphAnalyzer instance
        test_data: list of dicts with keys "form" and "analysis"
                   (from data_loader.load_unimorph or similar)
        verbose: print progress

    Returns:
        dict with metrics and detailed results
    """
    total = len(test_data)
    if total == 0:
        print("No test data provided!")
        return {}

    covered = 0           # words with at least one analysis
    correct = 0           # words where correct analysis is found
    total_analyses = 0    # sum of analyses per word (for ambiguity)
    errors = []           # detailed error list

    for i, entry in enumerate(test_data):
        surface = entry["form"]
        expected = entry["analysis"]

        analyses = morph_analyzer.analyze(surface)
        num_analyses = len(analyses)
        total_analyses += num_analyses

        if num_analyses > 0:
            covered += 1
            if expected in analyses:
                correct += 1
            else:
                # Covered but wrong analysis
                errors.append({
                    "form": surface,
                    "expected": expected,
                    "got": analyses,
                    "category": "wrong_analysis",
                })
        else:
            # Not covered at all
            errors.append({
                "form": surface,
                "expected": expected,
                "got": [],
                "category": "no_coverage",
            })

        if verbose and (i + 1) % 500 == 0:
            print(f"  Evaluated {i + 1}/{total}...")

    # Compute metrics
    coverage = covered / total if total > 0 else 0
    accuracy = correct / total if total > 0 else 0
    ambiguity = total_analyses / covered if covered > 0 else 0

    metrics = {
        "total": total,
        "covered": covered,
        "correct": correct,
        "coverage": coverage,
        "accuracy": accuracy,
        "ambiguity": ambiguity,
    }

    if verbose:
        print()
        print("=" * 60)
        print("EVALUATION RESULTS")
        print("=" * 60)
        print(f"  Total test words:    {total}")
        print(f"  Covered:             {covered} ({coverage:.1%})")
        print(f"  Correct:             {correct} ({accuracy:.1%})")
        print(f"  Avg. ambiguity:      {ambiguity:.2f} analyses/word")
        print(f"  Errors:              {len(errors)}")
        print("=" * 60)

    return {
        "metrics": metrics,
        "errors": errors,
    }


def error_analysis(errors, verbose=True):
    """
    Categorize errors into types:
      (a) OOV: word stem missing from dictionary
      (b) Missing spelling rule: word is in dictionary but spelling rule fails
      (c) Irregular not covered: irregular form not in our irregulars list
      (d) Wrong/spurious analysis: system gives analysis but not the correct one

    Args:
        errors: list of error dicts from evaluate()
        verbose: print detailed report

    Returns:
        dict with categorized errors and counts
    """
    categories = defaultdict(list)

    for err in errors:
        cat = err["category"]
        if cat == "no_coverage":
            # Determine sub-category
            expected = err["expected"]
            if "+V;" in expected:
                # Check if it's likely irregular
                lemma = expected.split("+")[0]
                features = expected.split("+", 1)[1]
                if any(f in features for f in ["PST", "PTCP"]):
                    categories["irregular_not_covered"].append(err)
                else:
                    categories["oov_missing_stem"].append(err)
            else:
                categories["oov_missing_stem"].append(err)
        elif cat == "wrong_analysis":
            categories["wrong_analysis"].append(err)

    # Count by category
    counts = {cat: len(errs) for cat, errs in categories.items()}

    if verbose:
        print()
        print("=" * 60)
        print("ERROR ANALYSIS")
        print("=" * 60)
        total_errors = sum(counts.values())
        print(f"Total errors: {total_errors}")
        print()

        category_labels = {
            "oov_missing_stem": "(a) Missing from dictionary (OOV)",
            "missing_spelling_rule": "(b) Missing spelling rules",
            "irregular_not_covered": "(c) Irregular forms not covered",
            "wrong_analysis": "(d) Wrong/spurious analyses",
        }

        for cat_key, label in category_labels.items():
            count = counts.get(cat_key, 0)
            pct = count / total_errors * 100 if total_errors > 0 else 0
            print(f"  {label}: {count} ({pct:.1f}%)")

        # Show examples for each category
        print()
        for cat_key, label in category_labels.items():
            cat_errors = categories.get(cat_key, [])
            if cat_errors:
                print(f"\n--- {label} (showing up to 10 examples) ---")
                for err in cat_errors[:10]:
                    got_str = ", ".join(err["got"]) if err["got"] else "<none>"
                    print(f"  '{err['form']}': expected '{err['expected']}', got [{got_str}]")

    return {
        "categories": {k: v for k, v in categories.items()},
        "counts": counts,
    }


def save_results(metrics, error_report, filepath="results/evaluation_report.json"):
    """Save evaluation results to a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Convert error lists to serializable format (limit size)
    serializable = {
        "metrics": metrics,
        "error_counts": error_report["counts"],
        "error_samples": {},
    }
    for cat, errs in error_report["categories"].items():
        serializable["error_samples"][cat] = errs[:20]  # save top 20 examples

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to {filepath}")


def generate_report_text(metrics, error_report, filepath="results/evaluation_report.txt"):
    """Generate a human-readable text report."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    lines = []
    lines.append("=" * 70)
    lines.append("ENGLISH MORPHOLOGICAL ANALYZER - EVALUATION REPORT")
    lines.append("=" * 70)
    lines.append("")

    m = metrics
    lines.append("METRICS")
    lines.append("-" * 40)
    lines.append(f"  Total test words:       {m['total']}")
    lines.append(f"  Coverage:               {m['covered']}/{m['total']} ({m['coverage']:.1%})")
    lines.append(f"  Accuracy:               {m['correct']}/{m['total']} ({m['accuracy']:.1%})")
    lines.append(f"  Average ambiguity:      {m['ambiguity']:.2f} analyses/word")
    lines.append("")

    lines.append("ERROR ANALYSIS")
    lines.append("-" * 40)
    total_errors = sum(error_report["counts"].values())
    lines.append(f"  Total errors: {total_errors}")
    lines.append("")

    category_labels = {
        "oov_missing_stem": "(a) Missing from dictionary (OOV)",
        "missing_spelling_rule": "(b) Missing spelling rules",
        "irregular_not_covered": "(c) Irregular forms not covered",
        "wrong_analysis": "(d) Wrong/spurious analyses",
    }

    for cat_key, label in category_labels.items():
        count = error_report["counts"].get(cat_key, 0)
        pct = count / total_errors * 100 if total_errors > 0 else 0
        lines.append(f"  {label}: {count} ({pct:.1f}%)")

    lines.append("")
    lines.append("DETAILED ERROR EXAMPLES")
    lines.append("-" * 40)

    for cat_key, label in category_labels.items():
        cat_errors = error_report["categories"].get(cat_key, [])
        if cat_errors:
            lines.append(f"\n  {label}:")
            for err in cat_errors[:15]:
                got_str = ", ".join(err["got"]) if err["got"] else "<none>"
                lines.append(f"    '{err['form']}' -> expected: '{err['expected']}', got: [{got_str}]")

    text = "\n".join(lines)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Report saved to {filepath}")
    return text
