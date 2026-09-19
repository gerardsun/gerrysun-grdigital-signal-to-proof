from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from signal_to_proof.pipeline import run_manifest


SCENARIOS = {
    "observational": ROOT / "demo" / "manifests" / "observational.json",
    "randomized": ROOT / "demo" / "manifests" / "randomized.json",
}


def compact_print(result: dict) -> None:
    print("\nSIGNAL-TO-PROOF")
    print("=" * 72)
    print(f"Scenario: {result['scenario']}")
    print(f"Decision: {result['decision']['question']}")
    print("-" * 72)
    print(f"Pearson r: {result['correlation']['pearson_r']:.3f}")
    if result.get("controlled_model"):
        print(f"Controlled exposure coefficient: {result['controlled_model']['exposure_coefficient']:.5f}")
    if result.get("causal_estimate"):
        print(f"Estimated randomized pre/post effect: {result['causal_estimate']['effect']:.5f}")
    print(f"Evidence grade: {result['evidence_grade']}")
    print(f"Allowed claim: {result['allowed_claim']}")
    print(f"Blocked claim: {result['blocked_claim']}")
    print(f"Business action: {result['business_action']}")
    print(f"Next evidence step: {result['next_evidence_step']}")
    print("\nGates")
    for gate in result["gates"]:
        print(f"  {gate['status']:<14} {gate['name']}: {gate['reason']}")
    print("=" * 72)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a packaged Signal-to-Proof demo scenario.")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="observational")
    parser.add_argument("--json", action="store_true", help="Print full structured JSON")
    args = parser.parse_args()

    result = run_manifest(SCENARIOS[args.scenario])
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        compact_print(result)


if __name__ == "__main__":
    main()
