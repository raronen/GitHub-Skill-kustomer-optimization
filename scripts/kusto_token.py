"""
Cross-platform (Windows/macOS/Linux) cached-token helper, Python equivalent of
Get-KustoToken.ps1. `az account get-access-token` typically costs 1-2s to spawn
per call; when an investigation issues several queries against the same
resource, repeating that call wastes several seconds. This module caches the
token + expiry as JSON under the OS temp dir, keyed by resource URI, and only
refreshes when within 5 minutes of expiry.

Usage (as a library):
    from kusto_token import get_token
    token = get_token("https://kuskushead.westeurope.kusto.windows.net")

Usage (CLI, prints the token to stdout):
    python kusto_token.py --resource https://kuskushead.westeurope.kusto.windows.net
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta

DEFAULT_RESOURCE = "https://kuskushead.westeurope.kusto.windows.net"

# Windows-only fixed install paths (az.cmd may not be on PATH in some shells).
# On macOS/Linux, `az` is normally already on PATH (Homebrew/pip installs), so
# shutil.which("az") below covers those platforms.
WINDOWS_AZ_CANDIDATES = (
    r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
    r"C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
)


def _resolve_az_executable() -> str:
    for candidate in WINDOWS_AZ_CANDIDATES:
        if os.path.exists(candidate):
            return candidate
    found = shutil.which("az") or shutil.which("az.cmd")
    return found or "az"


def _cache_file(resource: str) -> str:
    cache_key = re.sub(r"[^a-zA-Z0-9]", "_", resource)
    return os.path.join(tempfile.gettempdir(), f"kusto_token_{cache_key}.json")


def _read_cache(resource: str):
    path = _cache_file(resource)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            cached = json.load(f)
        expiry = datetime.fromisoformat(cached["expiry"])
        if expiry > datetime.now() + timedelta(minutes=5):
            return cached["token"]
    except Exception:
        pass  # Corrupt/unreadable cache - fall through and refresh.
    return None


def _write_cache(resource: str, token: str, expires_on: str) -> None:
    path = _cache_file(resource)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"token": token, "expiry": expires_on}, f)


def get_token(resource: str = DEFAULT_RESOURCE, force_refresh: bool = False) -> str:
    """Returns a cached (or freshly-fetched) AAD bearer token for `resource`."""
    if not force_refresh:
        cached = _read_cache(resource)
        if cached:
            return cached

    az_executable = _resolve_az_executable()
    result = subprocess.run(
        [az_executable, "account", "get-access-token", "--resource", resource, "--output", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        error_text = result.stderr.strip() or "Azure CLI did not return an access token."
        raise RuntimeError(f"Failed to acquire Azure CLI token for '{resource}': {error_text}")

    parsed = json.loads(result.stdout)
    token = parsed["accessToken"]
    # az's expiresOn is a naive local-time string like "2026-08-09 10:15:00.000000";
    # normalize to isoformat so datetime.fromisoformat can parse it back on read.
    expires_on = parsed.get("expiresOn") or parsed.get("expires_on")
    try:
        expiry_dt = datetime.strptime(expires_on.split(".")[0], "%Y-%m-%d %H:%M:%S")
    except (ValueError, AttributeError):
        expiry_dt = datetime.now() + timedelta(hours=1)
    _write_cache(resource, token, expiry_dt.isoformat())
    return token


def main() -> int:
    parser = argparse.ArgumentParser(description="Return a cached AAD access token for a Kusto resource.")
    parser.add_argument("--resource", default=DEFAULT_RESOURCE, help=f"Resource URI. Defaults to {DEFAULT_RESOURCE}.")
    parser.add_argument("--force-refresh", action="store_true", help="Ignore any cached token and fetch a new one.")
    args = parser.parse_args()
    print(get_token(args.resource, force_refresh=args.force_refresh))
    return 0


if __name__ == "__main__":
    sys.exit(main())
