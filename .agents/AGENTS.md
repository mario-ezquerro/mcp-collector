# Workspace Rules for Antigravity & AI Agents

Welcome to **MCP Collector**. This repository contains a real-time Model Context Protocol (MCP) hub, data aggregator, and lead generation engine running on FastAPI, FastMCP 2.x, and Google Cloud Run.

## Quick Rules Summary
1. **Language**: All markdowns, code comments, commit messages, and UI text must be in English.
2. **Versioning**: The root `VERSION` file is the single source of truth for version numbering.
3. **Architecture**: Always follow the specifications defined in [`SPEC.md`](../SPEC.md).
4. **Cloud Run Ready**: Maintain Cloud Run portability (bind `$PORT`, use `/tmp` storage fallback, support WebSockets/SSE streaming).
5. **Git Workflow**: Always commit clean code and push to `origin main` after verifying changes.

Refer to the modular rules in `.agents/rules/` for detailed guidelines.
