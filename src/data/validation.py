from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.data.dataset_loader import REQUIRED_COLUMNS


TARGET_HORIZONS = {
    "traffic_load_t_plus_1": 1,
    "traffic_load_t_plus_5": 5,
    "traffic_load_t_plus_10": 10,
}


@dataclass(frozen=True)
class ValidationResult:
    name: str
    passed: bool
    details: str


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates()
    cleaned = cleaned.sort_values(["episode_id", "step"]).reset_index(drop=True)
    return cleaned


def validate_dataset(df: pd.DataFrame) -> list[ValidationResult]:
    results: list[ValidationResult] = []

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    results.append(
        ValidationResult(
            "required_columns",
            not missing_columns,
            "Có đủ các cột bắt buộc."
            if not missing_columns
            else f"Thiếu cột: {missing_columns}",
        )
    )
    if missing_columns:
        return results

    missing_values = int(df.isna().sum().sum())
    results.append(
        ValidationResult(
            "missing_values",
            missing_values == 0,
            f"Tổng giá trị thiếu: {missing_values}",
        )
    )

    duplicate_rows = int(df.duplicated().sum())
    results.append(
        ValidationResult(
            "duplicate_rows",
            duplicate_rows == 0,
            f"Số dòng trùng lặp: {duplicate_rows}",
        )
    )

    traffic_columns = ["traffic_load", *TARGET_HORIZONS.keys()]
    out_of_range = {
        column: int((~df[column].between(0.0, 1.0)).sum()) for column in traffic_columns
    }
    results.append(
        ValidationResult(
            "traffic_range",
            all(count == 0 for count in out_of_range.values()),
            f"Số dòng ngoài khoảng [0, 1]: {out_of_range}",
        )
    )

    invalid_ue = int((df["ue_count"] < 0).sum())
    results.append(
        ValidationResult(
            "ue_count_range",
            invalid_ue == 0,
            f"Số dòng có ue_count âm: {invalid_ue}",
        )
    )

    invalid_demand = int((df["traffic_demand_bps"] < 0).sum())
    results.append(
        ValidationResult(
            "traffic_demand_range",
            invalid_demand == 0,
            f"Số dòng có traffic_demand_bps âm: {invalid_demand}",
        )
    )

    invalid_time_ratio = int((~df["time_ratio"].between(0.0, 1.0)).sum())
    results.append(
        ValidationResult(
            "time_ratio_range",
            invalid_time_ratio == 0,
            f"Số dòng ngoài khoảng [0, 1]: {invalid_time_ratio}",
        )
    )

    step_results = _validate_episode_steps(df)
    results.extend(step_results)
    results.extend(_validate_target_alignment(df))

    return results


def write_dataset_summary(df: pd.DataFrame, output_path: str | Path) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    numeric_summary = df.describe().T
    numeric_summary.insert(0, "column_type", "numeric")

    event_counts = (
        df["mobility_event"]
        .value_counts()
        .rename_axis("value")
        .reset_index(name="count")
    )
    event_counts.insert(0, "column", "mobility_event")

    with output.open("w", encoding="utf-8") as file:
        numeric_summary.to_csv(file)
        file.write("\n[mobility_event_counts]\n")
        event_counts.to_csv(file, index=False)


def write_validation_report(
    df: pd.DataFrame,
    results: list[ValidationResult],
    output_path: str | Path,
) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    passed = sum(result.passed for result in results)
    total = len(results)
    status = "PASS" if passed == total else "FAIL"
    episode_count = df["episode_id"].nunique()
    row_count = len(df)
    step_count = df.groupby("episode_id").size()

    lines = [
        "# Báo Cáo Validation Dataset V0",
        "",
        f"Trạng thái tổng thể: **{status}**",
        "",
        "## Dataset",
        "",
        f"- Số dòng: {row_count}",
        f"- Số cột: {len(df.columns)}",
        f"- Số episode: {episode_count}",
        f"- Số dòng mỗi episode: min={step_count.min()}, max={step_count.max()}, mean={step_count.mean():.2f}",
        "",
        "## Check",
        "",
        "| Check | Trạng thái | Chi tiết |",
        "|---|---:|---|",
    ]

    for result in results:
        check_status = "PASS" if result.passed else "FAIL"
        details = result.details.replace("|", "\\|")
        lines.append(f"| {result.name} | {check_status} | {details} |")

    lines.extend(
        [
            "",
        "## Kết Luận V0",
        "",
        "Dataset phù hợp để chuyển sang V1 baseline forecasting khi tất cả check đều PASS.",
        "Target alignment được kiểm tra ở các dòng có future step trong dataset đã export.",
        ]
    )

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _validate_episode_steps(df: pd.DataFrame) -> list[ValidationResult]:
    grouped = df.groupby("episode_id")["step"]
    duplicate_steps = int(df.duplicated(["episode_id", "step"]).sum())
    monotonic_failures = 0
    continuity_failures = 0

    for _, steps in grouped:
        sorted_steps = steps.sort_values().to_numpy()
        if not np.array_equal(steps.to_numpy(), sorted_steps):
            monotonic_failures += 1
        expected = np.arange(sorted_steps.min(), sorted_steps.max() + 1)
        if not np.array_equal(sorted_steps, expected):
            continuity_failures += 1

    return [
        ValidationResult(
            "episode_step_duplicates",
            duplicate_steps == 0,
            f"Số cặp episode-step trùng lặp: {duplicate_steps}",
        ),
        ValidationResult(
            "episode_step_order",
            monotonic_failures == 0,
            f"Số episode không được sort theo step: {monotonic_failures}",
        ),
        ValidationResult(
            "episode_step_continuity",
            continuity_failures == 0,
            f"Số episode bị thiếu step: {continuity_failures}",
        ),
    ]


def _validate_target_alignment(df: pd.DataFrame) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    indexed = df.set_index(["episode_id", "step"])["traffic_load"]

    for target_column, horizon in TARGET_HORIZONS.items():
        comparable = 0
        mismatches = 0

        for row in df[["episode_id", "step", target_column]].itertuples(index=False):
            key = (row.episode_id, row.step + horizon)
            if key not in indexed.index:
                continue
            comparable += 1
            expected = indexed.loc[key]
            actual = getattr(row, target_column)
            if not np.isclose(actual, expected, rtol=1e-7, atol=1e-7):
                mismatches += 1

        results.append(
            ValidationResult(
                f"{target_column}_alignment",
                mismatches == 0,
                f"Số dòng so sánh được: {comparable}; số mismatch: {mismatches}",
            )
        )

    return results
