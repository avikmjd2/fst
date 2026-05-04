# λ Pullinguistics — Hybrid Morphological Analyzer

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-00a393.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg)
![Pynini](https://img.shields.io/badge/Pynini%2FOpenFST-rule--based-green.svg)
![Languages](https://img.shields.io/badge/languages-English%20%7C%20Hindi%20%7C%20Bengali-orange.svg)

**Pullinguistics** is a research-grade **Hybrid Morphological Analyzer** that fuses the deterministic precision of rule-based Finite State Transducers (FST) with the robust generalization power of a Character-Level Transformer neural network.

The core design principle: **rules handle the known, neural networks handle the unknown.** The FST provides guaranteed-correct analyses for every word within its lexicon. When a word falls outside that lexicon (Out-Of-Vocabulary), the neural fallback immediately takes over, ensuring **100% coverage** at all times.

The project ships a full-stack application: a **FastAPI backend** serving real-time morphological analyses and FST state-graph data, and a polished **dark-mode web UI** that renders both a "Raw OpenFST Lattice" diagram and a synthetically aligned "Textbook" diagram for every query.

---

## Table of Contents

1. [Key Features](#key-features)
2. [System Architecture](#system-architecture)
3. [Repository Structure](#repository-structure)
4. [The English FST Engine](#the-english-fst-engine)
   - [Lexicon](#1-lexicon)
   - [Morphotactics](#2-morphotactics)
   - [Spelling Rules](#3-spelling-rules--orthographic-rewrite-rules)
   - [Irregular Forms](#4-irregular-forms)
   - [FST Composition](#5-fst-composition--inversion)
5. [The Neural Fallback (CharTransformer)](#the-neural-fallback-chartransformer)
   - [Architecture](#architecture)
   - [Training](#training)
   - [Inference](#inference--greedy-decoding)
6. [Hindi & Bengali FSTs](#hindi--bengali-fsts)
7. [The REST API](#the-rest-api-fastapi)
8. [The Frontend UI](#the-frontend-ui)
9. [Dual Graph Visualization](#dual-graph-visualization)
10. [Evaluation & Performance](#evaluation--performance)
11. [Getting Started](#getting-started)
12. [API Reference](#api-reference)

---

## Key Features

- **Multi-Language Analysis** — Morphological analysis for English, Hindi, and Bengali, conforming to the [UniMorph schema](https://unimorph.github.io/).
- **Hybrid Architecture** — FST-first precision with guaranteed neural fallback. Zero OOV errors.
- **Dual-Graph Visualization** — Two SVG diagrams per query: a raw OpenFST lattice traversal and a perfectly aligned textbook diagram.
- **Color-Coded Tapes** — Input characters displayed in pink, output/lemma characters in green, visually separating the two tapes of the transducer.
- **Interactive Web UI** — Quick-chips for example words, language switcher, source badge, analysis breakdowns with feature tags.
- **High-Performance API** — Asynchronous FastAPI backend serving all models. All models (FST + Neural + Hindi + Bengali) are loaded once at startup.

---

## System Architecture

When a word is submitted via the UI or API, the system routes it through a two-stage pipeline:

```
                        ┌──────────────────────┐
                        │   Input Surface Form  │
                        │      e.g. "walked"    │
                        └──────────┬───────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │        FST ENGINE           │
                    │  (Pynini / OpenFST)         │
                    │  Compose(word, analyzer_fst)│
                    └──────┬──────────────────────┘
                           │
              ─────────────┼──────────────────────
             │ Match found │                       │ OOV / No match
             ▼             │                       ▼
   ┌──────────────────┐    │           ┌──────────────────────┐
   │  FST Analysis    │    │           │   NEURAL FALLBACK    │
   │  walk+V;PST      │    │           │   CharTransformer    │
   └──────────────────┘    │           │   (seq2seq predict)  │
                           │           └──────────────────────┘
                           │                       │
                    ┌──────▼───────────────────────▼──────┐
                    │         FastAPI /analyze             │
                    │   Returns: analyses + fst_graph_raw  │
                    │           + fst_graph_textbook       │
                    └──────────────────────────────────────┘
                                       │
                    ┌──────────────────▼──────────────────┐
                    │         Frontend Web UI              │
                    │   Analysis cards + SVG state graphs  │
                    └──────────────────────────────────────┘
```

---

## Repository Structure

```
Pullinguistics/
├── README.md                        ← You are here
│
└── FST/
    └── fst/
        ├── fsl/                     ← MAIN BACKEND (English FST + Neural + API)
        │   ├── api.py               ← FastAPI server (single entry point for all languages)
        │   ├── fst_builder.py       ← Composes morphotactics + spelling rules + irregulars
        │   ├── morphotactics.py     ← Noun/verb/adj inflection rules (analysis → intermediate)
        │   ├── spelling_rules.py    ← Context-dependent rewrite rules (intermediate → surface)
        │   ├── lexicon.py           ← All stem lists: nouns, verbs, adjectives, prefixes
        │   ├── irregulars.py        ← Hand-coded irregular forms (go→went, good→better→best)
        │   ├── analyzer.py          ← Pynini composition helper
        │   ├── alphabet.py          ← SIGMA_STAR, VOWEL, CONSONANT character classes
        │   ├── evaluate.py          ← Accuracy evaluation against UniMorph data
        │   ├── evaluate_hybrid.py   ← Hybrid system evaluation (FST vs FST+Neural)
        │   ├── data/                ← UniMorph TSV data for training + evaluation
        │   ├── results/             ← Saved evaluation reports (JSON + TXT)
        │   └── neural/
        │       ├── model.py         ← CharTransformer (Encoder-Decoder Transformer)
        │       ├── train.py         ← Training loop with early stopping + checkpointing
        │       ├── predict.py       ← NeuralAnalyzer class (greedy decoding)
        │       ├── dataset.py       ← CharVocab + MorphDataset + DataLoader utils
        │       ├── data_prep.py     ← Converts UniMorph TSVs to (surface, analysis) pairs
        │       ├── data/            ← Train/dev TSV files for the neural model
        │       └── checkpoints/     ← best_model.pt + src_vocab.json + tgt_vocab.json
        │
        ├── bengali_fst/             ← Bengali FST (dictionary-based)
        │   ├── fst_builder.py
        │   ├── lexicon.py           ← Bengali vocabulary dict (surface → CoNLL-U tags)
        │   ├── analyzer.py
        │   └── ...
        │
        ├── hindi_fst/               ← Hindi FST (dictionary-based)
        │   ├── fst_builder.py
        │   ├── lexicon.py
        │   ├── analyzer.py
        │   └── ...
        │
        ├── fst/                     ← Legacy FST (Morpho Challenge 2010 format, not used by API)
        │
        └── website/
            └── frontend/
                ├── index.html       ← Single-page application shell
                ├── script.js        ← All rendering logic, API calls, SVG graph drawing
                └── style.css        ← Dark-mode design system, animations, graph styles
```

---

## The English FST Engine

The English FST is built from four composable components using [Pynini](https://www.openfst.org/twiki/bin/view/GRM/Pynini), a Python wrapper around OpenFST. The transducer is a two-tape machine:
- **Upper tape (input):** Abstract analysis string, e.g., `walk+V;PST`
- **Lower tape (output):** Concrete surface form, e.g., `walked`

Inverting the FST gives the **Analyzer**: it accepts a surface form on the input and produces an analysis on the output.

### 1. Lexicon

**File:** `fsl/lexicon.py`

The lexicon contains categorized lists of English stems, separated by their morphological class and inflectional behaviour:

| Category | Description | Example |
| :--- | :--- | :--- |
| `ALL_REGULAR_NOUNS` | Nouns taking regular `-s` plural | `cat`, `dog`, `house` |
| `REGULAR_VERBS` | Verbs with regular `-ed`, `-ing`, `-s` | `walk`, `talk`, `jump` |
| `SHORT_ADJECTIVES` | 1-2 syllable adjectives with `-er`, `-est` | `big`, `fast`, `tall` |
| `E_ADJECTIVES` | Adjectives ending in silent *e* | `nice`, `large`, `brave` |
| `Y_ADJECTIVES` | Adjectives ending in consonant + *y* | `happy`, `funny`, `busy` |
| `LONG_ADJECTIVES` | Adjectives using analytic `more/most` | `beautiful`, `interesting` |
| `UN_ADJECTIVES` | Adjectives that take `un-` prefix | `fair`, `happy`, `kind` |
| `RE_VERBS` | Verbs that take `re-` prefix | `build`, `write`, `do` |
| `NESS_ADJECTIVES` | Adjectives that take `-ness` suffix | `happy`, `kind`, `sad` |
| `LY_ADJECTIVES` | Adjectives that take `-ly` suffix | `quick`, `slow`, `kind` |

### 2. Morphotactics

**File:** `fsl/morphotactics.py`

The morphotactics FST maps abstract analysis strings to intermediate forms with a boundary marker `^`. This boundary is later consumed by the spelling rules. The `^` marker is crucial: it separates the stem from the suffix so that context-dependent rewrite rules can operate correctly.

**Example flow:**
```
walk+V;PST   →  walk^ed   (morphotactics)
walk^ed      →  walked    (spelling rules, boundary deletion)
```

The morphotactics FST covers the following inflectional paradigms:

**Nouns:**
```
stem+N;SG  →  stem        (singular = no suffix)
stem+N;PL  →  stem^s      (plural)
```

**Verbs:**
```
stem+V;NFIN;IMP+SBJV  →  stem        (base / imperative / subjunctive)
stem+V;PST            →  stem^ed     (simple past)
stem+V;PRS;3;SG       →  stem^s      (3rd person singular)
stem+V;V.PTCP;PRS     →  stem^ing    (present participle)
stem+V;V.PTCP;PST     →  stem^ed     (past participle)
```

**Adjectives:**
```
stem+ADJ       →  stem        (base form)
stem+ADJ;CMPR  →  stem^er     (comparative)
stem+ADJ;SPRL  →  stem^est    (superlative)
```

**Derivational Morphology:**
```
un+stem+ADJ    →  unstem      (un- prefix)
re+stem+V;...  →  restem      (re- prefix)
stem+N;NESS    →  stem^ness   (-ness nominalization)
stem+ADV;LY    →  stem^ly     (-ly adverbialization)
```

### 3. Spelling Rules — Orthographic Rewrite Rules

**File:** `fsl/spelling_rules.py`

The spelling rules are implemented as a **cascade of five context-dependent rewrite rules** using Pynini's `cdrewrite`. They fire on the intermediate form (which contains the `^` boundary marker) and produce the correct surface spelling.

The cascade is composed in order: `R1 @ R2 @ R3 @ R4 @ R5`.

| Rule | Transformation | Left Context | Right Context | Example |
| :--- | :--- | :--- | :--- | :--- |
| **R1** y → ie | `y` becomes `ie` | consonant | `^s` | `fly^s` → `flie^s` → `flies` |
| **R2** y → i | `y` becomes `i` | consonant | `^` + non-`i` letter | `carry^ed` → `carri^ed` → `carried` |
| **R3** e-deletion | silent `e` deleted | consonant | `^` + vowel | `hope^ing` → `hop^ing` → `hoping` |
| **R4** e-insertion | `e` inserted after sibilant | sibilant + `^` | `s` | `watch^s` → `watch^es` → `watches` |
| **R5** `^` deletion | boundary marker removed | — | — | `dog^s` → `dogs` |

> **Note:** Rule R1 fires before R2, preventing the double-firing issue. Rule R3 does not fire if the `e` is preceded by a vowel (e.g., `see^ing` correctly stays `seeing`).

### 4. Irregular Forms

**File:** `fsl/irregulars.py`

Irregular forms that cannot be derived from rules are stored as direct `(analysis, surface)` string-pair mappings. These are loaded into a separate FST using `pynini.string_map()` and unioned with the regular generator.

The irregular list is extensive and covers:

- **Irregular verb paradigms:** `go→went`, `be→was/were/been`, `have→had`, `do→did/done`, `say→said`, `make→made`, `take→took/taken`, `come→came/come`, `run→ran/run`, etc.
- **Irregular noun plurals:** `man→men`, `woman→women`, `child→children`, `mouse→mice`, `goose→geese`, `foot→feet`, `tooth→teeth`, `ox→oxen`, etc.
- **Irregular adjective comparatives:** `good→better→best`, `bad→worse→worst`, `far→farther→farthest`, `little→less→least`, etc.

### 5. FST Composition & Inversion

**File:** `fsl/fst_builder.py`

The final FST is assembled in four explicit steps:

```python
# Step 1: morphotactics (analysis → intermediate)
morphotactics = build_morphotactics()

# Step 2: spelling rules (intermediate → surface)
spelling_rules = build_spelling_rules()

# Step 3: compose the two (analysis → surface)
regular_generator = morphotactics @ spelling_rules

# Step 4: union with hand-coded irregulars
generator = pynini.union(regular_generator, irregulars_fst)

# Step 5: invert to get the analyzer (surface → analysis)
analyzer = pynini.invert(generator)
```

The resulting `analyzer` FST accepts a surface word and outputs all valid morphological analyses, including ambiguous ones (e.g., `flies` → `{fly+V;PRS;3;SG, fly+N;PL}`).

---

## The Neural Fallback (CharTransformer)

**Directory:** `fsl/neural/`

When the FST returns no results for a word (OOV), the `NeuralAnalyzer` is called. It is a character-level sequence-to-sequence machine translation model.

### Architecture

**File:** `neural/model.py` — `CharTransformer` class

The model is a compact **Transformer Encoder-Decoder** (Vaswani et al., 2017), scaled down for short character sequences (typical word length: 5–20 characters).

| Hyperparameter | Value |
| :--- | :--- |
| Embedding dimension (`d_model`) | 128 |
| Attention heads (`nhead`) | 4 |
| Encoder layers | 3 |
| Decoder layers | 3 |
| Feedforward dimension | 512 |
| Dropout | 0.1 |

**Data representation:** Every string (both source and target) is broken into individual characters. Four special tokens are reserved:

| Token | Index | Meaning |
| :--- | :--- | :--- |
| `<PAD>` | 0 | Padding for batch alignment |
| `<SOS>` | 1 | Start of sequence |
| `<EOS>` | 2 | End of sequence |
| `<UNK>` | 3 | Unknown character (unseen at train time) |

**Positional Encoding:** Because Transformers are order-agnostic, sinusoidal positional encodings (sine/cosine waves of varying frequencies) are added to each character embedding before the attention layers. This allows the model to distinguish `'e'` in position 2 from `'e'` in position 5.

**Causal Masking:** During training, the decoder uses an upper-triangular boolean mask to prevent any position from attending to future positions. This ensures teacher forcing is applied correctly and the model generates outputs auto-regressively at inference time.

### Training

**File:** `neural/train.py`

Training is performed on `(surface_form, analysis)` pairs derived from the UniMorph English dataset. Key details:

- **Optimizer:** Adam with β₁=0.9, β₂=0.98
- **Learning Rate:** 0.001 with `ReduceLROnPlateau` scheduling (halves LR when validation loss plateaus for 3 epochs)
- **Batch Size:** 256 pairs per step
- **Max Epochs:** 50, with **Early Stopping** (patience = 7 epochs without validation improvement)
- **Teacher Forcing:** During training, the decoder receives the gold target sequence as input (shifted right), not its own predictions. This stabilizes training.
- **Gradient Clipping:** `max_norm=1.0` prevents exploding gradients during backpropagation.
- **Checkpointing:** The checkpoint with the best validation loss is saved as `checkpoints/best_model.pt`.

### Inference — Greedy Decoding

**File:** `neural/predict.py` — `NeuralAnalyzer.analyze()`

At inference time, the model uses **Autoregressive Greedy Decoding**:

1. Encode the source word characters into the encoder memory tensor.
2. Initialize the decoder with `[<SOS>]`.
3. **Loop:** Feed the current output sequence into the decoder. Take the character with the highest logit (`argmax`) at the last position. Append it to the output.
4. **Stop** when `<EOS>` is predicted or the maximum output length (64) is reached.
5. Decode the integer indices back to a string, strip special tokens, return the analysis.

```
Input:  "retweeted"
        ↓ (encode)
Encoder memory: (1, 9, 128) tensor
        ↓
Decoder step 1: [<SOS>]           → argmax → 'r'
Decoder step 2: [<SOS>, 'r']      → argmax → 'e'
Decoder step 3: [<SOS>, 'r', 'e'] → argmax → 't'
...
Decoder step N:  [<SOS>, 'r','e','t','w','e','e','t'] → argmax → '+'
...                                                      → argmax → 'V'
...                                                      → argmax → ';'
...                                                      → argmax → 'P','S','T'
...                                                      → argmax → <EOS>
Output: "retweet+V;PST"
```

---

## Hindi & Bengali FSTs

**Directories:** `hindi_fst/` and `bengali_fst/`

The Hindi and Bengali systems follow a **dictionary-based FST** architecture. Instead of compositional morphotactics, these systems rely on a hand-curated `VOCABULARY` dictionary that maps surface forms directly to CoNLL-U formatted tags.

The FST is built from `pynini.string_map(VOCABULARY)`, creating direct (surface → analysis) transduction paths for each known word. Analysis tags are structured as `lemma+UPOS;features`.

When a Hindi or Bengali word is submitted:
1. It is composed with the language's FST. If successful, the analysis comes from the FST path.
2. If not in the FST, the `VOCABULARY` dict is checked directly.
3. If still not found, a heuristic rule-based fallback (`generate_conllu_line`) provides a best-guess analysis based on the word's surface form characteristics.

> **Note:** Hindi and Bengali currently do not have a neural fallback. The dictionary FST + heuristic fallback provides basic coverage.

---

## The REST API (FastAPI)

**File:** `fsl/api.py`

The API is built with **FastAPI** and served via **Uvicorn**. All three language models (English FST + Neural, Bengali FST, Hindi FST) are loaded once during the application lifespan event and kept in memory in a `_state` dictionary.

### Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Returns server status and loaded language flags |
| `POST` | `/analyze` | Analyze a single word |
| `POST` | `/analyze/batch` | Analyze a list of words |

### Request Schema

```json
POST /analyze
{
  "word": "walked",
  "language": "eng"   // "eng" | "hin" | "ben"
}
```

### Response Schema

```json
{
  "word": "walked",
  "language": "eng",
  "source": "FST",   // "FST" | "Neural" | "Dictionary" | "Heuristic"
  "analyses": [
    { "raw": "walk+V;PST", "lemma": "walk", "features": "V;PST" }
  ],
  "fst_graph_raw": { ... },       // Raw OpenFST lattice for the "Raw Graph"
  "fst_graph_textbook": { ... }   // Synthetically aligned graph for the "Textbook Graph"
}
```

### Graph Object Schema

```json
{
  "num_states": 6,
  "num_arcs": 5,
  "start_state": 0,
  "states": [
    {
      "id": 0, "is_start": true, "is_final": false,
      "arcs": [{ "src": 0, "dst": 1, "input_label": "w", "output_label": "w" }]
    }
  ],
  "traversal": [
    { "state": 0, "input_char": "w", "output_char": "w", "next_state": 1 }
  ]
}
```

---

## The Frontend UI

**Directory:** `website/frontend/`

The single-page application is built with pure HTML, CSS, and Vanilla JavaScript (no frameworks). Key design decisions:

- **Dark Mode First**: Deep dark backgrounds (`#080c14`) with vibrant accent colors.
- **Ambient Background**: Animated gradient orbs for visual depth.
- **Glassmorphism Cards**: `backdrop-filter: blur()` panels for a modern look.
- **Language-Aware UI**: The input placeholder, example word chips, and font family (Latin / Noto Sans Bengali / Noto Sans Devanagari) all swap dynamically when the language selector changes.
- **Source Badge Color Coding**: The pill badge showing `FST`, `Neural`, `Dictionary`, or `Heuristic` changes color depending on the analysis source.

---

## Dual Graph Visualization

One of the most distinctive features of Pullinguistics is its dual-graph visualization for every FST query.

### Raw OpenFST Graph (`fst_graph_raw`)
Generated directly from the Pynini lattice via `_extract_graph(lattice)`. This is an exact dump of the internal FST state machine, including epsilon transitions and any structural artifacts from Pynini's internal lattice composition. It shows the true mathematical structure of the computation.

### Textbook Alignment Graph (`fst_graph_textbook`)
Generated by `_build_textbook_graph(word, analysis)`. This graph is **synthetically constructed** — not extracted from the FST. It provides a perfectly human-readable, 1-to-1 character alignment:

```
Example: "walked" → "walk+V;PST"

q0 ─w:w─► q1 ─a:a─► q2 ─l:l─► q3 ─k:k─► q4 ─e:ε─► q5 ─d:ε─► q6 ─ε:+V;PST─► q7(final)
```

Both SVG graphs are rendered in the browser with:
- **Color-coded arc labels**: Input tape in pink, output tape in green, separator `:` in white.
- **Traversal highlighting**: States and arcs on the accepted path are highlighted in purple.
- **Linear layout**: All states laid out in a single horizontal row, eliminating arc overlap.
- **Dynamic spacing**: Arc label spacing computed at render time based on the longest label in the graph.

---

## Evaluation & Performance

Evaluated on **5,000 words** from the UniMorph English dataset:

| Metric | Pure FST | Hybrid (FST + Neural) | Δ |
| :--- | :---: | :---: | :---: |
| **Coverage** | 36.9% | **100.0%** | +63.1% |
| **Accuracy** | 25.4% | **74.3%** | +48.9% |
| **OOV Errors** | 3,156 | **0** | −3,156 |
| **Ambiguity** (avg analyses/word) | 1.18 | 1.07 | −0.11 |
| **Neural wins** | — | 2,374 | — |
| **Neural losses** | — | 637 | — |

The FST alone achieves only 36.9% coverage because it can only analyze words explicitly in its lexicon. The neural model raises this to 100% while adding net +1,737 correct analyses (2,374 wins − 637 losses).

### Neural Failure Modes

The 637 neural losses fall into predictable categories:

| Failure Type | Example | Expected | Got |
| :--- | :--- | :--- | :--- |
| **POS Ambiguity** | `wrench` | `wrench+V;NFIN;IMP+SBJV` | `wrench+N;SG` |
| **Naive lemma recovery** | `sped` | `speed+V;PST` | `spe+V;PST` |
| **Gerund vs. noun** | `lining` | `line+V;V.PTCP;PRS` | `lining+N;SG` |
| **Hallucination** | `MSRP` | `MSRP+N;SG` | `7+N;SG` |

---

## Getting Started

### Prerequisites

| Dependency | Version | Notes |
| :--- | :--- | :--- |
| Python | 3.10+ | Required |
| pynini | 2.1.5+ | Requires Linux / macOS / WSL |
| torch | 2.0+ | CPU or CUDA |
| fastapi | 0.100+ | |
| uvicorn | Latest | ASGI server |
| pydantic | v2 | |

Install all dependencies:
```bash
pip install pynini torch fastapi uvicorn pydantic
```

### 1. Start the Backend API

```bash
cd FST/fst/fsl
uvicorn api:app --reload --port 8000
```

The server will print model loading progress. When you see `ALL MODELS READY — eng / ben / hin`, the API is ready to receive requests at `http://localhost:8000`.

### 2. Serve the Frontend

```bash
cd FST/fst/website/frontend
python -m http.server 3000
```

Navigate to `http://localhost:3000` in your browser.

### 3. (Optional) Retrain the Neural Model

```bash
cd FST/fst/fsl
python neural/train.py
```

This will load UniMorph data from `neural/data/`, train the CharTransformer for up to 50 epochs with early stopping, and save the best checkpoint to `neural/checkpoints/best_model.pt`.

### 4. (Optional) Run the Hybrid Evaluation

```bash
cd FST/fst/fsl
python evaluate_hybrid.py
```

Results are saved to `results/hybrid_comparison.json` and `results/hybrid_comparison.txt`.

---

## API Reference

### `GET /health`
```json
{
  "status": "ok",
  "languages": { "eng": true, "ben": true, "hin": true }
}
```

### `POST /analyze`

**Request:**
```json
{ "word": "happiness", "language": "eng" }
```

**Response:**
```json
{
  "word": "happiness",
  "language": "eng",
  "source": "FST",
  "analyses": [
    { "raw": "happy+N;NESS", "lemma": "happy", "features": "N;NESS" }
  ],
  "fst_graph_raw": { "num_states": 14, "num_arcs": 13, "..." },
  "fst_graph_textbook": { "num_states": 10, "num_arcs": 9, "..." }
}
```

### `POST /analyze/batch`

**Request:**
```json
{ "words": ["walked", "running", "happiness"], "language": "eng" }
```

**Response:** Array of `AnalyzeResponse` objects (same schema as above).

---

*Built with ❤️ using Pynini, PyTorch, and FastAPI.*
