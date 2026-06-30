import type {
  AnalyzeIncidentRequest,
  AgentTrace,
  CurrentTelemetry,
  DiagnosisResult,
  DocumentSummary,
  EvaluationCase,
  IncidentDetail,
  IncidentSummary,
  IngestDocumentRequest,
  IngestDocumentResponse,
  MachineDetail,
  MachineSummary,
} from '../types/domain';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000').replace(/\/$/, '');

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`API request failed (${response.status}): ${detail}`);
  }

  return response.json() as Promise<T>;
}

export const api = {
  listMachines: () => request<MachineSummary[]>('/machines'),
  getMachine: (machineId: string) => request<MachineDetail>(`/machines/${encodeURIComponent(machineId)}`),
  getMachineTelemetry: (machineId: string) =>
    request<CurrentTelemetry>(`/machines/${encodeURIComponent(machineId)}/telemetry/current`),
  listIncidents: () => request<IncidentSummary[]>('/incidents'),
  getIncident: (incidentId: string) =>
    request<IncidentDetail>(`/incidents/${encodeURIComponent(incidentId)}`),
  analyzeIncident: (incidentId: string, payload: AnalyzeIncidentRequest) =>
    request<DiagnosisResult>(`/incidents/${encodeURIComponent(incidentId)}/analyze`, {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  listDocuments: () => request<DocumentSummary[]>('/documents'),
  ingestDocument: (payload: IngestDocumentRequest) =>
    request<IngestDocumentResponse>('/documents/ingest', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  getAgentTrace: (traceId: string) =>
    request<AgentTrace>(`/agent/traces/${encodeURIComponent(traceId)}`),
  listEvaluationCases: () => request<EvaluationCase[]>('/evaluation/cases'),
};

export function diagnosisEventsUrl(incidentId: string): string {
  return `${API_BASE_URL}/events/diagnosis/${encodeURIComponent(incidentId)}`;
}
