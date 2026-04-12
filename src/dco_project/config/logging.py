"""Logging helpers for the DCO project.

Notes
-----
Contains small wrappers for consistent logger creation across modules.
"""

from __future__ import annotations

import logging


def setup_logging(level: str = "INFO") -> None:
    """Configure root logging once for the whole application.

    Parameters
    ----------
    level : str, default="INFO"
        Logging level name (for example: ``"DEBUG"``, ``"INFO"``).
    """
    root = logging.getLogger()
    log_level = getattr(logging, level.upper(), logging.INFO)

    if root.handlers:
        root.setLevel(log_level)
        return

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    """Return module logger with unified naming.

    Parameters
    ----------
    name : str
        Logger name (usually ``__name__``).

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    return logging.getLogger(name)
