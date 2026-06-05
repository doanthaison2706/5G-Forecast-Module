from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "episode_id",
    "step",
    "traffic_load",
    "ue_count",
    "traffic_demand_bps",
    "mobility_event",
    "time_ratio",
    "traffic_load_t_plus_1",
    "traffic_load_t_plus_5",
    "traffic_load_t_plus_10",
]


def load_traffic_dataset(path: str | Path) -> pd.DataFrame:
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    df = pd.read_csv(dataset_path)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {missing_columns}")

    return df
