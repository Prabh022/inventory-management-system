# Power BI dashboard for this inventory

The app itself stays a command-line tool. This guide explains how to
point Power BI Desktop at the data it exports — no Power BI file is
checked in, because the dashboard is built from your live data.

## 1. Export the data

Run the app and choose option 8 (Export for Power BI), or run:

```bash
python -c "from powerbi_export import export_powerbi; export_powerbi()"
```

This writes two CSV files into `powerbi/` (this folder):

- `inventory_snapshot.csv` — one row per item: id, name, quantity,
  price, stock_value (quantity x price), and stock_status
  ("Low Stock" when quantity is below the threshold in `config.py`,
  otherwise "In Stock").
- `inventory_summary.csv` — one row of KPIs: total items, total
  quantity, total inventory value, and low-stock item count.

Re-run the export whenever the inventory changes, then refresh the
data in Power BI. The CSVs themselves are generated output, not
source files — only this guide is checked in.

## 2. Connect Power BI Desktop

Get Data -> Text/CSV -> select both CSV files -> Load. The two
tables need no relationship for the visuals below; if you want one,
join the summary row to nothing — it is a single row of KPIs, meant
for card visuals.

## 3. Suggested visuals

- Bar chart: stock_value by name (from the snapshot table).
- Table: items filtered to stock_status = "Low Stock".
- Cards: total_value and low_stock_count (from the summary table).
- Slicer: stock_status, to flip between in-stock and low-stock views.
