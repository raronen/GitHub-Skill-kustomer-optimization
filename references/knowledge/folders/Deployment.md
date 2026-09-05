# Deployment functions

Functions in folder `Deployment`.

## `FeatureFlagEnablements`

- Folder: `Deployment`
- Parameters: `(FF:string, Lookback:timespan=time(7.00:00:00))`
- Docstring: No docstring provided.
- Usage example: `FeatureFlagEnablements('FF-value', 1d) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.FeatureFlagEnablements(FF, Lookback)
    )
 }
```

## `FeatureFlagEnablementsInCluster`

- Folder: `Deployment`
- Parameters: `(Cluster:string, Lookback:timespan=time(7.00:00:00))`
- Docstring: No docstring provided.
- Usage example: `FeatureFlagEnablementsInCluster('Cluster-value', 1d) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.FeatureFlagEnablementsInCluster(Cluster, Lookback)
    )
 }
```

## `FeatureFlagsInCluster`

- Folder: `Deployment`
- Parameters: `(cluster:string)`
- Docstring: Shows feature flags existing in the cluster service configuration
- Usage example: `FeatureFlagsInCluster('cluster-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.FeatureFlagsInCluster(cluster)
    )
 }
```

## `FindFFsWithSubstring`

- Folder: `Deployment`
- Parameters: `(substring:string)`
- Docstring: No docstring provided.
- Usage example: `FindFFsWithSubstring('substring-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.FindFFsWithSubstring(substring)
    )
    | summarize count_ = sum(count_) by FF
    | order by FF asc
 }
```

## `StartUpLatestVersions1m`

- Folder: `Deployment`
- Parameters: `()`
- Docstring: Show versions from OnStart traces
- Usage example: `StartUpLatestVersions1m() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.StartUpLatestVersions1m
    )
 }
```

## `WhereFeatureFlag`

- Folder: `Deployment`
- Parameters: `(_ff:string)`
- Docstring: Shows clusters with specified feature flag
- Usage example: `WhereFeatureFlag('_ff-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.WhereFeatureFlag(_ff)
    )
 }
```

## `WhereFeatureFlagIsDisabled`

- Folder: `Deployment`
- Parameters: `(FeatureFlag:string, ServiceType:string="")`
- Docstring: Shows in how many clusters a specified feature flag is disabled by ring
- Usage example: `WhereFeatureFlagIsDisabled('FeatureFlag-value', 'ServiceType-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.WhereFeatureFlagIsDisabled(FeatureFlag, ServiceType)
    )
    | summarize
        TotalClusters = sum(TotalClusters),
        ClustersWithDisabledFF = sum(ClustersWithDisabledFF)
        by DeploymentRing
    | extend Percentage = ClustersWithDisabledFF * 100.0 / TotalClusters
    | order by TotalClusters desc
 }
```

## `WhereFeatureFlagIsEnabled`

- Folder: `Deployment`
- Parameters: `(FeatureFlag:string, ServiceType:string="")`
- Docstring: Shows in how many clusters a specified feature flag is enabled by ring
- Usage example: `WhereFeatureFlagIsEnabled('FeatureFlag-value', 'ServiceType-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.WhereFeatureFlagIsEnabled(FeatureFlag, ServiceType)
    )
    | summarize
        TotalClusters = sum(TotalClusters),
        ClustersWithEnabledFF = sum(ClustersWithEnabledFF)
        by DeploymentRing
    | extend Percentage = ClustersWithEnabledFF * 100.0 / TotalClusters
    | order by TotalClusters desc
 }
```

