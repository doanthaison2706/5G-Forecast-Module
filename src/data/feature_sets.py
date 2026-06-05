from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureSet:
    name: str
    description: str
    raw_columns: list[str]


FEATURE_SETS = {
    "traffic_only": FeatureSet(
        name="traffic_only",
        description="Chỉ dùng traffic hiện tại làm baseline autoregressive tối thiểu.",
        raw_columns=["traffic_load"],
    ),
    "traffic_ue": FeatureSet(
        name="traffic_ue",
        description="Thêm UE count để kiểm tra mật độ người dùng có cải thiện dự báo không.",
        raw_columns=["traffic_load", "ue_count"],
    ),
    "full_features": FeatureSet(
        name="full_features",
        description="Dùng toàn bộ feature baseline V1 có sẵn trước bước train model.",
        raw_columns=[
            "traffic_load",
            "ue_count",
            "traffic_demand_bps",
            "mobility_event",
            "time_ratio",
        ],
    ),
}

DEFAULT_FEATURE_SET_NAME = "full_features"


# Return one feature set by name with a clear error for unsupported names.
def get_feature_set(name: str) -> FeatureSet:
    if name not in FEATURE_SETS:
        supported = ", ".join(FEATURE_SETS)
        raise ValueError(f"Unsupported feature set '{name}'. Supported sets: {supported}")
    return FEATURE_SETS[name]


# Return the ordered raw columns for one feature set.
def get_feature_columns(name: str) -> list[str]:
    return list(get_feature_set(name).raw_columns)
