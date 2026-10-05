import pandas as pd


DEFAULT_SAME_SECTOR_FACTOR = 0.30


def calculate_propagation(
    portfolio: pd.DataFrame,
    entity: str,
    shock: float,
    same_sector_factor: float = DEFAULT_SAME_SECTOR_FACTOR,
) -> pd.DataFrame:
    """
    Propagate a company-specific shock through the portfolio.

    The affected company receives the full shock.
    Other holdings in the same sector receive a fraction
    controlled by same_sector_factor.
    Holdings in other sectors receive no propagated shock.
    """

    matches = portfolio[
        portfolio["entity"].str.lower() == entity.lower()
    ]

    if matches.empty:
        raise ValueError(f"Entity '{entity}' not found in portfolio.")

    source = matches.iloc[0]
    source_sector = source["sector"]

    results = portfolio.copy()

    results["propagation_factor"] = 0.0

    source_mask = results["entity"].str.lower() == entity.lower()
    same_sector_mask = (
        results["sector"].str.lower() == str(source_sector).lower()
    )

    results.loc[source_mask, "propagation_factor"] = 1.0

    results.loc[
        same_sector_mask & ~source_mask,
        "propagation_factor"
    ] = same_sector_factor

    results["scenario_shock"] = (
        shock * results["propagation_factor"]
    )

    results["portfolio_contribution"] = (
        results["weight"] * results["scenario_shock"]
    )

    return results[
        [
            "entity",
            "ticker",
            "sector",
            "weight",
            "propagation_factor",
            "scenario_shock",
            "portfolio_contribution",
        ]
    ]