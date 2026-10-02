from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from .normalize import norm_header
from .pipeline import iter_workbook


CODE_HEADER_TERMS = ("duty", "assignment", "position", "activity", "job", "code")


def candidate_headers(headers):
    return [
        {"index": i, "header": str(h or ""), "normalized": norm_header(h)}
        for i, h in enumerate(headers)
        if any(term in norm_header(h) for term in CODE_HEADER_TERMS)
    ]


def inventory_source(source):
    path = Path(source["local_path"])
    sheets = {}
    for sheet, _row_no, headers, _values in iter_workbook(path):
        if sheet not in sheets:
            sheets[sheet] = candidate_headers(headers)
    return {
        "school_year": source["school_year"],
        "sha256": source["sha256"],
        "sheets": [{"sheet": name, "candidate_headers": values} for name, values in sheets.items()],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Inventory S-275 duty/assignment code header candidates")
    ap.add_argument("--manifest", default="artifacts/manifests/collection.json")
    ap.add_argument("--output", default="artifacts/normalized/duty-code-header-inventory.json")
    args = ap.parse_args(argv)
    manifest = json.loads(Path(args.manifest).read_text())
    result = {
        "schema_version": 1,
        "purpose": "Plan 04 duty/assignment identifier discovery; candidates are not mappings",
        "years": [inventory_source(source) for source in manifest["sources"]],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"wrote duty-code header inventory for {len(result['years'])} year(s): {output}")


if __name__ == "__main__":
    main()
