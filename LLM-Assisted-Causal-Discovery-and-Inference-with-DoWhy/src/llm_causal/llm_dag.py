"""LLM-assisted DAG proposal utilities.

This is designed for *teaching notebooks*:
- call an OpenAI-compatible local server (Ollama / LM Studio)
- request a DAG edge list in JSON
- optionally request a short per-edge reason
- robustly parse the output and fall back when the server isn't available
"""

from __future__ import annotations

import json
from typing import Any

from .json_parsing import extract_first_json_object


FALLBACK_DAG_WITH_REASONS: dict[str, Any] = {
    "edges": [
        {"cause": "educ", "effect": "treat", "reason": "No LLM reasoning."},
        {"cause": "educ", "effect": "re78", "reason": "No LLM reasoning."},
        {"cause": "re74", "effect": "treat", "reason": "No LLM reasoning."},
        {"cause": "re75", "effect": "treat", "reason": "No LLM reasoning."},
        {"cause": "re74", "effect": "re78", "reason": "No LLM reasoning."},
        {"cause": "re75", "effect": "re78", "reason": "No LLM reasoning."},
        {"cause": "treat", "effect": "re78", "reason": "No LLM reasoning."},
    ]
}


def build_prompt_with_reasons(base_prompt: str) -> str:
    """Extend a base prompt to request edge reasons in a strict JSON schema."""

    return (
        base_prompt
        + """

Additional requirement:
- For each proposed edge, include a short reason (1 sentence).
- Output ONLY JSON (no markdown).

Return JSON in this exact format:
{
  \"edges\": [
    {\"cause\": \"educ\", \"effect\": \"treat\", \"reason\": \"Education influences selection into training.\"},
    {\"cause\": \"treat\", \"effect\": \"re78\", \"reason\": \"Training affects future earnings.\"}
  ]
}
"""
    )


def call_openai_compatible_chat(
    *,
    client: Any,
    model: str,
    prompt: str,
    temperature: float = 0.2,
) -> str | None:
    """Call an OpenAI-compatible chat completion endpoint.

    Returns the message content or None if the request fails.
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:  # noqa: BLE001 (teaching demo, we want broad fallback)
        print("Local LLM not available (or request failed). Using fallback response.")
        print("Error:", repr(e))
        return None


def parse_edges_with_reasons(
    text: str,
) -> tuple[list[tuple[str, str]], dict[tuple[str, str], str]]:
    """Parse extended-schema JSON into (edge_list, reason_map)."""

    raw_json = extract_first_json_object(text)
    obj = json.loads(raw_json)
    if not isinstance(obj, dict) or "edges" not in obj or not isinstance(obj["edges"], list):
        raise ValueError("Expected an object like {\"edges\": [...] }.")

    edge_list: list[tuple[str, str]] = []
    reason_map: dict[tuple[str, str], str] = {}
    for item in obj["edges"]:
        if not isinstance(item, dict):
            continue
        cause = item.get("cause")
        effect = item.get("effect")
        reason = item.get("reason", "")
        if isinstance(cause, str) and isinstance(effect, str):
            edge = (cause, effect)
            edge_list.append(edge)
            if isinstance(reason, str) and reason.strip():
                reason_map[edge] = reason.strip()

    if not edge_list:
        raise ValueError("No valid edges found in extended schema.")
    return edge_list, reason_map


def parse_edges_from_llm_output(text: str) -> list[list[str]]:
    """Parse an LLM response into an edge list.

    Supports two schemas:
      1) {"edges": [[cause, effect], ...]}
      2) {"edges": [{"cause": ..., "effect": ..., "reason": ...}, ...]}
    """

    raw_json = extract_first_json_object(text)
    obj = json.loads(raw_json)

    if not isinstance(obj, dict) or "edges" not in obj:
        raise ValueError("Parsed JSON must be an object with a top-level key `edges`.")

    edges = obj["edges"]
    if edges and isinstance(edges, list) and isinstance(edges[0], dict):
        converted: list[list[str]] = []
        for item in edges:
            if (
                isinstance(item, dict)
                and isinstance(item.get("cause"), str)
                and isinstance(item.get("effect"), str)
            ):
                converted.append([item["cause"], item["effect"]])
        edges = converted

    if not isinstance(edges, list):
        raise ValueError("`edges` must be a list.")

    cleaned: list[list[str]] = []
    for e in edges:
        if (
            isinstance(e, (list, tuple))
            and len(e) == 2
            and isinstance(e[0], str)
            and isinstance(e[1], str)
        ):
            cleaned.append([e[0], e[1]])

    if not cleaned:
        raise ValueError("No valid edges found. Expected pairs like ['educ', 'treat'].")

    return cleaned


def propose_dag_with_reasons(
    *,
    client: Any,
    model: str,
    prompt_with_reasons: str,
    fallback_dag_with_reasons: dict[str, Any] | None = None,
) -> tuple[str, list[list[str]], dict[tuple[str, str], str]]:
    """Request a DAG in extended JSON schema and parse it.

    Returns:
      raw_text: model output (or fallback JSON)
      edges: list of [cause, effect] pairs
      reason_map: mapping (cause, effect) -> short reason
    """

    raw_text = call_openai_compatible_chat(client=client, model=model, prompt=prompt_with_reasons)
    if raw_text is None:
        fallback_obj = fallback_dag_with_reasons or FALLBACK_DAG_WITH_REASONS
        raw_text = json.dumps(fallback_obj, indent=2)

    edges_tuples, reason_map = parse_edges_with_reasons(raw_text)
    edges = [[a, b] for (a, b) in edges_tuples]
    return raw_text, edges, reason_map
