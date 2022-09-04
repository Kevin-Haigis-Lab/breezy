#!/usr/bin/env python3

"""Process data from the Human Protein Atlas (HPA)."""

import janitor  # noqa: F401
import pandas as pd
from rich import print as rprint
from typer import Typer

from breezy.breezy_paths import data_dir, raw_data_dir

app = Typer()


def msg(s: str) -> None:
    """Print a message."""
    rprint(f"[blue]{s}[/blue]")


def _read_raw_data() -> pd.DataFrame:
    fp = raw_data_dir() / "cbioportal" / "cbioportal-data_tcga-KRAS-mutations.txt"
    return pd.read_csv(fp, sep="\t")


@app.command()
def main() -> None:
    msg("Processing cBioPortal KRAS mutation frequency.")
    output_fp = data_dir() / "cbioportal-kras-mutation-frequency.csv"
    _read_raw_data().clean_names().to_csv(output_fp)
    msg(f"Saving to '{output_fp}'.")


if __name__ == "__main__":
    app()
