from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


# Create all V0 exploratory figures.
def create_v0_figures(df: pd.DataFrame, output_dir: str | Path) -> None:
    figures_dir = Path(output_dir)
    figures_dir.mkdir(parents=True, exist_ok=True)

    _plot_traffic_distribution(df, figures_dir / "traffic_load_distribution.png")
    _plot_sample_episode(df, figures_dir / "sample_episode_timeseries.png")
    _plot_traffic_by_event(df, figures_dir / "traffic_load_by_mobility_event.png")


# Plot the distribution of current traffic load.
def _plot_traffic_distribution(df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["traffic_load"], bins=40, color="#2f6f6d", edgecolor="white")
    ax.set_title("Traffic Load Distribution")
    ax.set_xlabel("traffic_load")
    ax.set_ylabel("count")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


# Plot one sample episode as a traffic time series.
def _plot_sample_episode(df: pd.DataFrame, output_path: Path) -> None:
    first_episode = df["episode_id"].min()
    sample = df[df["episode_id"] == first_episode]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sample["step"], sample["traffic_load"], color="#1f4e79", linewidth=1.7)
    ax.set_title(f"Traffic Load Over Time - Episode {first_episode}")
    ax.set_xlabel("step")
    ax.set_ylabel("traffic_load")
    ax.set_ylim(0, 1.05)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


# Plot traffic load grouped by mobility event.
def _plot_traffic_by_event(df: pd.DataFrame, output_path: Path) -> None:
    grouped = [
        group["traffic_load"].to_numpy()
        for _, group in df.groupby("mobility_event", sort=True)
    ]
    labels = sorted(df["mobility_event"].unique())

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(grouped, labels=labels, patch_artist=True)
    ax.set_title("Traffic Load by Mobility Event")
    ax.set_xlabel("mobility_event")
    ax.set_ylabel("traffic_load")
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
