"""Microsoft Graph API helpers for Teams read operations."""

import re
from typing import Any

import requests

_GRAPH = "https://graph.microsoft.com/v1.0"


def get(token: str, url: str, params: dict[str, str] | None = None) -> Any:
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def _strip_html(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html or "").strip()


def _msg_record(m: dict) -> dict:
    sender = m.get("from") or {}
    user = sender.get("user") or {}
    return {
        "from": user.get("displayName", "unknown"),
        "created": m.get("createdDateTime", ""),
        "body_text": _strip_html((m.get("body") or {}).get("content", "")),
    }


def whoami(token: str) -> dict:
    data = get(token, f"{_GRAPH}/me")
    return {
        "displayName": data.get("displayName"),
        "upn": data.get("userPrincipalName"),
    }


def list_joined_teams(token: str) -> list[dict]:
    data = get(token, f"{_GRAPH}/me/joinedTeams")
    return [
        {"id": t["id"], "displayName": t["displayName"]}
        for t in data.get("value", [])
    ]


def list_channels(token: str, team_id: str) -> list[dict]:
    data = get(token, f"{_GRAPH}/teams/{team_id}/channels")
    return [
        {"id": c["id"], "displayName": c["displayName"]}
        for c in data.get("value", [])
    ]


def channel_messages(
    token: str,
    team_id: str,
    channel_id: str,
    limit: int = 25,
    since_iso: str = "",
) -> list[dict]:
    url = f"{_GRAPH}/teams/{team_id}/channels/{channel_id}/messages"
    params: dict[str, str] = {"$top": str(limit)}
    if since_iso:
        params["$filter"] = f"lastModifiedDateTime ge {since_iso}"
    try:
        data = get(token, url, params)
    except requests.HTTPError:
        params.pop("$filter", None)
        data = get(token, url, params)
    return [_msg_record(m) for m in data.get("value", [])]


def list_chats(token: str) -> list[dict]:
    data = get(token, f"{_GRAPH}/me/chats")
    return [
        {"id": c["id"], "topic": c.get("topic", ""), "chatType": c.get("chatType", "")}
        for c in data.get("value", [])
    ]


def chat_messages(
    token: str,
    chat_id: str,
    limit: int = 25,
    since_iso: str = "",
) -> list[dict]:
    url = f"{_GRAPH}/me/chats/{chat_id}/messages"
    params: dict[str, str] = {"$top": str(limit)}
    if since_iso:
        params["$filter"] = f"lastModifiedDateTime ge {since_iso}"
    try:
        data = get(token, url, params)
    except requests.HTTPError:
        params.pop("$filter", None)
        data = get(token, url, params)
    return [_msg_record(m) for m in data.get("value", [])]
