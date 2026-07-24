# pf-teams-insights — MCP Server para Microsoft Teams

Le mensagens do Teams via Microsoft Graph API para uso no Claude Desktop.

## Arquivos

```
teams-insights/
├── mcp_server.py              # MCP server (FastMCP + stdio)
├── setup_claude_desktop.py    # Configura claude_desktop_config.json
├── core/
│   ├── __init__.py
│   ├── auth.py                # MSAL auth (delegated, public client)
│   └── graph.py               # Graph API helpers
```

## Setup (Windows)

### 1. Copiar arquivos
Copiar todo o conteudo de `core/` e `mcp_server.py` para:
```
C:\Users\inael\OneDrive\Documentos\ClaudeDesktop\SEOP\teams-insights\
```

### 2. Instalar dependencias
```cmd
py -3 -m pip install --user mcp msal requests
```

### 3. Configurar Claude Desktop
```cmd
py -3 setup_claude_desktop.py
```
Ou manualmente, adicionar em `%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "pf-teams-insights": {
      "command": "py",
      "args": ["-3", "C:\\Users\\inael\\OneDrive\\Documentos\\ClaudeDesktop\\SEOP\\teams-insights\\mcp_server.py"]
    }
  }
}
```

### 4. Reiniciar Claude Desktop

### 5. Testar
Perguntar ao Claude Desktop: "quem sou eu no Teams?" (tool: whoami)

## Tools disponiveis

| Tool | Input | Retorno |
|------|-------|---------|
| `whoami` | — | `{displayName, upn}` |
| `teams_list` | — | `[{id, displayName}]` |
| `teams_channels` | `team_id` | `[{id, displayName}]` |
| `teams_messages` | `team_id, channel_id, limit?, since_iso?` | `[{from, created, body_text}]` |
| `chats_list` | — | `[{id, topic, chatType}]` |
| `chats_messages` | `chat_id, limit?, since_iso?` | `[{from, created, body_text}]` |

## Credenciais

Lidas em runtime de `~/.claude/credentials/services.env` (nunca commitadas).
Chaves esperadas: `SEOP_TEAMS_TENANT_ID`, `SEOP_TEAMS_CLIENT_ID`, `SEOP_TEAMS_CLIENT_SECRET`, `SEOP_TEAMS_REDIRECT_URI`, `SEOP_TEAMS_SCOPES`.
