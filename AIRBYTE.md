# Airbyte Agents Integration — Closed Loop Finance

This document describes how [Airbyte Agents](https://docs.airbyte.com/ai-agents) can replace the manual file-drop workflow with live data from ERP, billing, banking, and CRM systems for your 4-agent LangGraph finance pipeline.

---

## Overview

Airbyte Agents provides a data and context layer for AI agents. For Closed Loop Finance, it can:

- **Replace Drive file drops** with scheduled syncs from ERP/banking/CRM to a staging database
- **Add live financial data feeds** — Stripe MRR, Salesforce pipeline, QuickBooks GL — directly into the Evidence Agent's input
- **Provide MCP access** for the Analyst and CFO Brief agents to query live data during analysis

**Integration options:**
- **[MCP](https://docs.airbyte.com/ai-agents/interfaces/mcp)** — Remote Model Context Protocol server. Best for agentic queries during the analysis phase.
- **[SDK](https://docs.airbyte.com/ai-agents/interfaces/sdk)** — `airbyte_agent_sdk` Python library. Best for pre-loading evidence into the agent pipeline.
- **[CLI/API](https://docs.airbyte.com/ai-agents/interfaces/sdk)** — Shell and HTTP interfaces.

---

## Integration Points

### 1. Evidence Agent: Replace File Drops with Airbyte Syncs

The **Evidence Agent** currently loads files from Google Drive (local filesystem) — GL, P&L, Balance Sheet, Cash Flow, and close packs. Airbyte can sync this data directly from source systems.

**Recommended Airbyte sources to replace Drive file drops:**

| Data Domain | Airbyte Source | Replaces |
|-------------|---------------|----------|
| **General Ledger** | QuickBooks / Xero / NetSuite | Manual GL CSV exports |
| **Revenue** | Stripe / Chargebee / Recurly | Manual MRR/ARR exports |
| **Payroll** | Gusto / Rippling / BambooHR | Manual headcount cost exports |
| **Banking** | Plaid / Stripe Treasury | Manual bank statement CSV |
| **CRM Pipeline** | Salesforce / HubSpot | Manual pipeline exports |
| **Expenses** | Bill.com / Expensify / Concur | Manual expense report exports |
| **Inventory** | Cin7 / Fishbowl / Zoho Inventory | Manual inventory CSV |

**Example — Using the SDK to pre-load evidence:**

```python
from airbyte_agent_sdk import connect

async def gather_evidence(period: str) -> dict:
    """Pre-load financial evidence from Airbyte-connected sources."""
    evidence = {}
    
    # Pull revenue data from Stripe
    stripe = connect("stripe")
    try:
        invoices = await stripe.execute("invoices", "list", params={
            "status": "paid",
            "date_range": period,
        })
        evidence["revenue"] = invoices.data
    finally:
        await stripe.close()
    
    # Pull pipeline data from Salesforce
    sf = connect("salesforce")
    try:
        deals = await sf.execute("opportunities", "list", params={
            "stage": "closed_won",
            "close_date": period,
        })
        evidence["pipeline"] = deals.data
    finally:
        await sf.close()
    
    return evidence
```

### 2. Analyst Agent: Live Queries via MCP

During the Analyst step, the agent can use MCP to query live data:

```json
// Add to your MCP client config
{
  "mcpServers": {
    "airbyte": {
      "url": "https://mcp.airbyte.ai/mcp"
    }
  }
}
```

**Example Agent prompt:**
> Connect my QuickBooks account via Airbyte MCP. Pull the current month's P&L and compare it to last month's. Identify any variances > 5%.

### 3. Memory Agent: Sync Notion Decision Log

The **Memory Agent** reads from a Notion Decision Log database. Airbyte can:

- Sync Notion decisions to a data warehouse for BI/reporting (reverse ETL)
- Feed historical decisions into Vertex Vector Search for better retrieval

### 4. CFO Brief Agent: Enrich with Airbyte Data

The **CFO Brief Agent** synthesizes the final memo. MCP-connected data sources let it include live metrics:

- Current cash position (via Stripe Treasury or bank connector)
- MRR/ARR trends (via Stripe connector)
- Pipeline health (via Salesforce connector)
- Headcount costs (via payroll connector)

---

## Architecture: Airbyte + LangGraph

```
┌─────────────────────────────────────────────────────────┐
│                   Airbyte Agents                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Stripe   │  │Salesforce│  │QuickBooks│  ... 30+     │
│  │ Source   │  │ Source   │  │ Source   │  Connectors  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │             │             │                    │
│  ┌────▼─────────────▼─────────────▼────┐               │
│  │      MCP Server / SDK / API        │               │
│  └────────────────┬───────────────────┘               │
└───────────────────┼───────────────────────────────────┘
                    │
┌───────────────────▼───────────────────────────────────┐
│              Closed Loop Finance Pipeline              │
│                                                        │
│  START → Evidence → Analyst → Memory → CFO Brief → END│
│           ▲ Airbyte      ▲ MCP       ▲ MCP             │
│           │  Preload     │ Live      │ Enrichment       │
│           └──────────────┴───────────┘                 │
└────────────────────────────────────────────────────────┘
```

---

## Getting Started

1. **Sign up** at [app.airbyte.ai](https://app.airbyte.ai).
2. **Install the SDK** (Python):
   ```bash
   uv add airbyte-agent-sdk
   ```
3. **Add to your `.env.example`**:
   ```
   AIRBYTE_CLIENT_ID=your_client_id
   AIRBYTE_CLIENT_SECRET=your_client_secret
   ```
4. **Create `agents/src/tools/airbyte_loader.py`** — an Airbyte wrapper tool that the Evidence Agent calls to load synced data instead of Drive files.

---

## Connector Catalog

| Category | Connectors |
|----------|-----------|
| **Accounting/ERP** | QuickBooks, Xero, NetSuite, Sage Intacct |
| **Billing** | Stripe, Chargebee, Recurly, Braintree |
| **Payroll/HRIS** | Gusto, Rippling, BambooHR, Workday |
| **CRM** | Salesforce, HubSpot, Zendesk Sell |
| **Banking** | Plaid, Stripe Treasury, Mercury |
| **Expenses** | Bill.com, Expensify, Concur |
| **Data Warehouse** | Snowflake, BigQuery, Postgres, Redshift |

Full catalog: [docs.airbyte.com/ai-agents/connectors](https://docs.airbyte.com/ai-agents/connectors)
