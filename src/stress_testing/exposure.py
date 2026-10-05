import pandas as pd


def calculate_direct_exposure(
    portfolio: pd.DataFrame,
    entity: str,
    shock: float,
) -> dict:
    """
    Calculate the direct portfolio impact of a company-specific shock.

    Parameters
    ----------
    portfolio : pd.DataFrame
        Portfolio containing entity names and weights.

    entity : str
        Company affected by the event.

    shock : float
        Expected percentage return shock expressed as a decimal.
        Example: -0.08 represents an 8% decline.

    Returns
    -------
    dict
        Direct exposure information and portfolio contribution.
    """

    matches = portfolio[portfolio["entity"].str.lower() == entity.lower()]

    if matches.empty:
        raise ValueError(f"Entity '{entity}' not found in portfolio.")

    holding = matches.iloc[0]

    weight = float(holding["weight"])
    portfolio_contribution = weight * shock

    return {
        "entity": holding["entity"],
        "ticker": holding["ticker"],
        "sector": holding["sector"],
        "portfolio_weight": round(weight, 4),
        "shock": round(shock, 4),
        "portfolio_contribution": round(portfolio_contribution, 4),
    }