from pathlib import Path

from src.data.dataset_loader import TARGET_COLUMNS, build_v1_forecast_dataset
from src.data.feature_sets import DEFAULT_FEATURE_SET_NAME, FEATURE_SETS


ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "data" / "processed" / "traffic_dataset_v0_clean.csv"
RESULTS_DIR = ROOT / "results" / "v1"
SUMMARY_PATH = RESULTS_DIR / "feature_set_definition.md"


# Generate the official V1 M2 Feature Set Definition milestone artifact.
def main() -> None:
    lines = [
        "# V1 M2 Định Nghĩa Feature Set",
        "",
        "File này là artifact chính thức cho V1 M2 Feature Set Definition.",
        "",
        "## Phạm Vi",
        "",
        "Feature set xác định các cột đầu vào được dùng trong pipeline dự báo baseline V1.",
        "Cột categorical được Dataset Loader chuyển thành cột numeric cho model.",
        "",
        "## Feature Set Mặc Định",
        "",
        f"- Mặc định: `{DEFAULT_FEATURE_SET_NAME}`",
        "",
        "## Forecast Target",
        "",
        "- Forecast target khả dụng:",
        *[
            f"  - `t+{horizon}` -> `{target_column}`"
            for horizon, target_column in TARGET_COLUMNS.items()
        ],
        "",
        "## Các Feature Set",
        "",
    ]

    for feature_set in FEATURE_SETS.values():
        dataset = build_v1_forecast_dataset(
            DATASET_PATH,
            horizon=1,
            feature_set_name=feature_set.name,
        )

        lines.extend(
            [
                f"### `{feature_set.name}`",
                "",
                f"- Mô tả: {feature_set.description}",
                f"- Số lượng raw feature: {len(feature_set.raw_columns)}",
                "- Tên raw feature:",
                *[f"  - `{column}`" for column in feature_set.raw_columns],
                f"- Số lượng encoded feature: {len(dataset.feature_columns)}",
                "- Tên encoded feature:",
                *[f"  - `{column}`" for column in dataset.feature_columns],
                "",
            ]
        )

    lines.extend(
        [
            "## Validation",
            "",
            "- Trạng thái định nghĩa feature set: PASS",
            "- Tất cả feature set đã định nghĩa đều build được bằng V1 Dataset Loader.",
        ]
    )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"V1 M2 Feature Set artifact: {SUMMARY_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
