# Industrial process emissions in Kazakhstan: data and code

Data, parameters and scripts for the article *Industrial process emissions in Kazakhstan: inventory harmonisation and exploratory LEAP pathways to 2050* (Zarina Nurzhanova, Ayagoz Khamzina, Nurkhat Zhakiyev; manuscript under review).

The analysis uses Kazakhstan's 2026 greenhouse-gas inventory submission to the UNFCCC (CRT 2026, 1990–2024) and compares it with the CRF 2023 and CRT 2025 submissions. The LEAP model covers 15 process-emission branches of mineral, metal and chemical industry (85.6% of 2024 IPPU emissions). All values are in kt CO2eq with AR5 GWP100 (CO2 = 1, CH4 = 28, N2O = 265).

## Contents

| Folder | Content |
|---|---|
| `data/processed/` | CSV files from which every number, table and figure of the article is taken. Files with the suffix `_crt2026` belong to the article; files without it or with `_crt2025` hold the CRF 2023 and CRT 2025 values used for the comparison of reporting cycles. |
| `data/metadata/` | Scenario parameters, literature-based factors (entries L01–L36 with page or table), activity-growth variants, 2.A.4 variants and the source registry with URLs. |
| `figures/` | Figures 1–7 of the article (PNG, 300 dpi). |
| `outputs/leap_ippu_import/` | `Kazakhstan_IPPU_LEAP_import_crt2026.xlsx`: LEAP import workbook (Current Accounts and `Interp()` expressions for Baseline, Moderate and Ambitious). `Kazakhstan_IPPU_LEAP_final_import.xlsx` is the LEAP export used as the template; it keeps the earlier CRT 2025 proxy values. |
| `scripts/` | Extraction, analysis and figure scripts. |

## Tables and figures

| Article | Files |
|---|---|
| Table 1, Table 2 | `data/metadata/leap_scenario_parameters_crt2026.csv`, `leap_scenario_parameters.csv`; `data/processed/unfccc_ippu_emissions_1990_2024_crt2026.csv` |
| Table 3 | `data/metadata/leap_scenario_parameters_crt2026.csv` |
| Table 4 | `data/processed/crt_2a4_subcategories_1990_2024_crt2026.csv` |
| Table 5 | `data/metadata/leap_sensitivity_factors.csv`, `scenario_levers_literature.csv` |
| Table 6, Table 7 | `data/metadata/leap_growth_variants.csv`, `data/processed/leap_ippu_sensitivity_growth_rates_crt2026.csv` |
| Table 8 | `data/processed/leap_ippu_historical_activity_growth_2012_2024_crt2026.csv` |
| Table 9 | `data/processed/inventory_submissions_ippu_comparison_1990_2021_crt2026.csv` |
| Table 10 | `data/processed/crt_ippu_subcategory_emissions_1990_2023_crt2025.csv`, `crt_ippu_subcategory_emissions_1990_2024_crt2026.csv` |
| Table 11 | `data/processed/ippu_process_comparability_2021.csv`, `bns_vs_crt_2025_activity_comparison_2021.csv`, `bns_index_2024_check_crt2026.csv` |
| Table 12 | `data/processed/leap_ippu_scenario_results_2024_2050_crt2026.csv`, `leap_ippu_2a4_mineral_variant_crt2026.csv` |
| Table 13 | `data/processed/leap_ippu_scenarios_two_bases_2030_2050_crt2026.csv` |
| Table 14 | `data/processed/leap_ippu_sensitivity_summary_2030_2050_crt2026.csv`, `leap_ippu_presented_vs_literature_by_branch_crt2026.csv` |
| Table 15 | `data/processed/leap_ippu_sensitivity_decomposition_crt2026.csv`, `leap_ippu_factor_growth_ratio_by_rate_crt2026.csv` |
| Figures 1–2 | `data/processed/ippu_historical_summary_1990_2024_crt2026.csv`, `ippu_category_shares_1990_2024_crt2026.csv` |
| Figure 3 | `data/processed/crt_2025_vs_crt_2026_total_ippu_comparison_1990_2023_crt2026.csv` |
| Figures 4–5 | `data/processed/leap_ippu_scenario_results_2024_2050_crt2026.csv` |
| Figures 6–7 | `data/processed/leap_ippu_sensitivity_2024_2050_crt2026.csv`, `leap_ippu_sensitivity_tornado_2050_crt2026.csv` |

## Reproducing the results

Python 3.11 or later:

```
pip install -r requirements.txt
```

Run from the repository root. The following steps use only the files in this repository and reproduce the processed CSV files, the LEAP workbook and Figures 1–7:

```
python scripts/compare_unfccc_versions.py --pair crt2025_crt2026
python scripts/compare_unfccc_versions.py --pair three_submissions
python scripts/analyze_ippu_timeseries.py --inventory crt2026
python scripts/build_leap_parameters.py --inventory crt2026
python scripts/fill_leap_import_template.py outputs/leap_ippu_import/Kazakhstan_IPPU_LEAP_final_import.xlsx outputs/leap_ippu_import/Kazakhstan_IPPU_LEAP_import_crt2026.xlsx --parameters data/metadata/leap_scenario_parameters_crt2026.csv
python scripts/analyze_leap_scenarios.py --inventory crt2026
python scripts/analyze_leap_sensitivity.py
```

The model was implemented in LEAP 2026.5.0.1 (Stockholm Environment Institute). The scenario results are computed with LEAP's deterministic `Interp()` expressions and reproduced in Python by `analyze_leap_scenarios.py`.

## Source data

The original inventory files are not included. To rebuild the inventory extracts (`extract_ippu_emissions.py`, `extract_ippu_activity_data.py`, `extract_crt_subcategory_emissions.py`, `extract_crt_2a4_subcategories.py`), download them from the UNFCCC and place them under `data/raw/` as listed in `data/metadata/source_registry.csv`:

- CRT 2026 (1990–2024), Kazakhstan: https://unfccc.int/documents/656739 → `data/raw/unfccc_crt_2026/KAZ-CRT-2026-V1.0.zip`
- CRT 2025 (1990–2023) and CRF 2023 (1990–2021): UNFCCC reports page for Kazakhstan (links in the registry)
- National Inventory Documents 2025 and 2026: https://unfccc.int/documents/646542, https://unfccc.int/documents/656738

Production statistics come from the Bureau of National Statistics of the Republic of Kazakhstan (https://stat.gov.kz). The literature behind the scenario factors is listed with page numbers in `data/metadata/scenario_levers_literature.csv`.

## Citation

Please cite the article once published. Repository DOI: to be added.

## License

To be added.
