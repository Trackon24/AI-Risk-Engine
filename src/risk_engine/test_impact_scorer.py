from src.risk_engine.impact_scorer import FinancialImpactScorer


scorer = FinancialImpactScorer()

result = scorer.calculate(
    event="earnings",
    sentiment_score=0.0779,
    event_confidence=0.4286,
)

print("Impact Score:", result["impact_score"])
print("Base Score:", result["base_score"])
print("Sentiment Adjustment:", result["sentiment_adjustment"])
print("Evidence Adjustment:", result["evidence_adjustment"])