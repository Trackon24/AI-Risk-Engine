class FinancialEventClassifier:
    """Classify financial documents into high-level event categories."""

    EVENT_KEYWORDS = {
        "earnings": [
            "earnings",
            "revenue",
            "profit",
            "loss",
            "quarterly results",
            "financial results",
            "net income",
            "eps",
        ],
        "m&a": [
            "acquisition",
            "acquire",
            "merger",
            "merging",
            "takeover",
            "purchase agreement",
        ],
        "credit_event": [
            "default",
            "bankruptcy",
            "credit downgrade",
            "debt restructuring",
            "loan default",
            "insolvency",
        ],
        "regulatory": [
            "regulatory",
            "regulator",
            "investigation",
            "compliance",
            "sanction",
            "antitrust",
            "government action",
            "regulations",
        ],
        "geopolitical": [
            "war",
            "conflict",
            "geopolitical",
            "tariff",
            "trade restriction",
            "sanctions",
            "military",
        ],
        "macroeconomic": [
            "inflation",
            "interest rate",
            "central bank",
            "recession",
            "unemployment",
            "gdp",
            "economic growth",
            "economic slowdown",
        ],
        "product_business": [
            "product launch",
            "new product",
            "new service",
            "expansion",
            "partnership",
            "business segment",
            "expand",
        ],
        "litigation": [
            "lawsuit",
            "litigation",
            "court",
            "legal action",
            "settlement",
            "claim",
        ],
    }

    def classify(self, text: str) -> dict:
        """Classify a financial text based on keyword evidence."""

        if not text or not text.strip():
            return {
                "event": "unknown",
                "confidence": 0.0,
                "matched_keywords": [],
            }

        text_lower = text.lower()

        matches = {}

        for event, keywords in self.EVENT_KEYWORDS.items():
            matched = [
                keyword
                for keyword in keywords
                if keyword in text_lower
            ]

            if matched:
                matches[event] = matched

        if not matches:
            return {
                "event": "unknown",
                "confidence": 0.0,
                "matched_keywords": [],
            }

        event = max(
            matches,
            key=lambda key: len(matches[key]),
        )

        total_matches = sum(
            len(keywords)
            for keywords in matches.values()
        )

        confidence = len(matches[event]) / total_matches

        return {
            "event": event,
            "confidence": round(confidence, 4),
            "matched_keywords": matches[event],
        }