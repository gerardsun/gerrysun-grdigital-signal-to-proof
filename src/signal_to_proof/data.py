from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_data(manifest: dict) -> pd.DataFrame:
    manifest_path = Path(manifest["_manifest_path"])
    configured = Path(manifest["dataset"]["path"])
    path = configured if configured.is_absolute() else (manifest_path.parent / configured)
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() != ".csv":
        raise ValueError("Public demonstrator accepts CSV demo data")
    return pd.read_csv(path)


def required_columns(manifest: dict) -> list[str]:
    cols = [
        manifest["dataset"]["unit_column"],
        manifest["dataset"]["time_column"],
        manifest["measurement"]["exposure_column"],
        manifest["measurement"]["outcome_column"],
        *manifest["measurement"].get("controls", []),
    ]
    design = manifest["design"]
    if design["type"] == "randomized":
        cols.extend([design["treatment_column"], design["post_column"]])
    baseline_intent = manifest["measurement"].get("baseline_intent_column")
    if baseline_intent:
        cols.append(baseline_intent)
    return list(dict.fromkeys(cols))
