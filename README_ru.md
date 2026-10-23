<div align="center">

# Процессные выбросы промышленности Казахстана

### Данные и код к статье о согласовании кадастра и исследовательских траекториях LEAP до 2050 г.

**Язык:** [Русский](README_ru.md) · [English](README.md)

Zarina Nurzhanova, Ayagoz Khamzina, Nurkhat Zhakiyev  
Astana IT University, Astana, Kazakhstan

[![Статус — статья на рецензировании](https://img.shields.io/badge/статус-статья%20на%20рецензировании-f9a825)](#цитирование)
[![Охват — Казахстан, 1990–2024](https://img.shields.io/badge/охват-Казахстан%2C%201990–2024-1565c0)](data/processed/ippu_historical_summary_1990_2024_crt2026.csv)
[![Сектор — МГЭИК 2 IPPU](https://img.shields.io/badge/сектор-МГЭИК%202%20IPPU-6a1b9a)](data/metadata/leap_scenario_parameters_crt2026.csv)
[![Код — MIT](https://img.shields.io/badge/код-MIT-455a64)](LICENSE)
[![Данные — CC BY 4.0](https://img.shields.io/badge/данные-CC%20BY%204.0-455a64)](LICENSE-DATA)

</div>

> [!IMPORTANT]
> Репозиторий сопровождает статью *Industrial process emissions in Kazakhstan: inventory harmonisation and exploratory LEAP pathways to 2050*. В нём собраны обработанные данные, параметры, рисунки, книга импорта LEAP и скрипты, на которые ссылается статья. Пути к файлам совпадают с указанными в таблицах статьи и в разделе Data availability.

## О проекте

Исследование использует представление кадастра парниковых газов Казахстана в РКИК ООН 2026 г. (CRT 2026, 1990–2024 гг.), сравнивает его с циклами отчётности CRF 2023 и CRT 2025 и строит модель LEAP из 15 ветвей процессных выбросов минеральной, металлургической и химической промышленности:

```text
представления кадастра → извлечение рядов → сравнение циклов отчётности → сверка с национальной статистикой → база 2024 г. → траектории LEAP и чувствительность
```

Модель охватывает 22 088 тыс. т CO2-экв., или 85.6% выбросов IPPU в 2024 г. F-газы, ПФУ алюминия, ряд малых источников IPPU и сжигание топлива в промышленности в границу не входят. Все значения — в тыс. т CO2-экв. с GWP100 из AR5 (CO2 = 1, CH4 = 28, N2O = 265).

> [!WARNING]
> Траектории исследовательские, это не прогноз. Множители остаточных выбросов — заданные авторами огибающие, проверенные по опубликованным траекториям; это не официальные цели, не технологические потенциалы и не решение минимальной стоимости.

## Основные сценарии

| Сценарий | 2030, тыс. т CO2-экв. | 2050, тыс. т CO2-экв. |
|---|---:|---:|
| Baseline | 22 088 | 22 088 |
| Moderate mitigation | 20 006 | 15 463 |
| Ambitious mitigation | 17 247 | 9 979 |

Постоянная активность; категория 2.A.4 (прочее использование карбонатов) оставлена с f = 1.00. Источник: [`leap_ippu_scenario_results_2024_2050_crt2026.csv`](data/processed/leap_ippu_scenario_results_2024_2050_crt2026.csv). Варианты роста активности, множители по литературе и анализ «по одному допущению» — в файлах `leap_ippu_sensitivity_*_crt2026.csv`.

## Быстрый старт

### 1. Найти данные к таблице или рисунку

| Статья | Файлы |
|---|---|
| Табл. 1–3 | [`leap_scenario_parameters_crt2026.csv`](data/metadata/leap_scenario_parameters_crt2026.csv), [`leap_scenario_parameters.csv`](data/metadata/leap_scenario_parameters.csv), [`unfccc_ippu_emissions_1990_2024_crt2026.csv`](data/processed/unfccc_ippu_emissions_1990_2024_crt2026.csv) |
| Табл. 4 | [`crt_2a4_subcategories_1990_2024_crt2026.csv`](data/processed/crt_2a4_subcategories_1990_2024_crt2026.csv) |
| Табл. 5 | [`leap_sensitivity_factors.csv`](data/metadata/leap_sensitivity_factors.csv), [`scenario_levers_literature.csv`](data/metadata/scenario_levers_literature.csv) |
| Табл. 6–7 | [`leap_growth_variants.csv`](data/metadata/leap_growth_variants.csv), [`leap_ippu_sensitivity_growth_rates_crt2026.csv`](data/processed/leap_ippu_sensitivity_growth_rates_crt2026.csv) |
| Табл. 8 | [`leap_ippu_historical_activity_growth_2012_2024_crt2026.csv`](data/processed/leap_ippu_historical_activity_growth_2012_2024_crt2026.csv) |
| Табл. 9 | [`inventory_submissions_ippu_comparison_1990_2021_crt2026.csv`](data/processed/inventory_submissions_ippu_comparison_1990_2021_crt2026.csv) |
| Табл. 10 | [`crt_ippu_subcategory_emissions_1990_2023_crt2025.csv`](data/processed/crt_ippu_subcategory_emissions_1990_2023_crt2025.csv), [`crt_ippu_subcategory_emissions_1990_2024_crt2026.csv`](data/processed/crt_ippu_subcategory_emissions_1990_2024_crt2026.csv) |
| Табл. 11 | [`ippu_process_comparability_2021.csv`](data/processed/ippu_process_comparability_2021.csv), [`bns_vs_crt_2025_activity_comparison_2021.csv`](data/processed/bns_vs_crt_2025_activity_comparison_2021.csv), [`bns_index_2024_check_crt2026.csv`](data/processed/bns_index_2024_check_crt2026.csv) |
| Табл. 12 | [`leap_ippu_scenario_results_2024_2050_crt2026.csv`](data/processed/leap_ippu_scenario_results_2024_2050_crt2026.csv), [`leap_ippu_2a4_mineral_variant_crt2026.csv`](data/processed/leap_ippu_2a4_mineral_variant_crt2026.csv) |
| Табл. 13 | [`leap_ippu_scenarios_two_bases_2030_2050_crt2026.csv`](data/processed/leap_ippu_scenarios_two_bases_2030_2050_crt2026.csv) |
| Табл. 14 | [`leap_ippu_sensitivity_summary_2030_2050_crt2026.csv`](data/processed/leap_ippu_sensitivity_summary_2030_2050_crt2026.csv), [`leap_ippu_presented_vs_literature_by_branch_crt2026.csv`](data/processed/leap_ippu_presented_vs_literature_by_branch_crt2026.csv) |
| Табл. 15 | [`leap_ippu_sensitivity_decomposition_crt2026.csv`](data/processed/leap_ippu_sensitivity_decomposition_crt2026.csv), [`leap_ippu_factor_growth_ratio_by_rate_crt2026.csv`](data/processed/leap_ippu_factor_growth_ratio_by_rate_crt2026.csv) |
| Рис. 1–2 | [`ippu_historical_summary_1990_2024_crt2026.csv`](data/processed/ippu_historical_summary_1990_2024_crt2026.csv), [`ippu_category_shares_1990_2024_crt2026.csv`](data/processed/ippu_category_shares_1990_2024_crt2026.csv) |
| Рис. 3 | [`crt_2025_vs_crt_2026_total_ippu_comparison_1990_2023_crt2026.csv`](data/processed/crt_2025_vs_crt_2026_total_ippu_comparison_1990_2023_crt2026.csv) |
| Рис. 4–5 | [`leap_ippu_scenario_results_2024_2050_crt2026.csv`](data/processed/leap_ippu_scenario_results_2024_2050_crt2026.csv) |
| Рис. 6–7 | [`leap_ippu_sensitivity_2024_2050_crt2026.csv`](data/processed/leap_ippu_sensitivity_2024_2050_crt2026.csv), [`leap_ippu_sensitivity_tornado_2050_crt2026.csv`](data/processed/leap_ippu_sensitivity_tornado_2050_crt2026.csv) |

Файлы с суффиксом `_crt2026` относятся к статье; файлы без суффикса или с `_crt2025` содержат значения CRF 2023 и CRT 2025 для сравнения циклов отчётности и табл. 13.

### 2. Воспроизвести результаты

- **Требования.** Python 3.11 или новее с `openpyxl` и `matplotlib` (`pip install -r requirements.txt`).
- **Без скачивания.** Команды ниже используют только файлы репозитория и воспроизводят обработанные CSV, книгу LEAP и рисунки 1–7.

```bash
python scripts/compare_unfccc_versions.py --pair crt2025_crt2026
python scripts/compare_unfccc_versions.py --pair three_submissions
python scripts/analyze_ippu_timeseries.py --inventory crt2026
python scripts/build_leap_parameters.py --inventory crt2026
python scripts/fill_leap_import_template.py outputs/leap_ippu_import/Kazakhstan_IPPU_LEAP_final_import.xlsx outputs/leap_ippu_import/Kazakhstan_IPPU_LEAP_import_crt2026.xlsx --parameters data/metadata/leap_scenario_parameters_crt2026.csv
python scripts/analyze_leap_scenarios.py --inventory crt2026
python scripts/analyze_leap_sensitivity.py
```

- **Из исходных представлений.** Скрипты извлечения (`extract_ippu_emissions.py`, `extract_ippu_activity_data.py`, `extract_crt_subcategory_emissions.py`, `extract_crt_2a4_subcategories.py`) читают файлы РКИК ООН, которые здесь не распространяются. Скачайте их по ссылкам из [`source_registry.csv`](data/metadata/source_registry.csv) и сохраните в `data/raw/` по пути из столбца `raw_file_path`.

### 3. Использовать модель в LEAP

Модель реализована в LEAP 2026.5.0.1 (Stockholm Environment Institute). [`Kazakhstan_IPPU_LEAP_import_crt2026.xlsx`](outputs/leap_ippu_import/Kazakhstan_IPPU_LEAP_import_crt2026.xlsx) содержит текущие счета (2024 г.) и выражения `Interp()` сценариев Baseline, Moderate и Ambitious для 15 ветвей. Ветви CO2 заданы в метрических тоннах; ветвь CH4 ферросплавов и ветвь N2O азотной кислоты — в килограммах, единице шаблона LEAP. [`Kazakhstan_IPPU_LEAP_final_import.xlsx`](outputs/leap_ippu_import/Kazakhstan_IPPU_LEAP_final_import.xlsx) — экспорт LEAP, использованный как шаблон; в нём сохранены прежние значения базы CRT 2025 proxy.

## Структура

```text
.
├── data/
│   ├── processed/    # извлечённые ряды, сравнения, результаты сценариев и чувствительности
│   └── metadata/     # параметры сценариев, множители по литературе, варианты роста, реестр источников
├── figures/           # рисунки 1–7 статьи
├── outputs/
│   └── leap_ippu_import/   # книга импорта LEAP и шаблон
├── scripts/           # извлечение, сравнение, сценарии и чувствительность
├── LICENSE            # MIT, код
├── LICENSE-DATA       # CC BY 4.0, данные и рисунки
└── requirements.txt
```

## Источники

- РКИК ООН: CRT 2026 и NID 2026 Казахстана; CRT 2025, CRF 2023 и NID 2025 для сравнения циклов отчётности;
- Бюро национальной статистики Республики Казахстан (БНС), статистика производства;
- Руководящие принципы МГЭИК 2006 г. и уточнение 2019 г., том 3 (IPPU); GWP100 из AR5 (CRT) и AR4 (CRF 2023);
- опубликованные траектории, на которых основаны множители сценариев (IEA, МГЭИК AR6, EU BREF, отраслевые дорожные карты, исследования по Казахстану), со страницей или таблицей для каждого значения в [`scenario_levers_literature.csv`](data/metadata/scenario_levers_literature.csv).

Ссылки на все источники — в [`source_registry.csv`](data/metadata/source_registry.csv).

## Цитирование

После публикации цитируйте статью вместе с этим репозиторием. DOI репозитория будет добавлен при выпуске.

## Лицензия

- **Код** в `scripts/`: [MIT License](LICENSE).
- **Данные, рисунки и документация**: [Creative Commons Attribution 4.0 International](LICENSE-DATA).

Обработанные файлы получены из открытых источников РКИК ООН и БНС, у которых свои условия использования. Лицензия распространяется на обработку, согласование и сценарные результаты авторов; при использовании значения указывайте первичный источник и сохраняйте год представления, единицы и систему GWP.
