"""Produce reproducible IPPU trend, composition and CRF--CRT comparison outputs.

Inputs are the long-form files generated from unmodified UNFCCC workbooks.
The script writes analysis tables to ``data/processed`` and publication-ready
PNG figures to ``figures``. CRT total CO2eq uses AR5; CRF total CO2eq is
recalculated with AR4. Therefore the CO2eq version comparison is displayed as
a reporting-comparison signal, not as a pure inventory revision.

--inventory crt2025 (default) writes the archived conference outputs;
--inventory crt2026 writes the same tables and figures for CRT 2026 (1990-2024)
with the suffix _crt2026, and compares CRT 2025 with CRT 2026 (both AR5).
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

from inventory_versions import VERSIONS, selected_version


VERSION = selected_version()
LAST = VERSIONS[VERSION]["last_year"]
SUFFIX = VERSIONS[VERSION]["suffix"]
EMISSIONS = Path(f"data/processed/unfccc_ippu_emissions_1990_{LAST}{SUFFIX}.csv")
COMPARISON = {
    "crt2025": {"input": Path("data/processed/crf_2023_vs_crt_2025_ippu_comparison_1990_2021.csv"),
                "output": "crf_crt_total_ippu_comparison_1990_2021.csv", "old": "crf", "end": 2021,
                "titles": ("Total CO$_2$eq difference: CRT 2025 (AR5) − CRF 2023 (AR4)", "CO$_2$ difference: CRT 2025 − CRF 2023"),
                "ylabel": "Difference, % of CRF", "suptitle": "Comparison of total IPPU emissions in two UNFCCC submissions",
                "figure": "figure_3_crf_2023_vs_crt_2025_total_ippu_comparison.png"},
    "crt2026": {"input": Path("data/processed/crt_2025_vs_crt_2026_ippu_comparison_1990_2023_crt2026.csv"),
                "output": "crt_2025_vs_crt_2026_total_ippu_comparison_1990_2023_crt2026.csv", "old": "crt2025", "end": 2023,
                "titles": ("Total CO$_2$eq difference: CRT 2026 − CRT 2025 (both AR5)", "CO$_2$ difference: CRT 2026 − CRT 2025"),
                "ylabel": "Difference, % of CRT 2025", "suptitle": "Recalculation of total IPPU emissions between the CRT 2025 and CRT 2026 submissions",
                "figure": "figure_3_crt_2025_vs_crt_2026_total_ippu_comparison_crt2026.png"},
}[VERSION]
TITLE_TAG = "" if VERSION == "crt2025" else " (CRT 2026)"
PROCESSED = Path("data/processed")
FIGURES = Path("figures")
CATEGORY_CODES = ["2.A", "2.B", "2.C", "2.D", "2.E", "2.F", "2.G", "2.H"]
CATEGORY_LABELS = {
    "2.A": "2.A Mineral industry",
    "2.B": "2.B Chemical industry",
    "2.C": "2.C Metal industry",
    "2.D": "2.D Fuel / solvent use",
    "2.E": "2.E Electronics",
    "2.F": "2.F F-gases",
    "2.G": "2.G Other product use",
    "2.H": "2.H Other",
}


def read_csv(path):
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"No rows to write to {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main():
    PROCESSED.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    rows = read_csv(EMISSIONS)
    crt = [row for row in rows if row["source"] == VERSIONS[VERSION]["source"]]
    index = {(int(row["inventory_year"]), row["category_code"]): row for row in crt}
    years = list(range(1990, LAST + 1))

    historical = []
    shares = []
    values_by_category = {code: [] for code in CATEGORY_CODES}
    totals = []
    for year in years:
        total = float(index[year, "2"]["total_ghg_kt_co2eq"])
        totals.append(total)
        previous = totals[-2] if len(totals) > 1 else None
        historical.append({
            "inventory_year": year,
            "total_ippu_kt_co2eq_ar5": total,
            "annual_change_kt_co2eq": "" if previous is None else total - previous,
            "annual_change_percent": "" if previous in (None, 0) else (total - previous) / previous * 100,
        })
        for code in CATEGORY_CODES:
            value = float(index.get((year, code), {"total_ghg_kt_co2eq": 0})["total_ghg_kt_co2eq"])
            values_by_category[code].append(value)
            shares.append({
                "inventory_year": year,
                "category_code": code,
                "category_label": CATEGORY_LABELS[code],
                "emissions_kt_co2eq_ar5": value,
                "share_of_total_ippu_percent": value / total * 100 if total else "",
            })

    write_csv(PROCESSED / f"ippu_historical_summary_1990_{LAST}{SUFFIX}.csv", historical)
    write_csv(PROCESSED / f"ippu_category_shares_1990_{LAST}{SUFFIX}.csv", shares)

    comparisons = [
        row for row in read_csv(COMPARISON["input"])
        if row["category_code"] == "2"
    ]
    write_csv(PROCESSED / COMPARISON["output"], comparisons)

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(10, 5.6), layout="constrained")
    ax.plot(years, totals, color="#00695C", linewidth=2.5, marker="o", markersize=3)
    minimum_year = years[totals.index(min(totals))]
    for year in (1990, minimum_year, LAST):
        value = totals[years.index(year)]
        ax.scatter(year, value, color="#E65100", zorder=3)
        ax.annotate(f"{year}: {value:,.0f}", (year, value), xytext=(0, 10),
                    textcoords="offset points", ha="center", fontsize=9)
    ax.set_title(f"Kazakhstan IPPU emissions, 1990–{LAST}{TITLE_TAG}")
    ax.set_ylabel("kt CO$_2$eq (AR5)")
    ax.set_xlabel("Inventory year")
    ax.set_xlim(1989.3, LAST + 0.7)
    fig.savefig(FIGURES / f"figure_1_ippu_total_emissions_1990_{LAST}{SUFFIX}.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5.8), layout="constrained")
    colors = ["#4E79A7", "#F28E2B", "#59A14F", "#E15759", "#B07AA1", "#76B7B2", "#EDC948", "#9C755F"]
    ax.stackplot(years, *(values_by_category[code] for code in CATEGORY_CODES),
                 labels=[CATEGORY_LABELS[code] for code in CATEGORY_CODES], colors=colors, alpha=0.9)
    ax.set_title(f"Composition of Kazakhstan IPPU emissions by IPCC category{TITLE_TAG}")
    ax.set_ylabel("kt CO$_2$eq (AR5)")
    ax.set_xlabel("Inventory year")
    ax.set_xlim(1990, LAST)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8, frameon=False)
    fig.savefig(FIGURES / f"figure_2_ippu_category_composition_1990_{LAST}{SUFFIX}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    comparison_years = [int(row["inventory_year"]) for row in comparisons]
    total_diff = [float(row[f"total_difference_percent_of_{COMPARISON['old']}"]) for row in comparisons]
    co2_diff = [float(row[f"co2_difference_percent_of_{COMPARISON['old']}"]) for row in comparisons]
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True, layout="constrained")
    for ax, series, title, color in (
        (axes[0], total_diff, COMPARISON["titles"][0], "#8E24AA"),
        (axes[1], co2_diff, COMPARISON["titles"][1], "#1565C0"),
    ):
        ax.axhline(0, color="#424242", linewidth=0.8)
        ax.plot(comparison_years, series, color=color, linewidth=1.7)
        ax.set_ylabel(COMPARISON["ylabel"])
        ax.set_title(title, fontsize=10)
    axes[1].set_xlabel("Inventory year")
    axes[1].set_xlim(1990, COMPARISON["end"])
    fig.suptitle(COMPARISON["suptitle"], fontsize=13)
    fig.savefig(FIGURES / COMPARISON["figure"], dpi=300)
    plt.close(fig)

    minimum = min(historical, key=lambda row: float(row["total_ippu_kt_co2eq_ar5"]))
    print(f"Wrote historical tables and figures. Minimum: {minimum['inventory_year']} = "
          f"{float(minimum['total_ippu_kt_co2eq_ar5']):,.3f} kt CO2eq.")


if __name__ == "__main__":
    main()

