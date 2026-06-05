from pathlib import Path

from src.data.dataset_loader import (
    TARGET_COLUMNS,
    build_v1_forecast_dataset,
    load_traffic_dataset,
)
from src.data.validation import validate_dataset


ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "data" / "processed" / "traffic_dataset_v0_clean.csv"
RESULTS_DIR = ROOT / "results" / "v1"
SUMMARY_PATH = RESULTS_DIR / "dataset_loader_summary.md"


# Generate the official V1 M1 Dataset Loader milestone artifact.
def main() -> None:
    df = load_traffic_dataset(DATASET_PATH)
    validation_results = validate_dataset(df)
    dataset = build_v1_forecast_dataset(DATASET_PATH, horizon=1)

    total_rows = len(df)
    train_rows = len(dataset.train_rows)
    test_rows = len(dataset.test_rows)
    train_ratio = train_rows / total_rows
    test_ratio = test_rows / total_rows
    passed_checks = sum(result.passed for result in validation_results)
    total_checks = len(validation_results)
    validation_status = "PASS" if passed_checks == total_checks else "FAIL"

    lines = [
        "# V1 M1 Tóm Tắt Dataset Loader",
        "",
        "File này là artifact chính thức cho V1 M1 Dataset Loader.",
        "",
        "## Chia Dataset",
        "",
        f"- Tổng số dòng dataset: {total_rows:,}",
        f"- Số dòng train: {train_rows:,}",
        f"- Số dòng test: {test_rows:,}",
        f"- Tỷ lệ train/test: {train_ratio:.2%} / {test_ratio:.2%}",
        "",
        "## Feature",
        "",
        f"- Số lượng feature: {len(dataset.feature_columns)}",
        "- Tên feature:",
        *[f"  - `{feature}`" for feature in dataset.feature_columns],
        "",
        "## Forecast Target",
        "",
        "- Forecast target khả dụng:",
        *[
            f"  - `t+{horizon}` -> `{target_column}`"
            for horizon, target_column in TARGET_COLUMNS.items()
        ],
        "",
        "## Validation",
        "",
        f"- Trạng thái validation: {validation_status}",
        f"- Số check validation đạt: {passed_checks}/{total_checks}",
    ]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"V1 M1 Dataset Loader artifact: {SUMMARY_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
