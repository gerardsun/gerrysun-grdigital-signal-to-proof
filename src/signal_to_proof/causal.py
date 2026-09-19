from __future__ import annotations

import pandas as pd
import statsmodels.formula.api as smf


def randomized_prepost_effect(
    df: pd.DataFrame,
    outcome: str,
    treatment_column: str,
    post_column: str,
    unit_column: str,
    time_column: str,
) -> dict:
    clean = df[[outcome, treatment_column, post_column, unit_column, time_column]].dropna().copy()
    clean[treatment_column] = clean[treatment_column].astype(int)
    clean[post_column] = clean[post_column].astype(int)

    formula = (
        f"{outcome} ~ {treatment_column} * {post_column} "
        f"+ C({unit_column}) + C({time_column})"
    )
    model = smf.ols(formula, data=clean).fit(cov_type="HC3")
    interaction = f"{treatment_column}:{post_column}"
    if interaction not in model.params:
        interaction = f"{post_column}:{treatment_column}"
    ci_low, ci_high = model.conf_int().loc[interaction]

    pre = clean[clean[post_column] == 0]
    post = clean[clean[post_column] == 1]
    pre_means = pre.groupby(treatment_column)[outcome].mean().to_dict()
    post_means = post.groupby(treatment_column)[outcome].mean().to_dict()

    return {
        "n": int(model.nobs),
        "effect": float(model.params[interaction]),
        "robust_se": float(model.bse[interaction]),
        "p_value": float(model.pvalues[interaction]),
        "ci_95": [float(ci_low), float(ci_high)],
        "pre_means": {str(k): float(v) for k, v in pre_means.items()},
        "post_means": {str(k): float(v) for k, v in post_means.items()},
        "design": "randomized_prepost",
    }
