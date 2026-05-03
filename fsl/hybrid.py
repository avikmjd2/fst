"""
hybrid.py - Hybrid Morphological Analyzer (FST + Neural Fallback)

Combines the rule-based Pynini FST analyzer with a character-level
neural Transformer fallback model.

Pipeline:
    1. Try the FST first (fast, precise, rule-based)
    2. If FST returns no analysis (OOV word), fall back to the neural model
    3. Tag the result source as "FST" or "Neural" for evaluation

Usage (from fsl/ directory):
    python hybrid.py                  # interactive mode
    python hybrid.py walked           # single word
    python hybrid.py batch words.txt  # batch mode
"""
import sys
import time

from fst_builder import build_fst
from analyzer import MorphAnalyzer
from neural.predict import NeuralAnalyzer


class HybridAnalyzer:
    """
    Hybrid morphological analyzer combining FST + Neural fallback.
    
    The FST is always tried first. If the FST cannot analyze a word
    (returns empty list), the neural model is used as a backup.
    
    Attributes:
        fst_analyzer: MorphAnalyzer (Pynini-based FST)
        neural_analyzer: NeuralAnalyzer (character-level Transformer)
    """
    
    def __init__(self, fst_analyzer, neural_analyzer):
        """
        Args:
            fst_analyzer: MorphAnalyzer instance (from analyzer.py)
            neural_analyzer: NeuralAnalyzer instance (from neural/predict.py)
        """
        self.fst_analyzer = fst_analyzer
        self.neural_analyzer = neural_analyzer
    
    def analyze(self, word):
        """
        Analyze a word using FST first, neural fallback second.
        
        Args:
            word: surface form string (e.g., "walked")
            
        Returns:
            dict with keys:
                "source": "FST" or "Neural"
                "analyses": list of analysis strings
                "word": the input word
        """
        # Step 1: Try FST
        fst_results = self.fst_analyzer.analyze(word)
        
        if fst_results:
            return {
                "source": "FST",
                "analyses": fst_results,
                "word": word,
            }
        
        # Step 2: Fallback to Neural Model
        neural_results = self.neural_analyzer.analyze(word)
        
        return {
            "source": "Neural",
            "analyses": neural_results,
            "word": word,
        }
    
    def batch_analyze(self, words):
        """
        Analyze a list of words.
        
        Returns:
            list of result dicts (one per word)
        """
        results = []
        for word in words:
            results.append(self.analyze(word))
        return results
    
    def analyze_verbose(self, word):
        """
        Analyze with detailed output including source attribution.
        """
        result = self.analyze(word)
        parsed = []
        for a in result["analyses"]:
            parts = a.split("+", 1)
            lemma = parts[0]
            features = parts[1] if len(parts) > 1 else ""
            parsed.append({
                "raw": a,
                "lemma": lemma,
                "features": features,
            })
        return {
            "word": word,
            "source": result["source"],
            "analyses": parsed,
            "count": len(parsed),
        }


def build_hybrid_analyzer(neural_model_dir=None):
    """
    Build the complete hybrid analyzer.
    
    1. Builds the Pynini FST
    2. Loads the trained neural model
    3. Wraps them in a HybridAnalyzer
    
    Args:
        neural_model_dir: path to neural model checkpoints
                          (default: neural/checkpoints/)
    
    Returns:
        HybridAnalyzer instance
    """
    import os
    if neural_model_dir is None:
        neural_model_dir = os.path.join(os.path.dirname(__file__), "neural", "checkpoints")
    
    # Build FST
    print("=" * 60)
    print("BUILDING HYBRID ANALYZER")
    print("=" * 60)
    print()
    
    print("[1/2] Building FST analyzer...")
    generator, analyzer_fst = build_fst()
    fst_analyzer = MorphAnalyzer(generator, analyzer_fst)
    print()
    
    # Load neural model
    print("[2/2] Loading neural fallback model...")
    neural_analyzer = NeuralAnalyzer(neural_model_dir)
    print()
    
    print("=" * 60)
    print("HYBRID ANALYZER READY")
    print("  FST: rule-based Pynini transducer (primary)")
    print("  Neural: character-level Transformer (fallback)")
    print("=" * 60)
    
    return HybridAnalyzer(fst_analyzer, neural_analyzer)


def run_interactive(hybrid):
    """Interactive REPL for the hybrid analyzer."""
    print("\nHYBRID MORPHOLOGICAL ANALYZER (interactive mode)")
    print("  Type a word to analyze, or 'quit' to exit.")
    print("-" * 50)
    
    while True:
        try:
            word = input("\n> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        
        if not word or word in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        
        result = hybrid.analyze(word)
        source = result["source"]
        analyses = result["analyses"]
        
        if analyses:
            source_tag = f"[{source}]"
            print(f"  {source_tag:>10s}  Analyses for '{word}':")
            for a in analyses:
                parts = a.split("+", 1)
                lemma = parts[0]
                features = parts[1] if len(parts) > 1 else ""
                print(f"              {a:35s}  (lemma: {lemma}, features: {features})")
        else:
            print(f"  No analysis found for '{word}'")


def main():
    hybrid = build_hybrid_analyzer()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "batch" and len(sys.argv) >= 3:
            # Batch mode
            filepath = sys.argv[2]
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    words = [line.strip().lower() for line in f if line.strip()]
            except FileNotFoundError:
                print(f"File not found: {filepath}")
                return
            
            print(f"\nAnalyzing {len(words)} words...\n")
            fst_count = 0
            neural_count = 0
            
            for word in words:
                result = hybrid.analyze(word)
                source = result["source"]
                analyses_str = " | ".join(result["analyses"]) if result["analyses"] else "[NONE]"
                print(f"  [{source:>7s}]  {word:20s} -> {analyses_str}")
                
                if source == "FST":
                    fst_count += 1
                else:
                    neural_count += 1
            
            print(f"\nSummary: {fst_count} FST, {neural_count} Neural")
        else:
            # Single word mode
            word = sys.argv[1].strip().lower()
            result = hybrid.analyze(word)
            source = result["source"]
            analyses = result["analyses"]
            analyses_str = " | ".join(analyses) if analyses else "[NONE]"
            print(f"[{source}] {word} -> {analyses_str}")
    else:
        run_interactive(hybrid)


if __name__ == "__main__":
    main()
