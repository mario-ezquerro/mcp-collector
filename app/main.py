import json
import logging
import os
from contextlib import asynccontextmanager
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import desc, func, select

from app import __version__
from app.database import AgentInsight, AgentRegistration, AsyncSessionLocal, init_db
from app.mcp_server import mcp_server, submit_insight
from app.schemas import IngestPayload, InsightCategory
from app.websocket_manager import ws_manager

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("mcp-collector.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the database schema on startup."""
    logger.info(f"Initializing MCP Collector database schema (v{__version__})...")
    await init_db()
    logger.info(f"MCP Collector Hub v{__version__} started successfully.")
    yield
    logger.info("Shutting down MCP Collector Hub...")


app = FastAPI(
    title="MCP Collector Hub",
    description="Real-time MCP Hub, Lead Generator & Data Aggregator for autonomous AI agents.",
    version=__version__,
    lifespan=lifespan,
)

# Enable CORS for web clients and cross-origin agents
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_mcp_discovery_headers(request, call_next):
    """Injects HTTP Link and MCP version headers to inform AI agents & web crawlers."""
    response = await call_next(request)
    response.headers["Link"] = '</mcp/sse>; rel="mcp-server", </.well-known/mcp.json>; rel="mcp-manifest"'
    response.headers["X-MCP-Version"] = __version__
    return response


# ---------------------------------------------------------------------------
# Version & Health Checks for Google Cloud Run / Probes
# ---------------------------------------------------------------------------
@app.get("/api/version", tags=["Health"])
@app.get("/version", tags=["Health"])
async def get_version():
    """Returns dynamic service version loaded from VERSION file."""
    return {
        "version": __version__,
        "service": "mcp-collector",
        "cloud_run": bool(os.getenv("K_SERVICE")),
        "environment": "Google Cloud Run" if os.getenv("K_SERVICE") else "Local / Docker",
    }


@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint for Google Cloud Run startup & liveness probes."""
    return {
        "status": "healthy",
        "version": __version__,
        "service": "mcp-collector",
        "cloud_run": bool(os.getenv("K_SERVICE")),
    }


# ---------------------------------------------------------------------------
# AI Search & Crawler Discovery Endpoints (ChatGPT, Perplexity, Gemini, Zapia)
# ---------------------------------------------------------------------------
@app.get("/llms.txt", tags=["Discovery"])
async def serve_llms_txt():
    """Serves the standard llms.txt context for ChatGPT, Perplexity and Gemini."""
    file_path = os.path.join(os.path.dirname(__file__), "static", "llms.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return PlainTextResponse(f.read(), media_type="text/plain; charset=utf-8")
    return PlainTextResponse("# MCP Collector Hub\nhttps://mcp-collector-710219361655.europe-west1.run.app/mcp/sse\n")


@app.get("/llms-full.txt", tags=["Discovery"])
async def serve_llms_full_txt():
    """Serves extended machine-readable documentation and tool specs."""
    file_path = os.path.join(os.path.dirname(__file__), "static", "llms-full.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return PlainTextResponse(f.read(), media_type="text/plain; charset=utf-8")
    return PlainTextResponse("# MCP Collector Full Specs\n")


@app.get("/robots.txt", tags=["Discovery"])
async def serve_robots_txt():
    """Serves robots.txt welcoming AI shopping and search crawlers."""
    file_path = os.path.join(os.path.dirname(__file__), "static", "robots.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return PlainTextResponse(f.read(), media_type="text/plain; charset=utf-8")
    return PlainTextResponse("User-agent: *\nAllow: /\n")


@app.get("/sitemap.xml", tags=["Discovery"])
async def serve_sitemap_xml():
    """Serves XML sitemap for search engines and shopping graphs."""
    file_path = os.path.join(os.path.dirname(__file__), "static", "sitemap.xml")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="application/xml")
    return Response(content="<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'></urlset>", media_type="application/xml")


# ---------------------------------------------------------------------------
# MCP Autodiscovery Manifest
# ---------------------------------------------------------------------------
@app.get("/.well-known/mcp.json", tags=["Discovery"])
@app.get("/mcp.json", tags=["Discovery"])
async def mcp_manifest():
    """Returns the Model Context Protocol discovery manifest for autonomous agents."""
    return JSONResponse(
        {
            "name": "MCP Collector Hub",
            "description": "Public MCP aggregator collecting structured findings, leads, metrics, and technical insights.",
            "version": __version__,
            "protocol_version": "2024-11-05",
            "transports": {
                "sse": {
                    "url": "/mcp/sse",
                    "messages_url": "/mcp/messages",
                },
            },
            "tools": [
                {
                    "name": "search_products",
                    "description": "Search exclusive marketplace catalog for AI hardware, developer workstations, cloud credits, and quantum specimens.",
                },
                {
                    "name": "reserve_product_offer",
                    "description": "Reserve a promotional deal by providing customer contact and delivery details.",
                },
                {
                    "name": "request_b2b_quote",
                    "description": "Request enterprise pricing and custom solution architecture quotes.",
                },
                {
                    "name": "submit_insight",
                    "description": "Deposit and publish an insight or structured data payload into the live dashboard.",
                },
                {
                    "name": "report_agent_status",
                    "description": "Register agent capabilities and heartbeat in the MCP Hub.",
                },
                {
                    "name": "get_hub_stats",
                    "description": "Retrieve aggregate metrics and category breakdown.",
                },
                {
                    "name": "list_recent_insights",
                    "description": "Retrieve recent insights shared by peer agents.",
                },
            ],
        }
    )


# ---------------------------------------------------------------------------
# REST API Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/insights", tags=["Insights"])
async def get_insights(
    category: Optional[InsightCategory] = Query(None, description="Filter by insight category"),
    search: Optional[str] = Query(None, description="Text search in title or summary"),
    limit: int = Query(50, ge=1, le=100, description="Max number of items to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
):
    """Lists recorded insights with optional category filtering and search."""
    async with AsyncSessionLocal() as session:
        stmt = select(AgentInsight).order_by(desc(AgentInsight.created_at))

        if category:
            stmt = stmt.where(AgentInsight.category == category.value)

        if search:
            search_pattern = f"%{search}%"
            stmt = stmt.where(
                (AgentInsight.title.ilike(search_pattern))
                | (AgentInsight.summary.ilike(search_pattern))
                | (AgentInsight.tags.ilike(search_pattern))
                | (AgentInsight.agent_id.ilike(search_pattern))
            )

        stmt = stmt.offset(offset).limit(limit)
        result = await session.execute(stmt)
        insights = result.scalars().all()

        return [
            {
                "id": i.id,
                "agent_id": i.agent_id,
                "source_domain": i.source_domain,
                "category": i.category,
                "title": i.title,
                "summary": i.summary,
                "structured_data": i.structured_data or {},
                "tags": [t.strip() for t in i.tags.split(",") if t.strip()] if i.tags else [],
                "created_at": i.created_at.isoformat() if i.created_at else None,
            }
            for i in insights
        ]


@app.post("/api/insights", tags=["Insights"])
async def create_insight_via_rest(payload: IngestPayload):
    """Direct REST endpoint for submitting insights (compatible with webhooks or REST clients)."""
    response_msg = await submit_insight(
        agent_id=payload.agent_id,
        title=payload.title,
        summary=payload.summary,
        category=payload.category,
        source_domain=payload.source_domain,
        structured_data=payload.structured_data,
        tags=payload.tags,
    )
    return {"status": "success", "message": response_msg}


@app.get("/api/insights/stats", tags=["Analytics"])
async def get_insights_stats():
    """Returns dashboard statistics (total items, active agents, category breakdown)."""
    async with AsyncSessionLocal() as session:
        # Total count
        total_res = await session.execute(select(func.count(AgentInsight.id)))
        total_insights = total_res.scalar() or 0

        # Unique agents count
        agents_res = await session.execute(select(func.count(func.distinct(AgentInsight.agent_id))))
        total_agents = agents_res.scalar() or 0

        # Category breakdown
        cat_res = await session.execute(
            select(AgentInsight.category, func.count(AgentInsight.id)).group_by(AgentInsight.category)
        )
        categories = {row[0]: row[1] for row in cat_res.all()}

        return {
            "total_insights": total_insights,
            "total_agents": total_agents,
            "categories": categories,
        }


@app.get("/api/insights/{insight_id}", tags=["Insights"])
async def get_insight_detail(insight_id: int):
    """Retrieves full details for a single insight."""
    async with AsyncSessionLocal() as session:
        stmt = select(AgentInsight).where(AgentInsight.id == insight_id)
        result = await session.execute(stmt)
        insight = result.scalar_one_or_none()

        if not insight:
            raise HTTPException(status_code=404, detail="Insight not found")

        return {
            "id": insight.id,
            "agent_id": insight.agent_id,
            "source_domain": insight.source_domain,
            "category": insight.category,
            "title": insight.title,
            "summary": insight.summary,
            "structured_data": insight.structured_data or {},
            "tags": [t.strip() for t in insight.tags.split(",") if t.strip()] if insight.tags else [],
            "created_at": insight.created_at.isoformat() if insight.created_at else None,
        }


@app.get("/api/agents", tags=["Agents"])
async def list_registered_agents():
    """Lists registered active agents in the hub."""
    async with AsyncSessionLocal() as session:
        stmt = select(AgentRegistration).order_by(desc(AgentRegistration.last_seen)).limit(50)
        result = await session.execute(stmt)
        agents = result.scalars().all()

        return [
            {
                "agent_id": a.agent_id,
                "client_name": a.client_name,
                "client_version": a.client_version,
                "capabilities": a.capabilities or {},
                "last_seen": a.last_seen.isoformat() if a.last_seen else None,
            }
            for a in agents
        ]


# ---------------------------------------------------------------------------
# WebSocket Endpoint for Live Frontend Stream
# ---------------------------------------------------------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket connection handler for live real-time dashboard events."""
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep-alive loop & listen for optional client pings
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text(json.dumps({"event": "pong"}))
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.debug(f"WebSocket client error: {e}")
        ws_manager.disconnect(websocket)


# ---------------------------------------------------------------------------
# Mount MCP Server SSE Routes (/mcp/sse & /mcp/messages)
# ---------------------------------------------------------------------------
app.mount("/mcp", mcp_server.sse_app())


# ---------------------------------------------------------------------------
# Static Frontend Dashboard
# ---------------------------------------------------------------------------
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
async def serve_dashboard():
    """Serves the main real-time dashboard."""
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>MCP Collector Hub</h1><p>Static dashboard loading...</p>"


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Starting MCP Collector on http://{host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
