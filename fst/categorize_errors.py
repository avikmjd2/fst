"""Categorize errors to find most impactful fixes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fst_builder import build_analyzer
from analyzer import analyze

cats = {}
with open('test_data.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or '\t' not in line:
            continue
        surface, annot = line.split('\t', 1)
        surface = surface.strip().lower()
        alts = [a.strip() for a in annot.split(',') if a.strip()]
        
        r = analyze(surface, None)
        output = r.lexical if r else None
        
        if output and output in alts:
            continue  # correct
        
        if output is None:
            cat = "NOT_RECOGNIZED"
        elif any('+PAST' in a for a in alts) and '+PAST' not in (output or ''):
            cat = "WRONG_PAST"
        elif any('+PL' in a for a in alts) and '+PL' not in (output or ''):
            cat = "WRONG_PL"
        elif any('+PCP1' in a for a in alts) and '+PCP1' not in (output or ''):
            cat = "WRONG_PCP1"
        elif any('+GEN' in a for a in alts) and '+GEN' not in (output or ''):
            cat = "WRONG_GEN"
        elif any('+CMP' in a for a in alts) and output and '+CMP' in output:
            cat = "WRONG_CMP_MATCH"
        elif output and '+CMP' in output:
            cat = "SPURIOUS_CMP"
        else:
            cat = "OTHER"
        
        cats.setdefault(cat, []).append((surface, output, alts[0] if alts else ''))

for cat in sorted(cats, key=lambda c: -len(cats[c])):
    print(f"\n=== {cat}: {len(cats[cat])} errors ===")
    for s, o, e in cats[cat][:5]:
        print(f"  {s}: got [{o}] expected [{e}]")
