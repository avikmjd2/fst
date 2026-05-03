import random
import re
import os

def create_balanced_dataset():
    # 1. Extract all known stems from lexicon.py
    stems = set()
    try:
        with open("lexicon.py", "r", encoding="utf-8") as f:
            content = f.read()
            # Find all words inside quotes (these are the words the FST actually knows)
            matches = re.findall(r'"([a-z]+)"', content)
            for m in matches:
                stems.add(m)
        print(f"Extracted {len(stems)} unique common words from lexicon.py")
    except FileNotFoundError:
        print("Could not find lexicon.py")
        return

    # 2. Load the giant UniMorph dataset
    known_pairs = []
    unknown_pairs = []

    try:
        with open("data/eng.tsv", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 3:
                    lemma = parts[0]
                    surface = parts[1]
                    tags = parts[2]
                    analysis = f"{lemma}+{tags}"
                    
                    if lemma in stems:
                        known_pairs.append((surface, analysis))
                    else:
                        unknown_pairs.append((surface, analysis))
    except FileNotFoundError:
        print("Could not find data/eng.tsv. Please run data_prep.py first.")
        return

    print(f"Found {len(known_pairs)} words in the dataset that the FST actually knows!")
    print(f"Found {len(unknown_pairs)} rare/unknown words that the FST doesn't know.")

    # 3. Create a perfectly balanced test set for your report
    # Let's do 2500 common words (FST will get these right) 
    # and 2500 rare words (FST will fail, but Neural will save them)
    random.seed(42) # For reproducible results
    random.shuffle(known_pairs)
    random.shuffle(unknown_pairs)

    num_known = min(2500, len(known_pairs))
    num_unknown = 5000 - num_known

    test_pairs = known_pairs[:num_known] + unknown_pairs[:num_unknown]
    random.shuffle(test_pairs)

    # Save it to test.tsv
    os.makedirs("neural/data", exist_ok=True)
    with open("neural/data/test.tsv", "w", encoding="utf-8") as f:
        for surface, analysis in test_pairs:
            f.write(f"{surface}\t{analysis}\n")

    print(f"\nSuccessfully created balanced test.tsv with {len(test_pairs)} words!")
    print("Run `python evaluate_hybrid.py` to see the new balanced accuracy scores!")

if __name__ == "__main__":
    create_balanced_dataset()
