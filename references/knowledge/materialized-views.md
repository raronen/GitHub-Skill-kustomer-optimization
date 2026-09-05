# Materialized view-like functions

These are the functions that look like MV entry points in this database. The live metadata call `.show materialized-views` returned no rows, so this file documents MV-style query surfaces exposed as functions.

## Querying pattern

Most of these can be queried directly as functions, for example:

```kusto
DimClustersMv() | take 10
UsageDailyMv() | summarize count() by bin(Timestamp, 1d)
DataIngestHistoryMv() | take 10
```

## `DataCapacityHistoryMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DataCapacityHistoryMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DataCapacityHistoryMv
    )
 }
```

## `DataIngestHistoryMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DataIngestHistoryMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DataIngestHistoryMv
    )
 }
```

## `DataOperationsHistoryMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DataOperationsHistoryMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DataOperationsHistoryMv
    )
 }
```

## `DimClustersDailyMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DimClustersDailyMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DimClustersDailyMv
    )
 }
```

## `DimClustersMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DimClustersMv() | take 10`
- Notes: Composed function with custom logic.
- **CustomerType**: Use the `CustomerType` column to distinguish external vs. internal customers.
  - `CustomerType == "External"` → external (paying) customer
  - `CustomerType == "Internal"` → Microsoft-internal cluster
  - Example: `DimClustersMv() | where ClusterName == "<cluster>" | project ClusterName, CustomerType`

```kusto
{
     let EUS2Regions = datatable(Region: string)
[
    "East US 2", "West US", "South Central US", "West US 3", 
    "Southwest US" 
];
     let SEASRegions = datatable(Region: string)
[
    "Southeast Asia"
];
     let movedRegions = EUS2Regions | union SEASRegions;
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DimClustersMv
        | where (Region in (EUS2Regions) and Kuskus.$current_cluster_endpoint contains 'EUS2') 
            or (Region in (SEASRegions) and Kuskus.$current_cluster_endpoint contains 'SEAS') 
            or not(Region in (movedRegions))
    )
 }
```

## `DmSettingsMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DmSettingsMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DmSettingsMv
    )
}
```

## `execute_on_owning_cm`

- Folder: `OPS`
- Parameters: `(service:string, cmd:string)`
- Docstring: Execute commands on the CM owning a specific service
- Usage example: `execute_on_owning_cm('service-value', 'cmd-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     let CM=toscalar(
        DimClustersMv
        | where Source == toscalar(GetTridentServiceNameFromClusterAlias(service))
        | project CmConnectionString
        | take 1);
     evaluate execute_show_command(CM, cmd)
 }
```

## `execute_on_service`

- Folder: `OPS`
- Parameters: `(service:string, cmd:string)`
- Docstring: Execute commands a service based on its name
- Usage example: `execute_on_service('service-value', 'cmd-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     let SVC=toscalar(
        DimClustersMv
        | where Source == toscalar(GetTridentServiceNameFromClusterAlias(service))
        | project ServiceConnectionString);
     evaluate execute_show_command(SVC, cmd)
 }
```

## `ExtendedHealthDashboard`

- Folder: `OPS`
- Parameters: `(_source:string, _region:string)`
- Docstring: Generate Jarvis Dashboard Links
- Usage example: `ExtendedHealthDashboard('_source-value', '_region-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     union withsource=SourceTable
        DimClustersMv(),
        cluster("kuskusdfv3").database("KuskusFF").DimClustersMv,
        cluster("kuskusdfv3").database("KuskusMC").DimClustersMv
    | where Source =~ _source and Region =~ _region and Kind in("Engine", "DataManagement")
    | extend cluster = toupper(ServiceConfiguration.ProfileName)
    | extend mdmAccount = ServiceConfiguration.MonitoringAccount
    | extend MainMdmAccount = iff
                              (
                                  ServiceConfiguration.ServiceConnectionString has "kusto.usgovcloudapi.net",
                                  "KustoProdFF",
                                  iff(ServiceConfiguration.ServiceConnectionString has "kusto.chinacloudapi.cn", "KustoProdMC", "KustoProd")
                              )
    | extend engineDashboad = strcat
                              (
                                  "https://jarvis-west.dc.ad.msft.net/dashboard/KustoProd/MdmEngineMetrics/engine%2520health%2520V3?overrides=%5B%7B%22query%22:%22//dataSources%22,%22key%22:%22account%22,%22replacement%22:%22",
                                  mdmAccount,
                                  "%22%7D,%7B%22query%22:%22//*%5Bid=%27Cluster%27%5D%22,%22key%22:%22value%22,%22replacement%22:%22",
                                  cluster,
                                  "%22%7D%5D%20"
                              )
    | extend dmDashboard = strcat
                           (
                               "https://jarvis-west.dc.ad.msft.net/dashboard/KustoProd/MdmDataMgmtMetrics/DM%2520health%2520v3?overrides=%5B%7B%22query%22:%22//dataSources%22,%22key%22:%22account%22,%22replacement%22:%22",
                               mdmAccount,
                               "%22%7D,%7B%22query%22:%22//*%5Bid=%27Cluster%27%5D%22,%22key%22:%22value%22,%22replacement%22:%22INGEST-",
                               cluster,
                               "%22%7D%5D%20"
                           )
    | extend kustoDashboard = strcat("https://kustodashboard.azurewebsites.net/#/profile/", cluster, "/360?")
    | extend alertsDashboard = strcat
                               (
                                   "https://jarvis-west.dc.ad.msft.net/dashboard/KustoProd/MdmEngineMetrics/Alerts?overrides=%5B%7B%22query%22:%22//dataSources%22,%22key%22:%22account%22,%22replacement%22:%22",
                                   MainMdmAccount,
                                   "%22%7D,%7B%22query%22:%22//*%5Bid=%27Cluster%27%5D%22,%22key%22:%22value%22,%22replacement%22:%22",
                                   cluster,
                                   "%22%7D%5D%20"
                               )
    | extend dmDashboardv4 = strcat
                             (
                                 "https://portal.microsoftgeneva.com/dashboard/KustoProd/MdmDataMgmtMetrics/DM%2520health%2520v4?overrides=[{%22query%22:%22//dataSources%22,%22key%22:%22account%22,%22replacement%22:%22",
                                 mdmAccount,
                                 "%22},{%22query%22:%22//*[id%3D%27Cluster%27]%22,%22key%22:%22value%22,%22replacement%22:%22",
                                 cluster,
                                 ",INGEST-",
                                 cluster,
                                 "%22}]%20"
                             )
    | extend dmDashboardLogsv4 = strcat
                                 (
                                     "https://portal.microsoftgeneva.com/dashboard/KustoProd/MdmDataMgmtMetrics/DM%2520health%2520v4-%2520Kuskus%2520Appendices?overrides=[{%22query%22:%22//dataSources%22,%22key%22:%22account%22,%22replacement%22:%22",
                                     mdmAccount,
                                     "%22},{%22query%22:%22//*[id%3D%27Cluster%27]%22,%22key%22:%22value%22,%22replacement%22:%22",
                                     cluster,
                                     ",INGEST-",
                                     cluster,
                                     "%22}]%20"
                                 )
    | project
        engineDashboad,
        dmDashboard,
        kustoDashboard,
        alertsDashboard,
        dmDashboardv4,
        dmDashboardLogsv4//, cluster
 }
```

## `ExtendedHealthDashboardForDM`

- Folder: `OPS`
- Parameters: `(_source:string, _region:string)`
- Docstring: Generate Jarvis Additional DM Dashboard Links
- Usage example: `ExtendedHealthDashboardForDM('_source-value', '_region-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     union
        DimClustersMv(),
        cluster("kuskusdfv3").database("KuskusFF").DimClustersMv,
        cluster("kuskusdfv3").database("KuskusMC").DimClustersMv
    | where Source !has _source
        and Region =~ _region
        and Kind in("DataManagement")
        and ServiceConfiguration.DmSettings.EngineUri has _source
    | extend EngineUri = tostring(parse_json(ServiceConfiguration.DmSettings.EngineUri))
    | extend Engine = split(parse_url(tostring(EngineUri)).Host, ".", 0)
    | where Engine[0] has _source
    | extend cluster = toupper(ServiceConfiguration.ProfileName)
    | extend mdmAccount = ServiceConfiguration.MonitoringAccount
    | extend MainMdmAccount = iff
                              (
                                  ServiceConfiguration.ServiceConnectionString has "kusto.usgovcloudapi.net",
                                  "KustoProdFF",
                                  iff(ServiceConfiguration.ServiceConnectionString has "kusto.chinacloudapi.cn", "KustoProdMC", "KustoProd")
                              )
    | extend dmDashboard = strcat
                           (
                               "https://jarvis-west.dc.ad.msft.net/dashboard/KustoProd/MdmDataMgmtMetrics/DM%2520health%2520v3?overrides=%5B%7B%22query%22:%22//dataSources%22,%22key%22:%22account%22,%22replacement%22:%22",
                               mdmAccount,
                               "%22%7D,%7B%22query%22:%22//*%5Bid=%27Cluster%27%5D%22,%22key%22:%22value%22,%22replacement%22:%22",
                               Source,
                               "%22%7D%5D%20"
                           )
    | extend alertsDashboard = strcat
                               (
                                   "https://jarvis-west.dc.ad.msft.net/dashboard/KustoProd/MdmEngineMetrics/Alerts?overrides=%5B%7B%22query%22:%22//dataSources%22,%22key%22:%22account%22,%22replacement%22:%22",
                                   MainMdmAccount,
                                   "%22%7D,%7B%22query%22:%22//*%5Bid=%27Cluster%27%5D%22,%22key%22:%22value%22,%22replacement%22:%22",
                                   cluster,
                                   "%22%7D%5D%20"
                               )
    | project Source, dmDashboard, alertsDashboard
    | take 10
 }
```

## `GetClusterOwners`

- Folder: `Info`
- Parameters: `(cluster:string)`
- Docstring: Get dev, PM owners and admins of a given cluster
- Usage example: `GetClusterOwners('cluster-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     DimClustersMv
    | where Source == cluster
    | extend rawsub =  tostring(ArmResourceId)
    | extend SubscriptionId = extract("/subscriptions/([^/]+)", 1, rawsub)
    | join kind=leftouter hint.strategy=broadcast (
        cluster("https://datastudiostreaming.kusto.windows.net").database("Shared").DataStudio_ServiceTree_AzureSubscription_Snapshot
        | project SubscriptionId, ServiceId
        | join kind= fullouter (
            cluster("https://datastudiostreaming.kusto.windows.net").database("Shared").DataStudio_ServiceTree_ServiceCommonMetadata_Snapshot
            | project ServiceId, ServiceName, DevOwner, PMOwner, Admins)
            on ServiceId
        | summarize by SubscriptionId, ServiceName, DevOwner, PMOwner, Admins
        )
        on SubscriptionId
    | project Source, Kind, State, Region, DevOwner, PMOwner, Admins
 }
```

## `GetComputeSubscriptionPurpose`

- Folder: `OPS`
- Parameters: `(cluster:string)`
- Docstring: Gets the compute subscription purpose for a given service
- Usage example: `GetComputeSubscriptionPurpose('cluster-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     let DimCluster =  DimClustersMv
        | where Source =~ ['cluster']
        | project
            CmConnectionString,
            ComputeSubscriptionId=parse_json(ServiceConfiguration).ComputeSubscriptionId;
     let cmConnectionStringDim = toscalar(DimCluster | project CmConnectionString);
     let ComputeSubscriptionId = toscalar(DimCluster | project ComputeSubscriptionId);
     let subPurposes = iif (isempty(ComputeSubscriptionId), '.show version | project SubscriptionId="" , Purposes=""', strcat('.show unallocated subscriptions | where SubscriptionId =="', ComputeSubscriptionId, '" | project SubscriptionId , Purposes'));
     let cmConnectionString = iif (isempty(ComputeSubscriptionId), ".", cmConnectionStringDim);
     evaluate execute_show_command(cmConnectionString, subPurposes)
    | extend IsAZSC = not(Purposes has_any ('Storage', 'OneCert', 'Compute', 'OpsOnly') or isempty(Purposes))
 }
```

## `MaterializedViewByRaid`

- Folder: `MaterializedViews`
- Parameters: `(rootActivityId:string)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewByRaid('rootActivityId-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewByRaid(rootActivityId))
 }
```

## `MaterializedViewParseSampleExtentRebuild`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewParseSampleExtentRebuild(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewParseSampleExtentRebuild(startTime, endTime))
 }
```

## `MaterializedViewsAgeMetric`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsAgeMetric(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsAgeMetric(startTime, endTime))
 }
```

## `MaterializedViewsAlerts`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsAlerts(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsAlerts(startTime, endTime))
 }
```

## `MaterializedViewsArgMaxOptimization`

- Folder: `MaterializedViews`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsArgMaxOptimization() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsArgMaxOptimization())
 }
```

## `MaterializedViewsCompletionMetric`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsCompletionMetric(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsCompletionMetric(startTime, endTime))
 }
```

## `MaterializedViewsDurations`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsDurations(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsDurations(startTime, endTime))
 }
```

## `MaterializedViewsErrors`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime, source:string)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsErrors(datetime(2026-01-01), datetime(2026-01-01), 'source-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsErrors(startTime, endTime, source))
 }
```

## `MaterializedViewsMonitoring`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsMonitoring(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsMonitoring(startTime, endTime))
 }
```

## `MaterializedViewsParseStatus`

- Folder: `MaterializedViews`
- Parameters: `(start:datetime, end:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsParseStatus(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsParseStatus(['start'], end))
 }
```

## `MaterializedViewsRetainRemoveStats`

- Folder: `MaterializedViews`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsRetainRemoveStats() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsRetainRemoveStats())
 }
```

## `MaterializedViewsSoftDeletePartitions`

- Folder: `MaterializedViews`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsSoftDeletePartitions() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsSoftDeletePartitions())
 }
```

## `MaterializedViewsStatisticsCollector`

- Folder: `MaterializedViews`
- Parameters: `(fromTime:datetime, toTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsStatisticsCollector(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsStatisticsCollector(fromTime, toTime))
 }
```

## `MaterializedViewsTrigger`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsTrigger(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsTrigger(startTime, endTime))
 }
```

## `MaterializedViewsUnknownErrors`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsUnknownErrors(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsUnknownErrors(startTime, endTime))
 }
```

## `SqlMonitoringAttachMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `SqlMonitoringAttachMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.SqlMonitoringAttachMv()
    )
 }
```

## `UsageDailyMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `UsageDailyMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.UsageDailyMv
    )
 }
```

