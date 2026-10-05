import tempfile
from pathlib import Path

import pandas as pd

from src.stress_testing.portfolio import load_portfolio
from src.stress_testing.scenarios import get_scenario
from src.stress_testing.stress_engine import PortfolioStressEngine


PORTFOLIO_PATH = "data/demo/portfolio.csv"


def test_invalid_portfolio_weights():
    invalid_portfolio = pd.DataFrame(
        {
            "entity": ["Apple Inc."],
            "ticker": ["AAPL"],
            "sector": ["Technology"],
            "weight": [0.50],
        }
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        invalid_path = Path(temp_dir) / "invalid_portfolio.csv"
        invalid_portfolio.to_csv(invalid_path, index=False)

        try:
            load_portfolio(str(invalid_path))
            raise AssertionError("Invalid portfolio should have failed.")
        except ValueError:
            print("PASS: invalid portfolio weights rejected.")


def test_unknown_entity():
    portfolio = load_portfolio(PORTFOLIO_PATH)

    engine = PortfolioStressEngine(portfolio)

    try:
        engine.run(
            entity="Unknown Company",
            scenario="moderate",
        )
        raise AssertionError("Unknown entity should have failed.")
    except ValueError:
        print("PASS: unknown entity rejected.")


def test_invalid_scenario():
    try:
        get_scenario("extreme")
        raise AssertionError("Invalid scenario should have failed.")
    except ValueError:
        print("PASS: invalid scenario rejected.")


def main():
    print("Stress-testing validation tests")
    print("--------------------------------")

    test_invalid_portfolio_weights()
    test_unknown_entity()
    test_invalid_scenario()

    print()
    print("All validation tests passed.")


if __name__ == "__main__":
    main()