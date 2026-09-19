from __future__ import annotations

from pathlib import Path
from typing import Any

from .causal import randomized_prepost_effect
from .claims import grade_and_claim
from .correlation import correlation_summary, controlled_association, lagged_correlations
from .data import load_data
from .economics import economic_screen
from .gates import collect_basic_gates
from .manifest import load_manifest
from .power import mde_two_group
from .recommend import recommend_next_step
from .types import GateStatus


def _power_gate(power_result: dict | None, manifest: dict) -> dict | None:
    if power_result is None:
        return None
    business_mde = manifest["design"].get("business_mde")
    if business_mde is None or power_result.get("outcome_unit_mde") is None:
        return {
            "name": "power",
            "status": GateStatus.WARN.value,
            "reason": "Power is estimable, but no business minimum effect was declared.",
            "details": power_result,
        }
    passes = power_result["outcome_unit_mde"] <= float(business_mde)
    return {
        "name": "power",
        "status": GateStatus.PASS.value if passes else GateStatus.FAIL.value,
        "reason": (
            "The available design can detect the declared business-relevant effect."
            if passes
            else "The available design is too weak to detect the declared business-relevant effect."
        ),
        "details": {**power_result, "business_mde": float(business_mde)},
    }


def run_manifest(manifest_path: str | Path) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    df = load_data(manifest)

    exposure = manifest["measurement"]["exposure_column"]
    outcome = manifest["measurement"]["outcome_column"]
    controls = manifest["measurement"].get("controls", [])
    fixed_effects = manifest["measurement"].get("fixed_effects", [])

    gates = [g.to_dict() for g in collect_basic_gates(df, manifest)]
    if any(g["status"] == GateStatus.FAIL.value and g["name"] in {"data_completeness", "grain"} for g in gates):
        raise ValueError("Core data-readiness gate failed; modeling is blocked")

    corr = correlation_summary(df, exposure, outcome)
    lags = lagged_correlations(
        df,
        manifest["dataset"]["unit_column"],
        manifest["dataset"]["time_column"],
        exposure,
        outcome,
        manifest["measurement"].get("lags", [0, 1, 2]),
    )

    controlled = None
    if controls:
        controlled = controlled_association(df, exposure, outcome, controls, fixed_effects)

    causal_estimate = None
    power_result = None
    power_gate = None
    if manifest["design"]["type"] == "randomized":
        causal_estimate = randomized_prepost_effect(
            df,
            outcome,
            manifest["design"]["treatment_column"],
            manifest["design"]["post_column"],
            manifest["dataset"]["unit_column"],
            manifest["dataset"]["time_column"],
        )
        power_result = mde_two_group(
            df,
            outcome,
            manifest["design"]["treatment_column"],
            manifest["design"]["post_column"],
            alpha=float(manifest["design"].get("alpha", 0.05)),
            power=float(manifest["design"].get("power", 0.80)),
        )
        power_gate = _power_gate(power_result, manifest)
        gates.append(power_gate)

    economics = economic_screen(manifest["economics"])
    claim = grade_and_claim(manifest, gates, controlled, causal_estimate, power_gate)

    result: dict[str, Any] = {
        "scenario": manifest["project_name"],
        "decision": manifest["decision"],
        "economics": economics,
        "correlation": corr,
        "lagged_correlations": lags,
        "controlled_model": controlled,
        "causal_estimate": causal_estimate,
        "power_gate": power_gate,
        "gates": gates,
        **claim,
    }
    result.update(recommend_next_step(result, manifest))
    return result
