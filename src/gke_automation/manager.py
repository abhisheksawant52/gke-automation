"""High-level manager wrapping the Google Kubernetes Engine API.

The :class:`GKEManager` provides typed, documented methods over
``google.cloud.container_v1.ClusterManagerClient`` for the common lifecycle
operations: creating and deleting clusters, listing and describing them,
managing node pools, and rendering a kubeconfig for a running cluster.

The manager is intentionally thin. It builds the request payloads, delegates
to the underlying client, and returns the API objects (or lightly shaped
dictionaries) so callers can compose higher-level workflows.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from google.cloud import container_v1

from gke_automation.config import Settings, get_settings
from gke_automation.logging_config import configure_logging, get_logger
from gke_automation.models import ClusterSpec, NodePoolSpec

if TYPE_CHECKING:
    from google.auth.credentials import Credentials

logger = get_logger(__name__)


class GKEManager:
    """Manage GKE clusters and node pools for a single project/location.

    Args:
        settings: Optional :class:`~gke_automation.config.Settings`. When
            omitted, settings are loaded from the environment.
        credentials: Optional pre-built Google auth credentials. When
            omitted, Application Default Credentials are used.
    """

    def __init__(
        self,
        settings: Settings | None = None,
        credentials: "Credentials | None" = None,
    ) -> None:
        self.settings = settings or get_settings()
        configure_logging(self.settings.log_level)
        self._credentials = credentials
        self._client: container_v1.ClusterManagerClient | None = None

    # ------------------------------------------------------------------ #
    # Client plumbing
    # ------------------------------------------------------------------ #
    @property
    def client(self) -> container_v1.ClusterManagerClient:
        """Return a lazily-initialised cluster manager client."""
        if self._client is None:
            self._client = container_v1.ClusterManagerClient(
                credentials=self._resolve_credentials()
            )
        return self._client

    def _resolve_credentials(self) -> "Credentials | None":
        """Resolve credentials from explicit input, key file, or ADC."""
        if self._credentials is not None:
            return self._credentials
        if self.settings.credentials_file:
            from google.oauth2 import service_account

            self._credentials = service_account.Credentials.from_service_account_file(
                self.settings.credentials_file
            )
            return self._credentials
        # Fall back to Application Default Credentials.
        import google.auth

        self._credentials, _ = google.auth.default()
        return self._credentials

    # ------------------------------------------------------------------ #
    # Cluster lifecycle
    # ------------------------------------------------------------------ #
    def create_cluster(self, spec: ClusterSpec | None = None) -> Any:
        """Create a GKE cluster.

        Args:
            spec: Cluster specification. When omitted, one is derived from
                the active settings.

        Returns:
            The long-running :class:`Operation` returned by the API.
        """
        spec = spec or ClusterSpec.from_settings(self.settings)
        cluster = container_v1.Cluster(
            name=spec.name,
            initial_node_count=spec.node_count,
            release_channel=container_v1.ReleaseChannel(channel=spec.release_channel),
            node_config=container_v1.NodeConfig(
                machine_type=spec.machine_type,
                oauth_scopes=["https://www.googleapis.com/auth/cloud-platform"],
            ),
        )
        request = container_v1.CreateClusterRequest(
            parent=self.settings.parent, cluster=cluster
        )
        logger.info("Creating cluster %s in %s", spec.name, self.settings.location)
        return self.client.create_cluster(request=request)

    def get_cluster(self, cluster_name: str | None = None) -> Any:
        """Fetch a single cluster by name.

        Args:
            cluster_name: Cluster name; defaults to the configured cluster.

        Returns:
            The :class:`Cluster` resource.
        """
        name = self.settings.cluster_path(cluster_name)
        logger.debug("Describing cluster %s", name)
        return self.client.get_cluster(request=container_v1.GetClusterRequest(name=name))

    def list_clusters(self) -> list[Any]:
        """List all clusters in the configured project/location.

        Returns:
            A list of :class:`Cluster` resources.
        """
        request = container_v1.ListClustersRequest(parent=self.settings.parent)
        response = self.client.list_clusters(request=request)
        return list(response.clusters)

    def delete_cluster(self, cluster_name: str | None = None) -> Any:
        """Delete a cluster.

        Args:
            cluster_name: Cluster name; defaults to the configured cluster.

        Returns:
            The long-running :class:`Operation` returned by the API.
        """
        name = self.settings.cluster_path(cluster_name)
        logger.info("Deleting cluster %s", name)
        return self.client.delete_cluster(
            request=container_v1.DeleteClusterRequest(name=name)
        )

    def update_master_version(
        self, version: str, cluster_name: str | None = None
    ) -> Any:
        """Upgrade the control-plane (master) version of a cluster.

        Args:
            version: Target Kubernetes version, e.g. ``"1.29.5-gke.1091002"``.
            cluster_name: Cluster name; defaults to the configured cluster.

        Returns:
            The long-running :class:`Operation` returned by the API.
        """
        name = self.settings.cluster_path(cluster_name)
        logger.info("Upgrading control plane of %s to %s", name, version)
        request = container_v1.UpdateMasterRequest(name=name, master_version=version)
        return self.client.update_master(request=request)

    # ------------------------------------------------------------------ #
    # Node pool management
    # ------------------------------------------------------------------ #
    def create_node_pool(
        self, spec: NodePoolSpec, cluster_name: str | None = None
    ) -> Any:
        """Create a node pool on an existing cluster.

        Args:
            spec: Node pool specification.
            cluster_name: Cluster name; defaults to the configured cluster.

        Returns:
            The long-running :class:`Operation` returned by the API.
        """
        parent = self.settings.cluster_path(cluster_name)
        node_pool = container_v1.NodePool(
            name=spec.name,
            initial_node_count=spec.node_count,
            config=container_v1.NodeConfig(machine_type=spec.machine_type),
            autoscaling=container_v1.NodePoolAutoscaling(
                enabled=spec.autoscaling,
                min_node_count=spec.min_nodes,
                max_node_count=spec.max_nodes,
            ),
        )
        request = container_v1.CreateNodePoolRequest(parent=parent, node_pool=node_pool)
        logger.info("Creating node pool %s on %s", spec.name, parent)
        return self.client.create_node_pool(request=request)

    def resize_node_pool(
        self, node_pool: str, node_count: int, cluster_name: str | None = None
    ) -> Any:
        """Set the node count of a node pool.

        Args:
            node_pool: Name of the node pool to resize.
            node_count: Desired number of nodes.
            cluster_name: Cluster name; defaults to the configured cluster.

        Returns:
            The long-running :class:`Operation` returned by the API.
        """
        name = f"{self.settings.cluster_path(cluster_name)}/nodePools/{node_pool}"
        logger.info("Resizing node pool %s to %d nodes", name, node_count)
        request = container_v1.SetNodePoolSizeRequest(name=name, node_count=node_count)
        return self.client.set_node_pool_size(request=request)

    def set_node_pool_autoscaling(
        self,
        node_pool: str,
        min_nodes: int,
        max_nodes: int,
        enabled: bool = True,
        cluster_name: str | None = None,
    ) -> Any:
        """Configure autoscaling for a node pool.

        Args:
            node_pool: Name of the node pool.
            min_nodes: Minimum node count.
            max_nodes: Maximum node count.
            enabled: Whether autoscaling is enabled.
            cluster_name: Cluster name; defaults to the configured cluster.

        Returns:
            The long-running :class:`Operation` returned by the API.
        """
        name = f"{self.settings.cluster_path(cluster_name)}/nodePools/{node_pool}"
        autoscaling = container_v1.NodePoolAutoscaling(
            enabled=enabled, min_node_count=min_nodes, max_node_count=max_nodes
        )
        logger.info(
            "Setting autoscaling on %s (enabled=%s, min=%d, max=%d)",
            name,
            enabled,
            min_nodes,
            max_nodes,
        )
        request = container_v1.SetNodePoolAutoscalingRequest(
            name=name, autoscaling=autoscaling
        )
        return self.client.set_node_pool_autoscaling(request=request)

    # ------------------------------------------------------------------ #
    # Access / kubeconfig
    # ------------------------------------------------------------------ #
    def get_kubeconfig(self, cluster_name: str | None = None) -> dict[str, Any]:
        """Build a kubeconfig dictionary for a running cluster.

        The returned mapping follows the kubectl kubeconfig schema and uses
        the ``gcp`` / ``gke-gcloud-auth-plugin`` auth provider. It can be
        serialised to YAML and written to disk by the caller.

        Args:
            cluster_name: Cluster name; defaults to the configured cluster.

        Returns:
            A kubeconfig-shaped dictionary.
        """
        cluster = self.get_cluster(cluster_name)
        name = cluster_name or self.settings.cluster_name
        context = f"gke_{self.settings.project_id}_{self.settings.location}_{name}"
        server = f"https://{getattr(cluster, 'endpoint', '')}"
        ca_cert = getattr(
            getattr(cluster, "master_auth", None), "cluster_ca_certificate", ""
        )
        return {
            "apiVersion": "v1",
            "kind": "Config",
            "current-context": context,
            "clusters": [
                {
                    "name": context,
                    "cluster": {
                        "server": server,
                        "certificate-authority-data": ca_cert,
                    },
                }
            ],
            "contexts": [
                {"name": context, "context": {"cluster": context, "user": context}}
            ],
            "users": [
                {
                    "name": context,
                    "user": {
                        "exec": {
                            "apiVersion": "client.authentication.k8s.io/v1beta1",
                            "command": "gke-gcloud-auth-plugin",
                            "provideClusterInfo": True,
                        }
                    },
                }
            ],
        }
