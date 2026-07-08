"""Command-line interface for gke-automation.

Exposes a ``gke-automate`` command with subcommands mirroring the
:class:`~gke_automation.manager.GKEManager` operations. The CLI is a thin
wrapper: it constructs a manager from the environment-backed settings and
prints the results of each operation.
"""

from __future__ import annotations

import json

import click

from gke_automation import __version__
from gke_automation.config import get_settings
from gke_automation.logging_config import configure_logging, get_logger
from gke_automation.manager import GKEManager
from gke_automation.models import ClusterSpec, NodePoolSpec

logger = get_logger(__name__)


def _manager() -> GKEManager:
    """Build a manager from the active settings."""
    settings = get_settings()
    configure_logging(settings.log_level)
    return GKEManager(settings=settings)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="gke-automate")
def cli() -> None:
    """Automate the lifecycle of Google Kubernetes Engine clusters."""


@cli.command()
@click.option("--name", help="Cluster name (defaults to configured cluster).")
@click.option("--node-count", type=int, help="Initial node count.")
@click.option("--machine-type", help="Compute Engine machine type.")
def create(name: str | None, node_count: int | None, machine_type: str | None) -> None:
    """Create a new GKE cluster."""
    manager = _manager()
    settings = manager.settings
    spec = ClusterSpec(
        name=name or settings.cluster_name,
        node_count=node_count or settings.node_count,
        machine_type=machine_type or settings.machine_type,
        release_channel=settings.release_channel,
    )
    operation = manager.create_cluster(spec)
    click.echo(f"Cluster creation started: {getattr(operation, 'name', operation)}")


@cli.command(name="list")
def list_clusters() -> None:
    """List clusters in the configured project/location."""
    manager = _manager()
    clusters = manager.list_clusters()
    if not clusters:
        click.echo("No clusters found.")
        return
    for cluster in clusters:
        status = getattr(cluster, "status", "UNKNOWN")
        click.echo(f"{getattr(cluster, 'name', '?')}\t{status}")


@cli.command()
@click.option("--name", help="Cluster name (defaults to configured cluster).")
def describe(name: str | None) -> None:
    """Describe a single cluster."""
    manager = _manager()
    cluster = manager.get_cluster(name)
    click.echo(
        json.dumps(
            {
                "name": getattr(cluster, "name", None),
                "location": getattr(cluster, "location", None),
                "status": getattr(cluster, "status", None),
                "node_count": getattr(cluster, "current_node_count", None),
                "master_version": getattr(cluster, "current_master_version", None),
            },
            indent=2,
            default=str,
        )
    )


@cli.command()
@click.option("--name", help="Cluster name (defaults to configured cluster).")
@click.confirmation_option(prompt="Are you sure you want to delete this cluster?")
def delete(name: str | None) -> None:
    """Delete a GKE cluster."""
    manager = _manager()
    operation = manager.delete_cluster(name)
    click.echo(f"Cluster deletion started: {getattr(operation, 'name', operation)}")


@cli.command()
@click.option("--node-pool", default="default-pool", show_default=True)
@click.option("--node-count", type=int, required=True, help="Desired node count.")
@click.option("--name", help="Cluster name (defaults to configured cluster).")
def resize(node_pool: str, node_count: int, name: str | None) -> None:
    """Resize a node pool to a fixed node count."""
    manager = _manager()
    operation = manager.resize_node_pool(node_pool, node_count, name)
    click.echo(f"Resize started: {getattr(operation, 'name', operation)}")


@cli.command()
@click.option("--version", "target_version", required=True, help="Target k8s version.")
@click.option("--name", help="Cluster name (defaults to configured cluster).")
def upgrade(target_version: str, name: str | None) -> None:
    """Upgrade the control-plane version of a cluster."""
    manager = _manager()
    operation = manager.update_master_version(target_version, name)
    click.echo(f"Upgrade started: {getattr(operation, 'name', operation)}")


@cli.command(name="node-pool")
@click.option("--node-pool", required=True, help="Node pool name.")
@click.option("--min-nodes", type=int, required=True)
@click.option("--max-nodes", type=int, required=True)
@click.option("--name", help="Cluster name (defaults to configured cluster).")
def node_pool(node_pool: str, min_nodes: int, max_nodes: int, name: str | None) -> None:
    """Create an autoscaling node pool on a cluster."""
    manager = _manager()
    spec = NodePoolSpec(
        name=node_pool,
        machine_type=manager.settings.machine_type,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
    )
    operation = manager.create_node_pool(spec, name)
    click.echo(f"Node pool creation started: {getattr(operation, 'name', operation)}")


@cli.command()
@click.option("--name", help="Cluster name (defaults to configured cluster).")
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False, writable=True),
    help="Write kubeconfig to this file instead of stdout.",
)
def kubeconfig(name: str | None, output: str | None) -> None:
    """Render a kubeconfig for a cluster."""
    manager = _manager()
    config = manager.get_kubeconfig(name)
    payload = json.dumps(config, indent=2, default=str)
    if output:
        with open(output, "w", encoding="utf-8") as handle:
            handle.write(payload)
        click.echo(f"Wrote kubeconfig to {output}")
    else:
        click.echo(payload)


def main() -> None:
    """Console-script entrypoint."""
    cli()


if __name__ == "__main__":
    main()
