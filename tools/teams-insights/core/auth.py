"""MSAL auth: load env from services.env + acquire delegated token."""

import os
import sys
import msal

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_BASE_DIR = os.path.dirname(_SCRIPT_DIR)
_CACHE_FILE = os.path.join(_BASE_DIR, ".msal_cache.bin")
_CREDENTIALS = os.path.join(
    os.path.expanduser("~"), ".claude", "credentials", "services.env"
)


def _parse_env(path: str) -> dict[str, str]:
    env: dict[str, str] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            env[key.strip()] = val.strip().strip("\"'")
    return env


def load_env() -> dict[str, str]:
    if not os.path.exists(_CREDENTIALS):
        raise FileNotFoundError(f"Credentials not found: {_CREDENTIALS}")
    return _parse_env(_CREDENTIALS)


def acquire_token() -> str:
    env = load_env()
    tenant_id = env["SEOP_TEAMS_TENANT_ID"]
    client_id = env["SEOP_TEAMS_CLIENT_ID"]
    scopes = env["SEOP_TEAMS_SCOPES"].split()
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    cache = msal.SerializableTokenCache()
    if os.path.exists(_CACHE_FILE):
        with open(_CACHE_FILE, encoding="utf-8") as f:
            cache.deserialize(f.read())

    app = msal.PublicClientApplication(
        client_id, authority=authority, token_cache=cache
    )

    result = None
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(scopes, account=accounts[0])

    if not result or "access_token" not in result:
        print("[auth] Cache miss — opening browser for login...", file=sys.stderr)
        result = app.acquire_token_interactive(scopes=scopes)

    if cache.has_state_changed:
        with open(_CACHE_FILE, "w", encoding="utf-8") as f:
            f.write(cache.serialize())

    if "access_token" not in result:
        err = result.get("error_description", str(result))
        raise RuntimeError(f"Token acquisition failed: {err}")

    print("[auth] Token acquired", file=sys.stderr)
    return result["access_token"]
