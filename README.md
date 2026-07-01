# Industrial AI Troubleshooting Copilot

A portfolio-ready full-stack skeleton for industrial equipment diagnostics.

Current status: non-AI skeleton only. The app includes typed API contracts, Vue pages, mock operational data, PostgreSQL with `pgvector`, and reserved extension points for future manual RAG, LangGraph, tool calling, and human-in-the-loop workflows.

## Stack

- Frontend: Vue 3, TypeScript, Vite, Pinia
- Backend: Python, FastAPI, Pydantic
- Database: PostgreSQL with the `pgvector` extension
- Realtime: Server-Sent Events placeholder
- Infra: Docker Compose

## Repository Layout

```text
apps/
  api/        FastAPI service, typed schemas, mock data, and placeholders
  web/        Vue 3 + Vite frontend
docs/
  AGENTS.md
  ARCHITECTURE.md
infra/
  postgres/  database bootstrap scripts
data/
  synthetic/ structured hydraulic equipment fixtures
```

## Quick Start

Start PostgreSQL with pgvector:

```bash
docker compose up -d postgres
```

Run the API:

```bash
cd apps/api
python -m venv .venv
.venv/Scripts/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Run the web app:

```bash
cd apps/web
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000`. Override it with `VITE_API_BASE_URL` if needed.

Run backend smoke tests:

```bash
cd apps/api
pytest
```

## API Surface

- `GET /health`
- `GET /machines`
- `GET /machines/{machine_id}`
- `GET /machines/{machine_id}/telemetry/current`
- `GET /incidents`
- `GET /incidents/{incident_id}`
- `POST /incidents/{incident_id}/analyze`
- `GET /documents`
- `GET /documents/{document_id}`
- `GET /documents/{document_id}/chunks`
- `POST /documents/ingest`
- `POST /rag/search`
- `GET /events/diagnosis/{incident_id}`
- `GET /agent/traces/{trace_id}`
- `GET /evaluation/cases`

## Synthetic Data

Day 2 adds JSON-backed synthetic industrial data under `data/synthetic/`:

- `machines/`: five hydraulic assets.
- `telemetry/`: current telemetry scenarios for each machine.
- `error_codes/`: hydraulic fault code catalog.
- `manuals/`: maintenance manual metadata and sections.
- `repair_cases/`: 30 repair cases exposed as incidents.
- `evaluation/`: 10 evaluation cases for future diagnosis scoring.

The API loads these files through `apps/api/app/data/synthetic_loader.py`; route handlers do not hardcode synthetic records.

## RAG Scaffolding

Day 3 adds RAG infrastructure scaffolding only:

- PostgreSQL tables for `documents`, `document_chunks`, and `document_ingestion_runs`.
- A pgvector-ready `embedding vector(1536)` placeholder column.
- Placeholder service contracts under `apps/api/app/rag/`.
- Document detail and placeholder chunk-preview endpoints.
- A placeholder `/rag/search` endpoint for frontend integration.
- Document Library UI panels for ingestion status, document detail, chunk previews, search, and search results.

Planned ingestion flow:

1. Load source documents.
2. Parse document text and metadata.
3. Chunk content by section and token budget.
4. Generate embeddings.
5. Store documents, chunks, and vectors in PostgreSQL/pgvector.
6. Retrieve with vector and hybrid search.
7. Pass retrieved evidence to a future diagnosis workflow.

Only the contracts and UI are present today. The actual chunking, embeddings, vector search, hybrid search, and diagnosis integration still require manual implementation.

## Intentionally Not Implemented

The following are intentionally not implemented yet:

- Real AI or LLM calls
- RAG retrieval
- LangGraph workflows
- OpenAI, Anthropic, Claude, or other model provider integrations
- Embedding generation
- Vector search and hybrid search
- Tool execution against plant systems
- Durable database repositories and application migrations
- Production authentication, authorization, and audit logging

The `/incidents/{incident_id}/analyze` endpoint returns a typed placeholder `Diagnosis` response only. The `/rag/search` endpoint returns placeholder chunk previews only. The `/agent/traces/{trace_id}` endpoint returns mock trace steps only. Evaluation cases are static fixtures and do not score model behavior yet.

## Planned Next Steps

1. Add synthetic telemetry and incident datasets.
2. Add database repositories and a real migration workflow.
3. Implement document loading, parsing, chunking, and embedding storage.
4. Implement RAG retrieval manually behind the reserved `apps/api/app/rag/` interfaces.
5. Implement a diagnosis graph manually behind the reserved `apps/api/app/agent/` interfaces.
6. Add evaluation cases and regression scoring.
7. Add human review states, approvals, and audit logs.
