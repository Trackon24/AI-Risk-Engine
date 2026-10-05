from src.stress_testing.portfolio import load_portfolio
from src.stress_testing.stress_engine import PortfolioStressEngine


PORTFOLIO_PATH = "data/demo/portfolio.csv"


def main():
    portfolio = load_portfolio(PORTFOLIO_PATH)

    engine = PortfolioStressEngine(
        portfolio=portfolio,
        same_sector_factor=0.30,
    )

    for scenario in ["mild", "moderate", "severe"]:
        result = engine.run(
            entity="Apple Inc.",
            scenario=scenario,
        )

        print()
        print(f"{scenario.upper()} SCENARIO")
        print("-" * 40)
        print(f"Shock: {result['shock']:.2%}")
        print(
            f"Direct impact: "
            f"{result['direct_impact']:.2%}"
        )
        print(
            f"Indirect impact: "
            f"{result['indirect_impact']:.2%}"
        )
        print(
            f"Total portfolio impact: "
            f"{result['total_portfolio_impact']:.2%}"
        )

        print()
        print("Affected holdings:")

        for holding in result["affected_holdings"]:
            print(
                f"  {holding['ticker']}: "
                f"{holding['portfolio_contribution']:.2%}"
            )


if __name__ == "__main__":
    main()