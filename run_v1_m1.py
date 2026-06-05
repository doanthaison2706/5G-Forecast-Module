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
        "# V1 M1 Dataset Loader Summary",
        "",
        "This file is the official milestone artifact for V1 M1 Dataset Loader.",
        "",
        "## Dataset Split",
        "",
        f"- Total dataset rows: {total_rows:,}",
        f"- Train rows: {train_rows:,}",
        f"- Test rows: {test_rows:,}",
        f"- Train/test ratio: {train_ratio:.2%} / {test_ratio:.2%}",
        "",
        "## Features",
        "",
        f"- Feature count: {len(dataset.feature_columns)}",
        "- Feature names:",
        *[f"  - `{feature}`" for feature in dataset.feature_columns],
        "",
        "## Forecast Targets",
        "",
        "- Available forecast targets:",
        *[
            f"  - `t+{horizon}` -> `{target_column}`"
            for horizon, target_column in TARGET_COLUMNS.items()
        ],
        "",
        "## Validation",
        "",
        f"- Validation status: {validation_status}",
        f"- Validation checks passed: {passed_checks}/{total_checks}",
    ]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"V1 M1 Dataset Loader artifact: {SUMMARY_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
