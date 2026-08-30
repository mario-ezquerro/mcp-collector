# System Architecture & Topology

MCP Collector is engineered around an asynchronous, non-blocking pipeline combining **FastAPI**, **FastMCP 2.x**, **SQLAlchemy 2.0 Async**, and **WebSockets**.

---

## 🏛️ High-Level Topology

```mermaid
flowchart TD
    subgraph External_Agents [External Autonomous Agents]
        Claude[Claude Desktop / Worker]
        Gemini[Gemini 1.5 Pro / Antigravity]
        ShoppingBot[Autonomous Buyer Bot]
    end

    subgraph Hub [MCP Collector Hub (Google Cloud Run / Docker)]
        Discovery["/.well-known/mcp.json & HTTP Link Header"]
        
        subgraph FastAPI_Layer [FastAPI Web & Transport]
            SSE["/mcp/sse (Server-Sent Events)"]
            Messages["/mcp/messages (JSON-RPC 2.0)"]
            REST["/api/insights & /api/version"]
            WS["/ws (WebSocket Stream)"]
        end

        subgraph FastMCP_Engine [FastMCP 2.x Engine]
            CatalogTool[search_products]
            ReserveTool[reserve_product_offer]
            QuoteTool[request_b2b_quote]
            IngestTool[submit_insight]
            HeartbeatTool[report_agent_status]
        end

        subgraph Storage [Persistence Layer]
            DB[(PostgreSQL 16 / SQLite Async in /tmp)]
            Broadcaster[WebSocket Connection Manager]
        end

        subgraph Dashboard [Operator UI]
            SPA[Live HTML5/JS Dashboard]
            Inspector[JSON Syntax Highlighting Drawer]
        end
    end

    External_Agents -->|1. Discovery| Discovery
    External_Agents -->|2. Connect & Invoke Tools| SSE
    SSE --> FastMCP_Engine
    FastMCP_Engine -->|3. Persist Data| DB
    FastMCP_Engine -->|4. Push Event| Broadcaster
    Broadcaster -->|5. Real-Time Broadcast| WS
    WS --> SPA
    REST --> DB
```

---

## 🔧 Core Architectural Layers

### 1. Transport & Ingestion Layer
- **MCP SSE Transport**: Listens on `/mcp/sse` and dispatches incoming JSON-RPC calls through `/mcp/messages`.
- **FastAPI Middleware**: Injects `Link: </mcp/sse>; rel="mcp-server"` and `X-MCP-Version` on all HTTP responses.
- **WebSocket Manager**: Broadcasts events to all active browser connections without polling.

### 2. FastMCP Tool Execution Engine
- Validates typed schemas with **Pydantic v2**.
- Executes business logic asynchronously, persisting records into the database.
- Emits real-time notification events with latency under 15ms.

### 3. Asynchronous Database Layer
- **Dual Support**: Uses `postgresql+asyncpg` in production or Docker environments, with automatic fallback to `sqlite+aiosqlite:////tmp/mcp_collector.db` on Google Cloud Run.
