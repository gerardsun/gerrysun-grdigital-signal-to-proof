from signal_to_proof.pipeline import run_manifest
from conftest import ROOT


def test_observational_claim_language_is_bounded():
    result = run_manifest(ROOT / "demo/manifests/observational.json")
    assert "associated" in result["allowed_claim"].lower()
    assert "caused" in result["blocked_claim"].lower()


def test_randomized_claim_still_blocks_universal_generalization():
    result = run_manifest(ROOT / "demo/manifests/randomized.json")
    assert "same effect" in result["blocked_claim"].lower()
