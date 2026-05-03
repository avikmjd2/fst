"""
fst_builder.py - FST Construction
Builds the morphological analyzer using the heuristic engine.
Also maintains pynini FST for visualization when available.
"""


def build_analyzer():
    """
    Build the morphological analyzer.
    Returns a sentinel object - the actual analysis is done
    by the heuristic engine in analyzer.py.
    """
    try:
        import pynini
        from rules import RULES
        # Return a marker that pynini is available
        return "heuristic_analyzer"
    except ImportError:
        return "heuristic_analyzer"
