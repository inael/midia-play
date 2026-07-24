"""Merge pf-teams-insights into Claude Desktop config (idempotent)."""

import json
import os
import sys

CONFIG_DIR = os.path.join(os.environ.get("APPDATA", ""), "Claude")
CONFIG_FILE = os.path.join(CONFIG_DIR, "claude_desktop_config.json")
MCP_ENTRY = {
    "command": "py",
    "args": [
        "-3",
        os.path.join(
            os.path.expanduser("~"),
            "OneDrive",
            "Documentos",
            "ClaudeDesktop",
            "SEOP",
            "teams-insights",
            "mcp_server.py",
        ),
    ],
}


def main() -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)

    config: dict = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, encoding="utf-8") as f:
            config = json.load(f)
        print(f"[setup] Loaded existing config: {CONFIG_FILE}")
    else:
        print(f"[setup] Creating new config: {CONFIG_FILE}")

    config.setdefault("mcpServers", {})
    config["mcpServers"]["pf-teams-insights"] = MCP_ENTRY

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"[setup] pf-teams-insights added to {CONFIG_FILE}")
    print("[setup] Restart Claude Desktop to load the MCP server.")


if __name__ == "__main__":
    main()
