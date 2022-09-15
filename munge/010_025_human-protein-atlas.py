#!/usr/bin/env python3

"""Process data from the Human Protein Atlas (HPA)."""

import json
from typing import Any

import janitor  # noqa: F401
import pandas as pd
from rich import print as rprint
from typer import Typer

from breezy.breezy_paths import data_dir, raw_data_dir

app = Typer()

EXPR_DATA_OUTPUT = data_dir() / "human-protein-atlas-expression.csv"
METADATA_OUTPUT = data_dir() / "human-protein-atlas-metadata.json"


def msg(s: str) -> None:
    """Print a message."""
    rprint(f"[blue]{s}[/blue]")


def hpa_raw_data() -> pd.DataFrame:
    """Get the raw HPA data."""
    data_path = raw_data_dir() / "human-protein-atlas" / "kras.tsv"
    return pd.read_csv(data_path, sep="\t")


def parse_source_info(df: pd.DataFrame) -> pd.DataFrame:
    info = df["source"]
    data_type = [x.split(" - ")[0].strip() for x in info]
    source = [x.split(" - ")[1].split("[")[0].strip() for x in info]
    unit = [x.split("[")[1].split("]")[0] for x in info]
    df["data_type"] = data_type
    df["source"] = source
    df["unit"] = unit
    return df


def process_expression_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process expression data from HPA."""
    return (
        df.pivot_longer("Gene", names_to="source", values_to="expr")
        .pipe(parse_source_info)
        .clean_names()[["gene", "data_type", "source", "unit", "expr"]]
    )


def process_metadata(df: pd.DataFrame) -> dict[str, Any]:
    """Process the meta data from HPA."""
    df = df.pivot_longer()
    return {k: v for k, v in zip(df["variable"], df["value"])}


@app.command()
def main() -> None:
    msg("Preparing Human Protein Atlas data for KRAS.")
    hpa_data = hpa_raw_data()
    hpa_data = hpa_data.query("Gene == 'KRAS'").drop(
        columns=["Gene synonym", "Ensembl"]
    )
    assert len(hpa_data) == 1, "Too many results for KRAS."
    FIRST_COL = "Tissue RNA - adipose tissue [nTPM]"
    cols = list(hpa_data.columns)
    split_idx = cols.index(FIRST_COL)
    expr_data = process_expression_data(hpa_data[["Gene"] + cols[split_idx:]])
    meta_data = process_metadata(hpa_data[cols[:split_idx]])
    msg(f"Saving expression data to '{EXPR_DATA_OUTPUT}'.")
    expr_data.to_csv(EXPR_DATA_OUTPUT, index=False)
    msg(f"Saving meta data data to '{METADATA_OUTPUT}'.")
    with open(METADATA_OUTPUT, "w") as fp:
        json.dump(meta_data, fp)


if __name__ == "__main__":
    app()
