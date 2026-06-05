from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.data.dataset_loader import TARGET_COLUMNS, build_v1_forecast_dataset, load_traffic_dataset
from src.data.feature_sets import DEFAULT_FEATURE_SET_NAME, FEATURE_SETS
from src.evaluation.visualization import create_v1_evaluation_figures, summarize_predictions
from src.models.linear_regression import (
    evaluate_regression,
    fit_linear_regression,
    predict_linear_regression,
)
from src.models.random_forest import fit_random_forest, predict_random_forest


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
    window_dir: Path
    window_report_path: Path
    window_metrics_path: Path
    window_predictions_path: Path
    window_figures_dir: Path
    feature_dir: Path
    feature_report_path: Path
    feature_metrics_path: Path
    feature_predictions_path: Path
    feature_figures_dir: Path
    model_dir: Path
    model_report_path: Path
    model_metrics_path: Path
    model_predictions_path: Path
    model_figures_dir: Path


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
        window_dir=results_dir / "window_analysis",
        window_report_path=results_dir / "window_analysis" / "README.md",
        window_metrics_path=results_dir / "window_analysis" / "window_metrics.csv",
        window_predictions_path=results_dir / "window_analysis" / "window_predictions.csv",
        window_figures_dir=results_dir / "window_analysis" / "figures",
        feature_dir=results_dir / "feature_analysis",
        feature_report_path=results_dir / "feature_analysis" / "README.md",
        feature_metrics_path=results_dir / "feature_analysis" / "feature_metrics.csv",
        feature_predictions_path=results_dir / "feature_analysis" / "feature_predictions.csv",
        feature_figures_dir=results_dir / "feature_analysis" / "figures",
        model_dir=results_dir / "model_comparison",
        model_report_path=results_dir / "model_comparison" / "README.md",
        model_metrics_path=results_dir / "model_comparison" / "model_metrics.csv",
        model_predictions_path=results_dir / "model_comparison" / "model_predictions.csv",
        model_figures_dir=results_dir / "model_comparison" / "figures",
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


# Run V2 Experiment 2: History Window Analysis.
def run_v2_window_analysis(paths: V2Paths) -> None:
    paths.window_dir.mkdir(parents=True, exist_ok=True)

    run_rows, predictions = _run_window_benchmark(paths.dataset_path)
    metrics = _summarize_window_predictions(predictions)
    metrics = _add_window_diagnostics(metrics)
    figure_predictions = predictions.rename(columns={"window": "horizon"})
    figure_metrics = metrics.rename(columns={"window": "horizon"})
    stale_metric_figure = paths.window_figures_dir / "linear_regression_metrics_by_horizon.png"
    if stale_metric_figure.exists():
        stale_metric_figure.unlink()
    figure_paths = create_v1_evaluation_figures(
        figure_predictions,
        figure_metrics,
        paths.window_figures_dir,
        group_label="window",
    )

    predictions.to_csv(paths.window_predictions_path, index=False)
    metrics.to_csv(paths.window_metrics_path, index=False)
    paths.window_report_path.write_text(
        _build_window_report(
            paths=paths,
            run_rows=run_rows,
            metrics=metrics,
            figure_paths=figure_paths,
        ),
        encoding="utf-8",
    )


# Run V2 Experiment 3: Feature Contribution Analysis.
def run_v2_feature_analysis(paths: V2Paths) -> None:
    paths.feature_dir.mkdir(parents=True, exist_ok=True)

    run_rows, predictions = _run_feature_benchmark(paths.dataset_path)
    metrics = _summarize_feature_predictions(predictions)
    metrics = _add_feature_diagnostics(metrics)
    figure_predictions = predictions.rename(columns={"feature_set": "horizon"})
    figure_metrics = metrics.rename(columns={"feature_set": "horizon"})
    figure_paths = create_v1_evaluation_figures(
        figure_predictions,
        figure_metrics,
        paths.feature_figures_dir,
        group_label="feature_set",
    )

    predictions.to_csv(paths.feature_predictions_path, index=False)
    metrics.to_csv(paths.feature_metrics_path, index=False)
    paths.feature_report_path.write_text(
        _build_feature_report(
            paths=paths,
            run_rows=run_rows,
            metrics=metrics,
            figure_paths=figure_paths,
        ),
        encoding="utf-8",
    )


# Run V2 Experiment 4: Model Comparison.
def run_v2_model_comparison(paths: V2Paths) -> None:
    paths.model_dir.mkdir(parents=True, exist_ok=True)

    run_rows, predictions = _run_model_benchmark(paths.dataset_path)
    metrics = _summarize_model_predictions(predictions)
    metrics = _add_model_diagnostics(metrics)
    figure_predictions = predictions.rename(columns={"model": "horizon"})
    figure_metrics = metrics.rename(columns={"model": "horizon"})
    figure_paths = create_v1_evaluation_figures(
        figure_predictions,
        figure_metrics,
        paths.model_figures_dir,
        group_label="model",
    )

    predictions.to_csv(paths.model_predictions_path, index=False)
    metrics.to_csv(paths.model_metrics_path, index=False)
    paths.model_report_path.write_text(
        _build_model_report(
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


# Train one model per traffic history window with fixed horizon t+1.
def _run_window_benchmark(dataset_path: Path) -> tuple[list[dict[str, object]], pd.DataFrame]:
    source = load_traffic_dataset(dataset_path)
    rows = []
    prediction_frames = []

    for window_size in [5, 10, 20, 30]:
        dataset = _build_window_dataset(source, window_size=window_size, horizon=1)
        feature_columns = [column for column in dataset.columns if column.startswith("traffic_load_lag_")]
        train_rows, test_rows = _split_window_rows_by_episode(dataset, test_size=0.2)

        model = fit_linear_regression(train_rows[feature_columns], train_rows["target"])
        predictions = predict_linear_regression(model, test_rows[feature_columns])
        metrics = evaluate_regression(test_rows["target"], predictions)

        rows.append(
            {
                "window": f"window_{window_size}",
                "window_size": window_size,
                "horizon": "t+1",
                "history_features": len(feature_columns),
                "train_rows": len(train_rows),
                "predict_rows": len(test_rows),
                "mae": metrics.mae,
                "rmse": metrics.rmse,
                "r2": metrics.r2,
            }
        )
        prediction_frames.append(
            pd.DataFrame(
                {
                    "window": f"window_{window_size}",
                    "window_size": window_size,
                    "episode_id": test_rows["episode_id"].reset_index(drop=True),
                    "step": test_rows["step"].reset_index(drop=True),
                    "actual": test_rows["target"].reset_index(drop=True),
                    "prediction": predictions,
                }
            )
        )

    return rows, pd.concat(prediction_frames, ignore_index=True)


# Train one model per feature set with fixed horizon t+1.
def _run_feature_benchmark(dataset_path: Path) -> tuple[list[dict[str, object]], pd.DataFrame]:
    rows = []
    prediction_frames = []

    for feature_set_name in ["traffic_only", "traffic_ue", "full_features"]:
        feature_set = FEATURE_SETS[feature_set_name]
        dataset = build_v1_forecast_dataset(
            dataset_path,
            horizon=1,
            feature_set_name=feature_set_name,
        )
        model = fit_linear_regression(dataset.features_train, dataset.target_train)
        predictions = predict_linear_regression(model, dataset.features_test)
        metrics = evaluate_regression(dataset.target_test, predictions)

        rows.append(
            {
                "feature_set": feature_set_name,
                "horizon": "t+1",
                "raw_features": len(feature_set.raw_columns),
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
                    "feature_set": feature_set_name,
                    "episode_id": dataset.test_rows["episode_id"],
                    "step": dataset.test_rows["step"],
                    "actual": dataset.target_test,
                    "prediction": predictions,
                }
            )
        )

    return rows, pd.concat(prediction_frames, ignore_index=True)


# Train supported models with fixed horizon t+1 and full_features.
def _run_model_benchmark(dataset_path: Path) -> tuple[list[dict[str, object]], pd.DataFrame]:
    dataset = build_v1_forecast_dataset(
        dataset_path,
        horizon=1,
        feature_set_name=DEFAULT_FEATURE_SET_NAME,
    )
    model_specs = [
        (
            "linear_regression",
            "least_squares",
            lambda: fit_linear_regression(dataset.features_train, dataset.target_train),
            lambda model: predict_linear_regression(model, dataset.features_test),
        ),
        (
            "random_forest",
            "n_estimators=100, n_jobs=1, random_state=42",
            lambda: fit_random_forest(
                dataset.features_train,
                dataset.target_train,
                n_estimators=100,
                random_state=42,
            ),
            lambda model: predict_random_forest(model, dataset.features_test),
        ),
    ]

    rows = []
    prediction_frames = []

    for model_name, model_config, fit_model, predict_model in model_specs:
        model = fit_model()
        predictions = predict_model(model)
        metrics = evaluate_regression(dataset.target_test, predictions)

        rows.append(
            {
                "model": model_name,
                "model_config": model_config,
                "horizon": "t+1",
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
                    "model": model_name,
                    "episode_id": dataset.test_rows["episode_id"],
                    "step": dataset.test_rows["step"],
                    "actual": dataset.target_test,
                    "prediction": predictions,
                }
            )
        )

    return rows, pd.concat(prediction_frames, ignore_index=True)


# Build traffic_load lag features within each episode.
def _build_window_dataset(source: pd.DataFrame, window_size: int, horizon: int) -> pd.DataFrame:
    ordered = source.sort_values(["episode_id", "step"]).reset_index(drop=True)
    grouped = ordered.groupby("episode_id", sort=False)

    dataset = ordered[["episode_id", "step"]].copy()
    for lag in range(window_size):
        dataset[f"traffic_load_lag_{lag}"] = grouped["traffic_load"].shift(lag)
    dataset["target"] = grouped["traffic_load"].shift(-horizon)

    return dataset.dropna().reset_index(drop=True)


# Split complete episodes so train and test do not share episode ids.
def _split_window_rows_by_episode(
    df: pd.DataFrame,
    test_size: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    episode_ids = pd.Series(df["episode_id"].drop_duplicates().to_list())
    split_index = int(len(episode_ids) * (1.0 - test_size))
    if split_index <= 0 or split_index >= len(episode_ids):
        raise ValueError("test_size creates an empty train or test episode split.")

    train_episodes = set(episode_ids.iloc[:split_index])
    train_rows = df[df["episode_id"].isin(train_episodes)].reset_index(drop=True)
    test_rows = df[~df["episode_id"].isin(train_episodes)].reset_index(drop=True)
    return train_rows, test_rows


# Summarize window prediction output into metric rows.
def _summarize_window_predictions(predictions: pd.DataFrame) -> pd.DataFrame:
    metrics = summarize_predictions(predictions.rename(columns={"window": "horizon"}))
    metrics = metrics.rename(columns={"horizon": "window"})
    window_sizes = predictions[["window", "window_size"]].drop_duplicates()
    return metrics.merge(window_sizes, on="window", how="left")


# Summarize feature-set prediction output into metric rows.
def _summarize_feature_predictions(predictions: pd.DataFrame) -> pd.DataFrame:
    metrics = summarize_predictions(predictions.rename(columns={"feature_set": "horizon"}))
    return metrics.rename(columns={"horizon": "feature_set"})


# Summarize model prediction output into metric rows.
def _summarize_model_predictions(predictions: pd.DataFrame) -> pd.DataFrame:
    metrics = summarize_predictions(predictions.rename(columns={"model": "horizon"}))
    return metrics.rename(columns={"horizon": "model"})


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


# Add V2-specific window comparison fields to the metric table.
def _add_window_diagnostics(metrics: pd.DataFrame) -> pd.DataFrame:
    enriched = metrics.sort_values("window_size").reset_index(drop=True)
    baseline_mae = float(enriched.iloc[0]["mae"])
    baseline_rmse = float(enriched.iloc[0]["rmse"])
    previous_mae = enriched["mae"].shift(1)

    enriched["mae_change_vs_window_5"] = enriched["mae"] - baseline_mae
    enriched["rmse_change_vs_window_5"] = enriched["rmse"] - baseline_rmse
    enriched["mae_change_vs_previous_window"] = enriched["mae"] - previous_mae
    enriched["decision"] = enriched.apply(_classify_window, axis=1)
    return enriched


# Add V2-specific feature-set comparison fields to the metric table.
def _add_feature_diagnostics(metrics: pd.DataFrame) -> pd.DataFrame:
    order = pd.CategoricalDtype(
        categories=["traffic_only", "traffic_ue", "full_features"],
        ordered=True,
    )
    enriched = metrics.copy()
    enriched["feature_set"] = enriched["feature_set"].astype(order)
    enriched = enriched.sort_values("feature_set").reset_index(drop=True)

    baseline_mae = float(enriched.iloc[0]["mae"])
    baseline_rmse = float(enriched.iloc[0]["rmse"])
    baseline_r2 = float(enriched.iloc[0]["r2"])
    previous_mae = enriched["mae"].shift(1)

    enriched["mae_change_vs_traffic_only"] = enriched["mae"] - baseline_mae
    enriched["rmse_change_vs_traffic_only"] = enriched["rmse"] - baseline_rmse
    enriched["r2_gain_vs_traffic_only"] = enriched["r2"] - baseline_r2
    enriched["mae_change_vs_previous_feature_set"] = enriched["mae"] - previous_mae
    enriched["decision"] = enriched.apply(_classify_feature_set, axis=1)
    enriched["feature_set"] = enriched["feature_set"].astype(str)
    return enriched


# Add V2-specific model comparison fields to the metric table.
def _add_model_diagnostics(metrics: pd.DataFrame) -> pd.DataFrame:
    order = pd.CategoricalDtype(
        categories=["linear_regression", "random_forest"],
        ordered=True,
    )
    enriched = metrics.copy()
    enriched["model"] = enriched["model"].astype(order)
    enriched = enriched.sort_values("model").reset_index(drop=True)

    baseline_mae = float(enriched.iloc[0]["mae"])
    baseline_rmse = float(enriched.iloc[0]["rmse"])
    baseline_r2 = float(enriched.iloc[0]["r2"])

    enriched["mae_change_vs_linear_regression"] = enriched["mae"] - baseline_mae
    enriched["rmse_change_vs_linear_regression"] = enriched["rmse"] - baseline_rmse
    enriched["r2_gain_vs_linear_regression"] = enriched["r2"] - baseline_r2
    enriched["decision"] = enriched.apply(_classify_model, axis=1)
    enriched["model"] = enriched["model"].astype(str)
    return enriched


# Classify whether a horizon is suitable for V2 Forecast State integration.
def _classify_horizon(row: pd.Series) -> str:
    if row["r2"] >= 0.9 and row["mae"] <= 0.08:
        return "recommended"
    if row["r2"] >= 0.75 and row["mae"] <= 0.12:
        return "usable"
    return "risky"


# Classify whether a history window adds enough value for V2 integration.
def _classify_window(row: pd.Series) -> str:
    if row["r2"] >= 0.9 and row["mae"] <= 0.04:
        return "recommended"
    if row["r2"] >= 0.88 and row["mae"] <= 0.045:
        return "usable"
    return "risky"


# Classify whether a feature set adds enough value for V2 integration.
def _classify_feature_set(row: pd.Series) -> str:
    if row["r2"] >= 0.9 and row["mae"] <= 0.04:
        return "recommended"
    if row["r2"] >= 0.88 and row["mae"] <= 0.045:
        return "usable"
    return "risky"


# Classify whether a model is suitable for V2 integration.
def _classify_model(row: pd.Series) -> str:
    if row["r2"] >= 0.9 and row["mae"] <= 0.04:
        return "recommended"
    if row["r2"] >= 0.88 and row["mae"] <= 0.045:
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
            "- Có thể chuyển sang V2 Experiment 2 - History Window Analysis.",
        ]
    )

    return "\n".join(lines) + "\n"


# Build the V2 Window Analysis report in Vietnamese.
def _build_window_report(
    paths: V2Paths,
    run_rows: list[dict[str, object]],
    metrics: pd.DataFrame,
    figure_paths: list[Path],
) -> str:
    best_row = metrics.sort_values(["mae", "rmse"], ascending=True).iloc[0]
    recommended = metrics[metrics["decision"] == "recommended"]
    compact_choice = recommended.iloc[0] if not recommended.empty else best_row

    lines = [
        "# V2 Experiment 2 - History Window Analysis",
        "",
        "Mục tiêu của thí nghiệm này là đánh giá bao nhiêu bước lịch sử traffic là đủ cho dự báo.",
        "",
        "## Cấu Hình Cố Định",
        "",
        "- Model: `linear_regression`",
        "- Target horizon: `t+1`",
        "- Feature: `traffic_load` history trong cùng episode",
        "- Window được hiểu là `lag_0` đến `lag_n`, trong đó `lag_0` là traffic hiện tại.",
        "- Train/test split: 80/20 theo `episode_id`",
        "- Window so sánh: `5`, `10`, `20`, `30`",
        "",
        "## Kết Quả Train/Predict",
        "",
        "| Window | Horizon | History feature | Dòng train | Dòng predict | MAE | RMSE | R² |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]

    for row in run_rows:
        lines.append(
            "| "
            f"`{row['window']}` | "
            f"{row['horizon']} | "
            f"{row['history_features']} | "
            f"{row['train_rows']:,} | "
            f"{row['predict_rows']:,} | "
            f"{row['mae']:.6f} | "
            f"{row['rmse']:.6f} | "
            f"{row['r2']:.6f} |"
        )

    lines.extend(
        [
            "",
            "## Window Diagnostics",
            "",
            "| Window | MAE | RMSE | R² | MAE đổi so với window 5 | RMSE đổi so với window 5 | MAE đổi so với window trước | Quyết định |",
            "|---|---:|---:|---:|---:|---:|---:|---|",
        ]
    )

    for row in metrics.itertuples(index=False):
        previous_delta = (
            "n/a"
            if pd.isna(row.mae_change_vs_previous_window)
            else f"{row.mae_change_vs_previous_window:.6f}"
        )
        lines.append(
            "| "
            f"`{row.window}` | "
            f"{row.mae:.6f} | "
            f"{row.rmse:.6f} | "
            f"{row.r2:.6f} | "
            f"{row.mae_change_vs_window_5:.6f} | "
            f"{row.rmse_change_vs_window_5:.6f} | "
            f"{previous_delta} | "
            f"`{row.decision}` |"
        )

    lines.extend(
        [
            "",
            "## Nhận Định",
            "",
            f"- Window tốt nhất theo MAE/RMSE là `{best_row.window}`.",
            f"- Window gọn nhất đạt mức recommended là `{compact_choice.window}`.",
            "- Nếu window dài hơn không giảm sai số rõ rệt, V2 nên dùng window ngắn hơn để giữ Forecast State nhỏ và dễ tích hợp.",
            "",
            "Figure đã tạo:",
            "",
            *[f"- `{path.relative_to(paths.root)}`" for path in figure_paths],
            "",
            "## Artifact",
            "",
            f"- Report: `{paths.window_report_path.relative_to(paths.root)}`",
            f"- Metric CSV: `{paths.window_metrics_path.relative_to(paths.root)}`",
            f"- Prediction CSV: `{paths.window_predictions_path.relative_to(paths.root)}`",
            f"- Figure: `{paths.window_figures_dir.relative_to(paths.root)}/`",
            "",
            "## Kết Luận",
            "",
            f"- History Window được đề xuất cho V2 hiện tại: `{compact_choice.window}`.",
            "- Có thể chuyển sang V2 Experiment 3 - Feature Contribution Analysis.",
        ]
    )

    return "\n".join(lines) + "\n"


# Build the V2 Feature Contribution Analysis report in Vietnamese.
def _build_feature_report(
    paths: V2Paths,
    run_rows: list[dict[str, object]],
    metrics: pd.DataFrame,
    figure_paths: list[Path],
) -> str:
    best_row = metrics.sort_values(["mae", "rmse"], ascending=True).iloc[0]
    recommended = metrics[metrics["decision"] == "recommended"]
    compact_choice = recommended.iloc[0] if not recommended.empty else best_row

    lines = [
        "# V2 Experiment 3 - Feature Contribution Analysis",
        "",
        "Mục tiêu của thí nghiệm này là đánh giá thông tin ngoài traffic hiện tại có giúp cải thiện dự báo hay không.",
        "",
        "## Cấu Hình Cố Định",
        "",
        "- Model: `linear_regression`",
        "- Target horizon: `t+1`",
        "- Train/test split: 80/20 theo `episode_id`",
        "- Feature set so sánh: `traffic_only`, `traffic_ue`, `full_features`",
        "",
        "## Feature Set",
        "",
        "| Feature set | Raw feature | Mô tả |",
        "|---|---|---|",
    ]

    for feature_set_name in ["traffic_only", "traffic_ue", "full_features"]:
        feature_set = FEATURE_SETS[feature_set_name]
        raw_columns = ", ".join(f"`{column}`" for column in feature_set.raw_columns)
        lines.append(
            "| "
            f"`{feature_set.name}` | "
            f"{raw_columns} | "
            f"{feature_set.description} |"
        )

    lines.extend(
        [
            "",
            "## Kết Quả Train/Predict",
            "",
            "| Feature set | Horizon | Raw feature | Encoded feature | Dòng train | Dòng predict | MAE | RMSE | R² |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )

    for row in run_rows:
        lines.append(
            "| "
            f"`{row['feature_set']}` | "
            f"{row['horizon']} | "
            f"{row['raw_features']} | "
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
            "## Feature Diagnostics",
            "",
            "| Feature set | MAE | RMSE | R² | MAE đổi so với traffic_only | RMSE đổi so với traffic_only | R² tăng so với traffic_only | MAE đổi so với set trước | Quyết định |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )

    for row in metrics.itertuples(index=False):
        previous_delta = (
            "n/a"
            if pd.isna(row.mae_change_vs_previous_feature_set)
            else f"{row.mae_change_vs_previous_feature_set:.6f}"
        )
        lines.append(
            "| "
            f"`{row.feature_set}` | "
            f"{row.mae:.6f} | "
            f"{row.rmse:.6f} | "
            f"{row.r2:.6f} | "
            f"{row.mae_change_vs_traffic_only:.6f} | "
            f"{row.rmse_change_vs_traffic_only:.6f} | "
            f"{row.r2_gain_vs_traffic_only:.6f} | "
            f"{previous_delta} | "
            f"`{row.decision}` |"
        )

    lines.extend(
        [
            "",
            "## Nhận Định",
            "",
            f"- Feature set tốt nhất theo MAE/RMSE là `{best_row.feature_set}`.",
            f"- Feature set gọn nhất đạt mức recommended là `{compact_choice.feature_set}`.",
            "- Nếu feature ngoài traffic hiện tại không giảm sai số rõ rệt, V2 nên ưu tiên feature set nhỏ để giữ Forecast State đơn giản.",
            "",
            "Figure đã tạo:",
            "",
            *[f"- `{path.relative_to(paths.root)}`" for path in figure_paths],
            "",
            "## Artifact",
            "",
            f"- Report: `{paths.feature_report_path.relative_to(paths.root)}`",
            f"- Metric CSV: `{paths.feature_metrics_path.relative_to(paths.root)}`",
            f"- Prediction CSV: `{paths.feature_predictions_path.relative_to(paths.root)}`",
            f"- Figure: `{paths.feature_figures_dir.relative_to(paths.root)}/`",
            "",
            "## Kết Luận",
            "",
            f"- Feature set được đề xuất cho V2 hiện tại: `{compact_choice.feature_set}`.",
            "- Có thể chuyển sang V2 Experiment 4 - Model Comparison.",
        ]
    )

    return "\n".join(lines) + "\n"


# Build the V2 Model Comparison report in Vietnamese.
def _build_model_report(
    paths: V2Paths,
    run_rows: list[dict[str, object]],
    metrics: pd.DataFrame,
    figure_paths: list[Path],
) -> str:
    best_row = metrics.sort_values(["mae", "rmse"], ascending=True).iloc[0]

    lines = [
        "# V2 Experiment 4 - Model Comparison",
        "",
        "Mục tiêu của thí nghiệm này là so sánh Linear Regression với Random Forest trên cùng cấu hình forecast.",
        "",
        "## Cấu Hình Cố Định",
        "",
        "- Target horizon: `t+1`",
        f"- Feature set: `{DEFAULT_FEATURE_SET_NAME}`",
        "- Train/test split: 80/20 theo `episode_id`",
        "- Random Forest: `n_estimators=100`, `n_jobs=1`, `random_state=42`",
        "",
        "## Kết Quả Train/Predict",
        "",
        "| Model | Config | Horizon | Feature set | Encoded feature | Dòng train | Dòng predict | MAE | RMSE | R² |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]

    for row in run_rows:
        lines.append(
            "| "
            f"`{row['model']}` | "
            f"`{row['model_config']}` | "
            f"{row['horizon']} | "
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
            "## Model Diagnostics",
            "",
            "| Model | MAE | RMSE | R² | MAE đổi so với Linear Regression | RMSE đổi so với Linear Regression | R² tăng so với Linear Regression | Quyết định |",
            "|---|---:|---:|---:|---:|---:|---:|---|",
        ]
    )

    for row in metrics.itertuples(index=False):
        lines.append(
            "| "
            f"`{row.model}` | "
            f"{row.mae:.6f} | "
            f"{row.rmse:.6f} | "
            f"{row.r2:.6f} | "
            f"{row.mae_change_vs_linear_regression:.6f} | "
            f"{row.rmse_change_vs_linear_regression:.6f} | "
            f"{row.r2_gain_vs_linear_regression:.6f} | "
            f"`{row.decision}` |"
        )

    lines.extend(
        [
            "",
            "## Nhận Định",
            "",
            f"- Model tốt nhất theo MAE/RMSE là `{best_row.model}`.",
            "- Random Forest được giới hạn 100 cây và chạy một worker để phù hợp máy cá nhân.",
            "- Nếu Random Forest không cải thiện rõ rệt, Linear Regression vẫn là lựa chọn dễ giải thích và nhẹ hơn cho V2.",
            "",
            "Figure đã tạo:",
            "",
            *[f"- `{path.relative_to(paths.root)}`" for path in figure_paths],
            "",
            "## Artifact",
            "",
            f"- Report: `{paths.model_report_path.relative_to(paths.root)}`",
            f"- Metric CSV: `{paths.model_metrics_path.relative_to(paths.root)}`",
            f"- Prediction CSV: `{paths.model_predictions_path.relative_to(paths.root)}`",
            f"- Figure: `{paths.model_figures_dir.relative_to(paths.root)}/`",
            "",
            "## Kết Luận V2",
            "",
            f"- Model được đề xuất cho V2 hiện tại: `{best_row.model}`.",
            "- V2 Forecast Benchmark đã hoàn tất các experiment chính trong roadmap.",
        ]
    )

    return "\n".join(lines) + "\n"
