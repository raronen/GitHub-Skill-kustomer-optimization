# Generating chart images for investigation reports

`query_kusto.py` returns raw JSON rows over an HTTP API — it does **not** render Kusto's native
`| render timechart` / `| render piechart` as an actual image (those are Kusto Web UI / dashboard
features, not something the REST query endpoint returns). To include a real chart in a markdown
investigation report (`Investigations/<yyyy-mm>/*.md`), generate it locally with **matplotlib**
from the query's JSON output and embed it **inline in the markdown as a base64 data URI** —
**do not** write a separate `.png` file into the `Investigations/` folder. Charts should travel
with the report as a single self-contained `.md` file.

> **For health checks, don't hand-write a throwaway script** — `scripts/invoke_health_check.py`
> already runs the cores-breakdown query and calls `scripts/generate_cores_charts.py` to produce
> the timechart as a base64 PNG automatically, saving it to
> `<tempdir>/healthcheck_charts_<Engine>.json` (OS temp dir). Read that file and embed
> `timechart_b64` directly. The manual steps below are for other investigation
> types or ad-hoc charts.

## Steps

1. **Run the KQL query** (keep the `| render ...` clause in the query text for documentation/
   reproducibility — it's harmless and ignored by the JSON endpoint).
2. **Capture the JSON rows** from `query_kusto.py`'s stdout (one JSON object per line).
3. **Write a small, throwaway Python script** (matplotlib) that parses/hardcodes the captured rows,
   renders the chart to an **in-memory buffer**, and prints the **base64-encoded PNG** to stdout —
   do **not** save a `.png` file to disk. Use the `create` tool to write the `.py` file (no
   PowerShell heredoc support), run it with `python <file>.py`, capture the base64 string, then
   delete the throwaway script.
4. **Embed the chart directly in the markdown report** as a data URI image:
   `![kuskusweu CPU breakdown timechart](data:image/png;base64,<BASE64_STRING>)`
   — this keeps the whole report (text + charts) in a single `.md` file with no companion assets.
5. Install matplotlib once per environment if missing: `pip install matplotlib --quiet` (check
   first with `python -c "import matplotlib"` to avoid redundant installs).

## Timechart pattern (multi-series line chart → base64, no file)

```python
import matplotlib
matplotlib.use('Agg')          # headless — no display server needed
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import io, base64

# rows: list of tuples parsed/hardcoded from the query_kusto.py JSON output
# e.g. (Timestamp, QueryCores, IngestCores, MaterializeCores, OtherCores)
ts = [datetime.strptime(r[0], "%Y-%m-%dT%H:%M:%SZ") for r in rows]

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(ts, [r[1] for r in rows], label="QueryCores", marker='o', ms=3)
ax.plot(ts, [r[2] for r in rows], label="IngestCores", marker='o', ms=3)
ax.set_title("<cluster> - CPU cores by workload type (last 1d)")
ax.set_xlabel("Timestamp (UTC)")
ax.set_ylabel("Cores")
ax.legend(loc='upper left', fontsize=8)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
fig.autofmt_xdate()
ax.grid(alpha=0.3)
fig.tight_layout()

buf = io.BytesIO()
fig.savefig(buf, format='png', dpi=130)
print(base64.b64encode(buf.getvalue()).decode('ascii'))
```

## Embedding in the report

```markdown
![kuskusweu CPU breakdown timechart](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...)
```

## Notes

- **Never write chart `.png` files into `Investigations/<yyyy-mm>/`** — only the single `.md`
  report file belongs there. Charts must be inline base64 data URIs so the report is fully
  self-contained and portable.
- Avoid non-ASCII characters (em dashes, curly quotes) in chart titles/labels rendered by
  matplotlib on Windows — the default font may not have the glyph, producing a "missing glyph"
  warning (harmless, but prefer a plain hyphen `-` in titles to keep output clean).
- Use `dpi=130` (or similar) for a crisp-but-reasonably-sized embedded image; base64 inflates size
  by ~33%, so keep figures compact (avoid huge `figsize`/`dpi` that bloat the markdown file).
- Always delete the throwaway generator script after capturing the base64 output — nothing except
  the `.md` report should remain in the `Investigations/` folder.
- **Every health-check investigation must include the CPU cores breakdown (query/ingest/
  materialize/other) as a timechart** — this is mandatory, not optional.
  `scripts/invoke_health_check.py` runs the
  cores-breakdown query and generates the chart
  automatically via `scripts/generate_cores_charts.py`, writing it to
  `<tempdir>/healthcheck_charts_<Engine>.json` for the report step to embed. For all other
  investigation types, only add charts (timechart) when a CPU/workload breakdown is
  otherwise relevant to the finding.
- **Any WARN/ALERT/outlier finding on a time-series metric (query latency, query errors,
  ingestion latency/volume/failures, CPU, etc.) must include its own timechart of that metric**
  over a window wide enough to show the spike/regression (e.g. the 24-48h hourly series that
  revealed it) — separate from the mandatory cores-breakdown chart. Build it with the same
  matplotlib-to-base64 pattern above (one `plt.plot()` series per metric, no separate `.png` file).
  PASS indicators don't need a dedicated chart unless explicitly requested.
