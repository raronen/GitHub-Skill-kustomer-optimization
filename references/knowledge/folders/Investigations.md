# Investigations functions

Functions in folder `Investigations`.

## `AdminCPU`

- Folder: `Investigations`
- Parameters: `(cluster:string, lookback:timespan=time(7.00:00:00), resolution:timespan=time(00:01:00))`
- Docstring: CPU of admin node
- Usage example: `AdminCPU('cluster-value', 1d, 1d) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.AdminCPU(cluster, lookback, resolution)
    )
 }
```

## `AdminHistory`

- Folder: `Investigations`
- Parameters: `(cluster:string, lookback:timespan=time(31.00:00:00))`
- Docstring: History of admin nodes on a cluster in a timespan (default 1 month)
- Usage example: `AdminHistory('cluster-value', 1d) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.AdminHistory(cluster, lookback)
    )
 }
```

## `AllKeyVaultChanges`

- Folder: `Investigations`
- Parameters: `(secretName:string="", clusterName:string="", duration:timespan=time(28.00:00:00))`
- Docstring: Find All Key Vault Changes
- Usage example: `AllKeyVaultChanges('secretName-value', 'clusterName-value', 1d) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.AllKeyVaultChanges(secretName, clusterName, duration)
    )
    | order by Timestamp desc 
 }
```

## `AriaBridgeConfigurationDeltaUpdateResults`

- Folder: `Investigations`
- Parameters: `(bridgeName:string, startTime:datetime)`
- Docstring: Get delta update results from provided Aria bridge
- Usage example: `AriaBridgeConfigurationDeltaUpdateResults('bridgeName-value', datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.AriaBridgeConfigurationDeltaUpdateResults(bridgeName, startTime)
    )
 }
```

## `AriaBridgeConfigurationUpdateFailures`

- Folder: `Investigations`
- Parameters: `(bridgeName:string, startTime:datetime)`
- Docstring: Get tenant update failures from provided Aria bridge
- Usage example: `AriaBridgeConfigurationUpdateFailures('bridgeName-value', datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.AriaBridgeConfigurationUpdateFailures(bridgeName, startTime)
    )
 }
```

## `DiskFirmware`

- Folder: `Investigations`
- Parameters: `(cluster:string)`
- Docstring: Find disk firmware
- Usage example: `DiskFirmware('cluster-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     let vms = cluster('azcrpbi.kusto.windows.net').database('bi_allprod').TenantModelProcessedVM
        | where TIMESTAMP > ago(3d)
        | where ResourceGroupName has cluster
        | extend Source = extract("^KUCOMPUTE-(.*?)(?:-S)?(?:-2)?$", 1, ResourceGroupName)
        | where Source == cluster
        | summarize arg_max(TIMESTAMP, VMId, VMName = Name, SubscriptionId) by ComputerName
    ;
     let vmids = vms | project VMId;
     let maptonodes = cluster('azcore.centralus.kusto.windows.net').database('AzureCP').MycroftContainerSnapshot
        | where TIMESTAMP > ago(3d)
        | where VirtualMachineUniqueId in (vmids)
        | summarize arg_max(TIMESTAMP, NodeId) by VMId = VirtualMachineUniqueId
    ;
     maptonodes
    | join kind=inner vms on VMId
    | join kind = inner
        (
        cluster("Azuredcm").database("AzureDCMDb").dcmInventoryComponentDisk
        | where IsPhysical == 1 // Only Physical drives
        )
        on NodeId
    | join kind = leftouter
        cluster("Azuredcm").database("AzureDCMDb").dcmInventoryComponentDiskUtil
        on NodeId, $left.DriveSerialNumber == $right.Serial
    | where DriveMountPoints != @"C:\" // Look only on data drive, not system one.
    | summarize
        by
        ComputerName,
        VMName,
        DriveProductId,
        Size,
        FirmwareRevision,
        VMId,
        NodeId,
        SubscriptionId
    | order by ComputerName asc
 }
```

## `GetClusterVMIds`

- Folder: `Investigations`
- Parameters: `(cluster:string)`
- Docstring: Get cluster VM ids - includes engine and DM VMs
- Usage example: `GetClusterVMIds('cluster-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     cluster('azcrpbi.kusto.windows.net').database('bi_allprod').TenantModelProcessedVM
    | where TIMESTAMP > ago(3d)
    | where ResourceGroupName has cluster
    | parse ResourceGroupName with ResourceType "-" *
    | summarize arg_max(Timestamp = TIMESTAMP, VmName = Name, ResourceType, SubscriptionId, VMId, VMSize) by Instance = ComputerName
    | order by ResourceType asc, Instance asc
 }
```

## `LatestKeyVaultChanges`

- Folder: `Investigations`
- Parameters: `(secretName:string="", clusterName:string="", duration:timespan=time(28.00:00:00))`
- Docstring: Find Latest Key Vault Changes
- Usage example: `LatestKeyVaultChanges('secretName-value', 'clusterName-value', 1d) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.LatestKeyVaultChanges(secretName, clusterName, duration)
    )
    | order by Timestamp desc 
 }
```

## `MapInstanceToVMId`

- Folder: `Investigations`
- Parameters: `(cluster:string, instance:string)`
- Docstring: Map instance to VM id
- Usage example: `MapInstanceToVMId('cluster-value', 'instance-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     cluster('azcrpbi.kusto.windows.net').database('bi_allprod').TenantModelProcessedVM
    | where TIMESTAMP > ago(3d)
    | where ResourceGroupName has cluster
    | where ComputerName =~ instance
    | parse ResourceGroupName with ResourceType "-" *
    | summarize arg_max(Timestamp = TIMESTAMP, VmName = Name, ResourceType, SubscriptionId, VMId, VMSize)
 }
```

## `MemStats`

- Folder: `Investigations`
- Parameters: `()`
- Docstring: Parses MEMORYSTATS traces
- Usage example: `MemStats() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MemStats
    )
 }
```

## `network_corruptions_raw`

- Folder: `Investigations`
- Parameters: `(horizon:datetime)`
- Docstring: Retrieve network corruption cases
- Usage example: `network_corruptions_raw(datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.network_corruptions_raw(horizon)
    )
 }
```

## `PerNodeQueryStats`

- Folder: `Investigations`
- Parameters: `(cid:string, lookback:timespan=time(7.00:00:00))`
- Docstring: Presents per-node query statistics in tabular format
- Usage example: `PerNodeQueryStats('cid-value', 1d) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.PerNodeQueryStats(cid, lookback)
    )
 }
```

## `RowStoreTrimOperations`

- Folder: `Investigations`
- Parameters: `(start:datetime, interval:timespan, sourceName:string)`
- Docstring: No docstring provided.
- Usage example: `RowStoreTrimOperations(datetime(2026-01-01), 1d, 'sourceName-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.RowStoreTrimOperations(start, interval, sourceName)
    )
 }
```

## `V3_FunctionsMissing`

- Folder: `Investigations`
- Parameters: `(_period:timespan)`
- Docstring: Show statistics of v3 missing functions
- Usage example: `V3_FunctionsMissing(1d) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.V3_FunctionsMissing(_period)
    )
    | summarize Count=sum(Count), Clusters=sum(Clusters) by Function
 }
```

