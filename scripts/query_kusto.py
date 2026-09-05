import argparse
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.request
import uuid
from urllib.error import HTTPError, URLError


CLUSTER = "https://kuskushead.westeurope.kusto.windows.net"
DATABASE = "Kuskus"
AZ_CMD_CANDIDATES = (
    r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
    r"C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
)


def get_az_cli_token() -> str:
    az_executable = next(
        (path for path in AZ_CMD_CANDIDATES if os.path.exists(path)),
        "az.cmd",
    )
    result = subprocess.run(
        [
            az_executable,
            "account",
            "get-access-token",
            "--resource",
            CLUSTER,
            "--query",
            "accessToken",
            "--output",
            "tsv",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    token = result.stdout.strip()
    if result.returncode != 0 or not token:
        error_text = result.stderr.strip() or "Azure CLI did not return an access token."
        raise RuntimeError(f"Failed to acquire Azure CLI token: {error_text}")
    return token


def build_https_opener() -> urllib.request.OpenerDirector:
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_2
    return urllib.request.build_opener(urllib.request.HTTPSHandler(context=context))


def execute_kusto(query: str, database: str, retries: int = 3) -> dict:
    endpoint = "/v1/rest/mgmt" if query.lstrip().startswith(".") else "/v1/rest/query"
    body = json.dumps({"db": database, "csl": query}).encode("utf-8")
    last_error = None
    for attempt in range(1, retries + 1):
        request = urllib.request.Request(
            CLUSTER + endpoint,
            data=body,
            headers={
                "Authorization": f"Bearer {get_az_cli_token()}",
                "Content-Type": "application/json; charset=utf-8",
                "Accept": "application/json",
                "x-ms-client-request-id": f"copilot-dh;{uuid.uuid4()}",
            },
            method="POST",
        )
        try:
            with build_https_opener().open(request, timeout=600) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Kusto HTTP {error.code}: {details}") from error
        except URLError as error:
            last_error = error
            if attempt == retries:
                break
            time.sleep(attempt)

    raise RuntimeError(f"Kusto request failed after {retries} attempts: {last_error}") from last_error


def rows_to_dicts(response: dict) -> list[dict]:
    if not response.get("Tables"):
        return []
    table = response["Tables"][0]
    columns = [column["ColumnName"] for column in table["Columns"]]
    return [dict(zip(columns, row)) for row in table["Rows"]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query the Kuskus Azure Data Explorer database with Python."
    )
    parser.add_argument(
        "query",
        nargs="?",
        default=".show version",
        help="KQL query or management command to execute.",
    )
    parser.add_argument(
        "--database",
        default=DATABASE,
        help=f"Database name. Defaults to {DATABASE}.",
    )
    parser.add_argument(
        "--cluster",
        default=CLUSTER,
        help=f"Kusto cluster endpoint. Defaults to {CLUSTER}.",
    )
    return parser.parse_args()


def flatten_record(record: dict) -> dict:
    """Replace newlines in all string values so each record serializes to one line."""
    result = {}
    for k, v in record.items():
        if isinstance(v, str):
            result[k] = v.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
        else:
            result[k] = v
    return result


def main() -> int:
    args = parse_args()
    global CLUSTER
    CLUSTER = args.cluster
    response = execute_kusto(args.query, args.database)
    for record in rows_to_dicts(response):
        print(json.dumps(flatten_record(record), default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
