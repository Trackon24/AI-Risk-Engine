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
        """Analyze the financial sentiment of a piece of text."""

        if not text or not text.strip():
            return {
                "label": "neutral",
                "score": 0.0,
                "probabilities": {},
            }

        results = self.pipeline(text[:512])[0]

        probabilities = {
            result["label"].lower(): float(result["score"])
            for result in results
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
            "probabilities": probabilities,
        }

    @staticmethod
    def _calculate_sentiment_score(probabilities: dict) -> float:
        """Convert FinBERT probabilities to a -1 to +1 score."""

        positive = probabilities.get("positive", 0.0)
        negative = probabilities.get("negative", 0.0)

        score = positive - negative

        return round(score, 4)