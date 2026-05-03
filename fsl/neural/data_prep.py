"""
data_prep.py - Training Data Generation

Generates training data for the neural fallback model by:
1. Loading UniMorph data (surface form -> analysis pairs)
2. Splitting into train/dev/test sets
3. Saving as TSV files that the neural model can consume

The neural model learns to map: surface form -> morphological analysis
    e.g., "walked" -> "walk+V;PST"
"""
import os
import sys
import random

# Add parent directory to path so we can import fsl modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data_loader import download_unimorph, load_unimorph


def prepare_data(data_dir="data", output_dir="neural/data", seed=42):
    """
    Prepare train/dev/test TSV files for neural model training.
    
    Each line in the TSV is: surface_form\tanalysis
    e.g., walked\twalk+V;PST
    
    Args:
        data_dir: directory containing UniMorph data
        output_dir: directory to save train/dev/test TSV files
        seed: random seed for reproducibility
        
    Returns:
        dict with paths to train, dev, test files and counts
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Download UniMorph data if needed
    data_path = download_unimorph(data_dir)
    if data_path is None:
        print("ERROR: Could not download UniMorph data.")
        return None
    
    # Load entries
    entries = load_unimorph(data_path)
    if not entries:
        print("ERROR: No data loaded.")
        return None
    
    # Create (surface_form, analysis) pairs
    # Deduplicate: same surface form can map to different analyses
    pairs = []
    seen = set()
    for entry in entries:
        key = (entry["form"], entry["analysis"])
        if key not in seen:
            pairs.append(key)
            seen.add(key)
    
    print(f"Total unique (surface, analysis) pairs: {len(pairs)}")
    
    # Shuffle and split: 80% train, 10% dev, 10% test
    random.seed(seed)
    random.shuffle(pairs)
    
    # Downsample to 50,000 words max for faster training
    pairs = pairs[:50000]
    print(f"Downsampled to: {len(pairs)} pairs for faster training")
    
    n = len(pairs)
    train_end = int(0.8 * n)
    dev_end = int(0.9 * n)
    
    train_pairs = pairs[:train_end]
    dev_pairs = pairs[train_end:dev_end]
    test_pairs = pairs[dev_end:]
    
    # Save to TSV files
    splits = {
        "train": train_pairs,
        "dev": dev_pairs,
        "test": test_pairs,
    }
    
    paths = {}
    for split_name, split_pairs in splits.items():
        filepath = os.path.join(output_dir, f"{split_name}.tsv")
        with open(filepath, "w", encoding="utf-8") as f:
            for surface, analysis in split_pairs:
                f.write(f"{surface}\t{analysis}\n")
        paths[split_name] = filepath
        print(f"  {split_name}: {len(split_pairs)} pairs -> {filepath}")
    
    return {
        "paths": paths,
        "counts": {k: len(v) for k, v in splits.items()},
    }


def load_tsv(filepath):
    """
    Load a TSV file of (surface, analysis) pairs.
    
    Returns:
        list of (surface_form, analysis) tuples
    """
    pairs = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                pairs.append((parts[0], parts[1]))
    return pairs


if __name__ == "__main__":
    # Run from the fsl/ directory
    result = prepare_data()
    if result:
        print(f"\nData preparation complete!")
        for split, count in result["counts"].items():
            print(f"  {split}: {count} pairs")
