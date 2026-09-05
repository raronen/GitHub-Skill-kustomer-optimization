# kustomer-optimization — Cluster Investigation Skill

A GitHub Copilot skill for investigating Azure Data Explorer (Kusto) and Fabric Eventhouse
cluster issues — ingestion, query performance, resource/capacity, crashes, failures,
materialized views, and update policies. It runs diagnostic KQL against the **Kuskus**
fleet-monitoring database and produces a structured, copy-pasteable investigation report.

## When to use

Invoke the skill when you have a **cluster name** and a **customer complaint or issue**
(ideally with a time window). It handles two kinds of investigations:

- **Cluster investigation** — diagnose a specific symptom (slow queries, MV lag, ingestion
  delay, high CPU, throttling, crashes) on one cluster.
- **Tenant investigation** — profile all clusters belonging to a customer (SKU, ingestion
  volume, extents, databases, tables, scaling patterns).

Trigger phrases: *"cluster investigation"*, *"cluster health"*, *"performance issue"*,
*"query failure"*, *"mv age growing"*, *"ingestion delayed"*, *"throttling"*.

## How to invoke

Ask Copilot to use the skill and give it the cluster + issue, e.g.:

```
Use the kustomer-optimization skill to investigate: cluster=WIZPRODUS102 mv age growing starting 27 june
```
```
Investigate a claim from cluster=DATATUBEPRODEU — queries are slow since yesterday
```

If no time period is given, the skill assumes **7 days**.

## Prerequisites

- **Azure CLI** signed in with access to the Kuskus clusters
  (`az login`). The query script acquires a token via
  `az account get-access-token` for the selected Kuskus endpoint.
- **Python 3** (standard library only — no extra packages required).
- Network access to the regional Kuskus endpoints.

## How it works

All queries run through the bundled script — **do not create new scripts or tools**:

```powershell
# From the skill's scripts/ directory
python query_kusto.py "DimClustersMv() | where Source == toupper('<cluster>') | project Source, SourceQualified, RegionalTracingTargetUrl"

# For a specific-cluster investigation, use RegionalTracingTargetUrl afterward
python query_kusto.py --cluster "<RegionalTracingTargetUrl>" "QueryCompletion | take 10"
```

- Defaults to cluster `kuskushead.westeurope`, database `Kuskus`.
- Override with `--cluster` and `--database`.
- Output is one JSON object per row (newlines flattened), easy to scan or pipe.

### Typical investigation flow

1. **Identify the cluster** — query `DimClustersMv()` for tenant, region, SKU, node
   count, `SourceQualified`, and `RegionalTracingTargetUrl`. (Use `DimClustersMv`,
   *not* `DimClusters`, for cluster details.)
2. **Pick the right Kuskus** — use `kuskushead.westeurope` for all-region or
   multi-region investigations. Only for a specific-cluster investigation, use
   its `RegionalTracingTargetUrl` directly as the regional Kuskus endpoint. Do
   not derive it from `ServiceConnectionString` or assume a static regional
   endpoint.
3. **Run targeted diagnostics** — choose queries by symptom category (ingestion, query,
   resource, workload, update policy, materialized views).
4. **Always check autoscaling** during any degradation (machine-count changes, scale
   reasons, capacity-restricted scale-out).
5. **Check Memento** for policy/definition changes before concluding a system root cause
   (no short time filter — changes can be years old).
6. **Write the report** to its `Investigations/yyyy-mm/` folder.

## Reference material

| Path | Contents |
|---|---|
| `SKILL.md` | The skill instructions Copilot follows (start here). |
| `scripts/query_kusto.py` | The only query runner — KQL/management commands via Azure CLI auth. |
| `references/new-kuskus-useful-queries.md` | Curated, symptom-organized investigation queries. |
| `references/queries.md`, `references/kuskus-useful-queries.md` | Additional query collections. |
| `references/knowledge/mv-investigation-guide.md` | End-to-end materialized-view diagnosis guide. |
| `references/knowledge/ingestion-monitoring.md` | Ingestion observability knowledge base (two-layer architecture, gaps, owners). |
| `references/knowledge/KustoMdmMetricsV1-guide.md` | Guide to the MDM time-series metrics. |
| `references/knowledge/functions-index.md` | All Kuskus functions grouped by folder. |
| `references/knowledge/folders/*.md` | Per-folder function documentation (AutoScale, DM, OPS, etc.). |

## Special notes

- **Fabric Eventhouses** have names starting with `TRD-`. In `QueryCompletion`,
  `CommandCompletion`, and other `KustoLogs`-derived tables, their `Source` is prefixed
  with the hoster name (e.g. `KUTRIDENTHOSTERWEU.TRD-...`). Run `DimClustersMv()` first and
  use the qualified source for subsequent queries; strip the hoster prefix when joining to
  `DataIngestHistoryMv` / `DimClustersMv`.
- **`QueryCompletion.Machine`** identifies the node that did query *planning* (the admin
  node), **not** execution. Seeing all queries on one machine is normal. Use
  `PerfCounterCPU` (grouped by `Machine`, `bin(Timestamp, 10m)`, `avg(CounterValue)`) for
  real per-node load.
- Always show the **tenant name** alongside the cluster name (`DimClustersMv().TenantName`).

## Output

The skill produces a Markdown report saved as
`Investigations/yyyy-mm/yyyy-mm-dd-tenantname-clustername-report.md`, with two
sections:

1. **Investigation Summary** — tenant, cluster, timeline, issue, root cause, impact,
   mitigations (no queries; ready to paste into Outlook).
2. **Investigation Summary including Queries (Internal use)** — identical content plus the
   KQL behind every finding and conclusion.
