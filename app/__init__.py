"""MCP Collector - Real-time MCP Hub, Data Aggregator & AI Agent Marketplace."""
import os

version_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "VERSION")
if os.path.exists(version_file):
    with open(version_file, "r", encoding="utf-8") as f:
        __version__ = f.read().strip()
else:
    __version__ = "1.1.0"
