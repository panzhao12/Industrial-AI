<script setup lang="ts">
import { onMounted, reactive } from 'vue';

import { useDocumentStore } from '../stores/documents';
import type { DocumentKind, IngestDocumentRequest } from '../types/domain';

const documentStore = useDocumentStore();
const documentKinds: DocumentKind[] = ['manual', 'maintenance_log', 'sop', 'incident_report'];
const form = reactive<IngestDocumentRequest>({
  name: '',
  kind: 'manual',
  machine_id: '',
  source_uri: '',
  domain: 'hydraulics',
  machine_type: '',
});
const searchForm = reactive({
  query: 'pressure oscillation under load',
  topK: 5,
});

onMounted(async () => {
  await documentStore.fetchDocuments();
  if (documentStore.documents[0]) {
    await selectDocument(documentStore.documents[0].id);
  }
});

async function selectDocument(documentId: string) {
  await documentStore.fetchDocument(documentId);
}

async function submitIngest() {
  await documentStore.ingestDocument({
    name: form.name,
    kind: form.kind,
    machine_id: form.machine_id || null,
    source_uri: form.source_uri || null,
    domain: form.domain || null,
    machine_type: form.machine_type || null,
  });
  form.name = '';
  form.machine_id = '';
  form.source_uri = '';
}

async function submitSearch() {
  await documentStore.search(searchForm.query, searchForm.topK);
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat('en', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  }).format(new Date(value));
}
</script>

<template>
  <section class="page-heading">
    <div>
      <p class="eyebrow">Knowledge base</p>
      <h1>Document Library</h1>
    </div>
  </section>

  <section class="split-layout">
    <div class="surface">
      <div class="section-title">
        <h2>Documents</h2>
      </div>
      <p v-if="documentStore.error" class="error-text">{{ documentStore.error }}</p>
      <div class="list-stack">
        <button
          v-for="document in documentStore.documents"
          :key="document.id"
          type="button"
          :class="[
            'list-row',
            'plain',
            'document-button',
            { selected: documentStore.selectedDocument?.id === document.id },
          ]"
          @click="selectDocument(document.id)"
        >
          <span>
            <strong>{{ document.title ?? document.name }}</strong>
            <small>
              {{ document.machine_type ?? document.kind }} / {{ document.machine_id ?? 'plant-wide' }}
              <template v-if="document.sections.length"> / {{ document.sections.length }} sections</template>
            </small>
          </span>
          <span class="muted">{{ formatDate(document.uploaded_at) }}</span>
        </button>
      </div>
    </div>

    <form class="surface form-stack" @submit.prevent="submitIngest">
      <h2>Ingest Request</h2>
      <label>
        Document name
        <input v-model="form.name" required type="text" placeholder="Compressor inspection log" />
      </label>
      <label>
        Type
        <select v-model="form.kind">
          <option v-for="kind in documentKinds" :key="kind" :value="kind">{{ kind }}</option>
        </select>
      </label>
      <label>
        Machine ID
        <input v-model="form.machine_id" type="text" placeholder="compressor-02" />
      </label>
      <label>
        Source URI
        <input v-model="form.source_uri" type="text" placeholder="s3://manuals/example.pdf" />
      </label>
      <label>
        Domain
        <input v-model="form.domain" type="text" placeholder="hydraulics" />
      </label>
      <label>
        Machine type
        <input v-model="form.machine_type" type="text" placeholder="hydraulic excavator" />
      </label>
      <button class="button" type="submit" :disabled="documentStore.loading">
        Submit
      </button>
      <p v-if="documentStore.lastIngest" class="success-text">
        {{ documentStore.lastIngest.message }}
      </p>
      <p v-if="documentStore.lastIngest" class="muted">
        Run {{ documentStore.lastIngest.run_id }} / {{ documentStore.lastIngest.status }}
      </p>
    </form>
  </section>

  <section class="detail-grid document-workspace">
    <div class="surface">
      <h2>Document Detail</h2>
      <template v-if="documentStore.selectedDocument">
        <dl class="data-list">
          <div>
            <dt>Title</dt>
            <dd>{{ documentStore.selectedDocument.title ?? documentStore.selectedDocument.name }}</dd>
          </div>
          <div>
            <dt>Source type</dt>
            <dd>{{ documentStore.selectedDocument.source_type ?? 'metadata only' }}</dd>
          </div>
          <div>
            <dt>Domain</dt>
            <dd>{{ documentStore.selectedDocument.domain ?? 'unspecified' }}</dd>
          </div>
          <div>
            <dt>File path</dt>
            <dd>{{ documentStore.selectedDocument.file_path ?? documentStore.selectedDocument.source_uri }}</dd>
          </div>
        </dl>
      </template>
      <p v-else class="muted">Select a document to inspect metadata.</p>
    </div>

    <div class="surface">
      <h2>Chunks Preview</h2>
      <p class="muted">Placeholder chunks only. No parsing, embeddings, or vector writes have run.</p>
      <div class="list-stack chunk-list">
        <article v-for="chunk in documentStore.chunks" :key="chunk.id" class="list-row plain chunk-row">
          <span>
            <strong>{{ chunk.section_title ?? `Chunk ${chunk.chunk_index}` }}</strong>
            <small>{{ chunk.content }}</small>
          </span>
        </article>
      </div>
    </div>

    <form class="surface form-stack" @submit.prevent="submitSearch">
      <h2>RAG Search</h2>
      <label>
        Query
        <input v-model="searchForm.query" required type="text" />
      </label>
      <label>
        Top K
        <input v-model.number="searchForm.topK" min="1" max="20" type="number" />
      </label>
      <button class="button" type="submit" :disabled="documentStore.searching">
        Search
      </button>
      <p v-if="documentStore.searchResponse" class="muted">
        {{ documentStore.searchResponse.message }}
      </p>
    </form>

    <div class="surface">
      <h2>Search Results</h2>
      <div v-if="documentStore.searchResponse" class="list-stack">
        <article
          v-for="result in documentStore.searchResponse.results"
          :key="result.chunk_id"
          class="list-row plain chunk-row"
        >
          <span>
            <strong>{{ result.document_title }}</strong>
            <small>{{ result.section_title }} / score {{ result.score }}</small>
            <small>{{ result.content }}</small>
          </span>
        </article>
      </div>
      <p v-else class="muted">Populate the local RAG index through the API, then run a search.</p>
    </div>
  </section>
</template>
