from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, InvalidOperation


ALIASES = {
    "district_name": {"school district"},
    "employee_name": {"name"},
    "duty_title": {"duty title"},
    "certificated_fte": {"cert fte"},
    "classified_fte": {"clas fte", "class fte"},
    "base_salary": {"base salary"},
    "total_salary": {"total salary"},
    "insurance_benefits": {"insurance benefits"},
    "mandatory_benefits": {"mandatory benefits"},
    "last_name": {"last name"},
    "first_name": {"first name"},
    "certificate_number": {"cert #"},
    "location_code": {"location code"},
    "location_name": {"building location name"},
}

NUMERIC_FIELDS = {
    "certificated_fte", "classified_fte", "base_salary", "total_salary",
    "insurance_benefits", "mandatory_benefits",
}


def norm_header(value) -> str:
    return " ".join(str(value or "").strip().lower().split())


def header_positions(headers) -> dict[str, list[int]]:
    positions = defaultdict(list)
    for index, header in enumerate(headers):
        positions[norm_header(header)].append(index)
    return dict(positions)


def _value(row, positions, aliases, *, duplicate_policy="first_nonempty"):
    indexes = []
    for alias in aliases:
        indexes.extend(positions.get(alias, []))
    indexes.sort()
    values = [row[i] if i < len(row) else None for i in indexes]
    nonempty = [v for v in values if v not in (None, "")]
    if not nonempty:
        return None
    if duplicate_policy == "first_nonempty":
        return nonempty[0]
    raise RuntimeError(f"unsupported duplicate policy: {duplicate_policy}")


def numeric(value):
    if value in (None, ""):
        return None
    try:
        return float(Decimal(str(value).replace(",", "").replace("$", "").strip()))
    except InvalidOperation as exc:
        raise ValueError(f"not numeric: {value!r}") from exc


def canonicalize_row(*, school_year, source_sha256, source_sheet, source_row, headers, row):
    positions = header_positions(headers)
    result = {
        "school_year": school_year,
        "source_sha256": source_sha256,
        "source_sheet": source_sheet,
        "source_row": source_row,
    }
    for field, aliases in ALIASES.items():
        value = _value(row, positions, aliases)
        result[field] = numeric(value) if field in NUMERIC_FIELDS else value
    return result


def is_riverview(row: dict) -> bool:
    name = " ".join(str(row.get("district_name") or "").lower().split())
    return name == "riverview school district"
