"""
dataset.py - Character-Level Dataset & Vocabulary

Handles:
  - Building character vocabularies from training data
  - Encoding/decoding between strings and integer tensors
  - PyTorch Dataset class for batched training
  
Special tokens:
  <PAD> = 0  (padding)
  <SOS> = 1  (start of sequence)
  <EOS> = 2  (end of sequence)
  <UNK> = 3  (unknown character)
"""
import os
import json
import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence


# Special token indices
PAD_IDX = 0
SOS_IDX = 1
EOS_IDX = 2
UNK_IDX = 3

SPECIAL_TOKENS = ["<PAD>", "<SOS>", "<EOS>", "<UNK>"]


class CharVocab:
    """
    Character-level vocabulary.
    
    Maps individual characters to integer indices and back.
    Built from a list of strings (words or analyses).
    """
    
    def __init__(self):
        self.char2idx = {}
        self.idx2char = {}
        self.size = 0
        
        # Add special tokens
        for token in SPECIAL_TOKENS:
            self._add(token)
    
    def _add(self, char):
        """Add a character to the vocabulary."""
        if char not in self.char2idx:
            idx = len(self.char2idx)
            self.char2idx[char] = idx
            self.idx2char[idx] = char
            self.size = len(self.char2idx)
    
    def build(self, strings):
        """
        Build vocabulary from a list of strings.
        Each string is split into individual characters.
        """
        for s in strings:
            for char in s:
                self._add(char)
        print(f"  Vocab size: {self.size} characters")
    
    def encode(self, string):
        """
        Encode a string into a list of indices.
        Adds <SOS> at the start and <EOS> at the end.
        """
        indices = [SOS_IDX]
        for char in string:
            indices.append(self.char2idx.get(char, UNK_IDX))
        indices.append(EOS_IDX)
        return indices
    
    def decode(self, indices):
        """
        Decode a list of indices back into a string.
        Strips <SOS>, <EOS>, and <PAD> tokens.
        """
        chars = []
        for idx in indices:
            if idx == EOS_IDX:
                break
            if idx in (PAD_IDX, SOS_IDX):
                continue
            char = self.idx2char.get(idx, "?")
            chars.append(char)
        return "".join(chars)
    
    def save(self, filepath):
        """Save vocabulary to a JSON file."""
        data = {
            "char2idx": self.char2idx,
            "idx2char": {str(k): v for k, v in self.idx2char.items()},
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self, filepath):
        """Load vocabulary from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.char2idx = data["char2idx"]
        self.idx2char = {int(k): v for k, v in data["idx2char"].items()}
        self.size = len(self.char2idx)


class MorphDataset(Dataset):
    """
    PyTorch Dataset for character-level morphological data.
    
    Each sample is a (source_tensor, target_tensor) pair where:
      - source = character indices of the surface form  (e.g., "walked")
      - target = character indices of the analysis      (e.g., "walk+V;PST")
    """
    
    def __init__(self, pairs, src_vocab, tgt_vocab):
        """
        Args:
            pairs: list of (surface_form, analysis) string tuples
            src_vocab: CharVocab for source (surface forms)
            tgt_vocab: CharVocab for target (analyses)
        """
        self.pairs = pairs
        self.src_vocab = src_vocab
        self.tgt_vocab = tgt_vocab
    
    def __len__(self):
        return len(self.pairs)
    
    def __getitem__(self, idx):
        surface, analysis = self.pairs[idx]
        src_indices = self.src_vocab.encode(surface)
        tgt_indices = self.tgt_vocab.encode(analysis)
        return (
            torch.tensor(src_indices, dtype=torch.long),
            torch.tensor(tgt_indices, dtype=torch.long),
        )


def collate_fn(batch):
    """
    Custom collate function for DataLoader.
    Pads source and target sequences to the same length within a batch.
    
    Returns:
        src_batch: (batch_size, max_src_len) padded source tensor
        tgt_batch: (batch_size, max_tgt_len) padded target tensor
    """
    src_batch, tgt_batch = zip(*batch)
    src_padded = pad_sequence(src_batch, batch_first=True, padding_value=PAD_IDX)
    tgt_padded = pad_sequence(tgt_batch, batch_first=True, padding_value=PAD_IDX)
    return src_padded, tgt_padded


def build_vocabs(train_pairs):
    """
    Build source and target vocabularies from training data.
    
    Args:
        train_pairs: list of (surface_form, analysis) tuples
        
    Returns:
        (src_vocab, tgt_vocab)
    """
    surfaces, analyses = zip(*train_pairs)
    
    print("Building source vocabulary (surface forms)...")
    src_vocab = CharVocab()
    src_vocab.build(surfaces)
    
    print("Building target vocabulary (analyses)...")
    tgt_vocab = CharVocab()
    tgt_vocab.build(analyses)
    
    return src_vocab, tgt_vocab
