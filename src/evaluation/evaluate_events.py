import pandas as pd

from src.risk_engine.event_classifier import FinancialEventClassifier


def main():
    path = "data/evaluation/event_eval.csv"

    df = pd.read_csv(path)

    classifier = FinancialEventClassifier()

    correct = 0
    results = []

    for _, row in df.iterrows():
        prediction = classifier.classify(row["text"])
        predicted = prediction["event"]
        actual = row["label"]

        is_correct = predicted == actual

        if is_correct:
            correct += 1

        results.append(
            {
                "actual": actual,
                "predicted": predicted,
                "correct": is_correct,
                "confidence": prediction["confidence"],
                "matched_keywords": prediction["matched_keywords"],
            }
        )

    accuracy = correct / len(df)

    print("=" * 65)
    print("EVENT CLASSIFICATION EVALUATION")
    print("=" * 65)

    print(f"Examples   : {len(df)}")
    print(f"Correct    : {correct}")
    print(f"Incorrect  : {len(df) - correct}")
    print(f"Accuracy   : {accuracy:.2%}")

    print("\nDETAILS")
    print("-" * 65)

    for result in results:
        status = "PASS" if result["correct"] else "FAIL"

        print(
            f"{status:6} | "
            f"Actual: {result['actual']:17} | "
            f"Predicted: {result['predicted']:17} | "
            f"Confidence: {result['confidence']:.4f}"
        )

    print("=" * 65)


if __name__ == "__main__":
    main()