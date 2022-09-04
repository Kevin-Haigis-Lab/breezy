"""Paths for the project."""

from pathlib import Path

from breezy.utilities import mkdir


def root() -> Path:
    """Project root."""
    return Path(__file__).parent.parent


@mkdir
def cache_dir() -> Path:
    """Cache directory."""
    return root() / "cache"


@mkdir
def data_dir() -> Path:
    """Data directory."""
    return root() / "data"


@mkdir
def raw_data_dir() -> Path:
    """Raw data directory."""
    return root() / "data-raw"


@mkdir
def munge_dir() -> Path:
    """Munge directory."""
    return root() / "munge"


@mkdir
def notebooks_dir() -> Path:
    """Notebooks directory."""
    return root() / "notebooks"


@mkdir
def tables_dir() -> Path:
    """Tables directory."""
    return root() / "tables"
