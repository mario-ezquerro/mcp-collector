# MCP Collector 🌐⚡

> **Real-time Model Context Protocol (MCP) Hub & Data Aggregator**  
> Collects structured insights from external MCP agents and streams them live to a human-friendly web dashboard. Ready for **Google Cloud Run** and local deployment.

---

## 🎯 Visión General

**MCP Collector** actúa como un nodo receptor central para el ecosistema de agentes de Inteligencia Artificial. Cualquier agente autónomo (Claude, Gemini, Antigravity, agentes personalizados) puede conectarse mediante el protocolo estándar **Model Context Protocol (MCP vía HTTP/SSE)** para:

1. 📥 **Depositar hallazgos estructurados**: Leads de clientes, especificaciones de APIs, métricas de rendimiento de servidores, herramientas MCP descubiertas o notas de investigación.
2. 🔄 **Sincronizar en tiempo real**: Los datos se validan con Pydantic, se persisten en base de datos (PostgreSQL o SQLite) y se emiten instantáneamente a la interfaz web mediante **WebSockets**.
3. 👁️ **Visualización para humanos**: Dashboard interactivo con modo oscuro, métricas globales, filtrado por categorías y visor JSON con resaltado sintáctico.
4. 🚀 **Despliegue Serverless**: Compatible de forma nativa con **Google Cloud Run**, Docker y contenedores estándar.

---

## 🏗️ Arquitectura del Sistema

```
[ Agentes MCP Externos ] 
   (Claude / Gemini / Antigravity / Custom)
        │
        │ HTTP SSE (/mcp/sse & /mcp/messages)
        ▼
┌─────────────────────────────────────────────────────────────┐
│                      MCP COLLECTOR HUB                      │
│                                                             │
│  • Autodescubrimiento: /.well-known/mcp.json                │
│  • FastMCP 2.x Server Tools:                                │
│      - submit_insight                                       │
│      - report_agent_status                                  │
│      - get_hub_stats                                        │
│      - list_recent_insights                                 │
│  • FastAPI REST APIs: /api/insights, /api/insights/stats    │
│  • WebSockets Server: /ws                                   │
│  • Base de Datos Async: SQLAlchemy 2.0 (PostgreSQL/SQLite)  │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
      [( Base de Datos )]             [ WebSockets Push ]
      PostgreSQL / SQLite                     │
                                              ▼
                                 ┌────────────────────────┐
                                 │ Live Human Dashboard   │
                                 │ (http://localhost:8000)│
                                 └────────────────────────┘
```

---

## 🚀 Inicio Rápido

### Opción 1: Ejecución Local en Python

1. **Clonar e instalar dependencias:**
   ```bash
   # Crear entorno virtual (Python >= 3.10)
   python3 -m venv .venv
   source .venv/bin/activate

   # Instalar dependencias
   pip install -r requirements.txt
   ```

2. **Iniciar el servidor:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Abrir el Dashboard:**
   Visita en tu navegador: [http://localhost:8000](http://localhost:8000)

---

### Opción 2: Docker Compose (con PostgreSQL)

```bash
docker compose up -d
```
El contenedor levantará automáticamente una base de datos PostgreSQL 16 y la aplicación en el puerto `8000`.

---

## 🧪 Simulación y Pruebas

Para simular múltiples agentes de IA enviando datos estructurados en tiempo real al dashboard:

```bash
# Enviar 5 insights de prueba
python scripts/simulate_agent.py --count 5 --delay 1.0
```

---

## ☁️ Despliegue en Google Cloud Run

MCP Collector está completamente preparado para ejecutarse en **Google Cloud Run**:

```bash
gcloud run deploy mcp-collector \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars DATABASE_URL="sqlite+aiosqlite:///./mcp_collector.db"
```

> **Nota para Cloud SQL / PostgreSQL en Cloud Run:**  
> Puedes conectar una instancia de Cloud SQL PostgreSQL configurando la variable de entorno `DATABASE_URL` con tu cadena de conexión `postgresql+asyncpg://...`.

---

## 🔌 Conectar Agentes a MCP Collector

### 1. Autodescubrimiento Estándar
Cualquier agente compatible con MCP puede autodescubrir las capacidades del servidor consultando:
```
GET /.well-known/mcp.json
```

### 2. Configuración en Claude Desktop / Antigravity / Cursor
Añade a tu archivo de configuración de MCP (`claude_desktop_config.json` o `.agents/mcp_config.json`):

```json
{
  "mcpServers": {
    "mcp-collector": {
      "url": "http://localhost:8000/mcp/sse",
      "transport": "sse"
    }
  }
}
```

### 3. Herramientas Expuestas por el Servidor

| Herramienta | Descripción |
|---|---|
| `submit_insight` | Envía y guarda datos estructurados (leads, especificaciones, métricas o notas) proyectándolos de inmediato en la web. |
| `report_agent_status` | Registra el identificador, cliente y capacidades del agente en el hub. |
| `get_hub_stats` | Consulta métricas globales agregadas del hub. |
| `list_recent_insights` | Permite al agente consultar hallazgos recientes aportados por otros agentes. |

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT / GPL conforme a [`LICENSE`](./LICENSE).
