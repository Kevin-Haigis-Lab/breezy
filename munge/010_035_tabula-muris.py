#!/usr/bin/env python3

"""Process data from the Human Protein Atlas (HPA)."""

import janitor  # noqa: F401
import pandas as pd
from rich import print as rprint
from typer import Typer

from breezy.breezy_paths import data_dir, raw_data_dir

app = Typer()


def _read_raw_data() -> pd.DataFrame:
    fp = raw_data_dir() / "tabula-muris" / "TabulaMuris_KrasExpression_PerCell.csv"
    return pd.read_csv(fp)


@app.command()
def main() -> None:
    rprint("Preparing Tabula Muris data.")
    _output_fp = data_dir() / "tabula-muris.csv"
    (
        _read_raw_data()
        .rename(columns={"Unnamed: 0": "cell_id"})
        .clean_names()
        .to_csv(_output_fp, index=None)
    )
    rprint(f"Done. Saved to '{_output_fp}'")
    return None


if __name__ == "__main__":
    app()
