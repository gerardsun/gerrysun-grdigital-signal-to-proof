import json
from signal_to_proof.manifest import validate_manifest


def test_valid_observational_manifest():
    manifest = {
        "version":"1",
        "project_name":"x",
        "decision":{"question":"q","decision_options":["a"],"required_evidence_grade":"CONTROLLED_ASSOCIATION"},
        "dataset":{"path":"x.csv","grain":"unit_time","unit_column":"unit","time_column":"time"},
        "measurement":{"exposure_column":"x","outcome_column":"y","controls":[]},
        "design":{"type":"observational"},
        "economics":{"decision_exposure":1,"test_cost":1,"error_cost_fraction":0.1,"uncertainty_fraction":0.1}
    }
    validate_manifest(manifest)
