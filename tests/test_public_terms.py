from pathlib import Path
from conftest import ROOT

BANNED = [
    "to" + "yo" + "ta",
    "smart" + "path",
    "touch" + "storm",
    "1" + "to" + "yo" + "ta",
]


def test_public_repository_has_no_restricted_client_terms():
    text_ext = {".md", ".py", ".json", ".html", ".css", ".js", ".yml", ".yaml", ".txt", ".toml", ".cff", ".svg"}
    hits = []
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in text_ext:
            content = path.read_text(encoding="utf-8", errors="ignore").lower()
            for token in BANNED:
                if token in content:
                    hits.append((str(path.relative_to(ROOT)), token))
    assert not hits, hits
