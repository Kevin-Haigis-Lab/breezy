"""Miscellaneous utilities."""

import functools
from pathlib import Path
from typing import Any, Callable, NoReturn


def assert_never(value: NoReturn) -> NoReturn:
    """Force runtime and static enumeration exhaustiveness.

    Args:
        value (NoReturn): Some value passed as an enum value.

    Returns:
        NoReturn: Nothing.
    """
    assert False, f"Unhandled value: {value} ({type(value).__name__})"  # noqa: B011


def mkdir(func: Callable[..., Path]) -> Callable[..., Path]:
    """Function decorator that creates the directory returned by the function."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Path:
        d = func(*args, **kwargs)
        if not d.exists():
            d.mkdir()
        return d

    return wrapper
