from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from .workbook import validate_workbook_bytes


def normalized_headers(identity: dict) -> list[str]:
    return [str(value).strip().lower() for value in identity["headers"]]


def duplicate_headers(headers: list[str]) -> dict[str, int]:
    counts = Counter(headers)
    return {name: count for name, count in counts.items() if name and count > 1}


def schema_family(headers: list[str]) -> str:
    values = set(headers)
    if {"location code", "building location name", "sex", "hispanic", "race", "highest degree", "cert yrs exp"}.issubset(values):
        return "2022-plus"
    return "legacy-core"


def inventory_manifest(manifest: dict) -> dict:
    years = []
    for source in manifest["sources"]:
        identity = source.get("workbook_identity")
        if not identity:
            raise RuntimeError(f"{source['school_year']}: missing workbook_identity")
        headers = normalized_headers(identity)
        years.append(
            {
                "school_year": source["school_year"],
                "format": identity["format"],
                "sheet": identity["sheet"],
                "schema_family": schema_family(headers),
                "header_count": len(headers),
                "duplicate_headers": duplicate_headers(headers),
                "headers": headers,
                "sha256": source["sha256"],
            }
        )
    return {"schema_version": 1, "years": years}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inventory validated S-275 workbook schemas")
    parser.add_argument("--manifest", default="artifacts/manifests/collection.json")
    parser.add_argument("--output", default="artifacts/schema-inventory.json")
    args = parser.parse_args(argv)
    manifest = json.loads(Path(args.manifest).read_text())
    inventory = inventory_manifest(manifest)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(inventory, indent=2) + "\n")
    print(f"inventoried {len(inventory['years'])} S-275 schema(s): {output}")


if __name__ == "__main__":
    main()
