from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm


def correlation_summary(df: pd.DataFrame, exposure: str, outcome: str) -> dict:
    clean = df[[exposure, outcome]].dropna()
    if len(clean) < 3:
        raise ValueError("At least three complete rows are required for correlation")
    pearson_r, pearson_p = stats.pearsonr(clean[exposure], clean[outcome])
    spearman_r, spearman_p = stats.spearmanr(clean[exposure], clean[outcome])
    return {
        "n": int(len(clean)),
        "pearson_r": float(pearson_r),
        "pearson_p": float(pearson_p),
        "spearman_rho": float(spearman_r),
        "spearman_p": float(spearman_p),
    }


def controlled_association(
    df: pd.DataFrame,
    exposure: str,
    outcome: str,
    controls: list[str],
    fixed_effects: list[str] | None = None,
) -> dict:
    fixed_effects = fixed_effects or []
    columns = [outcome, exposure, *controls, *fixed_effects]
    clean = df[columns].dropna().copy()
    if len(clean) < 10:
        raise ValueError("Controlled model requires at least ten complete rows")

    X = clean[[exposure, *controls]].copy()
    for col in fixed_effects:
        dummies = pd.get_dummies(clean[col].astype(str), prefix=col, drop_first=True, dtype=float)
        X = pd.concat([X, dummies], axis=1)

    X = sm.add_constant(X.astype(float), has_constant="add")
    y = clean[outcome].astype(float)
    model = sm.OLS(y, X).fit(cov_type="HC3")
    ci_low, ci_high = model.conf_int().loc[exposure]
    return {
        "n": int(model.nobs),
        "exposure_coefficient": float(model.params[exposure]),
        "robust_se": float(model.bse[exposure]),
        "p_value": float(model.pvalues[exposure]),
        "ci_95": [float(ci_low), float(ci_high)],
        "r_squared": float(model.rsquared),
        "controls": controls,
        "fixed_effects": fixed_effects,
    }


def lagged_correlations(
    df: pd.DataFrame,
    unit_column: str,
    time_column: str,
    exposure: str,
    outcome: str,
    lags: list[int],
) -> dict[str, float | None]:
    ordered = df.sort_values([unit_column, time_column]).copy()
    results: dict[str, float | None] = {}
    for lag in lags:
        shifted = ordered.groupby(unit_column)[outcome].shift(-lag)
        pair = pd.DataFrame({"x": ordered[exposure], "y": shifted}).dropna()
        if len(pair) < 3 or pair["x"].std() == 0 or pair["y"].std() == 0:
            results[str(lag)] = None
        else:
            results[str(lag)] = float(np.corrcoef(pair["x"], pair["y"])[0, 1])
    return results
