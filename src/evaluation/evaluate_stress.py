from src.stress_testing.portfolio import load_portfolio
from src.stress_testing.stress_engine import PortfolioStressEngine


def main():
    portfolio = load_portfolio("data/demo/portfolio.csv")

    engine = PortfolioStressEngine(
        portfolio=portfolio,
        same_sector_factor=0.30,
    )

    print("=" * 70)
    print("PORTFOLIO STRESS TEST EVALUATION")
    print("=" * 70)

    # ------------------------------------------------------------
    # Test 1: Scenario severity ordering
    # ------------------------------------------------------------

    mild = engine.run(
        entity="Apple Inc.",
        scenario="mild",
    )

    moderate = engine.run(
        entity="Apple Inc.",
        scenario="moderate",
    )

    severe = engine.run(
        entity="Apple Inc.",
        scenario="severe",
    )

    mild_loss = abs(mild["total_portfolio_impact"])
    moderate_loss = abs(moderate["total_portfolio_impact"])
    severe_loss = abs(severe["total_portfolio_impact"])

    severity_pass = (
        mild_loss < moderate_loss < severe_loss
    )

    print("\n1. SCENARIO SEVERITY")
    print(
        f"Mild       : "
        f"{mild['total_portfolio_impact']:+.4f}"
    )
    print(
        f"Moderate   : "
        f"{moderate['total_portfolio_impact']:+.4f}"
    )
    print(
        f"Severe     : "
        f"{severe['total_portfolio_impact']:+.4f}"
    )
    print(
        f"Result     : "
        f"{'PASS' if severity_pass else 'FAIL'}"
    )

    # ------------------------------------------------------------
    # Test 2: Direct exposure
    # ------------------------------------------------------------

    direct_pass = (
        abs(mild["direct_impact"] - (-0.01)) < 1e-6
    )

    print("\n2. DIRECT EXPOSURE")
    print(
        f"Expected AAPL contribution : -0.0100"
    )
    print(
        f"Actual AAPL contribution   : "
        f"{mild['direct_impact']:+.4f}"
    )
    print(
        f"Result                     : "
        f"{'PASS' if direct_pass else 'FAIL'}"
    )

    # ------------------------------------------------------------
    # Test 3: Same-sector propagation
    # ------------------------------------------------------------

    affected = mild["affected_holdings"]

    msft = next(
        row for row in affected
        if row["entity"] == "Microsoft Corporation"
    )

    nvda = next(
        row for row in affected
        if row["entity"] == "NVIDIA Corporation"
    )

    sector_pass = (
        msft["propagation_factor"] == 0.30
        and nvda["propagation_factor"] == 0.30
    )

    print("\n3. SAME-SECTOR PROPAGATION")
    print(
        f"Microsoft propagation factor : "
        f"{msft['propagation_factor']:.2f}"
    )
    print(
        f"NVIDIA propagation factor    : "
        f"{nvda['propagation_factor']:.2f}"
    )
    print(
        f"Expected factor              : 0.30"
    )
    print(
        f"Result                       : "
        f"{'PASS' if sector_pass else 'FAIL'}"
    )

    # ------------------------------------------------------------
    # Test 4: Unrelated sectors
    # ------------------------------------------------------------

    affected_entities = {
        row["entity"]
        for row in affected
    }

    unrelated_entities = {
        "JPMorgan Chase & Co.",
        "Exxon Mobil Corporation",
        "Coca-Cola Company",
    }

    unrelated_pass = not (
        affected_entities & unrelated_entities
    )

    print("\n4. UNRELATED SECTOR PROPAGATION")
    print(
        "Financials, Energy and Consumer Staples "
        "should receive no propagated shock."
    )
    print(
        f"Result : "
        f"{'PASS' if unrelated_pass else 'FAIL'}"
    )

    # ------------------------------------------------------------
    # Test 5: Direct + indirect = total
    # ------------------------------------------------------------

    reconciliation_pass = (
        abs(
            mild["direct_impact"]
            + mild["indirect_impact"]
            - mild["total_portfolio_impact"]
        )
        < 1e-6
    )

    print("\n5. IMPACT RECONCILIATION")
    print(
        f"Direct + indirect : "
        f"{mild['direct_impact'] + mild['indirect_impact']:+.4f}"
    )
    print(
        f"Total impact      : "
        f"{mild['total_portfolio_impact']:+.4f}"
    )
    print(
        f"Result            : "
        f"{'PASS' if reconciliation_pass else 'FAIL'}"
    )

    # ------------------------------------------------------------
    # Overall result
    # ------------------------------------------------------------

    all_pass = (
        severity_pass
        and direct_pass
        and sector_pass
        and unrelated_pass
        and reconciliation_pass
    )

    print("\n" + "=" * 70)
    print(
        f"OVERALL RESULT : "
        f"{'PASS' if all_pass else 'FAIL'}"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()