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


@mkdir
def figures_dir() -> Path:
    """Figures directory."""
    return root() / "figures"


@mkdir
def figure_dir(num: int, ver: int) -> Path:
    """Directory for a figure."""
    return figures_dir() / f"figure_{num:03d}-v{ver:03d}"


def figure_img_file(num: int, ver: int, name: str) -> Path:
    """Path for a figure image file."""
    return figure_dir(num, ver) / f"fig_{num:03d}-v{ver:03d}_{name}.png"


@mkdir
def dissertation_figure_stylesheet() -> Path:
    """Path to the stylesheet for figures."""
    return figures_dir() / "dissertation.mplstyle"
