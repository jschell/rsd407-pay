"""Offline survey of OSPI F-196 Table 2 and committed S-275 peer aggregates."""
import argparse
import csv
import hashlib
import json
import math
import statistics
from pathlib import Path

from openpyxl import load_workbook

ACTIVITIES = {
    "11": "Board of Directors", "12": "Superintendent's Office",
    "13": "Business Office", "14": "Human Resources", "15": "Public Relations",
    "21": "Supervision - Instruction", "23": "Principal's Office",
    "32": "Instructional Technology", "65": "Utilities",
    "72": "Informational Systems", "73": "Printing",
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def extract_sheet(sheet, year, wanted):
    rows = list(sheet.values)
    if rows[1][1] != f"{year} General Fund Expenditures by {sheet.title}":
        raise ValueError("Unexpected year or sheet title")
    if tuple(rows[3][2:5]) != ("District Name", "Total Full Enrollment", "Total"):
        raise ValueError("Unexpected district/enrollment/total schema")
    codes = [str(c) for c in rows[2][5:]]
    labels = rows[3][5:]
    if len(set(codes)) != len(codes):
        raise ValueError("Duplicate expenditure codes")
    if sheet.title == "Activity":
        for code, label in ACTIVITIES.items():
            if code not in codes or labels[codes.index(code)] != label:
                raise ValueError(f"Activity schema changed: {code}")
    if sheet.title == 'Object' and ('7' not in codes or labels[codes.index('7')] != 'Purchased Services'):
        raise ValueError('Purchased-services object schema changed')
    found = {}
    for index, row in enumerate(rows[5:], 6):
        code = str(row[1])
        if code not in wanted:
            continue
        if code in found:
            raise ValueError(f"Duplicate district {code}")
        if row[2] != wanted[code]:
            raise ValueError(f"District name mismatch: {code}")
        values = [float(v or 0) for v in row[5:]]
        total, enrollment = float(row[4]), float(row[3])
        if not all(math.isfinite(v) for v in values + [total, enrollment]) or enrollment <= 0:
            raise ValueError("Invalid financial values")
        if not math.isclose(sum(values), total, abs_tol=0.02, rel_tol=0):
            raise ValueError(f"Expenditure reconciliation failed: {code}/{sheet.title}")
        found[code] = dict(source_row=index, total=total,
                           reported_full_enrollment=enrollment,
                           amounts=dict(zip(codes, values)), labels=dict(zip(codes, labels)))
    if set(found) != set(wanted):
        raise ValueError("Missing selected districts")
    return found


def survey(peer_path, source_dir, manifest_path, annual_category_path):
    peer = json.loads(Path(peer_path).read_text())
    entries = json.loads(Path(manifest_path).read_text())
    if sorted(e['school_year'] for e in entries) != ['2023-24','2024-25']:
        raise ValueError('Expected exactly two financial source years')
    result = []
    for entry in entries:
        year = entry["school_year"]
        path = Path(source_dir) / entry["filename"]
        if digest(path) != entry["sha256"]:
            raise ValueError("Financial source hash mismatch")
        selected = [r for r in peer["rows"] if r["school_year"] == year]
        wanted = {r["district_code"]: r["source_label"] for r in selected}
        if len(wanted) != len(selected) or not wanted:
            raise ValueError("Duplicate or missing peer/year rows")
        workbook = load_workbook(path, read_only=True, data_only=True)
        sheets = {name: extract_sheet(workbook[name], year, wanted)
                  for name in ("Activity", "Object", "Program")}
        for r in selected:
            code = r["district_code"]
            a, o, p = (sheets[name][code] for name in ("Activity", "Object", "Program"))
            if max(a["total"], o["total"], p["total"]) - min(a["total"], o["total"], p["total"]) > 0.02:
                raise ValueError("Cross-sheet total mismatch")
            if max(a["reported_full_enrollment"],o["reported_full_enrollment"],p["reported_full_enrollment"]) - min(a["reported_full_enrollment"],o["reported_full_enrollment"],p["reported_full_enrollment"]) > 0.001:
                raise ValueError("Cross-sheet enrollment mismatch")
            fte = float(r["student_fte"])
            if not math.isfinite(fte) or fte <= 0:
                raise ValueError("Invalid P-223 enrollment")
            admin = sum(a["amounts"][c] for c in ("11", "12", "13", "14", "15"))
            result.append(dict(district=r["district"], district_code=code, school_year=year,
                student_fte=fte, f196_full_enrollment=a["reported_full_enrollment"],
                general_fund_expenditure=a["total"], administration_activities_11_15=admin,
                admin_per_1000_student_fte=admin / fte * 1000,
                admin_share_general_fund=admin / a["total"],
                purchased_services_districtwide=o["amounts"]["7"],
                activity_amounts={c: a["amounts"][c] for c in ACTIVITIES},
                source_rows={name: sheets[name][code]["source_row"] for name in sheets}))
        workbook.close()
    with Path(annual_category_path).open() as f:
        history = [r for r in csv.DictReader(f) if r['job_family'] in ('district/central administration', 'clerical/office')]
    keys = [(r['school_year'],r['job_family']) for r in history]
    expected = {(f'{y}-{str(y+1)[-2:]}', family) for y in range(2013,2025)
                for family in ('district/central administration','clerical/office')}
    if set(keys) != expected or len(keys) != len(set(keys)):
        raise ValueError('Expected twelve years of central and clerical history')
    for r in history:
        for k in ('total_fte','fte_per_1000_student_fte','reported_employer_compensation'):
            r[k] = float(r[k])
            if not math.isfinite(r[k]) or r[k] < 0:
                raise ValueError('Invalid annual personnel aggregate')
    latest = [r for r in result if r['school_year']=='2024-25']
    rv = next(r for r in latest if r['district']=='Riverview')
    old = next(r for r in result if r['district']=='Riverview' and r['school_year']=='2023-24')
    size_peers = [r for r in latest if r['district']!='Riverview' and 0.7*rv['student_fte'] <= r['student_fte'] <= 1.3*rv['student_fte']]
    median = statistics.median(r['admin_per_1000_student_fte'] for r in size_peers)
    findings = dict(size_peer_districts=[r['district'] for r in size_peers],
        size_peer_median_per_1000=median, riverview_difference_from_size_median=rv['admin_per_1000_student_fte']/median-1,
        riverview_nominal_admin_increase=rv['administration_activities_11_15']-old['administration_activities_11_15'],
        riverview_admin_change=rv['administration_activities_11_15']/old['administration_activities_11_15']-1,
        nearby_differences={r['district']:rv['admin_per_1000_student_fte']/r['admin_per_1000_student_fte']-1
                            for r in latest if r['district'] in ('Snoqualmie Valley','Northshore','Monroe')})
    return dict(schema_version=1, financial_rows=result, findings=findings, riverview_annual_history=history,
        personnel_rows=peer["rows"], duty_title_evidence=peer["duty_title_evidence"],
        provenance=dict(peer_input_sha256=digest(peer_path), annual_category_sha256=digest(annual_category_path), financial_sources=entries,
                        parser_sha256=digest(__file__), parser_version=1),
        limitations=["Activity totals and object totals are separate marginal tables, not a district activity-by-object cross-tab.",
            "Purchased services are districtwide and include student-facing services; they are not avoidable overhead.",
            "F-196 actual general-fund expenditures and S-275 employer compensation have different coverage and accounting bases; do not add or reconcile them as identical measures.",
            "Rates use the committed P-223 K-12 student FTE. F-196 Total Full Enrollment differs and is retained separately without inferring the reason.",
            "Reported activities and duty titles do not establish necessary staffing, duplicated work, service quality, or attainable savings.",
            "Nominal financial change covers only 2023-24 to 2024-25. Peer personnel observations cover only three selected years."])


def write_report(data, output):
    output.mkdir(parents=True, exist_ok=True)
    (output / "overhead-review.json").write_text(json.dumps(data, indent=2) + "\n")
    rows = data["financial_rows"]
    fields = [k for k in rows[0] if k not in ("activity_amounts", "source_rows")]
    with (output / "overhead-financial.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fields); writer.writeheader()
        writer.writerows({k: r[k] for k in fields} for r in rows)
    lines = ["# Overhead spending and staffing survey", "", "Financial years: 2023–24 and 2024–25. All dollars nominal. Generated from retained OSPI F-196 Table 2 sources and committed S-275 comparison data.", "",
        "## Actual general-fund expenditure comparison", "",
        "Administration is the sum of activities 11–15: board, superintendent, business office, HR, and public relations. This includes all spending objects within those activities, and differs from the strict personnel-title category.", "",
        "| District | 2024–25 administration | Per 1,000 P-223 student FTE | Share of general fund | Change from 2023–24 |", "| --- | ---: | ---: | ---: | ---: |"]
    for r in [r for r in rows if r["school_year"] == "2024-25"]:
        old = next(x for x in rows if x["district"] == r["district"] and x["school_year"] == "2023-24")
        change = r["administration_activities_11_15"] / old["administration_activities_11_15"] - 1
        lines.append(f'| {r["district"]} | ${r["administration_activities_11_15"]:,.0f} | ${r["admin_per_1000_student_fte"]:,.0f} | {r["admin_share_general_fund"]:.1%} | {change:+.1%} |')
    lines += ['', f"Riverview is {data['findings']['riverview_difference_from_size_median']:.1%} above the median of the six selected peers within 30% of its P-223 enrollment on activities 11–15. This is a descriptive comparison, not a savings estimate. These are the same size peers used in the personnel evaluation.", '']
    lines += ["", "## Riverview expenditure detail", "", "| Activity | 2023–24 | 2024–25 | Dollar change |", "| --- | ---: | ---: | ---: |"]
    old, new = [next(r for r in rows if r["district"] == "Riverview" and r["school_year"] == y) for y in ("2023-24", "2024-25")]
    for c, label in ACTIVITIES.items():
        x, y = old["activity_amounts"][c], new["activity_amounts"][c]
        lines.append(f"| {c} {label} | ${x:,.0f} | ${y:,.0f} | ${y-x:+,.0f} |")
    lines += ["", "## Personnel classification sensitivity", "", "These buckets remain separate. Director/Supervisor and Office/Clerical titles span school and operational functions and cannot be treated as central overhead without assignment evidence.", "",
        "| District | Strict central FTE | Director/Supervisor FTE | Office/Clerical FTE |", "| --- | ---: | ---: | ---: |"]
    for r in [r for r in data["personnel_rows"] if r["school_year"] == "2024-25"]:
        clerical = data["duty_title_evidence"]["2024-25"][r["district"]].get("Office/Clerical", {}).get("fte", 0)
        lines.append(f'| {r["district"]} | {r["central_fte"]:.3f} | {r["director_supervisor_fte_excluded"]:.3f} | {clerical:.3f} |')
    lines += ["", "## Riverview selected-year staffing", "", "| Year | Student FTE | Strict central FTE | Director/Supervisor FTE | Office/Clerical FTE |", "| --- | ---: | ---: | ---: | ---: |"]
    for r in [r for r in data["personnel_rows"] if r["district"] == "Riverview"]:
        clerical = data["duty_title_evidence"][r["school_year"]]["Riverview"].get("Office/Clerical", {}).get("fte", 0)
        lines.append(f'| {r["school_year"]} | {r["student_fte"]:,.2f} | {r["central_fte"]:.3f} | {r["director_supervisor_fte_excluded"]:.3f} | {clerical:.3f} |')
    lines += ["", "## Limits", ""] + ["- " + x for x in data["limitations"]]
    lines += ["", "## Twelve-year central staffing check", "", "| Year | Central FTE | Clerical FTE |", "| --- | ---: | ---: |"]
    history = data['riverview_annual_history']
    for year in sorted({r['school_year'] for r in history}):
        central = next(r for r in history if r['school_year']==year and r['job_family']=='district/central administration')
        clerical = next(r for r in history if r['school_year']==year and r['job_family']=='clerical/office')
        lines.append(f"| {year} | {central['total_fte']:.3f} | {clerical['total_fte']:.3f} |")
    lines += ['', 'The latest central FTE increase follows two lower years. Four FTE in 2024–25 equals 2013–14 and 2019–20, and is below several intervening years. Annual family history uses the Riverview job-family mapping; the peer mapping adds deputy/assistant superintendent titles (none in Riverview latest year).', '']
    lines += ["", "See [source manifest](overhead-sources.json), [calculation evidence](overhead-review.json), and [public-document review and next investigations](overhead-findings.md).", ""]
    (output / "overhead-review.md").write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--peer", type=Path, required=True)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--annual-category", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_report(survey(args.peer, args.sources, args.manifest, args.annual_category), args.output)


if __name__ == "__main__":
    main()
