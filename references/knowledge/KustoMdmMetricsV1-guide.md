# KustoMdmMetricsV1 Metrics Reference Guide

## Overview

- `KustoMdmMetricsV1()` is a function in the `Kuskus` database that provides MDM (Monitoring Data Management) metrics for Azure Data Explorer/Kusto clusters.
- It is exposed as a cross-cluster shortcut over the `Kuskus` entity group, so one query can read metrics from all regional Kuskus instances.
- This guide was generated from the supplied extracts covering **4,944 distinct namespace/metric pairs** across **55 namespaces**.
- How to query: `KustoMdmMetricsV1() | where TIMESTAMP > ago(7d) | where metricNamespace == "..." | where metricName == "..."`
- Typical troubleshooting flow: filter by `TIMESTAMP`, then `Cluster`, then `metricNamespace`, and finally narrow by `metricName` and parsed dimensions.

## Table Schema

> Note: the schema below combines direct evidence from repository queries with the standard Geneva MDM metric shape used by `KustoMdmMetricsV1`. In day-to-day investigations, engineers usually rely on the normalized fields (`Cluster`, `metricNamespace`, `metricName`, `dimension*`, and the aggregate value columns); the `env_*` fields are envelope metadata and are often only needed for producer provenance.

| Column | Type | Meaning |
|---|---|---|
| `env_time` | `datetime` | Geneva envelope event time before/alongside normalized TIMESTAMP. |
| `env_ver` | `string` | Envelope schema/version marker for the emitted metric event. |
| `env_seqNum` | `long` | Producer sequence number used to order envelope events. |
| `env_epoch` | `long` | Producer epoch or generation value for sequence continuity. |
| `env_name` | `string` | Envelope event name/type emitted by the Geneva producer. |
| `env_flags` | `long` | Envelope flags describing producer/runtime behavior. |
| `env_os` | `string` | Operating system family reported by the producer. |
| `env_osVer` | `string` | Operating system version reported by the producer. |
| `env_cloud` | `string` | High-level cloud stamp or cloud context from the envelope. |
| `env_cloud_environment` | `string` | Cloud environment such as Azure public, sovereign, or test environment. |
| `env_cloud_location` | `string` | Envelope-level location/region metadata. |
| `env_cloud_name` | `string` | Cloud/stamp name emitted by the Geneva producer. |
| `env_cloud_role` | `string` | Envelope role name for the emitting service. |
| `env_cloud_roleInstance` | `string` | Envelope role instance/node for the emitting service. |
| `env_cloud_deploymentId` | `string` | Envelope deployment identifier. |
| `env_cloud_deploymentUnit` | `string` | Envelope deployment unit or scale-unit identifier. |
| `env_tenant` | `string` | Envelope tenant identifier as provided by the producer. |
| `env_account` | `string` | Envelope account/monitoring account identifier. |
| `env_moniker` | `string` | Envelope source moniker or logical producer name. |
| `env_namespace` | `string` | Envelope namespace identifying the source metric domain. |
| `env_node` | `string` | Envelope node or machine identifier for the metric emitter. |
| `TIMESTAMP` | `datetime` | Primary timestamp used in most KQL filters and aggregations. |
| `PreciseTimeStamp` | `datetime` | Higher-precision event timestamp when sub-bucket ordering matters. |
| `Tenant` | `string` | Normalized tenant identifier for the emitting service/cluster. |
| `Account` | `string` | Normalized account/monitoring account for the metric stream. |
| `Cluster` | `string` | Cluster name, usually uppercase in practice. |
| `DataCenter` | `string` | Datacenter/region for the cluster or emitting node. |
| `DeploymentID` | `string` | Deployment identifier for the cluster/service rollout. |
| `Role` | `string` | Service role that emitted the metric. |
| `RoleInstance` | `string` | Specific node/service instance that emitted the metric. |
| `CloudName` | `string` | Cloud environment/stamp name associated with the cluster. |
| `DeploymentRing` | `string` | Deployment ring (for example hotfix, pilot, prod) for the cluster/service. |
| `timeBucketUtc` | `datetime` | UTC aggregation bucket used by Geneva for pre-aggregated values. |
| `monitoringAccount` | `string` | Geneva monitoring account that owns the metric definition. |
| `metricNamespace` | `string` | Metric namespace, used first to narrow the search surface. |
| `metricName` | `string` | Metric name within the namespace. |
| `dimensionNameList` | `string` | Caret (^) separated list of dimension names. |
| `dimensionValueList` | `string` | Caret (^) separated list of dimension values aligned to dimensionNameList. |
| `scalingFactor` | `real` | Multiplier/divisor needed to convert stored values to display units when applicable. |
| `samplingTypeFlags` | `int` | Flags describing how the metric was sampled/aggregated upstream. |
| `minValue` | `real` | Minimum value observed in the aggregation bucket. |
| `maxValue` | `real` | Maximum value observed in the aggregation bucket. |
| `sumValue` | `real` | Sum of all observed values in the aggregation bucket. |
| `sumOfSquaresValue` | `real` | Sum of squared values; useful for variance/stddev calculations. |
| `countValue` | `long` | Number of observations contributing to the aggregate. |
| `SourceNamespace` | `string` | Original source namespace before normalization/wrapping. |
| `SourceMoniker` | `string` | Original source moniker or component identifier. |
| `SourceVersion` | `string` | Version of the metric source/emitter. |
| `GenevaAccount` | `string` | Geneva account associated with the metric source. |
| `SourceCluster` | `string` | Upstream source cluster or stamp if different from Cluster. |
| `ComputeResourceId` | `string` | Azure resource ID or compute resource identifier for the emitting infrastructure. |

## Metric Namespaces Overview

### Core Engine Metrics

Query execution, CPU, memory, cache, extents, and engine-hosted virtual cluster state.

| Namespace | Metric count | Category description |
|---|---:|---|
| `engineMetrics` | 479 | Legacy/raw engine service metrics and Windows/OpenTelemetry counters for query execution, runtime, memory, and node health. |
| `MdmEngineMetrics` | 140 | Curated MDM engine metrics for extents, ingestion, query acceleration, cache, continuous export, and cluster data capacity. |
| `MdmEngineHosterMetrics` | 5 | Virtual-cluster hoster metrics for engine-hosted tenants, startup, and hoster state. |

### Data Management Metrics

Ingestion orchestration, batching, request handling, queues, and DM hoster behavior.

| Namespace | Metric count | Category description |
|---|---:|---|
| `dmMetrics` | 181 | Legacy/raw data-management service metrics and runtime counters for ingestion, queues, outbound calls, and process health. |
| `MdmDataMgmtMetrics` | 51 | Curated DM metrics for batching, authentication, request handling, ingestion age, and ingestion capacity. |
| `MdmDataMgmtHosterMetrics` | 6 | Hoster metrics for DM virtual clusters, node targets, CPU, and hoster health. |

### Cluster Management Metrics

Cluster operations, autoscale, maintenance jobs, and control-plane health.

| Namespace | Metric count | Category description |
|---|---:|---|
| `cmMetrics` | 92 | Legacy/raw cluster-management metrics for requests, background jobs, Cosmos DB calls, and control-plane operations. |
| `MdmClusterMgmtMetrics` | 54 | Curated CM metrics for autoscale, maintenance, deployment, operation latency, and cluster-management health. |
| `MdmOptimizerAutoScaleMetrics` | 6 | Optimizer and autoscale controller metrics for predictive/reactive scaling decisions. |

### Ingestion Pipeline Metrics

Pipeline stage metrics from pre-batching through streaming ingestion and Geneva ingestion.

| Namespace | Metric count | Category description |
|---|---:|---|
| `KustoIngestion` | 3 | End-to-end ingestion stage metrics covering latency and ingestion errors. |
| `KustoBatching` | 2 | Batching-stage latency metrics before data is ingested. |
| `KustoPreBatching` | 2 | Pre-batching stage latency metrics ahead of batching. |
| `KustoBlobDownloader` | 6 | Blob download stage metrics for ingestion sources, bytes downloaded, and row handling. |
| `StreamingIngestionMetrics` | 12 | Streaming ingestion row-store and seal metrics, including concurrency, duration, WAL size, and local storage pressure. |
| `MdmGenevaIngestionMetrics` | 8 | Metrics for shipping Geneva/MDM data into Kusto, including batch outcomes and blob latency. |

### Query Metrics

Query concurrency, latency, request pressure, and sandbox/container behavior.

| Namespace | Metric count | Category description |
|---|---:|---|
| `QueryMetrics` | 3 | Direct query workload metrics for concurrency, duration, and throttling. |
| `SandboxMetrics` | 7 | Sandbox/container lifecycle and throttling metrics for isolated query execution. |
| `RequestMetrics` | 2 | Request-level concurrency and request-classification metrics. |

### Resource Provider Metrics

ARM/RP operations, SaaS RP health, and service-probe or RP runtime counters.

| Namespace | Metric count | Category description |
|---|---:|---|
| `resourceProviderMetrics` | 99 | Resource-provider control-plane metrics for ARM objects such as clusters, data connections, and attached DB configurations. |
| `MdmSaasRpMetrics` | 58 | Curated SaaS resource-provider metrics and runtime counters. |
| `spMetrics` | 85 | Service-probe service runtime counters, mostly process/.NET and network metrics. |
| `rpMetrics` | 1 | Very small RP metric surface, mainly raw processor counters. |

### Platform & Infrastructure

Node/platform counters plus bridge and gateway service behavior.

| Namespace | Metric count | Category description |
|---|---:|---|
| `PlatformMetrics` | 4 | Basic host infrastructure counters such as CPU, memory, and disk free space. |
| `BridgeMetrics` | 60 | Bridge service operational metrics plus host counters and outbound HTTP timings. |
| `MdmBridgeMetrics` | 8 | Curated bridge health and synchronization freshness metrics. |
| `GatewayMetrics` | 2 | Gateway authentication and throttling metrics. |

### Billing Metrics

Billing and resource-usage telemetry, dominated by Windows/.NET counters with a few billing-specific metrics.

| Namespace | Metric count | Category description |
|---|---:|---|
| `billingMetrics` | 3206 | Billing/usage namespace dominated by guest and agent performance counters, with a small set of billing-specific job metrics. |

### Kubernetes/Kuiper Metrics

Container and Kubernetes infrastructure metrics collected from Kuiper/Prometheus exporters.

| Namespace | Metric count | Category description |
|---|---:|---|
| `Kuiper.CgroupExporter` | 8 | cgroup-level Linux container resource metrics for CPU, memory, and IO. |
| `Kuiper.MetricsCollector.AzureCNI` | 8 | Azure CNI metrics for IP allocation state and collector process CPU. |
| `Kuiper.MetricsCollector.CoreDNS` | 12 | CoreDNS cache and DNS request metrics. |
| `Kuiper.MetricsCollector.KubeProxy` | 11 | Kube-proxy rule programming and sync duration metrics. |
| `Kuiper.MetricsCollector.KubeStateMetricsV2` | 41 | Kubernetes object-state metrics for pods, deployments, daemonsets, jobs, PVCs, and nodes. |
| `Kuiper.MetricsCollector.Kubelet` | 11 | Kubelet operational metrics for CSI, pod start, image pulls, and node startup. |
| `Kuiper.MetricsCollector.NodeExporter` | 23 | Node-exporter host metrics for CPU, disk, filesystem, and memory. |
| `Kuiper.MetricsCollector.NodeProblemDetector` | 1 | Node problem detector state metric. |
| `Kuiper.MetricsCollector.cAdvisor` | 22 | Container resource metrics for CPU, filesystem, and memory working set. |

### Synthetics & Monitoring

Synthetic probes and monitoring pipeline health for the Kusto estate.

| Namespace | Metric count | Category description |
|---|---:|---|
| `Canary` | 2 | Simple canary metrics used to verify pipeline or namespace presence. |
| `HealthSuiteMetrics` | 9 | Health suite metrics for operational latency, table health, ingestion latency, and base memory counters. |
| `Monitoring Agent` | 26 | Monitoring agent self-observability metrics such as CPU, ETW loss, and data delay. |
| `MetricsExtension` | 5 | Metric extension pipeline counters for received, lost, dropped, and published aggregates. |
| `MetricsExtension2` | 18 | Second-generation metrics extension metrics for config load, publication queues, ingest counts, and CPU/memory usage. |
| `SyntheticsBridgeMetrics` | 1 | Synthetic probes for bridge availability. |
| `SyntheticsClusterManagementMetrics` | 1 | Synthetic probes for CM availability. |
| `SyntheticsDataManagementMetrics` | 6 | Synthetic DM probes for service, hoster, configuration, and virtual-cluster ingestion. |
| `SyntheticsEngineMetrics` | 51 | Synthetic engine probes and capacity metrics mirroring critical engine-state indicators. |
| `SyntheticsPlatformMetrics` | 1 | Synthetic execution-time metric for platform checks. |
| `SyntheticsResourceProviderMetrics` | 2 | Synthetic RP availability and ARM-call probe metrics. |
| `SyntheticsSaasResourceProviderMetrics` | 1 | Synthetic SaaS RP availability probes. |
| `SyntheticsServiceProbeMetrics` | 1 | Synthetic service-probe availability metric. |

### Other

Miscellaneous namespaces that do not fit the core Kusto service buckets.

| Namespace | Metric count | Category description |
|---|---:|---|
| `OneLakeClient` | 7 | OneLake client latency and throughput metrics for read/write/billing operations. |
| `OrchestrationsMetrics` | 8 | Durable orchestration/activity metrics, especially queue latency and orchestration duration. |
| `CommandMetrics` | 1 | Command-level throttling metric. |
| `DefaultNamespace` | 26 | Uncategorized/default Geneva metrics, often related to batching, ingestion size, and operation duration. |
| `Microsoft/Web/AppServicePlans` | 21 | Azure App Service Plan platform metrics surfaced through MDM. |
| `Microsoft/Web/WebApps` | 38 | Azure Web App runtime and request metrics surfaced through MDM. |

## Detailed Metrics by Namespace

The sections below summarize each namespace, list the observed metrics and dimensions, and add a practical explanation of what each metric likely measures based on its name and surrounding namespace context.

### Core Engine Metrics

Query execution, CPU, memory, cache, extents, and engine-hosted virtual cluster state.

#### `engineMetrics` (479 metrics)

Legacy/raw engine service metrics and Windows/OpenTelemetry counters for query execution, runtime, memory, and node health.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dns.lookup.duration` | `Cluster^DataCenter^dns.question.name^VirtualClusterName` | Likely measures latency or duration for dns lookup duration. |
| `http.client.connection.duration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^network.peer.address^network.protocol.version^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely measures latency or duration for http client connection duration. |
| `http.client.request.duration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.request.method^http.response.status_code^network.protocol.version^ResourceId^server.address^server.port^url.scheme^VirtualClusterName` | Likely measures latency or duration for http client request duration. |
| `process.runtime.dotnet.gc.duration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures latency or duration for process runtime dotnet gc duration. |
| `process.runtime.dotnet.thread_pool.completed_items.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures latency or duration for process runtime dotnet thread pool completed items count. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dotnet.thread_pool.queue.length` | `(none)` | Likely counts the current amount of dotnet thread pool queue length. |
| `dotnet.thread_pool.thread.count` | `(none)` | Likely counts the current amount of dotnet thread pool thread count. |
| `dotnet.thread_pool.work_item.count` | `(none)` | Likely counts the current amount of dotnet thread pool work item count. |
| `http.client.active_requests` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.request.method^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely counts the current amount of http client active requests. |
| `http.client.request.time_in_queue` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.request.method^network.protocol.version^ResourceId^server.address^server.port^url.scheme^VirtualClusterName` | Likely counts the current amount of http client request time in queue. |
| `process.runtime.dotnet.assemblies.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet assemblies count. |
| `process.runtime.dotnet.jit.methods_compiled.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet jit methods compiled count. |
| `process.runtime.dotnet.monitor.lock_contention.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet monitor lock contention count. |
| `process.runtime.dotnet.thread_pool.queue.length` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet thread pool queue length. |
| `process.runtime.dotnet.thread_pool.threads.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet thread pool threads count. |
| `process.runtime.dotnet.timer.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet timer count. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dotnet.gc.collections` | `(none)` | Likely tracks resource usage or capacity for dotnet gc collections. |
| `dotnet.gc.heap.total_allocated` | `(none)` | Likely tracks resource usage or capacity for dotnet gc heap total allocated. |
| `process.runtime.dotnet.gc.collections.count` | `Cluster^DataCenter` | Likely counts the current amount of process runtime dotnet gc collections count. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dotnet.jit.compiled_il.size` | `(none)` | Likely measures size, volume, or throughput for dotnet jit compiled il size. |
| `process.runtime.dotnet.gc.allocations.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc allocations size. |
| `process.runtime.dotnet.gc.committed_memory.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc committed memory size. |
| `process.runtime.dotnet.gc.heap.fragmentation.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^generation^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc heap fragmentation size. |
| `process.runtime.dotnet.gc.heap.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^generation^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc heap size. |
| `process.runtime.dotnet.gc.objects.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc objects size. |
| `process.runtime.dotnet.jit.il_compiled.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet jit il compiled size. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dotnet.exceptions` | `DataCenter` | Likely counts errors, failures, or throttling for dotnet exceptions. |
| `process.runtime.dotnet.exceptions.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for process runtime dotnet exceptions count. |

##### Windows / .NET perf counters

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `\.NET CLR Exceptions(Kusto.WinSvc.Svc)\# of Exceps Thrown / sec` | `(none)` | Windows/Geneva performance counter for # of exceps thrown / sec on NET CLR Exceptions (Kusto.WinSvc.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.Svc)\# Bytes in all Heaps` | `Account^Cluster^DataCenter^RoleInstance` | Windows/Geneva performance counter for # bytes in all heaps on NET CLR Memory (Kusto.WinSvc.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.Svc)\# Total committed Bytes` | `Tenant` | Windows/Geneva performance counter for # total committed bytes on NET CLR Memory (Kusto.WinSvc.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.Svc)\% Time in GC` | `(none)` | Windows/Geneva performance counter for % time in gc on NET CLR Memory (Kusto.WinSvc.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.Svc)\Allocated Bytes/sec` | `(none)` | Windows/Geneva performance counter for allocated bytes/sec on NET CLR Memory (Kusto.WinSvc.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.Svc)\Gen 0 heap size` | `(none)` | Windows/Geneva performance counter for gen 0 heap size on NET CLR Memory (Kusto.WinSvc.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.Svc)\Gen 1 heap size` | `(none)` | Windows/Geneva performance counter for gen 1 heap size on NET CLR Memory (Kusto.WinSvc.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.Svc)\Gen 2 heap size` | `__Tenant` | Windows/Geneva performance counter for gen 2 heap size on NET CLR Memory (Kusto.WinSvc.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.Svc)\Large Object Heap size` | `(none)` | Windows/Geneva performance counter for large object heap size on NET CLR Memory (Kusto.WinSvc.Svc). |
| `\LogicalDisk(_Total)\% Free Space` | `Cluster^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Read Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Write Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Current Disk Queue Length` | `Account^Cluster^DataCenter` | Windows/Geneva performance counter for current disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Free Megabytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for free megabytes on Logical Disk (_Total). |
| `\LogicalDisk(C:)\% Free Space` | `Cluster^RoleInstance` | Windows/Geneva performance counter for % free space on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Write Queue Length` | `Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (C:). |
| `\LogicalDisk(C:\Packages\Plugins\Microsoft.Azure.Security.AzureDiskEncryption\2.5.0.55\BekMountDir)\% Free Space` | `(none)` | Windows/Geneva performance counter for % free space on Logical Disk (C:\Packages\Plugins\Microsoft.Azure.Security.AzureDiskEncryption\2.5.0.55\BekMountDir). |
| `\LogicalDisk(C:\Packages\Plugins\Microsoft.Azure.Security.AzureDiskEncryption\2.5.0.55\BekMountDir)\Avg. Disk Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (C:\Packages\Plugins\Microsoft.Azure.Security.AzureDiskEncryption\2.5.0.55\BekMountDir). |
| `\LogicalDisk(C:\Packages\Plugins\Microsoft.Azure.Security.AzureDiskEncryption\2.5.0.55\BekMountDir)\Avg. Disk Read Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (C:\Packages\Plugins\Microsoft.Azure.Security.AzureDiskEncryption\2.5.0.55\BekMountDir). |
| `\LogicalDisk(C:\Packages\Plugins\Microsoft.Azure.Security.AzureDiskEncryption\2.5.0.55\BekMountDir)\Avg. Disk Write Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (C:\Packages\Plugins\Microsoft.Azure.Security.AzureDiskEncryption\2.5.0.55\BekMountDir). |
| `\LogicalDisk(C:\Packages\Plugins\Microsoft.Azure.Security.AzureDiskEncryption\2.5.0.55\BekMountDir)\Current Disk Queue Length` | `(none)` | Windows/Geneva performance counter for current disk queue length on Logical Disk (C:\Packages\Plugins\Microsoft.Azure.Security.AzureDiskEncryption\2.5.0.55\BekMountDir). |
| `\LogicalDisk(D:)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Read Queue Length` | `__Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (D:). |
| `\LogicalDisk(D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{7fab9a7d-0f1b-43cb-9721-47365c73aff9})\% Free Space` | `(none)` | Windows/Geneva performance counter for % free space on Logical Disk (D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{7fab9a7d-0f1b-43cb-9721-47365c73aff9}). |
| `\LogicalDisk(D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{7fab9a7d-0f1b-43cb-9721-47365c73aff9})\Avg. Disk Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{7fab9a7d-0f1b-43cb-9721-47365c73aff9}). |
| `\LogicalDisk(D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{7fab9a7d-0f1b-43cb-9721-47365c73aff9})\Avg. Disk Read Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{7fab9a7d-0f1b-43cb-9721-47365c73aff9}). |
| `\LogicalDisk(D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{7fab9a7d-0f1b-43cb-9721-47365c73aff9})\Avg. Disk Write Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{7fab9a7d-0f1b-43cb-9721-47365c73aff9}). |
| `\LogicalDisk(D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{7fab9a7d-0f1b-43cb-9721-47365c73aff9})\Current Disk Queue Length` | `(none)` | Windows/Geneva performance counter for current disk queue length on Logical Disk (D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{7fab9a7d-0f1b-43cb-9721-47365c73aff9}). |
| `\LogicalDisk(D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{b41ae063-0000-0000-0000-100000000000})\% Free Space` | `(none)` | Windows/Geneva performance counter for % free space on Logical Disk (D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{b41ae063-0000-0000-0000-100000000000}). |
| `\LogicalDisk(D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{b41ae063-0000-0000-0000-100000000000})\Avg. Disk Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{b41ae063-0000-0000-0000-100000000000}). |
| `\LogicalDisk(D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{b41ae063-0000-0000-0000-100000000000})\Avg. Disk Read Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{b41ae063-0000-0000-0000-100000000000}). |
| `\LogicalDisk(D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{b41ae063-0000-0000-0000-100000000000})\Avg. Disk Write Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{b41ae063-0000-0000-0000-100000000000}). |
| `\LogicalDisk(D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{b41ae063-0000-0000-0000-100000000000})\Current Disk Queue Length` | `(none)` | Windows/Geneva performance counter for current disk queue length on Logical Disk (D:\SandboxPackagesStore\WorkingDirectory\ContainerMount\Volume{b41ae063-0000-0000-0000-100000000000}). |
| `\LogicalDisk(E:)\% Free Space` | `(none)` | Windows/Geneva performance counter for % free space on Logical Disk (E:). |
| `\LogicalDisk(E:)\Avg. Disk Queue Length` | `Role` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (E:). |
| `\LogicalDisk(E:)\Avg. Disk Read Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (E:). |
| `\LogicalDisk(E:)\Avg. Disk Write Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (E:). |
| `\LogicalDisk(E:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (E:). |
| `\LogicalDisk(F:)\% Free Space` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for % free space on Logical Disk (F:). |
| `\LogicalDisk(F:)\Avg. Disk Queue Length` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (F:). |
| `\LogicalDisk(F:)\Avg. Disk Read Queue Length` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (F:). |
| `\LogicalDisk(F:)\Avg. Disk Write Queue Length` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (F:). |
| `\LogicalDisk(F:)\Current Disk Queue Length` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for current disk queue length on Logical Disk (F:). |
| `\LogicalDisk(HarddiskVolume1)\% Free Space` | `(none)` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Read Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Write Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Current Disk Queue Length` | `(none)` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume2)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume3)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume33)\% Free Space` | `(none)` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume33). |
| `\LogicalDisk(HarddiskVolume33)\Avg. Disk Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume33). |
| `\LogicalDisk(HarddiskVolume33)\Avg. Disk Read Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume33). |
| `\LogicalDisk(HarddiskVolume33)\Avg. Disk Write Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume33). |
| `\LogicalDisk(HarddiskVolume33)\Current Disk Queue Length` | `(none)` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume33). |
| `\LogicalDisk(HarddiskVolume36)\% Free Space` | `(none)` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume36). |
| `\LogicalDisk(HarddiskVolume36)\Avg. Disk Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume36). |
| `\LogicalDisk(HarddiskVolume36)\Avg. Disk Read Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume36). |
| `\LogicalDisk(HarddiskVolume36)\Avg. Disk Write Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume36). |
| `\LogicalDisk(HarddiskVolume36)\Current Disk Queue Length` | `(none)` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume36). |
| `\LogicalDisk(HarddiskVolume4)\% Free Space` | `(none)` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume4). |
| `\LogicalDisk(HarddiskVolume4)\Avg. Disk Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume4). |
| `\LogicalDisk(HarddiskVolume4)\Avg. Disk Read Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume4). |
| `\LogicalDisk(HarddiskVolume4)\Avg. Disk Write Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume4). |
| `\LogicalDisk(HarddiskVolume4)\Current Disk Queue Length` | `(none)` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume4). |
| `\LogicalDisk(HarddiskVolume5)\% Free Space` | `ResourceId` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume5). |
| `\LogicalDisk(HarddiskVolume5)\Avg. Disk Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume5). |
| `\LogicalDisk(HarddiskVolume5)\Avg. Disk Read Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume5). |
| `\LogicalDisk(HarddiskVolume5)\Avg. Disk Write Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume5). |
| `\LogicalDisk(HarddiskVolume5)\Current Disk Queue Length` | `DataCenter` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume5). |
| `\LogicalDisk(HarddiskVolume6)\% Free Space` | `(none)` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume6). |
| `\LogicalDisk(HarddiskVolume6)\Avg. Disk Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume6). |
| `\LogicalDisk(HarddiskVolume6)\Avg. Disk Read Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume6). |
| `\LogicalDisk(HarddiskVolume6)\Avg. Disk Write Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume6). |
| `\LogicalDisk(HarddiskVolume6)\Current Disk Queue Length` | `(none)` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume6). |
| `\LogicalDisk(HarddiskVolume7)\% Free Space` | `(none)` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume7). |
| `\LogicalDisk(HarddiskVolume7)\Avg. Disk Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume7). |
| `\LogicalDisk(HarddiskVolume7)\Avg. Disk Read Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume7). |
| `\LogicalDisk(HarddiskVolume7)\Avg. Disk Write Queue Length` | `(none)` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume7). |
| `\LogicalDisk(HarddiskVolume7)\Current Disk Queue Length` | `(none)` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume7). |
| `\LogicalDisk(HarddiskVolume9)\% Free Space` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume9). |
| `\LogicalDisk(HarddiskVolume9)\Current Disk Queue Length` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume9). |
| `\LogicalDisk(Z:)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (Z:). |
| `\LogicalDisk(Z:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (Z:). |
| `\LogicalDisk(Z:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (Z:). |
| `\LogicalDisk(Z:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (Z:). |
| `\LogicalDisk(Z:)\Current Disk Queue Length` | `__Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (Z:). |
| `\Memory\Available Bytes` | `Account^CloudName^Cluster^DataCenter^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for available bytes on Memory. |
| `\Memory\Cache Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for cache bytes on Memory. |
| `\Network Adapter(Microsoft Hyper-V Network Adapter _2)\Bytes Received/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes received/sec on Network Adapter (Microsoft Hyper-V Network Adapter _2). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter _2)\Bytes Sent/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes sent/sec on Network Adapter (Microsoft Hyper-V Network Adapter _2). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Received/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes received/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Sent/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes sent/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\PhysicalDisk(0 C:)\Disk Read Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (0 C:). |
| `\PhysicalDisk(0 C:)\Disk Reads/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (0 C:). |
| `\PhysicalDisk(0 C:)\Disk Write Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (0 C:). |
| `\PhysicalDisk(0 C:)\Disk Writes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (0 C:). |
| `\PhysicalDisk(0)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (0). |
| `\PhysicalDisk(0)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (0). |
| `\PhysicalDisk(0)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (0). |
| `\PhysicalDisk(0)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (0). |
| `\PhysicalDisk(1 C:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (1 C:). |
| `\PhysicalDisk(1 C:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (1 C:). |
| `\PhysicalDisk(1 C:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (1 C:). |
| `\PhysicalDisk(1 C:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (1 C:). |
| `\PhysicalDisk(1 D:)\Disk Read Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (1 D:). |
| `\PhysicalDisk(1 D:)\Disk Reads/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (1 D:). |
| `\PhysicalDisk(1 D:)\Disk Write Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (1 D:). |
| `\PhysicalDisk(1 D:)\Disk Writes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (1 D:). |
| `\PhysicalDisk(1)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (1). |
| `\PhysicalDisk(1)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (1). |
| `\PhysicalDisk(1)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (1). |
| `\PhysicalDisk(1)\Disk Writes/sec` | `__Role` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (1). |
| `\PhysicalDisk(10)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (10). |
| `\PhysicalDisk(10)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (10). |
| `\PhysicalDisk(10)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (10). |
| `\PhysicalDisk(10)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (10). |
| `\PhysicalDisk(11)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (11). |
| `\PhysicalDisk(11)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (11). |
| `\PhysicalDisk(11)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (11). |
| `\PhysicalDisk(11)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (11). |
| `\PhysicalDisk(12)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (12). |
| `\PhysicalDisk(12)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (12). |
| `\PhysicalDisk(12)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (12). |
| `\PhysicalDisk(12)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (12). |
| `\PhysicalDisk(13)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (13). |
| `\PhysicalDisk(13)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (13). |
| `\PhysicalDisk(13)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (13). |
| `\PhysicalDisk(13)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (13). |
| `\PhysicalDisk(14)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (14). |
| `\PhysicalDisk(14)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (14). |
| `\PhysicalDisk(14)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (14). |
| `\PhysicalDisk(14)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (14). |
| `\PhysicalDisk(15)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (15). |
| `\PhysicalDisk(15)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (15). |
| `\PhysicalDisk(15)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (15). |
| `\PhysicalDisk(15)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (15). |
| `\PhysicalDisk(16)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (16). |
| `\PhysicalDisk(16)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (16). |
| `\PhysicalDisk(16)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (16). |
| `\PhysicalDisk(16)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (16). |
| `\PhysicalDisk(17)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (17). |
| `\PhysicalDisk(17)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (17). |
| `\PhysicalDisk(17)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (17). |
| `\PhysicalDisk(17)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (17). |
| `\PhysicalDisk(18)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (18). |
| `\PhysicalDisk(18)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (18). |
| `\PhysicalDisk(18)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (18). |
| `\PhysicalDisk(18)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (18). |
| `\PhysicalDisk(19)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (19). |
| `\PhysicalDisk(19)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (19). |
| `\PhysicalDisk(19)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (19). |
| `\PhysicalDisk(19)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (19). |
| `\PhysicalDisk(2 C:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (2 C:). |
| `\PhysicalDisk(2 C:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (2 C:). |
| `\PhysicalDisk(2 C:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (2 C:). |
| `\PhysicalDisk(2 C:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (2 C:). |
| `\PhysicalDisk(2 D:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (2 D:). |
| `\PhysicalDisk(2 D:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (2 D:). |
| `\PhysicalDisk(2 D:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (2 D:). |
| `\PhysicalDisk(2 D:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (2 D:). |
| `\PhysicalDisk(2 Z:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (2 Z:). |
| `\PhysicalDisk(2 Z:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (2 Z:). |
| `\PhysicalDisk(2 Z:)\Disk Write Bytes/sec` | `Account` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (2 Z:). |
| `\PhysicalDisk(2 Z:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (2 Z:). |
| `\PhysicalDisk(2)\Disk Read Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (2). |
| `\PhysicalDisk(2)\Disk Reads/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (2). |
| `\PhysicalDisk(2)\Disk Write Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (2). |
| `\PhysicalDisk(2)\Disk Writes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (2). |
| `\PhysicalDisk(20)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (20). |
| `\PhysicalDisk(20)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (20). |
| `\PhysicalDisk(20)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (20). |
| `\PhysicalDisk(20)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (20). |
| `\PhysicalDisk(21)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (21). |
| `\PhysicalDisk(21)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (21). |
| `\PhysicalDisk(21)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (21). |
| `\PhysicalDisk(21)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (21). |
| `\PhysicalDisk(22)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (22). |
| `\PhysicalDisk(22)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (22). |
| `\PhysicalDisk(22)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (22). |
| `\PhysicalDisk(22)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (22). |
| `\PhysicalDisk(23)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (23). |
| `\PhysicalDisk(23)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (23). |
| `\PhysicalDisk(23)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (23). |
| `\PhysicalDisk(23)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (23). |
| `\PhysicalDisk(24)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (24). |
| `\PhysicalDisk(24)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (24). |
| `\PhysicalDisk(24)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (24). |
| `\PhysicalDisk(24)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (24). |
| `\PhysicalDisk(25)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (25). |
| `\PhysicalDisk(25)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (25). |
| `\PhysicalDisk(25)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (25). |
| `\PhysicalDisk(25)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (25). |
| `\PhysicalDisk(26)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (26). |
| `\PhysicalDisk(26)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (26). |
| `\PhysicalDisk(26)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (26). |
| `\PhysicalDisk(26)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (26). |
| `\PhysicalDisk(27)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (27). |
| `\PhysicalDisk(27)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (27). |
| `\PhysicalDisk(27)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (27). |
| `\PhysicalDisk(27)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (27). |
| `\PhysicalDisk(28)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (28). |
| `\PhysicalDisk(28)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (28). |
| `\PhysicalDisk(28)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (28). |
| `\PhysicalDisk(28)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (28). |
| `\PhysicalDisk(29)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (29). |
| `\PhysicalDisk(29)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (29). |
| `\PhysicalDisk(29)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (29). |
| `\PhysicalDisk(29)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (29). |
| `\PhysicalDisk(3 D:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (3 D:). |
| `\PhysicalDisk(3 D:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (3 D:). |
| `\PhysicalDisk(3 D:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (3 D:). |
| `\PhysicalDisk(3 D:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (3 D:). |
| `\PhysicalDisk(3 E:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (3 E:). |
| `\PhysicalDisk(3 E:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (3 E:). |
| `\PhysicalDisk(3 E:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (3 E:). |
| `\PhysicalDisk(3 E:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (3 E:). |
| `\PhysicalDisk(3 Z:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (3 Z:). |
| `\PhysicalDisk(3 Z:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (3 Z:). |
| `\PhysicalDisk(3 Z:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (3 Z:). |
| `\PhysicalDisk(3 Z:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (3 Z:). |
| `\PhysicalDisk(3)\Disk Read Bytes/sec` | `ResourceId` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (3). |
| `\PhysicalDisk(3)\Disk Reads/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (3). |
| `\PhysicalDisk(3)\Disk Write Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (3). |
| `\PhysicalDisk(3)\Disk Writes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (3). |
| `\PhysicalDisk(30)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (30). |
| `\PhysicalDisk(30)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (30). |
| `\PhysicalDisk(30)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (30). |
| `\PhysicalDisk(30)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (30). |
| `\PhysicalDisk(31)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (31). |
| `\PhysicalDisk(31)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (31). |
| `\PhysicalDisk(31)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (31). |
| `\PhysicalDisk(31)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (31). |
| `\PhysicalDisk(32)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (32). |
| `\PhysicalDisk(32)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (32). |
| `\PhysicalDisk(32)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (32). |
| `\PhysicalDisk(32)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (32). |
| `\PhysicalDisk(33)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (33). |
| `\PhysicalDisk(33)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (33). |
| `\PhysicalDisk(33)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (33). |
| `\PhysicalDisk(33)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (33). |
| `\PhysicalDisk(34 Z:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (34 Z:). |
| `\PhysicalDisk(34 Z:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (34 Z:). |
| `\PhysicalDisk(34 Z:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (34 Z:). |
| `\PhysicalDisk(34 Z:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (34 Z:). |
| `\PhysicalDisk(34)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (34). |
| `\PhysicalDisk(34)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (34). |
| `\PhysicalDisk(34)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (34). |
| `\PhysicalDisk(34)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (34). |
| `\PhysicalDisk(35 E:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (35 E:). |
| `\PhysicalDisk(35 E:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (35 E:). |
| `\PhysicalDisk(35 E:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (35 E:). |
| `\PhysicalDisk(35 E:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (35 E:). |
| `\PhysicalDisk(35 Z:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (35 Z:). |
| `\PhysicalDisk(35 Z:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (35 Z:). |
| `\PhysicalDisk(35 Z:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (35 Z:). |
| `\PhysicalDisk(35 Z:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (35 Z:). |
| `\PhysicalDisk(4 C:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (4 C:). |
| `\PhysicalDisk(4 C:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (4 C:). |
| `\PhysicalDisk(4 C:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (4 C:). |
| `\PhysicalDisk(4 C:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (4 C:). |
| `\PhysicalDisk(4 D:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (4 D:). |
| `\PhysicalDisk(4 D:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (4 D:). |
| `\PhysicalDisk(4 D:)\Disk Write Bytes/sec` | `Tenant` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (4 D:). |
| `\PhysicalDisk(4 D:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (4 D:). |
| `\PhysicalDisk(4 E:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (4 E:). |
| `\PhysicalDisk(4 E:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (4 E:). |
| `\PhysicalDisk(4 E:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (4 E:). |
| `\PhysicalDisk(4 E:)\Disk Writes/sec` | `Tenant` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (4 E:). |
| `\PhysicalDisk(4 F:)\Disk Read Bytes/sec` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (4 F:). |
| `\PhysicalDisk(4 F:)\Disk Reads/sec` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (4 F:). |
| `\PhysicalDisk(4 F:)\Disk Write Bytes/sec` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (4 F:). |
| `\PhysicalDisk(4 F:)\Disk Writes/sec` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (4 F:). |
| `\PhysicalDisk(4 Z:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (4 Z:). |
| `\PhysicalDisk(4 Z:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (4 Z:). |
| `\PhysicalDisk(4 Z:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (4 Z:). |
| `\PhysicalDisk(4 Z:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (4 Z:). |
| `\PhysicalDisk(4)\Disk Read Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (4). |
| `\PhysicalDisk(4)\Disk Reads/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (4). |
| `\PhysicalDisk(4)\Disk Write Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (4). |
| `\PhysicalDisk(4)\Disk Writes/sec` | `__Tenant` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (4). |
| `\PhysicalDisk(5 D:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (5 D:). |
| `\PhysicalDisk(5 D:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (5 D:). |
| `\PhysicalDisk(5 D:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (5 D:). |
| `\PhysicalDisk(5 D:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (5 D:). |
| `\PhysicalDisk(5 E:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (5 E:). |
| `\PhysicalDisk(5 E:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (5 E:). |
| `\PhysicalDisk(5 E:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (5 E:). |
| `\PhysicalDisk(5 E:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (5 E:). |
| `\PhysicalDisk(5 Z:)\Disk Read Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (5 Z:). |
| `\PhysicalDisk(5 Z:)\Disk Reads/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (5 Z:). |
| `\PhysicalDisk(5 Z:)\Disk Write Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (5 Z:). |
| `\PhysicalDisk(5 Z:)\Disk Writes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (5 Z:). |
| `\PhysicalDisk(5)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (5). |
| `\PhysicalDisk(5)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (5). |
| `\PhysicalDisk(5)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (5). |
| `\PhysicalDisk(5)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (5). |
| `\PhysicalDisk(6 D:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (6 D:). |
| `\PhysicalDisk(6 D:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (6 D:). |
| `\PhysicalDisk(6 D:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (6 D:). |
| `\PhysicalDisk(6 D:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (6 D:). |
| `\PhysicalDisk(6 E:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (6 E:). |
| `\PhysicalDisk(6 E:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (6 E:). |
| `\PhysicalDisk(6 E:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (6 E:). |
| `\PhysicalDisk(6 E:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (6 E:). |
| `\PhysicalDisk(6 Z:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (6 Z:). |
| `\PhysicalDisk(6 Z:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (6 Z:). |
| `\PhysicalDisk(6 Z:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (6 Z:). |
| `\PhysicalDisk(6 Z:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (6 Z:). |
| `\PhysicalDisk(6)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (6). |
| `\PhysicalDisk(6)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (6). |
| `\PhysicalDisk(6)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (6). |
| `\PhysicalDisk(6)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (6). |
| `\PhysicalDisk(7 E:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (7 E:). |
| `\PhysicalDisk(7 E:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (7 E:). |
| `\PhysicalDisk(7 E:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (7 E:). |
| `\PhysicalDisk(7 E:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (7 E:). |
| `\PhysicalDisk(7 Z:)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (7 Z:). |
| `\PhysicalDisk(7 Z:)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (7 Z:). |
| `\PhysicalDisk(7 Z:)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (7 Z:). |
| `\PhysicalDisk(7 Z:)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (7 Z:). |
| `\PhysicalDisk(7)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (7). |
| `\PhysicalDisk(7)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (7). |
| `\PhysicalDisk(7)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (7). |
| `\PhysicalDisk(7)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (7). |
| `\PhysicalDisk(8)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (8). |
| `\PhysicalDisk(8)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (8). |
| `\PhysicalDisk(8)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (8). |
| `\PhysicalDisk(8)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (8). |
| `\PhysicalDisk(9)\Disk Read Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (9). |
| `\PhysicalDisk(9)\Disk Reads/sec` | `(none)` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (9). |
| `\PhysicalDisk(9)\Disk Write Bytes/sec` | `(none)` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (9). |
| `\PhysicalDisk(9)\Disk Writes/sec` | `(none)` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (9). |
| `\PhysicalDisk(_Total)\Disk Read Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk read bytes/sec on Physical Disk (_Total). |
| `\PhysicalDisk(_Total)\Disk Reads/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk reads/sec on Physical Disk (_Total). |
| `\PhysicalDisk(_Total)\Disk Write Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk write bytes/sec on Physical Disk (_Total). |
| `\PhysicalDisk(_Total)\Disk Writes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for disk writes/sec on Physical Disk (_Total). |
| `\Process(Kusto.WinSvc.Svc)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Process (Kusto.WinSvc.Svc). |
| `\Process(Kusto.WinSvc.Svc)\Pool Nonpaged Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for pool nonpaged bytes on Process (Kusto.WinSvc.Svc). |
| `\Process(Kusto.WinSvc.Svc)\Pool Paged Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for pool paged bytes on Process (Kusto.WinSvc.Svc). |
| `\Process(Kusto.WinSvc.Svc)\Private Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for private bytes on Process (Kusto.WinSvc.Svc). |
| `\Process(Kusto.WinSvc.Svc)\Thread Count` | `Cluster^DataCenter^RoleInstance` | Windows/Geneva performance counter for thread count on Process (Kusto.WinSvc.Svc). |
| `\Process(Kusto.WinSvc.Svc)\Working Set` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set on Process (Kusto.WinSvc.Svc). |
| `\Process(Kusto.WinSvc.Svc)\Working Set - Private` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set - private on Process (Kusto.WinSvc.Svc). |
| `\Process(Kusto.WinSvc.Svc)\Working Set Peak` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set peak on Process (Kusto.WinSvc.Svc). |
| `\Processor(0)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (0). |
| `\Processor(0)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (0). |
| `\Processor(1)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (1). |
| `\Processor(1)\% Processor Time` | `RoleInstance` | Windows/Geneva performance counter for % processor time on Processor (1). |
| `\Processor(10)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (10). |
| `\Processor(10)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (10). |
| `\Processor(11)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (11). |
| `\Processor(11)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (11). |
| `\Processor(12)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (12). |
| `\Processor(12)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (12). |
| `\Processor(13)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (13). |
| `\Processor(13)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (13). |
| `\Processor(14)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (14). |
| `\Processor(14)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (14). |
| `\Processor(15)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (15). |
| `\Processor(15)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (15). |
| `\Processor(16)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (16). |
| `\Processor(16)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (16). |
| `\Processor(17)\% DPC Time` | `DataCenter` | Windows/Geneva performance counter for % dpc time on Processor (17). |
| `\Processor(17)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (17). |
| `\Processor(18)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (18). |
| `\Processor(18)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (18). |
| `\Processor(19)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (19). |
| `\Processor(19)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (19). |
| `\Processor(2)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (2). |
| `\Processor(2)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (2). |
| `\Processor(20)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (20). |
| `\Processor(20)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (20). |
| `\Processor(21)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (21). |
| `\Processor(21)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (21). |
| `\Processor(22)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (22). |
| `\Processor(22)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (22). |
| `\Processor(23)\% DPC Time` | `__Tenant` | Windows/Geneva performance counter for % dpc time on Processor (23). |
| `\Processor(23)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (23). |
| `\Processor(24)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (24). |
| `\Processor(24)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (24). |
| `\Processor(25)\% DPC Time` | `DataCenter` | Windows/Geneva performance counter for % dpc time on Processor (25). |
| `\Processor(25)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (25). |
| `\Processor(26)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (26). |
| `\Processor(26)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (26). |
| `\Processor(27)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (27). |
| `\Processor(27)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (27). |
| `\Processor(28)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (28). |
| `\Processor(28)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (28). |
| `\Processor(29)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (29). |
| `\Processor(29)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (29). |
| `\Processor(3)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (3). |
| `\Processor(3)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (3). |
| `\Processor(30)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (30). |
| `\Processor(30)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (30). |
| `\Processor(31)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (31). |
| `\Processor(31)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (31). |
| `\Processor(32)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (32). |
| `\Processor(32)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (32). |
| `\Processor(33)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (33). |
| `\Processor(33)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (33). |
| `\Processor(34)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (34). |
| `\Processor(34)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (34). |
| `\Processor(35)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (35). |
| `\Processor(35)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (35). |
| `\Processor(36)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (36). |
| `\Processor(36)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (36). |
| `\Processor(37)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (37). |
| `\Processor(37)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (37). |
| `\Processor(38)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (38). |
| `\Processor(38)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (38). |
| `\Processor(39)\% DPC Time` | `(none)` | Windows/Geneva performance counter for % dpc time on Processor (39). |
| `\Processor(39)\% Processor Time` | `(none)` | Windows/Geneva performance counter for % processor time on Processor (39). |
| `\Processor(4)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (4). |
| `\Processor(4)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (4). |
| `\Processor(5)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (5). |
| `\Processor(5)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (5). |
| `\Processor(6)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (6). |
| `\Processor(6)\% Processor Time` | `CloudName` | Windows/Geneva performance counter for % processor time on Processor (6). |
| `\Processor(7)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (7). |
| `\Processor(7)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (7). |
| `\Processor(8)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (8). |
| `\Processor(8)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (8). |
| `\Processor(9)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (9). |
| `\Processor(9)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (9). |
| `\Processor(_Total)\% DPC Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % dpc time on Processor (_Total). |
| `\Processor(_Total)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (_Total). |
| `\TCPv4\Connection Failures` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connection failures on TCPv4. |
| `\TCPv4\Connections Active` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connections active on TCPv4. |
| `\TCPv4\Connections Established` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connections established on TCPv4. |
| `\TCPv4\Connections Passive` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for connections passive on TCPv4. |
| `\TCPv4\Connections Reset` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for connections reset on TCPv4. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dotnet.jit.compiled_methods` | `(none)` | Likely measures dotnet jit compiled methods. |
| `dotnet.monitor.lock_contentions` | `(none)` | Likely measures dotnet monitor lock contentions. |
| `http.client.open_connections` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.connection.state^network.peer.address^network.protocol.version^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely measures http client open connections. |
| `process.runtime.dotnet.jit.compilation_time` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures process runtime dotnet jit compilation time. |

#### `MdmEngineMetrics` (140 metrics)

Curated MDM engine metrics for extents, ingestion, query acceleration, cache, continuous export, and cluster data capacity.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IsRowStoreUnhealthy` | `ResourceId` | Health or availability signal for is row store unhealthy. |
| `MaterializedViewHealth` | `Account^Cluster^Database^DataCenter^MaterializedViewName^ResourceId^VirtualClusterName` | Likely measures storage layout or data-management work for materialized view health. |
| `QueryAccelerationCatalogStaleWithHealthyState` | `Cluster^DataCenter^ExternalTable^VirtualClusterName` | Health or availability signal for query acceleration catalog stale with healthy state. |
| `UnavailableDatabases` | `Account^Cluster^Database^DataCenter^Reason` | Likely measures storage layout or data-management work for unavailable databases. |

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `AllPartitionedRecordsPercentage` | `Cluster^Database^DataCenter^ResourceId^Table` | Likely measures latency or duration for all partitioned records percentage. |
| `ContinuousExportDurationSeconds` | `Account^Cluster^ContinuousExportName^Database^DataCenter^ResourceId^Result^VirtualClusterName` | Likely measures latency or duration for continuous export duration seconds. |
| `ContinuousExportLatencyMinutes` | `Account^Cluster^ContinuousExportName^Database^DataCenter^ErrorCode^IsErrorPermanent^ResourceId^VirtualClusterName` | Likely measures latency or duration for continuous export latency minutes. |
| `ContinuousMaterializedViewDurationSeconds` | `Account^Cluster^ContinuousMaterializedViewName^Database^DataCenter^Result` | Likely measures latency or duration for continuous materialized view duration seconds. |
| `ContinuousMaterializedViewLatencyMinutes` | `Account^CloudName^Cluster^ContinuousMaterializedViewName^Database^DataCenter^DeploymentRing^ErrorCode^IsErrorPermanent^ResourceId^VirtualClusterName` | Likely measures latency or duration for continuous materialized view latency minutes. |
| `DatabasesLoadingDurationInSeconds` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures latency or duration for databases loading duration in seconds. |
| `FabricStorageSuccessfulReport` | `DataCenter^VirtualClusterName` | Likely measures latency or duration for fabric storage successful report. |
| `FollowerFullRefreshDurationMs` | `Account^Cluster^DataCenter^ResourceId^RoleInstance^State` | Likely measures latency or duration for follower full refresh duration ms. |
| `HotDataDiskSpaceUsage` | `ResourceId` | Likely measures latency or duration for hot data disk space usage. |
| `HotPartitionedRecordsPercentage` | `Cluster^Database^DataCenter^ResourceId^Table` | Likely measures latency or duration for hot partitioned records percentage. |
| `IngestCommandDuration` | `Account^Cluster^Database^DataCenter` | Likely measures latency or duration for ingest command duration. |
| `IngestCommandNumberOfStreams` | `Account^CloudName^Cluster^Database^DataCenter^DeploymentRing^ResourceId^Table^VirtualClusterName` | Likely measures latency or duration for ingest command number of streams. |
| `MaterializedViewAgeMinutes` | `Account^Cluster^Database^DataCenter^MaterializedViewName^ResourceId^VirtualClusterName` | Likely measures latency or duration for materialized view age minutes. |
| `MaterializedViewAgeSeconds` | `Account^Cluster^Database^DataCenter^MaterializedViewName^ResourceId` | Likely measures latency or duration for materialized view age seconds. |
| `MinPartitioningPercentageInSingleTable` | `ResourceId` | Likely measures latency or duration for min partitioning percentage in single table. |
| `MirroringDurationSeconds` | `Account^Cluster^DataCenter^MirroringName^Result^VirtualClusterName` | Likely measures latency or duration for mirroring duration seconds. |
| `MirroringLatencyMinutes` | `Cluster^Database^DataCenter^ErrorCode^MirroringName^VirtualClusterName` | Likely measures latency or duration for mirroring latency minutes. |
| `PurgeDuration` | `Account^Cluster^DeploymentRing` | Likely measures latency or duration for purge duration. |
| `QueryAccelerationCatalogAgeMinutes` | `Account^Cluster^Database^DataCenter^ExternalTable^VirtualClusterName` | Likely measures latency or duration for query acceleration catalog age minutes. |
| `QueryAccelerationCompletePercentage` | `Account^Cluster^Database^DataCenter^ExternalTable^VirtualClusterName` | Likely measures latency or duration for query acceleration complete percentage. |
| `RowStoreLocalStorageCapacityFactor` | `ResourceId` | Likely measures latency or duration for row store local storage capacity factor. |
| `ShardsMergeBatchesCalculationDurationMs` | `ResourceId` | Likely measures latency or duration for shards merge batches calculation duration ms. |
| `ShardsPartitioningBatchesCalculationDurationMs` | `ResourceId` | Likely measures latency or duration for shards partitioning batches calculation duration ms. |
| `StorageArtifactsCleanupOperationResult` | `Account^Cluster^Database^OperationType` | Likely measures latency or duration for storage artifacts cleanup operation result. |
| `WeakConsistencySnapshotLatencySeconds` | `Account^Cluster^Database^DataCenter^ResourceId^RoleInstance` | Likely measures latency or duration for weak consistency snapshot latency seconds. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ActiveServiceInstances` | `Cluster^DataCenter^DeploymentRing^RoleInstance^ServiceType` | Count of active service instances reporting for the component. |
| `FabricServiceInstancesActive` | `Account^Cluster^DataCenter^Service` | Likely counts the current amount of fabric service instances active. |
| `HosterTargetNumberOfNodes` | `ResourceId` | Likely counts the current amount of hoster target number of nodes. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ClusterDataCapacityFactor` | `ResourceId` | Likely tracks resource usage or capacity for cluster data capacity factor. |
| `GraphSnapshotsLoadFactor` | `ResourceId` | Likely tracks resource usage or capacity for graph snapshots load factor. |
| `InstancesTargetBasedOnDataCapacity` | `ResourceId` | Likely tracks resource usage or capacity for instances target based on data capacity. |
| `RequestQuotaExceeded` | `(none)` | Likely tracks resource usage or capacity for request quota exceeded. |
| `V3DataCapacityFactor` | `ResourceId` | Likely tracks resource usage or capacity for v3 data capacity factor. |
| `VirtualClusterProcessMemoryLimitHit` | `Cluster^DataCenter^VirtualClusterName` | Likely tracks resource usage or capacity for virtual cluster process memory limit hit. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ContinuousExportSizeInBytesArtifactsExported` | `Account^Cluster^ContinuousExportName^Database^DataCenter^VirtualClusterName` | Likely measures size, volume, or throughput for continuous export size in bytes artifacts exported. |
| `DbMetadataSizeBytes` | `Account^Cluster^Database^DataCenter` | Likely measures size, volume, or throughput for db metadata size bytes. |
| `DbObjectsSizeBytes` | `Account^Cluster^Database^DataCenter` | Likely measures size, volume, or throughput for db objects size bytes. |
| `ExtentsSize` | `ResourceId^StorageKind^Caching` | Total size of extents for the selected scope or tier. |
| `HotCacheSizeInBytes` | `Cluster^DataCenter^VirtualClusterName` | Size of hot cache data kept readily available on the cluster. |
| `IngestCommandExtentsSizeInBytes` | `Account^Cluster^ResourceId` | Likely measures size, volume, or throughput for ingest command extents size in bytes. |
| `IngestCommandOriginalSizeInBytes` | `Account^Cluster^Database^ResourceId` | Likely measures size, volume, or throughput for ingest command original size in bytes. |
| `StoredQueryResultSizeBytes` | `(none)` | Likely measures size, volume, or throughput for stored query result size bytes. |
| `TotalExtentSize` | `ResourceId` | Combined size of all extents in the selected scope. |
| `TotalOriginalDataSize` | `ResourceId` | Likely measures size, volume, or throughput for total original data size. |

##### Query & cache

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `QueryAccelerationCapacityUtilization` | `ResourceId` | Likely tracks resource usage or capacity for query acceleration capacity utilization. |
| `QueryAccelerationCapacityUtilizationInt` | `Cluster^DataCenter^VirtualClusterName` | Likely tracks resource usage or capacity for query acceleration capacity utilization int. |
| `QueryAccelerationIntegrityIssue` | `(none)` | Likely measures query or cache behavior for query acceleration integrity issue. |
| `QueryAccelerationNumberOfArtifactsPendingCaching` | `Account^Cluster^Database^ExternalTable^VirtualClusterName` | Likely counts the current amount of query acceleration number of artifacts pending caching. |
| `QueryAccelerationOperationsInProgress` | `ResourceId` | Likely counts the current amount of query acceleration operations in progress. |
| `QueryAccelerationOperationsLoadFactor` | `ResourceId` | Likely tracks resource usage or capacity for query acceleration operations load factor. |
| `StoredQueryResultRowsCount` | `(none)` | Likely counts the current amount of stored query result rows count. |
| `StoredQueryResultsInProgress` | `ResourceId` | Likely measures query or cache behavior for stored query results in progress. |

##### Ingestion pipeline

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IngestCommandNumberOfExtents` | `Account^Cluster^DataCenter` | Likely counts the current amount of ingest command number of extents. |
| `IngestCommandRowsCount` | `Account^Cluster` | Likely counts the current amount of ingest command rows count. |
| `IngestionCapacityUtilization` | `ResourceId` | Likely tracks resource usage or capacity for ingestion capacity utilization. |
| `IngestionCapacityUtilizationInt` | `Cluster^DataCenter^VirtualClusterName` | Likely tracks resource usage or capacity for ingestion capacity utilization int. |
| `IngestionResult` | `Account^Cluster^DataCenter^DeploymentRing^FailureKind^IngestionErrorCode^IngestionResultDetails^ResourceId^VirtualClusterName` | Likely measures ingestion pipeline behavior for ingestion result. |
| `IngestionsInProgress` | `ResourceId` | Likely measures ingestion pipeline behavior for ingestions in progress. |
| `IngestionsLoadFactor` | `ResourceId` | Likely tracks resource usage or capacity for ingestions load factor. |
| `IngestionsSuccessRate` | `ResourceId` | Success-rate metric for ingestions success rate. |
| `RowStoreSealsInProgress` | `ResourceId` | Likely measures ingestion pipeline behavior for row store seals in progress. |
| `ShardsMergeShardsCountPerBatch` | `ResourceId` | Likely counts the current amount of shards merge shards count per batch. |
| `ShardsPartitioningShardsCountPerBatch` | `ResourceId` | Likely counts the current amount of shards partitioning shards count per batch. |

##### Data layout & storage

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ContinuousExportDataLoss` | `(none)` | Likely measures storage layout or data-management work for continuous export data loss. |
| `ContinuousExportNumArtifactsExported` | `Account^Cluster^ContinuousExportName^Database^DataCenter^VirtualClusterName` | Likely measures storage layout or data-management work for continuous export num artifacts exported. |
| `ContinuousExportNumRecordsExported` | `Account^Cluster^ContinuousExportName^Database^DataCenter^ResourceId` | Likely measures storage layout or data-management work for continuous export num records exported. |
| `ContinuousExportResult` | `Account^Cluster^ContinuousExportName^Database^DataCenter^ErrorCode^IsErrorPermanent^ResourceId^Result^VirtualClusterName` | Likely measures storage layout or data-management work for continuous export result. |
| `ContinuousExportScopePeriodMinutes` | `Account^Cluster^ContinuousExportName^Database^DataCenter^ResourceId` | Likely measures storage layout or data-management work for continuous export scope period minutes. |
| `ContinuousMaterializedViewResult` | `Account^Cluster^ContinuousMaterializedViewName^Database^DataCenter^Result` | Likely measures storage layout or data-management work for continuous materialized view result. |
| `ContinuousMaterializedViewScopePeriodMinutes` | `Account^Cluster^ContinuousMaterializedViewName^Database^DataCenter` | Likely measures storage layout or data-management work for continuous materialized view scope period minutes. |
| `DataPartitioningLoadFactor` | `ResourceId` | Likely tracks resource usage or capacity for data partitioning load factor. |
| `DataPartitioningOperationsInProgress` | `ResourceId` | Likely counts the current amount of data partitioning operations in progress. |
| `ExportsInProgress` | `ResourceId` | Likely measures storage layout or data-management work for exports in progress. |
| `ExportsLoadFactor` | `ResourceId` | Likely tracks resource usage or capacity for exports load factor. |
| `ExtendedExtentsTotal` | `ResourceId` | Likely measures storage layout or data-management work for extended extents total. |
| `ExtentsCount` | `ResourceId^StorageKind^Caching` | Count of extents for the selected scope or tier. |
| `ExtentsTotal` | `ResourceId` | Total number of extents across the selected scope. |
| `MaterializedViewDataLoss` | `Account^Cluster^Database^DataCenter^Kind^MaterializedViewName^ResourceId` | Likely measures storage layout or data-management work for materialized view data loss. |
| `MaterializedViewDuplicates` | `(none)` | Likely measures storage layout or data-management work for materialized view duplicates. |
| `MaterializedViewExtentsRebuild` | `Account^Cluster^Database^DataCenter^MaterializedViewName^ResourceId^VirtualClusterName` | Likely measures storage layout or data-management work for materialized view extents rebuild. |
| `MaterializedViewRecordsInDelta` | `Account^Cluster^Database^DataCenter^MaterializedViewName^ResourceId` | Likely measures storage layout or data-management work for materialized view records in delta. |
| `MaterializedViewResult` | `Account^Cluster^Database^DataCenter^MaterializedViewName^ResourceId^Result^VirtualClusterName` | Likely measures storage layout or data-management work for materialized view result. |
| `MaterializedViewsInProgress` | `ResourceId` | Likely measures storage layout or data-management work for materialized views in progress. |
| `MaterializedViewsLoadFactor` | `ResourceId` | Likely tracks resource usage or capacity for materialized views load factor. |
| `MaterializedViewsTrigger` | `Account^Cluster^DataCenter^ResourceId` | Likely measures storage layout or data-management work for materialized views trigger. |
| `MaxContinuousExportLatenessMinutes` | `ResourceId` | Likely measures storage layout or data-management work for max continuous export lateness minutes. |
| `MaxMirroringPolicyJobsLatenessMinutes` | `ResourceId` | Likely counts the current amount of max mirroring policy jobs lateness minutes. |
| `MergesInProgress` | `ResourceId` | Likely measures storage layout or data-management work for merges in progress. |
| `MergesLoadFactor` | `ResourceId` | Likely tracks resource usage or capacity for merges load factor. |
| `MergesSuccessRate` | `ResourceId` | Success-rate metric for merges success rate. |
| `MirroringOperationsInProgress` | `ResourceId` | Likely counts the current amount of mirroring operations in progress. |
| `MirroringOperationsLoadFactor` | `ResourceId` | Likely tracks resource usage or capacity for mirroring operations load factor. |
| `MirroringResult` | `Cluster^Database^DataCenter^ErrorCode^IsErrorPermanent^MirroringName^Result^VirtualClusterName` | Likely measures storage layout or data-management work for mirroring result. |
| `MirroringScopePeriodMinutes` | `Cluster^Database^DataCenter^MirroringName^VirtualClusterName` | Likely measures storage layout or data-management work for mirroring scope period minutes. |
| `NumberOfDatabases` | `ResourceId` | Likely counts the current amount of number of databases. |
| `PartitionedRecords` | `Cluster^Database^DataCenter^ResourceId^Table` | Likely measures storage layout or data-management work for partitioned records. |
| `PartitionedShards` | `Cluster^Database^DataCenter^Table` | Likely measures storage layout or data-management work for partitioned shards. |
| `PendingContinuousExports` | `ResourceId` | Likely tracks resource usage or capacity for pending continuous exports. |
| `PendingMirroringPolicyJobs` | `ResourceId` | Likely counts the current amount of pending mirroring policy jobs. |
| `PurgeExtentsRebuildInProgress` | `ResourceId` | Likely measures storage layout or data-management work for purge extents rebuild in progress. |
| `PurgeExtentsRebuildLoadFactor` | `ResourceId` | Likely tracks resource usage or capacity for purge extents rebuild load factor. |
| `PurgeExtentsRebuiltCount` | `Table` | Likely counts the current amount of purge extents rebuilt count. |
| `PurgesInProgress` | `ResourceId` | Likely measures storage layout or data-management work for purges in progress. |
| `ShardsMergeCapacityPerNode` | `ResourceId` | Likely tracks resource usage or capacity for shards merge capacity per node. |
| `ShardsMergeConcurrentOperationsCount` | `Cluster^DataCenter` | Likely counts the current amount of shards merge concurrent operations count. |
| `ShardsMergeDryRunPendingOperationsCount` | `ResourceId` | Likely counts the current amount of shards merge dry run pending operations count. |
| `ShardsMergeDryRunPendingShardsCount` | `ResourceId` | Likely counts the current amount of shards merge dry run pending shards count. |
| `ShardsMergePendingOperationsCount` | `ResourceId` | Likely counts the current amount of shards merge pending operations count. |
| `ShardsMergePendingShardsCount` | `ResourceId` | Likely counts the current amount of shards merge pending shards count. |
| `ShardsPartitioningClusterCapacity` | `ResourceId` | Likely tracks resource usage or capacity for shards partitioning cluster capacity. |
| `ShardsPartitioningDryRunPendingOperationsCount` | `ResourceId` | Likely counts the current amount of shards partitioning dry run pending operations count. |
| `ShardsPartitioningDryRunPendingShardsCount` | `ResourceId` | Likely counts the current amount of shards partitioning dry run pending shards count. |
| `ShardsPartitioningPendingOperationsCount` | `ResourceId` | Likely counts the current amount of shards partitioning pending operations count. |
| `ShardsPartitioningPendingShardsCount` | `ResourceId` | Likely counts the current amount of shards partitioning pending shards count. |
| `ShardsWarmingTemperature` | `ResourceId` | Likely measures storage layout or data-management work for shards warming temperature. |
| `StalePurgeCleanup` | `Account^Cluster` | Likely measures storage layout or data-management work for stale purge cleanup. |
| `SuspendedDatabases` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^Reason^ResourceId^VirtualClusterName` | Likely measures storage layout or data-management work for suspended databases. |
| `V11DatabasesEquivalenceWithV10` | `(none)` | Likely measures storage layout or data-management work for v11 databases equivalence with v10. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `CorruptedShardsCount` | `Cluster^Database^DataCenter^DeploymentRing` | Likely counts errors, failures, or throttling for corrupted shards count. |
| `LowMemoryFailure` | `Cluster^DataCenter^VirtualClusterName` | Likely counts errors, failures, or throttling for low memory failure. |
| `QueryAccelerationCorruptedShardsCount` | `Cluster^DataCenter^ExternalTable^VirtualClusterName` | Likely counts errors, failures, or throttling for query acceleration corrupted shards count. |
| `QueryAccelerationUnexpectedErrorInCachedTableRefresh` | `Cluster^DataCenter^VirtualClusterName` | Likely counts errors, failures, or throttling for query acceleration unexpected error in cached table refresh. |
| `QueryAccelerationUnexpectedErrorInCatalogRefresh` | `Cluster^DataCenter^VirtualClusterName` | Likely counts errors, failures, or throttling for query acceleration unexpected error in catalog refresh. |
| `QueryAccelerationUnexpectedErrorInShardsDrop` | `Cluster^DataCenter^VirtualClusterName` | Likely counts errors, failures, or throttling for query acceleration unexpected error in shards drop. |
| `UpdatePolicyFailure` | `Cluster^DataCenter^DeploymentRing^IsTransactional^ResourceId` | Likely counts errors, failures, or throttling for update policy failure. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ExternalThrottling` | `Cluster^DataCenter^Kind^VirtualClusterName` | Likely measures external throttling. |
| `FabricActivitySuccessfulReport` | `DataCenter^VirtualClusterName` | Likely measures fabric activity successful report. |
| `FabricServiceInstancesRequested` | `Account^Cluster^DataCenter^ResourceId^Service` | Likely measures fabric service instances requested. |
| `GraphSnapshotCompletionResult` | `CloudName` | Likely measures graph snapshot completion result. |
| `GraphSnapshotsInProgress` | `ResourceId` | Likely measures graph snapshots in progress. |
| `GuestRemainingFreeSpace` | `Cluster^DataCenter^DiskCacheSizeInBytes^VirtualClusterName` | Likely measures guest remaining free space. |
| `MachinesOffline` | `ResourceId` | Likely measures machines offline. |
| `MachinesOnline` | `Cluster^DataCenter` | Likely measures machines online. |
| `MachinesTotal` | `ResourceId` | Likely measures machines total. |
| `ServiceLevelObjective` | `ResourceId` | Likely measures service level objective. |
| `StuckQueries` | `Cluster^DataCenter^VirtualClusterName` | Likely measures stuck queries. |

#### `MdmEngineHosterMetrics` (5 metrics)

Virtual-cluster hoster metrics for engine-hosted tenants, startup, and hoster state.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `VirtualClusterSelfSanity` | `Response^VirtualClusterName` | Likely measures virtual cluster self sanity. |

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `VirtualClusterStartupDurationMs` | `Cluster^DataCenter^RoleInstance^State` | Likely measures latency or duration for virtual cluster startup duration ms. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `NumberOfCalls` | `CallType^Cluster^DataCenter^DeploymentRing^ErrorCode^ErrorSubCode^RoleInstance^VirtualClusterName` | Likely counts the current amount of number of calls. |
| `NumberOfVirtualClusters` | `Cluster^DataCenter^RoleInstance^State` | Likely counts the current amount of number of virtual clusters. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `VirtualClusterState` | `Cluster^DataCenter^State^VirtualClusterName` | Likely measures virtual cluster state. |

### Data Management Metrics

Ingestion orchestration, batching, request handling, queues, and DM hoster behavior.

#### `dmMetrics` (181 metrics)

Legacy/raw data-management service metrics and runtime counters for ingestion, queues, outbound calls, and process health.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dns.lookup.duration` | `Cluster^DataCenter^dns.question.name^VirtualClusterName` | Likely measures latency or duration for dns lookup duration. |
| `http.client.connection.duration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^network.protocol.version^ResourceId^server.address^server.port^url.scheme^VirtualClusterName` | Likely measures latency or duration for http client connection duration. |
| `http.client.request.duration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.request.method^http.response.status_code^network.protocol.version^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely measures latency or duration for http client request duration. |
| `process.runtime.dotnet.gc.duration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures latency or duration for process runtime dotnet gc duration. |
| `process.runtime.dotnet.thread_pool.completed_items.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures latency or duration for process runtime dotnet thread pool completed items count. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dotnet.assembly.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of dotnet assembly count. |
| `dotnet.thread_pool.queue.length` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of dotnet thread pool queue length. |
| `dotnet.thread_pool.thread.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of dotnet thread pool thread count. |
| `dotnet.thread_pool.work_item.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of dotnet thread pool work item count. |
| `dotnet.timer.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of dotnet timer count. |
| `http.client.active_requests` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.request.method^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely counts the current amount of http client active requests. |
| `http.client.request.time_in_queue` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.request.method^network.protocol.version^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely counts the current amount of http client request time in queue. |
| `process.runtime.dotnet.assemblies.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet assemblies count. |
| `process.runtime.dotnet.jit.methods_compiled.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet jit methods compiled count. |
| `process.runtime.dotnet.monitor.lock_contention.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet monitor lock contention count. |
| `process.runtime.dotnet.thread_pool.queue.length` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet thread pool queue length. |
| `process.runtime.dotnet.thread_pool.threads.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet thread pool threads count. |
| `process.runtime.dotnet.timer.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet timer count. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dotnet.gc.collections` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^gc.heap.generation^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for dotnet gc collections. |
| `dotnet.gc.heap.total_allocated` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for dotnet gc heap total allocated. |
| `dotnet.gc.pause.time` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for dotnet gc pause time. |
| `dotnet.process.cpu.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of dotnet process cpu count. |
| `dotnet.process.cpu.time` | `Account^CloudName^Cluster^cpu.mode^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for dotnet process cpu time. |
| `dotnet.process.memory.working_set` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for dotnet process memory working set. |
| `process.runtime.dotnet.gc.collections.count` | `Cluster^DataCenter` | Likely counts the current amount of process runtime dotnet gc collections count. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dotnet.gc.last_collection.heap.fragmentation.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^gc.heap.generation^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for dotnet gc last collection heap fragmentation size. |
| `dotnet.gc.last_collection.heap.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^gc.heap.generation^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for dotnet gc last collection heap size. |
| `dotnet.gc.last_collection.memory.committed_size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for dotnet gc last collection memory committed size. |
| `dotnet.jit.compiled_il.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for dotnet jit compiled il size. |
| `process.runtime.dotnet.gc.allocations.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc allocations size. |
| `process.runtime.dotnet.gc.committed_memory.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc committed memory size. |
| `process.runtime.dotnet.gc.heap.fragmentation.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^generation^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc heap fragmentation size. |
| `process.runtime.dotnet.gc.heap.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^generation^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc heap size. |
| `process.runtime.dotnet.gc.objects.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc objects size. |
| `process.runtime.dotnet.jit.il_compiled.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet jit il compiled size. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dotnet.exceptions` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^error.type^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for dotnet exceptions. |
| `process.runtime.dotnet.exceptions.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for process runtime dotnet exceptions count. |

##### Windows / .NET perf counters

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `\.NET CLR Memory(Kusto.WinSvc.DM.Svc)\# Bytes in all Heaps` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for # bytes in all heaps on NET CLR Memory (Kusto.WinSvc.DM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.DM.Svc)\# Total committed Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for # total committed bytes on NET CLR Memory (Kusto.WinSvc.DM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.DM.Svc)\% Time in GC` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % time in gc on NET CLR Memory (Kusto.WinSvc.DM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.DM.Svc)\Allocated Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for allocated bytes/sec on NET CLR Memory (Kusto.WinSvc.DM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.DM.Svc)\Gen 0 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 0 heap size on NET CLR Memory (Kusto.WinSvc.DM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.DM.Svc)\Gen 1 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 1 heap size on NET CLR Memory (Kusto.WinSvc.DM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.DM.Svc)\Gen 2 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 2 heap size on NET CLR Memory (Kusto.WinSvc.DM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.DM.Svc)\Large Object Heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for large object heap size on NET CLR Memory (Kusto.WinSvc.DM.Svc). |
| `\LogicalDisk(_Total)\% Free Space` | `Cluster^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Read Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Write Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Current Disk Queue Length` | `Account^Cluster^DataCenter` | Windows/Geneva performance counter for current disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(C:)\% Free Space` | `Cluster^RoleInstance` | Windows/Geneva performance counter for % free space on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (C:). |
| `\LogicalDisk(D:)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (D:). |
| `\LogicalDisk(HarddiskVolume1)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume2)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume3)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume4)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume4). |
| `\LogicalDisk(HarddiskVolume4)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume4). |
| `\LogicalDisk(HarddiskVolume4)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume4). |
| `\LogicalDisk(HarddiskVolume4)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume4). |
| `\LogicalDisk(HarddiskVolume4)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume4). |
| `\LogicalDisk(HarddiskVolume5)\% Free Space` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume5). |
| `\LogicalDisk(HarddiskVolume5)\Avg. Disk Queue Length` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume5). |
| `\LogicalDisk(HarddiskVolume5)\Avg. Disk Read Queue Length` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume5). |
| `\LogicalDisk(HarddiskVolume5)\Avg. Disk Write Queue Length` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume5). |
| `\LogicalDisk(HarddiskVolume5)\Current Disk Queue Length` | `Not observed in sampled dimension extracts` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume5). |
| `\LogicalDisk(HarddiskVolume6)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume6). |
| `\LogicalDisk(HarddiskVolume6)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume6). |
| `\LogicalDisk(HarddiskVolume6)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume6). |
| `\LogicalDisk(HarddiskVolume6)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume6). |
| `\LogicalDisk(HarddiskVolume6)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume6). |
| `\Memory\Available Bytes` | `Account^CloudName^Cluster^DataCenter^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for available bytes on Memory. |
| `\Network Adapter(Microsoft Hyper-V Network Adapter _2)\Bytes Received/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes received/sec on Network Adapter (Microsoft Hyper-V Network Adapter _2). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter _2)\Bytes Sent/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes sent/sec on Network Adapter (Microsoft Hyper-V Network Adapter _2). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Received/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes received/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Sent/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes sent/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Process(Kusto.WinSvc.DM.Svc)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Process (Kusto.WinSvc.DM.Svc). |
| `\Process(Kusto.WinSvc.DM.Svc)\Pool Nonpaged Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for pool nonpaged bytes on Process (Kusto.WinSvc.DM.Svc). |
| `\Process(Kusto.WinSvc.DM.Svc)\Pool Paged Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for pool paged bytes on Process (Kusto.WinSvc.DM.Svc). |
| `\Process(Kusto.WinSvc.DM.Svc)\Private Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for private bytes on Process (Kusto.WinSvc.DM.Svc). |
| `\Process(Kusto.WinSvc.DM.Svc)\Thread Count` | `Account^Cluster^DataCenter^RoleInstance` | Windows/Geneva performance counter for thread count on Process (Kusto.WinSvc.DM.Svc). |
| `\Process(Kusto.WinSvc.DM.Svc)\Working Set` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for working set on Process (Kusto.WinSvc.DM.Svc). |
| `\Process(Kusto.WinSvc.DM.Svc)\Working Set - Private` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set - private on Process (Kusto.WinSvc.DM.Svc). |
| `\Process(Kusto.WinSvc.DM.Svc)\Working Set Peak` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set peak on Process (Kusto.WinSvc.DM.Svc). |
| `\Processor(0)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (0). |
| `\Processor(1)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (1). |
| `\Processor(10)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (10). |
| `\Processor(11)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (11). |
| `\Processor(12)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (12). |
| `\Processor(13)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (13). |
| `\Processor(14)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (14). |
| `\Processor(15)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (15). |
| `\Processor(16)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (16). |
| `\Processor(17)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (17). |
| `\Processor(18)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (18). |
| `\Processor(19)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (19). |
| `\Processor(2)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (2). |
| `\Processor(20)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (20). |
| `\Processor(21)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (21). |
| `\Processor(22)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (22). |
| `\Processor(23)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (23). |
| `\Processor(24)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (24). |
| `\Processor(25)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (25). |
| `\Processor(26)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (26). |
| `\Processor(27)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (27). |
| `\Processor(28)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (28). |
| `\Processor(29)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (29). |
| `\Processor(3)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (3). |
| `\Processor(30)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (30). |
| `\Processor(31)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (31). |
| `\Processor(32)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (32). |
| `\Processor(33)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (33). |
| `\Processor(34)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (34). |
| `\Processor(35)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (35). |
| `\Processor(36)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (36). |
| `\Processor(37)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (37). |
| `\Processor(38)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (38). |
| `\Processor(39)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (39). |
| `\Processor(4)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (4). |
| `\Processor(40)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (40). |
| `\Processor(41)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (41). |
| `\Processor(42)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (42). |
| `\Processor(43)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (43). |
| `\Processor(44)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (44). |
| `\Processor(45)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (45). |
| `\Processor(46)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (46). |
| `\Processor(47)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (47). |
| `\Processor(48)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (48). |
| `\Processor(49)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (49). |
| `\Processor(5)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (5). |
| `\Processor(50)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (50). |
| `\Processor(51)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (51). |
| `\Processor(52)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (52). |
| `\Processor(53)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (53). |
| `\Processor(54)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (54). |
| `\Processor(55)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (55). |
| `\Processor(56)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (56). |
| `\Processor(57)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (57). |
| `\Processor(58)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (58). |
| `\Processor(59)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (59). |
| `\Processor(6)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (6). |
| `\Processor(60)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (60). |
| `\Processor(61)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (61). |
| `\Processor(62)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (62). |
| `\Processor(63)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (63). |
| `\Processor(7)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (7). |
| `\Processor(8)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (8). |
| `\Processor(9)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (9). |
| `\Processor(_Total)\% Processor Time` | `Account^Cluster^DataCenter` | Windows/Geneva performance counter for % processor time on Processor (_Total). |
| `\TCPv4\Connection Failures` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connection failures on TCPv4. |
| `\TCPv4\Connections Active` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connections active on TCPv4. |
| `\TCPv4\Connections Established` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connections established on TCPv4. |
| `\TCPv4\Connections Passive` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for connections passive on TCPv4. |
| `\TCPv4\Connections Reset` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for connections reset on TCPv4. |
| `\TCPv4\Segments Received/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for segments received/sec on TCPv4. |
| `\TCPv4\Segments Sent/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for segments sent/sec on TCPv4. |
| `\TCPv4\Segments/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for segments/sec on TCPv4. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dotnet.jit.compilation.time` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures dotnet jit compilation time. |
| `dotnet.jit.compiled_methods` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures dotnet jit compiled methods. |
| `dotnet.monitor.lock_contentions` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures dotnet monitor lock contentions. |
| `http.client.open_connections` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.connection.state^network.peer.address^network.protocol.version^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely measures http client open connections. |
| `process.runtime.dotnet.jit.compilation_time` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures process runtime dotnet jit compilation time. |

#### `MdmDataMgmtMetrics` (51 metrics)

Curated DM metrics for batching, authentication, request handling, ingestion age, and ingestion capacity.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BatchPeriodSeconds` | `Account^Cluster^Database^DataCenter^ResourceId` | Likely measures latency or duration for batch period seconds. |
| `BlockExecutionDuration` | `BlockName^BlockType^Cluster^ComponentName^ComponentType^DataCenter^ExecutionStatus` | Likely measures latency or duration for block execution duration. |
| `EventHubEventAgeSeconds` | `Account^Cluster` | Likely measures latency or duration for event hub event age seconds. |
| `FetchedQueueMessages` | `Cluster^ComponentName^ComponentType^DataCenter^ResourceId^StorageAccountName^StorageObjectName^StorageObjectPurpose^VirtualClusterName` | Likely measures latency or duration for fetched queue messages. |
| `IngestedEventAgeSeconds` | `Account^Cluster^DataCenter^IngestionKind^ResourceId` | Likely measures latency or duration for ingested event age seconds. |
| `MessageAgeInPipelineSeconds` | `Account^Cluster^ComponentName^ComponentType^Database^DataCenter^DeploymentRing^IsRetry^ResourceId^VirtualClusterName` | Likely measures latency or duration for message age in pipeline seconds. |
| `MessageAgeInUpstreamSeconds` | `Account^Cluster^ComponentName^ComponentType^DataCenter^Moniker^ResourceId^VirtualClusterName` | Likely measures latency or duration for message age in upstream seconds. |
| `QueueMessagesFetchDuration` | `Cluster^ComponentName^ComponentType^StorageAccountName^StorageObjectName^StorageObjectPurpose` | Likely measures latency or duration for queue messages fetch duration. |
| `QueueOldestMessage` | `Account^Cluster^ComponentType^DataCenter^ResourceId^VirtualClusterName` | Likely measures latency or duration for queue oldest message. |
| `RequestDurationMs` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^EndpointPath^RequestMethod^ResourceId^StatusCode^VirtualClusterName` | Likely measures latency or duration for request duration ms. |
| `StorageOperationError` | `Account^Cluster^ComponentName^ComponentType^DataCenter^ErrorCode^StatusCode^StorageAccountName^StorageObjectOwnership^StorageObjectPurpose^StorageServiceType^VirtualClusterName` | Likely measures latency or duration for storage operation error. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ActiveServiceInstances` | `Cluster^DataCenter^DeploymentRing^RoleInstance^ServiceType` | Count of active service instances reporting for the component. |
| `FabricServiceInstancesActive` | `Account^Cluster^DataCenter^Service` | Likely counts the current amount of fabric service instances active. |
| `ObtainerPipelineActiveWorkers` | `Account^Cluster^DataCenter^ElementName` | Likely counts the current amount of obtainer pipeline active workers. |
| `QueueLength` | `Account^Cluster^ComponentType^DataCenter^ResourceId^VirtualClusterName` | Likely counts the current amount of queue length. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BlockUtilization` | `BlockName^BlockType^Cluster^ComponentName^ComponentType^DataCenter` | Likely tracks resource usage or capacity for block utilization. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BatchSizeBytes` | `Account^Cluster^Database^DataCenter^ResourceId` | Likely measures size, volume, or throughput for batch size bytes. |
| `BlockInputQueueSize` | `BlockName^BlockType^Cluster^ComponentName^ComponentType^DataCenter` | Likely measures size, volume, or throughput for block input queue size. |
| `BlockOutputQueueSize` | `BlockName^BlockType^Cluster^ComponentName^ComponentType^DataCenter` | Likely measures size, volume, or throughput for block output queue size. |
| `ObtainerPipelineInputQueueSize` | `Account^Cluster^DataCenter^ElementName` | Likely measures size, volume, or throughput for obtainer pipeline input queue size. |
| `ReceivedDataSizeBytes` | `Account^Cluster^ComponentName^ComponentType^ResourceId` | Likely measures size, volume, or throughput for received data size bytes. |

##### Ingestion pipeline

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BatchBlobCount` | `Account^Cluster^Database^DataCenter^ResourceId` | Likely counts the current amount of batch blob count. |
| `BatchesProcessed` | `Account^Cluster^Database^DataCenter^ResourceId^SealReason^VirtualClusterName` | Likely measures ingestion pipeline behavior for batches processed. |
| `BlobsProcessed` | `Account^Cluster^ComponentName^ComponentType^Database^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures ingestion pipeline behavior for blobs processed. |
| `BlobsReceived` | `Account^Cluster^ComponentName^ComponentType^Database^DataCenter^ResourceId^VirtualClusterName` | Likely measures ingestion pipeline behavior for blobs received. |
| `IngestionCapacityWaitTime` | `Cluster` | Likely tracks resource usage or capacity for ingestion capacity wait time. |

##### Data layout & storage

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `PurgePendingRequestsCount` | `Account^Cluster^DataCenter^State` | Likely counts the current amount of purge pending requests count. |
| `PurgeResult` | `Account^Cluster^DataCenter^ResourceId^ResultDetails^ResultKind` | Likely measures storage layout or data-management work for purge result. |
| `PurgeTimeInQueue` | `Account^Cluster^DataCenter` | Likely counts the current amount of purge time in queue. |
| `PurgeTotalProcessingTime` | `Account^Cluster^DataCenter` | Likely measures storage layout or data-management work for purge total processing time. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BlobsDropped` | `Account^Cluster^ComponentName^ComponentType^Database^DataCenter^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for blobs dropped. |
| `DataConnectionError` | `Cluster^ComponentName^ComponentType^DataCenter^DataConnectionResourceId^Reason^ResourceId` | Likely counts errors, failures, or throttling for data connection error. |
| `EventsDropped` | `Account^Cluster^ComponentName^ComponentType^DataCenter^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for events dropped. |
| `ObtainerConnectionError` | `Account^Cluster^DataCenter^ElementName^ElementType^FailureKind` | Likely counts errors, failures, or throttling for obtainer connection error. |
| `ObtainerInitializeError` | `Account^Cluster^DataCenter^DeploymentRing^ElementName^ElementType` | Likely counts errors, failures, or throttling for obtainer initialize error. |
| `SASRegenerationFailures` | `Account^Cluster^DataCenter` | Likely counts errors, failures, or throttling for sasregeneration failures. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ApplicationAuthenticationSuccess` | `ApplicationPrinicipalName^AuthenticationMethod^CloudName^Cluster^DataCenter` | Likely measures application authentication success. |
| `BlockDegreeOfParallelism` | `BlockName^BlockType^Cluster^ComponentName^ComponentType^DataCenter` | Likely measures block degree of parallelism. |
| `CriticalAttention` | `Account^Cluster^ComponentName^ComponentType^DataCenter^DeploymentRing^Ownership^ResourceId^State^VirtualClusterName` | Likely measures critical attention. |
| `EventsDiscarded` | `Cluster^ComponentName^ComponentType` | Likely measures events discarded. |
| `EventsProcessed` | `Account^Cluster^ComponentName^ComponentType^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures events processed. |
| `EventsReceived` | `Account^Cluster^ComponentName^ComponentType^DataCenter^ResourceId^VirtualClusterName` | Likely measures events received. |
| `FabricServiceInstancesRequested` | `Account^Cluster^DataCenter^ResourceId^Service` | Likely measures fabric service instances requested. |
| `MachinesOffline` | `Account^Cluster^DataCenter^DeploymentRing` | Likely measures machines offline. |
| `MachinesOnline` | `Cluster^DataCenter` | Likely measures machines online. |
| `MachinesTotal` | `Account^Cluster^DataCenter^DeploymentRing^ResourceId` | Likely measures machines total. |
| `NullSASReceived` | `Account^Cluster^DataCenter` | Likely measures null sasreceived. |
| `ObtainerPipelineCurrentWorkersLimit` | `Account^Cluster^DataCenter^ElementName` | Likely measures obtainer pipeline current workers limit. |
| `ObtainerPipelineWorkerExecutionResult` | `Account^Cluster^DataCenter^ElementName^ExecutionStatus` | Likely measures obtainer pipeline worker execution result. |
| `PeriodicJobExecution` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^Name^ResourceId^ResultKind^VirtualClusterName` | Likely measures periodic job execution. |
| `SASRegenerationAttempts` | `Account^Cluster^DataCenter` | Likely measures sasregeneration attempts. |

#### `MdmDataMgmtHosterMetrics` (6 metrics)

Hoster metrics for DM virtual clusters, node targets, CPU, and hoster health.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `VirtualClusterHosterHealth` | `Cluster^DataCenter^DeploymentRing^RoleInstance` | Likely measures virtual cluster hoster health. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `HosterTargetNumberOfNodes` | `Account^Cluster^DataCenter` | Likely counts the current amount of hoster target number of nodes. |
| `NumberOfCalls` | `CallType^Cluster^DataCenter^DeploymentRing^RoleInstance^State^VirtualClusterName` | Likely counts the current amount of number of calls. |
| `NumberOfVirtualClusters` | `Cluster^DataCenter^RoleInstance^State` | Likely counts the current amount of number of virtual clusters. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `VirtualClusterCpu` | `Cluster^DataCenter^VirtualClusterName` | Likely tracks resource usage or capacity for virtual cluster cpu. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `VirtualClusterState` | `Cluster^DataCenter^State^VirtualClusterName` | Likely measures virtual cluster state. |

### Cluster Management Metrics

Cluster operations, autoscale, maintenance jobs, and control-plane health.

#### `cmMetrics` (92 metrics)

Legacy/raw cluster-management metrics for requests, background jobs, Cosmos DB calls, and control-plane operations.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `SkuAvailability` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^Region^ResourceId^Sku^SubscriptionId^VirtualClusterName^Zone1^Zone2^Zone3` | Health or availability signal for sku availability. |

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `CosmosDbRequestDuration` | `ApiMethod^CloudName^Cluster^ContainerName^DataCenter` | Likely measures latency or duration for cosmos db request duration. |
| `DimClustersIgnestDuration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^DimClustersJobIngestTargetService^ResourceId^VirtualClusterName` | Likely measures latency or duration for dim clusters ignest duration. |
| `http.client.request.duration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.request.method^http.response.status_code^network.protocol.version^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely measures latency or duration for http client request duration. |
| `OperationDuration` | `Account^ArmResourceId^CloudName^Cluster^ContainsVnetCluster^DataCenter^DeploymentRing^ExceptionType^IsNoSLA^OperationKind^OperationState^ProfileName` | Duration of the named operation. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ConcurrentRequests` | `Account^Cluster^DataCenter^OperationKind^ServiceName` | Number of simultaneous requests being handled. |
| `DimClustersJobState` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of dim clusters job state. |
| `process.runtime.dotnet.assemblies.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet assemblies count. |
| `SlidingWindowRequests` | `Account^Cluster^OperationKind^ServiceName` | Likely counts the current amount of sliding window requests. |
| `UpdateExternalMeterRatesJobState` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of update external meter rates job state. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.gc.collections.count` | `Cluster^DataCenter` | Likely counts the current amount of process runtime dotnet gc collections count. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.gc.objects.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc objects size. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.exceptions.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for process runtime dotnet exceptions count. |
| `ThrottledRequests` | `Account^Cluster^OperationKind^ServiceName` | Likely counts errors, failures, or throttling for throttled requests. |

##### Windows / .NET perf counters

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `\.NET CLR Exceptions(Kusto.WinSvc.Svc)\# of Exceps Thrown / sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for # of exceps thrown / sec on NET CLR Exceptions (Kusto.WinSvc.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.CM.Svc)\# Bytes in all Heaps` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for # bytes in all heaps on NET CLR Memory (Kusto.WinSvc.CM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.CM.Svc)\# Total committed Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for # total committed bytes on NET CLR Memory (Kusto.WinSvc.CM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.CM.Svc)\% Time in GC` | `Account^Cluster` | Windows/Geneva performance counter for % time in gc on NET CLR Memory (Kusto.WinSvc.CM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.CM.Svc)\Allocated Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for allocated bytes/sec on NET CLR Memory (Kusto.WinSvc.CM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.CM.Svc)\Gen 0 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 0 heap size on NET CLR Memory (Kusto.WinSvc.CM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.CM.Svc)\Gen 1 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 1 heap size on NET CLR Memory (Kusto.WinSvc.CM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.CM.Svc)\Gen 2 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 2 heap size on NET CLR Memory (Kusto.WinSvc.CM.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.CM.Svc)\Large Object Heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for large object heap size on NET CLR Memory (Kusto.WinSvc.CM.Svc). |
| `\LogicalDisk(_Total)\% Free Space` | `Cluster^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Read Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Write Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Current Disk Queue Length` | `Account^Cluster^DataCenter` | Windows/Geneva performance counter for current disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Free Megabytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for free megabytes on Logical Disk (_Total). |
| `\LogicalDisk(C:)\% Free Space` | `Cluster^RoleInstance` | Windows/Geneva performance counter for % free space on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (C:). |
| `\LogicalDisk(D:)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (D:). |
| `\LogicalDisk(HarddiskVolume1)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume2)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume3)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume3). |
| `\Memory\Available Bytes` | `Account^CloudName^Cluster^DataCenter^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for available bytes on Memory. |
| `\Network Adapter(Microsoft Hyper-V Network Adapter _2)\Bytes Received/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes received/sec on Network Adapter (Microsoft Hyper-V Network Adapter _2). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter _2)\Bytes Sent/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes sent/sec on Network Adapter (Microsoft Hyper-V Network Adapter _2). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Received/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes received/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Sent/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes sent/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Process(Kusto.WinSvc.CM.Svc)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Process (Kusto.WinSvc.CM.Svc). |
| `\Process(Kusto.WinSvc.CM.Svc)\Pool Nonpaged Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for pool nonpaged bytes on Process (Kusto.WinSvc.CM.Svc). |
| `\Process(Kusto.WinSvc.CM.Svc)\Pool Paged Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for pool paged bytes on Process (Kusto.WinSvc.CM.Svc). |
| `\Process(Kusto.WinSvc.CM.Svc)\Private Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for private bytes on Process (Kusto.WinSvc.CM.Svc). |
| `\Process(Kusto.WinSvc.CM.Svc)\Thread Count` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for thread count on Process (Kusto.WinSvc.CM.Svc). |
| `\Process(Kusto.WinSvc.CM.Svc)\Working Set` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set on Process (Kusto.WinSvc.CM.Svc). |
| `\Process(Kusto.WinSvc.CM.Svc)\Working Set - Private` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set - private on Process (Kusto.WinSvc.CM.Svc). |
| `\Process(Kusto.WinSvc.CM.Svc)\Working Set Peak` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set peak on Process (Kusto.WinSvc.CM.Svc). |
| `\Processor(0)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (0). |
| `\Processor(1)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (1). |
| `\Processor(10)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (10). |
| `\Processor(11)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (11). |
| `\Processor(12)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (12). |
| `\Processor(13)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (13). |
| `\Processor(14)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (14). |
| `\Processor(15)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (15). |
| `\Processor(2)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (2). |
| `\Processor(3)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (3). |
| `\Processor(4)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (4). |
| `\Processor(5)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (5). |
| `\Processor(6)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (6). |
| `\Processor(7)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (7). |
| `\Processor(8)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (8). |
| `\Processor(9)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (9). |
| `\Processor(_Total)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (_Total). |
| `\TCPv4\Connection Failures` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connection failures on TCPv4. |
| `\TCPv4\Connections Active` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connections active on TCPv4. |
| `\TCPv4\Connections Established` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connections established on TCPv4. |
| `\TCPv4\Connections Passive` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for connections passive on TCPv4. |
| `\TCPv4\Connections Reset` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for connections reset on TCPv4. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BackgroundJobExecutions` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ExecutionStatus^JobName^ResourceId^VirtualClusterName` | Likely measures background job executions. |
| `CosmosDbRequestRequestCharge` | `ApiMethod^CloudName^Cluster^ContainerName^DataCenter` | Likely measures cosmos db request request charge. |
| `PartialDeployment` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^ServiceName^VirtualClusterName` | Likely measures partial deployment. |

#### `MdmClusterMgmtMetrics` (54 metrics)

Curated CM metrics for autoscale, maintenance, deployment, operation latency, and cluster-management health.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `AutoScalePersistenceStorageManagerAvailabilityMetric` | `Cluster^DataCenter` | Health or availability signal for auto scale persistence storage manager availability metric. |
| `AvailableRegionalVip` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^IpTagName^Region^ResourceId^VirtualClusterName` | Likely measures available regional vip. |
| `IsClusterMgmtHealthy` | `Account^Cluster^DataCenter` | Health or availability signal for is cluster mgmt healthy. |
| `UnallocatedSubscriptionsAvailableUsage` | `Account^Cluster^CustomerSegment^DataCenter^IsLocked^Location^Property^Purposes^SubscriptionId` | Likely measures latency or duration for unallocated subscriptions available usage. |
| `UnallocatedSubscriptionsSkuAvailability` | `Account^Cluster^DataCenter^Location^Property` | Health or availability signal for unallocated subscriptions sku availability. |
| `UnallocatedSubscriptionsSkuEffectiveAvailability` | `Cluster^DataCenter^Location^Property` | Health or availability signal for unallocated subscriptions sku effective availability. |
| `UnallocatedVirtualClustersPoolHealth` | `Cluster^DataCenter^DeploymentRing^VirtualClusterName` | Likely measures unallocated virtual clusters pool health. |

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `CloudVaultDuration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^VirtualClusterName` | Likely measures latency or duration for cloud vault duration. |
| `JobSuccessLongDuration` | `Cluster^DataCenter^DeploymentRing^JobName` | Likely measures latency or duration for job success long duration. |
| `JobSuccessMediumDuration` | `Cluster^DataCenter^DeploymentRing^JobName` | Likely measures latency or duration for job success medium duration. |
| `JobSuccessShortDuration` | `Cluster^DataCenter^DeploymentRing^JobName` | Likely measures latency or duration for job success short duration. |
| `OperationLatency` | `Account^Caller^Cluster^DataCenter^DeploymentRing^Operation^ResponsibleCm^State^TargetServiceType` | Likely measures latency or duration for operation latency. |
| `TridentOutboundAccessProtectionJobDuration` | `Cluster^DataCenter^ExceptionType^NumberOfWorkspaces^OperationState` | Likely measures latency or duration for trident outbound access protection job duration. |
| `TridentSubArtifactsSyncLatency` | `Cluster^DataCenter` | Likely measures latency or duration for trident sub artifacts sync latency. |
| `TridnetAlmArtifactsSyncLatency` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures latency or duration for tridnet alm artifacts sync latency. |
| `UnallocatedSubscriptionsCurrentUsage` | `Account^Cluster^CustomerSegment^DataCenter^IsLocked^Location^Property^Purposes^SubscriptionId` | Likely measures latency or duration for unallocated subscriptions current usage. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ActiveServiceInstances` | `Cluster^DataCenter^DeploymentRing^RoleInstance^ServiceType` | Count of active service instances reporting for the component. |
| `CloudServiceMaintenanceOperationsInProgress` | `Account^Cluster` | Likely counts the current amount of cloud service maintenance operations in progress. |
| `ClusterMetadataOperationsInProgress` | `Account^Cluster` | Likely counts the current amount of cluster metadata operations in progress. |
| `DeploymentOperationsInProgress` | `Account^Cluster` | Likely counts the current amount of deployment operations in progress. |
| `FabricServiceInstancesActive` | `Account^Cluster^DataCenter^Service` | Likely counts the current amount of fabric service instances active. |
| `OrchestrationMaxQueueLength` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of orchestration max queue length. |
| `TotalAccounts` | `Account^Cluster` | Likely counts the current amount of total accounts. |
| `UnallocatedSubscriptionsCount` | `Account^Cluster^DataCenter` | Likely counts the current amount of unallocated subscriptions count. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `FabricCapacityThrottlingLevel` | `Cluster^DataCenter^FabricEnvironment` | Likely tracks resource usage or capacity for fabric capacity throttling level. |

##### Data layout & storage

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `DatabaseCmkMismatchConfigurations` | `Account^CloudName^Cluster^DatabaseName^DataCenter^DeploymentRing^ResourceId^ServiceName^VirtualClusterName` | Likely measures storage layout or data-management work for database cmk mismatch configurations. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `FailedCloudServiceMaintenanceOperations` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for failed cloud service maintenance operations. |
| `FailedClusterMetadataOperations` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for failed cluster metadata operations. |
| `FailedCustomerOperations` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for failed customer operations. |
| `FailedDeploymentOperations` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for failed deployment operations. |
| `TridentClusterPrivateLinkOperationFailed` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationKind^ProfileName^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for trident cluster private link operation failed. |
| `TridentGetDiagnosticInfoFailed` | `Account^ArtifactsIds^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^TenantId^VirtualClusterName^WorkspacesIds` | Likely counts errors, failures, or throttling for trident get diagnostic info failed. |
| `TridentSubArtifactsSyncFailed` | `ArtifactId^Cluster^DataCenter^ExceptionType^SharedPlatformClusterUrl^TenantId` | Likely counts errors, failures, or throttling for trident sub artifacts sync failed. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `AffectedServices` | `Cluster^DataCenter^DeploymentRing^JobName` | Likely measures affected services. |
| `CloudServiceMaintenanceOperationsSuccessRate` | `Account^Cluster^DataCenter` | Success-rate metric for cloud service maintenance operations success rate. |
| `ClusterMetadataOperationsSuccessRate` | `Account^Cluster^DataCenter` | Success-rate metric for cluster metadata operations success rate. |
| `CmkMismatchConfigurations` | `Cluster^DataCenter^ServiceName` | Likely measures cmk mismatch configurations. |
| `CustomerOperationsSuccessRate` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Success-rate metric for customer operations success rate. |
| `DeploymentOperationsSuccessRate` | `Account^Cluster^DataCenter` | Success-rate metric for deployment operations success rate. |
| `DmAutoscale` | `DataCenter^TargetCluster` | Likely measures dm autoscale. |
| `DmAutoscaleAlgorithmMetric` | `Cluster^DataCenter^ScaleAlgorithm^TargetCluster` | Likely measures dm autoscale algorithm metric. |
| `FabricServiceInstancesRequested` | `Account^Cluster^DataCenter^ResourceId^Service` | Likely measures fabric service instances requested. |
| `GDPROperationsSuccessRate` | `Account^Cluster^DataCenter` | Success-rate metric for gdproperations success rate. |
| `MachinesOffline` | `Account^Cluster^DataCenter^DeploymentRing` | Likely measures machines offline. |
| `MachinesOnline` | `Cluster^DataCenter` | Likely measures machines online. |
| `MachinesTotal` | `Account^Cluster^DataCenter^DeploymentRing^ResourceId` | Likely measures machines total. |
| `PendingDistributedOperations` | `Account^Cluster` | Likely measures pending distributed operations. |
| `Reserved` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures reserved. |
| `Reserved0` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures reserved0. |
| `SoftDeleteMismatchConfigurations` | `Cluster^DataCenter^ResourceGroups^StorageAccount` | Likely measures soft delete mismatch configurations. |
| `TotalServices` | `Account^Cluster^DataCenter` | Likely measures total services. |
| `TridentFetchPrivateLinkState` | `Cluster^DataCenter^SharedPlatformClusterUrl^TenantId` | Likely measures trident fetch private link state. |
| `TridentFetchWorkspaceOutboundAccessProtectionRules` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ExceptionMessage^ResourceId^SharedPlatformClusterUrl^TenantId^VirtualClusterName^WorkspaceId` | Likely measures trident fetch workspace outbound access protection rules. |
| `TridentOutboundAccessProtectionJobInterval` | `Cluster^DataCenter` | Likely measures trident outbound access protection job interval. |

#### `MdmOptimizerAutoScaleMetrics` (6 metrics)

Optimizer and autoscale controller metrics for predictive/reactive scaling decisions.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `OptimizerServiceOperationDuration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^JobName^ResourceId^State^VirtualClusterName` | Likely measures latency or duration for optimizer service operation duration. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ReactiveAutoScale` | `Cluster^DataCenter^StatusDescription^TargetCluster` | Likely counts the current amount of reactive auto scale. |
| `ReactiveVirtualAutoScale` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^StatusDescription^TargetCluster^TargetHoster^VirtualClusterName` | Likely counts the current amount of reactive virtual auto scale. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `PredictiveAutoScale` | `Cluster^DataCenter^StatusDescription^TargetCluster` | Likely measures predictive auto scale. |
| `TridentExtremeBackgroundThrottlingEngineScaleIn` | `Cluster^DataCenter^TargetCluster^VirtualClusterName` | Likely measures trident extreme background throttling engine scale in. |
| `TridentSkuChangeAutoScale` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^DestinationSku^JobName^ResourceId^SourceSku^VirtualClusterName` | Likely measures trident sku change auto scale. |

### Ingestion Pipeline Metrics

Pipeline stage metrics from pre-batching through streaming ingestion and Geneva ingestion.

#### `KustoIngestion` (3 metrics)

End-to-end ingestion stage metrics covering latency and ingestion errors.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ComponentLatencyInSeconds` | `Cluster^Database^EventName` | Component-specific latency for the pipeline stage. |
| `LatencyInSeconds` | `Cluster^Database^EventName` | End-to-end latency for the pipeline stage. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IngestionErrors` | `Cluster^Database^EventName` | Likely counts errors, failures, or throttling for ingestion errors. |

#### `KustoBatching` (2 metrics)

Batching-stage latency metrics before data is ingested.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ComponentLatencyInSeconds` | `Cluster^Database^EventName` | Component-specific latency for the pipeline stage. |
| `LatencyInSeconds` | `Cluster^Database^EventName` | End-to-end latency for the pipeline stage. |

#### `KustoPreBatching` (2 metrics)

Pre-batching stage latency metrics ahead of batching.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ComponentLatencyInSeconds` | `Cluster^Database^EventName` | Component-specific latency for the pipeline stage. |
| `LatencyInSeconds` | `Cluster^Database^EventName` | End-to-end latency for the pipeline stage. |

#### `KustoBlobDownloader` (6 metrics)

Blob download stage metrics for ingestion sources, bytes downloaded, and row handling.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ComponentLatencyInSeconds` | `Cluster^ConsumerId^Database^EventName^LogsEnvironment^Namespace^SourceMonikerRegion` | Component-specific latency for the pipeline stage. |
| `LatencyInSeconds` | `Cluster^ConsumerId^Database^EventName^LogsEnvironment^Namespace^SourceMonikerRegion` | End-to-end latency for the pipeline stage. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BytesDownloaded` | `Cluster^ConsumerId^Database^EventName^LogsEnvironment^Namespace^SourceMonikerRegion` | Likely measures size, volume, or throughput for bytes downloaded. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `RowsDropped` | `Cluster^ConsumerId^Database^EventName^LogsEnvironment^Namespace^SourceMonikerRegion` | Likely counts errors, failures, or throttling for rows dropped. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `RowsReceived` | `Cluster^ConsumerId^Database^EventName^LogsEnvironment^Namespace^SourceMonikerRegion` | Likely measures rows received. |
| `RowsSent` | `Cluster^ConsumerId^Database^EventName^LogsEnvironment^Namespace^SourceMonikerRegion` | Likely measures rows sent. |

#### `StreamingIngestionMetrics` (12 metrics)

Streaming ingestion row-store and seal metrics, including concurrency, duration, WAL size, and local storage pressure.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `StreamingIngestionAvailableLocalStoragePercent` | `Cluster^DataCenter^RoleInstance` | Likely measures latency or duration for streaming ingestion available local storage percent. |

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IngestDuration` | `Account^Cluster^DataCenter^DeploymentRing^ResourceId^Result^RoleInstance^Usage^VirtualClusterName` | Streaming ingestion duration. |
| `RowStoreLoadFailureDueToLocalStorageLimitReached` | `(none)` | Likely measures latency or duration for row store load failure due to local storage limit reached. |
| `StreamingIngestionLocalStorageBytes` | `Account^Cluster^DataCenter^ResourceId^RoleInstance` | Likely measures latency or duration for streaming ingestion local storage bytes. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IngestSizeBytes` | `Account^Cluster^DataCenter^ResourceId^Usage^VirtualClusterName` | Bytes processed by ingestion. |
| `RowStoreWriteAheadLogSizeBytes` | `Account^Cluster^DataCenter^ResourceId^RowStoreName^VirtualClusterName` | Likely measures size, volume, or throughput for row store write ahead log size bytes. |

##### Ingestion pipeline

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ConcurrentIngests` | `Account^Cluster^DataCenter^RoleInstance^Usage^VirtualClusterName` | Likely counts the current amount of concurrent ingests. |
| `ConcurrentSeals` | `Account^Cluster^DataCenter^ResourceId^RoleInstance^Usage^VirtualClusterName` | Likely counts the current amount of concurrent seals. |
| `IngestsLoadFactor` | `Account^Cluster^DataCenter^ResourceId^Usage^VirtualClusterName` | Likely tracks resource usage or capacity for ingests load factor. |
| `RowStoreWriteAheadLogTrimming` | `Account^Cluster^DataCenter^ResourceId^RowStoreName` | Likely measures row store write ahead log trimming. |
| `SealsLoadFactor` | `Account^Cluster^DataCenter^ResourceId^Usage^VirtualClusterName` | Likely tracks resource usage or capacity for seals load factor. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BlockedKeyForEnabledReference` | `Account^Cluster^DataCenter` | Likely measures blocked key for enabled reference. |

#### `MdmGenevaIngestionMetrics` (8 metrics)

Metrics for shipping Geneva/MDM data into Kusto, including batch outcomes and blob latency.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BlobLatencyMillis` | `eventhubs.consumer.group^eventhubs.name^eventhubs.namespace^eventhubs.partition.id^kusto.log_analytics_database^kusto.log_analytics_id^mds.account^mds.environment^mds.event^mds.namespace^mds.region^mds.version^service.instance.id^service.name^service.namespace^service.version` | Likely measures latency or duration for blob latency millis. |
| `IdleTimeMillis` | `eventhubs.consumer.group^eventhubs.name^eventhubs.namespace^eventhubs.partition.id^kusto.log_analytics_database^kusto.log_analytics_id^mds.account^mds.environment^mds.event^mds.namespace^mds.region^mds.version^service.instance.id^service.name^service.namespace^service.version` | Likely measures latency or duration for idle time millis. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `InputByteCount` | `eventhubs.consumer.group^eventhubs.name^eventhubs.namespace^eventhubs.partition.id^kusto.log_analytics_database^kusto.log_analytics_id^mds.account^mds.environment^mds.event^mds.namespace^mds.region^mds.version^service.instance.id^service.name^service.namespace^service.version` | Likely counts the current amount of input byte count. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `EventProcessorCount` | `EventStreamProcessorId^process.pid^service.instance.id^service.name^service.namespace^service.version` | Likely counts the current amount of event processor count. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BlobSizeInBytes` | `eventhubs.consumer.group^eventhubs.name^eventhubs.namespace^eventhubs.partition.id^kusto.log_analytics_database^kusto.log_analytics_id^mds.account^mds.environment^mds.event^mds.namespace^mds.region^mds.version^service.instance.id^service.name^service.namespace^service.version` | Likely measures size, volume, or throughput for blob size in bytes. |

##### Ingestion pipeline

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BatchSent` | `count^eventhubs.consumer.group^eventhubs.name^eventhubs.namespace^eventhubs.partition.id^kusto.log_analytics_database^kusto.log_analytics_id^mds.account^mds.environment^service.instance.id^service.name^service.namespace^service.version` | Likely measures ingestion pipeline behavior for batch sent. |
| `BatchSucceeded` | `count^eventhubs.consumer.group^eventhubs.name^eventhubs.namespace^eventhubs.partition.id^kusto.log_analytics_database^kusto.log_analytics_id^mds.account^mds.environment^service.instance.id^service.name^service.namespace^service.version` | Likely measures ingestion pipeline behavior for batch succeeded. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `EventReceived` | `eventhubs.consumer.group^eventhubs.name^eventhubs.namespace^eventhubs.partition.id^kusto.log_analytics_database^kusto.log_analytics_id^mds.account^mds.environment^mds.event^mds.namespace^mds.region^mds.version^service.instance.id^service.name^service.namespace^service.version` | Likely measures event received. |

### Query Metrics

Query concurrency, latency, request pressure, and sandbox/container behavior.

#### `QueryMetrics` (3 metrics)

Direct query workload metrics for concurrency, duration, and throttling.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `QueryDuration` | `Account^Cluster^DataCenter^DeploymentRing^Fault^QueryStatus^Reason^ResourceId^VirtualClusterName` | End-to-end query duration. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ConcurrentQueries` | `Account^Cluster^DataCenter^ResourceId^RoleInstance^VirtualClusterName` | Number of queries executing concurrently. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `QueryThrottled` | `Account^Cluster^DataCenter^ResourceId^VirtualClusterName` | Count of queries throttled or rejected by query controls. |

#### `SandboxMetrics` (7 metrics)

Sandbox/container lifecycle and throttling metrics for isolated query execution.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ACIContainerAcquireDurationSeconds` | `(none)` | Likely measures latency or duration for acicontainer acquire duration seconds. |
| `ACIContainerStartDurationSeconds` | `(none)` | Likely measures latency or duration for acicontainer start duration seconds. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `SandboxedQueryThrottled` | `(none)` | Likely counts errors, failures, or throttling for sandboxed query throttled. |
| `SandboxInitializationFailed` | `Account^Cluster^DataCenter` | Likely counts errors, failures, or throttling for sandbox initialization failed. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ACIContainerCreation` | `(none)` | Likely measures acicontainer creation. |
| `ACIContainerInitialization` | `(none)` | Likely measures acicontainer initialization. |
| `ACIStandbyPoolState` | `(none)` | Likely measures acistandby pool state. |

#### `RequestMetrics` (2 metrics)

Request-level concurrency and request-classification metrics.

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ConcurrentRequests` | `Account^Cluster^DataCenter^WorkloadGroup` | Number of simultaneous requests being handled. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ClassificationFailure` | `(none)` | Likely counts errors, failures, or throttling for classification failure. |

### Resource Provider Metrics

ARM/RP operations, SaaS RP health, and service-probe or RP runtime counters.

#### `resourceProviderMetrics` (99 metrics)

Resource-provider control-plane metrics for ARM objects such as clusters, data connections, and attached DB configurations.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ManagedPrivateEndpointsCreated` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures latency or duration for managed private endpoints created. |
| `ManagedPrivateEndpointsDeleted` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures latency or duration for managed private endpoints deleted. |
| `OperationLatency` | `Account^Cluster^DataCenter^DeploymentRing^Operation^OperationState^StatusCode` | Likely measures latency or duration for operation latency. |
| `SandboxCustomImagesCreated` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures latency or duration for sandbox custom images created. |
| `SandboxCustomImagesDeleted` | `Not observed in sampled dimension extracts` | Likely measures latency or duration for sandbox custom images deleted. |

##### Data layout & storage

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `AttachedDatabaseConfigurationsCreated` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures storage layout or data-management work for attached database configurations created. |
| `AttachedDatabaseConfigurationsDeleted` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures storage layout or data-management work for attached database configurations deleted. |
| `DatabasesCreated` | `Account^Cluster^DataCenter^OperationState^StatusCode` | Likely measures storage layout or data-management work for databases created. |
| `DatabasesDeleted` | `Account^Cluster^DataCenter^OperationState^StatusCode` | Likely measures storage layout or data-management work for databases deleted. |

##### Windows / .NET perf counters

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `\.NET CLR Memory(Kusto.WinSvc.RP.Svc)\# Bytes in all Heaps` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for # bytes in all heaps on NET CLR Memory (Kusto.WinSvc.RP.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.RP.Svc)\# Total committed Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for # total committed bytes on NET CLR Memory (Kusto.WinSvc.RP.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.RP.Svc)\% Time in GC` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % time in gc on NET CLR Memory (Kusto.WinSvc.RP.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.RP.Svc)\Allocated Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for allocated bytes/sec on NET CLR Memory (Kusto.WinSvc.RP.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.RP.Svc)\Gen 0 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 0 heap size on NET CLR Memory (Kusto.WinSvc.RP.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.RP.Svc)\Gen 1 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 1 heap size on NET CLR Memory (Kusto.WinSvc.RP.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.RP.Svc)\Gen 2 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 2 heap size on NET CLR Memory (Kusto.WinSvc.RP.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.RP.Svc)\Large Object Heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for large object heap size on NET CLR Memory (Kusto.WinSvc.RP.Svc). |
| `\LogicalDisk(_Total)\% Free Space` | `Cluster^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Read Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Write Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Current Disk Queue Length` | `Account^Cluster^DataCenter` | Windows/Geneva performance counter for current disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(C:)\% Free Space` | `Cluster^RoleInstance` | Windows/Geneva performance counter for % free space on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (C:). |
| `\LogicalDisk(D:)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (D:). |
| `\LogicalDisk(HarddiskVolume1)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume2)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume3)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume3). |
| `\Memory\Available Bytes` | `Account^CloudName^Cluster^DataCenter^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for available bytes on Memory. |
| `\Network Adapter(Microsoft Hyper-V Network Adapter _2)\Bytes Received/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes received/sec on Network Adapter (Microsoft Hyper-V Network Adapter _2). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter _2)\Bytes Sent/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes sent/sec on Network Adapter (Microsoft Hyper-V Network Adapter _2). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Received/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes received/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Sent/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes sent/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Process(Kusto.WinSvc.RP.Svc)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Process (Kusto.WinSvc.RP.Svc). |
| `\Process(Kusto.WinSvc.RP.Svc)\Pool Nonpaged Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for pool nonpaged bytes on Process (Kusto.WinSvc.RP.Svc). |
| `\Process(Kusto.WinSvc.RP.Svc)\Pool Paged Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for pool paged bytes on Process (Kusto.WinSvc.RP.Svc). |
| `\Process(Kusto.WinSvc.RP.Svc)\Private Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for private bytes on Process (Kusto.WinSvc.RP.Svc). |
| `\Process(Kusto.WinSvc.RP.Svc)\Thread Count` | `Cluster^DataCenter^RoleInstance` | Windows/Geneva performance counter for thread count on Process (Kusto.WinSvc.RP.Svc). |
| `\Process(Kusto.WinSvc.RP.Svc)\Working Set` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set on Process (Kusto.WinSvc.RP.Svc). |
| `\Process(Kusto.WinSvc.RP.Svc)\Working Set - Private` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set - private on Process (Kusto.WinSvc.RP.Svc). |
| `\Process(Kusto.WinSvc.RP.Svc)\Working Set Peak` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set peak on Process (Kusto.WinSvc.RP.Svc). |
| `\Processor(0)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (0). |
| `\Processor(1)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (1). |
| `\Processor(10)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (10). |
| `\Processor(11)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (11). |
| `\Processor(12)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (12). |
| `\Processor(13)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (13). |
| `\Processor(14)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (14). |
| `\Processor(15)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (15). |
| `\Processor(2)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (2). |
| `\Processor(3)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (3). |
| `\Processor(4)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (4). |
| `\Processor(5)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (5). |
| `\Processor(6)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (6). |
| `\Processor(7)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (7). |
| `\Processor(8)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (8). |
| `\Processor(9)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (9). |
| `\Processor(_Total)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (_Total). |
| `\TCPv4\Connection Failures` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connection failures on TCPv4. |
| `\TCPv4\Connections Active` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connections active on TCPv4. |
| `\TCPv4\Connections Established` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connections established on TCPv4. |
| `\TCPv4\Connections Passive` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for connections passive on TCPv4. |
| `\TCPv4\Connections Reset` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for connections reset on TCPv4. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ClusterDataConnectionsCreated` | `Account^Cluster^DataCenter^OperationState^StatusCode` | Likely measures cluster data connections created. |
| `ClustersCreated` | `Account^Cluster^DataCenter^OperationState^StatusCode` | Likely measures clusters created. |
| `ClustersDeleted` | `Account^Cluster^DataCenter^OperationState^StatusCode` | Likely measures clusters deleted. |
| `ClustersMoved` | `Account^AccountName^CloudName^Cluster^DataCenter^DeploymentRing^Environment^Location^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures clusters moved. |
| `ClustersUpdated` | `Account^Cluster^DataCenter^OperationState^StatusCode` | Likely measures clusters updated. |
| `DataConnectionsCreated` | `Account^Cluster^DataCenter^DataConnectionKind^OperationState^StatusCode` | Likely measures data connections created. |
| `DataConnectionsDeleted` | `Account^Cluster^DataCenter^OperationState^StatusCode` | Likely measures data connections deleted. |
| `PrivateEndpointConnectionDeleted` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures private endpoint connection deleted. |
| `PrivateEndpointConnectionProxyCreated` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures private endpoint connection proxy created. |
| `PrivateEndpointConnectionProxyDeleted` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures private endpoint connection proxy deleted. |
| `PrivateEndpointConnectionProxyValidated` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures private endpoint connection proxy validated. |
| `PrivateEndpointConnectionUpdated` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures private endpoint connection updated. |
| `ScriptsCreated` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures scripts created. |
| `ScriptsDeleted` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures scripts deleted. |
| `ScriptsUpdated` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures scripts updated. |
| `SharedIdentitiesAssigned` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationState^ResourceId^StatusCode^VirtualClusterName` | Likely measures shared identities assigned. |
| `SuspiciousRequestToRp` | `Account^Cluster^DataCenter` | Likely measures suspicious request to rp. |

#### `MdmSaasRpMetrics` (58 metrics)

Curated SaaS resource-provider metrics and runtime counters.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `http.client.request.duration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.request.method^http.response.status_code^network.protocol.version^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely measures latency or duration for http client request duration. |
| `OperationDuration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^OperationKind^OperationState` | Duration of the named operation. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.assemblies.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet assemblies count. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.gc.collections.count` | `Cluster^DataCenter` | Likely counts the current amount of process runtime dotnet gc collections count. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.gc.objects.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc objects size. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.exceptions.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for process runtime dotnet exceptions count. |

##### Windows / .NET perf counters

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `\.NET CLR Memory(Kusto.WinSvc.SaasResourceProvider.Svc)\# Bytes in all Heaps` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for # bytes in all heaps on NET CLR Memory (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.SaasResourceProvider.Svc)\# Total committed Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for # total committed bytes on NET CLR Memory (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.SaasResourceProvider.Svc)\% Time in GC` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % time in gc on NET CLR Memory (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.SaasResourceProvider.Svc)\Allocated Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for allocated bytes/sec on NET CLR Memory (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.SaasResourceProvider.Svc)\Gen 0 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 0 heap size on NET CLR Memory (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.SaasResourceProvider.Svc)\Gen 1 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 1 heap size on NET CLR Memory (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.SaasResourceProvider.Svc)\Gen 2 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 2 heap size on NET CLR Memory (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.SaasResourceProvider.Svc)\Large Object Heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for large object heap size on NET CLR Memory (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\LogicalDisk(_Total)\% Free Space` | `Cluster^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Read Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Write Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Current Disk Queue Length` | `Account^Cluster^DataCenter` | Windows/Geneva performance counter for current disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(C:)\% Free Space` | `Cluster^RoleInstance` | Windows/Geneva performance counter for % free space on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (C:). |
| `\LogicalDisk(D:)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (D:). |
| `\LogicalDisk(HarddiskVolume1)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume1). |
| `\Memory\Available Bytes` | `Account^CloudName^Cluster^DataCenter^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for available bytes on Memory. |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Received/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes received/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Sent/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes sent/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Process(Kusto.WinSvc.SaasResourceProvider.Svc)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Process (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\Process(Kusto.WinSvc.SaasResourceProvider.Svc)\Pool Nonpaged Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for pool nonpaged bytes on Process (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\Process(Kusto.WinSvc.SaasResourceProvider.Svc)\Pool Paged Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for pool paged bytes on Process (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\Process(Kusto.WinSvc.SaasResourceProvider.Svc)\Private Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for private bytes on Process (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\Process(Kusto.WinSvc.SaasResourceProvider.Svc)\Thread Count` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for thread count on Process (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\Process(Kusto.WinSvc.SaasResourceProvider.Svc)\Working Set` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set on Process (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\Process(Kusto.WinSvc.SaasResourceProvider.Svc)\Working Set - Private` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set - private on Process (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\Process(Kusto.WinSvc.SaasResourceProvider.Svc)\Working Set Peak` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set peak on Process (Kusto.WinSvc.SaasResourceProvider.Svc). |
| `\Processor(0)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (0). |
| `\Processor(1)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (1). |
| `\Processor(2)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (2). |
| `\Processor(3)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (3). |
| `\Processor(4)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (4). |
| `\Processor(5)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (5). |
| `\Processor(6)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (6). |
| `\Processor(7)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (7). |
| `\Processor(_Total)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (_Total). |
| `\TCPv4\Connections Active` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connections active on TCPv4. |
| `\TCPv4\Connections Established` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connections established on TCPv4. |
| `\TCPv4\Connections Passive` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for connections passive on TCPv4. |
| `\TCPv4\Connections Reset` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for connections reset on TCPv4. |

#### `spMetrics` (85 metrics)

Service-probe service runtime counters, mostly process/.NET and network metrics.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `dns.lookup.duration` | `Cluster^DataCenter^dns.question.name^VirtualClusterName` | Likely measures latency or duration for dns lookup duration. |
| `http.client.connection.duration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^network.peer.address^network.protocol.version^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely measures latency or duration for http client connection duration. |
| `http.client.request.duration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.request.method^http.response.status_code^network.protocol.version^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely measures latency or duration for http client request duration. |
| `process.runtime.dotnet.gc.duration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures latency or duration for process runtime dotnet gc duration. |
| `process.runtime.dotnet.thread_pool.completed_items.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures latency or duration for process runtime dotnet thread pool completed items count. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `http.client.active_requests` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.request.method^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely counts the current amount of http client active requests. |
| `http.client.request.time_in_queue` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.request.method^network.protocol.version^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely counts the current amount of http client request time in queue. |
| `process.runtime.dotnet.assemblies.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet assemblies count. |
| `process.runtime.dotnet.jit.methods_compiled.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet jit methods compiled count. |
| `process.runtime.dotnet.monitor.lock_contention.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet monitor lock contention count. |
| `process.runtime.dotnet.thread_pool.queue.length` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet thread pool queue length. |
| `process.runtime.dotnet.thread_pool.threads.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet thread pool threads count. |
| `process.runtime.dotnet.timer.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet timer count. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.gc.collections.count` | `Cluster^DataCenter` | Likely counts the current amount of process runtime dotnet gc collections count. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.gc.allocations.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc allocations size. |
| `process.runtime.dotnet.gc.committed_memory.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc committed memory size. |
| `process.runtime.dotnet.gc.heap.fragmentation.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^generation^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc heap fragmentation size. |
| `process.runtime.dotnet.gc.heap.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^generation^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc heap size. |
| `process.runtime.dotnet.gc.objects.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc objects size. |
| `process.runtime.dotnet.jit.il_compiled.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet jit il compiled size. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.exceptions.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for process runtime dotnet exceptions count. |

##### Windows / .NET perf counters

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `\.NET CLR Memory(Kusto.WinSvc.ServiceProbe.Svc)\# Bytes in all Heaps` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for # bytes in all heaps on NET CLR Memory (Kusto.WinSvc.ServiceProbe.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.ServiceProbe.Svc)\# Total committed Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for # total committed bytes on NET CLR Memory (Kusto.WinSvc.ServiceProbe.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.ServiceProbe.Svc)\% Time in GC` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % time in gc on NET CLR Memory (Kusto.WinSvc.ServiceProbe.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.ServiceProbe.Svc)\Allocated Bytes/sec` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for allocated bytes/sec on NET CLR Memory (Kusto.WinSvc.ServiceProbe.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.ServiceProbe.Svc)\Gen 0 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 0 heap size on NET CLR Memory (Kusto.WinSvc.ServiceProbe.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.ServiceProbe.Svc)\Gen 1 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 1 heap size on NET CLR Memory (Kusto.WinSvc.ServiceProbe.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.ServiceProbe.Svc)\Gen 2 heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for gen 2 heap size on NET CLR Memory (Kusto.WinSvc.ServiceProbe.Svc). |
| `\.NET CLR Memory(Kusto.WinSvc.ServiceProbe.Svc)\Large Object Heap size` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for large object heap size on NET CLR Memory (Kusto.WinSvc.ServiceProbe.Svc). |
| `\LogicalDisk(_Total)\% Free Space` | `Cluster^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Read Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Write Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Current Disk Queue Length` | `Account^Cluster^DataCenter` | Windows/Geneva performance counter for current disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(C:)\% Free Space` | `Cluster^RoleInstance` | Windows/Geneva performance counter for % free space on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (C:). |
| `\LogicalDisk(D:)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (D:). |
| `\LogicalDisk(HarddiskVolume1)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume2)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume3)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume3). |
| `\Memory\Available Bytes` | `Account^CloudName^Cluster^DataCenter^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for available bytes on Memory. |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Received/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes received/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Sent/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes sent/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Process(Kusto.WinSvc.ServiceProbe.Svc)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Process (Kusto.WinSvc.ServiceProbe.Svc). |
| `\Process(Kusto.WinSvc.ServiceProbe.Svc)\Pool Nonpaged Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for pool nonpaged bytes on Process (Kusto.WinSvc.ServiceProbe.Svc). |
| `\Process(Kusto.WinSvc.ServiceProbe.Svc)\Pool Paged Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for pool paged bytes on Process (Kusto.WinSvc.ServiceProbe.Svc). |
| `\Process(Kusto.WinSvc.ServiceProbe.Svc)\Private Bytes` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for private bytes on Process (Kusto.WinSvc.ServiceProbe.Svc). |
| `\Process(Kusto.WinSvc.ServiceProbe.Svc)\Thread Count` | `Cluster^DataCenter^RoleInstance` | Windows/Geneva performance counter for thread count on Process (Kusto.WinSvc.ServiceProbe.Svc). |
| `\Process(Kusto.WinSvc.ServiceProbe.Svc)\Working Set` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set on Process (Kusto.WinSvc.ServiceProbe.Svc). |
| `\Process(Kusto.WinSvc.ServiceProbe.Svc)\Working Set - Private` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set - private on Process (Kusto.WinSvc.ServiceProbe.Svc). |
| `\Process(Kusto.WinSvc.ServiceProbe.Svc)\Working Set Peak` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for working set peak on Process (Kusto.WinSvc.ServiceProbe.Svc). |
| `\Processor(0)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (0). |
| `\Processor(1)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (1). |
| `\Processor(2)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (2). |
| `\Processor(3)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (3). |
| `\Processor(4)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (4). |
| `\Processor(5)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (5). |
| `\Processor(6)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (6). |
| `\Processor(7)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (7). |
| `\Processor(_Total)\% Processor Time` | `Cluster^DataCenter` | Windows/Geneva performance counter for % processor time on Processor (_Total). |
| `\TCPv4\Connections Active` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connections active on TCPv4. |
| `\TCPv4\Connections Established` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for connections established on TCPv4. |
| `\TCPv4\Connections Passive` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for connections passive on TCPv4. |
| `\TCPv4\Connections Reset` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for connections reset on TCPv4. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `http.client.open_connections` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.connection.state^network.peer.address^network.protocol.version^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely measures http client open connections. |
| `process.runtime.dotnet.jit.compilation_time` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures process runtime dotnet jit compilation time. |

#### `rpMetrics` (1 metrics)

Very small RP metric surface, mainly raw processor counters.

##### Windows / .NET perf counters

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `\Processor(_Total)\% Processor Time` | `Cluster^DataCenter` | Windows/Geneva performance counter for % processor time on Processor (_Total). |

### Platform & Infrastructure

Node/platform counters plus bridge and gateway service behavior.

#### `PlatformMetrics` (4 metrics)

Basic host infrastructure counters such as CPU, memory, and disk free space.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `Memory\Available MBytes` | `PrimaryStampName^RoleInstance` | Likely measures size, volume, or throughput for memory / available mbytes. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `Process\% Processor Time` | `PrimaryStampName^RoleInstance` | Likely tracks resource usage or capacity for process / % processor time. |
| `Processor\% Processor Time` | `PrimaryStampName^RoleInstance` | Likely tracks resource usage or capacity for processor / % processor time. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `LogicalDisk\Free Megabytes` | `PrimaryStampName^RoleInstance` | Likely measures size, volume, or throughput for logical disk / free megabytes. |

#### `BridgeMetrics` (60 metrics)

Bridge service operational metrics plus host counters and outbound HTTP timings.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `http.client.request.duration` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^http.request.method^http.response.status_code^network.protocol.version^ResourceId^server.address^url.scheme^VirtualClusterName` | Likely measures latency or duration for http client request duration. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.assemblies.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts the current amount of process runtime dotnet assemblies count. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.gc.collections.count` | `Cluster^DataCenter` | Likely counts the current amount of process runtime dotnet gc collections count. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.gc.objects.size` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for process runtime dotnet gc objects size. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process.runtime.dotnet.exceptions.count` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely counts errors, failures, or throttling for process runtime dotnet exceptions count. |

##### Windows / .NET perf counters

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `\LogicalDisk(_Total)\% Free Space` | `Cluster^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Read Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Avg. Disk Write Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (_Total). |
| `\LogicalDisk(_Total)\Current Disk Queue Length` | `Account^Cluster^DataCenter` | Windows/Geneva performance counter for current disk queue length on Logical Disk (_Total). |
| `\LogicalDisk(C:)\% Free Space` | `Cluster^RoleInstance` | Windows/Geneva performance counter for % free space on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (C:). |
| `\LogicalDisk(C:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (C:). |
| `\LogicalDisk(D:)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (D:). |
| `\LogicalDisk(D:)\Current Disk Queue Length` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for current disk queue length on Logical Disk (D:). |
| `\LogicalDisk(HarddiskVolume1)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume1)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume1). |
| `\LogicalDisk(HarddiskVolume2)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume2)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume2). |
| `\LogicalDisk(HarddiskVolume3)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(HarddiskVolume3)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (HarddiskVolume3). |
| `\LogicalDisk(Z:)\% Free Space` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % free space on Logical Disk (Z:). |
| `\LogicalDisk(Z:)\Avg. Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk queue length on Logical Disk (Z:). |
| `\LogicalDisk(Z:)\Avg. Disk Read Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk read queue length on Logical Disk (Z:). |
| `\LogicalDisk(Z:)\Avg. Disk Write Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for avg disk write queue length on Logical Disk (Z:). |
| `\LogicalDisk(Z:)\Current Disk Queue Length` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for current disk queue length on Logical Disk (Z:). |
| `\Memory\Available Bytes` | `Account^CloudName^Cluster^DataCenter^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for available bytes on Memory. |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Received/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes received/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Network Adapter(Microsoft Hyper-V Network Adapter)\Bytes Sent/sec` | `Account^Cluster^RoleInstance` | Windows/Geneva performance counter for bytes sent/sec on Network Adapter (Microsoft Hyper-V Network Adapter). |
| `\Processor(0)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (0). |
| `\Processor(1)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (1). |
| `\Processor(10)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (10). |
| `\Processor(11)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (11). |
| `\Processor(12)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (12). |
| `\Processor(13)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (13). |
| `\Processor(14)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (14). |
| `\Processor(15)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (15). |
| `\Processor(2)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (2). |
| `\Processor(3)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (3). |
| `\Processor(4)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (4). |
| `\Processor(5)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (5). |
| `\Processor(6)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (6). |
| `\Processor(7)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (7). |
| `\Processor(8)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (8). |
| `\Processor(9)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^DeploymentID^DeploymentRing^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (9). |
| `\Processor(_Total)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (_Total). |

#### `MdmBridgeMetrics` (8 metrics)

Curated bridge health and synchronization freshness metrics.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IsBridgeHealthy` | `Account^Cluster^DataCenter` | Health or availability signal for is bridge healthy. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ExternalCallFailure` | `Cluster^ExternalCallType` | Likely counts errors, failures, or throttling for external call failure. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `LastSuccessfulDeltaSync` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures last successful delta sync. |
| `LastSuccessfulFullSync` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures last successful full sync. |
| `LastSuccessfulUpdate` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures last successful update. |
| `SubscriptionsToDelete` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures subscriptions to delete. |
| `TenantsWithSubscriptionsToDelete` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^VirtualClusterName` | Likely measures tenants with subscriptions to delete. |
| `TenantUpdatesProcessed` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ResourceId^TenantUpdateResult^VirtualClusterName` | Likely measures tenant updates processed. |

#### `GatewayMetrics` (2 metrics)

Gateway authentication and throttling metrics.

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `GatewayThrottledRequests` | `ApiPrefix^Cluster^DataCenter` | Gateway requests throttled by policy or load. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `GatewayAuthentications` | `Account^CloudName^Cluster^DataCenter^FailureReason^IdentityType^ResourceId` | Authentication volume through the gateway layer. |

### Billing Metrics

Billing and resource-usage telemetry, dominated by Windows/.NET counters with a few billing-specific metrics.

#### `billingMetrics` (3206 metrics)

Billing/usage namespace dominated by guest and agent performance counters, with a small set of billing-specific job metrics.

This namespace is unusually large and is **mostly Windows / .NET performance counters** collected from billing-related hosts and guest agents rather than bespoke Kusto metrics. For investigation work, focus first on the small set of billing-specific metrics and then use the counter families only when you need host-level evidence.

**Observed patterns**

- The namespace contains 3,206 distinct metric names in the extract; more than 3,200 are Windows/.NET counters repeated across many guest/agent processes.
- The most useful billing-specific metrics are `JobDuration`, `JobRequests`, `JobResult`, `ReportTimeLatency`, and `TotalQuantity`.
- Most sampled rows had no dimensions; when dimensions were present, the common shapes were `(none)`, `Account^Cluster^RoleInstance`, and `Account^Cluster^DataCenter`.

**Common dimension patterns observed**

- `(none)` — observed for 2738 sampled metric definitions
- `Account^Cluster^RoleInstance` — observed for 10 sampled metric definitions
- `Account^Cluster^DataCenter` — observed for 4 sampled metric definitions
- `Cluster^DataCenter` — observed for 1 sampled metric definitions
- `Account^Cluster^DataCenter^Location^MeterCategory^MeterId^Source` — observed for 1 sampled metric definitions
- `Cluster^RoleInstance` — observed for 1 sampled metric definitions
- `Cluster^RoleInstance^Tenant` — observed for 1 sampled metric definitions
- `Account^CloudName^Cluster^DataCenter^Role^RoleInstance^Tenant` — observed for 1 sampled metric definitions

**Key billing-specific metrics**

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `JobDuration` | `(none)` | Likely measures latency or duration for job duration. |
| `JobRequests` | `Account^Cluster^DataCenter` | Likely counts the current amount of job requests. |
| `JobResult` | `Cluster^DataCenter` | Likely measures job result. |
| `ReportTimeLatency` | `Account^Cluster^DataCenter` | Likely measures latency or duration for report time latency. |
| `TotalQuantity` | `Account^Cluster^DataCenter^Location^MeterCategory^MeterId^Source` | Likely measures size, volume, or throughput for total quantity. |

**Representative counter families**

| Representative metric | Why it matters |
|---|---|
| `\Processor(_Total)\% Processor Time` | Windows/Geneva performance counter for % processor time on Processor (_Total). |
| `\Memory\Available Bytes` | Windows/Geneva performance counter for available bytes on Memory. |
| `\LogicalDisk(C:)\% Free Space` | Windows/Geneva performance counter for % free space on Logical Disk (C:). |
| `\.NET CLR Memory(_Global_)\% Time in GC` | Windows/Geneva performance counter for % time in gc on NET CLR Memory (_Global_). |

### Kubernetes/Kuiper Metrics

Container and Kubernetes infrastructure metrics collected from Kuiper/Prometheus exporters.

#### `Kuiper.CgroupExporter` (8 metrics)

cgroup-level Linux container resource metrics for CPU, memory, and IO.

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `kuiper_cgroup_cpu_quota_us` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^Pod^PodName^ResourceId^RoleInstance^VirtualClusterName^worker^Worker` | Likely tracks resource usage or capacity for kuiper cgroup cpu quota us. |
| `kuiper_cgroup_cpu_system_usec_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^Pod^PodName^ResourceId^RoleInstance^VirtualClusterName^worker^Worker` | Likely tracks resource usage or capacity for kuiper cgroup cpu system usec total. |
| `kuiper_cgroup_cpu_user_usec_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^Pod^PodName^ResourceId^RoleInstance^VirtualClusterName^worker^Worker` | Likely tracks resource usage or capacity for kuiper cgroup cpu user usec total. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `kuiper_cgroup_io_write_bytes_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^Pod^PodName^ResourceId^RoleInstance^VirtualClusterName^worker^Worker` | Likely measures size, volume, or throughput for kuiper cgroup io write bytes total. |
| `kuiper_cgroup_memory_anon_bytes` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^Pod^PodName^ResourceId^RoleInstance^VirtualClusterName^worker^Worker` | Likely measures size, volume, or throughput for kuiper cgroup memory anon bytes. |
| `kuiper_cgroup_memory_current_bytes` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^Pod^PodName^ResourceId^RoleInstance^VirtualClusterName^worker^Worker` | Likely measures size, volume, or throughput for kuiper cgroup memory current bytes. |
| `kuiper_cgroup_memory_max_bytes` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^Pod^PodName^ResourceId^RoleInstance^VirtualClusterName^worker^Worker` | Likely measures size, volume, or throughput for kuiper cgroup memory max bytes. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `kuiper_cgroup_cpu_throttled_usec_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^Pod^PodName^ResourceId^RoleInstance^VirtualClusterName^worker^Worker` | Likely counts errors, failures, or throttling for kuiper cgroup cpu throttled usec total. |

#### `Kuiper.MetricsCollector.AzureCNI` (8 metrics)

Azure CNI metrics for IP allocation state and collector process CPU.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `cx_available_ips_v2` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^customer_metric^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures cx available ips v2. |

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process_cpu_seconds_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for process cpu seconds total. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `process_network_receive_bytes_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for process network receive bytes total. |
| `process_network_transmit_bytes_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for process network transmit bytes total. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `cx_allocated_ips_v2` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^customer_metric^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures cx allocated ips v2. |
| `cx_assigned_ips_v2` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^customer_metric^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures cx assigned ips v2. |
| `cx_pending_programming_ips_v2` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^customer_metric^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures cx pending programming ips v2. |
| `cx_pending_release_ips_v2` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^customer_metric^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures cx pending release ips v2. |

#### `Kuiper.MetricsCollector.CoreDNS` (12 metrics)

CoreDNS cache and DNS request metrics.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `coredns_dns_request_duration_seconds_count` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^server^view^VirtualClusterName^zone` | Likely measures latency or duration for coredns dns request duration seconds count. |
| `coredns_dns_request_duration_seconds_sum` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^server^view^VirtualClusterName^zone` | Likely measures latency or duration for coredns dns request duration seconds sum. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `coredns_dns_requests_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^family^PodName^proto^ResourceId^RoleInstance^server^type^view^VirtualClusterName^zone` | Likely counts the current amount of coredns dns requests total. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `coredns_dns_request_size_bytes_count` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^proto^ResourceId^RoleInstance^server^view^VirtualClusterName^zone` | Likely measures size, volume, or throughput for coredns dns request size bytes count. |
| `coredns_dns_request_size_bytes_sum` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^proto^ResourceId^RoleInstance^server^view^VirtualClusterName^zone` | Likely measures size, volume, or throughput for coredns dns request size bytes sum. |
| `coredns_dns_response_size_bytes_count` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^proto^ResourceId^RoleInstance^server^view^VirtualClusterName^zone` | Likely measures size, volume, or throughput for coredns dns response size bytes count. |
| `coredns_dns_response_size_bytes_sum` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^proto^ResourceId^RoleInstance^server^view^VirtualClusterName^zone` | Likely measures size, volume, or throughput for coredns dns response size bytes sum. |

##### Query & cache

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `coredns_cache_entries` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^server^type^view^VirtualClusterName^zones` | Likely measures query or cache behavior for coredns cache entries. |
| `coredns_cache_hits_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^server^type^view^VirtualClusterName^zones` | Likely measures query or cache behavior for coredns cache hits total. |
| `coredns_cache_misses_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^server^view^VirtualClusterName^zones` | Likely measures query or cache behavior for coredns cache misses total. |
| `coredns_cache_requests_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^server^view^VirtualClusterName^zones` | Likely counts the current amount of coredns cache requests total. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `coredns_dns_responses_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^plugin^PodName^rcode^ResourceId^RoleInstance^server^view^VirtualClusterName^zone` | Likely measures coredns dns responses total. |

#### `Kuiper.MetricsCollector.KubeProxy` (11 metrics)

Kube-proxy rule programming and sync duration metrics.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `kubeproxy_network_programming_duration_seconds_count` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^ip_family^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubeproxy network programming duration seconds count. |
| `kubeproxy_network_programming_duration_seconds_sum` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^ip_family^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubeproxy network programming duration seconds sum. |
| `kubeproxy_sync_full_proxy_rules_duration_seconds_count` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^ip_family^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubeproxy sync full proxy rules duration seconds count. |
| `kubeproxy_sync_full_proxy_rules_duration_seconds_sum` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^ip_family^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubeproxy sync full proxy rules duration seconds sum. |
| `kubeproxy_sync_partial_proxy_rules_duration_seconds_count` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^ip_family^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubeproxy sync partial proxy rules duration seconds count. |
| `kubeproxy_sync_partial_proxy_rules_duration_seconds_sum` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^ip_family^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubeproxy sync partial proxy rules duration seconds sum. |
| `kubeproxy_sync_proxy_rules_duration_seconds_count` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^ip_family^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubeproxy sync proxy rules duration seconds count. |
| `kubeproxy_sync_proxy_rules_duration_seconds_sum` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^ip_family^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubeproxy sync proxy rules duration seconds sum. |
| `kubeproxy_sync_proxy_rules_last_timestamp_seconds` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^ip_family^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubeproxy sync proxy rules last timestamp seconds. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `kubeproxy_sync_proxy_rules_endpoint_changes_pending` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kubeproxy sync proxy rules endpoint changes pending. |
| `kubeproxy_sync_proxy_rules_iptables_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^ip_family^PodName^ResourceId^RoleInstance^table^VirtualClusterName` | Likely measures kubeproxy sync proxy rules iptables total. |

#### `Kuiper.MetricsCollector.KubeStateMetricsV2` (41 metrics)

Kubernetes object-state metrics for pods, deployments, daemonsets, jobs, PVCs, and nodes.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `kube_daemonset_status_number_available` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^daemonset^DataCenter^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kube daemonset status number available. |
| `kube_daemonset_status_number_unavailable` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^daemonset^DataCenter^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kube daemonset status number unavailable. |
| `kube_deployment_status_replicas_available` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^deployment^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kube deployment status replicas available. |
| `kube_deployment_status_replicas_unavailable` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^deployment^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kube deployment status replicas unavailable. |
| `kube_statefulset_status_replicas_available` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^statefulset^VirtualClusterName` | Likely measures kube statefulset status replicas available. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `kube_pod_container_resource_requests` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^namespace^node^pod^PodName^resource^ResourceId^RoleInstance^uid^unit^VirtualClusterName` | Likely counts the current amount of kube pod container resource requests. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `kube_node_status_capacity` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^node^PodName^resource^ResourceId^RoleInstance^unit^VirtualClusterName` | Likely tracks resource usage or capacity for kube node status capacity. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `kube_daemonset_status_number_misscheduled` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^daemonset^DataCenter^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kube daemonset status number misscheduled. |
| `kube_daemonset_status_number_ready` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^daemonset^DataCenter^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kube daemonset status number ready. |
| `kube_deployment_status_condition` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^condition^DataCenter^deployment^DeploymentRing^namespace^PodName^reason^ResourceId^RoleInstance^status^VirtualClusterName` | Likely measures kube deployment status condition. |
| `kube_deployment_status_replicas` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^deployment^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kube deployment status replicas. |
| `kube_deployment_status_replicas_ready` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^deployment^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kube deployment status replicas ready. |
| `kube_namespace_status_phase` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^namespace^phase^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kube namespace status phase. |
| `kube_node_info` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container_runtime_version^DataCenter^DeploymentRing^internal_ip^kernel_version^kubelet_version^kubeproxy_version^node^os_image^pod_cidr^PodName^provider_id^ResourceId^RoleInstance^system_uuid^VirtualClusterName` | Likely measures kube node info. |
| `kube_node_status_condition` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^condition^DataCenter^DeploymentRing^node^PodName^ResourceId^RoleInstance^status^VirtualClusterName` | Likely measures kube node status condition. |
| `kube_pod_container_info` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^container_id^DataCenter^DeploymentRing^image^image_id^image_spec^namespace^pod^PodName^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod container info. |
| `kube_pod_container_resource_limits` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^namespace^node^pod^PodName^resource^ResourceId^RoleInstance^uid^unit^VirtualClusterName` | Likely measures kube pod container resource limits. |
| `kube_pod_container_state_started` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^namespace^pod^PodName^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod container state started. |
| `kube_pod_container_status_last_terminated_reason` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^namespace^pod^PodName^reason^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod container status last terminated reason. |
| `kube_pod_container_status_ready` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^namespace^pod^PodName^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod container status ready. |
| `kube_pod_container_status_restarts_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^namespace^pod^PodName^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod container status restarts total. |
| `kube_pod_container_status_running` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^namespace^pod^PodName^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod container status running. |
| `kube_pod_container_status_terminated` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^namespace^pod^PodName^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod container status terminated. |
| `kube_pod_container_status_terminated_reason` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^namespace^pod^PodName^reason^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod container status terminated reason. |
| `kube_pod_container_status_waiting` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^namespace^pod^PodName^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod container status waiting. |
| `kube_pod_container_status_waiting_reason` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^namespace^pod^PodName^reason^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod container status waiting reason. |
| `kube_pod_info` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^created_by_kind^created_by_name^DataCenter^DeploymentRing^host_ip^host_network^namespace^node^pod^pod_ip^PodName^priority_class^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod info. |
| `kube_pod_init_container_status_terminated_reason` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^namespace^pod^PodName^reason^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod init container status terminated reason. |
| `kube_pod_status_phase` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^namespace^phase^pod^PodName^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod status phase. |
| `kube_pod_status_ready` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^condition^DataCenter^DeploymentRing^namespace^pod^PodName^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod status ready. |
| `kube_pod_status_reason` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^namespace^pod^PodName^reason^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod status reason. |
| `kube_pod_status_scheduled` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^condition^DataCenter^DeploymentRing^namespace^pod^PodName^ResourceId^RoleInstance^uid^VirtualClusterName` | Likely measures kube pod status scheduled. |
| `kube_replicaset_spec_replicas` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^namespace^PodName^replicaset^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kube replicaset spec replicas. |
| `kube_replicaset_status_ready_replicas` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^namespace^PodName^replicaset^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kube replicaset status ready replicas. |
| `kube_replicaset_status_replicas` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^namespace^PodName^replicaset^ResourceId^RoleInstance^VirtualClusterName` | Likely measures kube replicaset status replicas. |
| `kube_service_status_load_balancer_ingress` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^hostname^ip^namespace^PodName^ResourceId^RoleInstance^service^uid^VirtualClusterName` | Likely measures kube service status load balancer ingress. |
| `kube_statefulset_replicas` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^statefulset^VirtualClusterName` | Likely measures kube statefulset replicas. |
| `kube_statefulset_status_replicas` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^statefulset^VirtualClusterName` | Likely measures kube statefulset status replicas. |
| `kube_statefulset_status_replicas_current` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^statefulset^VirtualClusterName` | Likely measures kube statefulset status replicas current. |
| `kube_statefulset_status_replicas_ready` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^statefulset^VirtualClusterName` | Likely measures kube statefulset status replicas ready. |
| `kube_statefulset_status_replicas_updated` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^namespace^PodName^ResourceId^RoleInstance^statefulset^VirtualClusterName` | Likely measures kube statefulset status replicas updated. |

#### `Kuiper.MetricsCollector.Kubelet` (11 metrics)

Kubelet operational metrics for CSI, pod start, image pulls, and node startup.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `csi_operations_seconds_count` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^driver_name^grpc_status_code^method_name^migrated^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for csi operations seconds count. |
| `csi_operations_seconds_sum` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^driver_name^grpc_status_code^method_name^migrated^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for csi operations seconds sum. |
| `kubelet_cgroup_manager_duration_seconds_count` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^operation_type^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubelet cgroup manager duration seconds count. |
| `kubelet_cgroup_manager_duration_seconds_sum` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^operation_type^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubelet cgroup manager duration seconds sum. |
| `kubelet_image_pull_duration_seconds_count` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^image_size_in_bytes^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubelet image pull duration seconds count. |
| `kubelet_image_pull_duration_seconds_sum` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^image_size_in_bytes^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubelet image pull duration seconds sum. |
| `kubelet_node_startup_duration_seconds` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubelet node startup duration seconds. |
| `kubelet_pod_start_duration_seconds_count` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubelet pod start duration seconds count. |
| `kubelet_pod_start_duration_seconds_sum` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for kubelet pod start duration seconds sum. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `kubelet_active_pods` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^static^VirtualClusterName` | Likely counts the current amount of kubelet active pods. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `kubelet_desired_pods` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^ResourceId^RoleInstance^static^VirtualClusterName` | Likely measures kubelet desired pods. |

#### `Kuiper.MetricsCollector.NodeExporter` (23 metrics)

Node-exporter host metrics for CPU, disk, filesystem, and memory.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `node_memory_MemAvailable_bytes` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for node memory mem available bytes. |

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `node_cpu_seconds_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^cpu^DataCenter^DeploymentRing^KuiperApp^mode^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for node cpu seconds total. |
| `node_disk_io_time_seconds_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^device^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for node disk io time seconds total. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `node_disk_reads_completed_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^device^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely tracks resource usage or capacity for node disk reads completed total. |
| `node_disk_writes_completed_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^device^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely tracks resource usage or capacity for node disk writes completed total. |
| `node_network_receive_packets_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^device^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely tracks resource usage or capacity for node network receive packets total. |
| `node_network_transmit_packets_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^device^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely tracks resource usage or capacity for node network transmit packets total. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `node_disk_read_bytes_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^device^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for node disk read bytes total. |
| `node_disk_written_bytes_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^device^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for node disk written bytes total. |
| `node_filesystem_avail_bytes` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^device^device_error^fstype^KuiperApp^mountpoint^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for node filesystem avail bytes. |
| `node_filesystem_size_bytes` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^device^device_error^fstype^KuiperApp^mountpoint^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for node filesystem size bytes. |
| `node_memory_MemTotal_bytes` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for node memory mem total bytes. |
| `node_network_receive_bytes_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^device^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for node network receive bytes total. |
| `node_network_transmit_bytes_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^device^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for node network transmit bytes total. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `node_network_receive_drop_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^device^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely counts errors, failures, or throttling for node network receive drop total. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `node_load1` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures node load1. |
| `node_load15` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures node load15. |
| `node_load5` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures node load5. |
| `node_netstat_Tcp_CurrEstab` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures node netstat tcp curr estab. |
| `node_netstat_Tcp_RetransSegs` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures node netstat tcp retrans segs. |
| `node_sockstat_TCP_alloc` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures node sockstat tcp alloc. |
| `node_sockstat_TCP_orphan` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures node sockstat tcp orphan. |
| `node_sockstat_UDP_inuse` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^KuiperApp^nodeImageVersion^nodeVMSize^PodName^ResourceId^RoleInstance^VirtualClusterName` | Likely measures node sockstat udp inuse. |

#### `Kuiper.MetricsCollector.NodeProblemDetector` (1 metrics)

Node problem detector state metric.

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `problem_gauge` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^DataCenter^DeploymentRing^PodName^reason^ResourceId^RoleInstance^type^VirtualClusterName` | Likely measures problem gauge. |

#### `Kuiper.MetricsCollector.cAdvisor` (22 metrics)

Container resource metrics for CPU, filesystem, and memory working set.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `container_cpu_cfs_throttled_seconds_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for container cpu cfs throttled seconds total. |
| `container_cpu_load_average_10s` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for container cpu load average 10s. |
| `container_cpu_usage_seconds_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^cpu^DataCenter^DeploymentRing^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for container cpu usage seconds total. |
| `container_fs_usage_bytes` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^device^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for container fs usage bytes. |
| `container_memory_usage_bytes` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures latency or duration for container memory usage bytes. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `container_memory_mapped_file` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely tracks resource usage or capacity for container memory mapped file. |
| `container_memory_rss` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely tracks resource usage or capacity for container memory rss. |
| `container_memory_swap` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely tracks resource usage or capacity for container memory swap. |
| `container_network_receive_packets_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^interface^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely tracks resource usage or capacity for container network receive packets total. |
| `container_network_transmit_packets_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^interface^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely tracks resource usage or capacity for container network transmit packets total. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `container_fs_limit_bytes` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^device^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for container fs limit bytes. |
| `container_fs_reads_bytes_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^device^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for container fs reads bytes total. |
| `container_fs_writes_bytes_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^device^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for container fs writes bytes total. |
| `container_memory_working_set_bytes` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for container memory working set bytes. |
| `container_network_receive_bytes_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^interface^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for container network receive bytes total. |
| `container_network_transmit_bytes_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^interface^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures size, volume, or throughput for container network transmit bytes total. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `container_memory_failures_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^failure_type^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^scope^VirtualClusterName` | Likely counts errors, failures, or throttling for container memory failures total. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `container_fs_inodes_free` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^device^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures container fs inodes free. |
| `container_fs_inodes_total` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^device^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures container fs inodes total. |
| `container_processes` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures container processes. |
| `container_sockets` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures container sockets. |
| `container_threads` | `_microsoft_metrics_namespace^Account^agentpool^CloudName^Cluster^container^DataCenter^DeploymentRing^id^image^name^namespace^pod^PodName^ProductVersion^ResourceId^RoleInstance^VirtualClusterName` | Likely measures container threads. |

### Synthetics & Monitoring

Synthetic probes and monitoring pipeline health for the Kusto estate.

#### `Canary` (2 metrics)

Simple canary metrics used to verify pipeline or namespace presence.

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `Canary` | `SourceEnvironment^SourceRole^SourceRoleInstance` | Likely measures canary. |
| `MetricNamespaceCanary` | `MetricNamespace^SourceEnvironment^SourceRole^SourceRoleInstance` | Likely measures metric namespace canary. |

#### `HealthSuiteMetrics` (9 metrics)

Health suite metrics for operational latency, table health, ingestion latency, and base memory counters.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `HealthOperationsLatency` | `ResourceId` | Likely measures latency or duration for health operations latency. |
| `IsHealthy` | `ResourceId` | Boolean-style health indicator for the monitored component. |
| `TablesHealth` | `ResourceId` | Likely measures tables health. |

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `TablesIngestionLatency` | `ResourceId` | Likely measures latency or duration for tables ingestion latency. |

##### Windows / .NET perf counters

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `\Memory\Available Bytes` | `Account^CloudName^Cluster^DataCenter^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for available bytes on Memory. |
| `\Memory\Write Copies/sec` | `Cluster` | Windows/Geneva performance counter for write copies/sec on Memory. |
| `\Network Interface(Microsoft Hyper-V Network Adapter _2)\Bytes Total/sec` | `Account^Cluster^DataCenter` | Windows/Geneva performance counter for bytes total/sec on Network Interface (Microsoft Hyper-V Network Adapter _2). |
| `\Network Interface(Microsoft KM-TEST Loopback Adapter)\Bytes Total/sec` | `(none)` | Windows/Geneva performance counter for bytes total/sec on Network Interface (Microsoft KM-TEST Loopback Adapter). |
| `\Processor(_Total)\% Processor Time` | `__Role^__Tenant^Account^CloudName^Cluster^DataCenter^ResourceId^Role^RoleInstance^Tenant` | Windows/Geneva performance counter for % processor time on Processor (_Total). |

#### `Monitoring Agent` (26 metrics)

Monitoring agent self-observability metrics such as CPU, ETW loss, and data delay.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `CpuUsage` | `ClusterName^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | CPU usage reported by the monitoring component. |
| `DataDelayInSeconds` | `EventName^Namespace^Role^Tenant` | Likely measures latency or duration for data delay in seconds. |
| `MemoryUsage` | `ClusterName^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Likely measures latency or duration for memory usage. |
| `StorageFailures` | `AccountName^ClusterName^EventName^Namespace^Node^NodeTypeName^RolloutFQDN^Service^StorageType` | Likely measures latency or duration for storage failures. |
| `StorageRequests` | `AccountName^ClusterName^EventName^Namespace^Node^NodeTypeName^RolloutFQDN^Service^StorageType` | Likely measures latency or duration for storage requests. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `EtwEventsLost` | `ClusterName^Container^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Likely counts errors, failures, or throttling for etw events lost. |
| `EventsDropped` | `ClusterName^Container^EventName^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Likely counts errors, failures, or throttling for events dropped. |
| `ExtensionFailures` | `ClusterName^Name^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Likely counts errors, failures, or throttling for extension failures. |
| `FailedNotificationTask` | `Namespace^Role^Tenant` | Likely counts errors, failures, or throttling for failed notification task. |
| `FailedUploadTasks` | `Namespace^Role^Tenant` | Likely counts errors, failures, or throttling for failed upload tasks. |
| `GigFailures` | `ClusterName^EventName^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Likely counts errors, failures, or throttling for gig failures. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `CommittedGigTickets` | `ClusterName^EventName^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Likely measures committed gig tickets. |
| `EtwEventsLogged` | `ClusterName^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Likely measures etw events logged. |
| `EventsLogged` | `ClusterName^EventName^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Likely measures events logged. |
| `EventsSent` | `ClusterName^EventName^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Likely measures events sent. |
| `GigTicketBackoff` | `(none)` | Likely measures gig ticket backoff. |
| `IssuedGigTickets` | `ClusterName^EventName^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Health or availability signal for issued gig tickets. |
| `MaEventCosts` | `EventName^Namespace^Role^Tenant` | Likely measures ma event costs. |
| `MaOperationCosts` | `Namespace^Operation^Role^Tenant` | Likely measures ma operation costs. |
| `PendingGigTickets` | `EventName^Namespace^Role^Tenant` | Likely measures pending gig tickets. |
| `ServiceRequest` | `ClusterName^Endpoint^Namespace^Node^NodeTypeName^Region^RolloutFQDN^Service^Success^Type` | Likely measures service request. |
| `SucceededNotificationTask` | `ClusterName^EventName^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Likely measures succeeded notification task. |
| `SucceededUploadTasks` | `ClusterName^EventName^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Likely measures succeeded upload tasks. |
| `TimedoutNotificationTask` | `ClusterName^EventName^Namespace^Node^NodeTypeName^RolloutFQDN^Service` | Likely measures timedout notification task. |
| `TimedoutUploadTasks` | `Namespace^Role^Tenant` | Likely measures timedout upload tasks. |
| `UnknownGigTickets` | `(none)` | Likely measures unknown gig tickets. |

#### `MetricsExtension` (5 metrics)

Metric extension pipeline counters for received, lost, dropped, and published aggregates.

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `MetricEtwEventReceivedCount` | `Source^SourceEnvironment^SourceRole^SourceRoleInstance` | Likely counts the current amount of metric etw event received count. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `DroppedRawMetricEventsCountMetric` | `Reason^Source^SourceEnvironment^SourceRole^SourceRoleInstance` | Likely counts errors, failures, or throttling for dropped raw metric events count metric. |
| `MetricAggregatesDroppedCount` | `EndPoint^Reason^SourceEnvironment` | Likely counts errors, failures, or throttling for metric aggregates dropped count. |
| `MetricEtwEventLostCount` | `Reason^Source^SourceEnvironment^SourceRole^SourceRoleInstance` | Likely counts errors, failures, or throttling for metric etw event lost count. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `MetricAggregatesPublished` | `EndPoint^MEVersion^Source^SourceEnvironment^SourceRole^SourceRoleInstance` | Likely measures metric aggregates published. |

#### `MetricsExtension2` (18 metrics)

Second-generation metrics extension metrics for config load, publication queues, ingest counts, and CPU/memory usage.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ConfigurationLoadLatencyInMs` | `SourceEnvironment^Type` | Likely measures latency or duration for configuration load latency in ms. |
| `MetricsPipelineLatencyInMs` | `EndPoint^SourceEnvironment^Stage` | Likely measures latency or duration for metrics pipeline latency in ms. |
| `ProcessCpuUsagePercentage` | `SourceEnvironment` | Likely measures latency or duration for process cpu usage percentage. |
| `ProcessUptimeSeconds` | `MeVersion^SourceEnvironment` | Likely measures latency or duration for process uptime seconds. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `CardinalityOverflowCount` | `Metric^Namespace^SourceEnvironment` | Likely counts the current amount of cardinality overflow count. |
| `MetricAggregatesPublishedCount` | `Destination^EndPoint^SourceEnvironment` | Likely counts the current amount of metric aggregates published count. |
| `MetricEventsPublishedCount` | `Destination^EndPoint^SourceEnvironment` | Likely counts the current amount of metric events published count. |
| `MetricsMetadataPublishedCount` | `Destination^EndPoint^SourceEnvironment` | Likely counts the current amount of metrics metadata published count. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `MetricPublicationQueueLength` | `EndPoint^SourceEnvironment` | Likely counts the current amount of metric publication queue length. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `MemoryAreaSizeInBytes` | `SourceEnvironment^Type` | Likely measures size, volume, or throughput for memory area size in bytes. |
| `ProcessMemorySizeInBytes` | `SourceEnvironment^Type` | Likely measures size, volume, or throughput for process memory size in bytes. |

##### Ingestion pipeline

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `MetricsIngestedCount` | `Protocol^SourceEnvironment^Transport` | Likely counts the current amount of metrics ingested count. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `MeErrorsCount` | `Reason^SourceEnvironment^SourceRole^SourceRoleInstance^Type` | Likely counts errors, failures, or throttling for me errors count. |
| `MetricAggregatesDroppedCount` | `EndPoint^Reason^SourceEnvironment` | Likely counts errors, failures, or throttling for metric aggregates dropped count. |
| `MetricEventsDroppedCount` | `EndPoint^Reason^SourceEnvironment` | Likely counts errors, failures, or throttling for metric events dropped count. |
| `MetricsLostCount` | `Not observed in sampled dimension extracts` | Likely counts errors, failures, or throttling for metrics lost count. |
| `PublicationFailedCount` | `EndPoint^Reason^SourceEnvironment` | Likely counts errors, failures, or throttling for publication failed count. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `AuthLifetimeLeftMin` | `Id^SourceEnvironment` | Likely measures auth lifetime left min. |

#### `SyntheticsBridgeMetrics` (1 metrics)

Synthetic probes for bridge availability.

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IsServiceAlive` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ErrorCode^ResourceId` | Boolean-style synthetic probe indicating whether the service responded. |

#### `SyntheticsClusterManagementMetrics` (1 metrics)

Synthetic probes for CM availability.

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IsServiceAlive` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ErrorCode^ResourceId` | Boolean-style synthetic probe indicating whether the service responded. |

#### `SyntheticsDataManagementMetrics` (6 metrics)

Synthetic DM probes for service, hoster, configuration, and virtual-cluster ingestion.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ConfigurationHealthy` | `Cluster^DataCenter^ErrorCode` | Health or availability signal for configuration healthy. |
| `GetResourcesHealthy` | `Cluster^DataCenter^ErrorCode^ResourceId` | Health or availability signal for get resources healthy. |

##### Ingestion pipeline

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `isVirtualClusterIngest` | `Cluster^DataCenter^DeploymentRing^ErrorCode` | Health or availability signal for is virtual cluster ingest. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IsDataMgmtAlive` | `Account^Cluster^DataCenter^DeploymentRing^ErrorCode^ResourceId` | Health or availability signal for is data mgmt alive. |
| `IsHosterServiceAlive` | `Cluster^DataCenter^DeploymentRing^ErrorCode` | Health or availability signal for is hoster service alive. |
| `IsServiceAlive` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ErrorCode^ResourceId` | Boolean-style synthetic probe indicating whether the service responded. |

#### `SyntheticsEngineMetrics` (51 metrics)

Synthetic engine probes and capacity metrics mirroring critical engine-state indicators.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IsRowStoreUnhealthy` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^Details^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Health or availability signal for is row store unhealthy. |

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `HotDataDiskSpaceUsage` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures latency or duration for hot data disk space usage. |
| `MinPartitioningPercentageInSingleTable` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures latency or duration for min partitioning percentage in single table. |
| `RowStoreLocalStorageCapacityFactor` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures latency or duration for row store local storage capacity factor. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ClusterDataCapacityFactor` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for cluster data capacity factor. |
| `GraphSnapshotsLoadFactor` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for graph snapshots load factor. |
| `InstancesTargetBasedOnDataCapacity` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for instances target based on data capacity. |
| `V3DataCapacityFactor` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for v3 data capacity factor. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ExtentsSize` | `Account^Caching^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^StorageKind^VirtualClusterName` | Total size of extents for the selected scope or tier. |
| `TotalExtentSize` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Combined size of all extents in the selected scope. |
| `TotalOriginalDataSize` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures size, volume, or throughput for total original data size. |

##### Query & cache

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IsEngineAnsweringQuery` | `DataCenter` | Health or availability signal for is engine answering query. |
| `isVirtualClusterAnsweringQuery` | `Cluster^DataCenter^DeploymentRing^ErrorCode` | Health or availability signal for is virtual cluster answering query. |
| `QueryAccelerationCapacityUtilization` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for query acceleration capacity utilization. |
| `QueryAccelerationOperationsInProgress` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely counts the current amount of query acceleration operations in progress. |
| `QueryAccelerationOperationsLoadFactor` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for query acceleration operations load factor. |
| `StoredQueryResultsInProgress` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures query or cache behavior for stored query results in progress. |

##### Ingestion pipeline

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IngestionCapacityUtilization` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for ingestion capacity utilization. |
| `IngestionsInProgress` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures ingestion pipeline behavior for ingestions in progress. |
| `IngestionsLoadFactor` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for ingestions load factor. |
| `IngestionsSuccessRate` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Success-rate metric for ingestions success rate. |
| `RowStoreSealsInProgress` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures ingestion pipeline behavior for row store seals in progress. |

##### Data layout & storage

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `DataPartitioningLoadFactor` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for data partitioning load factor. |
| `DataPartitioningOperationsInProgress` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely counts the current amount of data partitioning operations in progress. |
| `ExportsInProgress` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures storage layout or data-management work for exports in progress. |
| `ExportsLoadFactor` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for exports load factor. |
| `ExtendedExtentsTotal` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ExtentsKind^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures storage layout or data-management work for extended extents total. |
| `ExtentsCount` | `Account^Caching^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^StorageKind^VirtualClusterName` | Count of extents for the selected scope or tier. |
| `ExtentsTotal` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Total number of extents across the selected scope. |
| `MaterializedViewsInProgress` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures storage layout or data-management work for materialized views in progress. |
| `MaterializedViewsLoadFactor` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for materialized views load factor. |
| `MaxContinuousExportLatenessMinutes` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures storage layout or data-management work for max continuous export lateness minutes. |
| `MaxMirroringPolicyJobsLatenessMinutes` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely counts the current amount of max mirroring policy jobs lateness minutes. |
| `MergesInProgress` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures storage layout or data-management work for merges in progress. |
| `MergesLoadFactor` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for merges load factor. |
| `MergesSuccessRate` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Success-rate metric for merges success rate. |
| `MirroringOperationsInProgress` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely counts the current amount of mirroring operations in progress. |
| `MirroringOperationsLoadFactor` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for mirroring operations load factor. |
| `NumberOfDatabases` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely counts the current amount of number of databases. |
| `PendingContinuousExports` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for pending continuous exports. |
| `PendingMirroringPolicyJobs` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely counts the current amount of pending mirroring policy jobs. |
| `PurgeExtentsRebuildInProgress` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures storage layout or data-management work for purge extents rebuild in progress. |
| `PurgeExtentsRebuildLoadFactor` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely tracks resource usage or capacity for purge extents rebuild load factor. |
| `PurgesInProgress` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures storage layout or data-management work for purges in progress. |
| `ShardsWarmingTemperature` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures storage layout or data-management work for shards warming temperature. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `GraphSnapshotsInProgress` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures graph snapshots in progress. |
| `IsEngineAlive` | `Account^Cluster^DataCenter` | Health or availability signal for is engine alive. |
| `IsHosterServiceAlive` | `Cluster^DataCenter^DeploymentRing^ErrorCode` | Health or availability signal for is hoster service alive. |
| `IsServiceAlive` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ErrorCode^ResourceId` | Boolean-style synthetic probe indicating whether the service responded. |
| `MachinesOffline` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures machines offline. |
| `MachinesTotal` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^metricNamespace^monitoringAccount^ResourceId^VirtualClusterName` | Likely measures machines total. |

#### `SyntheticsPlatformMetrics` (1 metrics)

Synthetic execution-time metric for platform checks.

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `TotalExecutionTime` | `DataCenter` | Likely measures total execution time. |

#### `SyntheticsResourceProviderMetrics` (2 metrics)

Synthetic RP availability and ARM-call probe metrics.

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ArmRpCallJob` | `Cluster^DataCenter^DeploymentRing^ErrorCode` | Likely measures arm rp call job. |
| `IsServiceAlive` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ErrorCode^ResourceId` | Boolean-style synthetic probe indicating whether the service responded. |

#### `SyntheticsSaasResourceProviderMetrics` (1 metrics)

Synthetic SaaS RP availability probes.

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IsServiceAlive` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ErrorCode^ResourceId` | Boolean-style synthetic probe indicating whether the service responded. |

#### `SyntheticsServiceProbeMetrics` (1 metrics)

Synthetic service-probe availability metric.

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `IsServiceAlive` | `Account^CloudName^Cluster^DataCenter^DeploymentRing^ErrorCode^ResourceId` | Boolean-style synthetic probe indicating whether the service responded. |

### Other

Miscellaneous namespaces that do not fit the core Kusto service buckets.

#### `OneLakeClient` (7 metrics)

OneLake client latency and throughput metrics for read/write/billing operations.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BillingLatencyInMs` | `http_status_code^onelake_client_environment^onelake_client_workload_name^service_version` | Likely measures latency or duration for billing latency in ms. |
| `IncomingRequestLatencyInMs` | `http_status_code^onelake_client_adls_operation^onelake_client_environment^onelake_client_route_type^onelake_client_shortcut_index_account_type^onelake_client_workload_name` | Likely measures latency or duration for incoming request latency in ms. |
| `OperationLatencyInMs` | `http_status_code^onelake_client_adls_operation^onelake_client_route_type^onelake_client_size_bucket^onelake_client_workload_name^service_version` | Likely measures latency or duration for operation latency in ms. |
| `PathInfoLatencyInMS` | `http_status_code^onelake_client_environment^onelake_client_workload_name^service_version` | Likely measures latency or duration for path info latency in ms. |
| `ShortcutIndexLatencyInMs` | `http_status_code^onelake_client_environment^onelake_client_workload_name^service_version` | Likely measures latency or duration for shortcut index latency in ms. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `OperationReadThroughputInMbPerSec` | `http_status_code^onelake_client_adls_operation^onelake_client_route_type^onelake_client_size_bucket^onelake_client_workload_name^service_version` | Likely measures size, volume, or throughput for operation read throughput in mb per sec. |
| `OperationWriteThroughputInMbPerSec` | `http_status_code^onelake_client_adls_operation^onelake_client_route_type^onelake_client_size_bucket^onelake_client_workload_name^service_version` | Likely measures size, volume, or throughput for operation write throughput in mb per sec. |

#### `OrchestrationsMetrics` (8 metrics)

Durable orchestration/activity metrics, especially queue latency and orchestration duration.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ActivityDuration` | `ActivityName^ActivityState^ActivityVersion^Cluster^DataCenter^DeploymentRing` | Likely measures latency or duration for activity duration. |
| `OrchestrationControlQueueLatency` | `Cluster^DataCenter^QueueName^TaskHubName` | Likely measures latency or duration for orchestration control queue latency. |
| `OrchestrationDuration` | `Cluster^DataCenter^DeploymentRing^OrchestrationName^OrchestrationState^OrchestrationVersion` | Likely measures latency or duration for orchestration duration. |
| `OrchestrationWorkItemQueueLatency` | `Cluster^DataCenter^QueueName^TaskHubName` | Likely measures latency or duration for orchestration work item queue latency. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `OrchestrationControlQueueLength` | `Cluster^DataCenter^QueueName^TaskHubName` | Likely counts the current amount of orchestration control queue length. |
| `OrchestrationWorkItemQueueLength` | `Cluster^DataCenter^QueueName^TaskHubName` | Likely counts the current amount of orchestration work item queue length. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ActivityStarted` | `ActivityName^ActivityVersion^Cluster^DataCenter^DeploymentRing` | Likely measures activity started. |
| `OrchestrationStarted` | `Cluster^DataCenter^DeploymentRing^OrchestrationName^OrchestrationVersion` | Likely measures orchestration started. |

#### `CommandMetrics` (1 metrics)

Command-level throttling metric.

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `CommandThrottled` | `Account^Cluster^CommandType^DataCenter^ResourceId` | Count of commands throttled by service limits. |

#### `DefaultNamespace` (26 metrics)

Uncategorized/default Geneva metrics, often related to batching, ingestion size, and operation duration.

##### Health & availability

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `SkuAvailability` | `otel.metric.overflow` | Health or availability signal for sku availability. |
| `UnallocatedSubscriptionsAvailableUsage` | `otel.metric.overflow` | Likely measures latency or duration for unallocated subscriptions available usage. |
| `UnallocatedSubscriptionsSkuAvailability` | `otel.metric.overflow` | Health or availability signal for unallocated subscriptions sku availability. |
| `UnavailableDatabases` | `(none)` | Likely measures storage layout or data-management work for unavailable databases. |

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BatchPeriodSeconds` | `otel.metric.overflow` | Likely measures latency or duration for batch period seconds. |
| `EventHubEventAgeSeconds` | `otel.metric.overflow` | Likely measures latency or duration for event hub event age seconds. |
| `IngestedEventAgeSeconds` | `otel.metric.overflow` | Likely measures latency or duration for ingested event age seconds. |
| `MessageAgeInPipelineSeconds` | `otel.metric.overflow` | Likely measures latency or duration for message age in pipeline seconds. |
| `OperationDuration` | `otel.metric.overflow` | Duration of the named operation. |
| `StorageArtifactsCleanupOperationResult` | `Not observed in sampled dimension extracts` | Likely measures latency or duration for storage artifacts cleanup operation result. |
| `UnallocatedSubscriptionsCurrentUsage` | `otel.metric.overflow` | Likely measures latency or duration for unallocated subscriptions current usage. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ActiveServiceInstances` | `otel.metric.overflow` | Count of active service instances reporting for the component. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BlockUtilization` | `otel.metric.overflow` | Likely tracks resource usage or capacity for block utilization. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BatchSizeBytes` | `otel.metric.overflow` | Likely measures size, volume, or throughput for batch size bytes. |
| `BlockInputQueueSize` | `otel.metric.overflow` | Likely measures size, volume, or throughput for block input queue size. |
| `BlockOutputQueueSize` | `otel.metric.overflow` | Likely measures size, volume, or throughput for block output queue size. |
| `IngestSizeBytes` | `(none)` | Bytes processed by ingestion. |

##### Ingestion pipeline

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BatchBlobCount` | `otel.metric.overflow` | Likely counts the current amount of batch blob count. |
| `BatchesProcessed` | `otel.metric.overflow` | Likely measures ingestion pipeline behavior for batches processed. |
| `BlobsProcessed` | `otel.metric.overflow` | Likely measures ingestion pipeline behavior for blobs processed. |
| `BlobsReceived` | `otel.metric.overflow` | Likely measures ingestion pipeline behavior for blobs received. |

##### Errors & throttling

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BlobsDropped` | `otel.metric.overflow` | Likely counts errors, failures, or throttling for blobs dropped. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BlockDegreeOfParallelism` | `otel.metric.overflow` | Likely measures block degree of parallelism. |
| `EventsReceived` | `otel.metric.overflow` | Likely measures events received. |
| `TridentFetchPrivateLinkState` | `otel.metric.overflow` | Likely measures trident fetch private link state. |
| `VirtualClusterState` | `otel.metric.overflow` | Likely measures virtual cluster state. |

#### `Microsoft/Web/AppServicePlans` (21 metrics)

Azure App Service Plan platform metrics surfaced through MDM.

##### Latency & duration

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `CpuPercentage` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures latency or duration for cpu percentage. |
| `MemoryPercentage` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures latency or duration for memory percentage. |

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `ActiveRequests` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely counts the current amount of active requests. |
| `HttpQueueLength` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely counts the current amount of http queue length. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `DiskQueueLength` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely counts the current amount of disk queue length. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BytesReceived` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for bytes received. |
| `BytesSent` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for bytes sent. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `SocketInboundAll` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures socket inbound all. |
| `SocketLoopback` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures socket loopback. |
| `SocketOutboundAll` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures socket outbound all. |
| `SocketOutboundEstablished` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures socket outbound established. |
| `SocketOutboundTimeWait` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures socket outbound time wait. |
| `TcpCloseWait` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures tcp close wait. |
| `TcpClosing` | `Not observed in sampled dimension extracts` | Likely measures tcp closing. |
| `TcpEstablished` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures tcp established. |
| `TcpFinWait1` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures tcp fin wait1. |
| `TcpFinWait2` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures tcp fin wait2. |
| `TcpLastAck` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures tcp last ack. |
| `TcpSynReceived` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures tcp syn received. |
| `TcpSynSent` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures tcp syn sent. |
| `TcpTimeWait` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures tcp time wait. |

#### `Microsoft/Web/WebApps` (38 metrics)

Azure Web App runtime and request metrics surfaced through MDM.

##### Counts & concurrency

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `Requests` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely counts the current amount of requests. |
| `StopRequests` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely counts the current amount of stop requests. |

##### Resource utilization

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `CpuTime` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely tracks resource usage or capacity for cpu time. |
| `CurrentMemoryWorkingSet` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely tracks resource usage or capacity for current memory working set. |
| `ScmCpuTime` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely tracks resource usage or capacity for scm cpu time. |

##### Size & throughput

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `BillableIncomingRequestResponseBytes` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for billable incoming request response bytes. |
| `IncomingRequestBytes` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for incoming request bytes. |
| `IncomingRequestResponseBytes` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for incoming request response bytes. |
| `IoOtherBytesPerSecond` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for io other bytes per second. |
| `IoReadBytesPerSecond` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for io read bytes per second. |
| `IoWriteBytesPerSecond` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for io write bytes per second. |
| `LocalReadBytes` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for local read bytes. |
| `LocalWrittenBytes` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for local written bytes. |
| `NetworkReadBytes` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for network read bytes. |
| `NetworkWrittenBytes` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for network written bytes. |
| `OutgoingRequestBytes` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for outgoing request bytes. |
| `OutgoingRequestResponseBytes` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for outgoing request response bytes. |
| `PrivateBytes` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for private bytes. |
| `ScmPrivateBytes` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures size, volume, or throughput for scm private bytes. |

##### Other

| Metric | Dimensions | Likely meaning |
|---|---|---|
| `AppConnections` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures app connections. |
| `CurrentAssemblies` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures current assemblies. |
| `Gen0Collections` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures gen0 collections. |
| `Gen1Collections` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures gen1 collections. |
| `Gen2Collections` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures gen2 collections. |
| `Handles` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures handles. |
| `Http2xx` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures http2xx. |
| `Http403` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures http403. |
| `Http404` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures http404. |
| `Http4xx` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures http4xx. |
| `IoOtherOperationsPerSecond` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures io other operations per second. |
| `IoReadOperationsPerSecond` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures io read operations per second. |
| `IoWriteOperationsPerSecond` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures io write operations per second. |
| `MaxResponseTime` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures max response time. |
| `MinResponseTime` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures min response time. |
| `ResponseTime` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures response time. |
| `Threads` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures threads. |
| `TotalAppDomains` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures total app domains. |
| `TotalAppDomainsUnloaded` | `Microsoft.RegionName^Microsoft.ResourceId^ResourceId^ServerName^StampName` | Likely measures total app domains unloaded. |

## Common Query Patterns

### Check cluster CPU usage over time

```kusto
KustoMdmMetricsV1()
| where TIMESTAMP > ago(24h)
| where Cluster == toupper('<cluster>')
| where metricNamespace == 'engineMetrics'
| where metricName == '\\Processor(_Total)\\% Processor Time'
| summarize avgCpu = avg(maxValue), peakCpu = max(maxValue) by bin(TIMESTAMP, 5m), RoleInstance
| render timechart
```

### Monitor ingestion latency

```kusto
KustoMdmMetricsV1()
| where TIMESTAMP > ago(24h)
| where Cluster == toupper('<cluster>')
| where metricNamespace == 'KustoIngestion'
| where metricName in ('LatencyInSeconds', 'ComponentLatencyInSeconds')
| summarize avgLatencySec = avg(sumValue / iff(countValue == 0, 1.0, todouble(countValue))), peakLatencySec = max(maxValue) by metricName, bin(TIMESTAMP, 10m)
| render timechart
```

### Track query performance

```kusto
KustoMdmMetricsV1()
| where TIMESTAMP > ago(24h)
| where Cluster == toupper('<cluster>')
| where metricNamespace == 'QueryMetrics'
| where metricName in ('QueryDuration', 'ConcurrentQueries', 'QueryThrottled')
| summarize value = avg(sumValue / iff(countValue == 0, 1.0, todouble(countValue))) by metricName, bin(TIMESTAMP, 5m)
| render timechart
```

### Monitor cache footprint / hit-style counters

```kusto
let hotCache = KustoMdmMetricsV1()
| where TIMESTAMP > ago(24h)
| where Cluster == toupper('<cluster>')
| where metricNamespace == 'MdmEngineMetrics'
| where metricName == 'HotCacheSizeInBytes'
| summarize hotCacheBytes = max(maxValue) by bin(TIMESTAMP, 10m);
let dnsCacheHitRate = KustoMdmMetricsV1()
| where TIMESTAMP > ago(24h)
| where metricNamespace == 'Kuiper.MetricsCollector.CoreDNS'
| where metricName in ('coredns_cache_hits_total', 'coredns_cache_requests_total')
| summarize value = max(maxValue) by metricName, bin(TIMESTAMP, 10m)
| evaluate pivot(metricName, take_any(value))
| extend cacheHitRate = todouble(coredns_cache_hits_total) / iff(coredns_cache_requests_total == 0, 1.0, todouble(coredns_cache_requests_total));
hotCache
| join kind=fullouter dnsCacheHitRate on TIMESTAMP
```

### Check extent counts

```kusto
KustoMdmMetricsV1()
| where TIMESTAMP > ago(24h)
| where Cluster == toupper('<cluster>')
| where metricNamespace == 'MdmEngineMetrics'
| where metricName in ('ExtentsCount', 'ExtentsSize', 'ExtentsTotal', 'TotalExtentSize')
| summarize latestValue = arg_max(TIMESTAMP, maxValue) by metricName, dimensionValueList
```

### Monitor streaming ingestion

```kusto
KustoMdmMetricsV1()
| where TIMESTAMP > ago(24h)
| where Cluster == toupper('<cluster>')
| where metricNamespace == 'StreamingIngestionMetrics'
| where metricName in ('ConcurrentIngests', 'ConcurrentSeals', 'IngestDuration', 'IngestSizeBytes', 'StreamingIngestionAvailableLocalStoragePercent', 'StreamingIngestionLocalStorageBytes')
| summarize value = max(maxValue) by metricName, bin(TIMESTAMP, 5m)
| render timechart
```

## Tips

- Always filter by `TIMESTAMP` first to avoid scanning too much data.
- Use `metricNamespace` early; it is the fastest way to cut the search space from thousands of metrics to a focused set.
- `dimensionNameList` and `dimensionValueList` use `^` as the separator; parse them together so the positions stay aligned.
- Values are pre-aggregated. Use `sumValue / countValue` for averages, `minValue`/`maxValue` for ranges, and `sumOfSquaresValue` when you need variance-style calculations.
- `KustoMdmMetricsV1()` is a cross-cluster wrapper over Kuskus entity groups, so always add a `Cluster` filter when investigating one cluster.
- For per-node investigations, filter on `RoleInstance` directly when populated, or parse it from `dimensionValueList` when the metric keeps it only as a dimension.
- When dimensions are missing in this guide, that means they were not present in the supplied dimension extracts; the live metric may still carry dimensions in Kusto.

