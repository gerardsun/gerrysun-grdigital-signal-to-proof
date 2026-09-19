from __future__ import annotations

import math
import numpy as np
import pandas as pd

from .data import required_columns
from .types import GateResult, GateStatus


def _gate(name: str, status: GateStatus, reason: str, **details) -> GateResult:
    return GateResult(name=name, status=status, reason=reason, details=details)


def data_completeness_gate(df: pd.DataFrame, manifest: dict) -> GateResult:
    missing_columns = [c for c in required_columns(manifest) if c not in df.columns]
    if missing_columns:
        return _gate(
            "data_completeness",
            GateStatus.FAIL,
            "Required columns are missing.",
            missing_columns=missing_columns,
        )
    required = required_columns(manifest)
    missing_rate = float(df[required].isna().mean().mean())
    status = GateStatus.PASS if missing_rate <= 0.05 else GateStatus.WARN
    return _gate(
        "data_completeness",
        status,
        "Required columns are present." if status == GateStatus.PASS else "Required columns are present, but missingness is material.",
        average_missing_rate=missing_rate,
        row_count=int(len(df)),
    )


def grain_gate(df: pd.DataFrame, manifest: dict) -> GateResult:
    unit = manifest["dataset"]["unit_column"]
    time = manifest["dataset"]["time_column"]
    if unit not in df or time not in df:
        return _gate("grain", GateStatus.FAIL, "Unit or time key is missing.")
    duplicate_rate = float(df.duplicated([unit, time]).mean())
    if duplicate_rate > 0:
        return _gate(
            "grain",
            GateStatus.FAIL,
            "Rows are not unique at the declared unit-time grain.",
            duplicate_rate=duplicate_rate,
        )
    return _gate(
        "grain",
        GateStatus.PASS,
        "Rows are unique at the declared unit-time grain.",
        units=int(df[unit].nunique()),
        periods=int(df[time].nunique()),
    )


def exposure_variation_gate(df: pd.DataFrame, manifest: dict) -> GateResult:
    exposure = manifest["measurement"]["exposure_column"]
    unit = manifest["dataset"]["unit_column"]
    if exposure not in df:
        return _gate("exposure_variation", GateStatus.FAIL, "Exposure column is missing.")
    total_var = float(df[exposure].var(ddof=1))
    unit_means = df.groupby(unit)[exposure].mean()
    between_var = float(unit_means.var(ddof=1)) if len(unit_means) > 1 else 0.0
    if not math.isfinite(total_var) or total_var <= 1e-10:
        return _gate(
            "exposure_variation",
            GateStatus.FAIL,
            "Exposure does not vary enough to estimate an exposure relationship.",
            total_variance=total_var,
            between_unit_variance=between_var,
        )
    status = GateStatus.PASS if between_var > 1e-6 else GateStatus.WARN
    reason = (
        "Exposure varies across the analytical units."
        if status == GateStatus.PASS
        else "Exposure varies over time but has little between-unit variation; interpretation should remain cautious."
    )
    return _gate(
        "exposure_variation",
        status,
        reason,
        total_variance=total_var,
        between_unit_variance=between_var,
    )


def control_gate(df: pd.DataFrame, manifest: dict) -> GateResult:
    controls = manifest["measurement"].get("controls", [])
    missing = [c for c in controls if c not in df]
    if missing:
        return _gate("controls", GateStatus.FAIL, "Declared controls are missing.", missing_controls=missing)
    if not controls:
        return _gate("controls", GateStatus.WARN, "No controls were declared.", control_count=0)
    return _gate("controls", GateStatus.PASS, "Declared controls are available.", control_count=len(controls))


def selection_risk_gate(df: pd.DataFrame, manifest: dict) -> GateResult:
    baseline = manifest["measurement"].get("baseline_intent_column")
    exposure = manifest["measurement"]["exposure_column"]
    if not baseline:
        return _gate(
            "selection_risk",
            GateStatus.WARN,
            "No baseline-intent proxy was declared, so self-selection cannot be screened in this public diagnostic.",
        )
    if baseline not in df or exposure not in df:
        return _gate("selection_risk", GateStatus.FAIL, "Selection diagnostic columns are missing.")
    pair = df[[baseline, exposure]].dropna()
    if len(pair) < 3 or pair[baseline].std() == 0 or pair[exposure].std() == 0:
        return _gate("selection_risk", GateStatus.WARN, "Selection diagnostic is not estimable.")
    corr = float(np.corrcoef(pair[baseline], pair[exposure])[0, 1])
    abs_corr = abs(corr)
    # Public demonstration heuristic only; not a production threshold.
    if abs_corr >= 0.25:
        return _gate(
            "selection_risk",
            GateStatus.WARN,
            "Exposure is materially related to baseline intent; self-selection remains plausible.",
            baseline_exposure_correlation=corr,
            public_demo_threshold=0.25,
        )
    return _gate(
        "selection_risk",
        GateStatus.PASS,
        "No large baseline-intent relationship is visible in this public diagnostic.",
        baseline_exposure_correlation=corr,
        public_demo_threshold=0.25,
    )


def counterfactual_gate(df: pd.DataFrame, manifest: dict) -> GateResult:
    design = manifest["design"]
    if design["type"] != "randomized":
        return _gate(
            "counterfactual",
            GateStatus.FAIL,
            "No randomized or otherwise identified counterfactual is declared in the observational design.",
        )
    treatment = design["treatment_column"]
    post = design["post_column"]
    if treatment not in df or post not in df:
        return _gate("counterfactual", GateStatus.FAIL, "Treatment or post indicator is missing.")
    groups = set(df[treatment].dropna().astype(int).unique())
    periods = set(df[post].dropna().astype(int).unique())
    if not {0, 1}.issubset(groups) or not {0, 1}.issubset(periods):
        return _gate(
            "counterfactual",
            GateStatus.FAIL,
            "Both treatment/control and pre/post observations are required.",
            treatment_values=sorted(groups),
            post_values=sorted(periods),
        )
    return _gate(
        "counterfactual",
        GateStatus.PASS,
        "Random assignment with treatment/control and pre/post observations provides a counterfactual for the tested scope.",
        treatment_values=sorted(groups),
        post_values=sorted(periods),
    )


def randomization_balance_gate(df: pd.DataFrame, manifest: dict) -> GateResult:
    design = manifest["design"]
    if design["type"] != "randomized":
        return _gate("randomization_balance", GateStatus.NOT_APPLICABLE, "Not a randomized design.")
    baseline = manifest["measurement"].get("baseline_intent_column")
    if not baseline:
        return _gate("randomization_balance", GateStatus.WARN, "No baseline covariate was declared for a simple balance diagnostic.")
    treatment = design["treatment_column"]
    unit = manifest["dataset"]["unit_column"]
    unit_level = df.groupby(unit).agg({treatment: "first", baseline: "mean"}).dropna()
    means = unit_level.groupby(treatment)[baseline].mean()
    if not {0, 1}.issubset(set(means.index.astype(int))):
        return _gate("randomization_balance", GateStatus.FAIL, "Treatment or control group missing in baseline diagnostic.")
    pooled_sd = float(unit_level[baseline].std(ddof=1))
    smd = abs(float(means.loc[1] - means.loc[0])) / pooled_sd if pooled_sd else 0.0
    status = GateStatus.PASS if smd <= 0.25 else GateStatus.WARN
    return _gate(
        "randomization_balance",
        status,
        "Simple baseline balance is acceptable for the public demonstration." if status == GateStatus.PASS else "Baseline imbalance is visible; randomization or sample size should be reviewed.",
        standardized_mean_difference=smd,
        public_demo_threshold=0.25,
    )


def primary_outcome_gate(manifest: dict) -> GateResult:
    primary = manifest["measurement"].get("primary_outcome", True)
    if primary:
        return _gate("primary_outcome", GateStatus.PASS, "A single primary outcome is declared for the demonstration.")
    return _gate("primary_outcome", GateStatus.WARN, "Primary outcome is not pre-declared.")


def collect_basic_gates(df: pd.DataFrame, manifest: dict) -> list[GateResult]:
    return [
        data_completeness_gate(df, manifest),
        grain_gate(df, manifest),
        exposure_variation_gate(df, manifest),
        control_gate(df, manifest),
        selection_risk_gate(df, manifest),
        counterfactual_gate(df, manifest),
        randomization_balance_gate(df, manifest),
        primary_outcome_gate(manifest),
    ]
