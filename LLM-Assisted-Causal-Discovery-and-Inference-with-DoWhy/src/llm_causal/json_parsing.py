"""Robust extraction helpers for LLM outputs.

Local LLMs often wrap JSON in markdown code fences or add extra text.
For a teaching workflow, we prefer tolerant parsing with clear errors.
"""

from __future__ import annotations


def strip_code_fences(text: str) -> str:
    """Remove a single surrounding triple-backtick code fence if present."""

    text = text.strip()
    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()
        if len(lines) >= 2:
            return "\n".join(lines[1:-1]).strip()
    return text


def extract_first_json_object(text: str) -> str:
    """Extract the first balanced {...} JSON object from arbitrary text."""

    text = strip_code_fences(text)
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON object start `{` found.")

    depth = 0
    in_string = False
    escape = False

    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue

        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]

    raise ValueError("Found `{` but could not find a matching closing `}`.")
