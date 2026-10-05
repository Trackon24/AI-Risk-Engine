class CombinedRiskBuilder:
    """
    Combine company-level SEC risk with external GDELT context.

    SEC risk remains the primary signal.
    GDELT acts as an external context modifier.

    The GDELT modifier is deliberately bounded so that
    external news context cannot overwhelm the company-level signal.
    """

    def __init__(self, external_context_weight: float = 0.20):
        if not 0.0 <= external_context_weight <= 1.0:
            raise ValueError("external_context_weight must be between 0 and 1.")

        self.external_context_weight = external_context_weight

    def build(
        self,
        risk_signal: dict,
        gdelt_context: dict,
    ) -> dict:

        company_impact = float(
            risk_signal.get("impact", {}).get("score", 0.0)
        )

        tone_score = float(
            gdelt_context.get("tone_score", 0.0)
        )

        records_found = int(
            gdelt_context.get("records_found", 0)
        )

        # GDELT tone is already normalized to [-1, 1].
        # Convert it into a bounded impact adjustment.
        external_adjustment = (
            tone_score
            * 2.0
            * self.external_context_weight
        )

        combined_impact = company_impact + external_adjustment

        # Keep the final score inside the required 1-10 range.
        combined_impact = max(1.0, min(10.0, combined_impact))

        if combined_impact >= 8.0:
            risk_level = "high"
        elif combined_impact >= 5.0:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "entity": risk_signal.get("entity", "Unknown"),
            "company_risk": {
                "impact_score": round(company_impact, 2),
                "risk_level": risk_signal.get("risk_level", "unknown"),
                "event": risk_signal.get("event", {}),
                "sentiment": risk_signal.get("sentiment", {}),
            },
            "external_context": {
                "records_found": records_found,
                "article_count": gdelt_context.get("article_count", 0),
                "average_tone": gdelt_context.get("average_tone", 0.0),
                "tone_score": tone_score,
                "financial_domains": gdelt_context.get(
                    "financial_domains", []
                ),
            },
            "combined_impact": round(combined_impact, 2),
            "external_adjustment": round(external_adjustment, 2),
            "risk_level": risk_level,
        }