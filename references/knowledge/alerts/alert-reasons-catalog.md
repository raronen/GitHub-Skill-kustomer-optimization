# Alert Reasons Catalog

A curated reference of `Alerts()` `Reason` values worth checking during an investigation, grouped by
category. The fleet has **hundreds** of reasons; this catalog focuses on the ones that are
**actionable** on a single cluster.

**Legend**
- **Level** — the `Level` observed for this reason (`Information`/`Warning`/`Error`/`Critical`).
- **✔ verified** — the message text was confirmed against a live cluster during an investigation.
  Un-marked rows are documented from the reason name, observed `Level`, and engine domain knowledge;
  always read the live `Message` before drawing conclusions.

> Reasons not listed here are usually query-plan/diagnostic noise (`Splay`, `Broadcast`,
> `ConstantSubtree`, `QueryPlanFarthestLeaf`, `TranslateCslToRelop`, `RelopToCsl`,
> `VisitCslDistinctOperatorRenames`, `DataReaderConverter_WriteJson`, `LeakDetection.*`, etc.).
> They can reach billions of rows fleet-wide and are rarely relevant to a customer complaint.

---

## 1. Update policies & streaming ingestion (data correctness) — **highest value**

These fire when an update policy (UP) cannot process the streaming-ingested (rowstore) data. With a
**non-transactional** UP the rows are **silently dropped from the target table** while the ingestion
command still succeeds — so the *only* signal is `Alerts()`. See the README for the full pattern.

| Reason | Level | Meaning & investigative action |
|---|---|---|
| `ProcessSingleDataUpdateFailedDueToUsingAdditionalTables` | Error | ✔ verified. UP query **references additional tables (a join / lookup)** while **streaming ingestion** is enabled on the source (directly or via the UP chain). Streaming rows are **not** written to the target. → Move the join out of the per-batch UP (materialized view / scheduled batch), or disable streaming on the source. Check target-table completeness. |
| `ProcessSingleDataUpdateDueToQuerySchemaDoesNotMatchTableSchema` / `UpdatePolicy.ProcessSingleDataUpdateDueToQuerySchemaDoesNotMatchTableSchema` | Warning | ✔ verified. UP query **output schema ≠ target table schema** on the streaming path (e.g. a `project-away` that drops a column the target still has). Streaming rows dropped. → Align the UP query output to the target schema. |
| `ProcessSingleDataUpdate` | Warning | Generic single-data-update (streaming) processing note from the UP engine. High counts → inspect the message and the surrounding UP reasons above. |
| `UnexpectedExceptionInSIUpdatePolicy` | Error | An unhandled exception in a **streaming-ingestion** update policy. → Read message; usually a bug in the UP query against streaming data. |
| `RunningUpdatePolicyFromRestrictedViewTableToUnrestricted` | Error | **Security/governance:** a UP copies data **from a RestrictedViewAccess table into a non-restricted table**, bypassing row-level/restricted-view protection. → Flag to the customer; the target leaks restricted data. |

---

## 2. Memory & capacity

| Reason | Level | Meaning & investigative action |
|---|---|---|
| `MemoryProfileTrigger_Results` | Critical | The engine's memory profiler tripped — node under **memory pressure**. Correlate with `PerfCounterMemoryAvailable` and low-memory query failures. Strong "cluster undersized / burst workload" signal. |
| `OutOfMemory` / `E_OUTOFMEMORY` | Error | An operation hit OOM. Pair with `QueryCompletion` `E_LOW_MEMORY_CONDITION` failures and per-node memory to decide between query optimization, workload-group caps, and scale-out. |
| `GrpcServiceConcurrencyRunningHigh` | Warning | Inter-node gRPC concurrency is high → the cluster is saturated / fan-out heavy. Check concurrency limits and node count. |

---

## 3. Reliability & crashes

| Reason | Level | Meaning & investigative action |
|---|---|---|
| `NativeCrash` | Critical | Engine native crash. Always investigate; correlate `Timestamp`/`Machine` with node restarts and query/ingestion failures. (See `queries.md` "Critical alerts".) |
| `FailedToReadDatabaseMetadata` | Critical/Error | The node could not read database metadata — can block queries/commands cluster-wide. |
| `SandboxManagerNotInitialized` | Error | The **Python/R plugin sandbox** is not ready → `python()`/`r()` plugin queries fail. Relevant when the complaint involves inline plugins. |
| `ActivityFailed` | Error | Generic background-activity failure. Read message to identify which activity (purge, merge, export, etc.). |

---

## 4. Ingestion & mapping

| Reason | Level | Meaning & investigative action |
|---|---|---|
| `IngestionFailureWithEmptyIngestionFailures` | Error | Ingestion failed but the failure list came back empty — investigate alongside `IngestionResult`/`CommandCompletion`. |
| `MappingReferenceWasNotFound` | Warning | A named ingestion **mapping referenced does not exist** → rows can be misparsed/dropped. → Verify the mapping name on the table. |
| `UnsupportedJsonPathInDataMapping` | Warning | A JSON path in the mapping is unsupported → columns silently unmapped. → Fix the mapping. |
| `MissingIngestionTimeOnAddedExtent` | Error | An added extent lacks an ingestion-time value → breaks `ingestion_time()`-based logic, retention, and arg_max-by-ingestion dedup. |
| `Ingestion.NoRowStoreShared` | Error | Streaming-ingestion rowstore problem. Relevant to streaming-latency / streaming-failure complaints. |
| `CommittingTimedOutExtent` | Warning | An extent commit timed out (often under load) → ingestion latency. |
| `Ingestion.Parquet.ImplicitlyMappedColumns` | Information | Parquet columns mapped implicitly (no explicit mapping). Usually benign; note if columns are missing. |

---

## 5. Materialized views

| Reason | Level | Meaning & investigative action |
|---|---|---|
| `MVApplyOrderCheck` | Error | An ordering/consistency check failed while applying an MV → possible MV correctness/lag issue. → Cross-check with `MaterializedViewsAlerts()` and the MV investigation guide. |

> For MV health use the dedicated **`MaterializedViewsAlerts(startTime, endTime)`** function and
> `references/knowledge/mv-investigation-guide.md` rather than relying on `Alerts()` alone.

---

## 6. Fabric mirroring (Eventhouse)

| Reason | Level | Meaning & investigative action |
|---|---|---|
| `Mirroring.DeadCode` | Error | Fabric mirroring continuous-export hit a dead-code/abort path. Relevant when the cluster uses Fabric mirroring (often a top CPU consumer on Eventhouses). |
| `UnexpectedFabricMirroringPolicyConnectionString` | Warning | Mirroring policy connection string is malformed/unexpected → mirroring may be misconfigured. |

---

## 7. Throttling & concurrency

| Reason | Level | Meaning & investigative action |
|---|---|---|
| `QueryThrottledByQueryService` | Warning | Queries throttled by the query service (concurrency/capacity). Pair with `QueryCompletion` "aborted due to throttling" and the concurrency-capacity guidance in the skill. |
| `IncomingRequestIsBeingThrottled` | Warning | Inbound requests throttled at the service layer. |
| `NewFromRequestLimitsPolicy` / `KustoGraphSameRequestThrottler` | Warning/Error | Request-limits / same-request throttling policy engaged. |

---

## 8. Policy hygiene & security

| Reason | Level | Meaning & investigative action |
|---|---|---|
| `RetentionPolicyIsNotDefined` / `RetentionPolicyIsNotDefinedOnAllTables` | Warning | Retention not set on some tables → unbounded growth / cost. → Recommend explicit retention. |
| `RLS.IgnoringBlockedRowLevelSecurity` | Warning | Row-level-security enforcement was bypassed for a path. Review if the customer has compliance requirements. |
| `MissingSecureConnectionStrings` / `MissingOriginalAadToken` | Warning | Auth/connection-string hygiene issues; relevant to impersonation/managed-identity setups. |

---

## 9. Data integrity & background maintenance

| Reason | Level | Meaning & investigative action |
|---|---|---|
| `InconsistentMinMaxColumnRange` | Error | An extent's min/max column index is inconsistent → can cause wrong results on range filters / poor pruning. |
| `SchemaManager.AddRemoveExtents` | Warning | Schema-manager churn adding/removing extents (often follows heavy ingestion/merge). High counts → metadata pressure. |
| `DatabasePurgeCleanerFailure` / `PurgeCleanupFailedGetExtentDescription` | Error | **Purge** background cleanup failed → GDPR/purge requests may be incomplete. Investigate if the customer relies on purge. |
| `DelayInStorageArtifactsCleanup` | Information | Storage-artifact cleanup is lagging; usually benign unless storage cost is the concern. |

---

## Quick-start query

```kusto
// One-shot triage: actionable (non-Information) alerts on the cluster, last 7 days
Alerts
| where Timestamp > ago(7d)
| where Source == toupper('<cluster>')
| where Level != 'Information'
| summarize Cnt=count(), LastSeen=max(Timestamp) by Reason, Level
| order by Cnt desc
```
