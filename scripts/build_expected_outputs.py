from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from signal_to_proof.pipeline import run_manifest

for scenario in ("observational", "randomized"):
    result = run_manifest(ROOT / "demo" / "manifests" / f"{scenario}.json")
    target = ROOT / "demo" / "expected" / f"{scenario}_result.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(target)
