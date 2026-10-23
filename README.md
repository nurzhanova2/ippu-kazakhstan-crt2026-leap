<div align="center">

# Industrial process emissions in Kazakhstan

### Data and code for inventory harmonisation and exploratory LEAP pathways to 2050

**Language:** [Русский](README_ru.md) · [English](README.md)

Zarina Nurzhanova¹, Ayagoz Khamzina¹, Nurkhat Zhakiyev²˒¹  
¹ Astana IT University, Astana, Kazakhstan  
² Harvard University, Cambridge, USA

[![Status — manuscript under review](https://img.shields.io/badge/status-manuscript%20under%20review-f9a825)](#citation)
[![Coverage — Kazakhstan, 1990–2024](https://img.shields.io/badge/coverage-Kazakhstan%2C%201990–2024-1565c0)](data/processed/ippu_historical_summary_1990_2024_crt2026.csv)
[![Sector — IPCC 2 IPPU](https://img.shields.io/badge/sector-IPCC%202%20IPPU-6a1b9a)](data/metadata/leap_scenario_parameters_crt2026.csv)
[![Code — MIT](https://img.shields.io/badge/code-MIT-455a64)](LICENSE)
[![Data — CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-455a64)](LICENSE-DATA)

</div>

> [!IMPORTANT]
> This repository accompanies the article *Industrial process emissions in Kazakhstan: inventory harmonisation and exploratory LEAP pathways to 2050*. It contains the processed data, parameters, figures, LEAP import workbook and scripts referred to in the article. File paths are the same as in the article's tables and Data availability section.

## About

The study uses Kazakhstan's 2026 greenhouse-gas inventory submission to the UNFCCC (CRT 2026, 1990–2024), compares it with the CRF 2023 and CRT 2025 reporting cycles and builds a LEAP model of 15 process-emission branches of mineral, metal and chemical industry:

```text
inventory submissions → extract series → compare reporting cycles → check against national statistics → 2024 base → LEAP pathways and sensitivity
```

The model covers 22,088 kt CO2eq, or 85.6% of IPPU emissions in 2024. F-gases, aluminium PFCs, several minor IPPU sources and industrial fuel combustion are outside the boundary. All values are in kt CO2eq with AR5 GWP100 (CO2 = 1, CH4 = 28, N2O = 265).

> [!WARNING]
> The pathways are exploratory, not forecasts. The remaining-emissions factors are author-selected envelopes tested against published pathways; they are not official targets, technology-specific potentials or a least-cost result.

## Main scenarios

| Scenario | 2030, kt CO2eq | 2050, kt CO2eq |
|---|---:|---:|
| Baseline | 22,088 | 22,088 |
| Moderate mitigation | 20,006 | 15,463 |
| Ambitious mitigation | 17,247 | 9,979 |

Constant activity; category 2.A.4 (other process uses of carbonates) is kept at f = 1.00. Source: [`leap_ippu_scenario_results_2024_2050_crt2026.csv`](data/processed/leap_ippu_scenario_results_2024_2050_crt2026.csv). Activity-growth variants, literature-based factors and the one-at-a-time analysis are in the `leap_ippu_sensitivity_*_crt2026.csv` files.

## Quick start

### 1. Find the data behind a table or figure

| Article | Files |
|---|---|
| Tables 1–3 | [`leap_scenario_parameters_crt2026.csv`](data/metadata/leap_scenario_parameters_crt2026.csv), [`leap_scenario_parameters.csv`](data/metadata/leap_scenario_parameters.csv), [`unfccc_ippu_emissions_1990_2024_crt2026.csv`](data/processed/unfccc_ippu_emissions_1990_2024_crt2026.csv) |
| Table 4 | [`crt_2a4_subcategories_1990_2024_crt2026.csv`](data/processed/crt_2a4_subcategories_1990_2024_crt2026.csv) |
| Table 5 | [`leap_sensitivity_factors.csv`](data/metadata/leap_sensitivity_factors.csv), [`scenario_levers_literature.csv`](data/metadata/scenario_levers_literature.csv) |
| Tables 6–7 | [`leap_growth_variants.csv`](data/metadata/leap_growth_variants.csv), [`leap_ippu_sensitivity_growth_rates_crt2026.csv`](data/processed/leap_ippu_sensitivity_growth_rates_crt2026.csv) |
| Table 8 | [`leap_ippu_historical_activity_growth_2012_2024_crt2026.csv`](data/processed/leap_ippu_historical_activity_growth_2012_2024_crt2026.csv) |
| Table 9 | [`inventory_submissions_ippu_comparison_1990_2021_crt2026.csv`](data/processed/inventory_submissions_ippu_comparison_1990_2021_crt2026.csv) |
| Table 10 | [`crt_ippu_subcategory_emissions_1990_2023_crt2025.csv`](data/processed/crt_ippu_subcategory_emissions_1990_2023_crt2025.csv), [`crt_ippu_subcategory_emissions_1990_2024_crt2026.csv`](data/processed/crt_ippu_subcategory_emissions_1990_2024_crt2026.csv) |
| Table 11 | [`ippu_process_comparability_2021.csv`](data/processed/ippu_process_comparability_2021.csv), [`bns_vs_crt_2025_activity_comparison_2021.csv`](data/processed/bns_vs_crt_2025_activity_comparison_2021.csv), [`bns_index_2024_check_crt2026.csv`](data/processed/bns_index_2024_check_crt2026.csv) |
| Table 12 | [`leap_ippu_scenario_results_2024_2050_crt2026.csv`](data/processed/leap_ippu_scenario_results_2024_2050_crt2026.csv), [`leap_ippu_2a4_mineral_variant_crt2026.csv`](data/processed/leap_ippu_2a4_mineral_variant_crt2026.csv) |
| Table 13 | [`leap_ippu_scenarios_two_bases_2030_2050_crt2026.csv`](data/processed/leap_ippu_scenarios_two_bases_2030_2050_crt2026.csv) |
| Table 14 | [`leap_ippu_sensitivity_summary_2030_2050_crt2026.csv`](data/processed/leap_ippu_sensitivity_summary_2030_2050_crt2026.csv), [`leap_ippu_presented_vs_literature_by_branch_crt2026.csv`](data/processed/leap_ippu_presented_vs_literature_by_branch_crt2026.csv) |
| Table 15 | [`leap_ippu_sensitivity_decomposition_crt2026.csv`](data/processed/leap_ippu_sensitivity_decomposition_crt2026.csv), [`leap_ippu_factor_growth_ratio_by_rate_crt2026.csv`](data/processed/leap_ippu_factor_growth_ratio_by_rate_crt2026.csv) |
| Figures 1–2 | [`ippu_historical_summary_1990_2024_crt2026.csv`](data/processed/ippu_historical_summary_1990_2024_crt2026.csv), [`ippu_category_shares_1990_2024_crt2026.csv`](data/processed/ippu_category_shares_1990_2024_crt2026.csv) |
| Figure 3 | [`crt_2025_vs_crt_2026_total_ippu_comparison_1990_2023_crt2026.csv`](data/processed/crt_2025_vs_crt_2026_total_ippu_comparison_1990_2023_crt2026.csv) |
| Figures 4–5 | [`leap_ippu_scenario_results_2024_2050_crt2026.csv`](data/processed/leap_ippu_scenario_results_2024_2050_crt2026.csv) |
| Figures 6–7 | [`leap_ippu_sensitivity_2024_2050_crt2026.csv`](data/processed/leap_ippu_sensitivity_2024_2050_crt2026.csv), [`leap_ippu_sensitivity_tornado_2050_crt2026.csv`](data/processed/leap_ippu_sensitivity_tornado_2050_crt2026.csv) |

Files with the suffix `_crt2026` belong to the article; files without it or with `_crt2025` hold the CRF 2023 and CRT 2025 values used for the comparison of reporting cycles and for Table 13.

### 2. Reproduce the results

- **Requirements.** Python 3.11 or later with `openpyxl` and `matplotlib` (`pip install -r requirements.txt`).
- **Without downloads.** The commands below use only the files in this repository and reproduce the processed CSV files, the LEAP workbook and Figures 1–7.

```bash
python scripts/compare_unfccc_versions.py --pair crt2025_crt2026
python scripts/compare_unfccc_versions.py --pair three_submissions
python scripts/analyze_ippu_timeseries.py --inventory crt2026
python scripts/build_leap_parameters.py --inventory crt2026
python scripts/fill_leap_import_template.py outputs/leap_ippu_import/Kazakhstan_IPPU_LEAP_final_import.xlsx outputs/leap_ippu_import/Kazakhstan_IPPU_LEAP_import_crt2026.xlsx --parameters data/metadata/leap_scenario_parameters_crt2026.csv
python scripts/analyze_leap_scenarios.py --inventory crt2026
python scripts/analyze_leap_sensitivity.py
```

- **From the original submissions.** The extraction scripts (`extract_ippu_emissions.py`, `extract_ippu_activity_data.py`, `extract_crt_subcategory_emissions.py`, `extract_crt_2a4_subcategories.py`) read the UNFCCC files, which are not distributed here. Download them from the URLs in [`source_registry.csv`](data/metadata/source_registry.csv) and save them under the listed `raw_file_path` in `data/raw/`.

### 3. Use the model in LEAP

The model was implemented in LEAP 2026.5.0.1 (Stockholm Environment Institute). [`Kazakhstan_IPPU_LEAP_import_crt2026.xlsx`](outputs/leap_ippu_import/Kazakhstan_IPPU_LEAP_import_crt2026.xlsx) holds the Current Accounts (2024) and the `Interp()` expressions of the Baseline, Moderate and Ambitious scenarios for the 15 branches. CO2 branches are in metric tonnes; the CH4 branch of ferroalloys and the N2O branch of nitric acid are in kilograms, the unit of the LEAP template. [`Kazakhstan_IPPU_LEAP_final_import.xlsx`](outputs/leap_ippu_import/Kazakhstan_IPPU_LEAP_final_import.xlsx) is the LEAP export used as the template; it keeps the earlier CRT 2025 proxy values.

## Structure

```text
.
├── data/
│   ├── processed/    # CSV extractions, comparisons, scenario and sensitivity results
│   └── metadata/     # scenario parameters, literature factors, growth variants, source registry
├── figures/           # Figures 1–7 of the article
├── outputs/
│   └── leap_ippu_import/   # LEAP import workbook and template
├── scripts/           # extraction, comparison, scenarios and sensitivity
├── LICENSE            # MIT, code
├── LICENSE-DATA       # CC BY 4.0, data and figures
└── requirements.txt
```

## Sources

- UNFCCC: Kazakhstan CRT 2026 and NID 2026; CRT 2025, CRF 2023 and NID 2025 for the comparison of reporting cycles;
- Bureau of National Statistics of the Republic of Kazakhstan (BNS), production statistics;
- IPCC 2006 Guidelines and 2019 Refinement, Volume 3 (IPPU); IPCC AR5 GWP100 (CRT) and AR4 GWP100 (CRF 2023);
- published pathways behind the scenario factors (IEA, IPCC AR6, EU BREF, industry roadmaps, Kazakhstan studies), with page or table for every value in [`scenario_levers_literature.csv`](data/metadata/scenario_levers_literature.csv).

URLs of all sources are in [`source_registry.csv`](data/metadata/source_registry.csv).

## Citation

Please cite the article once it is published, together with this repository. The repository DOI will be added on release.

## License

- **Code** in `scripts/`: [MIT License](LICENSE).
- **Data, figures and documentation**: [Creative Commons Attribution 4.0 International](LICENSE-DATA).

The processed files are derived from public UNFCCC and BNS sources, which keep their own terms of use. The license covers the authors' processing, harmonisation and scenario results; when using a value, cite the primary source and keep the submission year, units and GWP framework.
