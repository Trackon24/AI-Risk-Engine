from src.risk_engine.impact_scorer import FinancialImpactScorer


def main():
    scorer = FinancialImpactScorer()

    print("=" * 65)
    print("IMPACT SCORER EVALUATION")
    print("=" * 65)

    # Test 1: Event severity
    low_severity = scorer.calculate(
        event="product_business",
        sentiment_score=0.0,
        event_confidence=1.0,
    )

    high_severity = scorer.calculate(
        event="credit_event",
        sentiment_score=0.0,
        event_confidence=1.0,
    )

    severity_pass = (
        high_severity["impact_score"]
        > low_severity["impact_score"]
    )

    print("\n1. EVENT SEVERITY")
    print(
        f"Product/business impact : "
        f"{low_severity['impact_score']:.2f}"
    )
    print(
        f"Credit event impact     : "
        f"{high_severity['impact_score']:.2f}"
    )
    print(
        f"Result                  : "
        f"{'PASS' if severity_pass else 'FAIL'}"
    )

    # Test 2: Sentiment direction
    positive = scorer.calculate(
        event="earnings",
        sentiment_score=0.8,
        event_confidence=1.0,
    )

    negative = scorer.calculate(
        event="earnings",
        sentiment_score=-0.8,
        event_confidence=1.0,
    )

    sentiment_pass = (
        negative["impact_score"]
        > positive["impact_score"]
    )

    print("\n2. SENTIMENT DIRECTION")
    print(
        f"Positive sentiment impact : "
        f"{positive['impact_score']:.2f}"
    )
    print(
        f"Negative sentiment impact : "
        f"{negative['impact_score']:.2f}"
    )
    print(
        f"Result                    : "
        f"{'PASS' if sentiment_pass else 'FAIL'}"
    )

    # Test 3: Event confidence
    low_confidence = scorer.calculate(
        event="earnings",
        sentiment_score=0.0,
        event_confidence=0.2,
    )

    high_confidence = scorer.calculate(
        event="earnings",
        sentiment_score=0.0,
        event_confidence=1.0,
    )

    confidence_pass = (
        high_confidence["impact_score"]
        > low_confidence["impact_score"]
    )

    print("\n3. EVENT CONFIDENCE")
    print(
        f"Low confidence impact  : "
        f"{low_confidence['impact_score']:.2f}"
    )
    print(
        f"High confidence impact : "
        f"{high_confidence['impact_score']:.2f}"
    )
    print(
        f"Result                 : "
        f"{'PASS' if confidence_pass else 'FAIL'}"
    )

    # Test 4: Impact score bounds
    test_cases = [
        ("low", "product_business", 1.0, 0.0),
        ("high", "credit_event", -1.0, 1.0),
        ("unknown", "unknown", 0.0, 0.0),
    ]

    bounds_pass = True

    for _, event, sentiment, confidence in test_cases:
        result = scorer.calculate(
            event=event,
            sentiment_score=sentiment,
            event_confidence=confidence,
        )

        impact = result["impact_score"]

        if not 1.0 <= impact <= 10.0:
            bounds_pass = False

    print("\n4. IMPACT BOUNDS")
    print("Expected range : 1.00 to 10.00")
    print(
        f"Result         : "
        f"{'PASS' if bounds_pass else 'FAIL'}"
    )

    all_pass = (
        severity_pass
        and sentiment_pass
        and confidence_pass
        and bounds_pass
    )

    print("\n" + "=" * 65)
    print(
        f"OVERALL RESULT : "
        f"{'PASS' if all_pass else 'FAIL'}"
    )
    print("=" * 65)


if __name__ == "__main__":
    main()