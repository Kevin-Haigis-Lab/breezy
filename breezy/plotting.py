"""Project plotting."""

from enum import Enum
from typing import Any, Collection, Hashable, TypeVar

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from breezy.breezy_paths import dissertation_figure_stylesheet

H = TypeVar("H", bound=Hashable)
RGBA = tuple[float, float, float, float]

# --- Color palettes ---


def filter_pal(pal: dict[H, str], keys: Collection[H]) -> dict[H, str]:
    """Filter a palette with a set of keys."""
    return {k: v for k, v in pal.items() if k in keys}


def pal_to_legend_handles(
    pal: dict[str, str], leg_key: str = "color", **kwargs: Any
) -> list[Line2D]:
    """Convert a color palette to handles for a matplotlib legend.

    Extra keyword arguments are passed to `matplotlib.lines.Line2D()`.

    Args:
        pal (dict[str, str]): Color palette.

    Returns:
        list[Line2D]: Matplotlib legend handles.
    """
    handles: list[Line2D] = []
    for label, value in pal.items():
        kwargs[leg_key] = value
        handles.append(Line2D([0], [0], label=label, **kwargs))
    return handles


def align_legend_title(leg: mpl.legend.Legend, ha: str = "left") -> None:
    """Change horizontal alignment of a legend title."""
    leg._legend_box.align = ha


# --- Plot themes ---


class PlottingMode(str, Enum):
    """Specific plotting modes."""

    DEFAULT = "DEFAULT"
    DISSERTATION = "DISSERTATION"
    PAPER = "PAPER"


def set_breezy_theme(mode: PlottingMode | str = PlottingMode.DEFAULT) -> None:
    """Set the plot theme to the 'breezy' project theme."""
    if isinstance(mode, str):
        mode = PlottingMode(mode)

    plt.style.use(["seaborn-whitegrid"])
    if mode is PlottingMode.DISSERTATION:
        plt.style.use(dissertation_figure_stylesheet())
    return None
