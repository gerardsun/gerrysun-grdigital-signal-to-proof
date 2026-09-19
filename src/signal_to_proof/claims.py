from __future__ import annotations

from .types import EvidenceGrade, GateStatus


def _status(gates: list[dict], name: str) -> str | None:
    for gate in gates:
        if gate["name"] == name:
            return gate["status"]
    return None


def grade_and_claim(
    manifest: dict,
    gates: list[dict],
    controlled_model: dict | None,
    causal_estimate: dict | None,
    power_gate: dict | None,
) -> dict:
    design = manifest["design"]["type"]
    variation_ok = _status(gates, "exposure_variation") == GateStatus.PASS.value
    counterfactual_ok = _status(gates, "counterfactual") == GateStatus.PASS.value
    data_ok = _status(gates, "data_completeness") != GateStatus.FAIL.value
    grain_ok = _status(gates, "grain") == GateStatus.PASS.value
    power_ok = power_gate is not None and power_gate.get("status") == GateStatus.PASS.value

    if design == "randomized" and data_ok and grain_ok and counterfactual_ok and power_ok and causal_estimate:
        grade = EvidenceGrade.CAUSAL_EXPERIMENT
        allowed = "Within the tested design and period, the randomized intervention caused a measurable change in the primary outcome."
        blocked = "The intervention will produce the same effect in every market, audience, product, or future period."
        limitation = "Causal validity is limited to the tested scope; external validity requires replication and operating judgment."
    elif controlled_model and variation_ok:
        grade = EvidenceGrade.CONTROLLED_ASSOCIATION
        allowed = "Exposure is associated with the primary outcome after the declared measured controls and fixed effects."
        blocked = "Exposure caused the observed outcome change or incremental business value."
        limitation = "Unobserved selection, reverse causality, or residual time-varying confounding may still explain part of the relationship."
    else:
        grade = EvidenceGrade.DIRECTIONAL_ASSOCIATION
        allowed = "Exposure and the primary outcome move together in the observed data."
        blocked = "Exposure caused the observed outcome change."
        limitation = "The design does not isolate the intervention from alternative explanations."

    return {
        "evidence_grade": grade.value,
        "allowed_claim": allowed,
        "blocked_claim": blocked,
        "claim_ceiling": grade.value,
        "limitation": limitation,
    }
