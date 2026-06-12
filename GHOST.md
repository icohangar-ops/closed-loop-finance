# Ghost Integration — Closed Loop Finance

This document describes how [Ghost](https://ghost.build) — the Postgres database built for AI agents — can replace the file-based evidence pipeline with forkable, per-period databases for your 4-agent LangGraph finance pipeline.

---

## Overview

Ghost provides unlimited Postgres databases you can create, fork, and discard freely. For Closed Loop Finance, this means:

- **One database per close period** — each month's close gets its own isolated Postgres
- **Fork for variance analysis** — clone a period's data to test "what if" scenarios
- **PostgresSaver native** — Ghost Postgres is a drop-in for the pipeline's `PostgresSaver` checkpointer
- **MCP tools for agents** — the Evidence/Analyst/CFO Brief agents can query live data

**Key Ghost commands:**
```bash
brew install timescale/tap/ghost       # Install
ghost init                               # Configure
ghost create close-2026-03               # One DB per close period
ghost fork close-2026-03 close-2026-03-whatif  # Fork to experiment
ghost sql close-2026-03 "SELECT * FROM financial_statements"  # Query
ghost share close-2026-03               # Share with auditor
```

---

## Integration Points

### 1. Per-Period Database Isolation

```bash
# March close
ghost create close-2026-03

# Seed it with financial data (synced via Airbyte)
ghost sql close-2026-03 "
  INSERT INTO financial_statements (period, statement_type, data)
  VALUES ('2026-03', 'P&L', '{"revenue": 12000000, "cogs": 7200000, "opex": 3100000}'),
         ('2026-03', 'BS', '{"cash": 45000000, "ar": 8200000, "ap": 5300000}'),
         ('2026-03', 'CF', '{"operating": 2100000, "investing": -800000, "financing": -500000}');
"

# April close
ghost create close-2026-04
# ... same structure, different data
```

### 2. Fork for Variance Analysis

The **Analyst Agent** identifies variances. Ghost fork lets you dig into them:

```bash
# Fork the current period
ghost fork close-2026-04 close-2026-04-var-deepdive

# Run the Analyst Agent with different assumptions
agents/src/run.py --ghost-db close-2026-04 --period 2026-04
agents/src/run.py --ghost-db close-2026-04-var-deepdive --period 2026-04 --scenario "revenue_recognition_change"

# Compare findings
ghost sql close-2026-04 "SELECT finding, variance_pct FROM variance_analysis"
ghost sql close-2026-04-var-deepdive "SELECT finding, variance_pct FROM variance_analysis"

# Delete the experiment
ghost delete close-2026-04-var-deepdive
```

### 3. Replace SqliteSaver with Ghost PostgresSaver

The pipeline uses `SqliteSaver` for dev and `PostgresSaver` for prod. Ghost is production-grade Postgres:

```python
# Before: SqliteSaver
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

# After: Ghost PostgresSaver
import os
from langgraph.checkpoint.postgres import PostgresSaver

GHOST_DB = os.getenv("GHOST_DEFAULT_DB", "close-dev")
GHOST_URI = os.getenv("GHOST_CONNECTION_STRING")

checkpointer = PostgresSaver.from_conn_string(GHOST_URI)
```

### 4. MCP Integration for Agent Workflows

Install Ghost MCP:
```bash
ghost mcp install claude-code
```

**Example prompts for the Finance AI agent:**
> Create a Ghost database for the March 2026 close. Seed it with the financial statement schema. Fork it into three scenarios: aggressive revenue recognition, conservative accruals, and as-reported. Run the pipeline against all three.

> Connect to the Ghost database `close-2026-03` via MCP and run variance analysis against last month's data.

### 5. State Schema → Ghost Tables

The `GraphState` TypedDict fields map to Ghost Postgres tables:

```sql
-- Graph state persistence
CREATE TABLE graph_s loaf_state (
    thread_id TEXT PRIMARY KEY,
    period TEXT,
    evidence JSONB,
    findings JSONB,
    prior_decisions JSONB,
    cfo_brief JSONB,
    human_approved BOOLEAN,
    approver TEXT,
    notion_rows_written JSONB,
    messages JSONB,
    errors JSONB,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
```

---

## Architecture

```
Airbyte Agents (data sync)
    │
    ▼
Ghost Postgres DBs         ─── per close period
    │                           per scenario fork
    │
    ├── LangGraph PostgresSaver  ← graph state checkpoints
    ├── Evidence Agent           ← loads financial data
    ├── Analyst Agent            ← runs variance analysis
    ├── Memory Agent             ← reads/writes Notion decisions
    └── CFO Brief Agent          ← synthesizes memo
                                    │
                          Ghost MCP (tools)
                                    │
                            Claude / Codex / Cursor
```

---

## Getting Started

1. **Install Ghost:**
   ```bash
   brew install timescale/tap/ghost
   ghost init
   ```
2. **Create a development database:**
   ```bash
   ghost create close-dev
   ```
3. **Run the schema:**
   ```bash
   ghost sql close-dev < agents/src/state/schema.sql
   ```
4. **Install the MCP server:**
   ```bash
   ghost mcp install claude-code
   ```
5. **Add to `.env.example`:**
   ```
   GHOST_API_KEY=***   GHOST_DEFAULT_DB=close-dev
   ```

---

## Resources
- [Ghost Documentation](https://ghost.build/docs)
- [Ghost MCP Tools](https://ghost.build/docs/#mcp-integration)
- [Ghost API Reference](https://ghost.build/docs/#api-reference)
- [LangGraph PostgresSaver Docs](https://langchain-ai.github.io/langgraph/concepts/persistence/#postgres)
