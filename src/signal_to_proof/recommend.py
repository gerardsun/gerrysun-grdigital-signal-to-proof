from __future__ import annotations


def recommend_next_step(result: dict, manifest: dict) -> dict:
    grade = result["evidence_grade"]
    gates = {g["name"]: g for g in result["gates"]}
    economics = result["economics"]

    if gates.get("exposure_variation", {}).get("status") == "FAIL":
        next_step = "Create measurable treatment variation through staggered rollout, randomized routing, or another design that changes exposure across eligible units."
    elif grade in {"DIRECTIONAL_ASSOCIATION", "CONTROLLED_ASSOCIATION", "MATCHED_ASSOCIATION"}:
        if economics["test_economically_plausible"]:
            next_step = "Design a powered randomized or geo-based holdout around the primary decision before scaling the claim to incrementality."
        else:
            next_step = "Continue controlled observational monitoring and improve instrumentation; the simple economic screen does not yet justify a higher-cost causal test."
    elif grade == "QUASI_EXPERIMENTAL":
        next_step = "Stress-test identification assumptions and replicate in another period or market; randomize when operationally feasible."
    else:
        next_step = "Replicate the test across a new eligible population before generalizing the effect beyond the tested scope."

    if (result.get("power_gate") or {}).get("status") == "FAIL":
        next_step = "Redesign the test before interpreting a null: increase units or duration, reduce noise, or choose a nearer-term primary outcome with an acceptable business meaning."

    return {
        "next_evidence_step": next_step,
        "business_action": _business_action(grade, economics),
        "operating_implications": _operating_implications(grade),
    }


def _business_action(grade: str, economics: dict) -> str:
    if grade == "CAUSAL_EXPERIMENT":
        return "SCALE_WITH_BOUNDS"
    if economics["test_economically_plausible"]:
        return "PROVE_BEFORE_SCALE"
    return "MEASURE_AND_IMPROVE"


def _operating_implications(grade: str) -> dict:
    if grade == "CAUSAL_EXPERIMENT":
        return {
            "strategy": "Use the tested effect as decision evidence within scope; keep generalization explicit.",
            "economics": "Update the investment case with the incremental effect and its uncertainty interval.",
            "product": "Preserve treatment instrumentation and assignment logging for replication.",
            "ux": "Identify which experience moments plausibly mediated the measured effect without treating mediation as proven.",
            "gtm": "Scale only to populations sufficiently similar to the tested units, with monitoring for effect drift.",
            "ml": "Use predictive models to target learning or operational efficiency, not to overwrite the randomized effect estimate.",
        }
    return {
        "strategy": "Treat the relationship as a prioritization signal, not proof of incremental value.",
        "economics": "Use the result to decide whether stronger evidence is worth funding.",
        "product": "Improve event taxonomy, exposure logging, identity continuity, and treatment instrumentation.",
        "ux": "Use observed progression and friction as hypotheses for redesign and testing.",
        "gtm": "Prioritize the associated audience or journey hypothesis for a controlled activation rather than claiming lift.",
        "ml": "Use prediction and segmentation to focus the test surface while keeping effect estimation separate.",
    }
