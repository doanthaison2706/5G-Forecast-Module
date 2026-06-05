from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.data.dataset_loader import TARGET_COLUMNS, build_v1_forecast_dataset
from src.data.feature_sets import DEFAULT_FEATURE_SET_NAME
from src.evaluation.visualization import create_v1_evaluation_figures, summarize_predictions
from src.models.linear_regression import (
    evaluate_regression,
    fit_linear_regression,
    predict_linear_regression,
)


@dataclass(frozen=True)
class V2Paths:
    root: Path
    dataset_path: Path
    results_dir: Path
    horizon_dir: Path
    report_path: Path
    metrics_path: Path
    predictions_path: Path
    figures_dir: Path


# Build standard filesystem paths for the V2 Horizon Analysis pipeline.
def build_v2_paths(root: str | Path) -> V2Paths:
    project_root = Path(root)
    results_dir = project_root / "results" / "v2"
    horizon_dir = results_dir / "horizon_analysis"
    return V2Paths(
        root=project_root,
        dataset_path=project_root / "data" / "processed" / "traffic_dataset_v0_clean.csv",
        results_dir=results_dir,
        horizon_dir=horizon_dir,
        report_path=horizon_dir / "README.md",
        metrics_path=horizon_dir / "horizon_metrics.csv",
        predictions_path=horizon_dir / "horizon_predictions.csv",
        figures_dir=horizon_dir / "figures",
    )


# Run V2 Experiment 1: Forecast Horizon Analysis.
def run_v2_horizon_analysis(paths: V2Paths) -> None:
    paths.horizon_dir.mkdir(parents=True, exist_ok=True)

    run_rows, predictions = _run_horizon_benchmark(paths.dataset_path)
    metrics = summarize_predictions(predictions)
    metrics = _add_horizon_diagnostics(metrics)
    figure_paths = create_v1_evaluation_figures(predictions, metrics, paths.figures_dir)

    predictions.to_csv(paths.predictions_path, index=False)
    metrics.to_csv(paths.metrics_path, index=False)
    paths.report_path.write_text(
        _build_horizon_report(
            paths=paths,
            run_rows=run_rows,
            metrics=metrics,
            figure_paths=figure_paths,
        ),
        encoding="utf-8",
    )


# Train one baseline model per horizon while keeping model and feature set fixed.
def _run_horizon_benchmark(dataset_path: Path) -> tuple[list[dict[str, object]], pd.DataFrame]:
    rows = []
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

        rows.append(
            {
                "horizon": f"t+{horizon}",
                "target": dataset.target_column,
                "feature_set": DEFAULT_FEATURE_SET_NAME,
                "encoded_features": len(dataset.feature_columns),
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

    return rows, pd.concat(prediction_frames, ignore_index=True)


# Add V2-specific horizon comparison fields to the metric table.
def _add_horizon_diagnostics(metrics: pd.DataFrame) -> pd.DataFrame:
    enriched = metrics.copy()
    baseline_mae = float(enriched.iloc[0]["mae"])
    baseline_rmse = float(enriched.iloc[0]["rmse"])
    baseline_r2 = float(enriched.iloc[0]["r2"])

    enriched["mae_increase_vs_t_plus_1"] = enriched["mae"] - baseline_mae
    enriched["rmse_increase_vs_t_plus_1"] = enriched["rmse"] - baseline_rmse
    enriched["r2_drop_vs_t_plus_1"] = baseline_r2 - enriched["r2"]
    enriched["decision"] = enriched.apply(_classify_horizon, axis=1)
    return enriched


# Classify whether a horizon is suitable for V2 Forecast State integration.
def _classify_horizon(row: pd.Series) -> str:
    if row["r2"] >= 0.9 and row["mae"] <= 0.08:
        return "recommended"
    if row["r2"] >= 0.75 and row["mae"] <= 0.12:
        return "usable"
    return "risky"


# Build the V2 Horizon Analysis report in Vietnamese.
def _build_horizon_report(
    paths: V2Paths,
    run_rows: list[dict[str, object]],
    metrics: pd.DataFrame,
    figure_paths: list[Path],
) -> str:
    best_row = metrics.sort_values(["mae", "rmse"], ascending=True).iloc[0]
    longest_usable = metrics[metrics["decision"].isin(["recommended", "usable"])].iloc[-1]

    lines = [
        "# V2 Experiment 1 - Forecast Horizon Analysis",
        "",
        "Mục tiêu của thí nghiệm này là kiểm tra sai số dự báo thay đổi như thế nào khi horizon dài hơn.",
        "",
        "## Cấu Hình Cố Định",
        "",
        "- Model: `linear_regression`",
        f"- Feature set: `{DEFAULT_FEATURE_SET_NAME}`",
        "- Train/test split: 80/20 theo `episode_id`",
        "- Horizon so sánh: `t+1`, `t+5`, `t+10`",
        "",
        "## Kết Quả Train/Predict",
        "",
        "| Horizon | Target | Feature set | Encoded feature | Dòng train | Dòng predict | MAE | RMSE | R² |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]

    for row in run_rows:
        lines.append(
            "| "
            f"{row['horizon']} | "
            f"`{row['target']}` | "
            f"`{row['feature_set']}` | "
            f"{row['encoded_features']} | "
            f"{row['train_rows']:,} | "
            f"{row['predict_rows']:,} | "
            f"{row['mae']:.6f} | "
            f"{row['rmse']:.6f} | "
            f"{row['r2']:.6f} |"
        )

    lines.extend(
        [
            "",
            "## Horizon Diagnostics",
            "",
            "| Horizon | MAE | RMSE | R² | MAE tăng so với t+1 | RMSE tăng so với t+1 | R² giảm so với t+1 | Quyết định |",
            "|---|---:|---:|---:|---:|---:|---:|---|",
        ]
    )

    for row in metrics.itertuples(index=False):
        lines.append(
            "| "
            f"{row.horizon} | "
            f"{row.mae:.6f} | "
            f"{row.rmse:.6f} | "
            f"{row.r2:.6f} | "
            f"{row.mae_increase_vs_t_plus_1:.6f} | "
            f"{row.rmse_increase_vs_t_plus_1:.6f} | "
            f"{row.r2_drop_vs_t_plus_1:.6f} | "
            f"`{row.decision}` |"
        )

    lines.extend(
        [
            "",
            "## Nhận Định",
            "",
            f"- Horizon tốt nhất theo MAE/RMSE là `{best_row.horizon}`.",
            f"- Horizon dài nhất còn đạt ngưỡng usable là `{longest_usable.horizon}`.",
            "- Sai số tăng khi horizon dài hơn, nên V2 Predictive RL nên ưu tiên forecast ngắn hạn nếu chỉ cần một tín hiệu ổn định.",
            "",
            "Figure đã tạo:",
            "",
            *[f"- `{path.relative_to(paths.root)}`" for path in figure_paths],
            "",
            "## Artifact",
            "",
            f"- Report: `{paths.report_path.relative_to(paths.root)}`",
            f"- Metric CSV: `{paths.metrics_path.relative_to(paths.root)}`",
            f"- Prediction CSV: `{paths.predictions_path.relative_to(paths.root)}`",
            f"- Figure: `{paths.figures_dir.relative_to(paths.root)}/`",
            "",
            "## Kết Luận",
            "",
            f"- Forecast Horizon được đề xuất cho V2 hiện tại: `{best_row.horizon}`.",
            "- Có thể chuyển sang V2 Experiment 2 - Feature Contribution Analysis.",
        ]
    )

    return "\n".join(lines) + "\n"
