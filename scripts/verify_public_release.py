from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {
    ".md", ".py", ".json", ".html", ".css", ".js", ".yml", ".yaml", ".txt", ".toml", ".cff", ".svg", ".csv"
}

# Restricted terms are assembled from fragments so they do not become part of the public text corpus themselves.
RESTRICTED_PATTERNS = {
    "restricted client name": r"\b" + "to" + "yo" + "ta" + r"\b",
    "restricted program acronym": r"\b" + "p" + "s" + "e" + r"\b",
    "restricted industry placeholder": r"\b" + "o" + "e" + "m" + r"\b",
    "restricted platform name": r"\b" + "smart" + "path" + r"\b",
    "restricted platform name 2": r"\b" + "touch" + "storm" + r"\b",
    "restricted identity label": r"\b1" + "to" + "yo" + "ta" + r"\b",
    "protected internal system name": r"\b" + "ar" + "cana" + r"\b",
    "protected internal system name 2": r"\b" + "pi" + "se" + r"\b",
    "protected internal system name 3": r"\b" + "vi" + "ta" + r"\b",
}

hits = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    for label, pattern in RESTRICTED_PATTERNS.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append((str(path.relative_to(ROOT)), label))

if hits:
    print("Public-release scan FAILED")
    for hit in hits:
        print(" -", hit)
    sys.exit(1)

print("Public-release scan PASS: no restricted client or protected internal terms detected.")
