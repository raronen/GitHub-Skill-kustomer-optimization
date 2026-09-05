# Kuskus query knowledge
This folder was generated from live metadata in the `Kuskus` database on `kuskushead.westeurope`.
- Functions discovered: **232**
- MV-like functions discovered: **29**
- Note: `.show materialized-views` returned no rows in this database. In practice, MV-style assets here are exposed mainly as functions such as `DimClustersMv`, `DimClustersDailyMv`, `UsageDailyMv`, and similar wrappers.

## How to query
Use `Query-kusto.py` from this directory. Examples:

```powershell
python .\Query-kusto.py "QueryCompletion() | take 10"
python .\Query-kusto.py "DimClustersMv() | take 10"
python .\Query-kusto.py ".show functions | take 5"
```

## Files
- `functions-index.md`: all functions grouped by folder
- `materialized-views.md`: MV-like functions and querying guidance
- `mv-investigation-guide.md`: materialized-view investigation playbook
- `ingestion-latency-analysis.md`: ingestion-latency playbook that reports batching interval, batch processing time, and MV age for the main objects used by affected queries
- `alerts\`: **`Alerts()` investigation guide + categorized alert-reason catalog** — start here to surface silent reliability / data-correctness issues (e.g. update-policy data loss on streaming sources)
- `health-check-seasonal-baseline.md`: **fast fleet health-check technique** — 4-week same-hour-of-week trimmed-median seasonal baselines, PASS/WARN/ALERT thresholds and Geneva-metric queries for 7 indicators (query latency/errors, ingestion volume/failures/latency, SLO, active ICMs), the ICM query on `kuskusops/KustoAuto`, Geneva dashboard-link retrieval, regime-change-vs-outage logic, N/A rules, and indicator cross-check conclusions
- `failure-reason-bucketing.md`: **technique for bucketing `FailureReason`/free-text error fields into ≤15 categories** — use this instead of raw `summarize count() by FailureReason`, which fragments failures that embed GUIDs/shard IDs/blob URLs into hundreds of near-unique rows and hides the true dominant cause
- `chart-generation.md`: **how to produce real chart images (timechart/piechart) for investigation reports** — `query_kusto.py` only returns raw JSON, not rendered Kusto charts, so use matplotlib to generate PNGs from the query results and embed them via relative markdown links in `Investigations/<yyyy-mm>/*.md` reports
- `folders\*.md`: detailed per-folder function documentation
