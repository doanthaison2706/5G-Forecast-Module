from pathlib import Path

from src.v2_pipeline import (
    build_v2_paths,
    run_v2_feature_analysis,
    run_v2_horizon_analysis,
    run_v2_model_comparison,
    run_v2_window_analysis,
)


ROOT = Path(__file__).resolve().parent


# Run V2 experiments and write Forecast Benchmark artifacts.
def main() -> None:
    paths = build_v2_paths(ROOT)
    run_v2_horizon_analysis(paths)
    run_v2_window_analysis(paths)
    run_v2_feature_analysis(paths)
    run_v2_model_comparison(paths)

    print(f"V2 Horizon Analysis report: {paths.report_path.relative_to(ROOT)}")
    print(f"V2 Horizon Analysis metrics: {paths.metrics_path.relative_to(ROOT)}")
    print(f"V2 Horizon Analysis predictions: {paths.predictions_path.relative_to(ROOT)}")
    print(f"V2 Horizon Analysis figures: {paths.figures_dir.relative_to(ROOT)}")
    print(f"V2 Window Analysis report: {paths.window_report_path.relative_to(ROOT)}")
    print(f"V2 Window Analysis metrics: {paths.window_metrics_path.relative_to(ROOT)}")
    print(f"V2 Window Analysis predictions: {paths.window_predictions_path.relative_to(ROOT)}")
    print(f"V2 Window Analysis figures: {paths.window_figures_dir.relative_to(ROOT)}")
    print(f"V2 Feature Analysis report: {paths.feature_report_path.relative_to(ROOT)}")
    print(f"V2 Feature Analysis metrics: {paths.feature_metrics_path.relative_to(ROOT)}")
    print(f"V2 Feature Analysis predictions: {paths.feature_predictions_path.relative_to(ROOT)}")
    print(f"V2 Feature Analysis figures: {paths.feature_figures_dir.relative_to(ROOT)}")
    print(f"V2 Model Comparison report: {paths.model_report_path.relative_to(ROOT)}")
    print(f"V2 Model Comparison metrics: {paths.model_metrics_path.relative_to(ROOT)}")
    print(f"V2 Model Comparison predictions: {paths.model_predictions_path.relative_to(ROOT)}")
    print(f"V2 Model Comparison figures: {paths.model_figures_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
