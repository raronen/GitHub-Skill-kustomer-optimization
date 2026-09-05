# Materialized Views (MV) Investigation Guide

A comprehensive guide for diagnosing Materialized View issues on Azure Data Explorer / Kusto clusters using Kuskus functions and KustoMdmMetricsV1 metrics.

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start Investigation Flowchart](#quick-start-investigation-flowchart)
3. [Available Kuskus Functions](#available-kuskus-functions)
4. [Available MDM Metrics](#available-mdm-metrics)
5. [Investigation Scenarios](#investigation-scenarios)
6. [Function Reference & Schemas](#function-reference--schemas)
7. [Ready-to-Use Investigation Queries](#ready-to-use-investigation-queries)
8. [Tips & Pitfalls](#tips--pitfalls)

---

## Overview

Materialized Views (MVs) in Kusto continuously aggregate data from a source table using an aggregation query. The engine materializes incrementally — processing only new extents ingested since the last materialization cycle. When MVs malfunction, the typical symptoms are:

- **Lag**: The MV falls behind the source table (increasing age/growing delta).
- **Failures**: Materialization cycles fail repeatedly.
- **Resource pressure**: MV refresh consumes excessive CPU/memory, competing with queries and ingestion.
- **Data loss**: Extents are dropped or not materialized.

### Key Concepts

| Concept | Description |
|---|---|
| **Delta** | Un-materialized extents — data that has been ingested into the source table but not yet processed by the MV. |
| **Age** | How far behind the MV is from the source table, measured in minutes or seconds. |
| **MaterializedTo** | The cursor timestamp up to which the MV has processed data. |
| **Cycle / Run** | A single materialization iteration that processes a batch of delta extents. |
| **Lookback** | Period the MV query looks back when re-materializing (affects dedup/arg_max views). |
| **Extent Rebuild** | Full or partial rebuild of the MV's extents, usually expensive. |
| **Load Factor** | Ratio of MV work to cluster capacity — high values indicate saturation. |

### Choosing the Kuskus Endpoint

- **All regions / global fleet:** Run the query on
  `https://kuskushead.westeurope.kusto.windows.net` using the `Kuskus`
  database. Kuskushead sends the query to all regional Kuskus instances, so
  do not query each regional endpoint separately or manually merge the results.
- **Specific cluster only:** Use
  `DimClustersMv().RegionalTracingTargetUrl` as the Kuskus endpoint.

---

## Quick Start Investigation Flowchart

```
Customer reports MV issue
        │
        ▼
┌──────────────────────────┐
│ 1. Get cluster info      │
│    DimClustersMv()       │
│    (tenant, SKU, region) │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ 2. Check MV health overview     │
│    MaterializedViewsMonitoring() │
│    → Age trend? LastRun?        │
└──────────┬───────────────────────┘
           │
     ┌─────┴─────┐
     │           │
  Age stable  Age increasing
     │           │
     ▼           ▼
┌──────────┐  ┌────────────────────────┐
│ Check    │  │ 3. Check errors        │
│ errors   │  │    MaterializedViews-   │
│ & delta  │  │    Errors()            │
└────┬─────┘  │    MaterializedViews-   │
     │        │    UnknownErrors()     │
     │        └──────────┬─────────────┘
     │                   │
     ▼                   ▼
┌──────────────┐  ┌──────────────────────┐
│ 4. Check     │  │ 5. Check durations   │
│    MDM       │  │    MaterializedViews- │
│    metrics   │  │    Durations()       │
│    for trend │  │    → Duration, Ratio │
└──────────────┘  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ 6. Check resource    │
                  │    pressure (CPU,    │
                  │    memory, triggers) │
                  │    MaterializedViews- │
                  │    Trigger()         │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ 7. Check Memento for │
                  │    policy changes    │
                  │    (MV definition,   │
                  │    merge policy,     │
                  │    retention)        │
                  └──────────────────────┘
```

---

## Available Kuskus Functions

### MV-Specific Functions

| Function | Parameters | Purpose |
|---|---|---|
| `MaterializedViewsMonitoring` | `(startTime, endTime)` | **Primary health overview** — age trend, delta count, last run result per MV per cluster |
| `MaterializedViewsAgeMetric` | `(startTime, endTime)` | MV age over time from MDM metrics, good for trending |
| `MaterializedViewsCompletionMetric` | `(startTime, endTime)` | Completion status per materialization cycle |
| `MaterializedViewsDurations` | `(startTime, endTime)` | Duration of each materialization cycle with delta counts |
| `MaterializedViewsErrors` | `(startTime, endTime, source)` | Errors from failed materialization cycles (filter by cluster) |
| `MaterializedViewsUnknownErrors` | `(startTime, endTime)` | Unclassified/unexpected errors from MV processing |
| `MaterializedViewsAlerts` | `(startTime, endTime)` | Alert-level events from MV processing |
| `MaterializedViewsTrigger` | `(startTime, endTime)` | Trigger decisions: concurrency slots, available views, capacity |
| `MaterializedViewsParseStatus` | `(start, end)` | Parsed MV status: records in delta, cursors, health, query |
| `MaterializedViewsStatisticsCollector` | `(fromTime, toTime)` | Statistics collection success/failure tracking |
| `MaterializedViewByRaid` | `(rootActivityId)` | Lookup a specific MV operation by RootActivityId |
| `MaterializedViewsArgMaxOptimization` | `()` | arg_max optimization analysis — duplicates, efficiency |
| `MaterializedViewsRetainRemoveStats` | `()` | Extent retain/remove statistics during MV processing |
| `MaterializedViewsSoftDeletePartitions` | `()` | Soft-delete partition processing for MVs |
| `MaterializedViewParseSampleExtentRebuild` | `(startTime, endTime)` | Sampled extent rebuild analysis |

---

## Available MDM Metrics

These metrics are available in `KustoMdmMetricsV1()` and provide time-series monitoring data for MVs.

### Core MV Metrics (in `MdmEngineMetrics` namespace)

| Metric Name | Dimensions | Description |
|---|---|---|
| `MaterializedViewHealth` | `Account^Cluster^Database^DataCenter^MaterializedViewName^ResourceId^VirtualClusterName` | Health status of each MV (1 = healthy, 0 = unhealthy). **Primary health indicator.** |
| `MaterializedViewAgeMinutes` | `Account^Cluster^Database^DataCenter^MaterializedViewName^ResourceId^VirtualClusterName` | How many minutes the MV lags behind the source table. **Primary lag indicator.** |
| `MaterializedViewAgeSeconds` | `Account^Cluster^Database^DataCenter^MaterializedViewName^ResourceId` | Same as above but in seconds — finer granularity for low-lag views. |
| `MaterializedViewResult` | `Account^Cluster^Database^DataCenter^MaterializedViewName^ResourceId^Result^VirtualClusterName` | Result of each materialization cycle (Success/Failure). Use to count success rate. |
| `MaterializedViewRecordsInDelta` | `Account^Cluster^Database^DataCenter^MaterializedViewName^ResourceId` | Number of records waiting to be materialized. High values indicate the MV is falling behind. |
| `MaterializedViewExtentsRebuild` | `Account^Cluster^Database^DataCenter^MaterializedViewName^ResourceId^VirtualClusterName` | Count of extent rebuild operations. Frequent rebuilds indicate inefficiency. |
| `MaterializedViewDataLoss` | `Account^Cluster^Database^DataCenter^Kind^MaterializedViewName^ResourceId` | Data loss events — critical alert indicator. |
| `MaterializedViewDuplicates` | `(none)` | Duplicate record detection across MV extents. |
| `MaterializedViewsInProgress` | `Account^CloudName^Cluster^DataCenter^...^ResourceId^VirtualClusterName` | Number of MVs currently being materialized. |
| `MaterializedViewsLoadFactor` | `Account^CloudName^Cluster^DataCenter^...^ResourceId^VirtualClusterName` | Ratio of MV work to available capacity. Values close to 1.0 mean the cluster is saturated with MV work. |
| `MaterializedViewsTrigger` | `Account^Cluster^DataCenter^ResourceId` | Trigger events for MV scheduling. |

### Continuous MV Metrics (in `MdmEngineMetrics` namespace)

| Metric Name | Dimensions | Description |
|---|---|---|
| `ContinuousMaterializedViewDurationSeconds` | `Account^Cluster^ContinuousMaterializedViewName^Database^DataCenter^Result` | Duration of each continuous MV cycle in seconds. |
| `ContinuousMaterializedViewLatencyMinutes` | `Account^CloudName^Cluster^ContinuousMaterializedViewName^Database^DataCenter^...^ErrorCode^IsErrorPermanent^...` | Latency of continuous MV processing in minutes. Includes error code and permanence flag for failure analysis. |
| `ContinuousMaterializedViewResult` | `Account^Cluster^ContinuousMaterializedViewName^Database^DataCenter^Result` | Success/failure result of continuous MV cycles. |
| `ContinuousMaterializedViewScopePeriodMinutes` | `Account^Cluster^ContinuousMaterializedViewName^Database^DataCenter` | Scope period of the continuous MV in minutes — how much data each cycle covers. |

### How to Query MDM Metrics

```kusto
// General pattern for querying MV metrics
KustoMdmMetricsV1()
| where TIMESTAMP > ago(7d)
| where Cluster == toupper('<cluster>')
| where metricName == '<metric name>'
| extend dims = split(dimensionNameList, '^'), vals = split(dimensionValueList, '^')
| extend MaterializedViewName = tostring(vals[array_index_of(dims, 'MaterializedViewName')])
| summarize avg_value = avg(todouble(sumValue) / iff(countValue == 0, 1.0, todouble(countValue))),
            max_value = max(maxValue)
    by MaterializedViewName, bin(TIMESTAMP, 1h)
```

---

## Investigation Scenarios

### Scenario 1: MV is lagging / age is increasing

**Symptoms**: Customer reports stale data when querying the MV. Age is increasing over time.

**Investigation steps**:

```kusto
// Step 1: Check current MV age and whether it is increasing over time
MaterializedViewsMonitoring(ago(7d), now())
| where Source == toupper('<cluster>')
| project Source, ViewName, DatabaseName, Age, MaterializedTo, DeltaCount, LastRunResult, LastRun
| order by Age desc
```

```kusto
// Step 2: Trend the age over time using MDM metrics — look for sustained age increase
KustoMdmMetricsV1()
| where TIMESTAMP > ago(7d)
| where Cluster == toupper('<cluster>')
| where metricName == 'MaterializedViewAgeMinutes'
| extend dims = split(dimensionNameList, '^'), vals = split(dimensionValueList, '^')
| extend MVName = tostring(vals[array_index_of(dims, 'MaterializedViewName')])
| summarize maxAge = max(maxValue) by MVName, bin(TIMESTAMP, 1h)
| render timechart
```

```kusto
// Step 3: Check records in delta — are they growing?
KustoMdmMetricsV1()
| where TIMESTAMP > ago(7d)
| where Cluster == toupper('<cluster>')
| where metricName == 'MaterializedViewRecordsInDelta'
| extend dims = split(dimensionNameList, '^'), vals = split(dimensionValueList, '^')
| extend MVName = tostring(vals[array_index_of(dims, 'MaterializedViewName')])
| summarize maxDelta = max(maxValue) by MVName, bin(TIMESTAMP, 1h)
| render timechart
```

```kusto
// Step 4: Check materialization durations — are cycles taking too long?
MaterializedViewsDurations(ago(7d), now())
| where Source == toupper('<cluster>')
| summarize avgDuration = avg(Duration / 1s), maxDuration = max(Duration / 1s),
            avgDelta = avg(DeltaCount), totalFailed = countif(Result != 'Completed')
    by ViewName, bin(Timestamp, 1h)
| order by avgDuration desc
```

```kusto
// Step 5: Check trigger capacity — is the cluster able to schedule MV runs?
MaterializedViewsTrigger(ago(7d), now())
| where Source == toupper('<cluster>')
| project Timestamp, NumViewsToRunConcurrently, NumViewsAvailableForMaterialization, ConcurrentPolicy, Capacity
| order by Timestamp desc
```

```kusto
// Step 6: Check MV load factor via MDM — is MV work saturating the cluster?
KustoMdmMetricsV1()
| where TIMESTAMP > ago(7d)
| where Cluster == toupper('<cluster>')
| where metricName == 'MaterializedViewsLoadFactor'
| summarize avgLoad = avg(todouble(sumValue) / iff(countValue == 0, 1.0, todouble(countValue))),
            maxLoad = max(maxValue)
    by bin(TIMESTAMP, 1h)
| render timechart
```

**Common root causes**:
- Ingestion volume spike → delta grows faster than the MV can process
- Complex aggregation query → each cycle takes too long
- Too many MVs competing for limited concurrency slots
- Cluster under-provisioned or CPU-saturated by queries
- Merge policy producing many small extents

---

### Scenario 2: MV is failing / errors

**Symptoms**: MV marked unhealthy, LastRunResult shows failure.

**Investigation steps**:

```kusto
// Step 1: Get errors for the cluster
MaterializedViewsErrors(ago(7d), now(), toupper('<cluster>'))
| project Timestamp, ViewName, Database, Result, Level, EventText
| order by Timestamp desc
```

```kusto
// Step 2: Check for unknown/unclassified errors
MaterializedViewsUnknownErrors(ago(7d), now())
| where Source == toupper('<cluster>')
| project Timestamp, ViewName, Database, Result, Level, EventText, Machine
| order by Timestamp desc
```

```kusto
// Step 3: Check error trends via MDM
KustoMdmMetricsV1()
| where TIMESTAMP > ago(7d)
| where Cluster == toupper('<cluster>')
| where metricName == 'MaterializedViewResult'
| extend dims = split(dimensionNameList, '^'), vals = split(dimensionValueList, '^')
| extend MVName = tostring(vals[array_index_of(dims, 'MaterializedViewName')])
| extend Result = tostring(vals[array_index_of(dims, 'Result')])
| summarize count = sum(countValue) by MVName, Result, bin(TIMESTAMP, 1h)
| render timechart
```

```kusto
// Step 4: Check completion metric for the specific MV
MaterializedViewsCompletionMetric(ago(7d), now())
| where Source == toupper('<cluster>')
| summarize count() by ViewName, Result, bin(Timestamp, 1h)
| order by Timestamp desc
```

```kusto
// Step 5: Drill into a specific failed run
MaterializedViewByRaid('<rootActivityId from step 1>')
```

**Common error categories**:
- **Semantic errors**: MV query references a column/function that no longer exists — check Memento for schema changes
- **Resource errors**: Out of memory / CPU during materialization — check cluster resource pressure
- **Throttling**: Concurrent MV limit reached — check `MaterializedViewsTrigger()`
- **Timeout**: Cycle exceeds time limit — MV query too complex or delta too large

---

### Scenario 3: MV consuming excessive resources

**Symptoms**: High CPU on cluster correlated with MV activity, queries slowing down.

**Investigation steps**:

```kusto
// Step 1: Check MV command CPU consumption
CommandCompletion
| where Source == toupper('<cluster>')
| where Timestamp > ago(7d)
| where ActivityType has "MaterializedView"
| summarize Total = count(), Failed = countif(State == 'Failed'),
            avg_cpu_ms = avg(TotalCpuMs), max_cpu_ms = max(TotalCpuMs),
            avg_duration = avg(Duration / 1s)
    by ActivityType, bin(Timestamp, 1d)
| order by Timestamp asc
```

```kusto
// Step 2: Check MV load factor
KustoMdmMetricsV1()
| where TIMESTAMP > ago(7d)
| where Cluster == toupper('<cluster>')
| where metricName == 'MaterializedViewsLoadFactor'
| summarize avgLoad = avg(todouble(sumValue) / iff(countValue == 0, 1.0, todouble(countValue)))
    by bin(TIMESTAMP, 1h)
| render timechart
```

```kusto
// Step 3: Check MVs in progress — are too many running concurrently?
KustoMdmMetricsV1()
| where TIMESTAMP > ago(7d)
| where Cluster == toupper('<cluster>')
| where metricName == 'MaterializedViewsInProgress'
| summarize maxInProgress = max(maxValue) by bin(TIMESTAMP, 1h)
| render timechart
```

```kusto
// Step 4: Correlate with cluster CPU
KustoMdmMetricsV1()
| where TIMESTAMP > ago(7d)
| where Cluster == toupper('<cluster>')
| where metricNamespace == 'engineMetrics'
| where metricName == '\\Processor(_Total)\\% Processor Time'
| summarize avgCpu = avg(maxValue) by bin(TIMESTAMP, 1h)
| render timechart
```

```kusto
// Step 5: Check MV durations for heavy cycles
MaterializedViewsDurations(ago(7d), now())
| where Source == toupper('<cluster>')
| where Duration > 5m
| project Timestamp, ViewName, Duration, DeltaCount, Result, Ratio
| order by Duration desc
```

---

### Scenario 4: MV data loss

**Symptoms**: Data appears missing from MV results compared to source table.

**Investigation steps**:

```kusto
// Step 1: Check for data loss events
KustoMdmMetricsV1()
| where TIMESTAMP > ago(7d)
| where Cluster == toupper('<cluster>')
| where metricName == 'MaterializedViewDataLoss'
| extend dims = split(dimensionNameList, '^'), vals = split(dimensionValueList, '^')
| extend MVName = tostring(vals[array_index_of(dims, 'MaterializedViewName')])
| extend Kind = tostring(vals[array_index_of(dims, 'Kind')])
| where sumValue > 0 or maxValue > 0
| project TIMESTAMP, MVName, Kind, sumValue, maxValue
| order by TIMESTAMP desc
```

```kusto
// Step 2: Check extent rebuild operations
KustoMdmMetricsV1()
| where TIMESTAMP > ago(7d)
| where Cluster == toupper('<cluster>')
| where metricName == 'MaterializedViewExtentsRebuild'
| extend dims = split(dimensionNameList, '^'), vals = split(dimensionValueList, '^')
| extend MVName = tostring(vals[array_index_of(dims, 'MaterializedViewName')])
| summarize totalRebuilds = sum(countValue) by MVName, bin(TIMESTAMP, 1d)
| order by totalRebuilds desc
```

```kusto
// Step 3: Check retain/remove stats
MaterializedViewsRetainRemoveStats()
| where Source == toupper('<cluster>')
| project Timestamp, ViewName, ExtentId, RowCount, ToRetain, ToDelete
| order by Timestamp desc
```

```kusto
// Step 4: Check MV parse status — cursor gaps?
MaterializedViewsParseStatus(ago(7d), now())
| where Source == toupper('<cluster>')
| project Timestamp, ViewName, Database, RecordsInDelta, FromCursor, ToCursor, Healthy, Query
| order by Timestamp desc
```

---

### Scenario 5: MV not updating at all

**Symptoms**: MaterializedTo timestamp is stuck, no recent runs.

**Investigation steps**:

```kusto
// Step 1: Check monitoring — when was the last run?
MaterializedViewsMonitoring(ago(7d), now())
| where Source == toupper('<cluster>')
| project ViewName, MaterializedTo, Age, LastRunResult, LastRun, DeltaCount
| order by LastRun asc
```

```kusto
// Step 2: Check trigger — is the scheduler even trying?
MaterializedViewsTrigger(ago(7d), now())
| where Source == toupper('<cluster>')
| project Timestamp, NumViewsToRunConcurrently, NumViewsAvailableForMaterialization, ConcurrentPolicy, Capacity
| order by Timestamp desc
| take 50
```

```kusto
// Step 3: Check alerts for blocking conditions
MaterializedViewsAlerts(ago(7d), now())
| where Source == toupper('<cluster>')
| project Timestamp, Level, EventText, RootActivityId
| order by Timestamp desc
```

```kusto
// Step 4: Check MV definition in Memento — was it disabled or altered?
let entities = dynamic(["<MV name>", "<source table name>"]);
Memento()
| where Source == toupper('<cluster>')
| where EntityName in (entities) or UpdatedEntityName in (entities)
| project Timestamp, Event, EntityName, UpdatedEntityName, ChangeCommand
| order by Timestamp desc
```

```kusto
// Step 5: Check statistics collector — is the stats pipeline working?
MaterializedViewsStatisticsCollector(ago(7d), now())
| where Source == toupper('<cluster>')
| project Timestamp, ViewName, Kind, SuccessReportTimestamp, SuccessNumRecords,
          FailureReportTimestamp, FailureNumRecords, Result
| order by Timestamp desc
```

---

### Scenario 6: arg_max MV performance issues

**Symptoms**: arg_max-based MVs are slow, producing duplicates, or rebuilding frequently.

```kusto
// Step 1: Check arg_max optimization analysis
MaterializedViewsArgMaxOptimization()
| where Source == toupper('<cluster>')
| project Timestamp, View, Result, Count, Dcount, Percent, DuplicatesCountString, TargetNumIngestion
| order by Timestamp desc
```

```kusto
// Step 2: Check for duplicate records
KustoMdmMetricsV1()
| where TIMESTAMP > ago(7d)
| where Cluster == toupper('<cluster>')
| where metricName == 'MaterializedViewDuplicates'
| where sumValue > 0
| project TIMESTAMP, sumValue, maxValue, countValue
```

---

## Function Reference & Schemas

### `MaterializedViewsMonitoring(startTime, endTime)`
**Purpose**: Primary health overview for all MVs on a cluster.

| Column | Type | Description |
|---|---|---|
| `Source` | string | Cluster name (uppercase) |
| `Timestamp` | datetime | When the status was captured |
| `ViewName` | string | Name of the materialized view |
| `DatabaseName` | string | Database containing the MV |
| `DeltaCount` | long | Number of un-materialized extents |
| `MaterializedTo` | datetime | Cursor timestamp — how far the MV has processed |
| `Age` | timespan | How far behind the source table the MV is. Focus on whether age is **increasing over time** rather than the absolute value. |
| `LastRunResult` | string | Result of the most recent materialization cycle |
| `LastRun` | datetime | Timestamp of the most recent materialization cycle |

---

### `MaterializedViewsAgeMetric(startTime, endTime)`
**Purpose**: Age/lag time-series from MDM metrics for trending analysis.

| Column | Type | Description |
|---|---|---|
| `Source` | string | Cluster name |
| `Timestamp` | datetime | Metric timestamp |
| `MonitoringAccount` | string | Geneva monitoring account |
| `KustoAccount` | string | Kusto account name |
| `KustoCluster` | string | Cluster name |
| `DataCenter` | string | Datacenter/region |
| `CloudName` | string | Cloud environment |
| `ResourceId` | string | Azure resource ID |
| `MetricName` | string | Name of the metric being reported |
| `Value` | long | Metric value (age in the relevant unit) |

---

### `MaterializedViewsDurations(startTime, endTime)`
**Purpose**: Duration and details of each materialization cycle.

| Column | Type | Description |
|---|---|---|
| `Timestamp` | datetime | When the cycle ran |
| `Source` | string | Cluster name |
| `ViewName` | string | MV name |
| `DatabaseName` | string | Database name |
| `Result` | string | Cycle result (Completed, Failed, etc.) |
| `Duration` | timespan | How long the cycle took |
| `Range` | timespan | Time range of data processed in this cycle |
| `DeltaCount` | long | Number of extents processed |
| `Exception` | string | Exception message if failed |
| `RootActivityId` | string | Activity ID for drill-down |
| `Ratio` | real | Duration-to-range ratio — values > 1.0 mean the MV cannot keep up |

---

### `MaterializedViewsErrors(startTime, endTime, source)`
**Purpose**: Errors from failed materialization cycles for a specific cluster.

| Column | Type | Description |
|---|---|---|
| `RootActivityId` | string | Activity ID of the failed cycle |
| `ViewName` | string | MV name |
| `Database` | string | Database name |
| `Result` | string | Error classification |
| `Timestamp` | datetime | When the error occurred |
| `RootActivityId1` | string | Related activity ID (from trace) |
| `Level` | string | Log level (Error, Warning, etc.) |
| `EventText` | string | Detailed error message |

---

### `MaterializedViewsUnknownErrors(startTime, endTime)`
**Purpose**: Unclassified/unexpected errors — these often indicate bugs or new failure modes.

| Column | Type | Description |
|---|---|---|
| `Timestamp` | datetime | When the error occurred |
| `RootActivityId` | string | Activity ID |
| `ViewName` | string | MV name |
| `Database` | string | Database name |
| `Result` | string | Error result |
| `Source` | string | Cluster name |
| `Timestamp1` | datetime | Trace event timestamp |
| `Directory` | string | Log directory |
| `Level` | string | Log level |
| `Machine` | string | Node that reported the error |
| `InstanceID` | string | Service instance |
| `ProcessID` | int | Process ID |
| `ThreadID` | int | Thread ID |
| `ActivityID` | string | Activity ID |
| `RootActivityId1` | string | Root activity (trace) |
| `ActivityType` | string | Activity type |
| `ClientActivityId` | string | Client activity ID |
| `SourceId` | string | Source identifier |
| `EventText` | string | Full error text |

---

### `MaterializedViewsTrigger(startTime, endTime)`
**Purpose**: MV scheduler decisions — how many MVs can run and actual capacity.

| Column | Type | Description |
|---|---|---|
| `Source` | string | Cluster name |
| `Timestamp` | datetime | Decision timestamp |
| `RootActivityId` | string | Activity ID |
| `NumViewsToRunConcurrently` | int | How many MVs the scheduler decided to run concurrently |
| `NumViewsAvailableForMaterialization` | int | How many MVs have pending delta work |
| `ConcurrentPolicy` | int | Configured concurrency policy limit |
| `Capacity` | int | Effective capacity for MV runs |

---

### `MaterializedViewsCompletionMetric(startTime, endTime)`
**Purpose**: Completion records for each materialization cycle.

| Column | Type | Description |
|---|---|---|
| `Source` | string | Cluster name |
| `Timestamp` | datetime | Completion timestamp |
| `RootActivityId` | string | Activity ID |
| `ClientActivityId` | string | Client activity ID |
| `ViewName` | string | MV name |
| `Database` | string | Database name |
| `Result` | string | Result (Completed, Failed, etc.) |

---

### `MaterializedViewsParseStatus(start, end)`
**Purpose**: Parsed MV status with cursor and delta details.

| Column | Type | Description |
|---|---|---|
| `Source` | string | Cluster name |
| `Timestamp` | datetime | Status timestamp |
| `ViewName` | string | MV name |
| `Database` | string | Database name |
| `RecordsInDelta` | long | Records waiting to be materialized |
| `FromCursor` | datetime | Start cursor of current delta |
| `ToCursor` | datetime | End cursor of current delta |
| `Healthy` | bool | Health status |
| `Query` | string | The MV aggregation query definition |
| `RootActivityId` | string | Activity ID |

---

### `MaterializedViewsAlerts(startTime, endTime)`
**Purpose**: Alert-level trace events related to MV processing.

| Column | Type | Description |
|---|---|---|
| `Source` | string | Cluster name |
| `Timestamp` | datetime | Alert timestamp |
| `Directory` | string | Log directory |
| `Level` | string | Alert level |
| `Machine` | string | Reporting node |
| `InstanceID` | string | Service instance |
| `ProcessID` | int | Process ID |
| `ThreadID` | int | Thread ID |
| `ActivityID` | string | Activity ID |
| `RootActivityId` | string | Root activity ID |
| `ActivityType` | string | Activity type |
| `ClientActivityId` | string | Client activity ID |
| `SourceId` | string | Source identifier |
| `EventText` | string | Alert message text |

---

### `MaterializedViewsStatisticsCollector(fromTime, toTime)`
**Purpose**: Statistics collection pipeline health.

| Column | Type | Description |
|---|---|---|
| `Source` | string | Cluster name |
| `RootActivityId` | string | Activity ID |
| `ViewName` | string | MV name |
| `Timestamp` | datetime | Collection timestamp |
| `Kind` | string | Kind of statistics operation |
| `SuccessReportTimestamp` | datetime | Last successful report time |
| `SuccessNumRecords` | long | Records in last successful report |
| `FailureReportTimestamp` | datetime | Last failed report time |
| `FailureNumRecords` | long | Records in last failed report |
| `Result` | long | Overall result indicator |

---

### `MaterializedViewsArgMaxOptimization()`
**Purpose**: Deduplication/arg_max optimization analysis.

| Column | Type | Description |
|---|---|---|
| `Source` | string | Cluster name |
| `EventText` | string | Event details |
| `Timestamp` | datetime | Analysis timestamp |
| `ClientActivityId` | string | Client activity ID |
| `RootActivityId` | string | Root activity ID |
| `View` | string | MV name |
| `Result` | bool | Whether optimization was applied |
| `Count` | long | Total record count |
| `Dcount` | long | Distinct key count |
| `Percent` | int | Duplicate percentage |
| `DuplicatesCountString` | string | Distribution of duplicates |
| `TargetNumIngestion` | long | Target ingestion batch size |

---

### `MaterializedViewsRetainRemoveStats()`
**Purpose**: Extent retain/remove decisions during MV processing.

| Column | Type | Description |
|---|---|---|
| `Source` | string | Cluster name |
| `Timestamp` | datetime | Operation timestamp |
| `RootActivityId` | string | Activity ID |
| `Extents` | string | Extent details |
| `ViewName` | string | MV name |
| `ExtentId` | string | Specific extent ID |
| `RowCount` | long | Total rows in the extent |
| `ToRetain` | long | Rows retained |
| `ToDelete` | long | Rows deleted |

---

### `MaterializedViewsSoftDeletePartitions()`
**Purpose**: Soft-delete partition processing.

| Column | Type | Description |
|---|---|---|
| `Source` | string | Cluster name |
| `Timestamp` | datetime | Operation timestamp |
| `ClientActivityId` | string | Client activity ID |
| `RootActivityId` | string | Root activity ID |
| `ViewName` | string | MV name |
| `BatchSize` | long | Size of soft-delete batch |
| `Remaining` | long | Remaining partitions to process |
| `Iteration` | long | Current iteration number |

---

## Ready-to-Use Investigation Queries

### Quick Health Check (Copy-Paste)

```kusto
// Replace <cluster> with the cluster name
// Comprehensive MV health snapshot
MaterializedViewsMonitoring(ago(7d), now())
| where Source == toupper('<cluster>')
| project Source, ViewName, DatabaseName, Age, MaterializedTo, DeltaCount, LastRunResult, LastRun
| extend AgeMinutes = Age / 1m
| order by AgeMinutes desc
```

### Full MV Investigation Dashboard Query

```kusto
// All-in-one MV investigation for a cluster over the past 7 days
let cluster = toupper('<cluster>');
let start = ago(7d);
let end = now();
// Part 1: Health overview
let health = MaterializedViewsMonitoring(start, end)
| where Source == cluster
| summarize arg_max(Timestamp, *) by ViewName
| project ViewName, Age, MaterializedTo, DeltaCount, LastRunResult;
// Part 2: Error counts
let errors = MaterializedViewsErrors(start, end, cluster)
| summarize ErrorCount = count() by ViewName;
// Part 3: Duration stats
let durations = MaterializedViewsDurations(start, end)
| where Source == cluster
| summarize AvgDuration = avg(Duration / 1s), MaxDuration = max(Duration / 1s),
            FailedCycles = countif(Result != 'Completed'), TotalCycles = count()
    by ViewName;
// Join all
health
| join kind=leftouter errors on ViewName
| join kind=leftouter durations on ViewName
| project ViewName, Age, DeltaCount, LastRunResult, MaterializedTo,
          ErrorCount = coalesce(ErrorCount, 0),
          AvgDurationSec = round(coalesce(AvgDuration, 0.0), 1),
          MaxDurationSec = round(coalesce(MaxDuration, 0.0), 1),
          FailedCycles = coalesce(FailedCycles, 0),
          TotalCycles = coalesce(TotalCycles, 0)
| order by Age desc
```

### MV Definition Lookup via Memento

```kusto
// Find the MV creation/alter command and related policy changes
let entities = dynamic(["<MV name>", "<source table name>"]);
Memento()
| where Source == toupper('<cluster>')
| where EntityName in (entities) or UpdatedEntityName in (entities) or Event has 'MATERIALIZED'
| project Timestamp, Event, EntityName, UpdatedEntityName, ChangeCommand
| order by Timestamp desc
```

---

## Tips & Pitfalls

### ⚠️ Always Check Memento
Before concluding the root cause is a system issue, **always check Memento for policy/definition changes**. Common surprises:
- MV query was altered to include expensive joins
- Merge policy was changed, producing many small extents that overwhelm the MV
- Retention policy was shortened, causing cursor mismatches
- MV was disabled and re-enabled, triggering a full rebuild

### ⚠️ Ratio > 1.0 in `MaterializedViewsDurations`
If the `Ratio` column (Duration / Range) is consistently > 1.0, the MV **cannot keep up** with ingestion. Each cycle takes longer than the time window it covers, so the MV will fall further behind over time. Solutions:
- Simplify the MV aggregation query
- Reduce ingestion rate
- Increase cluster capacity
- Split the MV into multiple smaller views

### ⚠️ Concurrency Limits
The `MaterializedViewsTrigger` function shows how many MVs can run concurrently. If `NumViewsAvailableForMaterialization > Capacity`, MVs are queued. The default concurrency is controlled by the workload group policy.

### ⚠️ Fabric Eventhouses (TRD- prefix)
For a Fabric virtual cluster (VC), do not infer available cores from
`MachineCount` or a physical-cluster SKU. Read `EngineCoreLimit` from
`ServiceConfiguration.VirtualClusterSettings.Limits` instead.

Current core limit:

```kusto
DimClustersMv()
| where Source == toupper('<cluster>') and isnotempty(hoster)
| extend EngineCoreLimit =
    tolong(['ServiceConfiguration']['VirtualClusterSettings']['Limits']['EngineCoreLimit'])
| project Source, SourceQualified, Region, EngineCoreLimit
```

Core-limit history and changes:

```kusto
DimClusters
| where Cluster =~ '<cluster>'
| extend EngineCoreLimit =
    tolong(['ServiceConfiguration']['VirtualClusterSettings']['Limits']['EngineCoreLimit'])
| project LastUpdated, EngineCoreLimit
| order by LastUpdated asc
| serialize
| extend PreviousEngineCoreLimit = prev(EngineCoreLimit)
| where isnull(PreviousEngineCoreLimit)
    or EngineCoreLimit != PreviousEngineCoreLimit
```

`PerfCounterCPU` does not contain CPU utilization for Fabric virtual clusters.
Estimate VC engine CPU utilization by adding query CPU from
`QueryCompletion.TotalCPU` and command CPU from
`CommandCompletion.TotalCpuMs`, then normalizing the consumed CPU time by the
VC core limit and the duration of the time bin.

Both CPU columns are `timespan` values despite the `TotalCpuMs` name. Convert
both to the same unit before adding them:

```kusto
let StartTime = ago(1d);
let BinSize = 10m;
let ClusterInfo = materialize(
    DimClustersMv()
    | where Source == toupper('<cluster>') and isnotempty(hoster)
    | extend EngineCoreLimit =
        tolong(['ServiceConfiguration']['VirtualClusterSettings']['Limits']['EngineCoreLimit'])
    | project TelemetrySource = SourceQualified, EngineCoreLimit
);
let TelemetrySource = toscalar(ClusterInfo | project TelemetrySource);
let EngineCoreLimit = toscalar(ClusterInfo | project EngineCoreLimit);
union
(
    QueryCompletion
    | where Timestamp >= StartTime and Source == TelemetrySource
    | project Timestamp, CpuMs = tolong(TotalCPU / 1ms)
),
(
    CommandCompletion
    | where Timestamp >= StartTime and Source == TelemetrySource
    | project Timestamp, CpuMs = tolong(TotalCpuMs / 1ms)
)
| summarize UsedCpuMs = sum(CpuMs) by bin(Timestamp, BinSize)
| extend AvailableCpuMs =
    EngineCoreLimit * tolong(BinSize / 1ms)
| extend CpuUtilizationPct =
    100.0 * todouble(UsedCpuMs) / AvailableCpuMs
| project Timestamp, EngineCoreLimit, UsedCpuMs,
    CpuUtilizationPct = round(CpuUtilizationPct, 2)
```

For an investigation window that crosses a core-limit change, use
`DimClusters` history and apply the `EngineCoreLimit` that was effective in
each CPU time bin. Do not normalize the entire historical period using only
the latest value from `DimClustersMv()`.

For Fabric clusters, MV issues can also be caused by **Fabric capacity throttling** (separate from Kusto-level throttling). Always check:
```kusto
QueryCompletion
| where Source == toupper('<cluster>')
| where FailureReason contains "Fabric compute capacity has exceeded its limits"
| summarize count() by bin(Timestamp, 1h)
```

### ⚠️ MDM Metric Column Names
When querying `KustoMdmMetricsV1()`:
- The timestamp column is `TIMESTAMP` (all uppercase), not `Timestamp`
- Dimensions are in `dimensionNameList` and `dimensionValueList`, separated by `^`
- Values are pre-aggregated: use `sumValue / countValue` for averages, `maxValue` for peaks
- Always filter by `TIMESTAMP` first to limit scan scope

### Useful Cross-References
- **CPU during MV cycles**: For physical clusters, correlate
  `CommandCompletion` (where `ActivityType` has `"MaterializedView"`) with
  `PerfCounterCPU`. For Fabric VCs, use the normalized
  `QueryCompletion.TotalCPU` + `CommandCompletion.TotalCpuMs` method above.
- **Ingestion spikes**: Use `DataIngestHistoryMv()` or `KustoIngestion` metrics to check if ingestion bursts correlate with MV lag
- **Cluster scaling**: Use `DimClustersDailyMv()` to check if the cluster scaled during the MV issue period
