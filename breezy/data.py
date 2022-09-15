"""Data I/O."""

import numpy as np
import pandas as pd

from breezy.breezy_paths import data_dir


def cbioportal_kras_freq(cancer_type_inorder: bool = False) -> pd.DataFrame:
    """Read in cBioPortal KRAS mutation frequencies.

    These are the data from the TCGA projects.

    Args:
        cancer_type_inorder (bool, optional): Set the cancer types as a Categorical
        column in the order downloaded from cBioPortal. Defaults to False.

    Returns:
        pd.DataFrame: cBioPortal KRAS mutation frequencies.
    """
    df = pd.read_csv(data_dir() / "cbioportal-kras-mutation-frequency.csv")

    # Change "alteration type" names.
    diff_alt_types = {
        "amp": "amp.",
        "homdel": "homo. del.",
        "multiple": "multiple",
        "mutated": "mutated",
        "structuralVariant": "SV",
    }
    df["alteration_type"] = df["alteration_type"].map(diff_alt_types)
    df["alteration_type"] = pd.Categorical(
        df["alteration_type"], categories=list(diff_alt_types.values())
    )

    if cancer_type_inorder:
        cancer_order = df["cancer_type"].unique()
        df["cancer_type"] = pd.Categorical(df["cancer_type"], categories=cancer_order)
    return df


def _clean_source_name(x: str) -> str:
    return x.replace("_", " ").lower()


_clean_source_names = np.vectorize(_clean_source_name)


def gtex_expression_data(clean_source_names: bool = True) -> pd.DataFrame:
    """Read in GTEx KRAS expression data.

    Args:
        clean_source_names (bool, optional): Clean the names of the source of the
        expression data. Defaults to True.

    Returns:
        pd.DataFrame: GTEx KRAS expression data.
    """
    df = pd.read_csv(data_dir() / "gtex-expression.csv").rename(
        columns={"data": "expr", "tissue_site_detail_id": "source"}
    )
    if clean_source_names:
        df["source"] = _clean_source_names(df["source"])
    return df


def hpa_expression_data() -> pd.DataFrame:
    """Read in Human Protein Atlas expression data."""
    df = pd.read_csv(data_dir() / "human-protein-atlas-expression.csv")
    return df


def tabula_muris_data() -> pd.DataFrame:
    """Read Tabula Muris expression data."""
    df = (
        pd.read_csv(data_dir() / "tabula-muris.csv")
        .rename(columns={"kras_expression": "kras_expr"})
        .assign(
            kras_log_expr=lambda d: np.log10(d["kras_expr"] + 1.0),
            tissue=lambda d: _clean_source_names(d["tissue"]),
        )
    )
    return df
