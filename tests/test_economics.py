from signal_to_proof.economics import economic_screen


def test_economic_screen_is_transparent():
    result = economic_screen({
        "decision_exposure": 1_000_000,
        "test_cost": 50_000,
        "error_cost_fraction": 0.2,
        "uncertainty_fraction": 0.5,
    })
    assert result["expected_decision_loss"] == 100_000
    assert result["test_economically_plausible"] is True
