"""Unit tests for configuration and resource-path helpers."""

from __future__ import annotations

import pytest

from gke_automation.config import Settings


def test_parent_and_cluster_path() -> None:
    settings = Settings(project_id="acme", location="europe-west1", cluster_name="primary")
    assert settings.parent == "projects/acme/locations/europe-west1"
    assert settings.cluster_path() == "projects/acme/locations/europe-west1/clusters/primary"
    assert settings.cluster_path("other").endswith("/clusters/other")


def test_release_channel_normalised() -> None:
    settings = Settings(release_channel="stable")
    assert settings.release_channel == "STABLE"


def test_invalid_release_channel_rejected() -> None:
    with pytest.raises(ValueError):
        Settings(release_channel="turbo")


def test_max_nodes_must_exceed_min() -> None:
    with pytest.raises(ValueError):
        Settings(min_nodes=5, max_nodes=2)
