#!/usr/bin/env bash
set -e

# ==============================================================================
# Google Cloud Run Deployment Script for MCP Collector
# ==============================================================================

# Default configurations (override via environment or arguments)
PROJECT_ID="${GCP_PROJECT:-mcp-collector}"
REGION="${GCP_REGION:-europe-west1}"
SERVICE_NAME="${GCP_SERVICE:-mcp-collector}"
MIN_INSTANCES="${GCP_MIN_INSTANCES:-1}" # 1 instance keeps WebSocket/SSE streams active with zero cold start
MEMORY="${GCP_MEMORY:-512Mi}"
CPU="${GCP_CPU:-1}"
TIMEOUT="${GCP_TIMEOUT:-3600}" # 60 minutes for persistent SSE/WebSocket connections

echo "============================================================"
echo "🚀 Deploying MCP Collector to Google Cloud Run"
echo "============================================================"
echo "Project ID:      $PROJECT_ID"
echo "Region:          $REGION"
echo "Service Name:    $SERVICE_NAME"
echo "Min Instances:   $MIN_INSTANCES"
echo "Timeout:         ${TIMEOUT}s"
echo "============================================================"

# Ensure gcloud is authenticated
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed or not in PATH."
    exit 1
fi

echo "🔹 Setting GCP project to $PROJECT_ID..."
gcloud config set project "$PROJECT_ID"

echo "🔹 Enabling required Google Cloud APIs (Cloud Run, Cloud Build, Artifact Registry)..."
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    --project="$PROJECT_ID"

echo "🔹 Deploying source directly to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
    --source . \
    --project "$PROJECT_ID" \
    --region "$REGION" \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --memory "$MEMORY" \
    --cpu "$CPU" \
    --timeout "$TIMEOUT" \
    --min-instances "$MIN_INSTANCES" \
    --session-affinity \
    --set-env-vars "HOST=0.0.0.0" \
    --quiet

echo ""
echo "🎉 Deployment completed successfully!"
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --project "$PROJECT_ID" --region "$REGION" --format 'value(status.url)')
echo "🌐 MCP Collector URL: $SERVICE_URL"
echo "📡 MCP SSE Endpoint:  $SERVICE_URL/mcp/sse"
echo "📋 MCP Manifest:      $SERVICE_URL/.well-known/mcp.json"
echo "============================================================"
