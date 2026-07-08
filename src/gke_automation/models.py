"""Typed specifications used by the GKE manager.

These dataclasses decouple the manager's public API from the shape of the
underlying protobuf request objects and provide validated, well-documented
inputs that can be constructed from :class:`~gke_automation.config.Settings`.
"""

from __future__ import annotations

from dataclasses import dataclass

from gke_automation.config import Settings
from gke_automation.exceptions import InvalidConfigurationError


@dataclass(slots=True)
class ClusterSpec:
    """Specification for creating a GKE cluster.

    Attributes:
        name: Cluster name.
        node_count: Initial node count for the default node pool.
        machine_type: Compute Engine machine type for the nodes.
        release_channel: GKE release channel.
    """

    name: str
    node_count: int = 3
    machine_type: str = "e2-standard-4"
    release_channel: str = "REGULAR"

    def __post_init__(self) -> None:
        if self.node_count < 1:
            raise InvalidConfigurationError("node_count must be >= 1")

    @classmethod
    def from_settings(cls, settings: Settings) -> "ClusterSpec":
        """Build a cluster spec from the active settings."""
        return cls(
            name=settings.cluster_name,
            node_count=settings.node_count,
            machine_type=settings.machine_type,
            release_channel=settings.release_channel,
        )


@dataclass(slots=True)
class NodePoolSpec:
    """Specification for creating a node pool.

    Attributes:
        name: Node pool name.
        node_count: Initial node count.
        machine_type: Compute Engine machine type.
        autoscaling: Whether cluster autoscaling is enabled.
        min_nodes: Minimum node count when autoscaling.
        max_nodes: Maximum node count when autoscaling.
    """

    name: str
    node_count: int = 3
    machine_type: str = "e2-standard-4"
    autoscaling: bool = True
    min_nodes: int = 1
    max_nodes: int = 5

    def __post_init__(self) -> None:
        if self.autoscaling and self.max_nodes < self.min_nodes:
            raise InvalidConfigurationError("max_nodes must be >= min_nodes")

    @classmethod
    def from_settings(cls, settings: Settings, name: str = "default-pool") -> "NodePoolSpec":
        """Build a node pool spec from the active settings."""
        return cls(
            name=name,
            node_count=settings.node_count,
            machine_type=settings.machine_type,
            min_nodes=settings.min_nodes,
            max_nodes=settings.max_nodes,
        )
