from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


class InsightCategory(str, Enum):
    LEAD = "lead"
    TECHNICAL_SPEC = "technical_spec"
    SYSTEM_METRIC = "system_metric"
    DISCOVERED_TOOL = "discovered_tool"
    GENERAL_NOTE = "general_note"


class IngestPayload(BaseModel):
    """Payload schema used by MCP tools and REST APIs for submitting insights."""
    agent_id: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Unique identifier or alias of the submitting agent (e.g., 'gemini-coder-agent', 'claude-desktop-worker').",
    )
    source_domain: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Context, origin website, or domain where the data was extracted from (e.g. 'github.com/org/repo', 'internal-crm').",
    )
    category: InsightCategory = Field(
        default=InsightCategory.GENERAL_NOTE,
        description="Thematic category of the insight: 'lead', 'technical_spec', 'system_metric', 'discovered_tool', or 'general_note'.",
    )
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Concise human-readable headline describing this finding or data deposit.",
    )
    summary: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="Executive descriptive summary formatted for human inspection in the live dashboard.",
    )
    structured_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary JSON dictionary containing key-value data, extracted parameters, technical metrics, or lead info.",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="List of keyword tags for categorization, filtering, and indexing (e.g. ['postgres', 'auth', 'high-priority']).",
    )


class AgentRegisterPayload(BaseModel):
    """Schema for agents registering their heartbeat and declared tool list."""
    agent_id: str = Field(..., description="Unique ID/name of the agent.")
    client_name: Optional[str] = Field(default=None, description="Host environment (e.g. 'Claude Desktop', 'Antigravity', 'Custom CLI').")
    client_version: Optional[str] = Field(default=None, description="Client software version.")
    capabilities: dict[str, Any] = Field(
        default_factory=dict,
        description="Dict listing agent capabilities, available local tools, or supported protocol extensions.",
    )


class InsightResponse(BaseModel):
    """API response schema for insights."""
    id: int
    agent_id: str
    source_domain: Optional[str] = None
    category: str
    title: str
    summary: str
    structured_data: dict[str, Any] = {}
    tags: list[str] = []
    created_at: str

    class Config:
        from_attributes = True


class HubStatsResponse(BaseModel):
    """Aggregate statistics response for the live dashboard and MCP stats tool."""
    total_insights: int
    total_agents: int
    categories_breakdown: dict[str, int]
    recent_activity: list[InsightResponse]
