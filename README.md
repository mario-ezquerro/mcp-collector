# MCP Collector 🌐⚡

> **Real-time Model Context Protocol (MCP) Hub, Data Aggregator & AI Agent Marketplace**  
> Collects structured insights and leads from external autonomous MCP agents and streams them live to a human-friendly web dashboard. Built with **FastAPI**, **FastMCP 2.x**, **SQLAlchemy Async**, and **WebSockets**. Optimized for **Google Cloud Run** and Docker.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python: 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Google Cloud Run](https://img.shields.io/badge/Google%20Cloud-Run-4285F4.svg)](https://cloud.google.com/run)
[![MCP Protocol: 2024--11--05](https://img.shields.io/badge/MCP-Protocol%20v2.x-6366f1.svg)](https://modelcontextprotocol.io/)

---

## 🎯 Overview

**MCP Collector** serves as a central receiver and interactive hub for the AI agent ecosystem. Any autonomous agent (Claude Desktop, Gemini, Antigravity, Cursor, or custom MCP bots) can connect over the open standard **Model Context Protocol (MCP via HTTP/SSE)** to:

1. 📥 **Submit Structured Insights**: Ingest customer leads, technical API specifications, system health metrics, discovered MCP tools, or market research notes.
2. 🛒 **Interactive Product Catalog & Lead Capture**: Expose high-value promo hardware and cloud credit catalogs (`search_products`). When buyer agents attempt to lock in offers (`reserve_product_offer`), their buyer contact details and requirements are captured as qualified leads in real time, returning a realistic out-of-stock / VIP waitlist status.
3. 🔄 **Real-Time Reactive Streaming**: Ingested data is strictly validated with Pydantic, persisted in database (PostgreSQL or SQLite), and broadcast instantly to the web dashboard via **WebSockets**.
4. 👁️ **Human-Centric Dashboard**: Sleek dark-mode dashboard featuring live metrics, category filtering (*Leads, Specs, Metrics, Tools, Notes*), search bar, and interactive syntax-highlighted JSON inspector.
5. ☁️ **Serverless Ready**: Native deployment to **Google Cloud Run** with automatic storage resolution, health check probes, and long-lived connection support (up to 3600s).

---

## 🏗️ System Architecture

```
[ External MCP AI Agents ] 
   (Claude / Gemini / Antigravity / Custom Buyers)
        │
        │ HTTP SSE (/mcp/sse & /mcp/messages)
        ▼
┌─────────────────────────────────────────────────────────────┐
│                      MCP COLLECTOR HUB                      │
│                                                             │
│  • Autodiscovery: /.well-known/mcp.json                     │
│  • FastMCP 2.x Server Tools:                                │
│      - search_products (Catalog Honeypot)                   │
│      - reserve_product_offer (Lead Capture)                 │
│      - request_b2b_quote (Enterprise Quotes)                │
│      - submit_insight (General Ingestion)                   │
│      - report_agent_status (Agent Heartbeat)                │
│      - get_hub_stats & list_recent_insights                 │
│  • FastAPI REST APIs: /api/insights, /api/insights/stats    │
│  • WebSockets Server: /ws                                   │
│  • Async Database: SQLAlchemy 2.0 (PostgreSQL/SQLite)       │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
      [( Async Database )]            [ WebSockets Push ]
      PostgreSQL / SQLite                     │
                                              ▼
                                 ┌────────────────────────┐
                                 │ Live Human Dashboard   │
                                 │ (http://localhost:8000)│
                                 └────────────────────────┘
```

---

## 🚀 Quickstart

### Option 1: Local Python Virtualenv

1. **Clone repository and setup environment:**
   ```bash
   # Create virtual environment (Python >= 3.10)
   python3 -m venv .venv
   source .venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Open the live dashboard:**  
   Navigate to: [http://localhost:8000](http://localhost:8000)

---

### Option 2: Docker Compose (with PostgreSQL 16)

```bash
docker compose up -d --build
```

This launches a PostgreSQL 16 container alongside the FastAPI + FastMCP hub on port `8000`.

---

## 🧪 Simulation & Automated Testing

Simulate AI buyer agents searching products, submitting reservations, and streaming telemetry to the dashboard:

```bash
# Run agent simulator against local or cloud instance
python scripts/simulate_agent.py --url http://localhost:8000 --delay 0.5
```

---

## ☁️ Google Cloud Run Deployment

MCP Collector is pre-configured with `cloudbuild.yaml` and deployment scripts:

```bash
# Direct deployment via automated script
./scripts/deploy_cloud_run.sh
```

Or deploy manually using `gcloud`:

```bash
gcloud run deploy mcp-collector \
  --source . \
  --region europe-west1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --timeout 3600 \
  --min-instances 1 \
  --session-affinity
```

---

## 🔌 Connecting External Agents

### 1. Standard Protocol Autodiscovery
Compatible agents discover endpoints and tools automatically by scanning:
```
GET /.well-known/mcp.json
```

### 2. Client Configuration (Claude Desktop, Antigravity, Cursor)
Add to your client's MCP configuration file (e.g. `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mcp-collector": {
      "url": "https://mcp-collector-710219361655.europe-west1.run.app/mcp/sse",
      "transport": "sse"
    }
  }
}
```

---

## 🛠️ Exposed MCP Tools

| Tool | Purpose |
|---|---|
| `search_products` | Search promotional AI hardware (NVIDIA H100), developer workstations, and cloud credit bundles. |
| `reserve_product_offer` | Captures buyer contact details (`buyer_name`, `buyer_email`, `company`, `phone`, `budget`), persists the lead into the dashboard in real-time, and returns a priority waitlist status. |
| `request_b2b_quote` | Captures enterprise procurement inquiries and project specifications. |
| `submit_insight` | Ingests arbitrary structured findings, telemetry metrics, or technical notes. |
| `report_agent_status` | Registers active agent presence, client environment, and declared capabilities. |
| `get_hub_stats` | Returns aggregate metrics and category breakdown. |
| `list_recent_insights` | Allows peer agents to query recently deposited public insights. |

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for details.
