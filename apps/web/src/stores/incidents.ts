import { defineStore } from 'pinia';

import { api } from '../api/client';
import type { DiagnosisResult, IncidentDetail, IncidentSummary } from '../types/domain';

interface IncidentState {
  incidents: IncidentSummary[];
  selectedIncident: IncidentDetail | null;
  diagnosisResult: DiagnosisResult | null;
  loading: boolean;
  analyzing: boolean;
  error: string | null;
}

export const useIncidentStore = defineStore('incidents', {
  state: (): IncidentState => ({
    incidents: [],
    selectedIncident: null,
    diagnosisResult: null,
    loading: false,
    analyzing: false,
    error: null,
  }),
  actions: {
    async fetchIncidents() {
      this.loading = true;
      this.error = null;
      try {
        this.incidents = await api.listIncidents();
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Unable to load incidents.';
      } finally {
        this.loading = false;
      }
    },
    async fetchIncident(incidentId: string) {
      this.loading = true;
      this.error = null;
      try {
        this.selectedIncident = await api.getIncident(incidentId);
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Unable to load incident.';
      } finally {
        this.loading = false;
      }
    },
    async analyzeIncident(incidentId: string, operatorNotes?: string) {
      this.analyzing = true;
      this.error = null;
      try {
        this.diagnosisResult = await api.analyzeIncident(incidentId, {
          operator_notes: operatorNotes || undefined,
          requested_by: 'web-ui',
        });
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Unable to analyze incident.';
      } finally {
        this.analyzing = false;
      }
    },
  },
});
