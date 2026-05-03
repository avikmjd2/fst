from lexicon import get_all_surface_words
from fst_builder import build_analyzer
from analyzer import analyze

analyzer = build_analyzer()
words = get_all_surface_words()
with open('train_data.txt', 'w', encoding='utf-8') as f:
    for surface in words:
        result = analyze(surface, analyzer)
        if result is None:
            continue
        f.write(f"{surface}\t{result.lexical}\n")
print(f"Wrote train_data.txt with {len(words)} entries.")
