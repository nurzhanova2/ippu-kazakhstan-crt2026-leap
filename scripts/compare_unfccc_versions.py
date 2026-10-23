"""Compare common IPPU observations in two UNFCCC submissions.

Default: CRF 2023 vs CRT 2025 for 1990-2021 (archived output). With
"--pair crt2025_crt2026": CRT 2025 vs CRT 2026 for 1990-2023, in the same
format; both use AR5, so differences are recalculations.
With "--pair three_submissions": CRF 2023, CRT 2025 and CRT 2026 for
1990-2021 side by side, for four metrics (see THREE_METRICS).
"""

import csv
import sys
from pathlib import Path


PAIRS = {
    "crf2023_crt2025": {
        "inputs": [Path("data/processed/unfccc_ippu_emissions_1990_2023.csv")],
        "output": Path("data/processed/crf_2023_vs_crt_2025_ippu_comparison_1990_2021.csv"),
        "old": ("UNFCCC CRF 2023", "crf_2023", "ar4", "crf"),
        "new": ("UNFCCC CRT 2025", "crt_2025", "ar5", "crt"),
        "years": range(1990, 2022),
        "note": "Total CO2eq comparison combines CRF AR4 and CRT AR5 GWP frameworks; CO2-only difference is less affected by GWP changes.",
    },
    "crt2025_crt2026": {
        "inputs": [Path("data/processed/unfccc_ippu_emissions_1990_2023.csv"),
                   Path("data/processed/unfccc_ippu_emissions_1990_2024_crt2026.csv")],
        "output": Path("data/processed/crt_2025_vs_crt_2026_ippu_comparison_1990_2023_crt2026.csv"),
        "old": ("UNFCCC CRT 2025", "crt_2025", "ar5", "crt2025"),
        "new": ("UNFCCC CRT 2026", "crt_2026", "ar5", "crt2026"),
        "years": range(1990, 2024),
        "note": "Both submissions use AR5 GWPs; differences are recalculations (see NID 2026).",
    },
}
THREE_INPUTS = [Path("data/processed/unfccc_ippu_emissions_1990_2023.csv"),
                Path("data/processed/unfccc_ippu_emissions_1990_2024_crt2026.csv")]
THREE_OUTPUT = Path("data/processed/inventory_submissions_ippu_comparison_1990_2021_crt2026.csv")
THREE_SOURCES = ("UNFCCC CRF 2023", "UNFCCC CRT 2025", "UNFCCC CRT 2026")
# (metric, column, categories summed, note). CRF 2023 Table 2(I)s1 gives
# subcategories only for 2.A-2.C, so 2.A+2.B+2.C is the widest set that can be
# matched category by category; CO2 does not depend on the GWP set.
THREE_METRICS = [
    ("total_co2eq_as_reported", "total_ghg_kt_co2eq", ("2",),
     "Total IPPU, kt CO2eq; CRF 2023 with AR4 GWPs (recalculated from gas components), CRT 2025 and CRT 2026 with AR5 GWPs"),
    ("total_co2", "co2_kt", ("2",), "Total IPPU, kt CO2; independent of GWPs"),
    ("co2_2A_2B_2C", "co2_kt", ("2.A", "2.B", "2.C"),
     "Mineral, chemical and metal industry, kt CO2; same categories in all three submissions; independent of GWPs"),
    ("co2_2A4", "co2_kt", ("2.A.4",), "Other process uses of carbonates, kt CO2; independent of GWPs"),
    ("hfc_co2eq_as_reported", "hfc_kt_co2eq", ("2",),
     "HFCs, kt CO2eq as reported; AR4 GWPs in CRF 2023, AR5 GWPs in CRT; species-level data not extracted"),
]


def three_submissions():
    rows = []
    for path in THREE_INPUTS:
        with path.open(encoding="utf-8") as handle:
            rows.extend(csv.DictReader(handle))
    index = {(row["source"], row["inventory_year"], row["category_code"]): row for row in rows}
    records = []
    for year in range(1990, 2022):
        for metric, column, codes, note in THREE_METRICS:
            crf, crt25, crt26 = (sum(float(index[(source, str(year), code)][column]) for code in codes)
                                 for source in THREE_SOURCES)
            records.append({
                "inventory_year": year,
                "metric": metric,
                "crf_2023": crf,
                "crt_2025": crt25,
                "crt_2026": crt26,
                "difference_crt_2025_minus_crf_2023": crt25 - crf,
                "difference_percent_of_crf_2023": (crt25 - crf) / crf * 100 if crf else "",
                "difference_crt_2026_minus_crt_2025": crt26 - crt25,
                "difference_percent_of_crt_2025": (crt26 - crt25) / crt25 * 100 if crt25 else "",
                "note": note,
            })
    with THREE_OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"Wrote {len(records)} records to {THREE_OUTPUT}")


pair = sys.argv[sys.argv.index("--pair") + 1] if "--pair" in sys.argv else "crf2023_crt2025"
if pair == "three_submissions":
    three_submissions()
    sys.exit()
spec = PAIRS[pair]
old_source, old_name, old_gwp, old_short = spec["old"]
new_source, new_name, new_gwp, new_short = spec["new"]

rows = []
for path in spec["inputs"]:
    with path.open(encoding="utf-8") as handle:
        rows.extend(csv.DictReader(handle))

index = {(row["source"], row["inventory_year"], row["category_code"]): row for row in rows}
records = []
for year in spec["years"]:
    for code in sorted({row["category_code"] for row in rows if row["inventory_year"] == str(year)}):
        old = index.get((old_source, str(year), code))
        new = index.get((new_source, str(year), code))
        if not old or not new:
            continue
        old_total = float(old["total_ghg_kt_co2eq"])
        new_total = float(new["total_ghg_kt_co2eq"])
        old_co2 = float(old["co2_kt"])
        new_co2 = float(new["co2_kt"])
        records.append({
            "inventory_year": year,
            "category_code": code,
            "category_label": new["category_label"],
            f"{old_name}_total_ghg_kt_co2eq_{old_gwp}": old_total,
            f"{new_name}_total_ghg_kt_co2eq_{new_gwp}": new_total,
            f"total_difference_{new_short}_minus_{old_short}_kt_co2eq": new_total - old_total,
            f"total_difference_percent_of_{old_short}": (new_total - old_total) / old_total * 100 if old_total else "",
            f"{old_name}_co2_kt": old_co2,
            f"{new_name}_co2_kt": new_co2,
            f"co2_difference_{new_short}_minus_{old_short}_kt": new_co2 - old_co2,
            f"co2_difference_percent_of_{old_short}": (new_co2 - old_co2) / old_co2 * 100 if old_co2 else "",
            "interpretation_note": spec["note"],
        })

with spec["output"].open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)
print(f"Wrote {len(records)} records to {spec['output']}")
