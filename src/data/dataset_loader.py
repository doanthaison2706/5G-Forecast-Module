from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.data.feature_sets import DEFAULT_FEATURE_SET_NAME, get_feature_columns


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

DEFAULT_FEATURE_COLUMNS = get_feature_columns(DEFAULT_FEATURE_SET_NAME)

TARGET_COLUMNS = {
    1: "traffic_load_t_plus_1",
    5: "traffic_load_t_plus_5",
    10: "traffic_load_t_plus_10",
}


@dataclass(frozen=True)
class V1ForecastDataset:
    features_train: pd.DataFrame
    features_test: pd.DataFrame
    target_train: pd.Series
    target_test: pd.Series
    train_rows: pd.DataFrame
    test_rows: pd.DataFrame
    feature_columns: list[str]
    target_column: str
    horizon: int


# Load traffic dataset from CSV and verify the base simulator columns.
def load_traffic_dataset(path: str | Path) -> pd.DataFrame:
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    df = pd.read_csv(dataset_path)
    _ensure_columns(df, REQUIRED_COLUMNS)

    return df


# Build the V1 train/test dataset for one forecast horizon.
def build_v1_forecast_dataset(
    data: str | Path | pd.DataFrame,
    horizon: int = 1,
    feature_columns: list[str] | None = None,
    feature_set_name: str | None = None,
    test_size: float = 0.2,
    split_by_episode: bool = True,
) -> V1ForecastDataset:
    df = load_traffic_dataset(data) if isinstance(data, (str, Path)) else data.copy()
    _ensure_columns(df, REQUIRED_COLUMNS)

    target_column = _target_column_for_horizon(horizon)
    selected_features = _resolve_feature_columns(feature_columns, feature_set_name)
    _ensure_columns(df, [*selected_features, target_column])

    ordered = df.sort_values(["episode_id", "step"]).reset_index(drop=True)
    train_rows, test_rows = _split_rows(ordered, test_size, split_by_episode)

    features_train = _build_feature_frame(train_rows, selected_features)
    features_test = _build_feature_frame(test_rows, selected_features)
    features_test = features_test.reindex(columns=features_train.columns, fill_value=0)

    return V1ForecastDataset(
        features_train=features_train,
        features_test=features_test,
        target_train=train_rows[target_column].reset_index(drop=True),
        target_test=test_rows[target_column].reset_index(drop=True),
        train_rows=train_rows.reset_index(drop=True),
        test_rows=test_rows.reset_index(drop=True),
        feature_columns=list(features_train.columns),
        target_column=target_column,
        horizon=horizon,
    )


# Build V1 train/test datasets for every supported forecast horizon.
def build_v1_forecast_datasets(
    data: str | Path | pd.DataFrame,
    horizons: list[int] | None = None,
    feature_columns: list[str] | None = None,
    feature_set_name: str | None = None,
    test_size: float = 0.2,
    split_by_episode: bool = True,
) -> dict[int, V1ForecastDataset]:
    selected_horizons = horizons or list(TARGET_COLUMNS)
    return {
        horizon: build_v1_forecast_dataset(
            data=data,
            horizon=horizon,
            feature_columns=feature_columns,
            feature_set_name=feature_set_name,
            test_size=test_size,
            split_by_episode=split_by_episode,
        )
        for horizon in selected_horizons
    }


# Validate that all required columns are present before modeling.
def _ensure_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {missing_columns}")


# Resolve explicit feature columns or a named feature set for dataset building.
def _resolve_feature_columns(
    feature_columns: list[str] | None,
    feature_set_name: str | None,
) -> list[str]:
    if feature_columns is not None and feature_set_name is not None:
        raise ValueError("Use either feature_columns or feature_set_name, not both.")
    if feature_columns is not None:
        return list(feature_columns)
    if feature_set_name is not None:
        return get_feature_columns(feature_set_name)
    return list(DEFAULT_FEATURE_COLUMNS)


# Resolve the target column name from a numeric forecast horizon.
def _target_column_for_horizon(horizon: int) -> str:
    if horizon not in TARGET_COLUMNS:
        supported = ", ".join(str(value) for value in TARGET_COLUMNS)
        raise ValueError(f"Unsupported horizon {horizon}. Supported horizons: {supported}")
    return TARGET_COLUMNS[horizon]


# Split rows for V1 using episode-based split by default.
def _split_rows(
    df: pd.DataFrame,
    test_size: float,
    split_by_episode: bool,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not 0.0 < test_size < 1.0:
        raise ValueError("test_size must be between 0 and 1.")

    if split_by_episode:
        return _split_rows_by_episode(df, test_size)
    return _split_rows_by_order(df, test_size)


# Split complete episodes so train and test do not share episode ids.
def _split_rows_by_episode(
    df: pd.DataFrame,
    test_size: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    episode_ids = pd.Series(df["episode_id"].drop_duplicates().to_list())
    split_index = int(len(episode_ids) * (1.0 - test_size))
    if split_index <= 0 or split_index >= len(episode_ids):
        raise ValueError("test_size creates an empty train or test episode split.")

    train_episodes = set(episode_ids.iloc[:split_index])
    train_rows = df[df["episode_id"].isin(train_episodes)]
    test_rows = df[~df["episode_id"].isin(train_episodes)]
    return train_rows, test_rows


# Split rows by sorted row order when episode isolation is not requested.
def _split_rows_by_order(
    df: pd.DataFrame,
    test_size: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    split_index = int(len(df) * (1.0 - test_size))
    if split_index <= 0 or split_index >= len(df):
        raise ValueError("test_size creates an empty train or test row split.")
    return df.iloc[:split_index], df.iloc[split_index:]


# Convert selected raw feature columns into numeric modeling columns.
def _build_feature_frame(
    rows: pd.DataFrame,
    feature_columns: list[str],
) -> pd.DataFrame:
    features = rows[feature_columns].reset_index(drop=True)
    categorical_columns = [
        column for column in ["mobility_event"] if column in features.columns
    ]
    encoded = pd.get_dummies(features, columns=categorical_columns, dtype=float)
    return encoded.astype(float)
