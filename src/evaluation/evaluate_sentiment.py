import pandas as pd
from sklearn.metrics import classification_report

from src.risk_engine.sentiment import FinancialSentimentAnalyzer


def main():
    path = "data/evaluation/sentiment_eval.csv"

    df = pd.read_csv(path)

    analyzer = FinancialSentimentAnalyzer()

    correct = 0
    y_true = []
    y_pred = []
    results = []

    for _, row in df.iterrows():
        result = analyzer.analyze(row["text"])

        predicted = result["label"]
        actual = row["label"]

        y_true.append(actual)
        y_pred.append(predicted)

        is_correct = predicted == actual

        if is_correct:
            correct += 1

        results.append(
            {
                "actual": actual,
                "predicted": predicted,
                "correct": is_correct,
                "score": result["score"],
            }
        )

    accuracy = correct / len(df)

    print("=" * 65)
    print("FINBERT SENTIMENT EVALUATION")
    print("=" * 65)

    print(f"Examples   : {len(df)}")
    print(f"Correct    : {correct}")
    print(f"Incorrect  : {len(df) - correct}")
    print(f"Accuracy   : {accuracy:.2%}")

    print("\nPER-CLASS METRICS")
    print("-" * 65)

    print(
        classification_report(
            y_true,
            y_pred,
            labels=["positive", "neutral", "negative"],
            digits=4,
            zero_division=0,
        )
    )

    print("DETAILS")
    print("-" * 65)

    for result in results:
        status = "PASS" if result["correct"] else "FAIL"

        print(
            f"{status:6} | "
            f"Actual: {result['actual']:8} | "
            f"Predicted: {result['predicted']:8} | "
            f"Score: {result['score']:+.4f}"
        )

    print("=" * 65)


if __name__ == "__main__":
    main()