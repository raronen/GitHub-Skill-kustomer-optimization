# Cluster Alerts — Investigation Guide

The `Alerts()` function on Kuskus exposes engine-emitted diagnostic **alerts** (a.k.a. "reasons")
for every cluster. There are **hundreds of distinct `Reason` values**. Most are low-value noise
(query-plan annotations, distribution hints), but a meaningful subset reveals **real reliability,
data-correctness, security, and capacity problems** that are otherwise invisible in
`QueryCompletion` / `CommandCompletion` because the operation did **not** fail.

> **Why alerts matter:** Many of the highest-impact issues are *silent*. The clearest example is an
> update policy that references additional tables (a join) on a table with **streaming ingestion**
> enabled — every streaming flush is dropped from the target table, but because the update policy is
> **non-transactional** the ingestion command still reports success. There is **no failure** in
> `CommandCompletion`; the only evidence is hundreds of thousands of `Alerts()` rows.

Use this folder as a lookup catalog during any cluster investigation. See
[`alert-reasons-catalog.md`](alert-reasons-catalog.md) for the categorized reason reference.

---

## `Alerts()` schema

| Column | Type | Notes |
|---|---|---|
| `Source` | string | Cluster name (UPPERCASE). For Fabric Eventhouses use the same `Source`/`SourceQualified` rule as elsewhere. |
| `Timestamp` | datetime | When the alert fired. |
| `Machine` | string | Emitting node. |
| `Level` | string | `Information` / `Warning` / `Error` / `Critical`. |
| `ClientActivityId` | string | Correlate with `QueryCompletion`/`CommandCompletion`. |
| `RootActivityId` | string | Correlate across the operation tree. |
| `Reason` | string | The alert category (the key field — hundreds of values). |
| `Message` | string | Human-readable detail, usually naming the **table** and the offending query/condition. |

`Alerts` is a shortcut; `Alerts()` and `Alerts` (bare) both work. Related functions:
`TopAlerts(startTime, endTime, source)` (top alerts by source) and
`MaterializedViewsAlerts(startTime, endTime)` (MV-specific health alerts).

---

## Standard investigation workflow

**1. Triage — what is firing on this cluster?** Always start here on any investigation; high alert
volumes frequently point straight at the root cause.

```kusto
Alerts
| where Timestamp > ago(7d)
| where Source == toupper('<cluster>')
| summarize Cnt=count(), FirstSeen=min(Timestamp), LastSeen=max(Timestamp) by Reason, Level
| order by Cnt desc
```

**2. Read the message** for any high-count or `Error`/`Critical` reason — the message names the table
and the cause:

```kusto
Alerts
| where Timestamp > ago(7d)
| where Source == toupper('<cluster>')
| where Reason == '<Reason>'
| summarize Cnt=count() by Msg=substring(Message, 0, 320)
| order by Cnt desc
| take 10
```

**3. Trend it** to see whether it is chronic, a recent regression, or a one-off burst:

```kusto
Alerts
| where Timestamp > ago(14d)
| where Source == toupper('<cluster>')
| where Reason == '<Reason>'
| summarize Cnt=count() by bin(Timestamp, 1d)
| order by Timestamp asc
```

**4. Correlate** with the operation via `ClientActivityId` / `RootActivityId` into
`QueryCompletion`, `CommandCompletion`, or `DataOperations`.

---

## Severity interpretation

- **`Critical`** — act immediately (e.g. `MemoryProfileTrigger_Results`, native crashes).
- **`Error`** — real failure or data-correctness risk. Investigate even if `CommandCompletion`
  shows success — non-transactional paths swallow these.
- **`Warning`** — often benign at low volume, but **high or rising counts** of certain warnings
  (schema mismatch, mapping not found, retention undefined, throttling) indicate a real problem.
- **`Information`** — almost always noise (`Splay`, `Broadcast`, implicit mapping). Ignore unless
  cross-referenced.

> **Volume is contextual.** Fleet-wide, the noisiest reasons reach billions/day across hundreds of
> thousands of clusters. What matters is the count **on the one cluster you are investigating** and
> the `Level`. A few hundred `Error` alerts on a single small cluster can be far more significant
> than millions of `Information` alerts fleet-wide.

---

## ⚠️ Highest-value pattern: silent update-policy data loss

The `ProcessSingleDataUpdate*` family (see catalog) fires when an update policy **cannot process the
streaming-ingested (rowstore) portion** of data. With a **non-transactional** update policy
(`IsTransactional:false` — the recommended default for non-blocking ingestion), the failed rows are
**dropped from the target table while the ingestion command still succeeds**. This produces:

- **Hundreds of thousands of `Error`/`Warning` alerts** on the cluster, and
- **A silently incomplete target table** (no error anywhere in `CommandCompletion`).

Two common triggers, both verified against live clusters:

| Reason | Trigger | Message signature |
|---|---|---|
| `ProcessSingleDataUpdateFailedDueToUsingAdditionalTables` (Error) | UP query **joins / references another table** while streaming ingestion is enabled on the source (directly or via the UP chain). | *"Referencing additional tables from update policy is not allowed when streaming ingestion is enabled on the source table … Disable streaming"* |
| `ProcessSingleDataUpdateDueToQuerySchemaDoesNotMatchTableSchema` (Warning) | UP query **output schema ≠ target table schema** on the streaming path. | *"Query schema does not match table schema, UP query: '…'"* |

**Fixes:** (a) remove the additional-table reference / move the join out of the per-batch update
policy (use a **materialized view** or **scheduled batch** instead), or (b) disable **streaming
ingestion** on the source table(s) in the chain, or (c) fix the UP query so its output schema
matches the target. Option (a) is usually best — it also removes the per-batch cost of the join.

A real example of this pattern is documented in
`Investigations/2026-06/2026-06-22-JetBlue-TRD-VSW1CRNAD6GCKFCMKH-update-policy-cpu-report.md`
(JetBlue `gold_manifestbyflight`: ~420K `Error` alerts in 7 days, zero ingestion-command failures).
