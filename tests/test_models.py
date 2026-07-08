"""Unit tests for the spec dataclasses (pure logic, no network)."""

from __future__ import annotations

import pytest

from gke_automation.config import Settings
from gke_automation.exceptions import InvalidConfigurationError
from gke_automation.models import ClusterSpec, NodePoolSpec


def test_cluster_spec_from_settings() -> None:
    settings = Settings(cluster_name="primary", node_count=4, machine_type="e2-standard-8")
    spec = ClusterSpec.from_settings(settings)
    assert spec.name == "primary"
    assert spec.node_count == 4
    assert spec.machine_type == "e2-standard-8"


def test_cluster_spec_rejects_zero_nodes() -> None:
    with pytest.raises(InvalidConfigurationError):
        ClusterSpec(name="x", node_count=0)


def test_node_pool_spec_rejects_bad_autoscaling_bounds() -> None:
    with pytest.raises(InvalidConfigurationError):
        NodePoolSpec(name="pool", autoscaling=True, min_nodes=5, max_nodes=2)


def test_node_pool_spec_from_settings() -> None:
    settings = Settings(node_count=2, min_nodes=1, max_nodes=6)
    spec = NodePoolSpec.from_settings(settings, name="workers")
    assert spec.name == "workers"
    assert spec.min_nodes == 1
    assert spec.max_nodes == 6
