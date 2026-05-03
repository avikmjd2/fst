"""
train.py - Neural Model Training Loop

Trains the CharTransformer on (surface_form -> analysis) pairs.

Features:
  - Teacher forcing during training
  - Validation loss tracking
  - Early stopping to prevent overfitting
  - Model checkpointing (saves best model)
  - Learning rate scheduling

Usage (from fsl/ directory):
    python neural/train.py
"""
import os
import sys
import time
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from neural.data_prep import load_tsv, prepare_data
from neural.dataset import (
    MorphDataset, CharVocab, build_vocabs, collate_fn,
    PAD_IDX, SOS_IDX, EOS_IDX,
)
from neural.model import CharTransformer


# ── Hyperparameters ─────────────────────────────────────────────────

BATCH_SIZE = 256
LEARNING_RATE = 0.001
MAX_EPOCHS = 50
PATIENCE = 7          # early stopping patience (epochs without improvement)
D_MODEL = 128         # embedding / transformer hidden dimension
NHEAD = 4             # number of attention heads
NUM_ENC_LAYERS = 3    # encoder transformer layers
NUM_DEC_LAYERS = 3    # decoder transformer layers
DIM_FEEDFORWARD = 512 # feedforward hidden size
DROPOUT = 0.1

MODEL_DIR = os.path.join(os.path.dirname(__file__), "checkpoints")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def train_epoch(model, dataloader, optimizer, criterion, device):
    """Train for one epoch. Returns average loss."""
    model.train()
    total_loss = 0
    num_batches = 0
    
    for src, tgt in dataloader:
        src = src.to(device)
        tgt = tgt.to(device)
        
        # Teacher forcing: input = tgt[:-1], target = tgt[1:]
        tgt_input = tgt[:, :-1]   # everything except last token
        tgt_output = tgt[:, 1:]   # everything except first token (<SOS>)
        
        optimizer.zero_grad()
        logits = model(src, tgt_input)
        
        # Reshape for cross-entropy: (batch * seq_len, vocab_size) vs (batch * seq_len)
        loss = criterion(
            logits.reshape(-1, logits.size(-1)),
            tgt_output.reshape(-1),
        )
        
        loss.backward()
        # Gradient clipping to prevent exploding gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        
        total_loss += loss.item()
        num_batches += 1
    
    return total_loss / max(num_batches, 1)


def evaluate(model, dataloader, criterion, device):
    """Evaluate on validation set. Returns average loss."""
    model.eval()
    total_loss = 0
    num_batches = 0
    
    with torch.no_grad():
        for src, tgt in dataloader:
            src = src.to(device)
            tgt = tgt.to(device)
            
            tgt_input = tgt[:, :-1]
            tgt_output = tgt[:, 1:]
            
            logits = model(src, tgt_input)
            loss = criterion(
                logits.reshape(-1, logits.size(-1)),
                tgt_output.reshape(-1),
            )
            
            total_loss += loss.item()
            num_batches += 1
    
    return total_loss / max(num_batches, 1)


def train(data_dir=None, model_dir=None):
    """
    Full training pipeline.
    
    1. Load/prepare data
    2. Build vocabularies
    3. Create model
    4. Train with early stopping
    5. Save best model + vocabularies
    """
    if data_dir is None:
        data_dir = DATA_DIR
    if model_dir is None:
        model_dir = MODEL_DIR
    
    os.makedirs(model_dir, exist_ok=True)
    
    # ── Device ──────────────────────────────────────────────────────
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    print()
    
    # ── Load data ───────────────────────────────────────────────────
    train_path = os.path.join(data_dir, "train.tsv")
    dev_path = os.path.join(data_dir, "dev.tsv")
    
    if not os.path.exists(train_path):
        print("Training data not found. Generating from UniMorph...")
        result = prepare_data(
            data_dir=os.path.join(os.path.dirname(__file__), "..", "data"),
            output_dir=data_dir,
        )
        if result is None:
            print("ERROR: Could not prepare training data.")
            return
    
    print("Loading training data...")
    train_pairs = load_tsv(train_path)
    dev_pairs = load_tsv(dev_path)
    print(f"  Train: {len(train_pairs)} pairs")
    print(f"  Dev:   {len(dev_pairs)} pairs")
    print()
    
    # ── Build vocabularies ──────────────────────────────────────────
    src_vocab, tgt_vocab = build_vocabs(train_pairs)
    
    # Also include dev chars in vocab (to handle unseen chars gracefully)
    for surface, analysis in dev_pairs:
        for ch in surface:
            src_vocab._add(ch)
        for ch in analysis:
            tgt_vocab._add(ch)
    
    # Save vocabularies
    src_vocab.save(os.path.join(model_dir, "src_vocab.json"))
    tgt_vocab.save(os.path.join(model_dir, "tgt_vocab.json"))
    print(f"  Source vocab: {src_vocab.size} chars")
    print(f"  Target vocab: {tgt_vocab.size} chars")
    print()
    
    # ── Create datasets and dataloaders ─────────────────────────────
    train_dataset = MorphDataset(train_pairs, src_vocab, tgt_vocab)
    dev_dataset = MorphDataset(dev_pairs, src_vocab, tgt_vocab)
    
    train_loader = DataLoader(
        train_dataset, batch_size=BATCH_SIZE, shuffle=True,
        collate_fn=collate_fn, num_workers=0,
    )
    dev_loader = DataLoader(
        dev_dataset, batch_size=BATCH_SIZE, shuffle=False,
        collate_fn=collate_fn, num_workers=0,
    )
    
    # ── Create model ────────────────────────────────────────────────
    model = CharTransformer(
        src_vocab_size=src_vocab.size,
        tgt_vocab_size=tgt_vocab.size,
        d_model=D_MODEL,
        nhead=NHEAD,
        num_encoder_layers=NUM_ENC_LAYERS,
        num_decoder_layers=NUM_DEC_LAYERS,
        dim_feedforward=DIM_FEEDFORWARD,
        dropout=DROPOUT,
    ).to(device)
    
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Model parameters: {total_params:,} total, {trainable_params:,} trainable")
    print()
    
    # ── Loss, optimizer, scheduler ──────────────────────────────────
    criterion = nn.CrossEntropyLoss(ignore_index=PAD_IDX)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE, betas=(0.9, 0.98))
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=0.5, patience=3,
    )
    
    # ── Training loop with early stopping ───────────────────────────
    best_val_loss = float("inf")
    patience_counter = 0
    best_model_path = os.path.join(model_dir, "best_model.pt")
    
    print("=" * 60)
    print(f"{'Epoch':>6} | {'Train Loss':>11} | {'Val Loss':>11} | {'Time':>7} | {'LR':>10}")
    print("-" * 60)
    
    for epoch in range(1, MAX_EPOCHS + 1):
        start_time = time.time()
        
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss = evaluate(model, dev_loader, criterion, device)
        
        elapsed = time.time() - start_time
        lr = optimizer.param_groups[0]["lr"]
        
        print(f"{epoch:>6} | {train_loss:>11.4f} | {val_loss:>11.4f} | {elapsed:>5.1f}s | {lr:>10.6f}")
        
        # Learning rate scheduling
        scheduler.step(val_loss)
        
        # Early stopping check
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            # Save best model
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "val_loss": val_loss,
                "src_vocab_size": src_vocab.size,
                "tgt_vocab_size": tgt_vocab.size,
                "d_model": D_MODEL,
                "nhead": NHEAD,
                "num_encoder_layers": NUM_ENC_LAYERS,
                "num_decoder_layers": NUM_DEC_LAYERS,
                "dim_feedforward": DIM_FEEDFORWARD,
                "dropout": DROPOUT,
            }, best_model_path)
        else:
            patience_counter += 1
            if patience_counter >= PATIENCE:
                print(f"\nEarly stopping at epoch {epoch} (no improvement for {PATIENCE} epochs)")
                break
    
    print("=" * 60)
    print(f"Best validation loss: {best_val_loss:.4f}")
    print(f"Model saved to: {best_model_path}")
    print()


if __name__ == "__main__":
    train()
