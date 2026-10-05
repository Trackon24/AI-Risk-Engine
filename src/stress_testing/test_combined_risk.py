import json

from src.risk_engine.sentiment import FinancialSentimentAnalyzer
from src.risk_engine.event_classifier import FinancialEventClassifier
from src.risk_engine.impact_scorer import FinancialImpactScorer
from src.risk_engine.risk_signal import RiskSignalBuilder
from src.risk_engine.gdelt_context import GDELTContextAnalyzer
from src.risk_engine.combined_risk import CombinedRiskBuilder

from src.ingestion.gdelt_gkg_loader import read_gkg_records


DOCUMENT_PATH = "data/processed/edgar_documents.json"


def load_apple_document():
    with open(DOCUMENT_PATH, "r", encoding="utf-8") as file:
        documents = json.load(file)

    for document in documents:
        if document.get("entity") == "Apple Inc.":
            return document

    raise ValueError("Apple Inc. document not found.")


def main():
    document = load_apple_document()

    # ---------------------------------------------------------
    # SEC Risk Signal
    # ---------------------------------------------------------
    sentiment_analyzer = FinancialSentimentAnalyzer()
    event_classifier = FinancialEventClassifier()
    impact_scorer = FinancialImpactScorer()
    risk_signal_builder = RiskSignalBuilder()

    sentiment = sentiment_analyzer.analyze(document["text"])
    event = event_classifier.classify(document["text"])

    impact = impact_scorer.calculate(
        event=event["event"],
        sentiment_score=sentiment["score"],
        event_confidence=event["confidence"],
    )

    risk_signal = risk_signal_builder.build(
        entity=document["entity"],
        sentiment=sentiment,
        event=event,
        impact=impact,
    )

    # ---------------------------------------------------------
    # GDELT External Context
    # ---------------------------------------------------------
    gdelt_analyzer = GDELTContextAnalyzer()

    gdelt_context = gdelt_analyzer.analyze(
        records=read_gkg_records(),
        entity=document["entity"],
    )

    # ---------------------------------------------------------
    # Combined Risk
    # ---------------------------------------------------------
    combined_builder = CombinedRiskBuilder()

    combined = combined_builder.build(
        risk_signal=risk_signal,
        gdelt_context=gdelt_context,
    )

    print("=" * 60)
    print("SEC + GDELT COMBINED RISK")
    print("=" * 60)

    print("\nSEC COMPANY RISK")
    print("-" * 60)
    print(f"Entity       : {document['entity']}")
    print(f"Event        : {risk_signal['event']['type']}")
    print(f"Sentiment    : {risk_signal['sentiment']['score']:+.4f}")
    print(f"Impact       : {risk_signal['impact']['score']:.2f}/10")
    print(f"Risk level   : {risk_signal['risk_level']}")

    print("\nGDELT EXTERNAL CONTEXT")
    print("-" * 60)
    print(f"Records      : {gdelt_context['records_found']}")
    print(f"Articles     : {gdelt_context['article_count']}")
    print(f"Tone         : {gdelt_context['average_tone']:+.4f}")
    print(f"Tone score   : {gdelt_context['tone_score']:+.4f}")
    print(f"Domains      : {gdelt_context['financial_domains']}")

    print("\nCOMBINED RISK")
    print("-" * 60)
    print(f"Company impact      : {combined['company_risk']['impact_score']:.2f}")
    print(f"External adjustment : {combined['external_adjustment']:+.2f}")
    print(f"Combined impact     : {combined['combined_impact']:.2f}/10")
    print(f"Risk level          : {combined['risk_level']}")

    print("\n" + "=" * 60)
    print("COMBINED RISK TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()