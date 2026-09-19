import json
import pandas as pd
from signal_to_proof.gates import exposure_variation_gate
from signal_to_proof.manifest import load_manifest
from conftest import ROOT


def test_no_exposure_variation_fails_gate(tmp_path):
    manifest = load_manifest(ROOT / "demo/manifests/observational.json")
    df = pd.read_csv(ROOT / "demo/data/observational_signals.csv")
    df[manifest["measurement"]["exposure_column"]] = 1.0
    gate = exposure_variation_gate(df, manifest)
    assert gate.status.value == "FAIL"
