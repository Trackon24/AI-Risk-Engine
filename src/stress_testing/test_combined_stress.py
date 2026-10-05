import json

from src.risk_engine.sentiment import FinancialSentimentAnalyzer
from src.risk_engine.event_classifier import FinancialEventClassifier
from src.risk_engine.impact_scorer import FinancialImpactScorer
from src.risk_engine.risk_signal import RiskSignalBuilder
from src.risk_engine.gdelt_context import GDELTContextAnalyzer
from src.risk_engine.combined_risk import CombinedRiskBuilder

from src.ingestion.gdelt_gkg_loader import read_gkg_records

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

    print("=" * 65)
    print("END-TO-END TWO-SOURCE RISK → STRESS TEST")
    print("=" * 65)

    # ---------------------------------------------------------
    # 1. Load actual SEC document
    # ---------------------------------------------------------
    document = load_apple_document()

    # ---------------------------------------------------------
    # 2. Build SEC company risk
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
    # 3. Build GDELT external context
    # ---------------------------------------------------------
    gdelt_analyzer = GDELTContextAnalyzer()

    gdelt_context = gdelt_analyzer.analyze(
        records=read_gkg_records(),
        entity=document["entity"],
    )

    # ---------------------------------------------------------
    # 4. Combine SEC + GDELT
    # ---------------------------------------------------------
    combined_builder = CombinedRiskBuilder()

    combined_risk = combined_builder.build(
        risk_signal=risk_signal,
        gdelt_context=gdelt_context,
    )

    # ---------------------------------------------------------
    # 5. Load actual demo portfolio
    # ---------------------------------------------------------
    portfolio = load_portfolio(PORTFOLIO_PATH)

    # ---------------------------------------------------------
    # 6. Stress-test the portfolio
    # ---------------------------------------------------------
    stress_tester = RiskSignalStressTester(portfolio)

    print("\nTWO-SOURCE RISK SIGNAL")
    print("-" * 65)

    print(f"Entity              : {combined_risk['entity']}")

    print(
        f"SEC Event           : "
        f"{combined_risk['company_risk']['event']['type']}"
    )

    print(
        f"SEC Sentiment       : "
        f"{combined_risk['company_risk']['sentiment']['score']:+.4f}"
    )

    print(
        f"SEC Impact          : "
        f"{combined_risk['company_risk']['impact_score']:.2f}/10"
    )

    print(
        f"GDELT Records       : "
        f"{combined_risk['external_context']['records_found']}"
    )

    print(
        f"GDELT Tone         : "
        f"{combined_risk['external_context']['average_tone']:+.4f}"
    )

    print(
        f"GDELT Tone Score    : "
        f"{combined_risk['external_context']['tone_score']:+.4f}"
    )

    print(
        f"External Adjustment : "
        f"{combined_risk['external_adjustment']:+.2f}"
    )

    print(
        f"Combined Impact     : "
        f"{combined_risk['combined_impact']:.2f}/10"
    )

    print(
        f"Combined Risk       : "
        f"{combined_risk['risk_level']}"
    )

    # ---------------------------------------------------------
    # 7. Portfolio stress scenarios
    # ---------------------------------------------------------
    print("\nPORTFOLIO STRESS TEST")
    print("-" * 65)

    for scenario in ["mild", "moderate", "severe"]:

        result = stress_tester.run(
            risk_signal=risk_signal,
            scenario=scenario,
        )

        stress = result["stress_test"]

        print(
            f"{scenario.capitalize():<10}"
            f" Shock: {stress['shock']:+.2%} |"
            f" Direct: {stress['direct_impact']:+.2%} |"
            f" Indirect: {stress['indirect_impact']:+.2%} |"
            f" Portfolio: {stress['total_portfolio_impact']:+.2%}"
        )

    print("\n" + "=" * 65)
    print("TWO-SOURCE END-TO-END TEST PASSED")
    print("=" * 65)


if __name__ == "__main__":
    main()