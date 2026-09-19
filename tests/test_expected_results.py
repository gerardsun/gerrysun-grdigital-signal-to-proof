import json
from signal_to_proof.pipeline import run_manifest
from conftest import ROOT


def test_expected_outputs_match_current_public_pipeline():
    for scenario in ("observational", "randomized"):
        current = run_manifest(ROOT / "demo/manifests" / f"{scenario}.json")
        expected = json.loads((ROOT / "demo/expected" / f"{scenario}_result.json").read_text())
        assert current["evidence_grade"] == expected["evidence_grade"]
        assert current["allowed_claim"] == expected["allowed_claim"]
        assert current["blocked_claim"] == expected["blocked_claim"]
        assert round(current["correlation"]["pearson_r"], 6) == round(expected["correlation"]["pearson_r"], 6)
