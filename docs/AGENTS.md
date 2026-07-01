# Agent Contracts

This project intentionally does not implement AI logic yet. The current backend exposes typed boundaries so future RAG, LangGraph, tool calling, and human-in-the-loop diagnosis can be added without rewriting the HTTP API.

## Reserved Manual Implementation Areas

The following folders are reserved for future manual implementation and must not be modified unless explicitly requested:

- `apps/api/app/rag/`
- `apps/api/app/agent/`

Codex may create typed interfaces, placeholder classes, and TODO comments in these folders. Codex must not implement real AI, RAG, LangGraph, OpenAI, Claude, Anthropic, embedding, retrieval, prompt orchestration, or tool-calling logic there unless the user explicitly asks for that implementation.

The current placeholders should remain boring and safe: raise `NotImplementedError`, return disabled results, or expose empty typed contracts. Mock data belongs in `apps/api/app/data/mock_data.py`, not in the reserved implementation packages.

## RAG Retriever

Location: `apps/api/app/rag/retriever.py`

Purpose:

- Accept an incident or diagnostic query.
- Retrieve relevant chunks from manuals, maintenance logs, standard operating procedures, and past incidents.
- Return scored evidence with metadata and source references.

Current behavior:

- `PlaceholderRagRetriever` raises `NotImplementedError`.

## Embedding Service

Location: `apps/api/app/rag/embeddings.py`

Purpose:

- Convert document chunks and user/incident queries into vectors.
- Keep embedding vendor and model choice outside the route layer.

Current behavior:

- `PlaceholderEmbeddingProvider` raises `NotImplementedError`.

## Chunking and Hybrid Search

Locations:

- `apps/api/app/rag/document_loader.py`
- `apps/api/app/rag/chunker.py`
- `apps/api/app/rag/vector_store.py`
- `apps/api/app/rag/hybrid_search.py`

Purpose:

- Prepare future document chunking and combined lexical/vector search.
- Keep future pgvector and keyword-search details out of HTTP route handlers.

Current behavior:

- Placeholders raise `NotImplementedError`.

## Diagnosis Agent

Location: `apps/api/app/agent/graph.py`

Purpose:

- Orchestrate telemetry, incident context, retrieved evidence, and tool results.
- Produce probable causes, evidence trails, recommended actions, and human review requirements.

Current behavior:

- `PlaceholderDiagnosisAgentGraph` raises `NotImplementedError`.
- `POST /incidents/{incident_id}/analyze` does not call the graph yet. It returns a typed placeholder `Diagnosis` directly from mock data with a TODO pointing back to the future graph.

## Tool Calling Layer

Location: `apps/api/app/agent/tools.py`

Purpose:

- Provide typed adapters for safe external actions such as telemetry lookups, CMMS queries, maintenance ticket creation, and document search.
- Centralize authorization, validation, audit logging, and failure handling.

Current behavior:

- `PlaceholderToolRegistry` returns no tools and disabled call results.

## Agent Trace

Location: `apps/api/app/schemas/agent_trace.py`

Purpose:

- Represent future agent execution steps for debugging, review, and operator trust.

Current behavior:

- `GET /agent/traces/{trace_id}` returns mock trace data only.
- Mock steps are: `load_incident_context`, `detect_anomalies`, `retrieve_manuals`, `generate_hypotheses`, and `human_confirmation_pending`.
- The mock trace must not be treated as evidence that an agent, retriever, model, or tool ran.

## Evaluation

Location: `apps/api/app/agent/evaluation.py`

Purpose:

- Define the future boundary for diagnosis evaluation cases and scoring.

Current behavior:

- `EvaluationCase` is a stable schema.
- `PlaceholderDiagnosisEvaluator` raises a placeholder exception.

## Human-In-The-Loop Future State

Future diagnosis workflows should preserve:

- Who requested an analysis.
- Which retrieved documents and telemetry points were used.
- Which tools were called and with what inputs.
- Whether an operator approved, rejected, edited, or escalated a recommendation.
- A durable audit trail for reliability and safety reviews.
