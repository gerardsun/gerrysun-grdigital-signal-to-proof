from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "version",
    "project_name",
    "decision",
    "dataset",
    "measurement",
    "design",
    "economics",
}


def load_manifest(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    manifest["_manifest_path"] = str(path.resolve())
    return manifest


def validate_manifest(manifest: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL - set(manifest))
    if missing:
        raise ValueError(f"Manifest missing top-level fields: {missing}")

    for section in ("decision", "dataset", "measurement", "design", "economics"):
        if not isinstance(manifest[section], dict):
            raise ValueError(f"Manifest section '{section}' must be an object")

    dataset_required = {"path", "grain", "unit_column", "time_column"}
    measurement_required = {"exposure_column", "outcome_column", "controls"}
    decision_required = {"question", "decision_options", "required_evidence_grade"}
    economics_required = {
        "decision_exposure",
        "test_cost",
        "error_cost_fraction",
        "uncertainty_fraction",
    }

    checks = [
        ("dataset", dataset_required),
        ("measurement", measurement_required),
        ("decision", decision_required),
        ("economics", economics_required),
    ]
    for section, required in checks:
        absent = sorted(required - set(manifest[section]))
        if absent:
            raise ValueError(f"Manifest section '{section}' missing fields: {absent}")

    design_type = manifest["design"].get("type")
    if design_type not in {"observational", "randomized"}:
        raise ValueError("Public demonstrator supports design.type 'observational' or 'randomized'")

    if design_type == "randomized":
        required = {"treatment_column", "post_column"}
        absent = sorted(required - set(manifest["design"]))
        if absent:
            raise ValueError(f"Randomized design missing fields: {absent}")
