class RiskSignalBuilder:
    """Build a structured risk signal from individual risk components."""

    def build(
        self,
        entity: str,
        sentiment: dict,
        event: dict,
        impact: dict,
    ) -> dict:
        """Combine sentiment, event, and impact into one risk signal."""

        impact_score = impact.get("impact_score", 1.0)

        if impact_score >= 8.0:
            risk_level = "high"
        elif impact_score >= 5.0:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "entity": entity,
            "sentiment": {
                "label": sentiment.get("label", "neutral"),
                "score": sentiment.get("score", 0.0),
            },
            "event": {
                "type": event.get("event", "unknown"),
                "confidence": event.get("confidence", 0.0),
                "matched_keywords": event.get(
                    "matched_keywords",
                    [],
                ),
            },
            "impact": {
                "score": impact_score,
                "base_score": impact.get("base_score", 0.0),
                "sentiment_adjustment": impact.get(
                    "sentiment_adjustment",
                    0.0,
                ),
                "evidence_adjustment": impact.get(
                    "evidence_adjustment",
                    0.0,
                ),
            },
            "risk_level": risk_level,
        }