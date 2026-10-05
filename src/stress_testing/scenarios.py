SCENARIOS = {
    "mild": {
        "shock": -0.04,
        "description": "Limited adverse event impact",
    },
    "moderate": {
        "shock": -0.08,
        "description": "Material adverse event impact",
    },
    "severe": {
        "shock": -0.15,
        "description": "Severe adverse event impact",
    },
}


def get_scenario(name: str) -> dict:
    """Return the configuration for a named stress scenario."""

    scenario_name = name.lower()

    if scenario_name not in SCENARIOS:
        valid = ", ".join(SCENARIOS.keys())
        raise ValueError(
            f"Unknown scenario '{name}'. Choose from: {valid}."
        )

    return {
        "name": scenario_name,
        **SCENARIOS[scenario_name],
    }