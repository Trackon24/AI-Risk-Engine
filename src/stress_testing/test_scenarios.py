from src.stress_testing.scenarios import get_scenario


def main():
    print("Stress scenarios")
    print("----------------")

    for name in ["mild", "moderate", "severe"]:
        scenario = get_scenario(name)

        print(
            f"{scenario['name'].capitalize():<10}"
            f" Shock: {scenario['shock']:.2%}"
            f" | {scenario['description']}"
        )


if __name__ == "__main__":
    main()