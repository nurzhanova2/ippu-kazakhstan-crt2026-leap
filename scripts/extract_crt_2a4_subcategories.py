"""Extract the 2.A.4 subcategory breakdown from CRT 2025 Table 2(I).A-H.

The general activity-data extraction skips rows without a category code, so
the 2.A.4.d child row "Use of limestone and dolomite" is missing there. This
script keeps every row of the 2.A.4 block (2.A.4 to 2.A.4.d and uncoded child
rows, which inherit the code of the preceding 2.A.4.x row) for 1990-2023.
Notation keys (NO, NA, IE) are kept as reported.

row_level marks the hierarchy: "category" (2.A.4), "subcategory" (2.A.4.a-d)
and "item" (uncoded rows under a subcategory, e.g. "Use of limestone and
dolomite" under 2.A.4.d). The CO2 of an item repeats its subcategory, so sum
only the "subcategory" rows to obtain the 2.A.4 total.

--inventory crt2025 (default) or crt2026 selects the CRT submission.
"""

import csv
from pathlib import Path
import re

from inventory_versions import VERSIONS, crt_workbooks, selected_version, workbook_year


VERSION = selected_version()
OUTPUT = (Path("data/processed/crt_2025_2a4_subcategories_1990_2023.csv") if VERSION == "crt2025"
          else Path(f"data/processed/crt_2a4_subcategories_1990_{VERSIONS[VERSION]['last_year']}{VERSIONS[VERSION]['suffix']}.csv"))
TABLE = VERSIONS[VERSION]["source"].replace("UNFCCC ", "") + " Table2(I).A-H"


def value(row, index):
    cell = row[index] if len(row) > index else None
    return cell.strip() if isinstance(cell, str) else cell


def rows_2a4(name, book):
    year = workbook_year(name)
    sheet = book["Table2(I).A-H"]
    records, code, inside = [], None, False
    for row in sheet.iter_rows(values_only=True):
        label = value(row, 1)
        if not isinstance(label, str):
            continue
        match = re.match(r"^(2\.[A-H](?:\.\d+(?:\.[a-z]+)?)?)\.\s*(.*)$", label)
        if match:
            inside = match.group(1).startswith("2.A.4")
            if not inside:
                if records:
                    break
                continue
            code, label = match.group(1), match.group(2).strip()
            level = "category" if code == "2.A.4" else "subcategory"
        elif not inside:
            continue
        else:
            level = "item"
        records.append({
            "inventory_year": year,
            "row_level": level,
            "category_code": code,
            "category_label": label,
            "activity_description": value(row, 2),
            "activity_kt": value(row, 3),
            "implied_co2_ef_t_per_t": value(row, 4),
            "co2_kt": value(row, 7),
            "source_table": TABLE,
        })
    return records


records = []
for name, book in crt_workbooks(VERSION):
    records.extend(rows_2a4(name, book))

with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=records[0].keys(), lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
print(f"Wrote {len(records)} records to {OUTPUT}")
