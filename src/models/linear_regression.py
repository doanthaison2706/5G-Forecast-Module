from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class LinearRegressionBaseline:
    coefficients: np.ndarray
    intercept: float
    feature_columns: list[str]


@dataclass(frozen=True)
class RegressionMetrics:
    mae: float
    rmse: float
    r2: float


# Train a Linear Regression model with least squares.
def fit_linear_regression(
    features: pd.DataFrame,
    target: pd.Series,
) -> LinearRegressionBaseline:
    x = features.to_numpy(dtype=float)
    y = target.to_numpy(dtype=float)
    design_matrix = np.column_stack([np.ones(len(x)), x])
    solution, *_ = np.linalg.lstsq(design_matrix, y, rcond=None)

    return LinearRegressionBaseline(
        coefficients=solution[1:],
        intercept=float(solution[0]),
        feature_columns=list(features.columns),
    )


# Predict target values from a trained Linear Regression baseline.
def predict_linear_regression(
    model: LinearRegressionBaseline,
    features: pd.DataFrame,
) -> np.ndarray:
    aligned = features.reindex(columns=model.feature_columns, fill_value=0.0)
    return aligned.to_numpy(dtype=float) @ model.coefficients + model.intercept


# Evaluate predictions with MAE, RMSE, and R2.
def evaluate_regression(
    target: pd.Series | np.ndarray,
    predictions: np.ndarray,
) -> RegressionMetrics:
    y_true = np.asarray(target, dtype=float)
    y_pred = np.asarray(predictions, dtype=float)
    errors = y_true - y_pred
    mae = float(np.mean(np.abs(errors)))
    rmse = float(np.sqrt(np.mean(errors**2)))
    total_sum_squares = float(np.sum((y_true - np.mean(y_true)) ** 2))
    residual_sum_squares = float(np.sum(errors**2))
    r2 = 1.0 - residual_sum_squares / total_sum_squares

    return RegressionMetrics(mae=mae, rmse=rmse, r2=float(r2))
