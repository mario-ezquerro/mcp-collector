# Google Cloud Run Deployment

MCP Collector is designed for serverless execution on **Google Cloud Run**.

---

## ☁️ Prerequisites & Deployment

### 1. Automated Deployment Script
```bash
./scripts/deploy_cloud_run.sh
```

### 2. Manual CLI Deployment
```bash
gcloud run deploy mcp-collector \
    --source . \
    --project mcp-collector \
    --region europe-west1 \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --timeout 3600 \
    --min-instances 1 \
    --session-affinity \
    --set-env-vars "HOST=0.0.0.0"
```

---

## ⚙️ Key Configuration Details

1. **Port Binding**: Respects Cloud Run's dynamic `$PORT` variable (defaults to `8080`).
2. **Persistence Strategy**: Automatically detects `K_SERVICE`. When running in standalone Cloud Run mode without an external PostgreSQL instance, SQLite is directed to `/tmp/mcp_collector.db` (in-memory writable RAM disk).
3. **Session Affinity & Streaming**: `--session-affinity` ensures WebSocket connections and SSE sessions remain sticky across autoscaled instances.
4. **Timeout Extension**: Set to `3600s` (60 minutes) to prevent premature disconnections of real-time operator feeds.
