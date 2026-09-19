import pandas as pd
from signal_to_proof.gates import grain_gate
from signal_to_proof.manifest import load_manifest
from conftest import ROOT


def test_duplicate_unit_time_fails_grain_gate():
    manifest = load_manifest(ROOT / "demo/manifests/observational.json")
    df = pd.read_csv(ROOT / "demo/data/observational_signals.csv")
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    gate = grain_gate(df, manifest)
    assert gate.status.value == "FAIL"
