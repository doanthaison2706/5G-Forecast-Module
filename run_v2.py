from pathlib import Path

from src.v2_pipeline import build_v2_paths, run_v2_horizon_analysis


ROOT = Path(__file__).resolve().parent


# Run V2 Experiment 1 and write Horizon Analysis artifacts.
def main() -> None:
    paths = build_v2_paths(ROOT)
    run_v2_horizon_analysis(paths)

    print(f"V2 Horizon Analysis report: {paths.report_path.relative_to(ROOT)}")
    print(f"V2 Horizon Analysis metrics: {paths.metrics_path.relative_to(ROOT)}")
    print(f"V2 Horizon Analysis predictions: {paths.predictions_path.relative_to(ROOT)}")
    print(f"V2 Horizon Analysis figures: {paths.figures_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
