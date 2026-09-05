# Investigation Instructions Changelog

Chronological log of investigation-guidance changes requested in user
interactions. Repeated requests with the same meaning are represented once.
Append a new row whenever a user changes investigation guidance; record the
requesting user, interaction date, and the instruction itself.

| Date | User | Change |
|---|---|---|
| 2026-06-21 | @DanyhoterMS | Use `bin_at()` instead of `bin()` whenever an investigation must divide a filtered time range into equal-sized buckets. Anchor the bins to the beginning or end of the analyzed period so partial first and last buckets do not distort comparisons. |
| 2026-06-24 | @DanyhoterMS | Fleet-wide Fabric Eventhouse investigations must include virtual clusters, whose telemetry source is hoster-qualified as `<HOSTER>.TRD-...`, rather than filtering only sources that start with `TRD-`. Include the supporting queries in the report. |
| 2026-06-29 | @DanyhoterMS | Treat `DimClustersMv()` as one row per `Source`; do not add unnecessary `arg_max()` or deduplication by source. |
| 2026-07-07 | @DanyhoterMS | Before summarizing `FailureReason`, inspect at most the first 1,000 characters and classify failures into no more than 15 stable buckets. Use the buckets in later investigations instead of grouping by full free text. |
| 2026-07-14 | @DanyhoterMS | Engine and diagnostic telemetry is retained for about 30 days; `Memento()` is the exception. Do not compare the visible last 30 days with an unavailable earlier period or infer that the earliest visible record is the issue onset. |
| 2026-07-16 | @DanyhoterMS | For a Fabric Eventhouse investigation, read `DimClustersMv().RegionalTracingTargetUrl` and use that regional Kuskus endpoint for subsequent cluster telemetry queries. |
| 2026-07-16 | @DanyhoterMS | Apply the same `RegionalTracingTargetUrl` endpoint-selection rule to classic ADX clusters; do not derive regional Kuskus from the cluster query URL. |
| 2026-07-16 | @DanyhoterMS | Add an ingestion-health section to future cluster-health investigations for the main large tables. Model queryable-data latency as batch interval + batch processing time + MV age when an MV is present. |
| 2026-07-16 | @DanyhoterMS | Measure the real interval between ingestion batches from `DataIngest` or `CommandCompletion`; do not substitute the configured ingestion-batching policy interval. |
| 2026-07-16 | @DanyhoterMS | Present ingestion latency for the main queried tables as a table with three components: average time between batches, batch processing time, and MV age when applicable. |
| 2026-07-18 | @DanyhoterMS | For investigations that explicitly require information from all regions, query `kuskushead.westeurope` because Kuskushead sends the query to every regional Kuskus instance. Do not loop through and manually merge regional endpoints. |
| 2026-07-18 | @DanyhoterMS | For Fabric virtual clusters, obtain the latest core count from `DimClustersMv()` using `tolong(['ServiceConfiguration']['VirtualClusterSettings']['Limits']['EngineCoreLimit'])`. Use the same expression on `DimClusters` to analyze historical core-limit changes. |
| 2026-07-19 | @DanyhoterMS | `PerfCounterCPU` does not provide CPU utilization for Fabric virtual clusters. Calculate VC utilization by adding `QueryCompletion.TotalCPU` and `CommandCompletion.TotalCpuMs`, then dividing consumed CPU time by the VC's available cores and the analyzed interval. Use the historical core limit for intervals that cross core-count changes. |
| 2026-07-19 | @DanyhoterMS | Keep this changelog current whenever investigation instructions change, recording the user, date, and change. |
| 2026-07-19 | @DanyhoterMS | Store investigation artifacts in monthly `Investigations/yyyy-mm/` folders, using the date prefix in each filename to select the folder. |
