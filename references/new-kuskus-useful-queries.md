# KusKus Useful Queries — Organized by Information to Collect

This file maps each item from the "Information to collect" section to the specific KusKus queries needed.

> **Note:** Replace `<cluster name>` with the actual cluster name (always use `toupper()`). Adjust time ranges as needed.

---

## General Info

### Customer Tenant Name

```kusto
DimClustersMv()
| where Source == toupper('<cluster name>')
| project TenantName, Account, CustomerType
```

### Number of Clusters (for a customer/tenant)

```kusto
DimClustersMv()
| where TenantName == '<tenant name>'
| summarize ClusterCount = dcount(Source)
```

---

## Per Cluster Info

### Cluster Name, Region, SKU, Scaling Nodes (Min/Max)

```kusto
DimClustersMv()
| where Source == toupper('<cluster name>')
| project Source, Region, MachineSKU, MachineCount, SourceQualified,
    RegionalTracingTargetUrl
```

For a specific-cluster investigation, use `RegionalTracingTargetUrl` as the
Kuskus endpoint for subsequent queries, for both Fabric Eventhouses and classic
ADX clusters. For all-region or multi-region investigations, use
`kuskushead.westeurope` instead.

#### Scaling Patterns (weekdays, nights, etc.) (Number of Machines Over Time)
```kusto
DimClusters
| where Cluster == toupper('<cluster name>')
| where LastUpdated > ago(30d)
| order by LastUpdated asc
| where MachineCount != prev(MachineCount), or MachineSKU !=prev(MachineSKU)
| project Timestamp = LastUpdated, MachineCount, DayOfWeek = dayofweek(LastUpdated), HourOfDay = hourofday(LastUpdated)
```

### Ingestion Volume — Daily over past 30 days

```kusto
DataIngest
| where Source == toupper('<cluster name>')
| where Timestamp > ago(30d)
| summarize TotalIngestedGB = round(sum(OriginalSize) / pow(1024,3)) by bin(Timestamp, 1d)
| order by Timestamp asc
```

### Number of Extents per cluster and data size
```
//Hot data
KustoMdmMetricsV1
| where TIMESTAMP > ago(10m)
| where Cluster =='DATATUBEPRODMGMT'
| extend dimensionValueList = tostring(split(dimensionValueList,"^V3^",1)[0])
| where dimensionValueList == "Hot"
| where metricName in('ExtentsCount','ExtentsSize')
| summarize arg_max(TIMESTAMP,maxValue) by metricName, dimensionValueList
| summarize hotExtentSize = sumif(maxValue, metricName== "ExtentsSize"), hotExtentCount = sumif(maxValue, metricName== "ExtentsCount")
| extend averageExtentSize = round(hotExtentSize/hotExtentCount, 2)

//total data
KustoMdmMetricsV1
| where TIMESTAMP > ago(10m)
| where Cluster =='DATATUBEPRODMGMT'
| extend dimensionValueList = tostring(split(dimensionValueList,"^V3^",1)[0])
| where dimensionValueList == "Total"
| where metricName in('ExtentsCount','ExtentsSize')
| summarize arg_max(TIMESTAMP,maxValue) by metricName, dimensionValueList
| summarize totalExtentSize = sumif(maxValue, metricName== "ExtentsSize"), totalExtentCount = sumif(maxValue, metricName== "ExtentsCount")
| extend averageExtentSize = round(totalExtentSize/totalExtentCount, 2)
```


### Number of Extents per table
```
//get the number of extents per DB - works only when there are queries that were run in the time period
//https://dataexplorer.azure.com/clusters/kuskushead.westeurope/databases/Kuskus?

KustoLogs
| where Source == "<cluster name>"
| where Timestamp > ago(1d)
| where EventText has "TableExtentPrefilter.TraceStats:"
| project EventText
| parse EventText with * 'Database":"' DB '","Table":"' TBL '"' * '"TotalExtents":' Extents:long "," *
| summarize max(Extents) by DB, TBL
| order by max_Extents
```

> **Goal:** Each extent should be between 1GB and 2GB. If significantly smaller, merge policy may need adjustment.


### Ingested Data per Cluster (Daily Average GB in the last 30 days)

```kusto
DataIngestHistoryMv
| where Source has toupper('<cluster name>')
| extend Source = substring(Source, indexof(Source, ".") + 1)
| where Source == toupper('<cluster name>')
| where Day > ago(30d)
| summarize TotalOriginalSizeGB = round(sum(OriginalSize) / pow(1024,3), 2) by bin(Day, 1d)
| summarize AvgDailyIngestGB = round(avg(TotalOriginalSizeGB), 2)
```

### Database Count

```kusto
KustoMdmMetricsV1
| where TIMESTAMP > ago(10m)
| where Cluster =="<cluster name>"
| where metricName in('NumberOfDatabases')
| summarize arg_max(TIMESTAMP,maxValue) by metricName
```

### Tables Count per Database

```kusto
// ⚠️ NOT CORRECT: TBD — no query implemented yet.
// TBD
```

---

## Types of Investigations

---

### General — Hot Nodes & CPU

#### Are there hot nodes (CPU > 80%)?

```kusto
PerfCounterCPU
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| summarize avg_cpu = avg(CounterValue) by bin(Timestamp, 1h), Machine
| where avg_cpu > 80
| summarize HotNodes = dcount(Machine), TotalObservations = count() by bin(Timestamp, 1h)
| order by Timestamp asc
| render timechart
```

#### Identify hot node machines

```kusto
let bucket = 10m;
PerfCounterCPU
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize Cpu = avg(CounterValue) by Source, Machine, bin(Timestamp, bucket)
| summarize
    AvgCpu = round(avg(Cpu), 2),
    P95Cpu = round(percentile(Cpu, 95), 2),
    MaxCpu = round(max(Cpu), 2)
    by Source, Machine
| order by AvgCpu desc
```

#### Average cluster CPU vs. hot node outliers

```kusto
let nodeCpu =
    PerfCounterCPU
    | where Source == toupper('<cluster name>')
    | where Timestamp > ago(7d)
    | summarize Cpu = avg(CounterValue) by Source, Machine, bin(Timestamp, bucket);
let clusterCpu =
    nodeCpu
    | summarize ClusterAvgCpu = avg(Cpu) by Source, Timestamp;
nodeCpu
| join kind=inner clusterCpu on Source, Timestamp
| extend CpuAboveCluster = Cpu - ClusterAvgCpu
| summarize
    AvgCpu = round(avg(Cpu), 2),
    AvgClusterCpu = round(avg(ClusterAvgCpu), 2),
    AvgAboveCluster = round(avg(CpuAboveCluster), 2)
    by Source, Machine
| where AvgAboveCluster > 20
| order by AvgAboveCluster desc
```

#### Check if hot nodes are admin, multi-admin, or weak consistency

```kusto
KustoMdmMetricsV1
| where TIMESTAMP > ago(1d)
| where Cluster == toupper('<cluster name>')
| where metricName == "ActiveServiceInstances"
| where dimensionNameList == "Cluster^DataCenter^DeploymentRing^RoleInstance^ServiceType"
| parse dimensionValueList with * "^fabric://" ServiceType:string "/"
| where ServiceType in ("engine.weakconsistencyquery.svc", "engine.databaseadmin.svc")
| summarize dcount(RoleInstance), make_set(RoleInstance) by bin(TIMESTAMP, 10m), ServiceType
```

#### CPU to Duration ratio (level of query parallelism)

```kusto
QueryCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize totalCPU = sum(TotalCPU), totalDuration = sum(Duration) by bin(Timestamp, 1h)
| extend ratio = round(totalCPU / totalDuration, 2)
| summarize percentiles(ratio, 10, 50, 90, 95, 99) by Timestamp
```

#### Check for workload/query pattern changes

```kusto
QueryCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(14d)
| summarize QueryCount = count(), AvgCPU = avg(TotalCPU / 1s) by bin(Timestamp, 1d), Application = substring(Application, 0, 60)
| order by Timestamp asc, QueryCount desc
```

---

### Ingestion

#### Ingestion delays / latency

```kusto
DataIngest
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize avg(Duration), percentiles(Duration, 50, 90, 99) by bin(Timestamp, 1h)
| order by Timestamp asc
```

#### Ingestion failures / retries

```kusto
CommandCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| where ActivityType == 'DN.AdminCommand.DataIngestPullCommand'
| where State == 'Failed'
| summarize FailCount = count() by bin(Timestamp, 1h), FailureReason = substring(FailureReason, 0, 150)
| order by Timestamp asc
```

#### Ingestion volume spikes

```kusto
DataIngest
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize IngestedGB = round(sum(OriginalSize) / pow(1024,3), 2), RowCount = sum(RowCount) by bin(Timestamp, 1h)
| order by Timestamp asc
| render timechart
```

#### Ingestion throughput and batching

```kusto
DataIngest
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize IngestOps = count(), AvgBatchSizeMB = round(avg(OriginalSize) / 1048576.0, 2) by bin(Timestamp, 1h)
| order by Timestamp asc
```

#### Cost of update policies 
```kusto
DataOperations
| where Source == toupper('<cluster name>')
| where ClientActivityId == <Clientactivityid of a specific pull-ingest command(ActivityType==DN.AdminCommand.DataIngestPullCommand)>
```

#### Cluster resource saturation during ingestion

```kusto
PerfCounterCPU
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize avg_cpu = avg(CounterValue) by bin(Timestamp, 1h)
| join kind=inner (
    DataIngest
    | where Source == toupper('<cluster name>')
    | where Timestamp > ago(7d)
    | summarize IngestedGB = round(sum(OriginalSize) / pow(1024,3), 2) by bin(Timestamp, 1h)
) on Timestamp
| project Timestamp, avg_cpu, IngestedGB
| order by Timestamp asc
```

---

### Query / Performance

#### Query latency percentiles

```kusto
QueryCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize percentiles(Duration, 10, 50, 90, 95, 99) by bin(Timestamp, 1h)
| order by Timestamp asc
```

#### Queries completed vs. cancelled vs. failed

```kusto
QueryCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize Total = count(), Failed = countif(State == 'Failed'),
    Cancelled = countif(State == 'Cancelled'), Throttled = countif(State == 'Throttled')
  by bin(Timestamp, 1d)
| order by Timestamp asc
```

#### Slow queries — top by duration
----
```kusto
QueryCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| where State == 'Completed'
| top 20 by Duration desc
| project Timestamp, Duration, TotalCPU, Application, User, DatabaseName
```


#### Cache hit ratio (hot vs. cold data access)

```kusto
QueryCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| extend ScannedExtentsStatistics = todynamic(ScannedExtentsStatistics)
| extend HotExtents = tolong(ScannedExtentsStatistics.HotExtentsCount),
         ColdExtents = tolong(ScannedExtentsStatistics.ColdExtentsCount)
| where HotExtents + ColdExtents > 0
| summarize AvgHotRatio = round(100.0 * avg(HotExtents * 1.0 / (HotExtents + ColdExtents)), 1) by bin(Timestamp, 1d)
| order by Timestamp asc
```

#### Query distribution across databases

```kusto
QueryCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize count() by DatabaseName
| order by count_ desc
```

---

### Resource / Capacity

#### CPU / memory utilization trends

```kusto
// CPU trend
PerfCounterCPU
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize avg_cpu = avg(CounterValue), max_cpu = max(CounterValue) by bin(Timestamp, 1h)
| order by Timestamp asc
| render timechart
```

```kusto
// Memory available trend
PerfCounterMemoryAvailable()
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize avg_mem = avg(CounterValue) by bin(Timestamp, 1h)
| order by Timestamp asc
| render timechart
```

#### Hot Disk Usage & Data Capacity Factor

```kusto
// ⚠️ NOT CORRECT: DimCapacityMetrics does not exist in Kuskus. Use ClusterDataCapacity() or KustoMdmMetricsV1() instead.
// DimCapacityMetrics
// | where Cluster == toupper('<cluster name>')
// | where Timestamp > ago(7d)
// | summarize avg(HotDiskUsage), avg(DataCapacityFactor) by bin(Timestamp, 1d)
// | order by Timestamp desc
ClusterDataCapacity()
| where Source == toupper('<cluster name>')
```

#### Autoscale behavior and timing

```kusto
// Why we scale or don't scale
WhyWeScaleOutCluster(toupper('<cluster name>'), 7d)
```

```kusto
WhyWeDontScaleOutCluster(toupper('<cluster name>'), 7d)
```

```kusto
WhyWeScaleInCluster(toupper('<cluster name>'), 7d)
```

```kusto
WhyWeDontScaleInCluster(toupper('<cluster name>'), 7d)
```

#### Throttling — concurrent query capacity

```kusto
QueryCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| where FailureReason contains "aborted due to throttling"
| extend Capacity = extract(@"Capacity:\s*(\d+)", 1, FailureReason)
| summarize count() by bin(Timestamp, 1h), Capacity
```
#### Calculate query concurrency in a cluster at a certain period
```kusto
let Start=ago(1d);
let End=now();
let Granularity=10m;
let Cluster = toupper('<cluster name>');
let StartQueries=QueryCompletion
| where Source == Cluster
| where Timestamp between (Start .. End)
| where Timestamp > Start
| extend Timestamp = Timestamp - Duration // query start point
| extend StartEnd=1 // Start indication
| project Timestamp, StartEnd
;
let EndQueries=QueryCompletion
| where Source == Cluster
| where Timestamp between (Start .. End)
| extend StartQuery=Timestamp - Duration
| where StartQuery > Start
| extend StartEnd=-1 // End indication
| project Timestamp, StartEnd
;
union StartQueries, EndQueries
| order by Timestamp asc
| extend Concurrent =row_cumsum(StartEnd)
| summarize max(Concurrent) by bin(Timestamp,Granularity)
```

#### Throttling — Fabric capacity (Fabric clusters only)

```kusto
QueryCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| where FailureReason contains "Fabric compute capacity has exceeded its limits"
| summarize count() by bin(Timestamp, 1h)
```

---

### Workload / Usage Patterns

#### Workload distribution (ingestion vs query)

```kusto
CommandCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize count() by ActivityType
| order by count_ desc
| take 12
```

#### CPU breakdown by workload type (query vs ingest vs materialized views vs other)

```kusto
// Kuskus-based CPU breakdown by workload type (query vs ingest vs materialized views vs other)
// Kuskus splits telemetry across QueryCompletion (user queries) and CommandCompletion (admin commands).
// Both TotalCPU and TotalCpuMs are already timespan-typed (TotalCpuMs is misleadingly named — it is
// not a scalar count of milliseconds), so no unit conversion is needed; use both directly.
let cluster = toupper('<cluster name>');
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
| render timechart
```

> `OtherCores` here is leftover `CommandCompletion` activity (e.g. schema/purge/export commands) not
> matched by Ingest/Materialize — kuskus has no equivalent of the `ClientActivityId` MV-materialization
> signal available in `.show commands-and-queries`, so all `QueryCompletion` rows count as `Query`.



```kusto
QueryCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| summarize QueryCount = count() by HourOfDay = hourofday(Timestamp), DayOfWeek = dayofweek(Timestamp)
| order by DayOfWeek asc, HourOfDay asc
```

#### Heavy queries / long-running jobs

```kusto
QueryCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| where TotalCPU > 1m
| summarize count(), avg_duration = avg(Duration / 1s), avg_cpu = avg(TotalCPU / 1s)
  by Application = substring(Application, 0, 60)
| order by count_ desc
| take 10
```

---

### Update Policies

#### Update policy execution failures

```kusto
CommandCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| where ActivityType has "UpdatePolicy"
| where State == 'Failed'
| summarize count() by bin(Timestamp, 1h), FailureReason = substring(FailureReason, 0, 150)
| order by Timestamp asc
```

#### Update policy resource consumption (with p99 duration)

```kusto
CommandCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| where ActivityType has "UpdatePolicy"
| summarize Total = count(), Failed = countif(State == 'Failed'),
    avg_cpu_ms = avg(TotalCpuMs), avg_duration_sec = avg(Duration / 1s),
    p99_duration_sec = percentile(Duration / 1s, 99)
  by bin(Timestamp, 1h)
| order by Timestamp asc
```

#### Ingestion into source table — gaps & batching behavior

```kusto
DataIngest
| where Source == toupper('<cluster name>')
| where Timestamp > ago(1d)
| where DatabaseName == '<database name>'
| where TableName == '<source table name>'
| summarize IngestOps = count(), TotalRows = sum(RowCount), AvgBatchSizeMB = round(avg(OriginalSize) / 1048576.0, 2)
  by bin(Timestamp, 5m)
| order by Timestamp asc
```

#### Ingestion batching & update policy Memento changes

```kusto
Memento()
| where Source == toupper('<cluster name>')
| where Event has 'BATCHING' or Event has 'INGESTION' or Event has 'UPDATE-POLICY'
| project Timestamp, Event, ChangeCommand
| order by Timestamp desc
| take 20
```

#### Throttling blocking update policy execution

```kusto
QueryCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| where FailureReason contains "aborted due to throttling"
| summarize count() by bin(Timestamp, 1h)
```

#### Update policy execution gaps (detect missed triggers)

```kusto
CommandCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(1d)
| where ActivityType has "UpdatePolicy"
| where CommandText has '<target table name>' or CommandText has '<database name>'
| project Timestamp, State, Duration, TotalCpuMs
| order by Timestamp asc
| extend GapMinutes = round((Timestamp - prev(Timestamp)) / 1m, 1)
```

#### CPU pressure during update policy windows

```kusto
PerfCounterCPU
| where Source == toupper('<cluster name>')
| where Timestamp > ago(1d)
| summarize avg_cpu = avg(CounterValue) by bin(Timestamp, 5m)
| order by Timestamp asc
| render timechart
```

---

### Materialized Views (MV)

#### MV refresh latency / lag — using built-in function

```kusto
MaterializedViewsAgeMetric(ago(7d), now())
| where Source == toupper('<cluster name>')
```

#### MV errors

```kusto
MaterializedViewsErrors(ago(7d), now(), toupper('<cluster name>'))
```

#### MV monitoring overview

```kusto
MaterializedViewsMonitoring(ago(7d), now())
| where Source == toupper('<cluster name>')
```

#### MV command completion stats

```kusto
CommandCompletion
| where Source == toupper('<cluster name>')
| where Timestamp > ago(7d)
| where ActivityType has "MaterializedView"
| summarize Total = count(), Failed = countif(State == 'Failed'), avg_cpu_ms = avg(TotalCpuMs)
  by ActivityType, bin(Timestamp, 1d)
| order by Timestamp asc
```

---

## Policy Checks (Always verify before concluding root cause)

### All policy changes for a cluster

```kusto
Memento()
| where Source == toupper('<cluster name>')
| where Event has 'POLICY' or Event has 'WORKLOAD'
| project Timestamp, Event, ChangeCommand
| order by Timestamp asc
```

### Weak consistency policy

```kusto
Memento()
| where Source == toupper('<cluster name>')
| where Event has 'WEAK-CONSISTENCY'
| project Timestamp, Event, ChangeCommand
| order by Timestamp desc
| take 5
```

### Merge policy changes

```kusto
Memento()
| where Source == toupper('<cluster name>')
| where Event has 'MERGE-POLICY'
| project Timestamp, Event, ChangeCommand
| order by Timestamp desc
| take 5
```

## Materialized Views

### Check for the MV definition (MV creation command)
```
//see definition of MV / merge policy / lookback / backfill by move extents?
let entities = dynamic(["<MV name>", "<source table name>"]);
Memento
| where Timestamp > ago(300d)
| where Source == "<cluster name>"
| where EntityName in (entities)// or Event has "POLICY"
or UpdatedEntityName in (entities)
```

### Check the MV runs while processing the increments
```
MaterializedViewsDurations(ago(2d), now())
| where Source == "<cluster name>"

```

---

## Useful Built-in Functions Reference

| Function | Purpose |
|---|---|
| `AdminCPU('<cluster>', 7d)` | CPU of admin node over time |
| `AdminHistory('<cluster>', 14d)` | History of admin node elections |
| `ClusterDiagnostics('<cluster>', since, period)` | Full automated diagnostics |
| `PerNodeQueryStats('<cluster>', 7d)` | Per-node query statistics |
| `TopQueriesByCPU(10, '<cluster>', start, end)` | Top queries by CPU consumption |
| `TopQueriesByMemory(10, '<cluster>', start, end)` | Top queries by memory consumption |
| `TopUsersByCPU(10, '<cluster>', start, end)` | Top users by CPU |
| `TopUsersByMemory(10, '<cluster>', start, end)` | Top users by memory |
| `MemIntensiveQueries(10, '<cluster>', start, end)` | Memory-intensive queries |
| `ThrottlingonKustoCluster('<cluster>', start, end)` | Throttling events |
| `WhyWeScaleOutCluster('<cluster>', 7d)` | Why autoscale scaled out |
| `WhyWeDontScaleOutCluster('<cluster>', 7d)` | Why autoscale didn't scale out |
| `WhyWeScaleInCluster('<cluster>', 7d)` | Why autoscale scaled in |
| `WhyWeDontScaleInCluster('<cluster>', 7d)` | Why autoscale didn't scale in |
| `MaterializedViewsAgeMetric(start, end)` | MV age/lag metric |
| `MaterializedViewsErrors(start, end, source)` | MV errors |
| `MaterializedViewsMonitoring(start, end)` | MV health overview |
| `GetClusterOwners('<cluster>')` | Cluster ownership info |
| `FeatureFlagsInCluster('<cluster>')` | Feature flags enabled on cluster |
