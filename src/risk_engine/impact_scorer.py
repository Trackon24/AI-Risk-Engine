class FinancialImpactScorer:
    """Calculate a transparent 1-10 impact score for financial events."""

    EVENT_SEVERITY = {
        "credit_event": 9.0,
        "geopolitical": 8.0,
        "regulatory": 7.5,
        "litigation": 7.0,
        "macroeconomic": 7.0,
        "m&a": 6.5,
        "earnings": 6.0,
        "product_business": 4.5,
        "unknown": 3.0,
    }

    def calculate(
        self,
        event: str,
        sentiment_score: float,
        event_confidence: float,
    ) -> dict:
        """Calculate an impact score from event severity and evidence."""

        base_score = self.EVENT_SEVERITY.get(
            event,
            self.EVENT_SEVERITY["unknown"],
        )

        sentiment_adjustment = -2.0 * sentiment_score

        evidence_adjustment = 2.0 * event_confidence

        raw_score = (
            base_score
            + sentiment_adjustment
            + evidence_adjustment
        )

        impact_score = max(1.0, min(10.0, raw_score))

        return {
            "impact_score": round(impact_score, 2),
            "base_score": round(base_score, 2),
            "sentiment_adjustment": round(
                sentiment_adjustment,
                2,
            ),
            "evidence_adjustment": round(
                evidence_adjustment,
                2,
            ),
        }