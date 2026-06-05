from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


# Train a small Random Forest regressor for V2 model comparison.
def fit_random_forest(
    features: pd.DataFrame,
    target: pd.Series,
    n_estimators: int = 100,
    random_state: int = 42,
) -> RandomForestRegressor:
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=1,
    )
    model.fit(features.to_numpy(dtype=float), target.to_numpy(dtype=float))
    return model


# Predict target values from a trained Random Forest regressor.
def predict_random_forest(
    model: RandomForestRegressor,
    features: pd.DataFrame,
) -> np.ndarray:
    return model.predict(features.to_numpy(dtype=float))
