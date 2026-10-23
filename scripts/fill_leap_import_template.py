"""Fill a LEAP Export-to-Excel template while preserving its import identifiers.

The script only replaces the Expression cells in column L.  It deliberately
leaves BranchID, VariableID, ScenarioID, RegionID, paths, units and sheet
layout untouched, so the resulting workbook can be read by LEAP's
Import-from-Excel command.

usage: fill_leap_import_template.py INPUT.xlsx OUTPUT.xlsx [--parameters CSV]
The default parameters are the CRT 2025 proxy base (archived conference
workbook); data/metadata/leap_scenario_parameters_crt2026.csv gives the
CRT 2026 inventory 2024 base of the journal version.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.etree import ElementTree as ET

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
ET.register_namespace("", NS)

# Base values (tonnes of gas) and 2030/2050 factors shared with
# scripts/analyze_leap_scenarios.py. 2024 Current Accounts use the latest
# inventory year (CRT 2025, 2023) as a proxy. Baseline holds that level
# constant; moderate and ambitious are explicitly illustrative sensitivity
# pathways, not policy forecasts.
PARAMETERS = Path(sys.argv[sys.argv.index("--parameters") + 1]) if "--parameters" in sys.argv \
    else Path("data/metadata/leap_scenario_parameters.csv")

# Tonnes of gas -> native unit of each branch in the LEAP template. CO2
# branches are in Metric Tonne. Branches 361 (ferroalloys CH4) and 354
# (nitric acid N2O) are kg (branch unit in LEAP template): 36.894 t is
# written as 36894.0 and 592.4 t as 592400.0.
TO_LEAP_UNIT = {"Metric Tonne": 1.0, "Kilogramme": 1000.0}

with PARAMETERS.open(encoding="utf-8", newline="") as handle:
    PARAMS = {int(row["branch_id"]): row for row in csv.DictReader(handle)}

CURRENT = {branch_id: float(row["base_t"]) * TO_LEAP_UNIT[row["leap_unit"]]
           for branch_id, row in PARAMS.items()}


def scenario_expression(branch_id: int, scenario: str) -> str:
    value = CURRENT[branch_id]
    if scenario == "Baseline":
        f2030, f2050 = 1.0, 1.0
    elif scenario == "Moderate mitigation":
        f2030 = float(PARAMS[branch_id]["moderate_f2030"])
        f2050 = float(PARAMS[branch_id]["moderate_f2050"])
    elif scenario == "Ambitious mitigation":
        f2030 = float(PARAMS[branch_id]["ambitious_f2030"])
        f2050 = float(PARAMS[branch_id]["ambitious_f2050"])
    else:
        raise ValueError(f"Unexpected scenario: {scenario}")
    return f"Interp(2024,{value:.6f},2030,{value*f2030:.6f},2050,{value*f2050:.6f})"


def text_from_cell(cell: ET.Element, shared: list[str]) -> str:
    value = cell.find(f"{{{NS}}}v")
    if value is None or value.text is None:
        return ""
    return shared[int(value.text)] if cell.get("t") == "s" else value.text


def main(input_path: Path, output_path: Path) -> None:
    with ZipFile(input_path) as source:
        contents = {name: source.read(name) for name in source.namelist()}

    shared_root = ET.fromstring(contents["xl/sharedStrings.xml"])
    shared = ["".join(t.text or "" for t in item.iter(f"{{{NS}}}t")) for item in shared_root]
    shared_index = {value: index for index, value in enumerate(shared)}

    def add_shared(value: str) -> int:
        if value in shared_index:
            return shared_index[value]
        item = ET.SubElement(shared_root, f"{{{NS}}}si")
        text = ET.SubElement(item, f"{{{NS}}}t")
        text.text = value
        shared_index[value] = len(shared)
        shared.append(value)
        return shared_index[value]

    sheet = ET.fromstring(contents["xl/worksheets/sheet1.xml"])
    for row in sheet.findall(f".//{{{NS}}}row"):
        cells = {cell.get("r").rstrip("0123456789"): cell for cell in row.findall(f"{{{NS}}}c")}
        if "A" not in cells or "G" not in cells:
            continue
        try:
            branch_id = int(text_from_cell(cells["A"], shared))
        except ValueError:
            continue
        if branch_id not in CURRENT:
            continue
        unit = text_from_cell(cells["J"], shared)
        if unit != PARAMS[branch_id]["leap_unit"]:
            raise ValueError(f"Branch {branch_id}: template unit {unit!r}, "
                             f"parameters expect {PARAMS[branch_id]['leap_unit']!r}")
        scenario = text_from_cell(cells["G"], shared)
        if scenario == "Current Accounts":
            expression = f"{CURRENT[branch_id]:.6f}"
        else:
            expression = scenario_expression(branch_id, scenario)
        expression_cell = cells["L"]
        expression_cell.set("t", "s")
        for child in list(expression_cell):
            expression_cell.remove(child)
        value = ET.SubElement(expression_cell, f"{{{NS}}}v")
        value.text = str(add_shared(expression))

    shared_root.set("count", str(len(shared)))
    shared_root.set("uniqueCount", str(len(shared)))
    contents["xl/sharedStrings.xml"] = ET.tostring(shared_root, encoding="utf-8", xml_declaration=True)
    contents["xl/worksheets/sheet1.xml"] = ET.tostring(sheet, encoding="utf-8", xml_declaration=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output_path, "w", ZIP_DEFLATED) as target:
        for name, data in contents.items():
            target.writestr(name, data)


if __name__ == "__main__":
    positional = [a for i, a in enumerate(sys.argv[1:], 1)
                  if a != "--parameters" and sys.argv[i - 1] != "--parameters"]
    if len(positional) != 2:
        raise SystemExit("usage: fill_leap_import_template.py INPUT.xlsx OUTPUT.xlsx [--parameters CSV]")
    main(Path(positional[0]), Path(positional[1]))
