"""
Cross-platform (Windows/macOS/Linux) health-check runner, Python equivalent of
Invoke-HealthCheck.ps1. Implements the methodology in
references/knowledge/health-check-seasonal-baseline.md: 7 seasonal-baseline
indicators plus the mandatory CPU cores-breakdown query/charts, in the same 4
Kusto round trips as the PowerShell version (reusing a single cached AAD token
via kusto_token.get_token).

Usage:
    python invoke_health_check.py --engine TRD-S60F9UYQQV5UMWG9U6 --dm INGEST-TRD-S60F9UYQQV5UMWG9U6
    python invoke_health_check.py --engine KUSKUSWEU
    python invoke_health_check.py --engine KUSKUSWEU --skip-charts
    python invoke_health_check.py --engine KUSKUSWEU --charts-out-file /tmp/kuskusweu_charts.json

Charts (base64 PNG timechart + pie, per SKILL.md's "always include cores
breakdown in health checks" rule) are written to a JSON file (default:
<tempdir>/healthcheck_charts_<Engine>.json) for a report-writing step to embed
inline - never written as separate .png files, per chart-generation.md.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

from invoke_kusto_query import run_query

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICM_CLUSTER = "https://kuskusops.kusto.windows.net"
ICM_DATABASE = "KustoAuto"


def build_engine_query(engine: str) -> str:
    return f"""
let engines = dynamic(["{engine}"]);
let nowHour = bin(now(), 1h);
let curStart = nowHour - 1h;  let curEnd = nowHour;  let lookback = 4*7d + 2h;
let base = KustoMdmMetricsV1
| where TIMESTAMP between (curStart - lookback .. curEnd)
| where Cluster in (engines)
| where (metricNamespace == "QueryMetrics" and metricName == "QueryDuration")
     or (metricNamespace == "MdmEngineMetrics" and metricName == "IngestionResult")
| extend dims = split(dimensionValueList, "^"), names = split(dimensionNameList, "^")
| extend QueryStatus = tostring(dims[array_index_of(names, "QueryStatus")])
| extend FailureKind = tostring(dims[array_index_of(names, "FailureKind")])
| extend hourBucket = bin(TIMESTAMP, 1h), ageWeeks = toint((curStart - bin(TIMESTAMP,1h)) / 7d)
| extend phase = case(hourBucket == curStart, "current",
    ageWeeks in (1,2,3,4) and (curStart - hourBucket) % 7d == 0s, strcat("week-", ageWeeks), "ignore")
| where phase != "ignore";
let queryStats = base
| where metricNamespace == "QueryMetrics"
| summarize TotalCount = sum(countValue), TotalSum = sum(sumValue),
            Failed = sumif(countValue, QueryStatus != "Completed") by Cluster, phase
| extend AvgLatencyMs = iff(TotalCount == 0, 0.0, todouble(TotalSum)/TotalCount),
         ErrorRatePct = iff(TotalCount == 0, 0.0, round(100.0*Failed/TotalCount, 2))
| summarize curLat = sumif(AvgLatencyMs, phase == "current"),
            curErr = sumif(ErrorRatePct,  phase == "current"),
            curQueryCnt = sumif(TotalCount, phase == "current"),
            baseLats = make_list_if(AvgLatencyMs, phase startswith "week-"),
            baseErrs = make_list_if(ErrorRatePct, phase startswith "week-") by Cluster
| extend baseLatMedian = todouble(toreal(array_sort_asc(baseLats)[(array_length(baseLats)-1)/2])),
         baseErrMedian = todouble(toreal(array_sort_asc(baseErrs)[(array_length(baseErrs)-1)/2]))
| extend LatencyDeltaPct = iff(baseLatMedian == 0, 0.0, round(100.0*(curLat-baseLatMedian)/baseLatMedian, 1)),
         ErrorDeltaPP    = round(curErr - baseErrMedian, 2)
| project Cluster, curLat, baseLatMedian, LatencyDeltaPct, curErr, baseErrMedian, ErrorDeltaPP, curQueryCnt;
let ingestStats = base
| where metricNamespace == "MdmEngineMetrics"
| summarize TotalCount = sum(countValue),
            FailedCount = sumif(countValue, FailureKind != "" and FailureKind != "None") by Cluster, phase
| extend FailureRatePct = iff(TotalCount == 0, 0.0, round(100.0*FailedCount/TotalCount, 2))
| summarize curIngestCnt = sumif(TotalCount, phase=="current"), curFail = sumif(FailureRatePct, phase=="current"),
    baseCounts = make_list_if(TotalCount, phase startswith "week-"),
    baseFails = make_list_if(FailureRatePct, phase startswith "week-") by Cluster
| extend baseCntMedian = todouble(toreal(array_sort_asc(baseCounts)[(array_length(baseCounts)-1)/2])),
         baseFailMedian = todouble(toreal(array_sort_asc(baseFails)[(array_length(baseFails)-1)/2]))
| extend CountDeltaPct = iff(baseCntMedian == 0, 0.0, round(100.0*(curIngestCnt-baseCntMedian)/baseCntMedian,1)),
         FailureRateDeltaPP = round(curFail - baseFailMedian, 2)
| project Cluster, curIngestCnt, baseCntMedian, CountDeltaPct, curFail, baseFailMedian, FailureRateDeltaPP;
let sloStats = KustoMdmMetricsV1
| where TIMESTAMP > ago(1h)
| where Cluster in (engines)
| where metricNamespace == "MdmEngineMetrics" and metricName == "ServiceLevelObjective"
| summarize SLO = round(avg(todouble(sumValue)/countValue), 2), Samples = sum(countValue), MinSLO = min(todouble(minValue)) by Cluster;
queryStats
| join kind=fullouter ingestStats on Cluster
| join kind=fullouter sloStats on Cluster
| project Cluster = coalesce(Cluster, Cluster1, Cluster2),
          curLat, baseLatMedian, LatencyDeltaPct, curErr, baseErrMedian, ErrorDeltaPP, curQueryCnt,
          curIngestCnt, baseCntMedian, CountDeltaPct, curFail, baseFailMedian, FailureRateDeltaPP,
          SLO, Samples, MinSLO
"""


def build_dm_query(dm: str) -> str:
    return f"""
let dms = dynamic(["{dm}"]);
let nowHour = bin(now(), 1h);
let curStart = nowHour - 1h;  let curEnd = nowHour;  let lookback = 4*7d + 2h;
KustoMdmMetricsV1
| where TIMESTAMP between (curStart - lookback .. curEnd)
| where Cluster in (dms)
| where metricNamespace == "MdmDataMgmtMetrics" and metricName == "MessageAgeInPipelineSeconds"
| extend hourBucket = bin(TIMESTAMP, 1h), ageWeeks = toint((curStart - bin(TIMESTAMP,1h)) / 7d)
| extend phase = case(hourBucket == curStart, "current",
    ageWeeks in (1,2,3,4) and (curStart - hourBucket) % 7d == 0s, strcat("week-", ageWeeks), "ignore")
| where phase != "ignore"
| summarize TotalCount = sum(countValue), TotalSum = sum(sumValue), MaxAge = max(maxValue) by Cluster, phase
| extend AvgAgeSec = iff(TotalCount == 0, 0.0, round(todouble(TotalSum)/TotalCount,2))
| summarize curAvg = sumif(AvgAgeSec, phase == "current"), curMax = sumif(MaxAge, phase == "current"),
            curCnt = sumif(TotalCount, phase == "current"),
            baseAvgs = make_list_if(AvgAgeSec, phase startswith "week-") by Cluster
| extend baseAvgMedian = todouble(toreal(array_sort_asc(baseAvgs)[(array_length(baseAvgs)-1)/2]))
| project Cluster, curAvg, baseAvgMedian, curMax, curCnt
"""


def build_icm_query(cluster_names: list) -> str:
    cluster_list_kql = ",".join(f'"{name}"' for name in cluster_names)
    return f"""
KustoIcMIncidentsMV
| where CreateDate > ago(24h)
| where OwningTeamId == 23798
| where Status in ("ACTIVE","ASSIGNED","INPROGRESS","INVESTIGATING","MITIGATED")
| where OccurringDeviceName in ({cluster_list_kql})
| project IncidentId, Severity, Status, Title, OccurringDeviceName, CreateDate, ModifiedDate
| order by Severity asc, CreateDate desc
"""


def build_cores_query(engine: str) -> str:
    return f"""
let cluster = toupper("{engine}");
union
    (QueryCompletion
        | where Source == cluster
        | where Timestamp > ago(1d)
        | extend TotalCpuTs = TotalCPU, Category = "Query"),
    (CommandCompletion
        | where Source == cluster
        | where Timestamp > ago(1d)
        | extend TotalCpuTs = TotalCpuMs,
            Category = case(
                ActivityType contains "MaterializedView" or ActivityType contains "MaterializeView", "Materialize",
                ActivityType contains "DataIngestPull" or ActivityType contains "TableAppend" or ActivityType contains "ExtentsMove" or ActivityType contains "ExtentsMerge" or ActivityType contains "ExtentsRebuild", "Ingest",
                "Other"))
| summarize
    QueryCores=round(sumif(TotalCpuTs, Category == "Query")/1h, 2),
    IngestCores=round(sumif(TotalCpuTs, Category == "Ingest")/1h, 2),
    MaterializeCores=round(sumif(TotalCpuTs, Category == "Materialize")/1h, 2),
    OtherCores=round(sumif(TotalCpuTs, Category == "Other")/1h, 2)
  by bin(Timestamp, 1h)
| order by Timestamp asc
"""


def classify_query_latency(e: dict) -> tuple:
    if not e or not e.get("curQueryCnt"):
        return "N/A", "No query samples in current/baseline window"
    base_lat_median = e.get("baseLatMedian")
    delta = e.get("LatencyDeltaPct")
    base_disp = "n/a (sparse baseline)" if base_lat_median is None else f"{base_lat_median}ms"
    if delta is None:
        verdict = "PASS"
    elif delta > 75 or e.get("curLat", 0) > 5000:
        verdict = "ALERT"
    elif delta > 25:
        verdict = "WARN"
    else:
        verdict = "PASS"
    return verdict, f"cur={e.get('curLat')}ms base={base_disp} delta={delta}%"


def classify_query_errors(e: dict) -> tuple:
    if not e or not e.get("curQueryCnt"):
        return "N/A", "No query samples in current/baseline window"
    base_err_median = e.get("baseErrMedian")
    delta_pp = e.get("ErrorDeltaPP")
    base_disp = "n/a (sparse baseline)" if base_err_median is None else f"{base_err_median}%"
    if delta_pp is None:
        verdict = "PASS"
    elif delta_pp > 5 or (base_err_median is not None and base_err_median >= 1 and e.get("curErr", 0) >= 2 * base_err_median):
        verdict = "ALERT"
    elif delta_pp > 1:
        verdict = "WARN"
    else:
        verdict = "PASS"
    return verdict, f"cur={e.get('curErr')}% base={base_disp} deltaPP={delta_pp}"


def classify_ingestion_volume(e: dict) -> tuple:
    if not e or e.get("curIngestCnt") is None:
        return "N/A", "No ingestion samples"
    delta = e.get("CountDeltaPct", 0) or 0
    abs_delta = abs(delta)
    if abs_delta > 70 or delta > 300:
        verdict = "ALERT"
    elif abs_delta > 50 or (100 < delta <= 300):
        verdict = "WARN"
    else:
        verdict = "PASS"
    return verdict, f"cur={e.get('curIngestCnt')} base={e.get('baseCntMedian')} delta={delta}%"


def classify_ingestion_failures(e: dict) -> tuple:
    if not e or e.get("curIngestCnt") is None:
        return "N/A", "No ingestion samples"
    delta_pp = e.get("FailureRateDeltaPP", 0) or 0
    cur_fail = e.get("curFail", 0) or 0
    if delta_pp > 5 or cur_fail >= 10:
        verdict = "ALERT"
    elif delta_pp > 1:
        verdict = "WARN"
    else:
        verdict = "PASS"
    return verdict, f"curFail={cur_fail}% base={e.get('baseFailMedian')}% deltaPP={delta_pp}"


def classify_ingestion_latency(dm: str, d: dict) -> tuple:
    if not dm:
        return "N/A", "No DM specified"
    if not d or not d.get("curCnt"):
        return "N/A", "No pipeline samples in current window"
    cur_avg = d.get("curAvg", 0) or 0
    base_median = d.get("baseAvgMedian", 0) or 0
    threshold_warn = max(60, base_median * 1.5)
    if cur_avg > 300 or cur_avg > base_median * 3:
        verdict = "ALERT"
    elif cur_avg > threshold_warn:
        verdict = "WARN"
    else:
        verdict = "PASS"
    return verdict, f"curAvg={cur_avg}s base={base_median}s max={d.get('curMax')}s"


def classify_availability(e: dict) -> tuple:
    if not e or e.get("SLO") is None:
        return "N/A", "No SLO samples in current hour"
    slo = e["SLO"]
    verdict = "ALERT" if slo < 95 else ("WARN" if slo < 100 else "PASS")
    return verdict, f"SLO={slo}% samples={e.get('Samples')} min={e.get('MinSLO')}%"


def classify_icms(icm_rows: list) -> tuple:
    icm_count = len(icm_rows)
    high_sev = sum(1 for r in icm_rows if (r.get("Severity") or 99) <= 2)
    verdict = "ALERT" if (icm_count >= 3 or high_sev > 0) else ("WARN" if icm_count >= 1 else "PASS")
    return verdict, f"count={icm_count} (Sev<=2: {high_sev})"


def generate_charts(engine: str, cores_rows: list):
    """Pipes the cores rows into generate_cores_charts.py and returns the parsed result dict."""
    payload = json.dumps({"cluster": engine, "rows": cores_rows})
    chart_script = os.path.join(SCRIPT_DIR, "generate_cores_charts.py")
    result = subprocess.run(
        [sys.executable, chart_script],
        input=payload, capture_output=True, text=True, check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        print(f"WARNING: chart generation failed ({result.stderr.strip()}). "
              "Is matplotlib installed? 'pip install matplotlib'. Continuing without charts.", file=sys.stderr)
        return None
    return json.loads(result.stdout)


def run_health_check(engine: str, dm: str = None, skip_charts: bool = False, charts_out_file: str = None) -> dict:
    print("Running engine indicators (1,2,3,4,6)...")
    engine_rows = run_query(build_engine_query(engine), database="Kuskus")
    e = engine_rows[0] if engine_rows else None

    d = None
    if dm:
        print("Running DM indicator (5 - ingestion latency)...")
        dm_rows = run_query(build_dm_query(dm), database="Kuskus")
        d = dm_rows[0] if dm_rows else None

    print("Running ICM check (7)...")
    cluster_names = [engine] + ([dm] if dm else [])
    icm_rows = run_query(build_icm_query(cluster_names), database=ICM_DATABASE, cluster=ICM_CLUSTER)

    print("Running cores breakdown (query/ingest/materialize/other)...")
    cores_rows = run_query(build_cores_query(engine), database="Kuskus")

    charts_data = None
    if not skip_charts and cores_rows:
        print("Generating cores-breakdown timechart...")
        charts = generate_charts(engine, cores_rows)
        if charts:
            charts_data = {
                "cluster": engine,
                "rows": cores_rows,
                "timechart_b64": charts.get("timechart_b64"),
            }
            out_file = charts_out_file or os.path.join(
                tempfile.gettempdir(), f"healthcheck_charts_{''.join(c if c.isalnum() else '_' for c in engine)}.json"
            )
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(charts_data, f)
            print(f"Charts written to: {out_file}")
            charts_data["_out_file"] = out_file

    indicators = []
    v, detail = classify_query_latency(e); indicators.append(("1. Query Latency", v, detail))
    v, detail = classify_query_errors(e); indicators.append(("2. Query Errors", v, detail))
    v, detail = classify_ingestion_volume(e); indicators.append(("3. Ingestion Volume", v, detail))
    v, detail = classify_ingestion_failures(e); indicators.append(("4. Ingestion Failures", v, detail))
    v, detail = classify_ingestion_latency(dm, d); indicators.append(("5. Ingestion Latency", v, detail))
    v, detail = classify_availability(e); indicators.append(("6. Availability (SLO)", v, detail))
    v, detail = classify_icms(icm_rows); indicators.append(("7. Active ICMs", v, detail))

    verdicts = [v for _, v, _ in indicators if v != "N/A"]
    overall = "ALERT" if "ALERT" in verdicts else ("WARN" if "WARN" in verdicts else "PASS")

    print()
    print(f"=== Health Check: Engine={engine}  DM={dm or ''} ===")
    for name, v, detail in indicators:
        print(f"{name:<24}{v:<8}{detail}")
    print(f"Overall verdict: {overall}")

    if icm_rows:
        print()
        print("-- Active ICM detail --")
        for r in icm_rows:
            print(r)

    if cores_rows:
        latest = cores_rows[-1]
        print()
        print("-- CPU cores breakdown (latest hour) --")
        print(f"Query={latest.get('QueryCores')} Ingest={latest.get('IngestCores')} "
              f"Materialize={latest.get('MaterializeCores')} Other={latest.get('OtherCores')}")
        if charts_data:
            print(f"Chart (base64 PNG, timechart) saved to: {charts_data['_out_file']}")
            print("Embed it in the report per references/knowledge/chart-generation.md.")

    return {
        "engine": engine,
        "dm": dm,
        "overall": overall,
        "indicators": indicators,
        "icm_rows": icm_rows,
        "cores_rows": cores_rows,
        "charts": charts_data,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a full Kusto cluster health check (7 indicators + cores breakdown + charts).")
    parser.add_argument("--engine", required=True, help="Engine cluster Source name (e.g. TRD-S60F9UYQQV5UMWG9U6 or KUSKUSWEU).")
    parser.add_argument("--dm", default=None, help="Data-management (ingestion) cluster Source name. Optional.")
    parser.add_argument("--skip-charts", action="store_true", help="Skip cores-breakdown chart generation.")
    parser.add_argument("--charts-out-file", default=None, help="Path to write the base64 PNG + raw cores JSON.")
    args = parser.parse_args()

    run_health_check(args.engine, dm=args.dm, skip_charts=args.skip_charts, charts_out_file=args.charts_out_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
