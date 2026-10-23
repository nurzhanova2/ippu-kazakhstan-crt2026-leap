"""Build the LEAP branch parameters for a newer inventory base.

Copies branch IDs, groups, gases, LEAP units and the f2030/f2050 factors from
data/metadata/leap_scenario_parameters.csv (CRT 2025 proxy base, archived) and
replaces base_t with the CRT values of the inventory's last year, taken from
the subcategory emissions extracted from Table 2(I).A-H. Only the gas of each
branch is used (CO2 for sinter; CH4 of 2.C.1 is outside the boundary).

In the CRT 2026 journal version, branch 349 (other process uses of carbonates,
2.A.4) keeps f = 1.00 in Moderate and Ambitious (FACTOR_OVERRIDES); the archived
CRT 2025 parameters keep the mineral-group factors.

usage: build_leap_parameters.py --inventory crt2026
writes data/metadata/leap_scenario_parameters_crt2026.csv
"""

import csv
from pathlib import Path

from inventory_versions import VERSIONS, selected_version


# Model branch -> CRT subcategory or subcategories and the gas column used.
BRANCHES = {
    "Cement clinker": (["2.A.1"], "co2_kt"),
    "Lime": (["2.A.2"], "co2_kt"),
    "Glass": (["2.A.3"], "co2_kt"),
    "Other carbonate uses": (["2.A.4.a", "2.A.4.b", "2.A.4.d"], "co2_kt"),
    "Pig iron": (["2.C.1.b"], "co2_kt"),
    "Steel": (["2.C.1.a"], "co2_kt"),
    "Sinter": (["2.C.1.d"], "co2_kt"),
    "Pellets": (["2.C.1.e"], "co2_kt"),
    "Ferroalloys (CO2)": (["2.C.2"], "co2_kt"),
    "Ferroalloys (CH4)": (["2.C.2"], "ch4_kt"),
    "Aluminium": (["2.C.3"], "co2_kt"),
    "Zinc": (["2.C.6"], "co2_kt"),
    "Ammonia": (["2.B.1"], "co2_kt"),
    "Nitric acid": (["2.B.2"], "n2o_kt"),
    "Calcium carbide": (["2.B.5.b"], "co2_kt"),
}

# Journal version (decision of 23 October 2026): no lever is found in the
# literature for 2.A.4.a+b, and none can be attached to 2.A.4.d, a residual
# without identified end use, so 2.A.4 keeps f = 1.00 as in the literature
# factor sets. The mineral-group factors for 2.A.4 remain a sensitivity variant
# (scripts/analyze_leap_sensitivity.py).
FACTOR_OVERRIDES = {
    "crt2026": {"Other carbonate uses": {k: "1.00" for k in (
        "moderate_f2030", "moderate_f2050", "ambitious_f2030", "ambitious_f2050")}},
}

VERSION = selected_version("crt2026")
LAST = VERSIONS[VERSION]["last_year"]
SUFFIX = VERSIONS[VERSION]["suffix"]
SOURCE = Path("data/metadata/leap_scenario_parameters.csv")
EMISSIONS = Path(f"data/processed/crt_ippu_subcategory_emissions_1990_{LAST}{SUFFIX}.csv")
OUTPUT = Path(f"data/metadata/leap_scenario_parameters{SUFFIX}.csv")

with EMISSIONS.open(encoding="utf-8", newline="") as handle:
    crt = {row["category_code"]: row for row in csv.DictReader(handle)
           if row["row_level"] == "coded" and row["inventory_year"] == str(LAST)}
with SOURCE.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))

for row in rows:
    codes, column = BRANCHES[row["process"]]
    kt = sum(float(crt[code][column] or 0) for code in codes)
    row["base_t"] = f"{kt * 1000:.3f}"
    row.update(FACTOR_OVERRIDES.get(VERSION, {}).get(row["process"], {}))

with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print(f"Wrote {len(rows)} branches ({VERSIONS[VERSION]['source']}, {LAST}) to {OUTPUT}")
