from src.stress_testing.portfolio import load_portfolio


PORTFOLIO_PATH = "data/demo/portfolio.csv"


def main():
    portfolio = load_portfolio(PORTFOLIO_PATH)

    print("Portfolio loaded successfully.")
    print()
    print(portfolio)
    print()
    print(f"Number of holdings: {len(portfolio)}")
    print(f"Total weight: {portfolio['weight'].sum():.2f}")


if __name__ == "__main__":
    main()