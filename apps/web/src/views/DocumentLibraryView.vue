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
});

onMounted(documentStore.fetchDocuments);

async function submitIngest() {
  await documentStore.ingestDocument({
    name: form.name,
    kind: form.kind,
    machine_id: form.machine_id || null,
    source_uri: form.source_uri || null,
  });
  form.name = '';
  form.machine_id = '';
  form.source_uri = '';
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
        <article v-for="document in documentStore.documents" :key="document.id" class="list-row plain">
          <span>
            <strong>{{ document.name }}</strong>
            <small>
              {{ document.kind }} / {{ document.machine_id ?? 'plant-wide' }}
              <template v-if="document.sections.length"> / {{ document.sections.length }} sections</template>
            </small>
          </span>
          <span class="muted">{{ formatDate(document.uploaded_at) }}</span>
        </article>
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
      <button class="button" type="submit" :disabled="documentStore.loading">
        Submit
      </button>
      <p v-if="documentStore.lastIngest" class="success-text">
        {{ documentStore.lastIngest.message }}
      </p>
    </form>
  </section>
</template>
