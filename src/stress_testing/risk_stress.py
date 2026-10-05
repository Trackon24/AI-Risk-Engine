from src.stress_testing.stress_engine import PortfolioStressEngine


class RiskSignalStressTester:
    """
    Connect a unified risk signal to the portfolio stress engine.
    """

    def __init__(
        self,
        portfolio,
        same_sector_factor: float = 0.30,
    ):
        self.engine = PortfolioStressEngine(
            portfolio=portfolio,
            same_sector_factor=same_sector_factor,
        )

    def run(
        self,
        risk_signal: dict,
        scenario: str,
    ) -> dict:
        """
        Stress-test a portfolio using a unified risk signal.
        """

        entity = risk_signal.get("entity")

        if not entity:
            raise ValueError("Risk signal must contain an entity.")

        stress_result = self.engine.run(
            entity=entity,
            scenario=scenario,
        )

        return {
            "risk_signal": risk_signal,
            "stress_test": stress_result,
        }