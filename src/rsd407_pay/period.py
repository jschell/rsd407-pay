"""Accepted coverage; promotion requires synchronized retained inputs."""
import json
import re
from pathlib import Path


def accepted_years(config_path="config/sources.json"):
    years = json.loads(Path(config_path).read_text())["expected_final_years"]
    if not years or any(not re.fullmatch(r"20\d{2}-\d{2}", y) or
                        int(y[-2:]) != (int(y[:4]) + 1) % 100 for y in years):
        raise RuntimeError("invalid accepted school years")
    if years != sorted(set(years)) or any(int(b[:4]) != int(a[:4]) + 1
                                        for a, b in zip(years, years[1:])):
        raise RuntimeError("accepted years must be unique, ordered and contiguous")
    return years


def require_coverage(rows, years, label):
    observed = [r["school_year"] for r in rows]
    if sorted(observed) != sorted(years):
        raise RuntimeError(f"{label}: expected exact coverage {years}, got {observed}")


YEARS = accepted_years()
