"""
FST Builder: composes the morphotactics and spelling rules into the final
transducer, and unions it with irregular forms.

The final FST has:
  - Upper tape (input for generation): analysis string, e.g., "walk+V;PST"
  - Lower tape (output for generation): surface form, e.g., "walked"

Inverting the FST gives the analyzer (surface -> analysis).
"""
import pynini
from morphotactics import build_morphotactics
from spelling_rules import build_spelling_rules
from irregulars import ALL_IRREGULARS


def build_irregulars_fst():
    """Build FST for all irregular forms as direct (analysis, surface) mappings."""
    if not ALL_IRREGULARS:
        return None
    fst = pynini.string_map(ALL_IRREGULARS).optimize()
    print(f"  [irregulars] {len(ALL_IRREGULARS)} irregular mappings loaded")
    return fst


def build_fst():
    """
    Build the complete morphological FST.

    Architecture:
      generator = (morphotactics @ spelling_rules) | irregulars
      analyzer  = invert(generator)

    Returns:
      (generator, analyzer) tuple
    """
    print("Building morphological FST...")
    print()

    # Step 1: Build morphotactics (analysis -> intermediate form with ^ boundaries)
    print("[1/4] Building morphotactics...")
    morphotactics = build_morphotactics()
    print()

    # Step 2: Build spelling rules cascade (intermediate -> surface)
    print("[2/4] Building spelling rules...")
    spelling_rules = build_spelling_rules()
    print()

    # Step 3: Compose morphotactics with spelling rules
    print("[3/4] Composing morphotactics @ spelling rules...")
    regular_generator = (morphotactics @ spelling_rules).optimize()
    print("  Composition complete")
    print()

    # Step 4: Union with irregulars
    print("[4/4] Adding irregular forms...")
    irregulars_fst = build_irregulars_fst()

    if irregulars_fst is not None:
        generator = pynini.union(regular_generator, irregulars_fst).optimize()
    else:
        generator = regular_generator
    print()

    # Build analyzer by inverting the generator
    analyzer = pynini.invert(generator).optimize()

    # Print stats
    print("=" * 50)
    print("FST Build Complete!")
    def count_arcs(fst):
        return sum(fst.num_arcs(s) for s in fst.states())

    print(f"  Generator: {generator.num_states()} states, {count_arcs(generator)} arcs")
    print(f"  Analyzer:  {analyzer.num_states()} states, {count_arcs(analyzer)} arcs")
    print("=" * 50)

    return generator, analyzer
