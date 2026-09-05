"""
Cross-platform (Windows/macOS/Linux) fast KQL query runner, Python equivalent of
Invoke-KustoQuery.ps1. Reuses a cached AAD token (via kusto_token.get_token)
instead of spawning `az` per call, removing ~1-2s of Azure CLI startup latency
from every query in a multi-query investigation. Designed to be imported by
other scripts (e.g. invoke_health_check.py) as well as run standalone.

Usage (as a library):
    from invoke_kusto_query import run_query
    rows = run_query("DimClustersMv() | where Source == 'KUSKUSWEU' | take 5")
    rows = run_query(".show version", database="Kuskus")

Usage (CLI, prints one JSON object per row line, like query_kusto.py):
    python invoke_kusto_query.py "DimClustersMv() | where Source == 'KUSKUSWEU' | take 5"
    python invoke_kusto_query.py --database KustoAuto --cluster https://kuskusops.kusto.windows.net "KustoIcMIncidentsMV | take 1"
"""
import argparse
import json
import ssl
import sys
import urllib.request
import uuid
from urllib.error import HTTPError, URLError

from kusto_token import get_token

DEFAULT_CLUSTER = "https://kuskushead.westeurope.kusto.windows.net"
DEFAULT_DATABASE = "Kuskus"


def _build_https_opener() -> urllib.request.OpenerDirector:
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    return urllib.request.build_opener(urllib.request.HTTPSHandler(context=context))


def _rows_to_dicts(response: dict) -> list:
    if not response.get("Tables"):
        return []
    table = response["Tables"][0]
    columns = [column["ColumnName"] for column in table["Columns"]]
    return [dict(zip(columns, row)) for row in table["Rows"]]


def run_query(query: str, database: str = DEFAULT_DATABASE, cluster: str = DEFAULT_CLUSTER,
              retries: int = 3, timeout: int = 600) -> list:
    """Runs a KQL query/command against `cluster`/`database` and returns a list of dict rows."""
    token = get_token(cluster)
    endpoint = "/v1/rest/mgmt" if query.lstrip().startswith(".") else "/v1/rest/query"
    body = json.dumps({"db": database, "csl": query}).encode("utf-8")

    last_error = None
    for attempt in range(1, retries + 1):
        request = urllib.request.Request(
            cluster + endpoint,
            data=body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
                "Accept": "application/json",
                "x-ms-client-request-id": f"copilot-dh-py;{uuid.uuid4()}",
            },
            method="POST",
        )
        try:
            with _build_https_opener().open(request, timeout=timeout) as response:
                return _rows_to_dicts(json.loads(response.read().decode("utf-8")))
        except HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")
            # 401/403 likely means a stale cached token - refresh once and retry.
            if error.code in (401, 403) and attempt < retries:
                token = get_token(cluster, force_refresh=True)
                continue
            raise RuntimeError(f"Kusto HTTP {error.code}: {details}") from error
        except URLError as error:
            last_error = error
            if attempt == retries:
                break

    raise RuntimeError(f"Kusto request failed after {retries} attempts: {last_error}") from last_error


def _flatten_record(record: dict) -> dict:
    """Replace newlines in all string values so each record serializes to one line."""
    result = {}
    for k, v in record.items():
        if isinstance(v, str):
            result[k] = v.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
        else:
            result[k] = v
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a KQL query/command against a Kusto cluster (fast, cached-token).")
    parser.add_argument("query", nargs="?", default=".show version", help="KQL query or management command to execute.")
    parser.add_argument("--database", default=DEFAULT_DATABASE, help=f"Database name. Defaults to {DEFAULT_DATABASE}.")
    parser.add_argument("--cluster", default=DEFAULT_CLUSTER, help=f"Kusto cluster endpoint. Defaults to {DEFAULT_CLUSTER}.")
    args = parser.parse_args()

    rows = run_query(args.query, database=args.database, cluster=args.cluster)
    for record in rows:
        print(json.dumps(_flatten_record(record), default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
