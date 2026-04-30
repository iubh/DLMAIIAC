"""Utilities for causal-learn's PC output for teaching notebooks.

This module uses *lazy imports* so that importing `src.llm_causal` does not
immediately fail in environments where optional dependencies aren't installed.
The notebook itself still requires these dependencies to run the PC section.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


def run_pc(
    df: pd.DataFrame,
    *,
    alpha: float = 0.05,
) -> tuple[Any, pd.DataFrame]:
    """Run PC on the numeric columns of a dataframe (teaching-friendly defaults).

    Notes:
    - Ensures `treat` is int if present (some versions treat bool strangely).
    - Standard-scales numeric columns.
    """

    try:
        import numpy as np
        from causallearn.search.ConstraintBased.PC import pc
        from sklearn.preprocessing import StandardScaler
    except Exception as e:  # noqa: BLE001
        raise ImportError(
            "PC helpers require 'causal-learn', 'numpy', and 'scikit-learn'. "
            "Install via `pip install -r requirements.txt`."
        ) from e

    df_pc = df.copy()
    if "treat" in df_pc.columns:
        df_pc["treat"] = df_pc["treat"].astype(int)

    numeric_df = df_pc.select_dtypes(include=[np.number]).copy().dropna(axis=0)
    X = StandardScaler().fit_transform(numeric_df.values)
    cg = pc(X, alpha=alpha, node_names=list(numeric_df.columns))
    return cg, numeric_df


def pc_graph_to_edge_lists(cg: Any) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Split a causal-learn PC result into directed and undirected edges."""

    try:
        from causallearn.graph.Endpoint import Endpoint
    except Exception as e:  # noqa: BLE001
        raise ImportError(
            "pc_graph_to_edge_lists requires 'causal-learn'. "
            "Install via `pip install -r requirements.txt`."
        ) from e

    directed_edges: list[tuple[str, str]] = []
    undirected_edges: set[tuple[str, str]] = set()
    for edge in cg.G.get_graph_edges():
        n1 = edge.get_node1().get_name()
        n2 = edge.get_node2().get_name()
        ep1 = edge.get_endpoint1()
        ep2 = edge.get_endpoint2()

        if ep1 == Endpoint.TAIL and ep2 == Endpoint.ARROW:
            directed_edges.append((n1, n2))
        elif ep1 == Endpoint.ARROW and ep2 == Endpoint.TAIL:
            directed_edges.append((n2, n1))
        else:
            undirected_edges.add(tuple(sorted((n1, n2))))

    return directed_edges, sorted(undirected_edges)
