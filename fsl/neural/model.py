"""
model.py - Character-Level Transformer for Morphological Analysis

Architecture (Wu et al., 2021 inspired):
  - Encoder: character embeddings + positional encoding -> Transformer encoder layers
  - Decoder: character embeddings + positional encoding -> Transformer decoder layers  
  - Output:  linear projection -> softmax over target vocabulary

The model learns to transduce:
    surface form characters -> analysis characters
    e.g., ['w','a','l','k','e','d'] -> ['w','a','l','k','+','V',';','P','S','T']
"""
import math
import torch
import torch.nn as nn

from neural.dataset import PAD_IDX


class PositionalEncoding(nn.Module):
    """
    Sinusoidal positional encoding (Vaswani et al., 2017).
    
    Adds position information to character embeddings since
    Transformers have no inherent notion of sequence order.
    """
    
    def __init__(self, d_model, max_len=256, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)  # (1, max_len, d_model)
        self.register_buffer("pe", pe)
    
    def forward(self, x):
        """
        Args:
            x: (batch_size, seq_len, d_model)
        """
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


class CharTransformer(nn.Module):
    """
    Character-level Transformer encoder-decoder for morphological analysis.
    
    Hyperparameters are tuned for character-level tasks where sequences
    are short (typically 5-20 characters). We use smaller dimensions
    than standard NMT Transformers.
    
    Args:
        src_vocab_size: source vocabulary size (surface form characters)
        tgt_vocab_size: target vocabulary size (analysis characters)
        d_model:        embedding dimension (default: 128)
        nhead:          number of attention heads (default: 4)
        num_encoder_layers: encoder Transformer layers (default: 3)
        num_decoder_layers: decoder Transformer layers (default: 3)
        dim_feedforward:    feedforward hidden size (default: 512)
        dropout:        dropout rate (default: 0.1)
    """
    
    def __init__(
        self,
        src_vocab_size,
        tgt_vocab_size,
        d_model=128,
        nhead=4,
        num_encoder_layers=3,
        num_decoder_layers=3,
        dim_feedforward=512,
        dropout=0.1,
    ):
        super().__init__()
        
        self.d_model = d_model
        self.tgt_vocab_size = tgt_vocab_size
        
        # Character embeddings
        self.src_embedding = nn.Embedding(src_vocab_size, d_model, padding_idx=PAD_IDX)
        self.tgt_embedding = nn.Embedding(tgt_vocab_size, d_model, padding_idx=PAD_IDX)
        
        # Positional encoding
        self.pos_encoder = PositionalEncoding(d_model, dropout=dropout)
        self.pos_decoder = PositionalEncoding(d_model, dropout=dropout)
        
        # Transformer
        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_encoder_layers,
            num_decoder_layers=num_decoder_layers,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
        )
        
        # Output projection: d_model -> target vocab size
        self.output_projection = nn.Linear(d_model, tgt_vocab_size)
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Xavier uniform initialization for embeddings and projection."""
        init_range = 0.1
        self.src_embedding.weight.data.uniform_(-init_range, init_range)
        self.tgt_embedding.weight.data.uniform_(-init_range, init_range)
        self.output_projection.bias.data.zero_()
        self.output_projection.weight.data.uniform_(-init_range, init_range)
    
    def _generate_square_subsequent_mask(self, sz, device):
        """
        Generate a causal mask for the decoder.
        Prevents the decoder from attending to future positions.
        Returns a boolean mask (True = masked/blocked) to match
        the boolean key_padding_mask and avoid type mismatch warnings.
        """
        mask = torch.triu(torch.ones(sz, sz, device=device, dtype=torch.bool), diagonal=1)
        return mask
    
    def forward(self, src, tgt):
        """
        Forward pass through the full encoder-decoder.
        
        Args:
            src: (batch_size, src_len) source character indices
            tgt: (batch_size, tgt_len) target character indices (teacher forcing)
            
        Returns:
            logits: (batch_size, tgt_len, tgt_vocab_size) raw prediction scores
        """
        # Create padding masks
        src_key_padding_mask = (src == PAD_IDX)  # (batch, src_len)
        tgt_key_padding_mask = (tgt == PAD_IDX)  # (batch, tgt_len)
        
        # Create causal mask for decoder
        tgt_len = tgt.size(1)
        tgt_mask = self._generate_square_subsequent_mask(tgt_len, tgt.device)
        
        # Embed and add positional encoding
        src_emb = self.pos_encoder(self.src_embedding(src) * math.sqrt(self.d_model))
        tgt_emb = self.pos_decoder(self.tgt_embedding(tgt) * math.sqrt(self.d_model))
        
        # Transformer forward
        output = self.transformer(
            src_emb, tgt_emb,
            tgt_mask=tgt_mask,
            src_key_padding_mask=src_key_padding_mask,
            tgt_key_padding_mask=tgt_key_padding_mask,
            memory_key_padding_mask=src_key_padding_mask,
        )
        
        # Project to vocabulary
        logits = self.output_projection(output)
        return logits
    
    def encode(self, src):
        """
        Encode source sequence (used during inference).
        
        Args:
            src: (batch_size, src_len)
            
        Returns:
            memory: (batch_size, src_len, d_model) encoder output
            src_key_padding_mask: (batch_size, src_len) padding mask
        """
        src_key_padding_mask = (src == PAD_IDX)
        src_emb = self.pos_encoder(self.src_embedding(src) * math.sqrt(self.d_model))
        memory = self.transformer.encoder(
            src_emb,
            src_key_padding_mask=src_key_padding_mask,
        )
        return memory, src_key_padding_mask
    
    def decode_step(self, tgt, memory, memory_key_padding_mask):
        """
        Decode one step (used during greedy/beam search inference).
        
        Args:
            tgt: (batch_size, tgt_len_so_far)
            memory: encoder output
            memory_key_padding_mask: source padding mask
            
        Returns:
            logits: (batch_size, tgt_len_so_far, tgt_vocab_size)
        """
        tgt_len = tgt.size(1)
        tgt_mask = self._generate_square_subsequent_mask(tgt_len, tgt.device)
        tgt_key_padding_mask = (tgt == PAD_IDX)
        
        tgt_emb = self.pos_decoder(self.tgt_embedding(tgt) * math.sqrt(self.d_model))
        
        output = self.transformer.decoder(
            tgt_emb, memory,
            tgt_mask=tgt_mask,
            tgt_key_padding_mask=tgt_key_padding_mask,
            memory_key_padding_mask=memory_key_padding_mask,
        )
        
        logits = self.output_projection(output)
        return logits
