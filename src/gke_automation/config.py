"""Configuration for gke-automation.

Settings are loaded from environment variables (optionally from a ``.env``
file) using :mod:`pydantic_settings`. Every value has a sensible default so
the package can be imported without a populated environment; production use
is expected to override them via ``GKE_*`` environment variables.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the GKE automation toolkit.

    Attributes:
        project_id: The Google Cloud project that owns the cluster.
        location: Region or zone for the cluster (e.g. ``europe-west1`` or
            ``europe-west1-b``). Regional clusters use a region.
        zone: Optional explicit zone used for zonal node placement.
        cluster_name: Default cluster name for CLI operations.
        node_count: Initial node count per node pool.
        machine_type: Compute Engine machine type for nodes.
        min_nodes: Minimum node count when autoscaling is enabled.
        max_nodes: Maximum node count when autoscaling is enabled.
        release_channel: GKE release channel (``RAPID``, ``REGULAR``,
            ``STABLE`` or ``UNSPECIFIED``).
        credentials_file: Optional path to a service-account key file. When
            unset, Application Default Credentials are used.
        log_level: Root log level for the package logger.
    """

    model_config = SettingsConfigDict(
        env_prefix="GKE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_id: str = Field(default="my-gcp-project", description="GCP project id")
    location: str = Field(default="europe-west1", description="Region or zone")
    zone: str = Field(default="europe-west1-b", description="Compute zone")
    cluster_name: str = Field(default="primary", description="Default cluster name")

    node_count: int = Field(default=3, ge=1, description="Initial nodes per pool")
    machine_type: str = Field(default="e2-standard-4", description="Node machine type")
    min_nodes: int = Field(default=1, ge=0, description="Autoscaling minimum")
    max_nodes: int = Field(default=5, ge=1, description="Autoscaling maximum")

    release_channel: str = Field(default="REGULAR", description="GKE release channel")
    credentials_file: str | None = Field(default=None, description="SA key path")
    log_level: str = Field(default="INFO", description="Logging level")

    @field_validator("release_channel")
    @classmethod
    def _validate_channel(cls, value: str) -> str:
        allowed = {"RAPID", "REGULAR", "STABLE", "UNSPECIFIED"}
        upper = value.upper()
        if upper not in allowed:
            raise ValueError(f"release_channel must be one of {sorted(allowed)}")
        return upper

    @field_validator("max_nodes")
    @classmethod
    def _validate_max_nodes(cls, value: int, info) -> int:
        min_nodes = info.data.get("min_nodes", 0)
        if value < min_nodes:
            raise ValueError("max_nodes must be >= min_nodes")
        return value

    @property
    def parent(self) -> str:
        """Return the fully-qualified parent resource for API calls."""
        return f"projects/{self.project_id}/locations/{self.location}"

    def cluster_path(self, cluster_name: str | None = None) -> str:
        """Return the fully-qualified resource name for a cluster.

        Args:
            cluster_name: Cluster name; falls back to :attr:`cluster_name`.

        Returns:
            A resource path of the form
            ``projects/<p>/locations/<l>/clusters/<c>``.
        """
        name = cluster_name or self.cluster_name
        return f"{self.parent}/clusters/{name}"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance."""
    return Settings()
