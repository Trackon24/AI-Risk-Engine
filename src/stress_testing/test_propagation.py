from src.stress_testing.portfolio import load_portfolio
from src.stress_testing.propagation import calculate_propagation


PORTFOLIO_PATH = "data/demo/portfolio.csv"


def main():
    portfolio = load_portfolio(PORTFOLIO_PATH)

    result = calculate_propagation(
        portfolio=portfolio,
        entity="Apple Inc.",
        shock=-0.08,
    )

    print("Risk propagation")
    print("----------------")
    print(result.to_string(index=False))

    total_impact = result["portfolio_contribution"].sum()

    print()
    print(f"Total portfolio impact: {total_impact:.2%}")


if __name__ == "__main__":
    main()