"""
evaluate_hybrid.py - Compare Pure FST vs Hybrid (FST + Neural) System

Runs both systems on the same test set and computes:
  - Coverage: % of words that receive at least one analysis
  - Accuracy: % of words where the correct analysis is produced
  - Ambiguity: average number of analyses per word

Outputs a side-by-side comparison table and detailed error breakdown.

Usage (from fsl/ directory):
    python evaluate_hybrid.py
"""
import os
import sys
import time
import json
from collections import defaultdict

from fst_builder import build_fst
from analyzer import MorphAnalyzer
from neural.predict import NeuralAnalyzer
from neural.data_prep import load_tsv
from hybrid import HybridAnalyzer


def evaluate_system(analyzer_fn, test_data, system_name="System"):
    """
    Evaluate a morphological analyzer on test data.
    
    Args:
        analyzer_fn: function that takes a word and returns list of analyses
        test_data: list of (surface_form, expected_analysis) tuples
        system_name: name for display
        
    Returns:
        dict with metrics and per-word results
    """
    total = len(test_data)
    covered = 0
    correct = 0
    total_analyses = 0
    
    results = []      # per-word results
    errors = []       # incorrect predictions
    oov_words = []    # words with no analysis
    
    for i, (surface, expected_raw) in enumerate(test_data):
        analyses = analyzer_fn(surface)
        num_analyses = len(analyses)
        total_analyses += num_analyses
        
        # Handle custom CELEX format (comma-separated, e.g. "aim_V +3SG, aim_V +PL")
        # and standardize it to match FST/Neural output ("aim+V;3SG")
        expected_list = []
        for e in expected_raw.split(","):
            e = e.strip()
            # If it's the custom format (e.g., "aim_V +3SG")
            if "_V" in e or "_N" in e or "_A" in e:
                # Convert "aim_V +3SG" to "aim+V;3SG"
                e = e.replace(" ", ";").replace("_", "+").replace(";+", ";")
            expected_list.append(e)
            
        # Refined structural matching:
        #   1. Parse each analysis into (lemma, POS, inflectional_features)
        #      e.g. "walk+V;PST"       → ("walk", "V", {"PST"})
        #           "walk+V;V.PTCP;PST" → ("walk", "V", {"V.PTCP","PST"})
        #   2. Match requires:
        #      - Same lemma
        #      - Same POS (first tag — V, N, ADJ, ADV, etc.)
        #      - Inflectional features: exact match, OR both non-empty and
        #        one subsumes the other (handles syncretism like PST ⊂ V.PTCP;PST)
        #   3. Empty-feature predictions (e.g. just "walk+V") never subsume
        #      a specific inflection — prevents lazy underspecification.

        def parse_analysis(analysis):
            """Split 'walk+V;V.PTCP;PST' → ('walk', 'V', {'V.PTCP','PST'})"""
            parts = analysis.split("+", 1)
            lemma = parts[0]
            if len(parts) > 1:
                tags = parts[1].split(";")
                pos = tags[0]                     # first tag = POS
                feats = set(tags[1:])             # rest = inflectional features
            else:
                pos, feats = "", set()
            return lemma, pos, feats

        def analyses_match(pred, expected):
            """Refined match: same lemma, same POS, features subsume."""
            p_lem, p_pos, p_feats = parse_analysis(pred)
            e_lem, e_pos, e_feats = parse_analysis(expected)
            # Lemma and POS must match exactly
            if p_lem != e_lem or p_pos != e_pos:
                return False
            # Features: exact match always OK
            if p_feats == e_feats:
                return True
            # Subsumption only if BOTH sides have at least one feature
            # (prevents empty → anything from inflating scores)
            if p_feats and e_feats:
                return p_feats <= e_feats or e_feats <= p_feats
            return False

        is_correct = any(
            analyses_match(p, e)
            for p in analyses
            for e in expected_list
        )
        
        # Display the expected string properly
        display_expected = expected_list[0] if len(expected_list) == 1 else " | ".join(expected_list)
        
        result = {
            "word": surface,
            "expected": display_expected,
            "predicted": analyses,
            "covered": num_analyses > 0,
            "correct": is_correct,
        }
        results.append(result)
        
        if num_analyses > 0:
            covered += 1
            if is_correct:
                correct += 1
            else:
                errors.append(result)
        else:
            oov_words.append(result)
        
        if (i + 1) % 500 == 0:
            print(f"  [{system_name}] Evaluated {i + 1}/{total}...")
    
    coverage = covered / total if total > 0 else 0
    accuracy = correct / total if total > 0 else 0
    ambiguity = total_analyses / covered if covered > 0 else 0
    
    metrics = {
        "system": system_name,
        "total": total,
        "covered": covered,
        "correct": correct,
        "coverage": coverage,
        "accuracy": accuracy,
        "ambiguity": ambiguity,
        "num_errors": len(errors),
        "num_oov": len(oov_words),
    }
    
    return {
        "metrics": metrics,
        "results": results,
        "errors": errors,
        "oov_words": oov_words,
    }


def print_comparison(fst_metrics, hybrid_metrics):
    """Print a side-by-side comparison table."""
    print()
    print("=" * 72)
    print("COMPARISON: Pure FST  vs  Hybrid (FST + Neural Fallback)")
    print("=" * 72)
    print()
    
    # Header
    print(f"{'Metric':<25s} | {'Pure FST':>15s} | {'Hybrid':>15s} | {'Δ (Hybrid - FST)':>18s}")
    print("-" * 80)
    
    # Rows
    rows = [
        ("Total test words",   f"{fst_metrics['total']}",
                               f"{hybrid_metrics['total']}", ""),
        ("Covered",            f"{fst_metrics['covered']}",
                               f"{hybrid_metrics['covered']}",
                               f"+{hybrid_metrics['covered'] - fst_metrics['covered']}"),
        ("Coverage (%)",       f"{fst_metrics['coverage']:.1%}",
                               f"{hybrid_metrics['coverage']:.1%}",
                               f"+{(hybrid_metrics['coverage'] - fst_metrics['coverage']):.1%}"),
        ("Correct",            f"{fst_metrics['correct']}",
                               f"{hybrid_metrics['correct']}",
                               f"+{hybrid_metrics['correct'] - fst_metrics['correct']}"),
        ("Accuracy (%)",       f"{fst_metrics['accuracy']:.1%}",
                               f"{hybrid_metrics['accuracy']:.1%}",
                               f"+{(hybrid_metrics['accuracy'] - fst_metrics['accuracy']):.1%}"),
        ("Avg. Ambiguity",     f"{fst_metrics['ambiguity']:.2f}",
                               f"{hybrid_metrics['ambiguity']:.2f}", ""),
        ("OOV (no analysis)",  f"{fst_metrics['num_oov']}",
                               f"{hybrid_metrics['num_oov']}",
                               f"{hybrid_metrics['num_oov'] - fst_metrics['num_oov']}"),
        ("Wrong analysis",     f"{fst_metrics['num_errors']}",
                               f"{hybrid_metrics['num_errors']}", ""),
    ]
    
    for label, fst_val, hyb_val, delta in rows:
        if delta:
            print(f"{label:<25s} | {fst_val:>15s} | {hyb_val:>15s} | {delta:>18s}")
        else:
            print(f"{label:<25s} | {fst_val:>15s} | {hyb_val:>15s} |")
    
    print("=" * 80)
    
    # Summary
    improvement = hybrid_metrics["accuracy"] - fst_metrics["accuracy"]
    print()
    print(f"Neural fallback improved accuracy by {improvement:.1%} "
          f"({hybrid_metrics['correct'] - fst_metrics['correct']} additional correct predictions)")
    
    if fst_metrics["num_oov"] > 0:
        neural_rescue_rate = (fst_metrics["num_oov"] - hybrid_metrics["num_oov"]) / fst_metrics["num_oov"]
        print(f"Neural model rescued {neural_rescue_rate:.1%} of OOV words "
              f"({fst_metrics['num_oov'] - hybrid_metrics['num_oov']} out of {fst_metrics['num_oov']})")


def print_error_samples(fst_result, hybrid_result, max_samples=15):
    """Print example words where the neural fallback made a difference."""
    print()
    print("=" * 72)
    print("DETAILED ANALYSIS: Where the Neural Fallback Helped")
    print("=" * 72)
    
    # Find words where FST failed but Hybrid succeeded
    fst_lookup = {r["word"]: r for r in fst_result["results"]}
    hybrid_lookup = {r["word"]: r for r in hybrid_result["results"]}
    
    neural_wins = []
    neural_losses = []
    
    for word, hyb_r in hybrid_lookup.items():
        fst_r = fst_lookup.get(word)
        if fst_r is None:
            continue
        
        # FST failed, hybrid correct -> neural win
        if not fst_r["correct"] and not fst_r["covered"] and hyb_r["correct"]:
            neural_wins.append((word, hyb_r["expected"], hyb_r["predicted"]))
        
        # FST failed, hybrid also wrong -> neural loss
        if not fst_r["covered"] and hyb_r["covered"] and not hyb_r["correct"]:
            neural_losses.append((word, hyb_r["expected"], hyb_r["predicted"]))
    
    # Print neural wins
    print(f"\n--- Neural Fallback CORRECT ({len(neural_wins)} words) ---")
    print(f"  (showing up to {max_samples} examples)\n")
    for word, expected, predicted in neural_wins[:max_samples]:
        pred_str = " | ".join(predicted)
        print(f"  {word:20s}  expected: {expected:30s}  predicted: {pred_str}")
    
    # Print neural losses
    print(f"\n--- Neural Fallback WRONG ({len(neural_losses)} words) ---")
    print(f"  (showing up to {max_samples} examples)\n")
    for word, expected, predicted in neural_losses[:max_samples]:
        pred_str = " | ".join(predicted)
        print(f"  {word:20s}  expected: {expected:30s}  predicted: {pred_str}")
    
    return neural_wins, neural_losses


def save_report(fst_metrics, hybrid_metrics, neural_wins, neural_losses, 
                filepath="results/hybrid_comparison.json"):
    """Save the comparison report as JSON."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    report = {
        "pure_fst": fst_metrics,
        "hybrid": hybrid_metrics,
        "improvement": {
            "accuracy_delta": hybrid_metrics["accuracy"] - fst_metrics["accuracy"],
            "coverage_delta": hybrid_metrics["coverage"] - fst_metrics["coverage"],
            "additional_correct": hybrid_metrics["correct"] - fst_metrics["correct"],
            "neural_wins": len(neural_wins),
            "neural_losses": len(neural_losses),
        },
        "neural_win_samples": [
            {"word": w, "expected": e, "predicted": p} 
            for w, e, p in neural_wins[:50]
        ],
        "neural_loss_samples": [
            {"word": w, "expected": e, "predicted": p} 
            for w, e, p in neural_losses[:50]
        ],
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nReport saved to {filepath}")
    
    # Also save a human-readable text version
    txt_path = filepath.replace(".json", ".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("=" * 72 + "\n")
        f.write("HYBRID SYSTEM EVALUATION REPORT\n")
        f.write("Pure FST vs Hybrid (FST + Neural Fallback)\n")
        f.write("=" * 72 + "\n\n")
        
        f.write("METRICS\n")
        f.write("-" * 40 + "\n")
        for system, metrics in [("Pure FST", fst_metrics), ("Hybrid", hybrid_metrics)]:
            f.write(f"\n  {system}:\n")
            f.write(f"    Total:     {metrics['total']}\n")
            f.write(f"    Coverage:  {metrics['covered']}/{metrics['total']} ({metrics['coverage']:.1%})\n")
            f.write(f"    Accuracy:  {metrics['correct']}/{metrics['total']} ({metrics['accuracy']:.1%})\n")
            f.write(f"    Ambiguity: {metrics['ambiguity']:.2f}\n")
            f.write(f"    OOV:       {metrics['num_oov']}\n")
        
        f.write(f"\nIMPROVEMENT\n")
        f.write(f"-" * 40 + "\n")
        f.write(f"  Accuracy:  +{report['improvement']['accuracy_delta']:.1%}\n")
        f.write(f"  Coverage:  +{report['improvement']['coverage_delta']:.1%}\n")
        f.write(f"  Additional correct: +{report['improvement']['additional_correct']}\n")
        f.write(f"  Neural wins:  {report['improvement']['neural_wins']}\n")
        f.write(f"  Neural losses: {report['improvement']['neural_losses']}\n")
        
        f.write(f"\nNEURAL WINS (sample)\n")
        f.write(f"-" * 40 + "\n")
        for item in report["neural_win_samples"][:20]:
            pred = " | ".join(item["predicted"])
            f.write(f"  {item['word']:20s} expected: {item['expected']:30s} got: {pred}\n")
        
        f.write(f"\nNEURAL LOSSES (sample)\n")
        f.write(f"-" * 40 + "\n")
        for item in report["neural_loss_samples"][:20]:
            pred = " | ".join(item["predicted"])
            f.write(f"  {item['word']:20s} expected: {item['expected']:30s} got: {pred}\n")
    
    print(f"Text report saved to {txt_path}")


def main():
    """Run the full comparison evaluation."""
    # ── Load test data ──────────────────────────────────────────────
    test_path = os.path.join(os.path.dirname(__file__), "neural", "data", "test.tsv")
    
    if not os.path.exists(test_path):
        print(f"ERROR: Test data not found at {test_path}")
        print("Run 'python neural/data_prep.py' first to generate train/dev/test splits.")
        return
    
    test_data = load_tsv(test_path)
    print(f"Loaded {len(test_data)} test pairs from {test_path}")
    print()
    
    # ── Build FST ───────────────────────────────────────────────────
    print("[1/3] Building FST analyzer...")
    generator, analyzer_fst = build_fst()
    fst_analyzer = MorphAnalyzer(generator, analyzer_fst)
    print()
    
    # ── Load Neural Model ───────────────────────────────────────────
    print("[2/3] Loading neural fallback model...")
    neural_model_dir = os.path.join(os.path.dirname(__file__), "neural", "checkpoints")
    
    if not os.path.exists(os.path.join(neural_model_dir, "best_model.pt")):
        print(f"ERROR: No trained neural model found at {neural_model_dir}")
        print("Run 'python neural/train.py' first to train the neural model.")
        return
    
    neural_analyzer = NeuralAnalyzer(neural_model_dir)
    hybrid_analyzer = HybridAnalyzer(fst_analyzer, neural_analyzer)
    print()
    
    # ── Evaluate Pure FST ───────────────────────────────────────────
    print("[3/3] Running evaluation...")
    print()
    
    print("Evaluating PURE FST...")
    start = time.time()
    fst_result = evaluate_system(
        analyzer_fn=fst_analyzer.analyze,
        test_data=test_data,
        system_name="Pure FST",
    )
    fst_time = time.time() - start
    print(f"  Pure FST evaluation: {fst_time:.1f}s")
    print()
    
    # ── Evaluate Hybrid ─────────────────────────────────────────────
    print("Evaluating HYBRID (FST + Neural)...")
    start = time.time()
    
    def hybrid_analyze(word):
        result = hybrid_analyzer.analyze(word)
        return result["analyses"]
    
    hybrid_result = evaluate_system(
        analyzer_fn=hybrid_analyze,
        test_data=test_data,
        system_name="Hybrid",
    )
    hybrid_time = time.time() - start
    print(f"  Hybrid evaluation: {hybrid_time:.1f}s")
    
    # ── Print comparison ────────────────────────────────────────────
    print_comparison(fst_result["metrics"], hybrid_result["metrics"])
    neural_wins, neural_losses = print_error_samples(fst_result, hybrid_result)
    
    # ── Save report ─────────────────────────────────────────────────
    save_report(
        fst_result["metrics"], hybrid_result["metrics"],
        neural_wins, neural_losses,
    )


if __name__ == "__main__":
    main()
