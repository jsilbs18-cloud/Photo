# Raw Data Sources for Multi-Sector Deal Analysis — Direct Dataset Links

Direct links to specific downloadable datasets and APIs across energy, nuclear, pharma,
minerals/mining, and cross-sector deal research. Nearly everything below is free and comes as
CSV/Excel bulk downloads or a documented API, ready to pull into Excel, Tableau, Power BI, or
Python for mapping and modeling.

*Links compiled and checked against current sources July 2026. Government URLs occasionally move —
if one breaks, the dataset name + agency in a search engine will find the new home.*

---

## Energy (power, oil & gas, renewables)

| Dataset | Link | What it is |
|---|---|---|
| EIA Form EIA-860 | https://www.eia.gov/electricity/data/eia860/ | Generator-level data for every U.S. power plant ≥1 MW (capacity, fuel, location, owner, planned units). Yearly ZIPs of Excel files, 1990–present. |
| EIA Form EIA-923 | https://www.eia.gov/electricity/data/eia923/ | Plant-level monthly generation, fuel consumption, and fuel receipts/costs. Yearly ZIPped Excel. |
| EIA Open Data API | https://www.eia.gov/opendata/ | Free API (register for key) covering all EIA series — electricity, petroleum, gas, coal, prices. JSON. |
| EIA bulk data files | https://www.eia.gov/opendata/bulkfiles.php | Entire EIA datasets as single ZIP downloads. |
| EIA petroleum data hub | https://www.eia.gov/petroleum/data.php | Raw petroleum supply, production, stocks, and price tables. XLS/CSV/API. |
| EPA eGRID | https://www.epa.gov/egrid/download-data | Emissions, heat rates, and resource mix for every U.S. plant. Annual Excel workbooks. |
| EPA CAMPD custom download | https://campd.epa.gov/data/custom-data-download | Hourly stack-level (CEMS) emissions data; bulk files at https://campd.epa.gov/data/bulk-data-files. CSV. |
| FERC Form 1 | https://www.ferc.gov/general-information-0/electric-industry-forms/form-1-electric-utility-annual-report | Utility annual financial/operating reports (XBRL for 2021+; historical DB files linked from the page). |
| Global Energy Monitor trackers | https://globalenergymonitor.org/download-data | Unit-level spreadsheets of every coal/gas/wind/solar plant worldwide **with coordinates** — ideal for mapping. Free XLSX behind a short email form. |
| Ember yearly electricity data | https://ember-energy.org/data/yearly-electricity-data/ | Generation, capacity, emissions, demand for 200+ countries. Free CSV; monthly version at https://ember-energy.org/data/monthly-electricity-data/. |
| Energy Institute Statistical Review | https://www.energyinst.org/statistical-review/resources-and-data-downloads | Global energy production/consumption by country and fuel, 1965–present. One consolidated Excel workbook. |
| NREL Annual Technology Baseline | https://atb.nrel.gov/electricity/2025/data | Technology cost/performance projections (solar, wind, storage, gas…). Excel/CSV/Parquet. Check for a newer edition — URL pattern is /electricity/&lt;year&gt;/data. |
| Our World in Data energy | https://github.com/owid/energy-data | Cleaned country-year panel merging EI, EIA, and Ember data. Direct CSV: https://owid-public.owid.io/data/energy/owid-energy-data.csv |

## Nuclear

| Dataset | Link | What it is |
|---|---|---|
| IAEA PRIS country statistics | https://pris.iaea.org/pris/countrystatistics/countrystatisticslandingpage.aspx | The canonical database of every power reactor on Earth — status, capacity, operator, generation history. Reactors-by-status list: https://pris.iaea.org/pris/worldstatistics/operationalreactorsbycountry.aspx |
| IAEA "Nuclear Power Reactors in the World" | https://www.iaea.org/publications/15943/nuclear-power-reactors-in-the-world | Annual RDS-2 reference publication with full reactor tables (2025 edition, data through end-2024). PDF. |
| NRC daily power reactor status | https://www.nrc.gov/reading-rm/doc-collections/event-status/reactor-status/index | Daily % power for every U.S. reactor — raw text files, last 365 days plus yearly archives back to 2000. |
| NRC list of power reactor units | https://www.nrc.gov/reactors/operating/list-power-reactor-units | All licensed U.S. units with docket, type, location, owner/operator. |
| EIA nuclear & uranium data | https://www.eia.gov/nuclear/data.php | U.S. nuclear generation, capacity, daily outages. XLS/CSV/API. |
| EIA Uranium Marketing Annual | https://www.eia.gov/uranium/marketing/ | U.S. utility uranium purchases, prices, and contract data. XLS tables. |
| Cameco uranium prices | https://www.cameco.com/invest/markets/uranium-price | Free monthly spot and long-term uranium price indicators (UxC/TradeTech averages). |
| Global Energy Monitor Nuclear Tracker | https://globalenergymonitor.org/projects/global-nuclear-power-tracker/download-data/ | ~1,750 nuclear units worldwide with status, capacity, coordinates, owner. Free XLSX. |
| World Nuclear Performance Report | https://world-nuclear.org/our-association/publications/global-trends-reports/world-nuclear-performance-report | Annual industry performance report; browsable reactor database at https://world-nuclear.org/nuclear-reactor-database/summary |
| NRC ADAMS document search | https://adams-search.nrc.gov/ | Full-text search of 3M+ NRC licensing and inspection documents. |

## Pharma / Life Sciences

| Dataset | Link | What it is |
|---|---|---|
| openFDA drug APIs | https://open.fda.gov/apis/drug/ | APIs for approvals, labels, adverse events (FAERS), recalls, NDC directory, shortages. JSON; bulk downloads: https://open.fda.gov/apis/downloads |
| FDA Orange Book data files | https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files | Every approved drug with **patent and exclusivity expirations** — the key file for generic-entry / LOE analysis. ZIP of tab-delimited text. |
| FDA Purple Book | https://purplebooksearch.fda.gov/downloads | All licensed biologics with biosimilar/interchangeable status and exclusivity. CSV/Excel. |
| Drugs@FDA data files | https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files | Every drug approval since 1939. Weekly-updated ZIP of tab-delimited tables. |
| ClinicalTrials.gov API v2 | https://clinicaltrials.gov/data-api/api | REST API for every registered trial — phase, sponsor, indication, status, results. JSON. Bulk download of all records: https://clinicaltrials.gov/data-api/how-download-study-records |
| CMS Medicare Part D spending by drug | https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug | Annual Medicare spending per drug. CSV + API. |
| CMS NADAC drug pricing | https://www.medicaid.gov/medicaid/nadac | Weekly retail pharmacy drug acquisition costs by NDC. CSV + API via data.medicaid.gov. |
| CMS Open Payments | https://openpaymentsdata.cms.gov/datasets | All industry payments to physicians and teaching hospitals. ZIP/CSV per program year. |
| NIH RePORTER ExPORTER | https://reporter.nih.gov/exporter | Bulk NIH grant data (projects, abstracts, patents, linked publications) by fiscal year. Zipped CSV. |
| PatentsView | https://patentsview.org/downloads/data-downloads | Full USPTO patent data as bulk TSV tables; search API docs: https://search.patentsview.org/docs/ |
| EMA medicines data | https://www.ema.europa.eu/en/medicines/download-medicine-data | Spreadsheet of all EMA-authorised medicines and their assessment reports. XLSX. |

## Minerals / Mining

| Dataset | Link | What it is |
|---|---|---|
| USGS Mineral Commodity Summaries 2026 | https://pubs.usgs.gov/periodicals/mcs2026/mcs2026.pdf | Production, reserves, and prices for 90+ commodities by country — the starting point for any minerals market map. CSV data release: https://www.sciencebase.gov/catalog/item/696a75d5d4be0228872d3bf8 |
| USGS Minerals Yearbook | https://www.usgs.gov/publications/minerals-yearbook-volume-i-metals-and-minerals | Deep annual chapters per commodity with statistical tables. PDF + XLSX. |
| USGS MRDS / USMIN deposit databases | https://mrdata.usgs.gov/mrds/ | Mineral deposits worldwide **with coordinates** (shapefile/CSV/KML); successor U.S. database: https://mrdata.usgs.gov/deposit/ |
| SEDAR+ filings search | https://www.sedarplus.ca/ | Canadian filings including **NI 43-101 technical reports** — full geology, resource estimates, and project economics for most of the world's mining projects. Free PDFs. |
| BGS World Mineral Statistics | https://www.bgs.ac.uk/mineralsuk/statistics/world-mineral-statistics/world-mineral-statistics-data-download/ | World mineral production by country, 70+ commodities. Excel extract tool + API. |
| World Bank Pink Sheet | https://www.worldbank.org/en/research/commodity-markets | Monthly commodity prices (metals, energy, ag) back to 1960. XLSX. |
| LME market data | https://www.lme.com/en/market-data | Free delayed metals prices and warehouse stocks (registration required); historical: https://www.lme.com/market-data/accessing-market-data/historical-data |
| Geoscience Australia OZMIN | https://portal.ga.gov.au/ | 1,000+ Australian mineral deposits across ~60 commodities. CSV/geodatabase; also mirrored on data.gov.au. |

## Cross-Sector: Filings, Macro, Trade

| Dataset | Link | What it is |
|---|---|---|
| SEC EDGAR full-text search | https://www.sec.gov/edgar/search/ | Search every U.S. filing since 2001 — 10-Ks, 8-K deal announcements, S-1s, 13D/G stakes, merger proxies. |
| SEC EDGAR APIs & bulk data | https://www.sec.gov/search-filings/edgar-application-programming-interfaces | Free JSON APIs (data.sec.gov) plus nightly bulk ZIPs of all company facts and submissions. |
| FRED API | https://fred.stlouisfed.org/docs/api/fred/ | 800k+ macro and commodity time series. Free key; every series also downloadable as CSV from its page. |
| UN Comtrade | https://comtradeplus.un.org/ | Bilateral trade flows by commodity code — maps who buys/sells uranium, lithium, APIs, etc. between countries. API portal: https://comtradedeveloper.un.org/ |
| USAspending custom download | https://www.usaspending.gov/download_center/custom_award_data | Every U.S. federal contract and grant, filterable, as CSV ZIPs. Open API (no key): https://api.usaspending.gov/ |
| World Bank Indicators API | https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation | ~16,000 country-level economic series. JSON/XML, no key required. |

## Paid platforms (when free data runs out)

Standard tools deal teams buy for private-company coverage, cost curves, and convenience:
**Bloomberg, S&P Capital IQ Pro, PitchBook, LSEG/Refinitiv** (deals & comps);
**Wood Mackenzie, Rystad** (energy assets); **CRU, Benchmark Mineral Intelligence** (metals/battery);
**Evaluate Pharma, IQVIA, Citeline** (drug forecasts & pipelines);
**UxC, TradeTech** (uranium price benchmarks).

---

## Practical notes for deal mapping

- **Asset-level + coordinates = maps.** EIA-860, Global Energy Monitor trackers, IAEA PRIS, and
  USGS MRDS/USMIN all include locations — plants, reactors, and mines can be dropped straight onto a map.
- **Follow the filings.** For any specific target: EDGAR (US) and SEDAR+ (Canada) contain more raw
  operational detail than any aggregator — especially NI 43-101 and S-K 1300 technical reports for miners.
- **APIs beat scraping.** EIA, openFDA, ClinicalTrials.gov, FRED, Comtrade, and EDGAR all have free
  documented APIs — easy to automate refreshes for a living dashboard.
