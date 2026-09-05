```
//count hot nodes over time
 PerfCounterCPU
| where Timestamp between(datetime(2026-03-18T01:00:00Z) .. datetime(2026-03-18T23:00:00Z))
| where Source == toupper('<cluster name>')
| summarize avg_cpu = avg(CounterValue) by bin(Timestamp, 1m), Machine
| summarize HotNodes = countif(avg_cpu > 90), TotalNodes = dcount(Machine) by Window = Timestamp
| where HotNodes > 50
| order by Window asc 
| render timechart 


//SKU, Nodes, Autoscale:
DimClusters
| where Cluster == toupper('<cluster name>')
| where LastUpdated > ago(7d)
| order by LastUpdated desc
| take 1
| project MachineSKU, MachineCount, AutoscaleMinCount, AutoscaleMaxCount, AutoscaleEnabled

//ShardEngine & SketchCacheSize:
DimClustersMv
| where Cluster == toupper('<cluster name>')
| where LastUpdated > ago(7d)
| order by LastUpdated desc
| take 1
| project ShardEngineEnabled, SketchCacheSize

//Primary Database (query distribution):
QueryCompletion
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| summarize count() by DatabaseName
| order by count_ desc

//Total Original Data, Compressed Data, Extents:
// ⚠️ NOT CORRECT: DimDatabases does not exist in Kuskus. Use ClusterDataCapacity() instead.
// DimDatabases
// | where Cluster == toupper('<cluster name>')
// | where LastUpdated > ago(1d)
// | order by LastUpdated desc
// | take 1
// | project OriginalDataSize, CompressedDataSize, ExtentsCount
ClusterDataCapacity()
| where Source == toupper('<cluster name>')
| project Source, OriginalSize, CompressedSize, ExtentsCount

// Hot Disk Usage & Data Capacity Factor:
// ⚠️ NOT CORRECT: DimCapacityMetrics does not exist in Kuskus. Use ClusterDataCapacity() or KustoMdmMetricsV1() instead.
// DimCapacityMetrics
// | where Cluster == toupper('<cluster name>')
// | where Timestamp > ago(7d)
// | summarize avg(HotDiskUsage), avg(DataCapacityFactor) by bin(Timestamp, 1d)
// | order by Timestamp desc
ClusterDataCapacity()
| where Source == toupper('<cluster name>')

//Ingestion Volume:
DataIngest
| where Timestamp > ago(7d)
| where Source == toupper('<cluster name>')
| summarize TotalIngestedGB = sum(OriginalSize) / 1GB by bin(Timestamp, 1d)
| order by Timestamp desc

//count followers and following
DimClustersMv
| where Source == toupper('<cluster name>')
| project Following = array_length(ServiceConfiguration.AttachedDatabasesSettings.Following), Followed =array_length(ServiceConfiguration.AttachedDatabasesSettings.Followers)


//changes in number of machines over time
DimClusters
| where Cluster ==toupper('<cluster name>')
| where LastUpdated > ago(30d)
| order by LastUpdated asc
| where MachineCount != prev(MachineCount)


//number of long queries over a month
QueryCompletion
| where TotalCPU > 1m
| where Source == toupper('<cluster name>')
| extend ScannedExtentsStatistics=todynamic(ScannedExtentsStatistics)
| extend TotRows=tolong(['ScannedExtentsStatistics']['TotalRowsCount']),SCannedRows=tolong(['ScannedExtentsStatistics']['ScannedRowsCount'])
| summarize sum(SCannedRows) by bin(Timestamp,1h)
| render timechart
 
//busiest machines last 7d
 PerfCounterCPU
| where Source == toupper('<cluster name>')
| where Timestamp > ago(30d)
| summarize avg(CounterValue) by bin(Timestamp,1h)
| render timechart

//ingestion trend 30d 
DataIngest
| where Source == toupper('<cluster name>')
| summarize sum(RowCount) by bin(Timestamp,1d)
| render timechart 

// Is it multi-admin? How many admins?
// NOTE: DimClustersMv.IsMultiAdmin is NOT reliable for this check. Use KustoMdmMetricsV1 instead.
// It's multi admin if engine.databaseadmin.svc has more than one RoleInstance:
KustoMdmMetricsV1
| where TIMESTAMP >ago(1d)
| where Cluster == toupper('<cluster name>')
| where metricName == "ActiveServiceInstances"
 | where dimensionNameList == "Cluster^DataCenter^DeploymentRing^RoleInstance^ServiceType"
 | parse dimensionValueList with * "^fabric://"ServiceType:string"/"
 | where ServiceType in ("engine.weakconsistencyquery.svc", "engine.databaseadmin.svc")
 | summarize dcount(RoleInstance), make_set(RoleInstance) by bin(TIMESTAMP,10m), ServiceType
| render timechart


//are any Weak consistency queries running on the cluster
// NOTE: empty wc means strong consistency (legacy default), NOT weak
QueryCompletion
| where Timestamp >ago(1d)
| where Source == toupper('<cluster name>')
| where Api == "Query"
| extend wc = tostring(ClientRequestProperties['Options']['queryconsistency'])
| summarize count() by wc


//get the number of extents per DB - works only when there are queries that were run in the time period
//https://dataexplorer.azure.com/clusters/kuskushead.westeurope/databases/Kuskus?

KustoLogs
| where Source == "<cluster name>"
| where Timestamp > ago(10m)
| where EventText has "TableExtentPrefilter.TraceStats:"
| project EventText
| parse EventText with * 'Database":"' DB '","Table":"' TBL '"' * '"TotalExtents":' Extents:long "," *
| summarize max(Extents) by DB, TBL
| order by max_Extents

//nr of machines in cluster
let ClusterName = '<cluster name>';
let StartDate = datetime(2026-3-18);
let TimePeriod = 3d;
DimClusters
| where Cluster ==ClusterName
| where LastUpdated  between(StartDate..TimePeriod)
| order by LastUpdated asc
| where MachineCount  !=prev(MachineCount)
| project TimeStamp = LastUpdated, MachineCount
| render timechart   

//multiply the machines so they will be in the same scale
let ClusterName = '<cluster name>';
let StartDate = datetime(2026-3-18);
let TimePeriod = 2d;
let CL=DimClusters
| where Cluster==ClusterName
| where LastUpdated between(StartDate..TimePeriod)
| summarize Machines=avg(MachineCount) by Timestamp=bin(LastUpdated,10m)
| extend Machines=100*Machines;
union CL,
(QueryCompletion
| where Source =='<cluster name>'
| where Timestamp between(StartDate..TimePeriod)
| summarize TotalQueries=count(),Cancelled=countif(State=='Cancelled'),TotCPU=sum(TotalCPU)/1m/2 by bin(Timestamp,10m)
| extend Cancelled=Cancelled * (5594/268.))
| render timechart

//view CPU consumption
let StartTime = ['_startTime'];
let EndTime = ['_endTime']; 
let agg_unit_duration = datetime_diff("Minute", EndTime, StartTime);
PerfCounterCPU
| where Timestamp between(StartTime..EndTime)
| summarize CounterValue = avg(CounterValue) by Timestamp = bin(Timestamp, 10s), Cluster = Source, Source
| summarize avg_cpu = avg(CounterValue), max_cpu = max(CounterValue) by Timestamp = bin(Timestamp, 1m * agg_unit_duration / 500 ), Cluster, Source
| where Source == SourceQualified or Source == toupper(cluster)
| project-away Cluster

//view CPU consumption by node
let StartTime = ['_startTime'];
let EndTime = ['_endTime']; 
let agg_unit_duration = datetime_diff("Minute", EndTime, StartTime);
PerfCounterCPU
| where Timestamp between(StartTime..EndTime)
| summarize CounterValue = avg(CounterValue) by Timestamp = bin(Timestamp, 10s), Cluster = Source, Source, Machine
| summarize avg_cpu = avg(CounterValue), max_cpu = max(CounterValue) by Timestamp = bin(Timestamp, 1m * agg_unit_duration / 500 ), Machine, Source
| where Source == SourceQualified or Source == toupper(param_Cluster)


//compute SKu over time
let _cluster = param_Cluster;
DimClusters
| where Cluster =~ _cluster
| where LastUpdated between (_startTime .. _endTime)
| summarize avg(MachineCount), ManagedDisksProperties = any(ManagedDisksProperties), 
    MachineCoresLimit = avg(todouble(ServiceConfiguration.VirtualClusterSettings.Limits.EngineCoreLimit)), 
    EngineDiskCacheSizeInBytes = any(ServiceConfiguration.VirtualClusterSettings.Limits.EngineDiskCacheSizeInBytes)
    by MachineSKU, timestamp = bin(LastUpdated, 10m)
| extend MachineSKU = iif(
            MachineSKU  == "VC resource",
            strcat(
                "VC: ",
                tostring(round(todouble(MachineCoresLimit))), 
                " + ", 
                format_bytes(tolong(EngineDiskCacheSizeInBytes))),
            strcat(
                MachineSKU, 
                iff(tobool(ManagedDisksProperties.Enabled), 
                    strcat("+", ManagedDisksProperties.NumDisks, "TB"), "")))
| project timestamp, MachineSKU, NodeCount = avg_MachineCount

//cluster data estate
let _cluster = param_Cluster;
DimClusters
| where Cluster =~ _cluster
| where LastUpdated between (_startTime .. _endTime)
| summarize avg(MachineCount), ManagedDisksProperties = any(ManagedDisksProperties), 
    MachineCoresLimit = avg(todouble(ServiceConfiguration.VirtualClusterSettings.Limits.EngineCoreLimit)), 
    EngineDiskCacheSizeInBytes = any(ServiceConfiguration.VirtualClusterSettings.Limits.EngineDiskCacheSizeInBytes)
    by MachineSKU, timestamp = bin(LastUpdated, 10m)
| extend MachineSKU = iif(
            MachineSKU  == "VC resource",
            strcat(
                "VC: ",
                tostring(round(todouble(MachineCoresLimit))), 
                " + ", 
                format_bytes(tolong(EngineDiskCacheSizeInBytes))),
            strcat(
                MachineSKU, 
                iff(tobool(ManagedDisksProperties.Enabled), 
                    strcat("+", ManagedDisksProperties.NumDisks, "TB"), "")))
| project timestamp, MachineSKU, NodeCount = avg_MachineCount


//data ingested
let _endTime = datetime(2026-03-24T11:45:00Z);
let _startTime = datetime(2026-03-17T11:45:00Z);
let param_Cluster = '<cluster name>';
DataIngestHistoryMv
| where Source has param_Cluster
| extend Source = substring(Source, indexof(Source,".") + 1)
| where Source == toupper(param_Cluster)
| where Day between (startofday(_startTime) .. startofday(_endTime))
| project Day, ExtentSize, OriginalSize

//data retention
let param_Cluster = 'teamstelemetry02eu';
let clusters = DimClustersMv
| where Kind == "DataManagement"
| where Source == strcat("INGEST-", toupper(param_Cluster))
;
let GB = pow(2, 30);
cluster("kustodataestatefw.westeurope").database('Insights').table('TablesDetails') 
| where TIMESTAMP  > ago(2d)
| where Cluster in(clusters)
| project Cluster, TIMESTAMP, todynamic(tableDetails)
| mv-expand tableDetails
| project TIMESTAMP, Cluster, DatabaseName = tostring(tableDetails.DatabaseName),  TableName = tostring(tableDetails.TableName),  
    TotalExtentSize = tableDetails.TotalExtentSize,
    RetentionPolicy = tableDetails.RetentionPolicy,
    Recoverability = tableDetails.RetentionPolicy.Recoverability,
    Retention = parse_json(tableDetails.RetentionPolicy).SoftDeletePeriod,
    tableDetails 
| parse RetentionPolicy with '{"SoftDeletePeriod":"' RetentionInDays:string ':00:00"' * 
| extend RetentionInDays = toreal(RetentionInDays)
| where isnotnull(RetentionInDays) and TotalExtentSize > 0 
| summarize hint.strategy=shuffle arg_max(TIMESTAMP,  todecimal(TotalExtentSize), RetentionInDays) by Cluster, DatabaseName, TableName
| extend DailyExtentMargin = TotalExtentSize/RetentionInDays
| extend 
    Hot = DailyExtentMargin * min_of(RetentionInDays, 30),
    Cool = DailyExtentMargin * max_of(0, min_of(RetentionInDays, 90) - 30),
    Cold = DailyExtentMargin * max_of(0, RetentionInDays - 90)
| summarize ['1 month'] = toint(sum(Hot) / GB), ['2-3 months'] = toint(sum(Cool)/GB), ['3 months and more'] = toint(sum(Cold)/GB) by Cluster
| evaluate narrow()
| project Tier = Column, VolumeInGB = toint(Value)
| where Tier != "Cluster"


//query latency/ duration
let SourceQualified = toupper(<cluster name>);
QueryCompletion
| where Source == SourceQualified
| where Timestamp between (_startTime .. _endTime)
| summarize percentiles(Duration, 10, 50, 90, 95, 99) by bin(Timestamp, 1m * agg_unit_duration / 500 )

//shows level of query parallelism - query cpu duration ratio
let SourceQualified = toupper(<cluster name>);
QueryCompletion
| where Source == SourceQualified
| where Timestamp between (_startTime .. _endTime)
| summarize totalCPU = sum(TotalCPU), totalDuration = sum(Duration) by bin(Timestamp, 1h )
| extend ratio = round(totalCPU/totalDuration, 2)
| summarize percentiles(ratio, 10, 50, 90, 95, 99) by Timestamp

//query completed vs cancelled vs failed
let SourceQualified = toupper(<cluster name>);
QueryCompletion
| where Source == SourceQualified
| where Timestamp between (_startTime .. _endTime)
| summarize  queryCount =count(), Cancelled = countif(State == "Cancelled") by  bin(Timestamp,1h)
| extend Ratio = 100.* Cancelled/queryCount

//check query distribution across Databases
QueryCompletion
| where Timestamp between (_startTime .. _endTime) 
| where Source == toupper(<cluster name>)
| summarize count() by bin(Timestamp,1h), DatabaseName
```