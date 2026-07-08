"""Logging configuration for gke-automation."""

from __future__ import annotations

import logging

_CONFIGURED = False
_LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


def configure_logging(level: str = "INFO") -> None:
    """Configure the root logger once for the package.

    Args:
        level: Logging level name (e.g. ``"INFO"`` or ``"DEBUG"``).
    """
    global _CONFIGURED
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    if _CONFIGURED:
        logging.getLogger().setLevel(numeric_level)
        return
    logging.basicConfig(level=numeric_level, format=_LOG_FORMAT)
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger for the given module.

    Args:
        name: Usually ``__name__`` of the calling module.

    Returns:
        A :class:`logging.Logger` scoped under ``gke_automation``.
    """
    return logging.getLogger(f"gke_automation.{name}")
