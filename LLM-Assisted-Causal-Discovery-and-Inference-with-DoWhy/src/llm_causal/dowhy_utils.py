"""Small helpers to keep DoWhy graph-building readable in notebooks."""

from __future__ import annotations


def build_backdoor_dot_graph(
    adjust: list[str],
    *,
    treatment: str = "treat",
    outcome: str = "re78",
) -> str:
    """Build a conservative backdoor-adjustment DOT graph for DoWhy."""

    dot_lines = ["digraph {"]
    for v in adjust:
        dot_lines.append(f"  {v} -> {treatment};")
        dot_lines.append(f"  {v} -> {outcome};")
    dot_lines.append(f"  {treatment} -> {outcome};")
    dot_lines.append("}")
    return "\n".join(dot_lines)
