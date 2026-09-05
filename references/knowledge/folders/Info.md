# Info functions

Functions in folder `Info`.

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

