import { defineStore } from 'pinia';

import { api } from '../api/client';
import type { DocumentSummary, IngestDocumentRequest, IngestDocumentResponse } from '../types/domain';

interface DocumentState {
  documents: DocumentSummary[];
  lastIngest: IngestDocumentResponse | null;
  loading: boolean;
  error: string | null;
}

export const useDocumentStore = defineStore('documents', {
  state: (): DocumentState => ({
    documents: [],
    lastIngest: null,
    loading: false,
    error: null,
  }),
  actions: {
    async fetchDocuments() {
      this.loading = true;
      this.error = null;
      try {
        this.documents = await api.listDocuments();
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Unable to load documents.';
      } finally {
        this.loading = false;
      }
    },
    async ingestDocument(payload: IngestDocumentRequest) {
      this.loading = true;
      this.error = null;
      try {
        this.lastIngest = await api.ingestDocument(payload);
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Unable to ingest document.';
      } finally {
        this.loading = false;
      }
    },
  },
});
