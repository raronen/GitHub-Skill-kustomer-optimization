# Bucketing `FailureReason` (and similar free-text error fields)

## Why this exists
`FailureReason` in `QueryCompletion` / `CommandCompletion` (and similar free-text fields such as
`Alerts.Message`) frequently embeds **variable content** — GUIDs, shard IDs, blob storage URLs,
extent IDs, principal IDs — inside the **first part** of the string. Grouping directly with
`summarize count() by FailureReason` treats every variant as a distinct row, which **fragments a
single real root cause into hundreds or thousands of near-unique rows**, each with a low count.
This can hide the true top failure category entirely from a `top N` view.

**Real example (CSADATAPOOL investigation, 2026-07-07):** grouping raw `FailureReason` showed only
`"PartialQueryEvaluator: Query timed out..." — count 4` and similar tiny counts near the bottom of
the list. Bucketing revealed **1,008** `PartialQueryEvaluator` failures, of which **1,003** were the
exact same root cause (HTTP 503 from Azure Blob Storage, error `0x80004005`) — the single largest
failure category on the cluster, invisible under raw grouping because each message embedded a
different shard ID / container name / blob URL.

## The technique
1. Take only the **first 1000 characters** of the reason string — `substring(FailureReason, 0, 1000)`.
   This is enough to contain the fixed "signature" text of virtually every known failure pattern while
   keeping `has`/`contains` matching cheap (avoids scanning arbitrarily long embedded query text or
   stack traces further into the string).
2. Classify that substring into a **fixed set of ≤15 canonical buckets** using a `case()` expression,
   ordered from most-specific to catch-all. Add new patterns to the `case()` as new signatures are
   discovered — do not let the bucket count exceed ~15 or it stops being a useful triage view.
3. Always run the bucketed summary **first**, before ever looking at raw `FailureReason` grouping.
   Only drill into raw `FailureReason` / full message text for a single bucket once it's identified as
   high-count or high-impact.

## Reusable let-statement
```kusto
let BucketFailureReason = (reason: string) {
    let r = substring(reason, 0, 1000);
    case(
        r has "Fabric compute capacity has exceeded",           "Fabric Capacity Throttling",
        r has "aborted due to throttling",                      "Concurrency Throttling",
        r has "Client disconnected" or r has "connection has been cut", "Client Disconnected/Timeout",
        r has "Query timed out",                                "Query Timed Out (server)",
        r has "E_QUERY_CANCELLED" or r has "Query cancelled",   "Query Cancelled",
        r has "not authorized",                                 "Authorization Denied",
        r has "SEM0100" or r has "Semantic error",              "Semantic Error - Entity/Column Not Found",
        r has "Syntax error" or r has "SYN0",                   "Syntax Error",
        r has "join" and r has "memory budget",                 "Memory Budget Exceeded (Join)",
        r has "Runaway query" or r has "E_RUNAWAY_QUERY",       "Runaway Query (Memory)",
        r has "Low memory condition" or r has "E_LOW_MEMORY_CONDITION", "Low Memory Condition",
        r has "PartialQueryEvaluator" and (r has "503" or r has "Rest(5"), "Storage Transient Error (5xx)",
        r has "DeadlineExceeded" or r has "ExecuteRemoteSubQuery", "Remote SubQuery/gRPC Failure",
        r has "PartialQueryEvaluator",                          "Other Partial Query Failure",
        isempty(r),                                             "No Failure Reason",
        "Other/Uncategorized"
    )
};
```
(15 branches total, including the catch-all — keep it at or under this limit.)

## Standard usage — run this instead of raw `summarize count() by FailureReason`
```kusto
let BucketFailureReason = (reason: string) { ... };  // paste definition above
QueryCompletion
| where Source == toupper('<cluster>')
| where Timestamp > ago(7d)
| where State != 'Completed'
// optionally scope to a client, e.g. Power BI: | where ClientActivityId startswith 'kpbi'
| extend Bucket = BucketFailureReason(FailureReason)
| summarize Count = count(), Sample = any(substring(FailureReason, 0, 300)) by Bucket
| order by Count desc
```

Then, for any high-count bucket, drill in further (e.g. by `DatabaseName`, hourly/daily trend, or
extracting structured fields like storage account name / HTTP code) exactly as you would for a single
`FailureReason` value — see the storage-throttling extraction pattern used in the CSADATAPOOL report:
```kusto
| extend HttpCode = extract(@'Rest\((\d+)', 1, FailureReason)
| extend ErrCode  = extract(@'\((0x[0-9a-fA-F]+)\)', 1, FailureReason)
```

## When to use this
- Any time you run `summarize count() by FailureReason` (or `by Reason` on `Alerts`) as part of a
  cluster/tenant investigation — use the bucketed version first.
- Especially important when the raw top-N list looks like "many small failure reasons, no dominant
  cause" — that pattern is a strong signal that fragmentation is hiding a real dominant bucket.
- Applies equally to `CommandCompletion.FailureReason` and other free-text diagnostic fields.

## Related
- `alerts/alert-reasons-catalog.md` — a similar categorization already exists for `Alerts.Reason`,
  which is a discrete enum rather than free text, so it doesn't need bucketing by substring — use it
  as-is.
- Real-world writeup: `Investigations/2026-07/2026-07-07-Microsoft-CSADATAPOOL-powerbi-query-errors-report.md`
