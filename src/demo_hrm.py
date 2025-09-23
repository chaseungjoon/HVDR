import torch.nn as nn

class DemoHRM(nn.Module):
    """Simplified demo version of HRM for demonstration"""
    def __init__(self, hidden_size=512, num_layers=6, vocab_size=1000):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.vocab_size = vocab_size

        # Hierarchical components
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.high_level_module = nn.LSTM(hidden_size, hidden_size, num_layers//2, batch_first=True)
        self.low_level_module = nn.LSTM(hidden_size, hidden_size, num_layers//2, batch_first=True)
        self.output_projection = nn.Linear(hidden_size, vocab_size)

        # Multi-scale processing
        self.cross_attention = nn.MultiheadAttention(hidden_size, 8, batch_first=True)
        self.layer_norm = nn.LayerNorm(hidden_size)

    def forward(self, x):
        # Embed input
        embedded = self.embedding(x)

        # High-level abstract processing (slow timescale)
        high_level_out, _ = self.high_level_module(embedded)

        # Low-level detailed processing (fast timescale)
        low_level_out, _ = self.low_level_module(embedded)

        # Cross-module attention (hierarchical reasoning)
        attended_out, _ = self.cross_attention(
            low_level_out, high_level_out, high_level_out
        )

        # Layer normalization and output
        normalized = self.layer_norm(attended_out + low_level_out)
        output = self.output_projection(normalized)

        return output