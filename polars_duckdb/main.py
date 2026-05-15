#!/usr/bin/env python3
"""Linear regression — Polars + DuckDB rewrite (no sklearn)."""

import argparse
import yaml
import logging
import numpy as np
import polars as pl
from pathlib import Path

from core import fit_regression, plot_regression_results

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_config(config_path: Path = None) -> dict:
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Linear regression — Polars + DuckDB")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--data-path", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    feature_cols = config["model"]["feature_columns"]
    target_col   = config["model"]["target_column"]
    output_dir   = Path(args.output_dir) if args.output_dir else Path(config["output"]["figures_dir"])
    output_dir.mkdir(exist_ok=True)

    if args.data_path and args.data_path.exists():
        df = pl.read_csv(args.data_path)
    elif config["data"]["generate_synthetic"]:
        rng = np.random.default_rng(config["data"]["seed"])
        n = config["data"]["n_samples"]
        f1 = rng.normal(50, 15, n)
        f2 = rng.normal(30, 10, n)
        target = 2 * f1 + 1.5 * f2 + rng.normal(0, 5, n)
        df = pl.DataFrame({
            feature_cols[0]: f1.tolist(),
            feature_cols[1]: f2.tolist(),
            target_col:      target.tolist(),
        })
    else:
        raise ValueError("No data source specified")

    coefs, intercept, metrics = fit_regression(df, feature_cols, target_col)

    logging.info("Regression Metrics:")
    logging.info(f"  R²   : {metrics['r2']:.4f}")
    logging.info(f"  RMSE : {metrics['rmse']:.4f}")
    logging.info(f"  MAE  : {metrics['mae']:.4f}")
    logging.info(f"  Coefficients : {[round(c, 4) for c in metrics['coefficients']]}")
    logging.info(f"  Intercept    : {metrics['intercept']:.4f}")

    plot_regression_results(
        df, feature_cols, target_col, coefs, intercept,
        "Linear Regression: Actual vs Predicted",
        output_dir / "regression_results.png",
    )

    logging.info(f"Analysis complete. Figures saved to {output_dir}")


if __name__ == "__main__":
    main()
