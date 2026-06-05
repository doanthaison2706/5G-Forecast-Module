import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/matplotlib")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Summarize prediction output into MAE, RMSE, R2, and residual statistics.
def summarize_predictions(predictions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for horizon, group in predictions.groupby("horizon", sort=False):
        actual = group["actual"].to_numpy(dtype=float)
        predicted = group["prediction"].to_numpy(dtype=float)
        residual = actual - predicted
        total_sum_squares = float(np.sum((actual - np.mean(actual)) ** 2))
        residual_sum_squares = float(np.sum(residual**2))
        rows.append(
            {
                "horizon": horizon,
                "predict_rows": len(group),
                "mae": float(np.mean(np.abs(residual))),
                "rmse": float(np.sqrt(np.mean(residual**2))),
                "r2": float(1.0 - residual_sum_squares / total_sum_squares),
                "residual_mean": float(np.mean(residual)),
                "residual_std": float(np.std(residual)),
            }
        )
    return pd.DataFrame(rows)


# Create all V1 M4 evaluation figures from prediction output and metric summary.
def create_v1_evaluation_figures(
    predictions: pd.DataFrame,
    metrics: pd.DataFrame,
    output_dir: str | Path,
    group_label: str = "horizon",
) -> list[Path]:
    figures_dir = Path(output_dir)
    figures_dir.mkdir(parents=True, exist_ok=True)

    output_paths = [
        figures_dir / f"linear_regression_metrics_by_{group_label}.png",
        figures_dir / "linear_regression_actual_vs_prediction.png",
        figures_dir / "linear_regression_residual_distribution.png",
        figures_dir / "linear_regression_sample_timeseries.png",
    ]

    _plot_metrics_by_horizon(metrics, output_paths[0], group_label)
    _plot_actual_vs_prediction(predictions, output_paths[1])
    _plot_residual_distribution(predictions, output_paths[2])
    _plot_sample_timeseries(predictions, output_paths[3])

    return output_paths


# Plot MAE, RMSE, and R2 by forecast horizon.
def _plot_metrics_by_horizon(
    metrics: pd.DataFrame,
    output_path: Path,
    group_label: str,
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    colors = ["#2f6f6d", "#6f4e7c", "#a95d40"]
    metric_specs = [
        ("mae", "MAE"),
        ("rmse", "RMSE"),
        ("r2", "R²"),
    ]

    for ax, (column, label), color in zip(axes, metric_specs, colors):
        ax.bar(metrics["horizon"], metrics[column], color=color)
        ax.set_title(label)
        ax.set_xlabel(group_label)
        ax.grid(axis="y", alpha=0.25)
        if column == "r2":
            ax.set_ylim(0.0, 1.0)

    fig.suptitle(f"Metric theo {group_label}")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


# Plot actual and predicted values for all forecast horizons.
def _plot_actual_vs_prediction(predictions: pd.DataFrame, output_path: Path) -> None:
    horizons = list(predictions["horizon"].drop_duplicates())
    fig, axes = plt.subplots(1, len(horizons), figsize=(14, 4), sharex=True, sharey=True)

    for ax, horizon in zip(axes, horizons):
        group = predictions[predictions["horizon"] == horizon]
        sample = group.sample(n=min(1200, len(group)), random_state=42)
        ax.scatter(sample["actual"], sample["prediction"], s=8, alpha=0.35, color="#2f6f6d")
        ax.plot([0, 1], [0, 1], color="#b33f3f", linewidth=1.2)
        ax.set_title(horizon)
        ax.set_xlabel("actual")
        ax.grid(alpha=0.25)

    axes[0].set_ylabel("prediction")
    fig.suptitle("Actual so với prediction")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


# Plot residual distribution for each forecast horizon.
def _plot_residual_distribution(predictions: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    for horizon, group in predictions.groupby("horizon", sort=False):
        residual = group["actual"] - group["prediction"]
        ax.hist(residual, bins=45, alpha=0.45, label=horizon)

    ax.axvline(0, color="#333333", linewidth=1.1)
    ax.set_title("Phân phối residual")
    ax.set_xlabel("actual - prediction")
    ax.set_ylabel("số dòng")
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


# Plot actual and predicted traffic for one sample test episode.
def _plot_sample_timeseries(predictions: pd.DataFrame, output_path: Path) -> None:
    first_episode = int(predictions["episode_id"].min())
    sample = predictions[predictions["episode_id"] == first_episode]
    horizons = list(sample["horizon"].drop_duplicates())

    fig, axes = plt.subplots(len(horizons), 1, figsize=(12, 8), sharex=True, sharey=True)
    for ax, horizon in zip(axes, horizons):
        group = sample[sample["horizon"] == horizon]
        ax.plot(group["step"], group["actual"], label="actual", color="#1f4e79", linewidth=1.4)
        ax.plot(
            group["step"],
            group["prediction"],
            label="prediction",
            color="#b35f3f",
            linewidth=1.2,
            alpha=0.85,
        )
        ax.set_title(horizon)
        ax.set_ylabel("traffic_load")
        ax.set_ylim(0, 1.05)
        ax.grid(alpha=0.25)

    axes[-1].set_xlabel("step")
    axes[0].legend(loc="upper right")
    fig.suptitle(f"Actual và prediction theo thời gian - episode {first_episode}")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
