# OPS functions

Functions in folder `OPS`.

## `AllCommandsAndQueries`

- Folder: `OPS`
- Parameters: `(ClusterName:string, StartTime:datetime, EndTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `AllCommandsAndQueries('ClusterName-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.AllCommandsAndQueries(ClusterName, StartTime, EndTime)
    )
 }
```

## `AllDimClusters`

- Folder: `OPS`
- Parameters: `()`
- Docstring: Union DimClusters tables for all Clouds
- Usage example: `AllDimClusters() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     union withsource=Table
        DimClusters,
        cluster("kuskusdfv3").database("KuskusFF").DimClusters,
        cluster("kuskusdfv3").database("KuskusMC").DimClusters
    | extend Cloud = case
             (
                 Table has "KuskusFF",
                 "FairFax",
                 Table has "KuskusMC",
                 "MoonCake",
                 "Public"
             )
    | project-away Table
 }
```

## `DimToDS`

- Folder: `OPS`
- Parameters: `()`
- Docstring: export DIM clusters data with Service Tree correlation to Data Map team
- Usage example: `DimToDS() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
cluster("kuskusprod").database("Kuskus").DimClusters | extend Cloud = "Public"
| where LastUpdated > ago(2d)
| where Kind == "Engine"
| extend SubscriptionId = extract(@"\/subscriptions\/(.*)\/resourceGroups",1,ArmResourceId)
| distinct  Cluster, ServiceConnectionString, SubscriptionId, Region, Cloud, TenantName, Account, State,Tags
| join kind= leftouter
(
cluster("datastudiostreaming").database("Shared").ServiceTree_AzureSubscription_Snapshot
)
on SubscriptionId
| join kind= leftouter
(
    cluster("datastudiostreaming").database("Shared").ServiceTree_ServiceHierarchy_Snapshot
) on $left.ServiceInternalId == $right.InternalId
| summarize arg_max(Modified, Name, Id1) by Cluster,SubscriptionId,Region, Cloud, State,ServiceConnectionString,Account,TenantName,Tags
| project Cluster, State,  ServiceConnectionString,SubscriptionId, ServiceName=Name, ServiceTreeGuid=Id1, Region, Cloud, TenantName, Account,Tags
| where isnotempty(ServiceTreeGuid)
}
```

## `EventGridIngestionVolume`

- Folder: `OPS`
- Parameters: `(dmName:string, startTime:datetime, endTime:datetime)`
- Docstring: Get the Event Grid Ingestion Volume for a  DM
- Usage example: `EventGridIngestionVolume('dmName-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.EventGridIngestionVolume(dmName, startTime, endTime)
    )
 }
```

## `EventHubIngestionVolume`

- Folder: `OPS`
- Parameters: `(ClusterName:string, startTime:datetime, endTime:datetime)`
- Docstring: Gets the ingestion volume for Event Hub.This needs to be run on Ingestion Service i.e INGEST-XXXXX
- Usage example: `EventHubIngestionVolume('ClusterName-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.EventHubIngestionVolume(ClusterName, startTime, endTime)
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

## `ExtendedDimClusters`

- Folder: `OPS`
- Parameters: `()`
- Docstring: returns full list of clusters including private customer clusters
- Usage example: `ExtendedDimClusters() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     union best_effort=true cluster("kuskusdfv3").database("KuskusDev").DimClusters, DimClusters()
    | extend Cloud = "Public"
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

## `FindUsageByCID24h`

- Folder: `OPS`
- Parameters: `(cid:string)`
- Docstring: No docstring provided.
- Usage example: `FindUsageByCID24h('cid-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.FindUsageByCID24h(cid)
    )
 }
```

## `FindUsageByRID24h`

- Folder: `OPS`
- Parameters: `(rid:string)`
- Docstring: No docstring provided.
- Usage example: `FindUsageByRID24h('rid-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.FindUsageByRID24h(rid)
    )
 }
```

## `GenevaIngestionByMoniker`

- Folder: `OPS`
- Parameters: `(MonikerName:string, startTime:datetime, endTime:datetime)`
- Docstring: Verify data flow from a given moniker
- Usage example: `GenevaIngestionByMoniker('MonikerName-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GenevaIngestionByMoniker(MonikerName, startTime, endTime)
    )
 }
```

## `GenevaIngestionVolume`

- Folder: `OPS`
- Parameters: `(dmName:string, startTime:datetime, endTime:datetime)`
- Docstring: Get the Ingestion Volume of a Geneva based DM
- Usage example: `GenevaIngestionVolume('dmName-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GenevaIngestionVolume(dmName, startTime, endTime)
    )
 }
```

## `GetCluster`

- Folder: `OPS`
- Parameters: `(source:string)`
- Docstring: Get cluster details
- Usage example: `GetCluster('source-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetCluster(source)
    )
 }
```

## `GetClusterChangesWithTimeMarker`

- Folder: `OPS`
- Parameters: `(source:string, clusterProblemStartTime:datetime)`
- Docstring: Get User changes close to a cluster degradation time. clusterProblemStartTime & deployments will show up as entries on the timechart
- Usage example: `GetClusterChangesWithTimeMarker('source-value', datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetClusterChangesWithTimeMarker(source, clusterProblemStartTime)
    )
    | render timechart
 }
```

## `GetClusterSource`

- Folder: `OPS`
- Parameters: `(source:string)`
- Docstring: Get cluster snapshot with Jarvis health link
- Usage example: `GetClusterSource('source-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetClusterSource(source)
    )
 }
```

## `GetCM`

- Folder: `OPS`
- Parameters: `(source:string)`
- Docstring: Obtain CM information for a cluster
- Usage example: `GetCM('source-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetCM(source)
    )
 }
```

## `GetCMForRegion`

- Folder: `OPS`
- Parameters: `(region:string)`
- Docstring: Function to return the regional CM for the given region
- Usage example: `GetCMForRegion('region-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetCMForRegion(region)
    )
 }
```

## `GetCMForService`

- Folder: `OPS`
- Parameters: `(service:string)`
- Docstring: Find owning CM
- Usage example: `GetCMForService('service-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetCMForService(service)
    )
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

## `GetDeployedServices`

- Folder: `OPS`
- Parameters: `(startDate:datetime, endDate:datetime)`
- Docstring: No docstring provided.
- Usage example: `GetDeployedServices(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetDeployedServices(startDate, endDate)
    )
 }
```

## `GetDeploymentRingMoveSuggestions`

- Folder: `OPS`
- Parameters: `(DeploymentRingtoMove:string)`
- Docstring: Get actual ring name with A,B or C for given cluster based on region
- Usage example: `GetDeploymentRingMoveSuggestions('DeploymentRingtoMove-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetDeploymentRingMoveSuggestions(DeploymentRingtoMove)
    )
 }
```

## `GetHosterInfo`

- Folder: `OPS`
- Parameters: `(_source:string)`
- Docstring: Get Hoster Information
- Usage example: `GetHosterInfo('_source-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetHosterInfo(_source)
    )
 }
```

## `GetKVDBErrors`

- Folder: `OPS`
- Parameters: `(window:datetime, excludeCluster:string="")`
- Docstring: Generate restart command for KVDatabase Errors
- Usage example: `GetKVDBErrors(datetime(2026-01-01), 'excludeCluster-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
// ⚠️ NOT CORRECT: GetKVDBErrorsRegional is an internal regional function — not available on kuskushead. This function body may be outdated or only resolvable on regional Kuskus instances.
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetKVDBErrorsRegional(window, excludeCluster)
    )
    | join kind=leftouter (
        cluster('kuskusops.kustomfa.windows.net').database('KustoServiceDashboard').KvDBRestarts
        | where Timestamp >= (window - 6h)
        )
        on $left.Cmd == $right.CommandUsed
    | extend Cmd = iff(isnotempty(CommandUsed), replace(".rebuild", ".reallocate", Cmd), Cmd)
    | project Source, CmConnectionString, Cmd
    | take 100
 }
```

## `GetServiceAuditLogs`

- Folder: `OPS`
- Parameters: `(service:string, lookback:timespan=time(1.00:00:00))`
- Docstring: Show service audit log
- Usage example: `GetServiceAuditLogs('service-value', 1d) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     let start_date = now() - lookback;
     let start_date_as_string = format_datetime(now(), "yyyy-MM-dd");
     let svc = toscalar(GetTridentServiceNameFromClusterAlias(service));
     execute_on_owning_cm(svc, strcat('.show service ', svc, ' audit log from "', start_date, '"'))
 }
```

## `GetServiceLBDashboard`

- Folder: `OPS`
- Parameters: `(source:string)`
- Docstring: Get the LB geneva Uri
- Usage example: `GetServiceLBDashboard('source-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     let region = toscalar(
        execute_on_owning_cm(source, strcat('.show service ', source, ' configuration'))
        | extend ServiceConfiguration = todynamic(ServiceConfiguration)
        | extend Region = tolower(replace_string(tostring(ServiceConfiguration.Location), ' ', ''))
        | project Region);
     let resource= toscalar(
        execute_on_owning_cm(source, strcat('.show service ', source, ' resources'))
        | where type == 'microsoft.network/loadbalancers'
        | project properties.resourceGuid);
     let a = 'https://portal.microsoftgeneva.com/dashboard/slbv2prod/AzureMonitor/SnatAvailability?overrides=[{%22query%22:%22//dataSources%22,%22key%22:%22account%22,%22replacement%22:%22';
     let b = 'slbhp';
     let c = '%22},{%22query%22:%22//*[id%3D%27VipAddress%27]%22,%22key%22:%22value%22,%22replacement%22:%22%22},{%22query%22:%22//*[id%3D%27PublicIpArmId%27]%22,%22key%22:%22value%22,%22replacement%22:%22%22},{%22query%22:%22//*[id%3D%27LoadBalancerArmId%27]%22,%22key%22:%22value%22,%22replacement%22:%22';
     let d = '%22}]%20';
     let LB = strcat(a, b, region, c, resource, d);
     print LB
 }
```

## `GetTridentServiceNameFromClusterAlias`

- Folder: `OPS`
- Parameters: `(cluster:string)`
- Docstring: Translate INGEST-HOSTER.KVC to INGEST-KVC
- Usage example: `GetTridentServiceNameFromClusterAlias('cluster-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetTridentServiceNameFromClusterAlias(cluster)
    )
 }
```

## `IsRestartAllowedByCustomer`

- Folder: `OPS`
- Parameters: `(clusterName:string)`
- Docstring: Returns a boolean if Gaia is allowed to restart the cluster
- Usage example: `IsRestartAllowedByCustomer('clusterName-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
// ⚠️ NOT CORRECT: IsRestartAllowedByCustomerInternal is an internal regional function — not available on kuskushead. This function body may be outdated or only resolvable on regional Kuskus instances.
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.IsRestartAllowedByCustomerInternal(clusterName)
    )
    | summarize Count = sum(Count)
    | project RestartAllowed = Count > 0
 }
```

## `LatestDimCluster`

- Folder: `OPS`
- Parameters: `(_Cluster:string)`
- Docstring: returns latest row of a service
- Usage example: `LatestDimCluster('_Cluster-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.LatestDimCluster(_Cluster)
    )
 }
```

## `ManagedBytesAllocatedForRequests`

- Folder: `OPS`
- Parameters: `(_startTime:datetime, _endTime:datetime, _source:string)`
- Docstring: ActivityType consuming high Managedmemory
- Usage example: `ManagedBytesAllocatedForRequests(datetime(2026-01-01), datetime(2026-01-01), '_source-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ManagedBytesAllocatedForRequests(_startTime, _endTime, _source)
    )
 }
```

## `MemIntensiveQueries`

- Folder: `OPS`
- Parameters: `(numberOfQueries:int, source:string, startTime:datetime, endTime:datetime)`
- Docstring: Useful to investigate OOM erros (case insensitive)
- Usage example: `MemIntensiveQueries(1, 'source-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MemIntensiveQueries(numberOfQueries, source, startTime, endTime)
    )
 }
```

## `MemIntensiveQueriesWithHash`

- Folder: `OPS`
- Parameters: `(numberOfQueries:int, source:string, startTime:datetime, endTime:datetime, hashLength:long)`
- Docstring: Useful to investigate OOM erros (case insensitive)
- Usage example: `MemIntensiveQueriesWithHash(1, 'source-value', datetime(2026-01-01), datetime(2026-01-01), 1) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MemIntensiveQueriesWithHash(numberOfQueries, source, startTime, endTime, hashLength)
    )
 }
```

## `SealingAggregation`

- Folder: `OPS`
- Parameters: `(clustername:string, startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `SealingAggregation('clustername-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.SealingAggregation(clustername, startTime, endTime)
    )
 }
```

## `ServicesNotInProductVersionByDiagnosticsResults`

- Folder: `OPS`
- Parameters: `(_DeploymentRing:string, _ProductVersion:string, _DeploymentStartTime:datetime)`
- Docstring: Services Not In Product Version By Diagnostics Resutls
- Usage example: `ServicesNotInProductVersionByDiagnosticsResults('_DeploymentRing-value', '_ProductVersion-value', datetime(2026-01-01)) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     SyntheticsResultsV2
    | where ClientActivityId startswith "Common.ShowVersion."
    | parse ClientActivityId with "Common.ShowVersion." Service "."*
    | where PreciseTimeStamp > _DeploymentStartTime
    | join DimClustersMv on $left.Service == $right.Source
    | where DeploymentRing == _DeploymentRing
    | where Source !contains "trident"
    | where State == "Running"
    | extend V = ResultData.ProductVersion
    | project Source, V, DeploymentRing, CmConnectionString
    | where V != ""
    | where V != _ProductVersion
    | extend vDate = replace_string (substring(V, 0, 10), ".", "-")
    | summarize max(tostring(V)) by Source, DeploymentRing, CmConnectionString
 }
```

## `ServicesRequiredDeploymentOperationByDiagnisticsResults`

- Folder: `OPS`
- Parameters: `(_DeploymentRing:string, _ProductVersion:string, _DeploymentStartTime:datetime)`
- Docstring: Services need special attention during deployment
- Usage example: `ServicesRequiredDeploymentOperationByDiagnisticsResults('_DeploymentRing-value', '_ProductVersion-value', datetime(2026-01-01)) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     ServicesNotInProductVersionByDiagnosticsResults(_DeploymentRing, _ProductVersion, _DeploymentStartTime)
    | where CmConnectionString !in("https://manage-kustoppe.kusto.windows.net",
        "https://manage-kustoppewus2.kusto.windows.net",
        "https://manage-kustokvcaustralia.kusto.windows.net",
        "https://manage-kustokvceuropa.kusto.windows.net",
        "https://manage-kustokvcnorthamerica.kusto.windows.net")
    | union (
        ServicesWtihInconsistVersionsByDiagnisticsResults(_DeploymentRing, _ProductVersion, _DeploymentStartTime)
        )
    | parse NotHealthyReason with * "'" NotHealthyReason "'" *
    | mv-expand parse_json(NotHealthyReason)
    | where tostring(NotHealthyReason) !has _ProductVersion
    | extend parts = split(NotHealthyReason, ":")
    | extend Instance = replace('{"', '', tostring(parts[0]))
    | extend Instance = replace('"', '', Instance)
    | summarize
        machinesetSCS = tostring(makeset(Instance)),
        NotHealthyReason=any(NotHealthyReason)
        by Source, ServiceConnectionString, CmConnectionString, Timestamp, max_V
    | extend machinesetSCS = replace(@'","', ';', machinesetSCS)
    | extend machinesetSCS = replace(@'\["', "", machinesetSCS)
    | extend machinesetSCS = replace(@'"\]', "", machinesetSCS)
    | extend Command = strcat('.reallocate service ', Source, ' with (Instancename = "', machinesetSCS, '")')
    | extend Command = iff(isnull(NotHealthyReason), strcat(".install service ", Source, " with(skipdeployedservices='true',prepareenvironment='true', ProductVersion='", _ProductVersion, "')"), Command)
    | project-away machinesetSCS, NotHealthyReason, Timestamp
    | sort by CmConnectionString
 }
```

## `ServicesStillInPreviousTrain`

- Folder: `OPS`
- Parameters: `(_DeploymentRing:string, _Train:string, _DeploymentStartTime:datetime)`
- Docstring: Detects rollbacks from a specific train number
- Usage example: `ServicesStillInPreviousTrain('_DeploymentRing-value', '_Train-value', datetime(2026-01-01)) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     cluster('kuskusdfv3.kusto.windows.net').database('Kuskus').ServicesStillInPreviousTrain(_DeploymentRing, _Train, _DeploymentStartTime)
 }
```

## `ServicesWtihInconsistVersionsByDiagnisticsResults`

- Folder: `OPS`
- Parameters: `(_DeploymentRing:string, _ProductVersion:string, _DeploymentStartTime:datetime)`
- Docstring: Services with different versions installed on nodes by DiagnosticsResults
- Usage example: `ServicesWtihInconsistVersionsByDiagnisticsResults('_DeploymentRing-value', '_ProductVersion-value', datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ServicesWtihInconsistVersionsByDiagnisticsResults(_DeploymentRing, _ProductVersion, _DeploymentStartTime)
    )
 }
```

## `SingleBlobIngestReason`

- Folder: `OPS`
- Parameters: `(ClusterName:string, StartTime:datetime, EndTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `SingleBlobIngestReason('ClusterName-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.SingleBlobIngestReason(ClusterName, StartTime, EndTime)
    )
 }
```

## `SyntheticsResultsV2`

- Folder: `OPS`
- Parameters: `()`
- Docstring: SyntheticsResultsV2
- Usage example: `SyntheticsResultsV2() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     TraceTelemetryResults
 }
```

## `ThrottlingonKustoCluster`

- Folder: `OPS`
- Parameters: `(ClusterName:string, startTime:datetime, endTime:datetime)`
- Docstring: Get the Storage Throttling on Kusto Clusters
- Usage example: `ThrottlingonKustoCluster('ClusterName-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ThrottlingonKustoCluster(ClusterName, startTime, endTime)
    )
 }
```

## `TopAlerts`

- Folder: `OPS`
- Parameters: `(startTime:string, endTime:string, source:string)`
- Docstring: Get top alerts by SourceID
- Usage example: `TopAlerts('startTime-value', 'endTime-value', 'source-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TopAlerts(startTime, endTime, source)
    )
 }
```

## `TopApplicationsConsumingAdminManagedMemory`

- Folder: `OPS`
- Parameters: `(_source:string, _startTime:datetime, _endTime:datetime)`
- Docstring: Get top application consuming admin memory
- Usage example: `TopApplicationsConsumingAdminManagedMemory('_source-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TopApplicationsConsumingAdminManagedMemory(_source, _startTime, _endTime)
    )
 }
```

## `TopExpensiveCancelledQueries`

- Folder: `OPS`
- Parameters: `(_source:string, startTime:datetime, endTime:datetime)`
- Docstring: Top expensive cancelled queries
- Usage example: `TopExpensiveCancelledQueries('_source-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TopExpensiveCancelledQueries(_source, startTime, endTime)
    )
 }
```

## `TopQueriesByCPU`

- Folder: `OPS`
- Parameters: `(numberOfQueries:int, source:string, startTime:datetime, endTime:datetime)`
- Docstring: Top cluster queries by consumed CPU
- Usage example: `TopQueriesByCPU(1, 'source-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TopQueriesByCPU(numberOfQueries, source, startTime, endTime)
    )
 }
```

## `TopQueriesByMemory`

- Folder: `OPS`
- Parameters: `(numberOfQueries:int, source:string, startTime:datetime, endTime:datetime)`
- Docstring: Top cluster queries by consumed memory
- Usage example: `TopQueriesByMemory(1, 'source-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TopQueriesByMemory(numberOfQueries, source, startTime, endTime)
    )
 }
```

## `TopQueriesConsumingAdminManagedMemory`

- Folder: `OPS`
- Parameters: `(_source:string, _startTime:datetime, _endTime:datetime)`
- Docstring: Get top queries consuming admin memory
- Usage example: `TopQueriesConsumingAdminManagedMemory('_source-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TopQueriesConsumingAdminManagedMemory(_source, _startTime, _endTime)
    )
 }
```

## `TopUsersByCPU`

- Folder: `OPS`
- Parameters: `(numberOfUsers:int, source:string, startTime:datetime, endTime:datetime)`
- Docstring: Top cluster users by consumed CPU
- Usage example: `TopUsersByCPU(1, 'source-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TopUsersByCPU(numberOfUsers, source, startTime, endTime)
    )
 }
```

## `TopUsersByMemory`

- Folder: `OPS`
- Parameters: `(numberOfUsers:int, source:string, startTime:datetime, endTime:datetime)`
- Docstring: Top cluster users by consumed memory
- Usage example: `TopUsersByMemory(1, 'source-value', datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TopUsersByMemory(numberOfUsers, source, startTime, endTime)
    )
 }
```

## `WhyWeDontScaleInCluster`

- Folder: `OPS`
- Parameters: `(clusterName:string, lookback:timespan)`
- Docstring: Function for getting why we dont scale in cluster in a given lookback period
- Usage example: `WhyWeDontScaleInCluster('clusterName-value', 1d) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.WhyWeDontScaleInCluster(clusterName, lookback)
    )
 }
```

## `WhyWeDontScaleOutCluster`

- Folder: `OPS`
- Parameters: `(clusterName:string, lookback:timespan)`
- Docstring: Function for getting why we dont scale out cluster in a given lookback period
- Usage example: `WhyWeDontScaleOutCluster('clusterName-value', 1d) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.WhyWeDontScaleOutCluster(clusterName, lookback)
    )
 }
```

## `WhyWeScaleInCluster`

- Folder: `OPS`
- Parameters: `(clusterName:string, lookback:timespan)`
- Docstring: Function for getting why we scale in cluster
- Usage example: `WhyWeScaleInCluster('clusterName-value', 1d) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.WhyWeScaleInCluster(clusterName, lookback)
    )
 }
```

## `WhyWeScaleOutCluster`

- Folder: `OPS`
- Parameters: `(clusterName:string, lookback:timespan)`
- Docstring: Function for getting why we scale out cluster
- Usage example: `WhyWeScaleOutCluster('clusterName-value', 1d) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.WhyWeScaleOutCluster(clusterName, lookback)
    )
 }
```

