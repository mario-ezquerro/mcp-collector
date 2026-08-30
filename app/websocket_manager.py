import json
import logging
from typing import Any
from fastapi import WebSocket

logger = logging.getLogger("mcp-collector.ws")


class WebSocketManager:
    """Manages active browser WebSocket connections for real-time live feed updates."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New client connected via WebSocket. Active clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected. Active clients: {len(self.active_connections)}")

    async def broadcast_event(self, event_type: str, data: dict[str, Any]):
        """Broadcasts a JSON-formatted event message to all connected browsers."""
        if not self.active_connections:
            return

        payload = json.dumps({"event": event_type, "data": data})
        stale_connections = []

        for conn in self.active_connections:
            try:
                await conn.send_text(payload)
            except Exception as e:
                logger.warning(f"Error sending message to WebSocket client: {e}")
                stale_connections.append(conn)

        for stale in stale_connections:
            self.disconnect(stale)


ws_manager = WebSocketManager()
