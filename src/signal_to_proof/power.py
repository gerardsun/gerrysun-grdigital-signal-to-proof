from __future__ import annotations

import math
import pandas as pd
from statsmodels.stats.power import TTestIndPower


def mde_two_group(
    df: pd.DataFrame,
    outcome: str,
    treatment_column: str,
    post_column: str,
    alpha: float = 0.05,
    power: float = 0.80,
) -> dict:
    post = df[df[post_column] == 1][[outcome, treatment_column]].dropna()
    n_t = int((post[treatment_column] == 1).sum())
    n_c = int((post[treatment_column] == 0).sum())
    if n_t < 2 or n_c < 2:
        return {
            "n_treatment": n_t,
            "n_control": n_c,
            "standardized_mde": None,
            "outcome_unit_mde": None,
            "alpha": alpha,
            "power": power,
        }

    ratio = n_c / n_t
    standardized = TTestIndPower().solve_power(
        effect_size=None,
        nobs1=n_t,
        alpha=alpha,
        power=power,
        ratio=ratio,
        alternative="two-sided",
    )
    outcome_sd = float(post[outcome].std(ddof=1))
    return {
        "n_treatment": n_t,
        "n_control": n_c,
        "standardized_mde": float(standardized),
        "outcome_unit_mde": float(standardized * outcome_sd),
        "alpha": alpha,
        "power": power,
        "outcome_sd": outcome_sd,
    }
