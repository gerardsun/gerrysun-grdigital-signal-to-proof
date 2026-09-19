from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import run_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Signal-to-Proof public demonstrator.")
    parser.add_argument("manifest", type=Path, help="Path to an evidence manifest JSON file")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()

    result = run_manifest(args.manifest)
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
