"""Helpers for the teaching notebooks.

This package intentionally contains *notebook-facing* utilities:
- robust parsing of local-LLM JSON-ish outputs
- a thin wrapper to call OpenAI-compatible local servers (Ollama/LM Studio)
- lightweight causal discovery helpers (PC) and visualization

The goal is readability in notebooks, not a full causal-discovery library.
"""

from .dowhy_utils import build_backdoor_dot_graph
from .llm_dag import (
    build_prompt_with_reasons,
    parse_edges_from_llm_output,
    propose_dag_with_reasons,
)
from .pc_utils import pc_graph_to_edge_lists, run_pc
from .viz import draw_edge_list_dag, draw_pc_graph

__all__ = [
    "build_backdoor_dot_graph",
    "build_prompt_with_reasons",
    "parse_edges_from_llm_output",
    "propose_dag_with_reasons",
    "pc_graph_to_edge_lists",
    "run_pc",
    "draw_edge_list_dag",
    "draw_pc_graph",
]
