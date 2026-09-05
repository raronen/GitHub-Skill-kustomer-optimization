# Ingestion Monitoring & Observability — Knowledge Base

**Last Updated:** 2026-06-09  
**Sources:** Internal email threads (May 30 – Jun 9, 2026), SharePoint design doc comments, ICM analysis

---

## Overview

Ingestion monitoring/observability is an active area of investment for Kusto/Eventhouse. The goal is to give users full visibility into their ingestion pipelines — covering batch ingestion, streaming ingestion, and data connections (both pull and push modes) — across both Azure (ADX) and Fabric (Eventhouse) surfaces.

**Key Design Document:** [Ingestion Observability.docx](https://microsoft.sharepoint.com/teams/Kusto/Internal/Shared%20Documents/Design/Ingestion%20Observability.docx)  
**Owner (Ingestion Observability spec):** Vincent-Philippe Lauzon  
**Stakeholders:** Guy Reginiano (Fabric Monitoring/Data Connections), Meital Taran-Gutman (management), Denise Schlesinger (Engine/MV observability), Tzvia Gitlin Troyna (Fabric Monitoring), Nir Boger (Engine), Slavik Neimer (Engine)

---

## Architecture: Two Layers

Per Meital's clarification (Jun 4, 2026):

### Layer 1 — Signal Collection (P0)
- Making sure all needed signals exist and are locally available in the system DB
- If a user runs `.show` commands, the data should be available
- Applies to **both** Fabric and Azure
- **Current status:** Still has gaps — this is the P0 priority

### Layer 2 — Centralized Monitoring Experience
- Azure: Azure Monitor (metrics + diagnostics)
- Fabric: Workspace Monitoring (WSM) — essentially an Eventhouse with low-CU that can scale out, plus built-in RTD templates
- A Fabric team is planning "Azure Monitor in Fabric" — first step is consolidating monitoring Eventhouses from per-workspace to per-tenant (planned Sept 2026)
- Layer 2 **depends on** Layer 1 being complete

---

## Key Debates & Decisions

### Metrics-First vs .show Commands-First

**Vincent-Philippe's position (metrics-first):**
- Historically, engineers guarded system tables aggressively (Alex)
- Ingestion volume can be considerable; writing more system data during high-ingestion stress = recipe for disaster
- Metrics are one UI, no KQL required — a non-KQL user can troubleshoot from charts
- Precedent: `.show data operations` exists (one row per ingestion per table)

**Meital's position (both layers are independent):**
- Layer 1 (`.show` commands) can exist independently of Layer 2
- Layer 1 is the prerequisite — signals must exist first
- We already have metrics AND logs in WSM, just not a full metrics model

**Nir's counter-proposal:**
- Brainstorm between Nir & Slavik on `.show command`-based approach
- Take all proposed metrics with all proposed dimensions (including tables & databases)
- Have one system table per metric and a corresponding `.show` command
- Must pass the "Tomer/Ziv test"

### Consensus
Both approaches are complementary. P0 is filling gaps in Layer 1 (signal capture during ingestion). The delivery mechanism (metrics vs .show commands) is secondary.

---

## Current Gaps & Pain Points

### 1. Data Connection Health (Dead Spot)
- Today: `.show data connections` is used in UI, but incomplete (not all cases covered)
- Users turn to `.show ingestion failures` and get frustrated
- **Proposed:** A "connection health" metric (0/1) with data connection as dimension
- **Complication:** Eventstream can push data via SDK without a data connection — push mode has no Data Connection object. Users expect both push and pull to expose the same monitoring visibility.

### 2. Streaming Ingestion Visibility
- `.show data operations` includes RowStoreSeal records, but sealing can take up to 24 hours — problematic for streaming use cases
- `.show streaming ingestion statistics | summarize sum(Count) by Database, Table` — no breakdown by application
- No equivalent of CPU/utilization metrics for streaming ingestion today

### 3. Ingestion Utilization Metrics (Limited Dimensions)
- Existing metrics:
  - **Ingestion Utilization** — for batch ingestion
  - **Streaming Ingest Utilization** — for streaming ingestion
- These metrics currently lack dimensions (database, table, application)

### 4. Pre-Ingestion Errors
- Open question: How to address errors before ingestion starts (e.g., authentication error in Event Hub)?
- Metrics are bound to ingestion count — how to attach non-ingestion errors in the ingestion flow?

### 5. Application Breakdown
- `.show journal | where Event in ("UpdatePolicy", "BatchIngest") | summarize sum(TotalCpu) by Database, Table` — no app-level breakdown
- No way to attribute ingestion load to specific applications

### 6. Input Volume Measurement
- "Input volume" = data entering Kusto in raw/original format (e.g., CSV files)
- Open question: compressed or original? Answer: original (per spec)

---

## Azure Monitor Issues

### Dev Cluster Stats Not Surfacing (Jun 7, 2026)
- **Reported by:** Ziv Caspi
- **Issue:** Dev cluster (zivckusto2) shows no metrics in Azure Monitor Insights blade even though logging is configured
- **Action:** Itay Sagui added Oren Hasbani (Insights expert) to investigate
- **Implication:** If internal dev clusters can't show metrics, external customers face same issues

---

## OneLake Continuous Ingestion (Jun 4, 2026)

- **Context:** Fabric Telemetry team moving workload from ADX to Eventhouse
- **Issue:** No ETA for continuous ingestion from OneLake
- **Related:** Troubleshooting continuous ingestion for parquet with customer (Debasis)
- **Ask:** Provide ETA for OneLake continuous ingestion — this blocks Fabric Telemetry migration

---

## MV Background Tasks Observability (Parallel Effort)

- **Owner:** Denise Schlesinger
- **PRD:** [mv-observability-prd.docx](https://microsofteur-my.sharepoint.com/:w:/g/personal/dschlesinger_microsoft_com/IQCaPc4IceQQQa3NZjc7SkwRAdWrZ1eaUIldGdo7uJVmPhY)
- **Status:** PRD being restructured; feature review meeting was scheduled then canceled (Jun 7)
- **Scope:** Observability for materialized view background processing
- **Invited reviewers:** Anshul Sharma, Brad Watts, Dany Hoter, Gabi Lehner, Guy Reginiano, Hadas Stern, Meital Taran-Gutman, Michal Bar, Naor Biton, Oded Sacher, Oron Kaiser, Shiri Morshtein, Tzvia Gitlin Troyna, Vincent-Philippe Lauzon, Ziv Caspi, Shiri Harel, Sagiv Michael, Amit Ofir, Roy Ofer

---

## ICM Impact Analysis (Jun 5, 2026)

- **Author:** Vincent-Philippe Lauzon
- **Finding:** ~50% of ICMs could potentially be addressed with better observability
- **Key Insight:** The real target isn't ICMs — it's users who try Kusto, fail silently, and abandon without ever opening a ticket
- **Published in:** Ingestion Observability spec, section 3.1

---

## File Streaming (Ingestion from Azure Storage)

- **Meeting series:** "File streaming" (ingestion from Azure Storage) | Kusto & Messaging weekly sync
- **Participants:** Guy Reginiano, Oren Hasbani, Michael Shikh, Yu Zhou
- **Status:** Multi-part walkthrough scheduled (Parts 2 & 3 tentatively accepted, Jun 8)
- **Relevance to monitoring:** File streaming is a new ingestion path that will need observability coverage

---

## Fabric Monitoring Integration (Guy's Domain)

Per Meital (Jun 4): "Once we have more signals for ingestion, @Guy Reginiano is the owner to make sure it's represented as needed in [Workspace Monitoring]."

**Current Fabric Monitoring state:**
- WSM starts with low CU but can scale out
- Built-in RTD templates exist for Eventhouse
- Both metrics and logs available, but no full metrics model (table-based)
- Consolidation from per-workspace to per-tenant monitoring Eventhouse: planned Sept 2026

---

## Key People & Roles

| Person | Role in Ingestion Monitoring |
|--------|------------------------------|
| Vincent-Philippe Lauzon | Ingestion Observability spec owner |
| Guy Reginiano | Fabric Monitoring / Data Connections / WSM representation |
| Meital Taran-Gutman | PM management, alignment |
| Denise Schlesinger | MV observability, engine alignment |
| Tzvia Gitlin Troyna | Fabric Monitoring |
| Nir Boger | Engine implementation options |
| Slavik Neimer | Engine implementation options |
| Ziv Caspi | Architecture / Azure Monitor gaps |
| Itay Sagui | Azure Monitor / Insights |
| Oren Hasbani | Insights expert, File Streaming |
| Shahar Prish | Engine |

---

## Open Actions & Next Steps

1. **Fill Layer 1 gaps** — capture missing ingestion signals (P0)
2. **Resolve metrics vs .show debate** — Nir/Slavik brainstorm on feasibility
3. **Data connection health metric** — design for both pull and push modes
4. **Dev cluster Azure Monitor issue** — Oren investigating
5. **OneLake continuous ingestion ETA** — needed for Fabric Telemetry migration
6. **MV observability PRD** — restructuring, will reschedule feature review
7. **File streaming observability** — ensure new ingestion path gets monitoring coverage
8. **Extend observability beyond Kusto** — input needed from Boisvert on unifying push/pull flows
