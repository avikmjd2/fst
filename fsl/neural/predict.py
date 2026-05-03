"""
predict.py - Neural Model Inference

Loads a trained CharTransformer checkpoint and performs
greedy decoding to predict morphological analyses for new words.

Usage (from fsl/ directory):
    # Single word
    python neural/predict.py walked
    
    # Interactive mode
    python neural/predict.py
"""
import os
import sys
import torch

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from neural.dataset import CharVocab, SOS_IDX, EOS_IDX, PAD_IDX
from neural.model import CharTransformer


class NeuralAnalyzer:
    """
    Wrapper for the trained CharTransformer model.
    
    Provides a simple .analyze(word) interface that mirrors
    the FST analyzer's interface for easy integration.
    """
    
    def __init__(self, model_dir=None, device=None):
        """
        Load a trained model from checkpoint.
        
        Args:
            model_dir: directory containing best_model.pt and vocab files
            device: torch device (auto-detected if None)
        """
        if model_dir is None:
            model_dir = os.path.join(os.path.dirname(__file__), "checkpoints")
        
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = device
        
        # Load vocabularies
        self.src_vocab = CharVocab()
        self.src_vocab.load(os.path.join(model_dir, "src_vocab.json"))
        
        self.tgt_vocab = CharVocab()
        self.tgt_vocab.load(os.path.join(model_dir, "tgt_vocab.json"))
        
        # Load model checkpoint
        checkpoint_path = os.path.join(model_dir, "best_model.pt")
        checkpoint = torch.load(checkpoint_path, map_location=self.device, weights_only=True)
        
        # Reconstruct model with saved hyperparameters
        self.model = CharTransformer(
            src_vocab_size=checkpoint["src_vocab_size"],
            tgt_vocab_size=checkpoint["tgt_vocab_size"],
            d_model=checkpoint.get("d_model", 128),
            nhead=checkpoint.get("nhead", 4),
            num_encoder_layers=checkpoint.get("num_encoder_layers", 3),
            num_decoder_layers=checkpoint.get("num_decoder_layers", 3),
            dim_feedforward=checkpoint.get("dim_feedforward", 512),
            dropout=checkpoint.get("dropout", 0.1),
        ).to(self.device)
        
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()
        
        print(f"Neural model loaded from {checkpoint_path}")
        print(f"  Trained for {checkpoint['epoch']} epochs, val loss: {checkpoint['val_loss']:.4f}")
    
    def analyze(self, word, max_len=64):
        """
        Predict morphological analysis for a surface form using greedy decoding.
        
        Args:
            word: surface form string (e.g., "walked")
            max_len: maximum output length
            
        Returns:
            list of analysis strings (currently returns one greedy prediction)
        """
        self.model.eval()
        
        with torch.no_grad():
            # Encode source word
            src_indices = self.src_vocab.encode(word)
            src_tensor = torch.tensor([src_indices], dtype=torch.long, device=self.device)
            
            # Get encoder output
            memory, src_mask = self.model.encode(src_tensor)
            
            # Greedy decode: start with <SOS>, predict one char at a time
            tgt_indices = [SOS_IDX]
            
            for _ in range(max_len):
                tgt_tensor = torch.tensor(
                    [tgt_indices], dtype=torch.long, device=self.device
                )
                
                logits = self.model.decode_step(tgt_tensor, memory, src_mask)
                
                # Take the last position's prediction
                next_token = logits[0, -1, :].argmax(dim=-1).item()
                
                if next_token == EOS_IDX:
                    break
                
                tgt_indices.append(next_token)
            
            # Decode back to string (skip <SOS>)
            analysis = self.tgt_vocab.decode(tgt_indices)
        
        return [analysis] if analysis else []
    
    def batch_analyze(self, words, max_len=64):
        """
        Analyze multiple words.
        
        Args:
            words: list of surface form strings
            
        Returns:
            dict mapping word -> list of analysis strings
        """
        results = {}
        for word in words:
            results[word] = self.analyze(word, max_len)
        return results


def main():
    """CLI interface for neural prediction."""
    model_dir = os.path.join(os.path.dirname(__file__), "checkpoints")
    
    if not os.path.exists(os.path.join(model_dir, "best_model.pt")):
        print("ERROR: No trained model found. Run train.py first.")
        print(f"  Expected: {model_dir}/best_model.pt")
        return
    
    analyzer = NeuralAnalyzer(model_dir)
    
    # Single word from command line
    if len(sys.argv) > 1:
        word = sys.argv[1].strip().lower()
        analyses = analyzer.analyze(word)
        if analyses:
            print(f"{word} -> {analyses[0]}")
        else:
            print(f"{word} -> [NO PREDICTION]")
        return
    
    # Interactive mode
    print("\nNeural Morphological Analyzer (interactive mode)")
    print("Type a word to analyze, or 'quit' to exit.\n")
    
    while True:
        try:
            word = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        
        if not word or word in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        
        analyses = analyzer.analyze(word)
        if analyses:
            print(f"  {word} -> {analyses[0]}")
        else:
            print(f"  {word} -> [NO PREDICTION]")


if __name__ == "__main__":
    main()
