from pathlib import Path

from src.v1_pipeline import build_v1_paths, run_v1_pipeline


ROOT = Path(__file__).resolve().parent


# Run the consolidated V1 pipeline and write the M5 results report.
def main() -> None:
    paths = build_v1_paths(ROOT)
    run_v1_pipeline(paths)

    print(f"V1 report: {paths.report_path.relative_to(ROOT)}")
    print(f"V1 metrics: {paths.metrics_path.relative_to(ROOT)}")
    print(f"V1 predictions: {paths.predictions_path.relative_to(ROOT)}")
    print(f"V1 figures: {paths.figures_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
