---
name: kustomer-optimization
description: >
    Investigate cluster issues related to Kusto cluster health, performance, and reliability. Covers diagnostics for ingestion volume, database count, query performance, crashes, and failures. Utilizes Kusto diagnostic queries. Triggers on: "cluster investigation", "cluster health", "performance issue", "query failure".
    You will be given the cluster name and a customer complaint or issue description within a specific timeline. Your task is to analyze the cluster's health and performance using Kusto queries, identify the root cause of the issue, and provide a clear summary of your findings.
---

# Cluster Investigation Skill

Investigate issues related to a customer (tenant) or cluster for ingestion volume, databases, performance, crashes, and failures.

## Tools
Use /scripts/query_kusto.py for running KQL queries on the appropriate cluster.
Do not create new scripts or tools beyond the ones already provided in `/scripts`.

### Faster Python tooling (use these instead of ad-hoc `query_kusto.py` calls, on Windows and macOS)

`query_kusto.py` re-runs `az account get-access-token` on every call, which adds
~1-2s of Azure CLI startup latency per query. For any investigation issuing more
than one or two queries (which is almost all of them), use the Python scripts
below instead — they work identically on Windows and macOS/Linux (no
PowerShell required anywhere), cache the AAD token across calls, and let you
batch several indicators into one Kusto round trip. **These scripts are the
only supported way to run investigations in this skill — do not use the
retired `.ps1` PowerShell scripts, and do not write new ad-hoc scripts.**

- **`scripts/kusto_token.py`** — returns a cached bearer token for a given
  resource URI, refreshing only when it's within 5 minutes of expiry. Called
  automatically by the other scripts; rarely needed directly. CLI:
  `python scripts/kusto_token.py --resource <uri>`.
- **`scripts/invoke_kusto_query.py`** — drop-in faster alternative to
  `query_kusto.py` for **any** investigation type (health check, throttling,
  ingestion, crash, capacity, ad-hoc, etc.), not just health checks:
  - As a library: `from invoke_kusto_query import run_query` /
    `rows = run_query(query, database=..., cluster=...)` — returns a list of
    dict rows, reusable for arbitrary follow-up queries within a single
    investigation.
  - As a CLI: `python scripts/invoke_kusto_query.py "<KQL>" [--database <db>] [--cluster <uri>]`
    — prints one JSON object per row line, same convention as `query_kusto.py`,
    but reuses the cached token so repeat calls are fast.
  - Use this for every multi-query investigation regardless of type — the
    token cache alone (no repeated `az` cold-start) is the main speed win, and
    it works whether the investigation is a health check, a throttling
    analysis, a CPU hotspot search, a capacity check, or anything else.
- **`scripts/invoke_health_check.py --engine <name> [--dm <name>]`** — runs the
  **entire** seasonal-baseline health check (see
  [`references/knowledge/health-check-seasonal-baseline.md`](references/knowledge/health-check-seasonal-baseline.md))
  in **4 Kusto round trips total** (engine indicators 1/2/3/4/6 combined into one
  query, DM indicator 5, ICM indicator 7, and the CPU cores-breakdown-by-workload
  query), instead of running each indicator as a separate query. Prints a
  PASS/WARN/ALERT table per indicator plus an overall verdict, **and always
  runs the CPU cores breakdown (query/ingest/materialize/other) and
  generates a timechart as a base64 PNG** (via
  `generate_cores_charts.py`), writing it to a JSON file
  (`<tempdir>/healthcheck_charts_<Engine>.json`, or `--charts-out-file <path>`)
  for the report-writing step to embed inline. Use `--skip-charts` only if
  matplotlib is unavailable. **Use this any time the investigation type is
  "Health check" — do not write a health-check report without the cores
  breakdown timechart.**
- **`scripts/generate_cores_charts.py`** — reusable chart generator invoked by
  `invoke_health_check.py`, and importable/runnable directly for any other
  investigation type that needs a cores-breakdown chart (e.g. CPU hotspot
  analyses); takes hourly `Category -> Cores` rows on stdin and prints a base64
  timechart PNG on stdout, following the base64-inline convention in
  [`references/knowledge/chart-generation.md`](references/knowledge/chart-generation.md)
  (never writes a separate `.png` file).

Requires `python3` with `matplotlib` installed (`pip install matplotlib`) for
chart generation, and the Azure CLI (`az`) on `PATH` (or already logged in) for
token acquisition — the scripts fall back to `az` automatically if a cached
token has expired.

## Special Instructions
### Fabric Eventhouses

**Fabric Eventhouse clusters have names starting with `TRD-`.**
When investigating a cluster whose name starts with `TRD-`, it is a Fabric Eventhouse (not a classic ADX cluster).
In tables like QueryCompletion, CommandCompletion and other tables which are derived from KustoLogs , the source column for Fabric Eventhouses clusters is prefixed with the hoster name (Starting with Kutrident) for virtual clusters and only then the cluster (Eventhouse) name. 
Example : KUTRIDENTHOSTERWEU.TRD-R6TB4D63576P2WHRW5. There is one hoster per region

When a Fabric cluster grows beyond the maximum size of a virtual cluster (12 cores) it is migrated to physical  cluster and the source column no longer includes the hostername.


Always run this query first:

```kusto
DimClustersMv()
| where Source == toupper('<cluster name>')
| project Source, Region, MachineSKU, MachineCount, SourceQualified,
    RegionalTracingTargetUrl
```
If `SourceQualified` is not empty, use it as the `Source` for subsequent
telemetry queries. Otherwise, use `Source`.

For an investigation of this specific cluster, use `RegionalTracingTargetUrl`
as the Kuskus cluster endpoint for all subsequent queries.


## ⚠️ Key Concept: QueryCompletion `Machine` field

**The `Machine` field in `QueryCompletion` indicates which node performed query planning, NOT which node executed the query.**

In a Kusto/ADX cluster, query planning is handled by the **admin node** — by default there is only one admin node per cluster, so all queries will always show the same machine in `QueryCompletion`. This is expected behavior.

- Seeing all queries attributed to a single machine in `QueryCompletion` is **normal** — it is the admin node doing planning.
- It does **not** mean there is a routing issue, sticky connection, or load balancer problem.
- Actual query execution is distributed across data nodes in the cluster.
- If the admin node has high CPU, the cause is query planning/compilation/aggregation overhead, not query execution being concentrated on one machine.

Use `PerfCounterCPU` (grouped by `Machine`) to see actual CPU load per node. Use `AdminCPU()` to specifically track admin node CPU.

> **Always use `bin(Timestamp, 10m)` and avg(Countervalue) when querying `PerfCounterCPU`** — finer granularity produces noisy results while coarser bins hide short spikes.

## ⚠️ Key Concept: `CommandCompletion.TotalCpuMs` is a `timespan`, not milliseconds

**Despite its name, `TotalCpuMs` in `CommandCompletion` is `timespan`-typed (like `TotalCPU` in `QueryCompletion`) — it is NOT a scalar count of milliseconds.**

- Do **not** multiply it by `1ms` (a timespan cannot be multiplied by another timespan — this is a compile error).
- Do **not** treat it as a `long`/`real` and divide by `1000` — use standard timespan arithmetic instead.
- To get a scalar number of seconds, divide by the timespan `1s` (timespan / timespan = scalar), e.g. `TotalCpuMs / 1s`.
- When unioning `QueryCompletion` and `CommandCompletion` to compute combined CPU (e.g. cores-per-hour breakdowns), both `TotalCPU` and `TotalCpuMs` can be used directly, side by side, with no unit conversion — they are already the same type.

## ⚠️ Key Concept: `CommandCompletion.TotalCpuMs` is a `timespan`, not milliseconds

**Despite its name, `TotalCpuMs` in `CommandCompletion` is `timespan`-typed (like `TotalCPU` in `QueryCompletion`) — it is NOT a scalar count of milliseconds.**

- Do **not** multiply it by `1ms` (a timespan cannot be multiplied by another timespan — this is a compile error).
- Do **not** treat it as a `long`/`real` and divide by `1000` — use standard timespan arithmetic instead.
- To get a scalar number of seconds, divide by the timespan `1s` (timespan / timespan = scalar), e.g. `TotalCpuMs / 1s`.
- When unioning `QueryCompletion` and `CommandCompletion` to compute combined CPU (e.g. cores-per-hour breakdowns), both `TotalCPU` and `TotalCpuMs` can be used directly, side by side, with no unit conversion — they are already the same type.

## ⚠️ Key Concept: use `contains`, not `has`, to match a substring inside `ActivityType`

**`has` (and `has_any`) only matches whole tokens — it does NOT match a substring embedded inside a larger token.** `ActivityType` values like `DN.AdminCommand.DataIngestPullCommand` or `DN.AdminCommand.MaterializedViewTableAppendCommand` are each a single token once split on `.` (Kusto's term index only tokenizes on non-alphanumeric characters, not on camelCase boundaries).

- `ActivityType has "DataIngestPull"` returns **zero rows**, even when matching rows clearly exist — because `"DataIngestPull"` is not the *entire* token `DataIngestPullCommand`.
- `ActivityType has "MaterializedView"` similarly returns **zero rows** against `MaterializedViewTableAppendCommand`.
- Use `ActivityType contains "DataIngestPull"` (substring match) instead — verified against live `kuskusweu` data to correctly return non-zero CPU/counts for `DataIngestPull`, `ExtentsMerge`, and `MaterializedView`/`MaterializeView` commands.
- `has_any (...)` has the same whole-token limitation as `has` — prefer chained `contains`/`or` (or `matches regex`) when matching partial `ActivityType` names.
- Several pre-existing queries in this skill's reference docs use `ActivityType has "UpdatePolicy"` / `has "MaterializedView"` — these silently return 0 rows and should be corrected to `contains` (and the actual `UpdatePolicy`-related activity type observed in practice is `TableUpdateDataPolicy*`, not a literal `"UpdatePolicy"` substring — verify the exact token before filtering).

## ⚠️ Choose Kuskus by Investigation Scope

- **All-region or multi-region investigation:** Use
  `kuskushead.westeurope` with the `Kuskus` database. Kuskushead dispatches the
  query to every regional Kuskus instance; do not query regional endpoints
  separately or manually merge their results.
- **Specific-cluster investigation:** For both Fabric Eventhouses and classic
  ADX clusters, obtain the cluster's regional Kuskus endpoint from
  `DimClustersMv().RegionalTracingTargetUrl` and use it as the `--cluster`
  argument to `query_kusto.py` for subsequent cluster-specific queries.

Use a regional Kuskus endpoint only when investigating a specific cluster. Do
not derive it from `ServiceConnectionString`, region names, or static
region-to-host mappings.

---

## How to query
All cluster investigations start from here:

investigate a claim from cluster=<cluster name>

* If not given a time period assume 7 days
* Find the reason for complaint if present, otherwise find the reason for the investigation
* Use [new-kuskus-useful-queries.md](references/new-kuskus-useful-queries.md) and [queries.md](references/queries.md)
* Use the knowledge of kuskus in the [knowledge](references/knowledge/) directory
* When looking for cluster details use dimclustersmv and not dimclusters
* There are 2 types of investigations: tenant and cluster.

---
## ⚠️ Query Failure Recovery — Self-Correct Before Reporting (MANDATORY)

**A failed query is never a final answer and must never be silently dropped from an investigation.**
Whenever a query returns an error (non-zero exit / Kusto error payload), **do not** skip it, guess the
result, or proceed to the report. **Correct it using kuskus knowledge and rerun it** until it succeeds or
you have positively confirmed the signal genuinely cannot be obtained on this cluster.

### Recovery loop (repeat until the query succeeds or is proven unobtainable)

1. **Read the actual error** — parse the Kusto error code/message, don't just note "it failed":
   - `SEM0100` *(Failed to resolve scalar expression / column named 'X')* → **wrong column name**. The
     table/function exists but the column doesn't (or has a different name).
   - `SEM0001` / unknown function or table → **wrong function/table name or missing `()`** (kuskus
     functions like `DimClustersMv()`, `Memento()`, `AdminCPU()` need parentheses).
   - `SYN0001` / syntax → **command/operator not supported** on this engine/endpoint, or a typo.
   - `Forbidden` / `403` / auth → **wrong endpoint or permission**, not a query-shape problem — do not
     rewrite the columns; re-check you are on the correct `RegionalTracingTargetUrl` / kuskushead.
   - Empty result is **not** an error — handle it per the retention/onset rules, do not "fix" it.
2. **Find the right shape from kuskus knowledge** — before rewriting, consult, in this order:
   - [`references/knowledge/functions-index.md`](references/knowledge/functions-index.md) and the
     [`references/knowledge/folders/`](references/knowledge/folders/) files — the **authoritative
     signature** (exact function name, parameters, and their order/defaults) for every kuskus function.
   - [`references/knowledge/`](references/knowledge/) topic guides (ingestion-latency, mv-investigation,
     failure-reason-bucketing, health-check-seasonal-baseline, KustoMdmMetricsV1-guide, etc.) for the
     **canonical query** for that investigation area.
   - [`references/new-kuskus-useful-queries.md`](references/new-kuskus-useful-queries.md),
     [`references/kuskus-useful-queries.md`](references/kuskus-useful-queries.md), and
     [`references/queries.md`](references/queries.md) for working example queries to copy the correct
     column names and patterns from.
3. **For a wrong-column error, discover the real schema** rather than guessing repeatedly — run the
   table/function bare first (or `getschema`) to see the actual columns, then re-project:
   ```kusto
   <TableOrFunction()> | take 1                       // inspect available columns
   <TableOrFunction()> | getschema                    // or list column names/types
   .show <management-command>                          // run bare to see its result schema first
   ```
   This is the same technique that resolved earlier failures (e.g. `.show diagnostics` /
   `.show databases datastats` projecting non-existent columns → run bare, read the schema, re-project).
4. **Rewrite and rerun** the corrected query. Confirm it now returns a valid result (or a legitimate empty
   set).
5. **If it still fails after correction**, try the next-best documented equivalent from the knowledge base
   (a different function/table that exposes the same signal). Only after those are exhausted may you
   conclude the signal is genuinely unavailable — and then you must **state explicitly in the report which
   signal could not be obtained, the exact error, and what you tried**, rather than omitting it.

### Hard rule

> **Do not produce the report while any intended query is still in a failed/unresolved state.** Every
> conclusion must be backed by a query that actually executed successfully. A finding may only rely on an
> "unavailable" signal if step 5's exhaustion was reached and the limitation is called out in the report.

---
## Tenant Investigation
When asked about a tenant , collect the following information to help diagnose the issue.
### General info
* Customer tenant name
* Number of clusters — Total clusters associated with the customer.

### Per cluster info (only for external tenants/customers)
* Cluster name, region, SKU, scaling nodes ( min, max) – find patterns (weekdays, nights etc)
* Ingestion volume — Daily ingestion volume per cluster over the past 30 days.
* Nr of Extents — Total number of extents per cluster.The compressed size should be between 1GB and 2GB per extent.
* new extents are normally smaller until they are compressed. Small extents older than 1 day is a problem
* Nr of Machines — Total number of machines per cluster over time.
* Ingested Data per Cluster— Average ingested data in GB per cluster
* Database count — Number of databases per cluster.
* Tables count — Number of tables per DB per cluster.

---
## Cluster investigations
### Types of investigations
Decide what type of investigation is needed based on the customer complaint or issue description. Use the following categories to guide your investigation:

#### Health check ("is cluster/tenant X healthy?")
##### Questions
* Is this cluster/tenant healthy right now?
* Any regressions after a deployment or flighting change?
##### Related investigations
* Run `python scripts/invoke_health_check.py --engine <name> [--dm <name>]` —
  implements
  [the health-check seasonal-baseline guide](references/knowledge/health-check-seasonal-baseline.md):
  baseline each Geneva metric against the 4-week same-hour-of-week trimmed
  median, classify query latency/errors, ingestion volume/failures/latency,
  SLO, and active ICMs as PASS/WARN/ALERT, and mark idle/follower clusters N/A.
* Distinguish a real regression from a permanent regime change (workload shift) by plotting 8–15 days of hourly history before alerting.
* **Every health-check investigation must include the CPU cores breakdown by
  workload type (query / ingest / materialize / other) as a
  timechart**, embedded inline as a base64 image per
  [`references/knowledge/chart-generation.md`](references/knowledge/chart-generation.md).
  `invoke_health_check.py` runs
  this query and generates the chart automatically — do not omit it from
  the report, and do not write a health-check report without it (unless
  the chart is proven unobtainable, e.g. matplotlib missing and uninstallable —
  note this explicitly if so).
* **Whenever a report calls out a WARN/ALERT/outlier finding for a time-series
  metric (query latency, query errors, ingestion latency, ingestion volume/
  failures, CPU, etc.), include a timechart of that specific metric over a
  window wide enough to show the spike/regression clearly** (e.g. the 24-48h
  hourly trend that revealed the anomaly), embedded inline as a base64 image
  per [`references/knowledge/chart-generation.md`](references/knowledge/chart-generation.md)
  — not just the cores-breakdown chart. This applies to any indicator called
  out as anomalous, not only health checks (e.g. a CPU-hotspot or latency
  investigation should chart the metric that triggered the finding). A PASS
  indicator does not need its own chart unless specifically requested.


#### General
##### Questions
* “are there “hot nodes” cpu>80”
##### Related Investigations
* unusually high ingestion volumes
* large numbers of extents
* ratio between cpu and duration in queries
* check if the nodes with high CPU were admin, multi-admin or running weak consistency. 
* calculate average cpu for the whole cluster and compare it to the nodes with high CPU to see if they are outliers. 
* check if there were any changes in the query patterns or workload that could have caused the increase in CPU consumption.


#### Ingestion
##### Questions
* Why is ingestion delayed?
* Why is ingestion failing?
* Why is data not appearing after ingestion?
* Why is ingestion throughput lower than expected?
* Why is ingestion latency inconsistent (spikes)?
* what is the cost of update policies on as part of ingestion cost
##### Related investigations
* For ingestion latency, follow [the ingestion latency analysis guide](references/knowledge/ingestion-latency-analysis.md) and report the three components for each main table used by the affected queries: average time between batches, batch processing time, and MV age when applicable.
* Ingestion delays / latency
* Ingestion failures / retries
* Ingestion batching / flushing behaviour
* Ingestion concurrency / throttling limits
* Ingestion queue backlog
* Cluster resource saturation during ingestion
* Source-side backlog / burst ingestion patterns
* SLA misunderstanding (ready vs. fully ingested)

#### Query / Performance
##### Questions
* Why are queries slow?
* Why do queries timeout or fail?
* Why is performance inconsistent?
* Why did query latency suddenly increase?
* Why are some queries faster than others on the same data?
##### Related investigations
* Query execution time breakdown
* Data scanning / filtering efficiency
* Cache usage (hot vs cold data)
* Query parallelism limits
* Heavy users / noisy neighbor impact
* Memory and CPU pressure
* When asked about query latency on a specific query, ask for ClientActivityId, then find, the user, the applicationId, the amount of CPU it consumed.
* in Kustologs there is a lot of information about each query, including the query text, the user who executed it, the time it was executed, and the resources it consumed. Query Text is available only on clusters that are internal to Microsoft
* When asked about query latency in general, check for ingestion spikes at the same time, cpu consumption changes in nodes or admins, check for other processes running at the same time, check for any changes in the cluster configuration or workload patterns that could correlate with the latency increase. check if the cluster scaled out or in durring the same period.


#### Resource / Capacity
##### Questions
* Is the cluster under-provisioned?
* Why is the cluster overloaded?
* Why do we see CPU/memory pressure?
* Why are operations throttled?
* Why does scaling not resolve the issue?
##### Related investigations
* CPU / memory utilization trends
* Extent cache pressure
* Storage vs compute bottlenecks
* Concurrency limits
* Workload spikes / burst behavior
* Autoscale behavior and timing
* Background processes (merge, ingestion)

#### Workload / Usage Patterns
##### Questions
* Did usage suddenly increase?
* Are there unexpected spikes in workload?
* Are certain workloads dominating cluster resources?
* Are ingestion and queries competing?
##### Related investigations
* Workload distribution (ingestion vs query)
* Burst patterns / time-of-day effects
* Heavy queries / long-running jobs
* Background processes (indexing, compaction)

#### Update Policies
##### Questions
* Why is the update policy not triggering?
* Why is the update policy failing?
##### Related investigations
* Update policy trigger behavior (ingestion completion dependency)
* Update policy execution failures / retries
* Update policy latency vs ingestion latency
* Resource consumption of update policy queries
* Interaction with batching / ingestion mode

#### Materialized Views (MV)
##### Questions
* Why is the materialized view lagging behind the source table?
* Why is the materialized view not updating?
##### Related investigations
* MV refresh latency / lag
* Incremental vs full recomputation behavior
* Extent coverage and materialization gaps
* MV query definition complexity
* Aggregation correctness / grouping issues
* Resource contention (CPU/memory during refresh)
* MV and partitioning competing

---
## Additional Investigation Guidelines
Consider the following information when investigating cluster issues.

### ⚠️ Always Check Cluster Scaling During Any Degradation Investigation

When investigating **any** cluster performance degradation (query latency, MV lag, ingestion delays, resource exhaustion), **always check cluster autoscaling behavior** during the incident period. This is critical because:

1. **Scaling may not have fired** — the cluster may have been at its max and unable to scale further, or autoscale may not have been triggered yet.
2. **Scaling fired but was delayed** — reactive autoscale reacts to metrics with a lag (often hours). Check timing vs incident start.
3. **Scale-out failed due to capacity** — the region/Fabric may not have had available machines to allocate.
4. **Predictive vs Reactive autoscaling** — predictive scales proactively based on historical patterns; reactive responds to current metrics. If only reactive is configured, spikes cause delayed responses.
5. **Scaling may not address the actual bottleneck** — e.g., MV runs on admin nodes, not data nodes. Adding data nodes won't fix MV memory exhaustion.

#### Queries to Run

```kusto
// 1. Machine count changes during the incident period
DimClusters
| where Cluster == '<CLUSTER>'
| where LastUpdated between(datetime(<START>) .. datetime(<END>))
| order by LastUpdated asc
| serialize
| where MachineCount != prev(MachineCount)
| project Timestamp=LastUpdated, MachineCount, MachineSKU
```

```kusto
// 2. Scale events from KustoLogs (run on cluster's regional Kuskus)
KustoLogs
| where Source == '<CLUSTER>'
| where Directory has 'AutoScale' or EventText has 'ScaleOut' or EventText has 'ScaleIn' or EventText has 'scale'
| where Timestamp between(datetime(<START>) .. datetime(<END>))
| project Timestamp, Directory, EventText
| order by Timestamp asc
| take 30
```

```kusto
// 3. Check for failed scale-out attempts (capacity issues)
KustoLogs
| where Source startswith 'MANAGE-'
| where Directory startswith 'AutoScale'
| where EventText has '<CLUSTER>'
| where EventText has 'fail' or EventText has 'error' or EventText has 'capacity'
| where Timestamp between(datetime(<START>) .. datetime(<END>))
| project Timestamp, EventText
```

```kusto
// 4. Check autoscale configuration/reason (use on kuskushead)
ReasonWeDoOrDontScaleCluster('<CLUSTER>', 14d, 'ScaleOut', true)
| where Timestamp between(datetime(<START>) .. datetime(<END>))
| project Timestamp, EventText
```

#### Key Interpretation Points
- If the cluster was already at **max nodes** and couldn't scale further → recommend increasing max node count.
- If scale-out **failed** with capacity errors → flag as Fabric/region capacity constraint.
- If scale-out was **delayed** (hours after incident start) → note that reactive autoscale has inherent lag; consider predictive autoscale for this workload pattern.
- If scale-out **succeeded but didn't help** → identify the actual bottleneck (e.g., admin node for MV, single-node operations for large queries).
- For **Fabric Eventhouse clusters (TRD-)**: scaling is managed differently. Check Fabric capacity throttling instead.



### ⚠️ Always Bucket `FailureReason` Before Summarizing Failures

`FailureReason` (and similar free-text fields like `Alerts.Message`) often embeds **variable content**
— GUIDs, shard IDs, blob storage URLs, extent IDs — inside the string. Running
`summarize count() by FailureReason` directly **fragments a single dominant root cause into hundreds
of near-unique rows**, hiding it from a top-N view.

**Always bucket first** using `substring(FailureReason, 0, 1000)` plus a `case()` classifier into
≤15 canonical categories, *before* looking at raw `FailureReason` grouping. Full technique, reusable
`let` statement, and a real example (CSADATAPOOL: raw grouping showed only ~4 rows for
`PartialQueryEvaluator`, bucketing revealed 1,008 — the largest failure category on the cluster, caused
by storage-account throttling) are documented in
[`references/knowledge/failure-reason-bucketing.md`](references/knowledge/failure-reason-bucketing.md).

A raw top-N `FailureReason` list that looks like "many small reasons, no dominant cause" is itself a
signal that fragmentation is hiding a real dominant bucket — treat it as a prompt to bucket, not a
conclusion that failures are diffuse.

### Two Kinds of Throttling

#### 1. Fabric Capacity Throttling (Fabric clusters only)
Occurs when the Fabric capacity backing the Eventhouse is overloaded.

**Identified by FailureReason containing:**
> `"Unable to complete the action because your organization's Fabric compute capacity has exceeded its limits."`

Only possible on Fabric Eventhouse clusters (TRD- prefix). The fix is to increase the Fabric capacity SKU or reduce query load.

```kusto
QueryCompletion
| where Source == toupper('<cluster>')
| where FailureReason contains "Fabric compute capacity has exceeded its limits"
| summarize count() by bin(Timestamp, 1h)
```

#### 2. Concurrent Query Capacity Throttling (ADX and Fabric)
Occurs when the number of concurrent queries exceeds the cluster's concurrency limit.

**Identified by FailureReason containing:**
> `"The query was aborted due to throttling. Retrying after some backoff might succeed. Capacity:"`

The number after `Capacity:` is the maximum concurrent queries allowed. **Default = 10× the number of cores in the SKU.**

```kusto
QueryCompletion
| where Source == toupper('<cluster>')
| where FailureReason contains "aborted due to throttling"
| extend Capacity = extract(@"Capacity:\s*(\d+)", 1, FailureReason)
| summarize count() by bin(Timestamp, 1h), Capacity
```

###  MV and partitioning competing

When a Materialized View has a partitioning policy, the materialization and partitioning process can compete with each other.  Both processes run in parallel (i.e. they aren't sequenced) and a materialization process could delete records on an extent that is in the process of being partitioned.  This results in the partitioning process to be abandoned.

This increases MV lag.  Since partitioning needs to start over again.

This typically becomes a problem when:

1. MV's source table has a high ingestion volume
1. The summarize by time key bins is large (e.g. one day) or non-existent (i.e. no time bins)

This usually improves once the time window closes since partitioning can then occur uninterrupted.  However, the same issue starts on the new time window.

This usually results in a MV age metric rising during the time window and dropping at the end of the time window:  a sort of staircase pattern.

We do not have mitigation at this point in time.

We can detect that pattern using:

```kusto
KustoLogs
| where Source == toupper('<CLUSTER>')
| where Timestamp between(datetime(<START>) .. datetime(<END>))
| where EventText has "ExtentsPartitionCommand: Operation has completed with state 'Abandoned'. Details: "
| count
```

If no specific time window is provided, use `ago(7d)` as the default lookback period.

The more of those (i.e. the bigger the count) the more pronounced the problem is.  Again, this is an issue only if MV lag (age) is high.

### Always Show Tenant Name with Cluster Name

Whenever a cluster name is mentioned in an investigation or report, always include the tenant name alongside it.

Use `TenantName` from `DimClustersMv`:

```kusto
DimClustersMv() | where Source == toupper('<cluster name>') | project TenantName, Account, CustomerType | take 1
```

Example output: `TRD-NF0F4D4D8F02Q8G15N` → **Hanwha Qcells CES**



### ⚠️ Check Memento for Policies Before Concluding Root Cause

When a metric shows an unexpected or extreme value, **always check Memento for relevant policy changes before concluding the cause is a system or workload issue**. Policies set by users (sometimes years ago) are a common root cause that is easy to miss.
----
Key policy-related Memento event types to look for:

| Event pattern | What it controls |
|---|---|
| `ALTER-CLUSTER-QUERY-WEAK-CONSISTENCY-POLICY` | WC snapshot refresh interval, node counts |
| `ALTER-CLUSTER-RETENTION-POLICY` | Data retention |
| `ALTER-CLUSTER-MERGE-POLICY` | Extent merge behavior |
| `ALTER-CLUSTER-WORKLOAD-GROUP` | Concurrency, memory, query consistency |
| `ALTER-DATABASE-*-POLICY` | Database-level overrides |
| `ALTER-TABLE-*-POLICY` | Table-level overrides |

Example — check all policy changes for a cluster (no time filter):

```kusto
Memento()
| where Source == toupper('<cluster>')
| where Event has 'POLICY' or Event has 'WORKLOAD'
| project Timestamp, Event, ChangeCommand
| order by Timestamp asc
```

**Real example**: PRDEPMKUSTOCLUSTERE07B had `WeakConsistencySnapshotLatencySeconds` ~1700s. The root cause was `RefreshPeriodInSeconds: 1800` in the `query_weak_consistency` policy, set by the customer in June 2024 — not a system issue.


### ⚠️ Querying Memento — Do Not Restrict to Last 28 Days

When querying `Memento()` or `DmMemento()`, **do not add a time filter for the last 28 days** (or any short window). Changes to policies, tables, functions, and other objects can have been applied **years ago**. Memento contains data going back to **2023**.

Always search for the **latest change** to the same object — use `arg_max` or `top 1 by Timestamp desc` grouped by the object identifier:

```kusto
Memento()
| where ClusterName == toupper('<cluster>')
| where ObjectType == "Table" and ObjectName == "<table>"
| summarize arg_max(Timestamp, *) by ObjectName
```


### ⚠️ Telemetry Is Retained Only ~30 Days (Memento Excepted) — Never Infer an Onset from the Data Edge

**All engine/diagnostic telemetry — `QueryCompletion`, `CommandCompletion`, `KustoLogs`, `DimClusters`, `PerfCounterCPU`, `DataIngest*`, `Alerts`, materialized-view monitoring, etc. — is retained for only the last ~30 days.** `Memento()` / `DmMemento()` is the **exception** (retained long-term, back to 2023).

Because of this hard ~30-day left edge, **do not**:

- Treat the **earliest visible timestamp** (`min(Timestamp)`, the first non-empty day/bin, the first row of an `ago(90d)`/`ago(180d)` query) as an **onset / first-occurrence date**. A query returning "nothing before date X" almost always just means the data aged out at the retention boundary, **not** that the phenomenon started on X.
- Make any **"last 30 days vs. the period before"** comparison, or conclude an issue/workload is **"new"**, **"just started"**, or **"was cut over"** on a given date, using these tables.

**What you *can* do:**

- State counts/trends as **within-window** ("N failures visible in the ~30-day window", "upward within the window"). A long lookback (`ago(180d)`) returning only ~30 days of data is expected — say so explicitly rather than reading it as an onset.
- Use **`Memento()`** for any genuine before/after or "did something change" question that must reach further back than ~30 days (e.g. policy, table/function definition, follower, workload-group, version changes).

When a report or finding depends on when something began, add an explicit caveat noting the ~30-day retention limit and that no onset date can be asserted from telemetry.


### Identifying External vs. Internal Customers

Use the `CustomerType` column in `DimClustersMv` to determine if a customer is external or internal:

- `CustomerType == "External"` → external (paying) customer
- `CustomerType == "Internal"` → Microsoft-internal cluster

```kusto
DimClustersMv() | where ClusterName == "<cluster>" | project ClusterName, CustomerType
```

### Checking if multi-admin will help ease the load on the admin node

If there is an extreme load on the admin node, check for query distribution across databases, if there are many databases and queries are equally distributed across them, it can benefit from using multi-admin configuration. 

**⚠️ Do NOT recommend multi-admin when queries are concentrated on a single database.** Multi-admin works by separating load per admin per database across different nodes. If all queries target the same database, multi-admin provides no benefit — all queries will still route to the same admin node. Only recommend multi-admin when queries are distributed across multiple databases.


### Opening Geneva Health Dashboard for a Cluster

When investigating a cluster, the **Geneva Health Dashboard V3** provides real-time monitoring (CPU, memory, ingestion, query latency, etc.) that complements KQL-based diagnostics.

To discover the pre-built Geneva Health Dashboard URL for any cluster, run:

```kusto
// Run on kuskushead.westeurope/Kuskus
GetServiceUrls("<CLUSTER_NAME>")
| project Geneva
```

This returns a URL like:
```
https://jarvis-west.dc.ad.msft.net/dashboard/KustoMonitoring/...&overrides=[{"query":"//*[id='ClusterName']","key":"value","replacement":"<CLUSTER>"}]
```

The URL includes the correct monitoring account for the cluster's region (e.g., `KustoEastUS`, `KustoWestEurope`).

> **Tip:** Always prefer this URL over manually constructing Geneva dashboard links — it resolves the correct monitoring account and dashboard version automatically.

> **Note:** `GetServiceUrls` is a function on `kuskushead.westeurope/Kuskus`. The cluster name argument should be in UPPERCASE.

---

## Output Format

**⚠️ Every investigation, regardless of type or size, must produce a saved report file under
`Investigations/yyyy-mm/`** — never answer an investigation purely in chat without also writing
the corresponding `.md` file (see naming/folder convention below). This applies to quick checks
("check for query failures in X") just as much as full health checks or multi-day analyses.

Format as copy-pasteable summary for Outlook.

> **⚠️ Prerequisite — resolve failed queries first.** Before writing the report, confirm **every** query
> used in the investigation executed successfully. If any query is still failing, apply the
> **Query Failure Recovery** loop above (correct via kuskus knowledge and rerun). **Do not create the
> report until all queries are corrected** — or, for a signal proven unobtainable, until its unavailability
> and the exact error are explicitly noted in the report.

> **⚠️ Always add this disclaimer at the very top of the report** (before the first section), verbatim:
> > **Disclaimer:** This diagnosis has been generated by an AI Agent. AI-generated content might be incorrect — please review carefully before use. If you have any doubts, feel free to validate these findings with us at any time.

> **⚠️ Never mention other customers, tenants, or their clusters in the customer-facing report ("Investigation Summary").** Do not reference other customers' cluster names, tenant names, or "previously documented patterns on other clusters" — even generically. Findings and comparisons must be framed solely in terms of the investigated cluster itself. (Cross-cluster context, if genuinely needed, may only appear in the internal section, and even there without exposing other customers' identities.)

Create 2 main sections: 
* "Investigation Summary" 
tenant name, cluster name, investigation timeline, issue summary, root cause, impact metrics, etc.(finding, KQL query, root cause, impact, mitigation).

* "Investigation Summary including Queries (Internal use)". 
Include the prompts
tenant name, cluster name, investigation timeline, issue summary, root cause, impact metrics, etc.(finding, KQL query, root cause, impact, mitigation). Include KQL queries for every point and conclusion.

The 2 sections should be identical, but the first section should be the report without the KQL queries, while the second section should include all the KQL queries, and supporting data.

Save it under the month derived from the filename date:
`Investigations/yyyy-mm/yyyy-mm-dd-tenantname-clustername-report.md` (unless
specified otherwise). Create the `yyyy-mm` folder when it does not exist.

> **Including chart images:** `query_kusto.py` returns raw JSON, not a rendered Kusto chart —
> to embed a real timechart image in a report, generate it with matplotlib into an
> in-memory buffer and embed it as a base64 `data:image/png;base64,...` URI directly in the
> markdown — **never** save a separate `.png` file. **Every health-check investigation must
> include the CPU cores breakdown (query/ingest/materialize/other) as a timechart**
> — `scripts/invoke_health_check.py` generates it automatically; charts are
> optional for all other investigation types. See
> [`references/knowledge/chart-generation.md`](references/knowledge/chart-generation.md) for the
> step-by-step method and reusable code patterns.
