import json
from pathlib import Path
from signal_to_proof.pipeline import run_manifest
from conftest import ROOT


def test_large_business_mde_requirement_can_fail_power_gate(tmp_path):
    manifest_path = ROOT / "demo/manifests/randomized.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["dataset"]["path"] = str((ROOT / "demo/data/randomized_signals.csv").resolve())
    # Requiring detection of an extremely small effect makes the existing design underpowered.
    manifest["design"]["business_mde"] = 0.0001
    temp = tmp_path / "manifest.json"
    temp.write_text(json.dumps(manifest))
    result = run_manifest(temp)
    assert result["power_gate"]["status"] == "FAIL"
    assert result["evidence_grade"] != "CAUSAL_EXPERIMENT"
