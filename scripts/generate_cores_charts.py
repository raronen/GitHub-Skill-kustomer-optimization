"""
Generates the standard health-check chart (CPU cores breakdown timechart) from
a single set of hourly Category->Cores rows, and prints it as a base64-encoded
PNG (JSON on stdout) - no PNG files are ever written to disk.

Reused by scripts/invoke_health_check.py so that every health-check investigation
includes the same cores-breakdown visual without hand-writing a throwaway
matplotlib script each time (see references/knowledge/chart-generation.md for
the underlying convention: base64-inline images only, never separate .png files).

Input (stdin): JSON object
{
  "cluster": "<cluster name>",
  "rows": [
    {"Timestamp": "2026-08-08T06:00:00Z", "QueryCores": 1.2, "IngestCores": 30.0,
     "MaterializeCores": 0.5, "OtherCores": 0.1},
    ...
  ]
}

Output (stdout): JSON object
{ "timechart_b64": "..." }
"""
import base64
import io
import json
import sys
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

CATEGORIES = ["QueryCores", "IngestCores", "MaterializeCores", "OtherCores"]
LABELS = {"QueryCores": "Query", "IngestCores": "Ingest",
          "MaterializeCores": "Materialize", "OtherCores": "Other"}
COLORS = {"Query": "#4C72B0", "Ingest": "#DD8452", "Materialize": "#55A868",
          "Other": "#C44E52"}


def parse_ts(value: str) -> datetime:
    value = value.replace("Z", "")
    if "." in value:
        value = value.split(".")[0]
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")


def make_timechart(cluster: str, rows: list) -> str:
    ts = [parse_ts(r["Timestamp"]) for r in rows]
    fig, ax = plt.subplots(figsize=(11, 5))
    for cat in CATEGORIES:
        ax.plot(ts, [r.get(cat, 0.0) for r in rows], label=LABELS[cat], marker="o", ms=2.5,
                color=COLORS[LABELS[cat]])
    ax.set_title(f"{cluster} - CPU cores by workload type (last 1d)")
    ax.set_xlabel("Timestamp (UTC)")
    ax.set_ylabel("Cores")
    ax.legend(loc="upper left", fontsize=8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
    fig.autofmt_xdate()
    ax.grid(alpha=0.3)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def main() -> int:
    payload = json.loads(sys.stdin.read())
    cluster = payload.get("cluster", "cluster")
    rows = payload.get("rows", [])

    if not rows:
        print(json.dumps({"timechart_b64": None, "error": "no rows"}))
        return 0

    result = {
        "timechart_b64": make_timechart(cluster, rows),
    }
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())

