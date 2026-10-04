class RiskExplanationBuilder:
    """Generate human-readable explanations for risk signals."""

    def build(self, risk_signal: dict) -> dict:
        """Explain the main factors contributing to the risk signal."""

        entity = risk_signal.get("entity", "Unknown")
        sentiment = risk_signal.get("sentiment", {})
        event = risk_signal.get("event", {})
        impact = risk_signal.get("impact", {})

        event_type = event.get("type", "unknown")
        sentiment_label = sentiment.get("label", "neutral")
        sentiment_score = sentiment.get("score", 0.0)
        impact_score = impact.get("score", 0.0)

        evidence = event.get("matched_keywords", [])

        reasons = []

        if event_type != "unknown":
            reasons.append(
                f"Event classified as {event_type}."
            )

        if evidence:
            reasons.append(
                "Supporting evidence: "
                + ", ".join(evidence)
                + "."
            )

        if sentiment_label == "negative":
            reasons.append(
                f"Negative financial sentiment detected "
                f"({sentiment_score:.2f})."
            )
        elif sentiment_label == "positive":
            reasons.append(
                f"Positive financial sentiment detected "
                f"({sentiment_score:.2f})."
            )
        else:
            reasons.append(
                f"Sentiment is broadly neutral "
                f"({sentiment_score:.2f})."
            )

        reasons.append(
            f"Calculated event impact is "
            f"{impact_score:.2f}/10."
        )

        return {
            "entity": entity,
            "summary": (
                f"{entity} has a {event_type} event "
                f"with an impact score of "
                f"{impact_score:.2f}/10."
            ),
            "reasons": reasons,
        }