from src.stress_testing.portfolio import load_portfolio
from src.stress_testing.exposure import calculate_direct_exposure


PORTFOLIO_PATH = "data/demo/portfolio.csv"


def main():
    portfolio = load_portfolio(PORTFOLIO_PATH)

    result = calculate_direct_exposure(
        portfolio=portfolio,
        entity="Apple Inc.",
        shock=-0.08,
    )

    print("Direct exposure calculation")
    print("---------------------------")
    print(f"Entity: {result['entity']}")
    print(f"Ticker: {result['ticker']}")
    print(f"Sector: {result['sector']}")
    print(f"Portfolio weight: {result['portfolio_weight']:.2%}")
    print(f"Shock: {result['shock']:.2%}")
    print(f"Portfolio contribution: {result['portfolio_contribution']:.2%}")


if __name__ == "__main__":
    main()