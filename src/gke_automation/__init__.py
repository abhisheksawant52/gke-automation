"""gke-automation: typed automation toolkit for Google Kubernetes Engine.

This package wraps the Google Cloud ``container_v1`` API with a small,
strongly typed manager and a Click-based command-line interface for the
day-to-day lifecycle of GKE clusters and node pools.
"""

from __future__ import annotations

__version__ = "0.1.0"

from gke_automation.config import Settings, get_settings
from gke_automation.manager import GKEManager

__all__ = ["GKEManager", "Settings", "get_settings", "__version__"]
