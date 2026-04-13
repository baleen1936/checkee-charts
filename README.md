# Checkee Charts

Auto-updated US visa administrative processing dashboard, sourced from [checkee.info](https://www.checkee.info).

**Live dashboard → https://baleen1936.github.io/checkee-charts**

![Dashboard Screenshot](screenshot.png?v=2)

## What it shows

### Visa group cards (top 9, 3-column grid)

Six visa group bar charts plus three summary cards.

| Card | Visas | Color |
|---|---|---|
| Business / Visitor | B1, B2 | Steel blue |
| Student | F1, F2 | Sage green |
| Work | H1, H4 | Coral red |
| Exchange Visitor | J1, J2 | Amber |
| Intracompany | L1, L2 | Teal |
| Extraordinary Ability | O1 | Purple |

Each shows daily case counts (stacked bar) with a stats footer: total cases, median / min / max waiting days.

**Issue Date Distribution** — stacked bar (Clear / Reject) by issue date, with a dashed avg cases/day reference line. Updates dynamically when a consulate filter is active.

**Waiting Days** — median waiting days over time with a min–max shaded band.

**Consulate Distribution** — horizontal bar chart of the top 10 consulates by volume. Click a bar to cross-filter all charts and the table; click again to reset.

### 10-year trend charts (below grid)

**Monthly Cases (Trailing 10 Years)** — stacked % bar chart of Clear / Reject / Pending by month, overlaid with a total cases line. Includes a 🦠 COVID-19 marker.

**Avg Waiting Days (Trailing 10 Years)** — monthly average waiting days line, with shaded bands for each US presidential administration and a 🦠 COVID-19 marker.

### Records table

Sortable table of all raw records from the last 90 days: Status, Check Date, Complete Date, Waiting Days, Visa Type, Entry, Consulate, Major, Details. Responds to the consulate cross-filter.

## How it works

1. `generate.py` scrapes checkee.info and produces a self-contained `index.html`
2. GitHub Actions runs every 2 hours, commits the updated HTML, and GitHub Pages serves it
3. Timestamps shown in CST (UTC+8)

## Run locally

```bash
pip install -r requirements.txt
python generate.py
open index.html
```
