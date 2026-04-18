"""
Analyzer: high-level interface for morphological analysis and generation.

Analysis:  surface form  -> list of analysis strings  (e.g., "walked" -> ["walk+V;PST", "walk+V;V.PTCP;PST"])
Generation: analysis string -> list of surface forms  (e.g., "walk+V;PST" -> ["walked"])
"""
import pynini


class MorphAnalyzer:
    """
    English morphological analyzer/generator built on composed FSTs.

    Usage:
        from fst_builder import build_fst
        gen, ana = build_fst()
        morph = MorphAnalyzer(gen, ana)

        # Analyze a surface form
        morph.analyze("walked")   # -> ["walk+V;PST", "walk+V;V.PTCP;PST"]

        # Generate surface forms
        morph.generate("walk+V;PST")  # -> ["walked"]
    """

    def __init__(self, generator, analyzer):
        """
        Args:
            generator: FST mapping analysis (upper) -> surface (lower)
            analyzer:  FST mapping surface (upper) -> analysis (lower)
        """
        self.generator = generator
        self.analyzer = analyzer

    def analyze(self, surface_form):
        """
        Analyze a surface word form and return all possible analyses.

        Args:
            surface_form: the word to analyze (e.g., "walked")

        Returns:
            List of analysis strings (e.g., ["walk+V;PST", "walk+V;V.PTCP;PST"])
            Empty list if no analysis is found.
        """
        try:
            lattice = pynini.compose(
                pynini.accep(surface_form, token_type="utf8"),
                self.analyzer
            )
            if lattice.start() == pynini.NO_STATE_ID:
                return []
            # Extract all output paths
            paths = lattice.paths(output_token_type="utf8")
            results = list(paths.ostrings())
            return sorted(set(results))
        except Exception:
            return []

    def generate(self, analysis_string):
        """
        Generate surface form(s) from an analysis string.

        Args:
            analysis_string: the morphological analysis (e.g., "walk+V;PST")

        Returns:
            List of surface forms (e.g., ["walked"])
            Empty list if generation fails.
        """
        try:
            lattice = pynini.compose(
                pynini.accep(analysis_string, token_type="utf8"),
                self.generator
            )
            if lattice.start() == pynini.NO_STATE_ID:
                return []
            paths = lattice.paths(output_token_type="utf8")
            results = list(paths.ostrings())
            return sorted(set(results))
        except Exception:
            return []

    def analyze_verbose(self, surface_form):
        """
        Analyze a word and return structured results.

        Returns:
            dict with keys: 'surface', 'analyses', 'count'
        """
        analyses = self.analyze(surface_form)
        parsed = []
        for a in analyses:
            parts = a.split("+", 1)
            lemma = parts[0]
            features = parts[1] if len(parts) > 1 else ""
            parsed.append({
                "raw": a,
                "lemma": lemma,
                "features": features,
            })
        return {
            "surface": surface_form,
            "analyses": parsed,
            "count": len(parsed),
        }

    def batch_analyze(self, words):
        """Analyze a list of words. Returns dict mapping word -> analyses."""
        results = {}
        for word in words:
            results[word] = self.analyze(word)
        return results
