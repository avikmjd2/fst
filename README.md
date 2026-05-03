# FST-Based Morphological Analyzer

Morphological analyzers for **English**, **Hindi**, and **Bengali** using Finite State Transducers (FST) and Finite State Lexicons (FSL), with an optional neural network fallback.

## Project Structure

```
fst/
├── fst/              # English rule-based FST (pynini)
├── fsl/              # English FSL + neural hybrid
│   ├── neural/       # Character-level Transformer model
│   └── results/      # Hybrid evaluation results
├── hindi_fsl/        # Hindi FSL (CoNLL-U)
├── bengali_fsl/      # Bengali FSL (CoNLL-U)
└── README.md
```

## Accuracy Summary

| System | Dataset | Accuracy |
|--------|---------|----------|
| English FST (pure) | test_data.txt | 0.7% |
| English Hybrid (FST + Neural) | test_data.txt | 78.1% |
| Hindi FSL | test.txt | 92.2% |
| Bengali FSL (train) | train_data.txt | 100.0% |
| Bengali FSL (test) | test.txt | 74.4% |

## Setup

**Requires WSL/Linux** (pynini is not available on native Windows).

```bash
# Clone
git clone https://github.com/avikmjd2/fst

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install pynini

# Run Hindi FSL
cd hindi_fsl && python main.py

# Run Bengali FSL
cd bengali_fsl && python main.py

# Test accuracy
python test.py                    # test on test.txt
python test.py --show-wrong-only  # show only mismatches
```

Alternatively, with **conda**:
```bash
conda activate <env_name>
conda install -c conda-forge pynini
python main.py
```

## Neural Network

The `fsl/neural/` module contains a **Character-Level Transformer** (encoder-decoder) that acts as a fallback for OOV words. It maps surface form characters → morphological analysis characters, achieving 78.1% hybrid accuracy on English (vs 0.7% pure FST).
