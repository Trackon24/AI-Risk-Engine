import pandas as pd


REQUIRED_COLUMNS = {"entity", "ticker", "sector", "weight"}


def load_portfolio(file_path: str) -> pd.DataFrame:
    """Load and validate a portfolio definition from CSV."""

    portfolio = pd.read_csv(file_path)

    missing_columns = REQUIRED_COLUMNS - set(portfolio.columns)

    if missing_columns:
        raise ValueError(
            f"Portfolio is missing required columns: {sorted(missing_columns)}"
        )

    if portfolio.empty:
        raise ValueError("Portfolio cannot be empty.")

    if portfolio["weight"].isna().any():
        raise ValueError("Portfolio contains missing weights.")

    if (portfolio["weight"] < 0).any():
        raise ValueError("Portfolio weights cannot be negative.")

    total_weight = portfolio["weight"].sum()

    if abs(total_weight - 1.0) > 1e-6:
        raise ValueError(
            f"Portfolio weights must sum to 1.0, got {total_weight:.4f}."
        )

    return portfolio