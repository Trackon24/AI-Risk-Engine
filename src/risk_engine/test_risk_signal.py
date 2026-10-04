import json

from src.risk_engine.sentiment import FinancialSentimentAnalyzer
from src.risk_engine.event_classifier import FinancialEventClassifier
from src.risk_engine.impact_scorer import FinancialImpactScorer
from src.risk_engine.risk_signal import RiskSignalBuilder


with open(
    "data/processed/edgar_documents.json",
    "r",
    encoding="utf-8",
) as f:
    documents = json.load(f)


document = documents[0]

sentiment_analyzer = FinancialSentimentAnalyzer()
event_classifier = FinancialEventClassifier()
impact_scorer = FinancialImpactScorer()
signal_builder = RiskSignalBuilder()


sentiment = sentiment_analyzer.analyze(
    document["text"]
)

event = event_classifier.classify(
    document["text"]
)

impact = impact_scorer.calculate(
    event=event["event"],
    sentiment_score=sentiment["score"],
    event_confidence=event["confidence"],
)

risk_signal = signal_builder.build(
    entity=document["entity"],
    sentiment=sentiment,
    event=event,
    impact=impact,
)


print(json.dumps(risk_signal, indent=2))