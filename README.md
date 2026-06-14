<div align="center">

# ClosedLoop

**The first CFO-native AI operating system. Close the loop on every financial decision — from variance to verdict, with machine-readable provenance.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-green.svg)](https://python.org)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-purple.svg)](https://github.com/langchain-ai/langgraph)
[![Vertex AI](https://img.shields.io/badge/Cloud-GCP%20Vertex%20AI-blue.svg)](https://cloud.google.com/vertex-ai)

</div>

---

## The Problem

Most CFOs run an **open loop**: a decision is made, executed, and never measured against its own assumptions. Variance analysis is written once, read once, archived forever. Institutional knowledge lives in one person's head. Every layer of the org chart adds latency and loses signal.

| Open Loop (status quo) | ClosedLoop |
|---|---|
| Senior controller carries 80% of institutional knowledge in their head | Decisions live in a structured Notion DB the LLM can query |
| Variance commentary is written, read once, archived | Variance becomes a decision row that next month's run retrieves |
| Each layer of the org chart adds latency and loses signal | Four agents replace translation; humans approve, don't transcribe |
| Audit trail is reconstructed from emails | Every run writes an immutable, hash-stamped audit note |

**Velocity in finance = velocity of information flow.** Removing every layer of human routing is a direct speed gain — without losing control, because the human still gates every external write.

---

## What ClosedLoop Does

ClosedLoop turns your monthly close from a one-way street into a **self-improving feedback loop**. Every cycle:

1. **Ingests** source evidence (Drive/SharePoint/ERP exports)
2. **Separates facts from assumptions** — pandas computes, LLM reasons
3. **Flags decisions required** — what needs human judgment
4. **Captures decisions** in a structured Notion Decision Log
5. **Retrieves prior decisions** on the next cycle — the feedback signal
6. **Closes the loop** — variance becomes lessons, lessons become recommendations

The Memory Agent on cycle N+1 retrieves what the Memory Agent wrote on cycle N. **That is the feedback signal the next brief is built on.**

---

## Two Layers, One System

| Path | Who It's For | What You Get |
|------|-------------|--------------|
| **Template + Claude Cowork** | CFOs and finance leaders who want the methodology now | Folder structure, Notion setup, Claude Cowork skill pack — no code required |
| **4-Agent Stack (Vertex AI)** | Eng teams standing up an agentic finance build | LangGraph orchestrator, 4 specialist agents, Notion memory, audit trail |

Both layers share the same source of truth: your file system + a Notion Decision Log you create once.

---

## Architecture

```
START -> evidence -> analyst -> memory_retrieve -> cfo_brief
                                                      |
                                              interrupt_before
                                                      |
                                            human approval (CLI / UI)
                                                      |
                                                      v
                                              memory_write -> END
```

### The 4 Agents

| Agent | Job | LLM? | Why |
|---|---|---|---|
| **Evidence** | Load every file, parse, hash, return typed Evidence | No | Deterministic — no LLM in the loading path |
| **Analyst** | Variance / cut-off / cash / inventory analysis. Splits facts vs. assumptions | Gemini 2.5 Pro | Pandas computes; LLM reasons over grounded summaries only |
| **Memory** | Retrieve prior decisions (Notion + Vector Search) before the brief; write back only after human approval | Gemini 2.5 Flash | Two layers: Vertex AI Vector Search + Notion Decision Log |
| **CFO Brief** | Synthesize close memo + 3 board messages + proposed Notion rows | Gemini 2.5 Pro | Full provenance — every claim traces to agent + grounding + CHP finding |

### Trust Model

| Layer | Mechanism |
|---|---|
| **Evidence** | SHA-256 hash for every file; no LLM in the loading path |
| **Analysis** | Pandas computes numbers deterministically; LLM reasons over grounded summaries only |
| **Validation** | JSON-schema-checked LLM output; typed Findings and CFOBrief objects |
| **Human gate** | `interrupt_before=["memory_write"]` — no external write without explicit approval |
| **Audit** | Immutable note listing inputs, agents, outputs, decisions |
| **Memory** | Notion DB is append-only by convention; corrections are new rows referencing prior notion_id |

---

## Quickstart — No Code (Claude Cowork)

1. Clone the repo to a folder you sync with Google Drive
2. Open `00 Claude Setup/project-instructions.md` and replace the tokens
3. Create the Notion page + Decision Log database
4. Install the ClosedLoop skill pack in Claude Cowork (4 base skills in `skills/`)
5. Drop a close pack into `03 Monthly Close/YYYY-MM Month Close/` and prompt:
   ```
   Run the closed-loop close review: produce the CFO close summary,
   identify open issues and follow-ups, propose Notion Decision Log
   entries (do not write yet), and write the audit note.
   ```

---

## Quickstart — Agent Stack (Vertex AI)

```bash
git clone https://github.com/icohangar-ops/closedloop.git
cd closedloop/agents
cp .env.example .env       # fill in GCP_PROJECT_ID, NOTION_TOKEN, NOTION_DECISION_DB_ID
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# (one-time) Index the Drive corpus into Vertex Vector Search
python scripts/index_corpus.py --root ..

# Run the closed-loop graph for a period
python -m src.run --period "2026-03 March Close"
```

---

## Tech Stack

| Component | Choice | Why |
|---|---|---|
| Cloud platform | **GCP Vertex AI** | Native Gemini access, Vector Search, Cloud SQL for state |
| Reasoning model | `gemini-2.5-pro` | Long-context for whole close packs, strong reasoning |
| Fast model | `gemini-2.5-flash` | Cheap deterministic tasks |
| Orchestrator | **LangGraph** | First-class state, checkpointing, interrupts, observability |
| State persistence | `SqliteSaver` (dev) → `PostgresSaver` on Cloud SQL (prod) | Resume runs across days/operators |
| Structured memory | **Notion** Decision Log DB | Human-legible, filterable, audit-friendly |
| File parsing | Pandas, openpyxl, pypdf | Deterministic numerical inputs to the Analyst |

---

## Cost

Typical end-to-end run: **low cents to low dollars** at current Vertex pricing. The dominant factor is the Pro context window if your close pack is large.

---

## Project Structure

```
closedloop/
├── 00 Claude Setup/          <- Cowork instructions, Notion setup
├── 01 Company Context/       <- charter, KPIs
├── 02 Board Meetings/        <- per-meeting subfolders
├── 03 Monthly Close/         <- one subfolder per close
├── 04 FP&A/                  <- forecast, scenarios
├── 05 Decisions Log/         <- Notion import seed
├── 06 Finance Processes/     <- close SOP, controls
├── 07 Audit Trail/           <- auto-generated
├── skills/                   <- ClosedLoop skill pack
└── agents/                   <- 4-agent reference build
    ├── src/
    │   ├── run.py
    │   ├── orchestrator/graph.py
    │   ├── agents/{evidence,analyst,memory,cfo_brief}.py
    │   ├── tools/{drive_loader,pandas_tool,notion_client,vector_store}.py
    │   └── state/schema.py
    ├── docs/                 <- 6 docs: arch, deploy, demo, runbook
    └── tests/                <- 129 tests
```

---

## Roadmap

- [ ] Replace SqliteSaver with PostgresSaver on Cloud SQL for multi-operator state
- [ ] Add a forecast agent that reads `04 FP&A/` and runs scenario sensitivity
- [ ] LangSmith traces wired by default
- [ ] Slack notifier on memo + audit note write
- [ ] Read-only Notion mirror to a Postgres view for BI tooling

---

## License

MIT. See [`LICENSE`](./LICENSE).

---

## CHP Governance

This repository is hardened with the [Consensus Hardening Protocol (CHP)](https://codeberg.org/cubiczan/consensus-hardening-protocol), Cubiczan's decision-governance layer for multi-agent AI systems.

### Protocol Layers
- **R0 Gate**: All decisions must pass Solvable, Scoped, Valid, Worth_it checks
- **Foundation Disclosure**: 1-3 weakest assumptions, 1-2 invalidation conditions, 1 key vulnerability
- **Adversarial Layer**: Mandatory devil's advocate at Phase 0 and Round 3
- **State Machine**: EXPLORING → PROVISIONAL → PROVISIONAL_LOCK → LOCKED
- **Third-Party Validation**: Independent CONFIRM/REJECT before lock

### Domain Configuration
- **Category**: Finance (CFO Accuracy)
- **Foundation Threshold**: 100
- **CFO Accuracy Guard**: Enabled

### Compliance Artifacts
| File | Purpose |
|------|---------|
| `.chp/STATE_MACHINE.md` | Decision state transitions |
| `.chp/R0_CONFIG.yaml` | Domain-calibrated thresholds |
| `.chp/ADVERSARIAL_PROMPTS.md` | Standardized challenge templates |
| `.chp/CHP_COMPLIANCE.md` | Compliance tracking & audit trail |

### CHP Version
cognitive-mesh-orchestrator 0.1.0 | [Protocol Docs](https://codeberg.org/cubiczan/consensus-hardening-protocol)
