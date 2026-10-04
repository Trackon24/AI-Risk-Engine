from transformers import pipeline


class FinancialSentimentAnalyzer:
    """Financial sentiment analyzer using a pretrained FinBERT model."""

    def __init__(
        self,
        model_name: str = "ProsusAI/finbert",
    ):
        self.model_name = model_name

        self.pipeline = pipeline(
            "text-classification",
            model=model_name,
            tokenizer=model_name,
            top_k=None,
        )

    def analyze(self, text: str) -> dict:
        """Analyze financial sentiment across an entire document."""

        if not text or not text.strip():
            return {
                "label": "neutral",
                "score": 0.0,
                "probabilities": {},
            }

        chunks = self._split_into_chunks(text)

        if not chunks:
            return {
                "label": "neutral",
                "score": 0.0,
                "probabilities": {},
            }

        chunk_results = []

        for chunk in chunks:
            results = self.pipeline(chunk)[0]

            probabilities = {
                result["label"].lower(): float(result["score"])
                for result in results
            }

            chunk_results.append(probabilities)

        labels = ["positive", "neutral", "negative"]

        probabilities = {
            label: sum(
                result.get(label, 0.0)
                for result in chunk_results
            ) / len(chunk_results)
            for label in labels
        }

        label = max(
            probabilities,
            key=probabilities.get,
        )

        sentiment_score = self._calculate_sentiment_score(
            probabilities
        )

        return {
            "label": label,
            "score": sentiment_score,
            "probabilities": {
                key: round(value, 4)
                for key, value in probabilities.items()
            },
            "chunks_analyzed": len(chunks),
        }

    def _split_into_chunks(
        self,
        text: str,
        max_tokens: int = 450,
    ) -> list[str]:
        """Split long financial text into tokenizer-safe chunks."""

        if not text or not text.strip():
            return []

        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            current_chunk.append(word)

            token_count = len(
                self.pipeline.tokenizer(
                    " ".join(current_chunk),
                    add_special_tokens=True,
                    truncation=False,
                )["input_ids"]
            )

            if token_count > max_tokens:
                current_chunk.pop()

                if current_chunk:
                    chunks.append(" ".join(current_chunk))

                current_chunk = [word]

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    @staticmethod
    def _calculate_sentiment_score(probabilities: dict) -> float:
        """Convert FinBERT probabilities to a -1 to +1 score."""

        positive = probabilities.get("positive", 0.0)
        negative = probabilities.get("negative", 0.0)

        score = positive - negative

        return round(score, 4)