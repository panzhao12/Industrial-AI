# Agent Contracts

This project contains an implemented local RAG MVP, but it intentionally does not implement an AI diagnosis workflow yet. The backend exposes typed boundaries so future LangGraph orchestration, tool calling, persistent retrieval, and human-in-the-loop diagnosis can be added without rewriting the HTTP API.

## Implementation Boundaries

`apps/api/app/rag/` contains intentional, active local-development implementations:

- Markdown and synthetic JSON document loading
- Markdown-aware chunking
- Deterministic fake embeddings
- Optional local sentence-transformer embeddings
- In-memory vector storage and cosine search
- Vector retrieval and RAG evaluation

Do not describe this RAG path as PostgreSQL-backed, durable, hybrid, reranked, or integrated with diagnosis. Those capabilities are not implemented.

`apps/api/app/agent/` remains reserved for future manual implementation. Do not implement LangGraph, LLM diagnosis, prompt orchestration, model-provider calls, or external tool execution there unless the user explicitly requests it.

Do not add OpenAI, Anthropic, Claude, or other hosted model-provider integrations anywhere in the project unless the user explicitly requests them. Placeholder agent components should remain boring and safe: raise `NotImplementedError`, return disabled results, or expose typed contracts. Mock diagnosis and trace data belongs in `apps/api/app/data/mock_data.py`.

## RAG Retriever

Location: `apps/api/app/rag/retriever.py`

Purpose:

- Accept an incident or diagnostic query.
- Retrieve relevant chunks from manuals, maintenance logs, standard operating procedures, and past incidents.
- Return scored evidence with metadata and source references.

Current behavior:

- `VectorRagRetriever` indexes embedded chunks through the configured vector-store boundary.
- It embeds queries, runs vector search, and returns scored `RetrievedChunk` results.
- The application runtime uses `VectorRagRetriever`.
- `PlaceholderRagRetriever` remains as an unused future/disabled implementation and raises `NotImplementedError`.

## Embedding Service

Location: `apps/api/app/rag/embeddings.py`

Purpose:

- Convert document chunks and user/incident queries into vectors.
- Keep embedding vendor and model choice outside the route layer.

Current behavior:

- `FakeEmbeddingProvider` is the default. It produces deterministic 1,536-dimensional vectors for development and tests; it is not semantic.
- `LocalSentenceTransformerEmbeddingProvider` provides optional local semantic embeddings.
- The local provider defaults to `intfloat/multilingual-e5-small` and uses E5 query/passage prefixes.
- `create_embedding_provider` supports `fake` and `local`.
- The local provider requires `sentence-transformers`, which is not part of the base project dependencies.

## Loading, Chunking, and Vector Search

Locations:

- `apps/api/app/rag/document_loader.py`
- `apps/api/app/rag/json_knowledge_loader.py`
- `apps/api/app/rag/chunker.py`
- `apps/api/app/rag/vector_store.py`
- `apps/api/app/rag/hybrid_search.py`

Purpose:

- Normalize supported knowledge sources into loaded documents.
- Split documents into retrieval-sized chunks.
- Keep vector-store and future hybrid-search details out of HTTP route handlers.

Current behavior:

- `MarkdownFileDocumentLoader` loads local Markdown files.
- `json_knowledge_loader.py` converts machines, telemetry, error codes, manual metadata, and repair cases into `LoadedDocument` objects.
- `MarkdownChunker` splits content by headings and character limits.
- `InMemoryVectorStore` stores records for the life of the API process and performs cosine-similarity search.
- `PlaceholderVectorStore` still raises `NotImplementedError` for future persistent storage.
- `PlaceholderHybridSearch` still raises `NotImplementedError`; lexical and hybrid retrieval are not implemented.

## RAG Runtime and Evaluation

Locations:

- `apps/api/app/rag/runtime.py`
- `apps/api/app/rag/evaluation.py`
- `apps/api/app/api/routes/rag.py`

Current behavior:

- The runtime wires the configured embedding provider to `InMemoryVectorStore` and `VectorRagRetriever`.
- Local ingestion can load Markdown manuals only or the broader synthetic knowledge base.
- `POST /rag/search` returns real retrieval results with `is_placeholder=false`.
- `POST /rag/evaluate` scores the populated index against five static RAG cases.
- The runtime is process-local and loses all indexed records when the API restarts.
- It does not write to PostgreSQL/pgvector.

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

Locations:

- `apps/api/app/rag/evaluation.py`
- `apps/api/app/agent/evaluation.py`

Purpose:

- Evaluate current retrieval behavior separately from future diagnosis quality.

Current behavior:

- `RagEvalCase` and `evaluate_rag_cases` implement retrieval evaluation.
- `POST /rag/evaluate` uses `data/synthetic/evaluation/rag_eval_cases.json`.
- `EvaluationCase` is a stable schema.
- `PlaceholderDiagnosisEvaluator` raises a placeholder exception.
- `GET /evaluation/cases` returns diagnosis fixtures but does not score model behavior.

## Human-In-The-Loop Future State

Future diagnosis workflows should preserve:

- Who requested an analysis.
- Which retrieved documents and telemetry points were used.
- Which tools were called and with what inputs.
- Whether an operator approved, rejected, edited, or escalated a recommendation.
- A durable audit trail for reliability and safety reviews.
