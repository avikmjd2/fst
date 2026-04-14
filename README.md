# English Morphological Analyzer

This project is a Finite State Transducer (FST) based morphological analyzer and generator for the English language, implemented using the [Pynini](https://github.com/kylebgorman/pynini) Python library.

It maps between surface word forms (e.g., `walked`) and underlying morphological analyses (e.g., `walk+V;PST`), supporting both analysis (surface -> underlying) and generation (underlying -> surface).

## Features

The system models English morphology using three primary cascaded components:

1. **Lexicon (`lexicon.py` & `irregulars.py`)**
   - Contains word stems organized by part of speech.
   - Handles an extensive list of irregular verbs (e.g., *go -> went*, *think -> thought*).
   - Handles irregular plural nouns and adjective comparatives.
   - Contains rules for special consonant doubling (e.g., *stop -> stopped*).

2. **Morphotactics (`morphotactics.py`)**
   - Rules determining which prefixes and suffixes can attach to which stems.
   - Handles regular inflectional morphology for verbs (e.g., *+V;PST* -> `^ed`), nouns, and adjectives.
   - Includes derivational morphotactics (e.g., `un-`, `re-`, `-ness`, `-ly`).

3. **Spelling Rules (`spelling_rules.py`)**
   - Context-dependent rewrite rules (`cdrewrite`) that resolve orthographic changes at morpheme boundaries.
   - **y -> ie**: `fly^s` $\rightarrow$ `flies`
   - **y -> i**: `carry^ed` $\rightarrow$ `carried`
   - **e-deletion**: `hope^ing` $\rightarrow$ `hoping`
   - **e-insertion**: `watch^s` $\rightarrow$ `watches`
   - **Boundary deletion**: Cleans up all `^` markers.

## Requirements

- Python 3.x
- [Pynini](https://github.com/kylebgorman/pynini) (`pip install pynini` or `conda install -c conda-forge pynini`)

## Usage

The system exposes a multi-purpose command-line interface through `main.py`.

### 1. Interactive Mode
Run the REPL to interactively test analysis and generation.
```bash
python main.py
```
* **To Analyze**: Just type any word (e.g., `walks`, `happiest`).
* **To Generate**: Type `gen` followed by an analysis tag (e.g., `gen walk+V;PST`).

### 2. Demonstration
Run a pre-defined suite of test words showcasing regular and irregular forms.
```bash
python main.py demo
```

### 3. Command-Line Processing
Execute single word operations directly from your terminal:
```bash
# Analyze a word
python main.py analyze happiest

# Generate a surface form
python main.py generate happy+ADJ;SPRL
```

### 4. File Batch Processing
Analyze a list of words from a text file (one word per line).
```bash
python main.py batch words.txt
```

### 5. Evaluation
Test the analyzer against the [UniMorph](https://unimorph.github.io/) English dataset. This automatically downloads the necessary TSV files, runs the analyzer on every entry, and computes **Coverage**, **Accuracy**, and **Ambiguity** metrics. It also performs a detailed error analysis categorized by error types (OOV, missing spelling rules, irregulars).
```bash
python main.py evaluate
```
*Results and detailed error reports are saved to the `results/` folder.*

---
## Project Structure

* `main.py`: CLI entry point.
* `fst_builder.py`: Core logic combining all components into the final FST and inverted analyzer.
* `analyzer.py`: High-level wrapper providing `analyze()` and `generate()` methods.
* `alphabet.py`: Shared character and symbol definitions.
* `lexicon.py`: Comprehensive POS-grouped standard vocabulary.
* `irregulars.py`: Direct mappings for words that break morphotactic rules.
* `morphotactics.py`: Tag-to-suffix mapping networks.
* `spelling_rules.py`: `cdrewrite` FST cascading module.
* `data_loader.py`: Downloader and parser for the UniMorph TSV dataset.
* `evaluate.py`: Logic for computing metrics and performing detailed error analysis.
