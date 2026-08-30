# Google Cloud Run Deployment Rules

## 1. Cloud Run Environment Constraints
- **Port Binding**: Cloud Run automatically injects the `$PORT` environment variable (default `8080`). Never override or pass `PORT` via `--set-env-vars` in `gcloud run deploy`. The server must bind to `0.0.0.0:${PORT:-8080}`.
- **Stateless Filesystem**: When running on Cloud Run (`K_SERVICE` is set) without a PostgreSQL connection string, default SQLite database storage to `/tmp/mcp_collector.db` (in-memory writable RAM disk).

## 2. Streaming & Timeouts
- Set request timeout to `--timeout 3600` (60 minutes) to allow persistent SSE streams and WebSocket subscriptions without premature disconnects.
- Enable `--session-affinity` for multi-instance deployments.
- Set `--min-instances 1` to prevent cold start latency on real-time operator feeds.

## 3. Health Probes
- Ensure `/health` and `/api/health` return HTTP `200 OK` with service name, current version, and environment flag.
