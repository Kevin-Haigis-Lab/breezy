#!/usr/bin/env python3

"""Collect data from GTEx."""

import json
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from pydantic import BaseModel
from rich import print as rprint
from typer import Typer

from breezy.breezy_paths import cache_dir, data_dir

REQUEST_URL = "https://gtexportal.org/rest/v1/expression/geneExpression"
REQUEST_INFO = {
    "datasetId": "gtex_v8",
    "gencodeId": "ENSG00000133703.11",
    "format": "json",
}

app = Typer()


def _to_camel(string: str) -> str:
    camels = [word.capitalize() for word in string.split("_")]
    camels[0] = camels[0].lower()
    return "".join(camels)


class GtexExpressionData(BaseModel):
    """GTEx expression data."""

    data: list[float]
    dataset_id: str
    gencode_id: str
    gene_symbol: str
    tissue_site_detail_id: str
    unit: str

    class Config:
        """Configuration."""

        alias_generator = _to_camel


class GtexExpressionDataResponse(BaseModel):
    """GTEx expression data request response."""

    gene_expression: list[GtexExpressionData]

    class Config:
        """Configuration."""

        alias_generator = _to_camel


def info(s: str) -> None:
    """Print info."""
    rprint(f"[grey]{s}[/grey]")


def msg(s: str) -> None:
    """Print a message."""
    rprint(f"[blue]{s}[/blue]")


def _write_cache(res: requests.Response, path: Path) -> None:
    with open(path, "w") as fp:
        json.dump(res.json(), fp)


def _get_cache(path: Path) -> dict[str, Any]:
    with open(path, "r") as fp:
        return json.load(fp)


def make_gtex_request(ignore_cache: bool) -> GtexExpressionDataResponse:
    """Make the request to GTEx and cache results."""
    _cache_path = cache_dir() / "kras-expr-cache.json"
    if _cache_path.exists() and not ignore_cache:
        rprint("[grey]Using cached data.[/grey]")
        return GtexExpressionDataResponse(**_get_cache(_cache_path))
    else:
        rprint("[grey]Requesting data from GTEx API.[/grey]")
        res = requests.get(REQUEST_URL, params=REQUEST_INFO)
        res.raise_for_status()
        rprint(f"[grey]Request status code: {res.status_code}.[/grey]")
        _write_cache(res, _cache_path)
        return GtexExpressionDataResponse(**res.json())


def expression_data_to_data_frame(
    expr_data: GtexExpressionDataResponse,
) -> pd.DataFrame:
    """Convert expression data into a data frame."""
    dfs: list[pd.DataFrame] = []
    info(f"Coalescing data from {len(expr_data.gene_expression)} sources.")
    for expr in expr_data.gene_expression:
        dfs.append(pd.DataFrame(expr.dict()))
    expr_df = pd.concat(dfs).reset_index(drop=True)
    info(f"Number of data points: {len(expr_df)}")
    return expr_df


@app.command()
def main(ignore_cache: bool = False) -> None:
    output_file = data_dir() / "gtex-expression.csv"
    msg("Acquiring GTEx data.")
    expr_data = make_gtex_request(ignore_cache)
    msg("Converting to a pandas DataFrame.")
    expression_data_to_data_frame(expr_data).to_csv(output_file, index=False)
    msg(f"Saved output to {data_dir().name}/{output_file.name}.")


if __name__ == "__main__":
    app()
