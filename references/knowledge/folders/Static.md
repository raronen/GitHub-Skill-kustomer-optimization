# Static functions

Functions in folder `Static`.

## `GetCoresFromSKU`

- Folder: `Static`
- Parameters: `(sku:string)`
- Docstring: Number of cores for SKUs
- Usage example: `GetCoresFromSKU('sku-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
    case(
        sku contains "D4_v2", 8,
        sku contains "DS4_v2", 8,
        sku contains "D3_v2", 4,
        sku contains "16",16,
        sku contains "20",20,
        sku contains "32",32,
        sku contains "64",64,
        sku contains "80",80,
        sku contains "11", 2,
        sku contains "12", 4,
        sku contains "13", 8,
        sku contains "14", 16,
        sku contains "15", 20,
        sku contains "8", 8,
        sku contains "3",  4, // this is here for D3_v2
        sku contains "1",  1,
        sku contains "2",  2,
        sku contains "4",  4,
        0)
 }
```

## `parse_rust_timespan`

- Folder: `Static`
- Parameters: `(tss:string)`
- Docstring: No docstring provided.
- Usage example: `parse_rust_timespan('tss-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     let value1=todouble(substring(tss, 0, strlen(tss)-1));
     let value2=todouble(substring(tss, 0, strlen(tss)-2));
     case(
         tss endswith "ms", value2*1ms,
         tss endswith "µs", value2/1000.0*1ms,
         tss endswith "ns", value2/(1000000.0)*1ms,
         tss endswith  "s", value1*1s,
         -1s)
 }
```

