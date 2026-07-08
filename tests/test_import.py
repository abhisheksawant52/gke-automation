"""Smoke tests: the package and its modules import cleanly."""

from __future__ import annotations

import gke_automation


def test_version() -> None:
    assert gke_automation.__version__ == "0.1.0"


def test_public_exports() -> None:
    assert hasattr(gke_automation, "GKEManager")
    assert hasattr(gke_automation, "Settings")
    assert callable(gke_automation.get_settings)
