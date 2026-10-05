from src.stress_testing.portfolio import load_portfolio
from src.stress_testing.risk_stress import RiskSignalStressTester


PORTFOLIO_PATH = "data/demo/portfolio.csv"


def main():
    portfolio = load_portfolio(PORTFOLIO_PATH)

    risk_signal = {
        "entity": "Apple Inc.",
        "sentiment": {
            "label": "neutral",
            "score": 0.0779,
        },
        "event": {
            "type": "earnings",
            "confidence": 0.4286,
            "matched_keywords": [
                "earnings",
                "revenue",
                "loss",
                "financial results",
                "net income",
                "eps",
            ],
        },
        "impact": {
            "score": 6.70,
            "base_score": 6.00,
            "sentiment_adjustment": -0.16,
            "evidence_adjustment": 0.86,
        },
        "risk_level": "medium",
    }

    tester = RiskSignalStressTester(
        portfolio=portfolio,
        same_sector_factor=0.30,
    )

    result = tester.run(
        risk_signal=risk_signal,
        scenario="moderate",
    )

    print("Risk → Stress Integration")
    print("-------------------------")

    signal = result["risk_signal"]
    stress = result["stress_test"]

    print(f"Entity: {signal['entity']}")
    print(f"Event: {signal['event']['type']}")
    print(f"Risk level: {signal['risk_level']}")
    print(f"Impact score: {signal['impact']['score']:.2f}/10")

    print()
    print(f"Scenario: {stress['scenario']}")
    print(f"Shock: {stress['shock']:.2%}")
    print(f"Direct impact: {stress['direct_impact']:.2%}")
    print(f"Indirect impact: {stress['indirect_impact']:.2%}")
    print(
        f"Portfolio impact: "
        f"{stress['total_portfolio_impact']:.2%}"
    )


if __name__ == "__main__":
    main()