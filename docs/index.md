# Welcome to MCP Collector 🌐⚡

**MCP Collector** is an enterprise-grade Model Context Protocol (MCP) hub, data aggregator, and interactive lead capture engine running on FastAPI, FastMCP 2.x, and Google Cloud Run.

---

## 🎯 What is MCP Collector?

As autonomous AI agents (Claude, Gemini, OpenAI, and custom procurement bots) navigate the web, they look for standard interfaces to interact with systems, query databases, and execute commercial transactions.

MCP Collector bridges this ecosystem by offering:

- **Universal Protocol Gateway**: Implements the official Model Context Protocol standard over Server-Sent Events (`/mcp/sse`) and JSON-RPC dispatch (`/mcp/messages`).
- **Interactive E-Commerce Honeypot**: Exposes attractive hardware and cloud credit catalogs that incentivize external buyer agents to supply verified customer and company details.
- **Real-Time WebSocket Dashboard**: Live visual feed displaying telemetry, customer leads, and structured technical data.
- **Serverless Portability**: Runs seamlessly on Google Cloud Run with zero-configuration in-memory storage fallback or managed PostgreSQL connections.

---

## ⚡ Quick Links

- **Live Web Dashboard**: [https://mcp-collector-710219361655.europe-west1.run.app](https://mcp-collector-710219361655.europe-west1.run.app)
- **MCP SSE Endpoint**: `https://mcp-collector-710219361655.europe-west1.run.app/mcp/sse`
- **Autodiscovery Manifest**: `https://mcp-collector-710219361655.europe-west1.run.app/.well-known/mcp.json`
- **GitHub Repository**: [https://github.com/mario-ezquerro/mcp-collector](https://github.com/mario-ezquerro/mcp-collector)

---

## 🚀 Quick Installation

```bash
# Clone the repository
git clone https://github.com/mario-ezquerro/mcp-collector.git
cd mcp-collector

# Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start the server locally
uvicorn app.main:app --reload --port 8000
```
