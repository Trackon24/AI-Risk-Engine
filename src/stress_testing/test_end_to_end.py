import json

from src.risk_engine.sentiment import FinancialSentimentAnalyzer
from src.risk_engine.event_classifier import FinancialEventClassifier
from src.risk_engine.impact_scorer import FinancialImpactScorer
from src.risk_engine.risk_signal import RiskSignalBuilder

from src.stress_testing.portfolio import load_portfolio
from src.stress_testing.risk_stress import RiskSignalStressTester


DOCUMENT_PATH = "data/processed/edgar_documents.json"
PORTFOLIO_PATH = "data/demo/portfolio.csv"


def load_apple_document():
    with open(DOCUMENT_PATH, "r", encoding="utf-8") as file:
        documents = json.load(file)

    for document in documents:
        if document.get("entity") == "Apple Inc.":
            return document

    raise ValueError("Apple Inc. document not found.")


def main():
    print("=" * 60)
    print("END-TO-END RISK → STRESS TEST")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Load real SEC document
    # ---------------------------------------------------------
    document = load_apple_document()

    print("\nDOCUMENT")
    print("-" * 60)
    print(f"Source   : {document['source']}")
    print(f"Entity   : {document['entity']}")
    print(f"Title    : {document['title']}")
    print(f"Text     : {len(document['text'])} characters")

    # ---------------------------------------------------------
    # 2. Run existing Risk Engine
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
    # 3. Display unified risk signal
    # ---------------------------------------------------------
    print("\nRISK SIGNAL")
    print("-" * 60)
    print(f"Entity          : {risk_signal['entity']}")
    print(
        f"Sentiment       : "
        f"{risk_signal['sentiment']['label']} "
        f"({risk_signal['sentiment']['score']:+.4f})"
    )
    print(
        f"Event           : "
        f"{risk_signal['event']['type']} "
        f"(confidence {risk_signal['event']['confidence']:.4f})"
    )
    print(f"Impact Score    : {risk_signal['impact']['score']:.2f}/10")
    print(f"Risk Level      : {risk_signal['risk_level']}")

    # ---------------------------------------------------------
    # 4. Load portfolio
    # ---------------------------------------------------------
    portfolio = load_portfolio(PORTFOLIO_PATH)

    # ---------------------------------------------------------
    # 5. Run Risk → Stress integration
    # ---------------------------------------------------------
    stress_tester = RiskSignalStressTester(portfolio)

    print("\nSTRESS TEST RESULTS")
    print("-" * 60)

    for scenario in ["mild", "moderate", "severe"]:
        result = stress_tester.run(
            risk_signal=risk_signal,
            scenario=scenario,
        )

        stress = result["stress_test"]

        print(
            f"{scenario.capitalize():<10} "
            f"Shock: {stress['shock']:+.2%} | "
            f"Direct: {stress['direct_impact']:+.2%} | "
            f"Indirect: {stress['indirect_impact']:+.2%} | "
            f"Portfolio: {stress['total_portfolio_impact']:+.2%}"
        )

    print("\n" + "=" * 60)
    print("END-TO-END TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()