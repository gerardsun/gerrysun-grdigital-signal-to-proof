from signal_to_proof.pipeline import run_manifest
from conftest import ROOT


def test_observational_counterfactual_fails():
    result = run_manifest(ROOT / "demo/manifests/observational.json")
    gate = next(g for g in result["gates"] if g["name"] == "counterfactual")
    assert gate["status"] == "FAIL"
    assert result["evidence_grade"] != "CAUSAL_EXPERIMENT"
