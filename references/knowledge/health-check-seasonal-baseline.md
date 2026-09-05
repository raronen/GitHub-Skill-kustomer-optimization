# Cluster Health Check — Seasonal Baselines & Indicator Thresholds

Reusable technique for a fast, false-positive-resistant health check of one or
more Eventhouse/ADX engines using Geneva metrics (`KustoMdmMetricsV1`) plus live
ICMs. Use it when asked "is cluster/tenant X healthy?", after a deployment or
flighting change, or as a first-pass triage before a deep investigation.

The core ideas are cluster-agnostic: substitute the engine/DM list you discover
from `DimClustersMv()` (native ADX) or `TridentDimClusters(now())` (Fabric) for
the target cluster or tenant.

---

## 1. Seasonal baseline: 4-week same-hour-of-week trimmed median

**Do not compare the current hour to a flat 24h or 7d average.** Kusto workloads
have strong daily and weekly seasonality (business-hours peaks, weekend dips,
regional lunch/dinner traffic). A flat average makes a normal peak hour look like
a regression and a normal quiet hour hide a real one.

Instead, baseline each metric against the **same hour-of-week from the prior 4
weeks** (this hour last week, 2 weeks ago, 3 weeks ago, 4 weeks ago), and take
the **trimmed median** = the lower-middle of the 4 sorted values. With 4 samples
that is the 2nd-lowest, i.e. the median of the 3 lowest weeks — it **drops the
single highest week**, so one anomalous week (a past incident, a one-off
backfill, a one-time data load) cannot inflate the baseline and produce a false
alert today.

KQL idiom for the trimmed median of a 4-element list:

```kusto
// baseX = make_list_if(value, phase startswith "week-")  // 4 weekly samples
| extend baseMedian = todouble(toreal(array_sort_asc(baseX)[(array_length(baseX)-1)/2]))
```

Phase-tagging idiom (current hour vs the 4 same-hour-of-week samples):

```kusto
let nowHour  = bin(now(), 1h);
let curStart = nowHour - 1h;
let curEnd   = nowHour;
let lookback = 4*7d + 2h;   // +2h absorbs ingest/TIMESTAMP skew so the 4-wk-old bucket is fully covered
// ... | where TIMESTAMP between (curStart - lookback .. curEnd)
| extend hourBucket = bin(TIMESTAMP, 1h)
| extend ageWeeks   = toint((curStart - hourBucket) / 7d)
| extend phase = case(
    hourBucket == curStart, "current",
    ageWeeks in (1,2,3,4) and (curStart - hourBucket) % 7d == 0s, strcat("week-", ageWeeks),
    "ignore")
| where phase != "ignore"
```

**Idle-cluster guard:** when a cluster emitted **zero** samples for a metric in
both the current hour and all 4 baseline weeks, treat the indicator as **N/A**,
never as ALERT. Guard every delta with `iff(baseMedian == 0, 0.0, ...)`.

The "current" window is always the most recently completed full hour
(`bin(now(),1h)-1h .. bin(now(),1h)`), not a partial in-flight hour.

---

## 2. Health indicators, metric sources, and PASS / WARN / ALERT thresholds

All metrics come from `KustoMdmMetricsV1()` (Geneva; cross-cluster shortcut over
all regional Kuskus — see `KustoMdmMetricsV1-guide.md`), except ICMs. Dimensions
live in `dimensionNameList` / `dimensionValueList`, caret (`^`) separated and
positionally aligned — parse with
`split(dimensionValueList,"^")[array_index_of(split(dimensionNameList,"^"),"<dim>")]`.

| # | Indicator | Source | Namespace / Metric | Key dimension |
|---|---|---|---|---|
| 1 | Query Latency | Engine | `QueryMetrics / QueryDuration` | — (uses `sumValue/countValue`) |
| 2 | Query Errors | Engine | `QueryMetrics / QueryDuration` | `QueryStatus` (≠ `Completed` = failed) |
| 3 | Ingestion Volume | Engine | `MdmEngineMetrics / IngestionResult` | `countValue` |
| 4 | Ingestion Failures | Engine | `MdmEngineMetrics / IngestionResult` | `FailureKind` (not `""`/`None` = failed) |
| 5 | Ingestion Latency | DM | `MdmEngineMetrics / MessageAgeInPipelineSeconds` | — (uses `sumValue/countValue`, `maxValue`) |
| 6 | Availability (SLO) | Engine | `MdmEngineMetrics / ServiceLevelObjective` | — (current 1h, no baseline) |
| 7 | Active ICMs | ICM | `KustoIcMIncidentsMV` (see §4) | — |

Classification thresholds (mark **N/A** when the cluster has zero samples in both
current and baseline windows — an idle VC must not be penalized):

| Indicator | PASS | WARN | ALERT |
|---|---|---|---|
| 1. Query Latency | `LatencyDeltaPct ≤ +25%` AND `curLat ≤ 5000ms` | `+25% < Δ ≤ +75%` | `Δ > +75%` OR `curLat > 5000ms` |
| 2. Query Errors | `ErrorDeltaPP ≤ +1pp` | `+1pp < Δ ≤ +5pp` | `Δ > +5pp` OR `curErr ≥ 2 × baseErr` (when `baseErr ≥ 1`) |
| 3. Ingestion Volume | `\|CountDeltaPct\| ≤ 50%` | `50% < \|Δ\| ≤ 70%` OR rise `100–300%` | drop `>70%` OR rise `>300%` |
| 4. Ingestion Failures | `FailureRateDeltaPP ≤ +1pp` AND `curFailureRate < 10%` | `+1pp < Δ ≤ +5pp` | `Δ > +5pp` OR `curFailureRate ≥ 10%` |
| 5. Ingestion Latency | `curAvg ≤ max(60s, base×1.5)` | `max(60s, base×1.5) < curAvg ≤ max(180s, base×3)` | `curAvg > 300s` OR `> base×3` |
| 6. Availability (SLO) | `SLO == 100` | `95 ≤ SLO < 100` | `SLO < 95` |
| 7. Active ICMs | 0 active | 1–2 active (Sev ≥ 3) | ≥3 active OR any Sev ≤ 2 |

**Delta conventions:** `DeltaPct = 100*(cur - baseMedian)/baseMedian`; `DeltaPP`
= arithmetic difference of two percentages (percentage points). Rate metrics
(errors, ingestion failures) are compared in **percentage points**, not relative
percent, so a rate near 0 does not produce a huge relative swing.

Aggregate: per-cluster verdict = worst of its indicators (ignoring N/A);
per-indicator across a fleet = worst across clusters; overall = worst per-cluster.

---

## 3. Indicator queries (parameterize the cluster list)

Discover the engine list first from `DimClustersMv()` / `TridentDimClusters(now())`
for the target cluster or tenant, and bind it to `engines`. Derive the DM list as
`INGEST-<engine>` for native ADX, or take DM rows (`Kind == "DataManagement"`)
directly from `DimClustersMv()` — follower / K2Bridge engines have **no** DM.

### 3.1 Query Latency + Query Errors (Indicators 1 & 2) — Engine

```kusto
let engines = dynamic([/* engine list from discovery */]);
let nowHour = bin(now(), 1h);
let curStart = nowHour - 1h;  let curEnd = nowHour;  let lookback = 4*7d + 2h;
KustoMdmMetricsV1
| where TIMESTAMP between (curStart - lookback .. curEnd)
| where Cluster in (engines)
| where metricNamespace == "QueryMetrics" and metricName == "QueryDuration"
| extend dims = split(dimensionValueList, "^"), names = split(dimensionNameList, "^")
| extend QueryStatus = tostring(dims[array_index_of(names, "QueryStatus")])
| extend hourBucket = bin(TIMESTAMP, 1h), ageWeeks = toint((curStart - bin(TIMESTAMP,1h)) / 7d)
| extend phase = case(hourBucket == curStart, "current",
    ageWeeks in (1,2,3,4) and (curStart - hourBucket) % 7d == 0s, strcat("week-", ageWeeks), "ignore")
| where phase != "ignore"
| summarize TotalCount = sum(countValue), TotalSum = sum(sumValue),
            Failed = sumif(countValue, QueryStatus != "Completed") by Cluster, phase
| extend AvgLatencyMs = iff(TotalCount == 0, 0.0, todouble(TotalSum)/TotalCount),
         ErrorRatePct = iff(TotalCount == 0, 0.0, round(100.0*Failed/TotalCount, 2))
| summarize curLat = sumif(AvgLatencyMs, phase == "current"),
            curErr = sumif(ErrorRatePct,  phase == "current"),
            curCnt = sumif(TotalCount,    phase == "current"),
            baseLats = make_list_if(AvgLatencyMs, phase startswith "week-"),
            baseErrs = make_list_if(ErrorRatePct, phase startswith "week-"),
            baseCounts = make_list_if(TotalCount, phase startswith "week-") by Cluster
| extend baseLatMedian = todouble(toreal(array_sort_asc(baseLats)[(array_length(baseLats)-1)/2])),
         baseErrMedian = todouble(toreal(array_sort_asc(baseErrs)[(array_length(baseErrs)-1)/2]))
| extend LatencyDeltaPct = iff(baseLatMedian == 0, 0.0, round(100.0*(curLat-baseLatMedian)/baseLatMedian, 1)),
         ErrorDeltaPP    = round(curErr - baseErrMedian, 2)
| project Cluster, curLat, baseLatMedian, LatencyDeltaPct, curErr, baseErrMedian, ErrorDeltaPP
| order by LatencyDeltaPct desc
```

### 3.2 Ingestion Volume + Failures (Indicators 3 & 4) — Engine

Same skeleton, on `MdmEngineMetrics / IngestionResult`; a row is a failure when
its `FailureKind` dimension is not `""`/`None`:

```kusto
| where metricNamespace == "MdmEngineMetrics" and metricName == "IngestionResult"
| extend FailureKind = tostring(split(dimensionValueList,"^")[array_index_of(split(dimensionNameList,"^"),"FailureKind")])
// ... phase-tag as above ...
| summarize TotalCount = sum(countValue),
            FailedCount = sumif(countValue, FailureKind != "" and FailureKind != "None") by Cluster, phase
| extend FailureRatePct = iff(TotalCount == 0, 0.0, round(100.0*FailedCount/TotalCount, 2))
// curCnt / baseCntMedian → CountDeltaPct (Indicator 3);  curFail / baseFailMedian → FailureRateDeltaPP (Indicator 4)
```

### 3.3 Ingestion Latency (Indicator 5) — DM

```kusto
| where Cluster in (dms)   // INGEST-<engine> list (native ADX) or DataManagement rows
| where metricNamespace == "MdmEngineMetrics" and metricName == "MessageAgeInPipelineSeconds"
// ... phase-tag ...
| summarize TotalCount = sum(countValue), TotalSum = sum(sumValue), MaxAge = max(maxValue) by Cluster, phase
| extend AvgAgeSec = iff(TotalCount == 0, 0.0, todouble(TotalSum)/TotalCount)
// curAvg / curMax / baseAvgMedian → threshold in §2
```

### 3.4 Availability / SLO (Indicator 6) — Engine, current hour only (no baseline)

```kusto
let engines = dynamic([/* engine list */]);
KustoMdmMetricsV1
| where TIMESTAMP > ago(1h)
| where Cluster in (engines)
| where metricNamespace == "MdmEngineMetrics" and metricName == "ServiceLevelObjective"
| summarize SLO = round(avg(todouble(sumValue)/countValue), 2), Samples = sum(countValue), MinSLO = min(todouble(minValue)) by Cluster
| order by SLO asc
```

---

## 4. Active ICMs (Indicator 7)

**Cluster:** `https://kuskusops.kusto.windows.net` — **Database:** `KustoAuto`
(via `KustoIcMIncidentsMV`). Only the **KustoLiveIncidents** owning team
(`OwningTeamId == 23798`) counts. A mitigated incident within the last 24h is
still listed but does not drive ALERT.

```kusto
let allClusters = dynamic([/* engine + DM names for the target scope */]);
KustoIcMIncidentsMV
| where CreateDate > ago(24h)
| where OwningTeamId == 23798
| where Status in ("ACTIVE","ASSIGNED","INPROGRESS","INVESTIGATING","MITIGATED")
| where OccurringDeviceName in (allClusters)
| project IncidentId, Severity, Status, Title, OccurringDeviceName, CreateDate, ModifiedDate
| order by Severity asc, CreateDate desc
```

---

## 5. Geneva dashboard links for an offending cluster

`GetCluster("<name>")` on `Kuskus` returns two rows per cluster in the
`HealthV3Link` column — an **Engine** health dashboard (URL contains
`MdmEngineMetrics`) and a **DM** health dashboard (URL contains
`MdmDataMgmtMetrics`). Fetch only for clusters that are actually WARN/ALERT —
`GetCluster()` is relatively expensive.

```kusto
GetCluster("<cluster name>")
| project HealthV3Link
| extend DashboardKind = case(HealthV3Link contains "MdmEngineMetrics", "Engine",
                              HealthV3Link contains "MdmDataMgmtMetrics", "DM", "Other")
```

---

## 6. Regime change vs. outage

A dramatic drop (e.g. `>70%` in ingestion volume) is **not always** an outage —
it can be a permanent, expected workload shift (e.g. an ingestion pattern moving
from hourly to twice-daily bursts, or a query volume stepping up ~50× to a new
steady state) that poisons the 4-week baseline until it self-heals.

To distinguish: **plot the last 8–15 days of hourly history** for the metric.

- If the value collapsed at a single point and stays flat/zero → likely an
  **outage/regression** — investigate.
- If the pattern permanently changed shape at a known point and the **new state
  has been stable for ≥ 3 days** → **regime change**. It will keep tripping the
  baseline for up to 4 weeks (until all 4 baseline weeks reflect the new state).
  Confirm it is customer-driven/expected before discounting it, and note the
  change date; a seasonal baseline fully rolls over ~28 days after the change.

Never discount **SLO (Indicator 6)** or **ICMs (Indicator 7)** as regime changes
— those always reflect real availability/incident state.

---

## 7. N/A cases — do not penalize

- **Idle / suspended VCs**: emit no telemetry; zero samples in current + all
  baseline weeks ⇒ N/A for that indicator.
- **Streaming-only ingestion**: Fabric workspace-level Eventhouses often ingest
  via engine streaming ingestion, not a DM cluster ⇒ Indicator 5 (DM ingestion
  latency) is frequently N/A. Native ADX fleets usually have one DM per engine
  (`INGEST-<engine>`) that emits `MessageAgeInPipelineSeconds` ⇒ Indicator 5 is
  meaningful there.
- **Follower / K2Bridge clusters**: serve queries only and never ingest ⇒
  Indicators 3, 4, 5 are N/A; do not derive a DM for them.

---

## 8. Cross-check conclusions (what indicator combinations imply)

| Combination | Likely root cause / next step |
|---|---|
| Query Latency ALERT **+** SLO PASS | Cluster is up but slow — check Engine CPU / sandbox / hot-cache pressure, not availability. |
| Ingestion Volume ALERT (drop) **+** Ingestion Latency PASS | Fewer blobs are reaching the engine — check data connections / upstream producers, not the DM queue. |
| Ingestion Failures ALERT **+** Ingestion Volume PASS | Same attempt volume, more failures — check mapping / schema / capacity, not the source. |
| Ingestion Latency ALERT **+** Ingestion Failures PASS | DM queue building up — check DM CPU / SNAT exhaustion / EventHub message age. |
| ICMs ALERT **+** all engine indicators PASS | Incident is likely platform-side (Fabric, networking) — follow the ICM context rather than the engine. |
