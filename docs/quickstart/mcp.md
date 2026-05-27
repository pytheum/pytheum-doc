# Quickstart — MCP

`pytheum-mcp` wraps the four [REST endpoints](../api/overview.md) as MCP tools so AI agents can query pytheum without writing their own retrieval layer.

| Tool | Endpoint |
|---|---|
| `t_find_markets(query, limit, group_by)` | [`/v1/markets/relevant-to`](../api/markets-relevant-to.md) |
| `t_market_context(market_ref, limit)` | [`/v1/markets/{ref}/context`](../api/markets-context.md) |
| `t_bundle_context(bundle_ref, limit)` | [`/v1/bundles/{ref}/context`](../api/bundles-context.md) |
| `t_event_related_markets(event_id, limit)` | [`/v1/events/{id}/related-markets`](../api/events-related.md) |

**Source:** [github.com/pytheum/pytheum-mcp](https://github.com/pytheum/pytheum-mcp) · **PyPI:** [`pytheum-mcp`](https://pypi.org/project/pytheum-mcp/) · **npm:** [`@pytheum/mcp`](https://www.npmjs.com/package/@pytheum/mcp)

## Install commands

Two distribution channels — both run the same Python server underneath. Pick whichever your client makes easier:

```bash
# npm (zero-Python install; recommended for Claude Desktop and any client without `uv`)
npx -y @pytheum/mcp

# PyPI (direct Python; needs `uv` — install via `curl -LsSf https://astral.sh/uv/install.sh | sh`)
uvx pytheum-mcp
```

Environment variable: `PYTHEUM_API_BASE` (default `https://api.pytheum.com`) — set to override the endpoint.

---

## Client matrix

| # | Client | Config path | Reload |
|---|---|---|---|
| 1 | [Claude Desktop](#claude-desktop) | macOS: `~/Library/Application Support/Claude/claude_desktop_config.json` · Win: `%APPDATA%\Claude\claude_desktop_config.json` | Cmd-Q + relaunch |
| 2 | [Claude Code (CLI)](#claude-code) | `~/.claude.json` or per-project `.mcp.json` | Auto next session; `/mcp` in-session |
| 3 | [Cursor](#cursor) | Global: `~/.cursor/mcp.json` · Project: `.cursor/mcp.json` | Settings → MCP → toggle |
| 4 | [Windsurf](#windsurf) | `~/.codeium/windsurf/mcp_config.json` | Refresh in Cascade panel |
| 5 | [Codex CLI (OpenAI)](#codex-cli) | `~/.codex/config.toml` | Restart `codex` |
| 6 | [VS Code (Copilot)](#vs-code) | Workspace: `.vscode/mcp.json` · User: cmd palette | `MCP: List Servers` |
| 7 | [Cline / Roo Code](#cline) | `cline_mcp_settings.json` (see below) | Auto on save |
| 8 | [Zed](#zed) | `settings.json` (`context_servers` key) | Auto on save |
| 9 | [OpenClaw](#openclaw) | `openclaw mcp set ...` | Gateway reconnect |
| 10 | [Goose](#goose) | `~/.config/goose/config.yaml` | Restart session |
| 11 | [Aider](#aider) | **No native MCP** — see workarounds | n/a |

### Universal footguns

- **Stripped PATH in desktop apps** — desktop apps don't inherit your terminal PATH. If `npx` or `uvx` works in Terminal but the client says "command not found," hard-code the absolute path: `/opt/homebrew/bin/npx` (Apple Silicon), `/usr/local/bin/npx` (Intel macOS / Linux).
- **Schema key differs per client** — `mcpServers` (most), `servers` (VS Code), `context_servers` (Zed), `mcp_servers` (Codex TOML), `extensions` (Goose YAML). Copy-paste across clients without renaming **will silently fail.**

---

### Claude Desktop

```json
{
  "mcpServers": {
    "pytheum": {
      "command": "npx",
      "args": ["-y", "@pytheum/mcp"]
    }
  }
}
```

Or via `uvx`:

```json
{
  "mcpServers": {
    "pytheum": {
      "command": "uvx",
      "args": ["pytheum-mcp"]
    }
  }
}
```

**Reload:** fully quit (Cmd-Q on macOS) and relaunch. **Verify:** the MCP slider icon in the prompt box lists `pytheum` with its tools. **Logs:** `~/Library/Logs/Claude/mcp-server-pytheum.log`.

> Claude Desktop bundles Node but **not Python**. For `uvx`, install `uv` first (`curl -LsSf https://astral.sh/uv/install.sh | sh`) and use an absolute path if PATH isn't picked up: `/opt/homebrew/bin/uvx`.

### Claude Code

```bash
# User scope (available across all your projects)
claude mcp add --transport stdio --scope user pytheum -- npx -y @pytheum/mcp

# Or via uvx
claude mcp add --transport stdio --scope user pytheum -- uvx pytheum-mcp

# Project scope (writes ./.mcp.json — commit to share with team)
claude mcp add --transport stdio --scope project pytheum -- npx -y @pytheum/mcp
```

**Verify:** `claude mcp list` (server should show `✓ Connected`) and `/mcp` panel in-session. The `--` separator before the command is required.

### Cursor

```json
{
  "mcpServers": {
    "pytheum": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@pytheum/mcp"]
    }
  }
}
```

**Reload:** Settings (Cmd+Shift+J) → Features → MCP → toggle pytheum off then on. Project config (`.cursor/mcp.json` at repo root) overrides global.

### Windsurf

```json
{
  "mcpServers": {
    "pytheum": {
      "command": "npx",
      "args": ["-y", "@pytheum/mcp"]
    }
  }
}
```

**Reload:** Refresh button in the Cascade MCP panel. **Footgun:** Windsurf has a hard 100-tool ceiling across all MCPs combined.

### Codex CLI

```bash
codex mcp add pytheum -- npx -y @pytheum/mcp
# or
codex mcp add pytheum -- uvx pytheum-mcp
```

Equivalent TOML in `~/.codex/config.toml`:

```toml
[mcp_servers.pytheum]
command = "npx"
args = ["-y", "@pytheum/mcp"]
```

**Verify:** `/mcp` inside the codex TUI. Note: TOML key is `mcp_servers` (snake_case), not the camelCase used elsewhere.

### VS Code

In `.vscode/mcp.json`:

```json
{
  "servers": {
    "pytheum": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@pytheum/mcp"]
    }
  }
}
```

**Reload:** Command Palette → `MCP: List Servers` → select pytheum → Restart Server. Top-level key is `servers` (not `mcpServers`).

### Cline / Roo Code

In the Cline panel, MCP Servers icon → "Configure MCP Servers" opens:

```json
{
  "mcpServers": {
    "pytheum": {
      "command": "npx",
      "args": ["-y", "@pytheum/mcp"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Config path:** `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` (macOS/Linux). Roo Code fork uses `rooveterinaryinc.roo-cline` in place of `saoudrizwan.claude-dev`. **Reload:** auto on save.

### Zed

In Zed `settings.json`:

```json
{
  "context_servers": {
    "pytheum": {
      "command": "npx",
      "args": ["-y", "@pytheum/mcp"],
      "env": {}
    }
  }
}
```

**Reload:** auto on save. Top-level key is `context_servers` (Zed's name for MCP servers).

### OpenClaw

```bash
openclaw mcp set pytheum --command "npx" --args "-y,@pytheum/mcp"
```

**Verify:** `openclaw mcp list`. Reload: gateway reconnect.

### Goose

```bash
goose configure
# → "Add Extension" → "Command-line Extension"
# → Name: pytheum
# → Command: npx -y @pytheum/mcp
```

Equivalent YAML in `~/.config/goose/config.yaml`:

```yaml
extensions:
  pytheum:
    name: pytheum
    type: stdio
    enabled: true
    cmd: npx
    args: ["-y", "@pytheum/mcp"]
    envs: {}
    timeout: 300
```

**Footgun:** YAML key is `cmd` (not `command`).

### Aider

**No native MCP support** as of 2026-05. Use one of the community bridges instead:
- [`mcpm-aider`](https://github.com/MCP-Mirror/mcpm-aider) — MCP-to-Aider bridge
- [`aider-mcp-client`](https://github.com/disler/aider-mcp-server) — community client wrapper

---

## Sample agent prompt

> *"Use pytheum to find Polymarket markets related to the Fed cutting rates in June. For the top match, pull the news context from the last 24 hours and summarize the directional signal."*

The agent calls `t_find_markets("fed cut june", group_by="bundle")` → picks top market → `t_market_context(<market_id>)` → summarizes.

## See also

- [API overview](../api/overview.md)
- [Concepts: embedding & pairing](../concepts/embedding-pairing.md)
- [SDKs index](../sdks/index.md)
