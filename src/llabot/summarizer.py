import torch
from transformers import pipeline, AutoTokenizer

class Summarizer:
    """Handles summarization tasks using BART model."""
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=self.device)

    def summarize_batch(self, dataset, batch_size):
        """Summarize a batch of text data."""
        summaries = self.summarizer(dataset["content"], batch_size=batch_size, min_length=60, max_length=130)
        return [{"index": data["index"], "summary_text": summary["summary_text"]}
                for data, summary in zip(dataset, summaries)]