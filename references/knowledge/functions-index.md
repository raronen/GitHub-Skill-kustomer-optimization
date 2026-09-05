# Function index

## Folders

- [AutoScale](folders/AutoScale.md) (2)
- [AutoScaleV24](folders/AutoScaleV24.md) (2)
- [Automation](folders/Automation.md) (2)
- [Automation/ClusterDiagnostics](folders/Automation-ClusterDiagnostics.md) (46)
- [CMHelpers](folders/CMHelpers.md) (10)
- [CMHelpersReporting](folders/CMHelpersReporting.md) (5)
- [DM](folders/DM.md) (1)
- [Deployment](folders/Deployment.md) (8)
- [Financials\Utilities](folders/Financials-Utilities.md) (1)
- [Financials\Views](folders/Financials-Views.md) (4)
- [Geospatial](folders/Geospatial.md) (3)
- [Info](folders/Info.md) (1)
- [Investigations](folders/Investigations.md) (14)
- [MaterializedViews](folders/MaterializedViews.md) (15)
- [OPS](folders/OPS.md) (53)
- [Parquet](folders/Parquet.md) (2)
- [PerfCounters](folders/PerfCounters.md) (5)
- [QuickFilters](folders/QuickFilters.md) (5)
- [Shortcuts](folders/Shortcuts.md) (44)
- [Static](folders/Static.md) (2)
- [Telemetry](folders/Telemetry.md) (1)
- [Trident](folders/Trident.md) (4)
- [V3Migration](folders/V3Migration.md) (2)

## All functions

### AutoScale

- `GetLastAutoScaleQueryOfCM(jobName:string, source:string, start:timespan=time(1.00:00:00), end:timespan=time(00:00:00))`
- `ReasonWeDoOrDontScaleCluster(clusterName:string, lookback:timespan, scaleOperationType:string, wasScaled:bool)`

### AutoScaleV24

- `GetLastAutoScaleQueryOfCMV24(jobName:string, source:string, start:timespan=timespan(1d), end:timespan=timespan(0h))`
- `ReasonWeDoOrDontScaleClusterV24(clusterName:string, lookback:timespan=time(7.00:00:00), scaleOperationType:string="scalein", wasScaled:bool=false)`

### Automation

- `Automation_ClusterDiagnostics_Steps()`
- `Automation_ClusterDiagnostics_Transitions()`

### Automation/ClusterDiagnostics

- `ClusterDiagnostics(cluster:string, since:datetime=datetime(null), period:timespan=time(1.00:00:00))`
- `ClusterDiagnostics_AdminCPU_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_AdminCPU_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_AdminGC_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_AdminGC_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_AdminStability_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_AdminStability_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_AnalyzePerNodeUsage_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_AnalyzePerNodeUsage_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_AnalyzeUsage_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_AnalyzeUsage_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_CriticalAlerts_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_CriticalAlerts_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_CriticalTraces_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_CriticalTraces_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_DrillIntoCommandsUsage_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_DrillIntoCommandsUsage_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_DrillIntoQueriesUsage_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_DrillIntoQueriesUsage_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_FindMachinesWithHighGC_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_FindMachinesWithHighGC_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_HighCPU_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_HighCPU_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_HighDiskQueue_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_HighDiskQueue_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_HighGC_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_HighGC_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_HighQueryLatency_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_HighQueryLatency_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_HighQueryLatencyDetails_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_HighQueryLatencyDetails_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_MachinesWithHighCPU_Base(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_MachinesWithHighCPU_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_MachinesWithHighCPU_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_MachinesWithHighGC_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_MachinesWithHighGC_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_OnOffMachines_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_OnOffMachines_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_RareFF_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_RareFF_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_SubqueryDelayed_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_SubqueryDelayed_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_TopHeavyQueries_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_TopHeavyQueries_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_UnhealthyMachines_GetData(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- `ClusterDiagnostics_UnhealthyMachines_NextSteps(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`

### CMHelpers

- `CmHelperShowAuditLogByClientActivityId(clientActivityId:string, from:datetime=datetime(null), ['to']:datetime=datetime(null), cm:string="")`
- `CmHelperShowClusterAuditLog(cluster:string, from:datetime=datetime(null), ['to']:datetime=datetime(null), cm:string="")`
- `CmHelperShowOperations(cm:string="", operations:dynamic=dynamic([]), state:string="")`
- `CmHelperShowServiceAuditLog(service:string, from:datetime=datetime(null), ['to']:datetime=datetime(null), cm:string="")`
- `GetADXCMsOperations()`
- `GetADXCMsServiceOperations()`
- `GetAllCMsOperations()`
- `GetAllCMsServiceOperations()`
- `GetFabricCMsOperations()`
- `GetFabricCMsServiceOperations()`

### CMHelpersReporting

- `CmServiceOperationsFailures(startTime:datetime, timePeriod:timespan)`
- `CmServiceOperationsRolledUpSLA(BeginTime:datetime, TimePeriod:timespan)`
- `CmServiceOperationsSLA(BeginTime:datetime, TimePeriod:timespan)`
- `CmServiceOperationsSLAOverTime(NumOperations:int=10)`
- `CmServiceOperationsWoWSLA()`

### DM

- `GetServiceUrls(service:string)`

### Deployment

- `FeatureFlagEnablements(FF:string, Lookback:timespan=time(7.00:00:00))`
- `FeatureFlagEnablementsInCluster(Cluster:string, Lookback:timespan=time(7.00:00:00))`
- `FeatureFlagsInCluster(cluster:string)`
- `FindFFsWithSubstring(substring:string)`
- `StartUpLatestVersions1m()`
- `WhereFeatureFlag(_ff:string)`
- `WhereFeatureFlagIsDisabled(FeatureFlag:string, ServiceType:string="")`
- `WhereFeatureFlagIsEnabled(FeatureFlag:string, ServiceType:string="")`

### Financials\Utilities

- `GetAccount(Source:string)`

### Financials\Views

- `FabricFinancials()`
- `KustoFinancials()`
- `KustoFinancialsWithRegions()`
- `KustoGrossMargin()`

### Geospatial

- `Geospatial_Clusters_Usage(from:datetime)`
- `Geospatial_ClustersByAccount_Usage(from:datetime)`
- `Geospatial_Functions_Usage(from:datetime)`

### Info

- `GetClusterOwners(cluster:string)`

### Investigations

- `AdminCPU(cluster:string, lookback:timespan=time(7.00:00:00), resolution:timespan=time(00:01:00))`
- `AdminHistory(cluster:string, lookback:timespan=time(31.00:00:00))`
- `AllKeyVaultChanges(secretName:string="", clusterName:string="", duration:timespan=time(28.00:00:00))`
- `AriaBridgeConfigurationDeltaUpdateResults(bridgeName:string, startTime:datetime)`
- `AriaBridgeConfigurationUpdateFailures(bridgeName:string, startTime:datetime)`
- `DiskFirmware(cluster:string)`
- `GetClusterVMIds(cluster:string)`
- `LatestKeyVaultChanges(secretName:string="", clusterName:string="", duration:timespan=time(28.00:00:00))`
- `MapInstanceToVMId(cluster:string, instance:string)`
- `MemStats()`
- `network_corruptions_raw(horizon:datetime)`
- `PerNodeQueryStats(cid:string, lookback:timespan=time(7.00:00:00))`
- `RowStoreTrimOperations(start:datetime, interval:timespan, sourceName:string)`
- `V3_FunctionsMissing(_period:timespan)`

### MaterializedViews

- `MaterializedViewByRaid(rootActivityId:string)`
- `MaterializedViewParseSampleExtentRebuild(startTime:datetime, endTime:datetime)`
- `MaterializedViewsAgeMetric(startTime:datetime, endTime:datetime)`
- `MaterializedViewsAlerts(startTime:datetime, endTime:datetime)`
- `MaterializedViewsArgMaxOptimization()`
- `MaterializedViewsCompletionMetric(startTime:datetime, endTime:datetime)`
- `MaterializedViewsDurations(startTime:datetime, endTime:datetime)`
- `MaterializedViewsErrors(startTime:datetime, endTime:datetime, source:string)`
- `MaterializedViewsMonitoring(startTime:datetime, endTime:datetime)`
- `MaterializedViewsParseStatus(start:datetime, end:datetime)`
- `MaterializedViewsRetainRemoveStats()`
- `MaterializedViewsSoftDeletePartitions()`
- `MaterializedViewsStatisticsCollector(fromTime:datetime, toTime:datetime)`
- `MaterializedViewsTrigger(startTime:datetime, endTime:datetime)`
- `MaterializedViewsUnknownErrors(startTime:datetime, endTime:datetime)`

### OPS

- `AllCommandsAndQueries(ClusterName:string, StartTime:datetime, EndTime:datetime)`
- `AllDimClusters()`
- `DimToDS()`
- `EventGridIngestionVolume(dmName:string, startTime:datetime, endTime:datetime)`
- `EventHubIngestionVolume(ClusterName:string, startTime:datetime, endTime:datetime)`
- `execute_on_owning_cm(service:string, cmd:string)`
- `execute_on_service(service:string, cmd:string)`
- `ExtendedDimClusters()`
- `ExtendedHealthDashboard(_source:string, _region:string)`
- `ExtendedHealthDashboardForDM(_source:string, _region:string)`
- `FindUsageByCID24h(cid:string)`
- `FindUsageByRID24h(rid:string)`
- `GenevaIngestionByMoniker(MonikerName:string, startTime:datetime, endTime:datetime)`
- `GenevaIngestionVolume(dmName:string, startTime:datetime, endTime:datetime)`
- `GetCluster(source:string)`
- `GetClusterChangesWithTimeMarker(source:string, clusterProblemStartTime:datetime)`
- `GetClusterSource(source:string)`
- `GetCM(source:string)`
- `GetCMForRegion(region:string)`
- `GetCMForService(service:string)`
- `GetComputeSubscriptionPurpose(cluster:string)`
- `GetDeployedServices(startDate:datetime, endDate:datetime)`
- `GetDeploymentRingMoveSuggestions(DeploymentRingtoMove:string)`
- `GetHosterInfo(_source:string)`
- `GetKVDBErrors(window:datetime, excludeCluster:string="")`
- `GetServiceAuditLogs(service:string, lookback:timespan=time(1.00:00:00))`
- `GetServiceLBDashboard(source:string)`
- `GetTridentServiceNameFromClusterAlias(cluster:string)`
- `IsRestartAllowedByCustomer(clusterName:string)`
- `LatestDimCluster(_Cluster:string)`
- `ManagedBytesAllocatedForRequests(_startTime:datetime, _endTime:datetime, _source:string)`
- `MemIntensiveQueries(numberOfQueries:int, source:string, startTime:datetime, endTime:datetime)`
- `MemIntensiveQueriesWithHash(numberOfQueries:int, source:string, startTime:datetime, endTime:datetime, hashLength:long)`
- `SealingAggregation(clustername:string, startTime:datetime, endTime:datetime)`
- `ServicesNotInProductVersionByDiagnosticsResults(_DeploymentRing:string, _ProductVersion:string, _DeploymentStartTime:datetime)`
- `ServicesRequiredDeploymentOperationByDiagnisticsResults(_DeploymentRing:string, _ProductVersion:string, _DeploymentStartTime:datetime)`
- `ServicesStillInPreviousTrain(_DeploymentRing:string, _Train:string, _DeploymentStartTime:datetime)`
- `ServicesWtihInconsistVersionsByDiagnisticsResults(_DeploymentRing:string, _ProductVersion:string, _DeploymentStartTime:datetime)`
- `SingleBlobIngestReason(ClusterName:string, StartTime:datetime, EndTime:datetime)`
- `SyntheticsResultsV2()`
- `ThrottlingonKustoCluster(ClusterName:string, startTime:datetime, endTime:datetime)`
- `TopAlerts(startTime:string, endTime:string, source:string)`
- `TopApplicationsConsumingAdminManagedMemory(_source:string, _startTime:datetime, _endTime:datetime)`
- `TopExpensiveCancelledQueries(_source:string, startTime:datetime, endTime:datetime)`
- `TopQueriesByCPU(numberOfQueries:int, source:string, startTime:datetime, endTime:datetime)`
- `TopQueriesByMemory(numberOfQueries:int, source:string, startTime:datetime, endTime:datetime)`
- `TopQueriesConsumingAdminManagedMemory(_source:string, _startTime:datetime, _endTime:datetime)`
- `TopUsersByCPU(numberOfUsers:int, source:string, startTime:datetime, endTime:datetime)`
- `TopUsersByMemory(numberOfUsers:int, source:string, startTime:datetime, endTime:datetime)`
- `WhyWeDontScaleInCluster(clusterName:string, lookback:timespan)`
- `WhyWeDontScaleOutCluster(clusterName:string, lookback:timespan)`
- `WhyWeScaleInCluster(clusterName:string, lookback:timespan)`
- `WhyWeScaleOutCluster(clusterName:string, lookback:timespan)`

### Parquet

- `NativeParquetIngestionUsage(from:datetime)`
- `NativeParquetQueryUsage(from:datetime)`

### PerfCounters

- `PerfCounterCPU()`
- `PerfCounterDiskCQueue()`
- `PerfCounterMemoryAvailable()`
- `PerfCounterThreads()`
- `PerfCounterTimeInGC()`

### QuickFilters

- `FindCIDPast1w(clientActivityId:string)`
- `FindCIDPast24h(clientActivityId:string)`
- `FindQueryEssentials(rootActivityId:string)`
- `FindRIDPast1w(rid:string)`
- `FindRIDPast24h(rid:string)`

### Shortcuts

- `Admins()`
- `Alerts()`
- `CmOperations()`
- `CmOperationsResults()`
- `CmServiceOperations()`
- `CmUsage()`
- `CommandCompletion()`
- `CriticalTraces()`
- `DataCapacityHistoryMv()`
- `DataIngest()`
- `DataIngestHistoryMv()`
- `DataOperations()`
- `DataOperationsHistoryMv()`
- `Deployments()`
- `DiagnosticsResults()`
- `DimClusters()`
- `DimClustersDailyMv()`
- `DimClustersMv()`
- `DmMemento()`
- `DmPurgeCommands()`
- `DmSettings()`
- `DmSettingsMv()`
- `DmUsage()`
- `KubernetesContainersStdoutLogs()`
- `KubernetesEvents()`
- `KuiperFlights()`
- `KuiperMetrics()`
- `KuiperTelemetry()`
- `KustoLogs()`
- `KustoMdmMetricsV1()`
- `KustoWorkloadLogs()`
- `LegacyMetadataContainersDeletions()`
- `MaHeartBeats()`
- `Memento()`
- `MetadataContainersDeletion()`
- `OverallQueryStats()`
- `PerfCounterEvent()`
- `QueryCompletion()`
- `SqlMonitoringAttachMv()`
- `TraceTelemetry()`
- `TraceTelemetryResults()`
- `Usage()`
- `UsageDailyMv()`
- `WebJobsLogs()`

### Static

- `GetCoresFromSKU(sku:string)`
- `parse_rust_timespan(tss:string)`

### Telemetry

- `ClusterDataCapacity()`

### Trident

- `GetTridentHosters(HosterKind:string)`
- `TridentDimClusters(excludePreprovisioned:bool)`
- `TridentTestTenants()`
- `TridentUsageDaily(StartTime:datetime)`

### V3Migration

- `FindDMs(engine_name:string)`
- `V3MigrationProgress(migration:string, userfilter:string="any")`

