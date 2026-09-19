from signal_to_proof.pipeline import run_manifest
from conftest import ROOT


def test_observational_stops_at_controlled_association():
    result = run_manifest(ROOT / "demo/manifests/observational.json")
    assert result["evidence_grade"] == "CONTROLLED_ASSOCIATION"
    assert "caused" in result["blocked_claim"].lower()
    assert result["business_action"] == "PROVE_BEFORE_SCALE"
