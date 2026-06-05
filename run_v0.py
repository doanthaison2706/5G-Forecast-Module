from pathlib import Path

from src.data.dataset_loader import load_traffic_dataset
from src.data.validation import (
    clean_dataset,
    validate_dataset,
    write_dataset_summary,
    write_validation_report,
)
from src.visualization import create_v0_figures


ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "data" / "raw" / "traffic_dataset.csv"
PROCESSED_DATASET_PATH = ROOT / "data" / "processed" / "traffic_dataset_v0_clean.csv"
RESULTS_DIR = ROOT / "results" / "v0"


def main() -> None:
    df = load_traffic_dataset(DATASET_PATH)
    cleaned = clean_dataset(df)

    PROCESSED_DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(PROCESSED_DATASET_PATH, index=False)

    results = validate_dataset(cleaned)
    write_dataset_summary(cleaned, RESULTS_DIR / "dataset_summary.csv")
    write_validation_report(cleaned, results, RESULTS_DIR / "validation_report.md")
    create_v0_figures(cleaned, RESULTS_DIR / "figures")

    passed = sum(result.passed for result in results)
    total = len(results)
    status = "PASS" if passed == total else "FAIL"
    print(f"V0 validation status: {status} ({passed}/{total} checks passed)")
    print(f"Clean dataset: {PROCESSED_DATASET_PATH.relative_to(ROOT)}")
    print(f"Result summary: {(RESULTS_DIR / 'README.md').relative_to(ROOT)}")
    print(f"Report: {(RESULTS_DIR / 'validation_report.md').relative_to(ROOT)}")
    print(f"Figures: {(RESULTS_DIR / 'figures').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
