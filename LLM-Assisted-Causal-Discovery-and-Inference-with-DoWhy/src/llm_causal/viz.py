"""Visualization helpers used by the teaching notebooks.

Uses lazy imports so that `import src.llm_causal` doesn't immediately fail in a
minimal environment. The teaching notebooks still require these dependencies.
"""

from __future__ import annotations

from collections.abc import Iterable


def draw_edge_list_dag(
    edges: Iterable[tuple[str, str] | list[str]],
    *,
    title: str = "LLM-Proposed DAG (semantic prior)",
    seed: int = 42,
    figsize: tuple[int, int] = (10, 7),
):
    """Draw a simple directed graph from an edge list."""

    try:
        import matplotlib.pyplot as plt
        import networkx as nx
    except Exception as e:  # noqa: BLE001
        raise ImportError(
            "Visualization helpers require 'matplotlib' and 'networkx'. "
            "Install via `pip install -r requirements.txt`."
        ) from e

    G = nx.DiGraph()
    G.add_edges_from([(a, b) for a, b in edges])

    plt.figure(figsize=figsize)
    pos = nx.spring_layout(G, seed=seed)
    nx.draw(G, pos, with_labels=True, node_size=2200, font_size=10, arrows=True)
    plt.title(title)
    plt.axis("off")
    plt.show()


def draw_pc_graph(
    directed_edges: list[tuple[str, str]],
    undirected_edges: list[tuple[str, str]],
    *,
    treatment: str = "treat",
    outcome: str = "re78",
    seed: int = 42,
):
    """Visualize PC output with directed and undirected/ambiguous edges."""

    try:
        import matplotlib.pyplot as plt
        import networkx as nx
    except Exception as e:  # noqa: BLE001
        raise ImportError(
            "Visualization helpers require 'matplotlib' and 'networkx'. "
            "Install via `pip install -r requirements.txt`."
        ) from e

    G_dir = nx.DiGraph()
    G_undir = nx.Graph()
    G_dir.add_edges_from(directed_edges)
    G_undir.add_edges_from(undirected_edges)

    all_nodes = set(G_dir.nodes()) | set(G_undir.nodes())
    G_all = nx.Graph()
    G_all.add_nodes_from(all_nodes)
    G_all.add_edges_from(undirected_edges)
    G_all.add_edges_from([(u, v) for (u, v) in directed_edges])

    pos = nx.spring_layout(G_all, seed=seed)

    def neighbors_of(node: str) -> set[str]:
        neigh = set()
        if node in G_all:
            neigh |= set(G_all.neighbors(node))
        return neigh

    def node_color(n: str) -> str:
        if n == treatment:
            return "#d62728"  # red
        if n == outcome:
            return "#2ca02c"  # green
        if n in neighbors_of(treatment) or n in neighbors_of(outcome):
            return "#ff7f0e"  # orange
        return "#1f77b4"  # blue

    def edge_width(u: str, v: str) -> float:
        return 3.5 if (u in (treatment, outcome) or v in (treatment, outcome)) else 2.0

    node_colors = [node_color(n) for n in G_all.nodes()]
    node_sizes = [2600 if n in (treatment, outcome) else 2000 for n in G_all.nodes()]

    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G_all, pos, node_color=node_colors, node_size=node_sizes)
    nx.draw_networkx_labels(G_all, pos, font_size=10)

    # Undirected/ambiguous edges (dashed gray)
    nx.draw_networkx_edges(
        G_undir,
        pos,
        edge_color="gray",
        style="dashed",
        width=[edge_width(u, v) for (u, v) in G_undir.edges()],
    )

    # Directed edges (solid arrows)
    highlight_edges: list[tuple[str, str]] = []
    normal_edges: list[tuple[str, str]] = []
    for (u, v) in G_dir.edges():
        if u == treatment and v == outcome:
            highlight_edges.append((u, v))
        else:
            normal_edges.append((u, v))

    nx.draw_networkx_edges(
        G_dir,
        pos,
        edgelist=normal_edges,
        edge_color="black",
        arrows=True,
        arrowsize=18,
        width=[edge_width(u, v) for (u, v) in normal_edges],
    )

    if highlight_edges:
        nx.draw_networkx_edges(
            G_dir,
            pos,
            edgelist=highlight_edges,
            edge_color="#1f77b4",
            arrows=True,
            arrowsize=22,
            width=[4.5 for _ in highlight_edges],
        )

    plt.title("PC output focused on treatment (red) and outcome (green)")
    plt.axis("off")
    plt.show()
