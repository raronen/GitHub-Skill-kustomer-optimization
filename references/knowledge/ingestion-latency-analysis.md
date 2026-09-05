# Ingestion Latency Analysis

Use this guide when data appears late in queries. Analyze latency only for the main
tables and materialized views used by the affected queries; cluster-wide averages
can hide the table causing stale results.

## Latency model

For each queried data path, report these three components:

| Component | Definition | Primary evidence |
|---|---|---|
| Average time between batches | Time from one ingestion batch arriving for the table to the next batch arriving | Consecutive `DataIngest` timestamps |
| Time to process each batch | Time Kusto spends processing the ingestion batch | `CommandCompletion.Duration` for `DataIngestPullCommand` |
| MV age | Time between data reaching the MV source table and being materialized | `MaterializedViewsMonitoring.Age`; use `0` or `N/A` when the query does not use an MV |

The estimated average end-to-end freshness is:

```text
average batch interval + average batch processing time + average MV age
```

Also calculate p95 or maximum values. An average alone hides intermittent latency
spikes. Do not add MV age for a query that reads the source table directly.

## Investigation procedure

1. Resolve the cluster's `Source` and regional Kuskus as required by `SKILL.md`.
2. Obtain the affected query or `ClientActivityId`. Identify the database and the
   main tables or MVs that determine the query's freshest data. Prioritize objects
   that dominate query volume, CPU, or scanned data; do not analyze every lookup
   or small dimension table.
3. If a queried object is an MV, record its source table. Analyze batching and
   batch processing on the source table, then analyze age on the MV.
4. Use the same incident time range for all three components. Default to seven
   days when no period is supplied.
5. Calculate the components per database and table/MV. Never combine unrelated
   tables into one cluster average.
6. Correlate spikes with ingestion volume, failures, CPU, scaling, and policy
   changes only after the three-component table identifies the dominant stage.

## 1. Average time between batches

Run on Kuskus. Replace `Source` with the qualified source when applicable.

```kusto
let Start = ago(7d);
let End = now();
DataIngest
| where Source == toupper('<qualified source>')
| where Timestamp between (Start .. End)
| where DatabaseName == '<database>'
| where TableName == '<source table>'
| order by Timestamp asc
| serialize
| extend PreviousBatch = prev(Timestamp)
| extend BatchInterval = Timestamp - PreviousBatch
| where isnotnull(PreviousBatch)
| summarize
    AverageBatchInterval = avg(BatchInterval),
    P95BatchInterval = percentile(BatchInterval, 95),
    MaximumBatchInterval = max(BatchInterval),
    BatchCount = count()
```

Interpret the interval in context:

- A stable long interval usually reflects the configured batching policy or a
  low-volume source.
- Irregular long gaps can be source-side delays, queueing, throttling, failures,
  or insufficient traffic to seal a batch.
- Check Memento for ingestion batching policy changes before concluding that a
  system regression caused the interval.

## 2. Time to process each batch

Use completed pull-ingestion commands for the same source table and time range.

```kusto
let Start = ago(7d);
let End = now();
CommandCompletion
| where Source == toupper('<qualified source>')
| where Timestamp between (Start .. End)
| where ActivityType == 'DN.AdminCommand.DataIngestPullCommand'
| where DatabaseName == '<database>'
| where TableName == '<source table>'
| summarize
    AverageBatchProcessingTime = avg(Duration),
    P95BatchProcessingTime = percentile(Duration, 95),
    MaximumBatchProcessingTime = max(Duration),
    FailedBatches = countif(State != 'Completed'),
    BatchCount = count()
```

If table identity is absent from these command rows, correlate
`CommandCompletion.ClientActivityId` with `DataIngest` or `DataOperations` and
retain only operations for the selected table. Do not substitute a cluster-wide
command duration.

High processing time can come from large batches, update policies, parsing,
extent commit pressure, throttling, or insufficient capacity. Compare duration
with batch size and CPU, and inspect failures using canonical failure-reason
buckets rather than raw failure strings.

## 3. MV age

Run this only for MVs used by the affected queries:

```kusto
let Start = ago(7d);
let End = now();
MaterializedViewsMonitoring(Start, End)
| where Source == toupper('<qualified source>')
| where DatabaseName == '<database>'
| where MaterializedViewName == '<materialized view>'
| summarize
    AverageMvAge = avg(Age),
    P95MvAge = percentile(Age, 95),
    MaximumMvAge = max(Age),
    MaximumDeltaCount = max(DeltaCount)
```

An old `Age` with `DeltaCount == 0` means the source is idle and the MV has no
unmaterialized data; it is not active MV lag. Report active MV latency only when
there is a nonzero delta. Use the exact column names returned by
`MaterializedViewsMonitoring()` if its deployed schema differs.

## Required result table

Produce one row per main queried table or MV. The three latency components must
remain separate so the dominant contributor is visible.

| Database | Queried table or MV | Ingestion source table | Avg time between batches | Avg batch processing time | Avg MV age | Dominant component |
|---|---|---|---:|---:|---:|---|
| `<db>` | `<table or MV>` | `<source table>` | `<duration>` | `<duration>` | `<duration or N/A>` | `<batching / processing / MV>` |

After the table, include p95 values and explain which component controls observed
freshness. State whether the numbers cover the requested incident period or only
the available telemetry window; engine telemetry is retained for only about 30
days.

