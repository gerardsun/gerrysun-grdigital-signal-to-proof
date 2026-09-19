from __future__ import annotations


def economic_screen(config: dict) -> dict:
    decision_exposure = float(config["decision_exposure"])
    test_cost = float(config["test_cost"])
    error_cost_fraction = float(config["error_cost_fraction"])
    uncertainty_fraction = float(config["uncertainty_fraction"])

    expected_decision_loss = decision_exposure * error_cost_fraction * uncertainty_fraction
    test_cost_ratio = test_cost / expected_decision_loss if expected_decision_loss else None
    test_economically_plausible = bool(expected_decision_loss > 0 and test_cost <= expected_decision_loss)

    return {
        "decision_exposure": decision_exposure,
        "test_cost": test_cost,
        "error_cost_fraction": error_cost_fraction,
        "uncertainty_fraction": uncertainty_fraction,
        "expected_decision_loss": expected_decision_loss,
        "test_cost_to_expected_loss": test_cost_ratio,
        "test_economically_plausible": test_economically_plausible,
        "interpretation": (
            "The test cost is below the simple expected-decision-loss screen."
            if test_economically_plausible
            else "The test cost exceeds the simple expected-decision-loss screen; continue lower-cost measurement unless the strategic value of learning is higher than represented here."
        ),
    }
