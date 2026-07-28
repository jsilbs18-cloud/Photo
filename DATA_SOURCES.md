# Raw Data Sources for Multi-Sector Deal Analysis

A reference guide to free (and a few industry-standard paid) sources of raw, downloadable data
across energy, nuclear, pharma, minerals/mining, and cross-sector deal research. Nearly every
free source below offers bulk CSV/Excel downloads or a public API, so the data can be pulled
into Excel, Tableau, Power BI, or Python for mapping and modeling.

---

## Energy (power, oil & gas, renewables)

| Source | What you get | Access |
|---|---|---|
| **U.S. EIA** — [eia.gov](https://www.eia.gov) | The single best free energy dataset: electricity generation/capacity, petroleum, natural gas, coal, prices, consumption, forecasts. Forms EIA-860/EIA-923 give plant-level and generator-level detail for every U.S. power plant. | Free API (`api.eia.gov`, register for key) + bulk CSV/Excel downloads |
| **FERC** — [ferc.gov](https://www.ferc.gov) | Utility financials (Form 1), electric quarterly reports, gas pipeline filings, rate cases | Free downloads (eLibrary, eForms) |
| **EPA eGRID & CAMPD** — [epa.gov/egrid](https://www.epa.gov/egrid), [campd.epa.gov](https://campd.epa.gov) | Emissions, heat rates, and fuel data for every U.S. power plant; hourly stack-level emissions (CEMS) | Free bulk downloads + API |
| **NREL** — [nrel.gov](https://www.nrel.gov) | Renewable resource maps (solar/wind), Annual Technology Baseline (cost/performance by technology) | Free API + downloads |
| **Global Energy Monitor** — [globalenergymonitor.org](https://globalenergymonitor.org) | Worldwide asset-level trackers: every coal/gas/wind/solar/nuclear plant, pipelines, LNG terminals, steel plants — with lat/long coordinates, ideal for mapping | Free spreadsheet downloads |
| **Ember** — [ember-energy.org](https://ember-energy.org) | Global electricity generation and emissions by country/fuel, monthly | Free CSVs |
| **Energy Institute Statistical Review** (formerly BP) | Long-run global energy production/consumption by country and fuel | Free Excel workbook, annual |
| **IEA** — [iea.org](https://www.iea.org) | Global energy balances, demand forecasts | Some free; full datasets paid |
| **Our World in Data** — [ourworldindata.org/energy](https://ourworldindata.org/energy) | Cleaned, merged global energy/emissions series | Free CSVs on GitHub |

## Nuclear

| Source | What you get | Access |
|---|---|---|
| **IAEA PRIS** — [pris.iaea.org](https://pris.iaea.org) | The canonical database of every power reactor on Earth: status, type, capacity, operator, generation history, construction dates | Free, browsable + annual reports |
| **U.S. NRC** — [nrc.gov](https://www.nrc.gov) | Daily power reactor status reports, license info, event reports, full document library (ADAMS) | Free downloads |
| **EIA nuclear data** | U.S. nuclear generation, capacity factors, outages, uranium marketing annual (utility uranium purchases and prices) | Free API/CSV |
| **World Nuclear Association** — [world-nuclear.org](https://world-nuclear.org) | Country profiles, reactor database, fuel cycle data | Mostly free |
| **UxC / TradeTech** | Uranium spot and term prices — the industry benchmarks | Paid (Cameco's site republishes UxC spot/term indicators free) |

## Pharma / Life Sciences

| Source | What you get | Access |
|---|---|---|
| **openFDA** — [open.fda.gov](https://open.fda.gov) | Drug approvals, labels, adverse events, recalls, device data | Free API + bulk JSON downloads |
| **Drugs@FDA / Orange Book / Purple Book** | Every approved drug; Orange Book lists patents and exclusivity expirations (key for generics/LOE analysis); Purple Book covers biologics/biosimilars | Free downloadable data files |
| **ClinicalTrials.gov** | All registered clinical trials worldwide: phase, sponsor, indication, status, results | Free API (v2) + full bulk download |
| **CMS** — [data.cms.gov](https://data.cms.gov) | Medicare Part B/D drug spending by drug, drug pricing (NADAC), Open Payments (industry payments to physicians) | Free API + CSV |
| **EMA** — [ema.europa.eu](https://www.ema.europa.eu) | European drug approvals (EPARs), shortages | Free downloads |
| **NIH RePORTER** — [reporter.nih.gov](https://reporter.nih.gov) | Every NIH research grant — useful for spotting early-stage science and academic spinouts | Free API + bulk |
| **PatentsView (USPTO)** — [patentsview.org](https://patentsview.org) | Full U.S. patent data, assignees, citations | Free API + bulk |
| **Evaluate Pharma, IQVIA, Citeline** | Drug sales forecasts, pipeline intelligence, prescription volumes | Paid — industry standard for pharma deal work |

## Minerals / Mining

| Source | What you get | Access |
|---|---|---|
| **USGS National Minerals Information Center** — [usgs.gov/centers/national-minerals-information-center](https://www.usgs.gov/centers/national-minerals-information-center) | Mineral Commodity Summaries (annual production, reserves, prices for ~90 commodities by country) + Minerals Yearbook. The starting point for any minerals market map | Free PDF/Excel |
| **SEDAR+** — [sedarplus.ca](https://www.sedarplus.ca) | Canadian securities filings, including **NI 43-101 technical reports** — full geology, resource/reserve estimates, and economics for mining projects worldwide (most global miners list in Canada) | Free |
| **SEC EDGAR** — [sec.gov/edgar](https://www.sec.gov/edgar) | U.S. filings incl. S-K 1300 technical report summaries for U.S.-listed miners | Free full-text search + API + bulk |
| **USGS MRDS / geologic maps** | Mineral occurrence and deposit database with coordinates — good for mapping | Free downloads |
| **British Geological Survey** — World Mineral Production | Global production statistics by commodity and country | Free |
| **Geoscience Australia / Natural Resources Canada** | National resource inventories, deposit databases, geophysical data | Free |
| **World Bank "Pink Sheet"** | Monthly commodity prices (metals, energy, ag) back decades | Free Excel |
| **LME** — [lme.com](https://www.lme.com) | Metals prices (delayed free; real-time paid) | Mixed |
| **S&P Global Market Intelligence (Capital IQ Pro / Metals & Mining)** | Mine-level production, costs, ownership — the industry standard | Paid |

## Cross-Sector: Companies, Deals, Macro, Trade

| Source | What you get | Access |
|---|---|---|
| **SEC EDGAR** | All U.S. public company filings — 10-Ks, 8-Ks (deal announcements), S-1s, 13D/G (activist stakes), merger proxies | Free API + full-text search + bulk data |
| **FRED** — [fred.stlouisfed.org](https://fred.stlouisfed.org) | 800k+ macro and commodity time series | Free API + CSV |
| **UN Comtrade** — [comtrade.un.org](https://comtrade.un.org) | Bilateral trade flows by commodity code — excellent for mapping who buys/sells what (e.g., uranium, lithium, APIs) between countries | Free API |
| **World Bank / IMF / OECD / Eurostat open data** | Country-level economic, industry, and commodity indicators | Free APIs |
| **data.gov / data.europa.eu** | Master portals indexing thousands of government datasets | Free |
| **USAspending.gov** | Every U.S. federal contract and grant — who's winning DOE/DOD/HHS money | Free API + bulk |
| **Bloomberg, S&P Capital IQ, PitchBook, LSEG/Refinitiv** | Deal comps, ownership, private company data | Paid — standard for deal teams |
| **Wood Mackenzie, Rystad (energy); CRU, Benchmark Mineral Intelligence (metals/battery)** | Asset-level cost curves and forecasts | Paid |

---

## Practical notes for deal mapping

- **Start free, then buy depth.** Government sources (EIA, USGS, FDA, EDGAR, IAEA) are authoritative
  and free; paid platforms mainly add convenience, private-company coverage, and cost curves.
- **Asset-level + coordinates = maps.** EIA-860, Global Energy Monitor, IAEA PRIS, and USGS MRDS all
  include locations, so plants/mines/reactors can be dropped straight onto a map.
- **Follow the filings.** For any specific deal target: EDGAR (US) and SEDAR+ (Canada) technical
  reports and 10-Ks contain more raw operational detail than any aggregator.
- **APIs beat scraping.** EIA, openFDA, ClinicalTrials.gov, FRED, Comtrade, and EDGAR all have
  documented free APIs — easy to automate refreshes for a living dashboard.
