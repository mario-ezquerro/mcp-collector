# REST & WebSocket API Reference

In addition to the MCP protocol, MCP Collector exposes standard RESTful endpoints and a WebSocket channel.

---

## 📡 Endpoints Specification

### Version & Health
- `GET /api/version` -> Returns dynamic version and runtime environment info.
- `GET /health` or `GET /api/health` -> Health check probe for Cloud Run and load balancers.

### Insights Management
- `GET /api/insights` -> Query recorded insights with pagination (`limit`, `offset`), category filter (`category`), and search (`search`).
- `POST /api/insights` -> Ingest insight via standard JSON REST payload (useful for webhooks).
- `GET /api/insights/stats` -> Returns global dashboard counts and category breakdown.
- `GET /api/insights/{id}` -> Returns full payload for a single insight.

### Agent Directory
- `GET /api/agents` -> Lists active registered agents and their declared capabilities.

### Real-Time WebSocket
- `ws://<host>/ws` or `wss://<host>/ws` -> Real-time bidirectional streaming channel for operator dashboards.
