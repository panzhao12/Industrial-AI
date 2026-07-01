import { defineStore } from 'pinia';

import { api } from '../api/client';
import type {
  DocumentChunk,
  DocumentSummary,
  IngestDocumentRequest,
  IngestDocumentResponse,
  RagSearchResponse,
} from '../types/domain';

interface DocumentState {
  documents: DocumentSummary[];
  selectedDocument: DocumentSummary | null;
  chunks: DocumentChunk[];
  lastIngest: IngestDocumentResponse | null;
  searchResponse: RagSearchResponse | null;
  loading: boolean;
  searching: boolean;
  error: string | null;
}

export const useDocumentStore = defineStore('documents', {
  state: (): DocumentState => ({
    documents: [],
    selectedDocument: null,
    chunks: [],
    lastIngest: null,
    searchResponse: null,
    loading: false,
    searching: false,
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
    async fetchDocument(documentId: string) {
      this.loading = true;
      this.error = null;
      try {
        const [document, chunks] = await Promise.all([
          api.getDocument(documentId),
          api.listDocumentChunks(documentId),
        ]);
        this.selectedDocument = document;
        this.chunks = chunks;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Unable to load document.';
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
    async search(query: string, topK: number) {
      this.searching = true;
      this.error = null;
      try {
        this.searchResponse = await api.searchRag({ query, top_k: topK });
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Unable to run placeholder RAG search.';
      } finally {
        this.searching = false;
      }
    },
  },
});
