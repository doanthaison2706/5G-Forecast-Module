from pathlib import Path

import pandas as pd

from src.data.dataset_loader import TARGET_COLUMNS, build_v1_forecast_dataset
from src.data.feature_sets import DEFAULT_FEATURE_SET_NAME
from src.models.linear_regression import (
    evaluate_regression,
    fit_linear_regression,
    predict_linear_regression,
)


ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "data" / "processed" / "traffic_dataset_v0_clean.csv"
RESULTS_DIR = ROOT / "results" / "v1"
SUMMARY_PATH = RESULTS_DIR / "linear_regression_baseline.md"
PREDICTION_PATH = RESULTS_DIR / "linear_regression_predictions.csv"


# Generate the official V1 M3 Linear Regression Baseline milestone artifact.
def main() -> None:
    result_rows = []
    prediction_frames = []

    for horizon in TARGET_COLUMNS:
        dataset = build_v1_forecast_dataset(
            DATASET_PATH,
            horizon=horizon,
            feature_set_name=DEFAULT_FEATURE_SET_NAME,
        )
        model = fit_linear_regression(dataset.features_train, dataset.target_train)
        predictions = predict_linear_regression(model, dataset.features_test)
        metrics = evaluate_regression(dataset.target_test, predictions)

        result_rows.append(
            {
                "horizon": f"t+{horizon}",
                "target": dataset.target_column,
                "train_rows": len(dataset.target_train),
                "predict_rows": len(predictions),
                "mae": metrics.mae,
                "rmse": metrics.rmse,
                "r2": metrics.r2,
            }
        )

        prediction_frames.append(
            pd.DataFrame(
                {
                    "horizon": f"t+{horizon}",
                    "episode_id": dataset.test_rows["episode_id"],
                    "step": dataset.test_rows["step"],
                    "actual": dataset.target_test,
                    "prediction": predictions,
                }
            )
        )

    results = pd.DataFrame(result_rows)
    predictions = pd.concat(prediction_frames, ignore_index=True)

    lines = [
        "# V1 M3 Linear Regression Baseline",
        "",
        "File này là artifact chính thức cho V1 M3 Linear Regression Baseline.",
        "",
        "## Cấu hình",
        "",
        f"- Model: Linear Regression",
        f"- Feature set: `{DEFAULT_FEATURE_SET_NAME}`",
        "- Train/test split: 80% / 20% theo `episode_id`",
        "- Forecast target: `t+1`, `t+5`, `t+10`",
        "",
        "## Kết Quả Output",
        "",
        "- Train: hoàn tất cho tất cả forecast target.",
        f"- Predict: đã ghi `{PREDICTION_PATH.relative_to(ROOT)}`.",
        "- Metric: MAE, RMSE, R².",
        "",
        "## Kết quả",
        "",
        "| Horizon | Target | Dòng train | Dòng predict | MAE | RMSE | R² |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]

    for row in results.itertuples(index=False):
        lines.append(
            "| "
            f"{row.horizon} | "
            f"`{row.target}` | "
            f"{row.train_rows:,} | "
            f"{row.predict_rows:,} | "
            f"{row.mae:.6f} | "
            f"{row.rmse:.6f} | "
            f"{row.r2:.6f} |"
        )

    lines.extend(
        [
            "",
            "## Kết luận M3",
            "",
            "- Trạng thái train: PASS",
            "- Trạng thái predict: PASS",
            "- Trạng thái đánh giá metric: PASS",
            "- Baseline này dùng làm mốc so sánh cho các cấu hình V1/V2 tiếp theo.",
        ]
    )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    predictions.to_csv(PREDICTION_PATH, index=False)

    print(f"V1 M3 Linear Regression artifact: {SUMMARY_PATH.relative_to(ROOT)}")
    print(f"V1 M3 prediction output: {PREDICTION_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
