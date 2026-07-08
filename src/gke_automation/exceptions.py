"""Exception hierarchy for gke-automation."""

from __future__ import annotations


class GKEAutomationError(Exception):
    """Base class for all errors raised by this package."""


class ClusterNotFoundError(GKEAutomationError):
    """Raised when a requested cluster does not exist."""


class NodePoolNotFoundError(GKEAutomationError):
    """Raised when a requested node pool does not exist."""


class InvalidConfigurationError(GKEAutomationError):
    """Raised when the supplied configuration is inconsistent."""
