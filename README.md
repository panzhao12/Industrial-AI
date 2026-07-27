# Industrial AI Troubleshooting Copilot

A portfolio-ready full-stack development project for industrial equipment diagnostics.

Current status: the application foundation and a local RAG MVP are implemented. The API can load synthetic Markdown and JSON knowledge, create chunks and embeddings, search an in-memory vector index, and run retrieval evaluation cases. Diagnosis generation, durable PostgreSQL/pgvector persistence, hybrid search, tool calling, and human-in-the-loop workflows remain placeholders or future work.

## Stack

- Frontend: Vue 3, TypeScript, Vite, Pinia
- Backend: Python, FastAPI, Pydantic
- Retrieval: heading-aware chunking, configurable fake or local embeddings, cosine-similarity search
- Runtime vector store: in-memory and non-persistent
- Database scaffold: PostgreSQL with the `pgvector` extension
- Realtime: Server-Sent Events placeholder
- Infra: Docker Compose

## Repository Layout

```text
apps/
  api/        FastAPI service, local RAG runtime, typed schemas, and mock diagnosis data
  web/        Vue 3 + Vite frontend
docs/
  AGENTS.md
  ARCHITECTURE.md
infra/
  postgres/   pgvector and RAG schema bootstrap scripts
data/
  synthetic/  structured hydraulic equipment fixtures and evaluation cases
```

## Quick Start

Run the API:

```bash
cd apps/api
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS or Linux
source .venv/bin/activate

pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The default `RAG_EMBEDDING_PROVIDER=fake` setting requires no model download. It creates deterministic development vectors, not semantic embeddings.

To use the implemented local sentence-transformer provider:

1. Copy `apps/api/.env.example` to `apps/api/.env`.
2. Set `RAG_EMBEDDING_PROVIDER=local`.
3. Install the optional runtime package with `pip install sentence-transformers`.

The default local model is `intfloat/multilingual-e5-small`. It is downloaded by `sentence-transformers` when first loaded and can be changed with `LOCAL_EMBEDDING_MODEL`.

Populate the process-local RAG index after starting the API:

```bash
curl -X POST http://localhost:8000/rag/ingest-local-knowledge-base
```

This loads the synthetic Markdown manuals plus JSON-backed machines, telemetry, error codes, manual metadata, and repair cases. To load only Markdown manuals, call `POST /rag/ingest-local-manuals` instead.

Search the populated index:

```bash
curl -X POST http://localhost:8000/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query":"pressure oscillation under load","top_k":5}'
```

The index is stored in application memory. It starts empty and is lost whenever the API process restarts.

Run the web app:

```bash
cd apps/web
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000`. Override it with `VITE_API_BASE_URL` if needed.

The current API does not require PostgreSQL to serve synthetic data or run the local RAG MVP. Start the PostgreSQL/pgvector scaffold when developing persistence:

```bash
docker compose up -d postgres
```

Run the backend tests:

```bash
cd apps/api
pytest
```

Run the frontend type-check and production build:

```bash
cd apps/web
npm run build
```

## API Surface

Application and synthetic data:

- `GET /health`
- `GET /machines`
- `GET /machines/{machine_id}`
- `GET /machines/{machine_id}/telemetry/current`
- `GET /incidents`
- `GET /incidents/{incident_id}`
- `POST /incidents/{incident_id}/analyze` — placeholder diagnosis response
- `GET /documents`
- `GET /documents/{document_id}`
- `GET /documents/{document_id}/chunks` — placeholder chunk previews
- `POST /documents/ingest` — accepts the request but does not persist or index it

Local RAG runtime:

- `GET /rag/status`
- `POST /rag/clear`
- `POST /rag/ingest-local-manuals`
- `POST /rag/ingest-local-knowledge-base`
- `POST /rag/search`
- `POST /rag/evaluate` — evaluates the populated index against RAG cases

Future workflow scaffolding:

- `GET /events/diagnosis/{incident_id}` — placeholder SSE stream
- `GET /agent/traces/{trace_id}` — mock trace
- `GET /evaluation/cases` — static diagnosis evaluation fixtures

## Synthetic Data

JSON-backed synthetic industrial data lives under `data/synthetic/`:

- `machines/`: five hydraulic assets.
- `telemetry/`: five current telemetry scenarios, one for each machine.
- `error_codes/`: 20 hydraulic fault codes.
- `manuals/`: five manual metadata records and a Markdown troubleshooting manual.
- `repair_cases/`: 30 repair cases exposed as incidents.
- `evaluation/evaluation_cases.json`: 10 static diagnosis evaluation cases.
- `evaluation/rag_eval_cases.json`: five executable RAG retrieval evaluation cases.

Application routes load the typed operational fixtures through `apps/api/app/data/synthetic_loader.py`. The local RAG knowledge-base ingestion route additionally converts supported JSON records into `LoadedDocument` instances through `apps/api/app/rag/json_knowledge_loader.py`.

## Current RAG Implementation

The active local pipeline is:

1. Load Markdown manuals and supported synthetic JSON records.
2. Convert sources into normalized `LoadedDocument` objects.
3. Split content by Markdown headings and character limits.
4. Generate embeddings with either:
   - `FakeEmbeddingProvider`, the deterministic default used for plumbing and tests; or
   - `LocalSentenceTransformerEmbeddingProvider`, an optional semantic provider.
5. Store embedded chunks in `InMemoryVectorStore`.
6. Embed queries and rank chunks by cosine similarity through `VectorRagRetriever`.
7. Return scored, non-placeholder results from `POST /rag/search`.
8. Evaluate retrieval results through `POST /rag/evaluate`.

The SQL bootstrap scripts separately create `documents`, `document_chunks`, and `document_ingestion_runs` tables, including a pgvector-ready `embedding vector(1536)` column. The active RAG runtime does not read or write those tables yet.

The `/documents` endpoints and the local `/rag` runtime are currently separate. `POST /documents/ingest` and `GET /documents/{document_id}/chunks` still expose placeholder behavior; use the `/rag/ingest-local-*` routes to populate the working in-memory index.

## Intentionally Not Implemented

The following are intentionally not implemented yet:

- LLM-based diagnosis or generation
- LangGraph workflows
- OpenAI, Anthropic, Claude, or other model provider integrations
- PostgreSQL/pgvector-backed RAG persistence
- Lexical search, hybrid search, and reranking
- General document upload, parsing, and durable ingestion
- Integration between retrieved evidence and incident diagnosis
- Tool execution against plant systems
- Durable database repositories and application migrations
- Production authentication, authorization, and audit logging

The `/incidents/{incident_id}/analyze` endpoint returns a typed placeholder `Diagnosis` response only. The `/agent/traces/{trace_id}` endpoint returns mock trace steps only. Diagnosis evaluation cases remain static fixtures and do not score model behavior; RAG evaluation is implemented separately for retrieval results.

## Planned Next Steps

1. Replace the in-memory vector store with PostgreSQL/pgvector persistence and migrations.
2. Connect the `/documents` ingestion API and UI to the working RAG pipeline.
3. Add lexical retrieval, hybrid fusion, reranking, and stronger RAG regression coverage.
4. Package and document optional local-model dependencies for reproducible installs.
5. Implement a diagnosis graph behind the reserved `apps/api/app/agent/` interfaces.
6. Pass retrieved evidence into diagnosis with traceable citations.
7. Add safe tool adapters, human review states, approvals, and audit logs.
