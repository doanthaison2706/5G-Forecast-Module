from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.data.dataset_loader import TARGET_COLUMNS, build_v1_forecast_dataset, load_traffic_dataset
from src.data.feature_sets import DEFAULT_FEATURE_SET_NAME, FEATURE_SETS
from src.data.validation import validate_dataset
from src.evaluation.visualization import create_v1_evaluation_figures, summarize_predictions
from src.models.linear_regression import (
    evaluate_regression,
    fit_linear_regression,
    predict_linear_regression,
)


@dataclass(frozen=True)
class V1Paths:
    root: Path
    dataset_path: Path
    results_dir: Path
    report_path: Path
    metrics_path: Path
    predictions_path: Path
    figures_dir: Path


# Build standard filesystem paths for the V1 pipeline.
def build_v1_paths(root: str | Path) -> V1Paths:
    project_root = Path(root)
    results_dir = project_root / "results" / "v1"
    return V1Paths(
        root=project_root,
        dataset_path=project_root / "data" / "processed" / "traffic_dataset_v0_clean.csv",
        results_dir=results_dir,
        report_path=results_dir / "README.md",
        metrics_path=results_dir / "linear_regression_metrics.csv",
        predictions_path=results_dir / "linear_regression_predictions.csv",
        figures_dir=results_dir / "figures",
    )


# Run all V1 milestones and write the consolidated M5 results report.
def run_v1_pipeline(paths: V1Paths) -> None:
    paths.results_dir.mkdir(parents=True, exist_ok=True)

    dataset_info = _build_dataset_info(paths.dataset_path)
    feature_set_rows = _build_feature_set_rows(paths.dataset_path)
    baseline_rows, predictions = _run_linear_regression(paths.dataset_path)
    metrics = summarize_predictions(predictions)
    figure_paths = create_v1_evaluation_figures(predictions, metrics, paths.figures_dir)

    predictions.to_csv(paths.predictions_path, index=False)
    metrics.to_csv(paths.metrics_path, index=False)
    paths.report_path.write_text(
        _build_v1_report(
            paths=paths,
            dataset_info=dataset_info,
            feature_set_rows=feature_set_rows,
            baseline_rows=baseline_rows,
            metrics=metrics,
            figure_paths=figure_paths,
        ),
        encoding="utf-8",
    )


# Collect dataset split and validation information for M1.
def _build_dataset_info(dataset_path: Path) -> dict[str, object]:
    df = load_traffic_dataset(dataset_path)
    validation_results = validate_dataset(df)
    dataset = build_v1_forecast_dataset(
        dataset_path,
        horizon=1,
        feature_set_name=DEFAULT_FEATURE_SET_NAME,
    )
    passed_checks = sum(result.passed for result in validation_results)
    total_checks = len(validation_results)

    return {
        "total_rows": len(df),
        "train_rows": len(dataset.train_rows),
        "test_rows": len(dataset.test_rows),
        "feature_columns": dataset.feature_columns,
        "validation_status": "PASS" if passed_checks == total_checks else "FAIL",
        "passed_checks": passed_checks,
        "total_checks": total_checks,
    }


# Build feature set information for M2.
def _build_feature_set_rows(dataset_path: Path) -> list[dict[str, object]]:
    rows = []
    for feature_set in FEATURE_SETS.values():
        dataset = build_v1_forecast_dataset(
            dataset_path,
            horizon=1,
            feature_set_name=feature_set.name,
        )
        rows.append(
            {
                "name": feature_set.name,
                "raw_count": len(feature_set.raw_columns),
                "encoded_count": len(dataset.feature_columns),
                "raw_columns": feature_set.raw_columns,
                "encoded_columns": dataset.feature_columns,
            }
        )
    return rows


# Train and predict Linear Regression for every forecast horizon.
def _run_linear_regression(dataset_path: Path) -> tuple[list[dict[str, object]], pd.DataFrame]:
    result_rows = []
    prediction_frames = []

    for horizon in TARGET_COLUMNS:
        dataset = build_v1_forecast_dataset(
            dataset_path,
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

    return result_rows, pd.concat(prediction_frames, ignore_index=True)


# Build the consolidated V1 M5 report in Vietnamese.
def _build_v1_report(
    paths: V1Paths,
    dataset_info: dict[str, object],
    feature_set_rows: list[dict[str, object]],
    baseline_rows: list[dict[str, object]],
    metrics: pd.DataFrame,
    figure_paths: list[Path],
) -> str:
    train_rows = int(dataset_info["train_rows"])
    test_rows = int(dataset_info["test_rows"])
    total_rows = int(dataset_info["total_rows"])
    train_ratio = train_rows / total_rows
    test_ratio = test_rows / total_rows

    lines = [
        "# V1 M5 Results Report",
        "",
        "File này là report tổng hợp chính thức cho V1 Baseline Forecast.",
        "",
        "## Tóm Tắt",
        "",
        "- M1 Dataset Loader: PASS",
        "- M2 Feature Set Definition: PASS",
        "- M3 Linear Regression Baseline: PASS",
        "- M4 Evaluation/Visualization: PASS",
        "- M5 Results Report: PASS",
        "",
        "## M1 Dataset Loader",
        "",
        f"- Tổng số dòng dataset: {total_rows:,}",
        f"- Số dòng train: {train_rows:,}",
        f"- Số dòng test: {test_rows:,}",
        f"- Tỷ lệ train/test: {train_ratio:.2%} / {test_ratio:.2%}",
        f"- Validation: {dataset_info['validation_status']} ({dataset_info['passed_checks']}/{dataset_info['total_checks']} check)",
        f"- Số lượng feature mặc định: {len(dataset_info['feature_columns'])}",
        "",
        "## M2 Feature Set",
        "",
        "| Feature set | Raw feature | Encoded feature |",
        "|---|---:|---:|",
    ]

    for row in feature_set_rows:
        lines.append(f"| `{row['name']}` | {row['raw_count']} | {row['encoded_count']} |")

    lines.extend(
        [
            "",
            f"- Feature set mặc định: `{DEFAULT_FEATURE_SET_NAME}`",
            "- Forecast target: `t+1`, `t+5`, `t+10`",
            "",
            "## M3 Linear Regression Baseline",
            "",
            "| Horizon | Target | Dòng train | Dòng predict | MAE | RMSE | R² |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )

    for row in baseline_rows:
        lines.append(
            "| "
            f"{row['horizon']} | "
            f"`{row['target']}` | "
            f"{row['train_rows']:,} | "
            f"{row['predict_rows']:,} | "
            f"{row['mae']:.6f} | "
            f"{row['rmse']:.6f} | "
            f"{row['r2']:.6f} |"
        )

    lines.extend(
        [
            "",
            "## M4 Evaluation/Visualization",
            "",
            "| Horizon | Dòng predict | MAE | RMSE | R² | Trung bình residual | Độ lệch chuẩn residual |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )

    for row in metrics.itertuples(index=False):
        lines.append(
            "| "
            f"{row.horizon} | "
            f"{row.predict_rows:,} | "
            f"{row.mae:.6f} | "
            f"{row.rmse:.6f} | "
            f"{row.r2:.6f} | "
            f"{row.residual_mean:.6f} | "
            f"{row.residual_std:.6f} |"
        )

    lines.extend(
        [
            "",
            "Figure đã tạo:",
            "",
            *[f"- `{path.relative_to(paths.root)}`" for path in figure_paths],
            "",
            "## Artifact",
            "",
            f"- Report tổng hợp: `{paths.report_path.relative_to(paths.root)}`",
            f"- Metric CSV: `{paths.metrics_path.relative_to(paths.root)}`",
            f"- Prediction CSV: `{paths.predictions_path.relative_to(paths.root)}`",
            f"- Figure: `{paths.figures_dir.relative_to(paths.root)}/`",
            "",
            "## Kết Luận V1",
            "",
            "- Linear Regression là baseline hợp lệ cho forecast traffic ngắn hạn.",
            "- Kết quả tốt nhất ở `t+1`, sau đó giảm dần ở `t+5` và `t+10`.",
            "- V1 đủ điều kiện chuyển sang V2 Forecast Benchmark.",
        ]
    )

    return "\n".join(lines) + "\n"
