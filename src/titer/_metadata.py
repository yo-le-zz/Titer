import tomllib
from pathlib import Path


# ─────────────────────────────────────────────
# Project metadata
# ─────────────────────────────────────────────

ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = ROOT / "pyproject.toml"

with PYPROJECT.open("rb") as file:
    _project = tomllib.load(file)["project"]


__name__ = _project["name"]
__version__ = _project["version"]
__description__ = _project["description"]

__author__ = ", ".join(
    author["name"]
    for author in _project.get("authors", [])
)

_license = _project.get("license", {})
__license__ = _license.get("text", "Unknown")


# ─────────────────────────────────────────────
# Supported languages
# ─────────────────────────────────────────────

LANG_DIR = Path(__file__).parent / "lang"

__language__ = ", ".join(
    directory.name
    for directory in LANG_DIR.iterdir()
    if directory.is_dir()
    and (directory / "__init__.py").is_file()
    and not directory.name.startswith("_")
)
