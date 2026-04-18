# Simple English Morphological Analyzer (FST)

This project is a lightweight Finite State Transducer (FST) based morphological analyzer for English, implemented using the [Pynini](https://github.com/kylebgorman/pynini) Python library.

It maps between surface word forms (e.g., `unhappiness`) and underlying morphological analyses (e.g., `un+happy+ness`), and includes a visualizer that shows the character-by-character state path through the FST, including orthographic branches like the `y -> i` transition.

## Features

This analyzer demonstrates core FST concepts using a small, focused lexicon and targeted rules:

1. **Lexicon (`lexicon.py`)**
   - Contains a predefined set of roots, prefixes, and suffixes.
   - Defines valid combinations (morphotactics) for these morphemes (e.g., `un+happy+ness`, `play+ing`).

2. **Orthographic Rules (`rules.py`)**
   - Context-dependent rewrite rules (`cdrewrite`) that resolve orthographic changes at morpheme boundaries.
   - **y -> i transformation**: When a root ending in `-y` is followed by a consonant-initial suffix (e.g., `happy+ness` -> `happiness`).
   - **Boundary deletion**: Cleans up all internal `+` markers.

3. **Analyzer & Visualizer (`analyzer.py` & `visualizer.py`)**
   - Extracts the shortest path through the composed FST using `pynini.shortestpath`.
   - Reconstructs morphological tags (e.g., `un (NEG) + happy (ROOT) + ness (SUFF)`).
   - Draws an ASCII-art state graph showing exactly how the input characters transition, explicitly visualizing where the `y -> i` rule applies.

## Requirements

- Python 3.x
- [Pynini](https://github.com/kylebgorman/pynini) (`pip install pynini` or `conda install -c conda-forge pynini`)

## Usage

The system provides a command-line interface through `main.py`.

### 1. Interactive Mode
Run the interactive prompt to test analysis dynamically.
```bash
python main.py
```
* **To Analyze**: Just type any word (e.g., `unhappiness`, `playful`).

### 2. Single-Word Mode
Analyze a word directly from your terminal:
```bash
python main.py unhappiness
```

---
## Project Structure

* `main.py`: CLI entry point and interactive REPL.
* `fst_builder.py`: Core logic combining the lexicon and rules into the final analyzer FST.
* `analyzer.py`: FST traversal logic, path extraction, and morpheme tagging.
* `lexicon.py`: Vocabulary definition and valid morphotactic combinations.
* `rules.py`: `cdrewrite` FST cascading module for spelling rules.
* `visualizer.py`: Formats the FST path into a readable ASCII state graph.
