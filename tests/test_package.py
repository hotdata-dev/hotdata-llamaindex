from __future__ import annotations

import re
from pathlib import Path

import pytest
from importlib.metadata import version as dist_version

import hotdata_llamaindex as hli


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO_ROOT / "hotdata_llamaindex"
_RUNTIME_SUBMODULE = re.compile(
    r"(?m)^\s*(?:from\s+hotdata_runtime\.(client|env|result|health)\s+import"
    r"|import\s+hotdata_runtime\.(client|env|result|health)(?:\s|$|,|as))"
)


def test_version_is_pep440_core():
    assert re.fullmatch(r"\d+\.\d+\.\d+(\+.*)?", hli.__version__)


def test_version_matches_distribution_metadata():
    assert dist_version("hotdata-llamaindex") == hli.__version__


@pytest.mark.parametrize("name", hli.__all__)
def test_public_export_is_importable(name: str):
    assert hasattr(hli, name), f"missing export: {name}"
    assert getattr(hli, name) is not None


def test_source_uses_hotdata_runtime_root_imports():
    violations: list[str] = []
    for path in SOURCE_ROOT.rglob("*.py"):
        if _RUNTIME_SUBMODULE.search(path.read_text(encoding="utf-8")):
            violations.append(str(path.relative_to(REPO_ROOT)))
    assert not violations, (
        "Use `from hotdata_runtime import ...` in package source; "
        f"found submodule imports in: {', '.join(violations)}"
    )
