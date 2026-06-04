"""
Data Loader for ZebraLogicBench
https://huggingface.co/datasets/allenai/ZebraLogicBench
"""
import json
import re
from pathlib import Path


def load_dataset(path: str = None) -> list:
    """Load puzzles from local JSONL or HuggingFace."""
    if path and Path(path).exists():
        with open(path) as f:
            return [json.loads(l) for l in f if l.strip()]
    try:
        from datasets import load_dataset as hf_load
        return list(hf_load("allenai/ZebraLogicBench", split="test"))
    except ImportError:
        raise ImportError("pip install datasets")


def puzzle_to_csp(puzzle: dict):
    """Parse a puzzle dict into (variables, domains, constraints)."""
    num_houses = puzzle.get("num_houses", 5)
    attributes = puzzle.get("attributes", {})

    variables, domains = [], {}
    for attr, values in attributes.items():
        for i in range(1, num_houses + 1):
            var = f"house_{i}_{attr}"
            variables.append(var)
            domains[var] = list(values)

    constraints = []
    # All-different within each attribute
    for attr in attributes:
        attr_vars = [f"house_{i}_{attr}" for i in range(1, num_houses + 1)]
        for j, v1 in enumerate(attr_vars):
            for v2 in attr_vars[j+1:]:
                constraints.append((v1, v2, lambda a, b: a != b))

    for clue in puzzle.get("clues", []):
        constraints.extend(_parse_clue(clue, num_houses))

    return variables, domains, constraints


def _parse_clue(clue: str, num_houses: int) -> list:
    """Basic natural-language clue parser. Extend for full coverage."""
    constraints = []
    m = re.search(r'house (\d+).*?(\w+) is (\w+)', clue, re.IGNORECASE)
    if m:
        house_n, attr, value = m.group(1), m.group(2).lower(), m.group(3).lower()
        var = f"house_{house_n}_{attr}"
        v = value
        constraints.append((var, var, lambda a, b, _v=v: a == _v))
    return constraints
