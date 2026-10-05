from src.stress_testing.propagation import calculate_propagation
from src.stress_testing.scenarios import get_scenario


class PortfolioStressEngine:
    """Run event-driven portfolio stress scenarios."""

    def __init__(
        self,
        portfolio,
        same_sector_factor: float = 0.30,
    ):
        self.portfolio = portfolio
        self.same_sector_factor = same_sector_factor

    def run(
        self,
        entity: str,
        scenario: str,
    ) -> dict:
        """Run a stress scenario for an affected company."""

        scenario_config = get_scenario(scenario)

        propagation = calculate_propagation(
            portfolio=self.portfolio,
            entity=entity,
            shock=scenario_config["shock"],
            same_sector_factor=self.same_sector_factor,
        )

        total_impact = propagation["portfolio_contribution"].sum()

        direct_impact = propagation.loc[
            propagation["entity"].str.lower() == entity.lower(),
            "portfolio_contribution",
        ].sum()

        indirect_impact = total_impact - direct_impact

        affected_holdings = propagation[
            propagation["propagation_factor"] > 0
        ].copy()

        affected_holdings["portfolio_contribution"] = (
            affected_holdings["portfolio_contribution"].round(4)
        )

        affected_holdings = affected_holdings.sort_values(
            "portfolio_contribution"
        )

        return {
            "entity": entity,
            "scenario": scenario_config["name"],
            "scenario_description": scenario_config["description"],
            "shock": scenario_config["shock"],
            "direct_impact": round(float(direct_impact), 4),
            "indirect_impact": round(float(indirect_impact), 4),
            "total_portfolio_impact": round(float(total_impact), 4),
            "affected_holdings": affected_holdings.to_dict(
                orient="records"
            ),
        }