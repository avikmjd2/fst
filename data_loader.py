"""
Data Loader: utilities for loading and parsing UniMorph datasets.

UniMorph format (TSV):
    lemma\tinflected_form\tfeatures
    run\truns\tV;IND;PRS;3;SG

We map UniMorph feature bundles to our internal tag format:
    lemma+POS;FEATURES
"""
import os
import csv
import urllib.request


# UniMorph feature bundle -> our internal tag format
# UniMorph uses semicolon-separated features; we map common patterns
UNIMORPH_TAG_MAP = {
    # Verbs
    "V;NFIN": "V;NFIN",
    "V;PST": "V;PST",
    "V;IND;PRS;3;SG": "V;PRS;3;SG",
    "V;IND;PRS;1;SG": "V;NFIN",       # "I walk", same as base
    "V;IND;PRS;2": "V;NFIN",          # "you walk", same as base
    "V;IND;PRS;1;PL": "V;NFIN",       # "we walk"
    "V;IND;PRS;3;PL": "V;NFIN",       # "they walk"
    "V;V.PTCP;PRS": "V;V.PTCP;PRS",
    "V;V.PTCP;PST": "V;V.PTCP;PST",
    # be - special cases
    "V;IND;PRS;1;SG": "V;PRS;1;SG",
    "V;IND;PST;1;SG": "V;PST;1;SG",
    "V;IND;PST;3;SG": "V;PST;3;SG",
    "V;IND;PST;2": "V;PST;2",
    "V;IND;PST;1;PL": "V;PST;1;PL",
    "V;IND;PST;3;PL": "V;PST;3;PL",
    # Nouns
    "N;SG": "N;SG",
    "N;PL": "N;PL",
    # Adjectives
    "ADJ": "ADJ",
    "ADJ;CMPR": "ADJ;CMPR",
    "ADJ;SPRL": "ADJ;SPRL",
}


def download_unimorph(dest_dir="data"):
    """
    Download the UniMorph English dataset from GitHub.
    Saves to dest_dir/eng.tsv
    """
    os.makedirs(dest_dir, exist_ok=True)
    url = "https://raw.githubusercontent.com/unimorph/eng/master/eng"
    dest_path = os.path.join(dest_dir, "eng.tsv")

    if os.path.exists(dest_path):
        print(f"UniMorph data already exists at {dest_path}")
        return dest_path

    print(f"Downloading UniMorph English data from {url}...")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"Saved to {dest_path}")
    except Exception as e:
        print(f"Download failed: {e}")
        print("Please manually download from https://github.com/unimorph/eng")
        print(f"and save the 'eng' file as {dest_path}")
        return None

    return dest_path


def load_unimorph(filepath="data/eng.tsv"):
    """
    Load UniMorph TSV data.

    Returns:
        List of dicts: [{"lemma": str, "form": str, "features": str, "analysis": str}, ...]
        where 'analysis' is our internal format: "lemma+MAPPED_FEATURES"
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        print("Run download_unimorph() first or provide the correct path.")
        return []

    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue

            lemma = parts[0].strip().lower()
            form = parts[1].strip().lower()
            features = parts[2].strip()

            # Map to our internal tag format
            internal_tag = UNIMORPH_TAG_MAP.get(features, features)
            analysis = f"{lemma}+{internal_tag}"

            entries.append({
                "lemma": lemma,
                "form": form,
                "features": features,
                "analysis": analysis,
            })

    print(f"Loaded {len(entries)} entries from {filepath}")
    return entries


def split_data(entries, train_ratio=0.8, seed=42):
    """
    Split entries into train and test sets.

    Args:
        entries: list of dicts from load_unimorph()
        train_ratio: fraction for training
        seed: random seed for reproducibility

    Returns:
        (train_entries, test_entries)
    """
    import random
    random.seed(seed)
    shuffled = entries.copy()
    random.shuffle(shuffled)
    split_idx = int(len(shuffled) * train_ratio)
    return shuffled[:split_idx], shuffled[split_idx:]


def get_test_words(entries):
    """Extract unique (form, analysis) pairs for evaluation."""
    pairs = set()
    for e in entries:
        pairs.add((e["form"], e["analysis"]))
    return list(pairs)
