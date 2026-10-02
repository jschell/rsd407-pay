from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def build_coverage(rows):
    by_title = {}
    by_year = defaultdict(dict)
    for row in rows:
        title = (row.get("duty_title") or "").strip() or "__MISSING__"
        cert = float(row.get("certificated_fte") or 0)
        clas = float(row.get("classified_fte") or 0)
        item = by_title.setdefault(title, {"rows": 0, "certificated_fte": 0.0, "classified_fte": 0.0, "years": set()})
        item["rows"] += 1
        item["certificated_fte"] += cert
        item["classified_fte"] += clas
        item["years"].add(row["school_year"])
        annual = by_year[row["school_year"]].setdefault(title, {"rows": 0, "certificated_fte": 0.0, "classified_fte": 0.0})
        annual["rows"] += 1
        annual["certificated_fte"] += cert
        annual["classified_fte"] += clas
    return {
        "titles": {title: {**{k: v for k, v in item.items() if k != "years"}, "years": sorted(item["years"])} for title, item in sorted(by_title.items())},
        "years": {year: dict(sorted(titles.items())) for year, titles in sorted(by_year.items())},
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Report exact RSD407 S-275 duty-title vocabulary and FTE coverage")
    ap.add_argument("--input", default="artifacts/normalized/rsd407.csv")
    ap.add_argument("--output", default="artifacts/normalized/duty-title-coverage.json")
    ap.add_argument("--vocabulary-output", default=None)
    args = ap.parse_args(argv)
    with Path(args.input).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    report = build_coverage(rows)
    report["schema_version"] = 1
    report["source"] = args.input
    report["distinct_titles"] = len(report["titles"])
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    if args.vocabulary_output:
        vocabulary = {
            "schema_version": 1,
            "source_snapshot": "s275-source-2026-10-02",
            "distinct_titles": report["distinct_titles"],
            "titles": list(report["titles"]),
        }
        vocab_path = Path(args.vocabulary_output)
        vocab_path.parent.mkdir(parents=True, exist_ok=True)
        vocab_path.write_text(json.dumps(vocabulary, indent=2) + "\n")

    print(f"wrote {report['distinct_titles']} exact duty title(s): {output}")
    print("Exact OSPI Duty Title coverage:")
    for title, item in report["titles"].items():
        total_fte = item["certificated_fte"] + item["classified_fte"]
        print(f"- {title}: rows={item['rows']}, certificated_fte={item['certificated_fte']:.4f}, classified_fte={item['classified_fte']:.4f}, total_fte={total_fte:.4f}")


if __name__ == "__main__":
    main()
