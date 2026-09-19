from signal_to_proof.pipeline import run_manifest
from conftest import ROOT


def test_randomized_design_can_earn_causal_grade():
    result = run_manifest(ROOT / "demo/manifests/randomized.json")
    assert result["power_gate"]["status"] == "PASS"
    assert result["evidence_grade"] == "CAUSAL_EXPERIMENT"
    assert "within the tested design" in result["allowed_claim"].lower()
