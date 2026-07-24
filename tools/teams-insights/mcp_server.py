"""MCP Server: pf-teams-insights — read Teams messages via Microsoft Graph."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP  # noqa: E402
from core.auth import acquire_token  # noqa: E402
from core.graph import (  # noqa: E402
    whoami as graph_whoami,
    list_joined_teams,
    list_channels,
    channel_messages,
    list_chats,
    chat_messages,
)

mcp = FastMCP("pf-teams-insights")


def _token() -> str:
    print("[mcp] Acquiring token...", file=sys.stderr)
    t = acquire_token()
    print("[mcp] Token OK", file=sys.stderr)
    return t


@mcp.tool()
def whoami() -> str:
    """Returns the current authenticated user's name and UPN (email)."""
    return json.dumps(graph_whoami(_token()), ensure_ascii=False)


@mcp.tool()
def teams_list() -> str:
    """Lists all Teams the user has joined. Returns [{id, displayName}]."""
    return json.dumps(list_joined_teams(_token()), ensure_ascii=False)


@mcp.tool()
def teams_channels(team_id: str) -> str:
    """Lists channels in a Team. Returns [{id, displayName}]."""
    return json.dumps(list_channels(_token(), team_id), ensure_ascii=False)


@mcp.tool()
def teams_messages(
    team_id: str,
    channel_id: str,
    limit: int = 25,
    since_iso: str = "",
) -> str:
    """Reads messages from a Team channel. Returns [{from, created, body_text}].
    HTML is stripped from body. Optional: limit (default 25), since_iso (ISO 8601 filter)."""
    return json.dumps(
        channel_messages(_token(), team_id, channel_id, limit, since_iso),
        ensure_ascii=False,
    )


@mcp.tool()
def chats_list() -> str:
    """Lists the user's 1:1 and group chats. Returns [{id, topic, chatType}]."""
    return json.dumps(list_chats(_token()), ensure_ascii=False)


@mcp.tool()
def chats_messages(
    chat_id: str,
    limit: int = 25,
    since_iso: str = "",
) -> str:
    """Reads messages from a chat. Returns [{from, created, body_text}].
    HTML is stripped. Optional: limit (default 25), since_iso (ISO 8601 filter)."""
    return json.dumps(
        chat_messages(_token(), chat_id, limit, since_iso),
        ensure_ascii=False,
    )


if __name__ == "__main__":
    print("[mcp] Starting pf-teams-insights server...", file=sys.stderr)
    mcp.run()
