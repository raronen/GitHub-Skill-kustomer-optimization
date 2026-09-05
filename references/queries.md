
## Part A: Diagnosing a Cluster

Follow these steps in order when investigating a cluster. Each step builds on the previous one to form a complete picture.

---

### Step 1: Get the Cluster Configuration

Start by understanding what you're looking at — SKU, node count, region, and customer type.

```kql
DimClustersMv
| where Source == toupper('<cluster name>')
| top 1 by LastUpdated desc
| project Source, MachineSKU, MachineCount, Kind, Region, CustomerType
```

**What to look for:** Note the SKU (determines cores/node) and node count — you'll need these for later thresholds (e.g., a Standard_L32as_v3 has 32 cores).

---

### Step 2: Check if Multi-Admin and Weak Consistency Are Enabled

> ⚠️ `DimClustersMv.IsMultiAdmin` is NOT reliable. Use the query below instead.

```kql
KustoMdmMetricsV1
| where TIMESTAMP > ago(1d)
| where Cluster == toupper('<cluster name>')
| where metricName == "ActiveServiceInstances"
| where dimensionNameList == "Cluster^DataCenter^DeploymentRing^RoleInstance^ServiceType"
| parse dimensionValueList with * "^fabric://" ServiceType:string "/"
| where ServiceType in ("engine.weakconsistencyquery.svc", "engine.databaseadmin.svc")
| summarize dcount(RoleInstance), make_set(RoleInstance) by bin(TIMESTAMP, 10m), ServiceType
```

**How to interpret:**
- `engine.databaseadmin.svc` with **>1 instance** → multi-admin cluster
- `engine.weakconsistencyquery.svc` present → weak consistency enabled (count = number of WC nodes)
- Only `engine.databaseadmin.svc` with 1 instance → single admin, no WC

If weak consistency is enabled, check its usage:

> ⚠️ Empty `queryconsistency` = **strong consistency (legacy default)**, NOT weak.

```kql
QueryCompletion
| where Timestamp > ago(1d)
| where Source == toupper('<cluster name>')
| where Api == "Query"
| extend wc = tostring(ClientRequestProperties['Options']['queryconsistency'])
| summarize count() by wc
```

---

### Step 3: Review Scale History (Node/SKU Changes)

Look for instability in cluster sizing over the past 30 days.

```kql
DimClusters
| where Cluster == toupper('<cluster name>')
| where LastUpdated > ago(30d)
| order by LastUpdated asc
| where MachineCount != prev(MachineCount) or MachineSKU != prev(MachineSKU)
| project Timestamp=LastUpdated, MachineCount, MachineSKU
```

To understand autoscale decisions, use these built-in functions:
- `WhyWeDontScaleInCluster`
- `WhyWeDontScaleOutCluster`
- `WhyWeScaleInCluster`
- `WhyWeScaleOutCluster`

**🔴 Red flags:** Frequent SKU changes (>3/week) — customer is panicking, each change restarts the cluster. Node count dropping to minimum overnight with high disk usage — storage capacity risk.

**✅ Healthy signs:** Stable node count and SKU over weeks. Single admin for small clusters, multi-admin for large ones (>100 nodes).

---

### Step 4: Check the Error Timeline and Classification

Get a timeline of errors, then classify them by pattern.

**Error timeline:**
```kql
KustoLogs
| where Timestamp between (datetime(<BASELINE_START>) .. datetime(<RECOVERY_TIME>))
| where Source == "<CLUSTER>"
| where Level in ("Error", "Critical")
| summarize ErrorCount=count() by bin(Timestamp, 15m)
| order by Timestamp asc
```

**Error classification:**
```kql
KustoLogs
| where Timestamp between (datetime(<START>) .. datetime(<END>))
| where Source == "<CLUSTER>"
| where Level in ("Error", "Critical")
| extend ErrorPattern = case(
    EventText contains "Timeout", "Timeout",
    EventText contains "Connection", "Connection",
    EventText contains "RangeOutOfBounds", "RangeOutOfBounds",
    EventText contains "OutOfMemory", "OutOfMemory",
    EventText contains "Rust panic", "RustPanic",
    EventText contains "Cache", "Cache",
    EventText contains "Fabric", "Fabric",
    "Other")
| summarize count() by ErrorPattern
| order by count_ desc
```

**Critical alerts (crashes and metadata failures):**

> See `knowledge/alerts/` for the full `Alerts()` investigation guide and a categorized reason
> catalog. High-volume `Error`/`Warning` alerts often reveal **silent** issues (e.g. update-policy
> data loss on streaming sources) that never surface as command failures.

```kql
Alerts
| where Timestamp between(datetime(<START>) .. datetime(<END>))
| where Source =~ "<CLUSTER>"
| where Level in ("Critical")
| where Reason has "NativeCrash" or Reason has "FailedToReadDatabaseMetadata"
| summarize count(), min(Timestamp), max(Timestamp) by substring(Message, 0, 60)
```

---

### Step 5: Assess Query Health (7-Day Summary)

Check the overall query success rate, failure/cancellation/throttling trends.

```kql
QueryCompletion
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| summarize Total=count(), Failed=countif(State == 'Failed'),
    Cancelled=countif(State == 'Cancelled'), Throttled=countif(State == 'Throttled')
  by bin(Timestamp, 1d)
| order by Timestamp asc
```

**How to interpret:**
- Failure rate <0.5% → healthy
- Failure rate >1% → investigate further (go to Step 5b)
- Throttled >0 → concurrency limit hit — check if default (10 × cores) was changed
- Look for trends — is the failure rate growing day over day?

**🔴 Red flags:** Failure rate >2% sustained. Throttled queries appearing. Cancellations >5%.

**✅ Healthy signs:** Failure rate <0.5%, zero throttled, cancellations <1%, no worsening trend.

---

### Step 5a: Categorize Cancelled Queries

If cancellations are significant, determine if they're timeouts, user cancellations, or cross-cluster aborts.

```kql
QueryCompletion
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| where State == 'Cancelled'
| summarize count() by Reason=substring(FailureReason, 0, 150)
| order by count_ desc
| take 10
```

**How to interpret:**
- **"Query timed out"** — server-side timeout. If >1% of total queries, the cluster is too slow.
- **"Aborted on [remote cluster]"** — cross-cluster cancel by the source. Not this cluster's fault.
- **"Client disconnected"** — client tool closed before query finished. Client-side issue.
- **"Result exceeds 64 MB"** — application should add `| take` or reduce the result set.

---

### Step 5b: Categorize Failed Queries

Separate user code bugs from actual cluster problems.

```kql
QueryCompletion
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| where State == 'Failed'
| summarize count() by Category=case(
    FailureReason has 'SEM0' or FailureReason has 'Semantic error', 'SemanticError_UserBug',
    FailureReason has 'SYN0' or FailureReason has 'Syntax error', 'SyntaxError_UserBug',
    FailureReason has 'memory' or FailureReason has 'E_LOW_MEMORY' or FailureReason has 'E_RUNAWAY_QUERY', 'LowMemory_ClusterProblem',
    FailureReason has 'Partial query failure', 'PartialFailure',
    FailureReason has 'timed', 'Timeout',
    FailureReason has 'Throttl', 'Throttled',
    'Other')
| order by count_ desc
```

**How to interpret:**
- **SemanticError/SyntaxError** — user code bugs. They do NOT indicate cluster problems.
- **LowMemory** — engine ran out of memory. This IS a cluster problem. Check if merges are saturated or cluster is undersized.
- **PartialFailure** — some subqueries failed on specific nodes. Usually transient (gRPC connectivity). If persistent, check node health via CPU analysis (Step 9).
- **Timeout** — queries taking too long. Check CPU (Step 9) and query cost (Step 6).

**🔴 Red flags:** LowMemory >5% of failures. PartialFailure count growing daily. Syntax/semantic errors >50% of failures (broken deployment or schema change).

---

### Step 6: Analyze Query CPU Outliers (p99 vs p50)

Compare p99 CPU to p50 CPU. If the ratio exceeds 60, identify the top consumers.

**Ratio check:**
```kql
QueryCompletion
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| where State == 'Completed'
| summarize p50_cpu=round(percentile(TotalCPU/1s, 50), 2),
    p99_cpu=round(percentile(TotalCPU/1s, 99), 2), count()
  by bin(Timestamp, 1d)
| extend Ratio=round(p99_cpu/p50_cpu, 1)
| order by Timestamp asc
```

**If ratio >60, identify the outlier users:**
```kql
QueryCompletion
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| where State == 'Completed'
| where TotalCPU > 10m
| summarize count(), avg_cpu_sec=round(avg(TotalCPU/1s), 0),
    avg_dur_sec=round(avg(Duration/1s), 1)
  by Application=substring(Application, 0, 60), User=substring(User, 0, 40)
| order by count_ desc
| take 10
```

**How to interpret:**
- Bimodal workloads (monitoring clusters) will always have extreme ratios — this is expected.
- Focus on **who** is running the expensive queries and whether they're legitimate.
- **LogicApps/Automation** queries = scheduled pipelines, usually legitimate.
- **KWE/Explorer** queries = ad-hoc users, may need guidance on query optimization.
- **Service principals** = automated systems, check if they're running inefficient queries.

**🔴 Red flags:** A single user consuming >50% of cluster CPU. Ad-hoc users (KWE/Explorer) in top 3. Queries averaging >1 hour CPU with <10 second duration.

---

### Step 7: Check Query Parallelism (CPU/Duration Ratio)

The ratio of `TotalCPU / Duration` shows how well queries parallelize. With N cores per node, a well-parallelized query should have a ratio of at least N/3.

```kql
QueryCompletion
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| where State == 'Completed'
| summarize avg_ratio=round(avg(TotalCPU/Duration), 1),
    p50_ratio=round(percentile(TotalCPU/Duration, 50), 1),
    p99_ratio=round(percentile(TotalCPU/Duration, 99), 1), count()
  by bin(Timestamp, 1d)
| order by Timestamp asc
```

**How to interpret:**
- p50 ratio 1–5 → normal for lightweight queries (lookups, status checks)
- p90 ratio > cores/3 → healthy parallelism on heavy queries
- p99 ratio > 100 → queries distributed across many nodes (expected for analytical queries)
- All ratios <5 → queries not parallelizing — possible single-node bottleneck or data skew

---

### Step 8: Assess Command Health (7-Day Summary)

Check command success rate and failure trends. Commands include ingestion, merges, MV runs, exports, and admin operations.

```kql
CommandCompletion
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| summarize Total=count(), Failed=countif(State == 'Failed')
  by bin(Timestamp, 1d)
| extend FailureRate=round(100.0*Failed/Total, 2)
| order by Timestamp asc
```

**How to interpret:**
- Failure rate <0.5% → healthy for background operations
- Look for trends — declining rate is good, increasing is a problem
- Total command count gives scale perspective — millions/day is normal for large clusters

**🔴 Red flags:** Failure rate >1% sustained. Failure rate increasing day over day. Total commands dropping significantly.

---

### Step 8a: Understand the Cluster's Workload Mix

See what the cluster is actually doing — ingestion vs merges vs MVs vs exports. In kuskushead, `CommandCompletion` uses `ActivityType` (prefixed with `DN.AdminCommand.`).

```kql
CommandCompletion
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| summarize count() by ActivityType
| order by count_ desc
| take 12
```

**How to interpret:**
- DataIngestPull dominating (>80%) → ingestion-heavy cluster (normal for telemetry)
- ExtentsMerge high count → lots of small extents being compacted. Check if merge capacity is saturated.
- MaterializedView* present → MVs are active. Check health separately.
- DataExportToFile present → exports running. Check failure rate.

---

### Step 8b: Check Command CPU Trends per Activity Type

Look for anomalies — sudden spikes or sustained increases.

> ⚠️ In kuskushead, the column is `TotalCpuMs` (not `TotalCPU`). Despite the name, it is
> `timespan`-typed (not a scalar millisecond count) — divide by `1s` to get seconds, never multiply by `1ms`.

```kql
CommandCompletion
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| where ActivityType in ('DN.AdminCommand.DataIngestPullCommand', 'DN.AdminCommand.ExtentsMergeCommand')
| summarize count(), avg_cpu_sec=round(avg(TotalCpuMs/1s), 1),
    failed=countif(State == 'Failed')
  by ActivityType, bin(Timestamp, 1d)
| order by Timestamp asc, avg_cpu_sec desc
```

**How to interpret:**
- Stable daily CPU across types → healthy
- Merge CPU doubling → merge policy changed or data volume increased
- Ingest CPU stable → consistent ingestion batch sizes
- New activity types appearing (e.g., ExtentsPartition) → someone added partitioning policies

**🔴 Red flags:** Any ActivityType's avg CPU doubling day-over-day. Merge avg CPU >500s. Merge failure rate >1%.

---

### Step 8c: Identify Who Is Running Commands

Distinguish between internal system operations and specific users/service principals.

```kql
CommandCompletion
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| where ActivityType in ('DN.AdminCommand.DataIngestPullCommand', 'DN.AdminCommand.ExtentsMergeCommand')
| summarize count(), failed=countif(State == 'Failed')
  by ActivityType, PrincipalType, User=substring(User, 0, 40)
| order by count_ desc
| take 10
```

**Principal classification guide:**

| Principal Pattern | Type | Meaning |
|---|---|---|
| `KustoServiceBuiltInPrincipal` | Internal system | Merges, rebuilds, extent operations — automatic |
| `KustoTraceIngestClient` | Internal system | Trace/diagnostic data ingestion |
| `AAD app id=...` | Service principal | Application/automation — identify which app via AAD app ID |
| `user@domain.com` | Human user | Interactive queries from a person |

Internal principals dominating (>95%) is normal. Human users in top command runners is unusual — investigate.

---

### Step 8d: Check Command CPU Outliers (p99 vs p50)

Flag any command type with p99/p50 ratio >60.

> ⚠️ In kuskushead, use `TotalCpuMs` (not `TotalCPU`). Despite the name, it is `timespan`-typed
> (not a scalar millisecond count) — divide by `1s` to get seconds, never multiply by `1ms`.

```kql
CommandCompletion
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| where ActivityType in ('DN.AdminCommand.DataIngestPullCommand', 'DN.AdminCommand.ExtentsMergeCommand',
    'DN.AdminCommand.MaterializeViewCommand', 'DN.AdminCommand.MaterializedViewTableAppendCommand')
| summarize count(), p50_cpu=round(percentile(TotalCpuMs/1s, 50), 2),
    p99_cpu=round(percentile(TotalCpuMs/1s, 99), 2)
  by ActivityType
| extend Ratio=round(p99_cpu/p50_cpu, 1)
| order by count_ desc
```

**How to interpret:** Ratio <10 → very uniform (e.g., ingestion). Ratio 10–60 → moderate spread, normal for merges. Ratio >60 → investigate which users/databases are involved.

---

### Step 9: Analyze Historical CPU Utilization

Unlike `.show` commands which give a snapshot, kuskushead provides **historical CPU** via `PerfCounterCPU`. This is the key advantage of kuskushead over customer cluster access.

**Cluster-wide trend:**
```kql
PerfCounterCPU
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| summarize avg_cpu = avg(CounterValue) by bin(Timestamp, 1h), Machine
| summarize HotNodes = countif(avg_cpu > 90), TotalNodes = dcount(Machine),
    AvgClusterCPU = round(avg(avg_cpu), 1) by bin(Timestamp, 2h)
| order by Timestamp asc
```

**Identify hot nodes:**
```kql
PerfCounterCPU
| where Timestamp between(datetime(<start>)..datetime(<end>))
| where Source == toupper('<cluster name>')
| summarize avg_cpu = avg(CounterValue) by Machine
| order by avg_cpu desc
| take 10
```

**Determine what role the hot nodes play:**
```kql
KustoMdmMetricsV1
| where TIMESTAMP between(datetime(<start>)..datetime(<end>))
| where Cluster == toupper('<cluster name>')
| where metricName == 'ActiveServiceInstances'
| where dimensionNameList == 'Cluster^DataCenter^DeploymentRing^RoleInstance^ServiceType'
| where dimensionValueList has '<hot node name>'
| parse dimensionValueList with * '^fabric://' ServiceType:string '/'
| summarize make_set(ServiceType)
  by RoleInstance=extract('(<hot node name>)', 1, dimensionValueList)
| where RoleInstance != ''
```

**How to interpret:**
- Avg CPU >60% → cluster is busy, investigate top consumers
- Hot nodes >50% of fleet → cluster is saturated
- 0 hot nodes but queries failing → problem is NOT CPU (check memory/connectivity)
- Hot node running `extentcreator` → ingestion overload on that node
- Hot node running `databaseadmin.svc` → admin node bottleneck
- Hot node running `weakconsistencyquery.svc` → WC queries overloading that node

---

### Step 10: Check High Memory and High CPU from Logs

**High memory investigation:**
```kql
let _bin = 1h;
KustoLogs
| where Timestamp between (datetime(<START>) .. datetime(<END>))
| where Source =~ '<CLUSTER>'
| where EventText has "per-node"
| extend Stats = parse_json(EventText)
| summarize MemoryPeak=max(tolong(Stats['Per-node stats'].memory['peak_per_node'])) by ActivityType, bin(Timestamp, _bin)
| top 10 by MemoryPeak
```

**High CPU investigation:**
```kql
KustoLogs
| where Timestamp between (datetime(<START>) .. datetime(<END>))
| where Source =~ '<CLUSTER>'
| where EventText has "per-node"
| extend Stats = parse_json(EventText)
| summarize CpuTime=max(tolong(Stats['Per-node stats'].resource_usage.cpu['total_cpu_time'])) by ActivityType, bin(Timestamp, 1h)
| top 10 by CpuTime
```

---

### Step 11: Check Admin Node Stability

```kql
AdminHistory('<cluster name>', 14d)
```

**How to interpret:**
- >1 admin change per day → admin instability — nodes are cycling
- Admin lasting <12 hours → a node is failing and admin is being re-elected
- Stable admin for days → healthy

---

### Step 12: Review Ingestion Volume

```kql
DataIngest
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| summarize IngestedGB=round(sum(OriginalSize)/1073741824.0, 1),
    IngestCount=count() by bin(Timestamp, 4h)
| order by Timestamp asc
```

**How to interpret:** Spikes >3× normal → ingestion surge driving CPU/merge pressure. Steady volume → healthy ingestion pipeline.

---

### Step 13: Look for Policy Changes (Often the Root Cause)

```kql
Memento
| where Source == toupper('<cluster name>')
| where Timestamp > ago(14d)
| where Event has 'PARTITION' or Event has 'MERGE' or Event has 'POLICY'
| summarize count() by Event
| order by count_ desc
```

**How to interpret:**
- Many ALTER-TABLE-DATA-PARTITIONING-POLICY → repartition storm risk
- ALTER-TABLE-EXTENTS-MERGE-POLICY → merge behavior changed
- ALTER-CLUSTER-CAPACITY-POLICY — check frequency: regular intervals = autoscale active, long gaps = autoscale off, frantic bursts = customer manually panicking

---

### Step 14: Check Database Churn

```kql
Memento
| where Source == toupper('<cluster name>')
| where Timestamp > ago(14d)
| where Event == 'ADD-DATABASE'
| summarize db_creates=count() by bin(Timestamp, 1d)
| order by Timestamp asc
```

**How to interpret:** >50 DB creates/day → metadata propagation storms → node instability. 0 per day → stable.

---

### Step 15: Check Control Plane Operations and Usage

**Control plane audit:**
```kql
// Run as management command on cluster's CM URL
.show service <CLUSTER_NAME> audit log
| project-away OperationId, AdditionalParameters, ServiceConfigurationSnapshot, ServiceType
```

**Usage correlation:**
```kql
Usage
| where Timestamp > ago(1d)
| where Source == "<CLUSTER>"
| summarize count() by bin(Timestamp, 1h), Api
```

---

### Step 16: Compile the Overall Health Assessment

Fill in this template with findings from all previous steps:

| Area | Status | Evidence |
|---|---|---|
| Query success rate | ___ | ___% success, ___% failure |
| Throttling | ___ | ___ throttled queries |
| Query CPU outliers | ___ | p99/p50 ratio = ___ |
| Command failure rate | ___ | ___% failure, trend: ___ |
| Merge health | ___ | ___ merge failures, CPU trend: ___ |
| CPU utilization | ___ | Avg ___%, ___ hot nodes |
| Admin stability | ___ | ___ admin changes in 14d |
| Ingestion | ___ | ___ GB/day, ___ spikes |
| Policy changes | ___ | ___ changes in 14d |

**Recommendations checklist — act on any that apply:**

- [ ] If failure rate >1% → investigate error categorization (Step 5b)
- [ ] If throttled >0 → check concurrency limits
- [ ] If CPU outlier ratio >60 → identify top consumers (Step 6)
- [ ] If merge failures >1% → check capacity and merge policy
- [ ] If hot nodes >50% of fleet → cluster needs scale-out
- [ ] If admin changes >1/day → investigate node health
- [ ] If partition policy changes detected → check for repartition storms
- [ ] If DB churn >50/day → metadata pressure risk

---

## Part B: Diagnosing a Customer (Tenant)

Follow these steps when investigating all clusters belonging to a customer/tenant.

---

### Step 1: List All Clusters for the Customer

```kql
cluster("kustoproductfw.westus").database("KustoBilling").KustoFinancials
| where Account contains '<tenant1>'
| where Day > ago(1d)
| parse ResourceIdCustomer with "/subscriptions/" subguid "/resourceGroups/" ResourceGroup "/providers/Microsoft.Kusto/Clusters/" * 
| project Account, Cluster, SubscriptionNameCustomer, ResourceIdCustomer, ResourceGroup, subguid
| summarize arg_max(ingestion_time(), *) by  Account, Cluster
| project Account, Cluster, SubscriptionName = SubscriptionNameCustomer, ResourceGroup, SubscriptionId = subguid
;
```

---

### Step 2: Get Machine Count per Cluster

```kql
let clusters = 
cluster("kustoproductfw.westus").database("KustoBilling").KustoFinancials
| where Account contains '<tenant1>'
| where Day > ago(1d)
| project Account, Cluster
| summarize arg_max(ingestion_time(), *) by  Account, Cluster
| project Account, Cluster=toupper(Cluster)
;
DimClusters
| where Cluster in ((clusters | project Cluster))
| where State !in ('Deleted', 'Stopped') and Kind == 'Engine'
| summarize arg_max(LastUpdated, *) by Cluster
| project Cluster, Region, Environment, MachineCount, LastUpdated, Kind
| sort by MachineCount desc
```

---

### Step 3: Check Total Extents per Cluster

```kql
let clusters = 
cluster("kustoproductfw.westus").database("KustoBilling").KustoFinancials
| where Account contains '<tenant1>'
| where Day > ago(1d)
| project Account, Cluster
| summarize arg_max(ingestion_time(), *) by  Account, Cluster
| project Account, Cluster=toupper(Cluster)
;
KustoMdmMetricsV1
| where TIMESTAMP > ago(6h)
| where metricName == 'ExtentsTotal'
| where Cluster in ((clusters | project Cluster))
| summarize ExtentsTotal = max(sumValue) by Cluster
| lookup kind=inner (clusters) on $left.Cluster == $right.Cluster
| project Cluster, Account, ExtentsTotal
| order by ExtentsTotal desc
```

---

### Step 4: Review Ingestion Volume Over Time (30 Days)

```kql
let clusters = 
cluster("kustoproductfw.westus").database("KustoBilling").KustoFinancials
| where Account contains '<tenant1>'
| where Day > ago(1d)
| project Account, Cluster
| summarize arg_max(ingestion_time(), *) by  Account, Cluster
| project Account, Cluster=toupper(Cluster)
;
DataIngest
| where Timestamp > ago(30d)
| where Source in ((clusters | project Cluster))
| summarize DailyIngestGB=round(sum(OriginalSize)/1073741824.0, 1) by bin(Timestamp, 1d)
| order by Timestamp asc
```

---

### Step 5: Track Machine Count Over Time (30 Days)

```kql
DimClusters
| where TenantName in ('<tenant1>')
| where LastUpdated > ago(30d)
| where State !in ('Deleted', 'Stopped') and Kind == 'Engine'
| summarize sum(MachineCount) by bin(LastUpdated, 1d)
```

---

### Step 6: Calculate Ingested Data per Cluster per Machine

```kql
let clusters = 
    DimClustersMv
    | summarize arg_max(LastUpdated, *) by Source
    | where State !in ('Deleted', 'Stopped') and Kind == 'Engine'
    | where TenantName  == '<tenant1>'
    | summarize nrOfMachines = sum(MachineCount) by bin(LastUpdated, 1d), Source
    | project nrOfMachines, Source;
let ingested =
   DataIngest
   | where Timestamp > ago(1d)
   | where Source in ((clusters | project Source))
   | summarize DailyIngestGB=round(sum(OriginalSize)/1073741824.0, 1) by Source, bin(Timestamp, 1d)
   | project Source, Timestamp, DailyIngestGB;
clusters
| join ingested on $left.Source == $right.Source
| extend IngestedGBPerMachine = round(DailyIngestGB/nrOfMachines, 1);
```

---

### Step 7: Count Databases per Cluster

```kql
let clusters = 
DimClustersMv
| summarize arg_max(LastUpdated, *) by Source
| where State !in ('Deleted', 'Stopped') and Kind == 'Engine'
| where TenantName  == '<tenant1>'
| project Source;
DataOperations
| where Timestamp > ago(1d)
| where Source in ((clusters | project Source))
| summarize by Source, Database
| summarize count() by Source 
```

---

### Step 8: Count Tables per Database per Cluster

```kql
let clusters = 
DimClustersMv
| summarize arg_max(LastUpdated, *) by Source
| where State !in ('Deleted', 'Stopped') and Kind == 'Engine'
| where TenantName  == '<tenant1>'
| project Source;
DataOperations
| where Timestamp > ago(1d)
| where Source in ((clusters | project Source))
| summarize  by Source, Database, Table
| summarize count() by Source, Database
```

---

### Step 9: Analyze Customer Results

After running all queries above, look for:

- Clusters with unusually high ingestion volumes
- Large numbers of extents that could indicate merge issues
- High ratio of ingested data to machine count (overloaded nodes)
- Unusual ratio between number of databases/tables and ingestion volume (misconfiguration or inefficient data organization)
- For any cluster that looks problematic, follow **Part A** (cluster diagnosis) for a deep dive