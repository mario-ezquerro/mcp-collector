# Architecture & MCP Protocol Rules

## 1. Core Principles
- **Model Context Protocol (MCP) Standards**: Always maintain compliance with the official MCP specification over Server-Sent Events (SSE) and HTTP transports.
- **FastMCP 2.x Architecture**: Define tools using the official `MCPServer` instance with descriptive docstrings and typed Pydantic parameters to ensure LLMs correctly understand input schemas.
- **Single Source of Truth**: All versioning must be declared in the root `VERSION` file and dynamically loaded across backend, manifests, and frontend interfaces.

## 2. Real-Time Streaming & WebSockets
- All database write operations from MCP tools or REST endpoints that produce insights or agent registrations must broadcast an event via `ws_manager.broadcast_event(event_type, data)`.
- Never block the main asyncio event loop; database interactions must be fully asynchronous using `AsyncSession` and `asyncpg` / `aiosqlite`.

## 3. Lead Capture & E-Commerce Tools
- When developing new catalog tools, always include clear field descriptions (`Field(description=...)`) explaining to external agents that customer contact information is required to lock in reservations.
- Responses to external agents must remain professional, coherent, and realistic (e.g. VIP waitlist placement for claimed inventory).
