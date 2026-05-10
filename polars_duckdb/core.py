"""Linear regression using Polars and DuckDB.

For univariate regression: DuckDB REGR_SLOPE / REGR_INTERCEPT / REGR_R2 replace sklearn entirely.
For multiple regression: numpy lstsq fits the model; DuckDB computes all evaluation metrics.
sklearn.linear_model and sklearn.metrics are not imported.
"""

import duckdb
import polars as pl
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Tuple


def fit_regression(
    df: pl.DataFrame,
    feature_cols: List[str],
    target_col: str,
) -> Tuple[np.ndarray, float, Dict]:
    """
    Fit linear regression and score it.

    Single feature  → DuckDB REGR_* functions (no numpy needed).
    Multiple features → numpy lstsq for coefficients; DuckDB for all metrics.

    Returns (coefficients, intercept, metrics_dict).
    """
    if len(feature_cols) == 1:
        x_col = feature_cols[0]
        params = duckdb.sql(f"""
            SELECT
                REGR_SLOPE("{target_col}", "{x_col}")     AS slope,
                REGR_INTERCEPT("{target_col}", "{x_col}") AS intercept,
                REGR_R2("{target_col}", "{x_col}")        AS r2
            FROM df
        """).pl().row(0, named=True)
        coefficients = np.array([params["slope"]])
        intercept    = params["intercept"]
    else:
        X = df.select(feature_cols).to_numpy()
        y = df[target_col].to_numpy()
        X_aug = np.column_stack([X, np.ones(len(X))])
        result, *_ = np.linalg.lstsq(X_aug, y, rcond=None)
        coefficients = result[:-1]
        intercept    = float(result[-1])

    # Build predicted column and score entirely in DuckDB
    pred_expr = " + ".join(
        f"{coef} * \"{col}\"" for coef, col in zip(coefficients, feature_cols)
    ) + f" + {intercept}"

    metrics = duckdb.sql(f"""
        WITH preds AS (
            SELECT
                "{target_col}" AS actual,
                {pred_expr}    AS predicted
            FROM df
        )
        SELECT
            REGR_R2(actual, predicted)                     AS r2,
            SQRT(AVG(POWER(actual - predicted, 2)))        AS rmse,
            AVG(ABS(actual - predicted))                   AS mae
        FROM preds
    """).pl().row(0, named=True)

    return coefficients, intercept, {**metrics, "coefficients": coefficients.tolist(), "intercept": intercept}


def plot_regression_results(
    df: pl.DataFrame,
    feature_cols: List[str],
    target_col: str,
    coefficients: np.ndarray,
    intercept: float,
    title: str,
    output_path: Path,
):
    pred_expr = " + ".join(
        f"{coef} * \"{col}\"" for coef, col in zip(coefficients, feature_cols)
    ) + f" + {intercept}"

    result = duckdb.sql(f"""
        SELECT "{target_col}" AS actual, {pred_expr} AS predicted FROM df
    """).pl()

    y_true = result["actual"].to_numpy()
    y_pred = result["predicted"].to_numpy()

    lo, hi = min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())

    if plot:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(y_true, y_pred, alpha=0.6, color="#4A90A4", s=30, edgecolors="none")
        ax.plot([lo, hi], [lo, hi], "r--", linewidth=1.2, label="Perfect Prediction")
        ax.set_xlabel("Actual Values")
        ax.set_ylabel("Predicted Values")
        ax.set_title(title)
        ax.legend(loc="best")
        plt.tight_layout()
        plt.savefig(output_path, dpi=100, bbox_inches="tight")
        plt.close()
