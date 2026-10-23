"""Extract IPPU emissions by subcategory from CRT Table 2(I).A-H.

Table 2(I) reports categories down to the second level (for example 2.C.1);
the model branches need the subcategory level (2.C.1.a, 2.C.1.b, 2.C.1.d,
2.C.1.e and so on), which Table 2(I).A-H reports together with activity data.
CO2, CH4 and N2O are in kt; total_kt_co2eq_ar5 applies CH4 = 28 and N2O = 265.
Uncoded rows inherit the code of the preceding coded row (row_level "item").

--inventory crt2025 (default) or crt2026 selects the CRT submission.
"""

import csv
from pathlib import Path
import re

from inventory_versions import VERSIONS, crt_workbooks, selected_version, workbook_year


VERSION = selected_version()
OUTPUT = Path(f"data/processed/crt_ippu_subcategory_emissions_1990_{VERSIONS[VERSION]['last_year']}"
              f"{'_crt2025' if VERSION == 'crt2025' else VERSIONS[VERSION]['suffix']}.csv")
GWP = {"co2": 1, "ch4": 28, "n2o": 265}


def number(value):
    return float(value) if isinstance(value, (int, float)) else None


def rows(name, book):
    year = workbook_year(name)
    records, code = [], None
    for row in book["Table2(I).A-H"].iter_rows(values_only=True):
        label = row[1].strip() if len(row) > 1 and isinstance(row[1], str) else None
        if not label:
            continue
        match = re.match(r"^(2\.[A-H](?:\.\d+(?:\.[a-z]+)?)?)\.\s*(.*)$", label)
        if match:
            code, label, level = match.group(1), match.group(2).strip(), "coded"
        elif code is None:
            continue
        else:
            level = "item"
        gases = {gas: number(row[i]) for gas, i in (("co2", 7), ("ch4", 8), ("n2o", 9))}
        if all(v is None for v in gases.values()):
            continue
        records.append({
            "source": VERSIONS[VERSION]["source"], "inventory_year": year, "row_level": level,
            "category_code": code, "category_label": label,
            "activity_kt": number(row[3]) if len(row) > 3 else None,
            "co2_kt": gases["co2"], "ch4_kt": gases["ch4"], "n2o_kt": gases["n2o"],
            "total_kt_co2eq_ar5": sum((v or 0.0) * GWP[g] for g, v in gases.items()),
            "source_table": "Table2(I).A-H",
        })
    return records


records = []
for name, book in crt_workbooks(VERSION):
    records.extend(rows(name, book))

with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=records[0].keys(), lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
print(f"Wrote {len(records)} records to {OUTPUT}")
