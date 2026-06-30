export type MachineStatus = 'healthy' | 'warning' | 'critical' | 'offline';
export type SensorStatus = 'normal' | 'warning' | 'critical';
export type IncidentSeverity = 'low' | 'medium' | 'high' | 'critical';
export type IncidentStatus = 'open' | 'investigating' | 'mitigated' | 'closed';
export type AnalysisStatus = 'placeholder' | 'queued' | 'completed' | 'failed';
export type DocumentKind = 'manual' | 'maintenance_log' | 'sop' | 'incident_report';
export type AgentTraceStatus = 'mock' | 'pending' | 'completed' | 'failed';

export interface MachineSummary {
  id: string;
  name: string;
  asset_tag: string;
  equipment_type: string;
  line: string;
  location: string;
  status: MachineStatus;
  criticality: string;
}

export interface MaintenanceWindow {
  starts_at: string;
  ends_at: string;
  description: string;
}

export interface MachineDetail extends MachineSummary {
  manufacturer: string;
  model: string;
  installed_at: string;
  last_service_at: string;
  next_maintenance: MaintenanceWindow;
  monitored_signals: string[];
}

export interface SensorReading {
  name: string;
  value: number;
  unit: string;
  status: SensorStatus;
  trend: string;
}

export interface CurrentTelemetry {
  scenario_id: string | null;
  machine_id: string;
  scenario_label: string | null;
  summary: string | null;
  captured_at: string;
  readings: SensorReading[];
}

export interface IncidentSummary {
  id: string;
  machine_id: string;
  title: string;
  severity: IncidentSeverity;
  status: IncidentStatus;
  opened_at: string;
  owner: string;
}

export interface IncidentTimelineEvent {
  occurred_at: string;
  label: string;
  description: string;
}

export interface IncidentDetail extends IncidentSummary {
  description: string;
  symptoms: string[];
  error_codes: string[];
  telemetry_summary: string | null;
  root_cause: string | null;
  actions_taken: string[];
  outcome: string | null;
  downtime_hours: number | null;
  related_manual_sections: string[];
  timeline: IncidentTimelineEvent[];
}

export interface AnalyzeIncidentRequest {
  operator_notes?: string;
  requested_by?: string;
}

export interface DiagnosisCause {
  label: string;
  rationale: string;
  confidence: number | null;
}

export interface DiagnosisRecommendation {
  action: string;
  priority: string;
  safety_note: string | null;
}

export interface DiagnosisEvidence {
  source: string;
  reference: string;
  excerpt: string;
}

export interface DiagnosisResult {
  incident_id: string;
  status: AnalysisStatus;
  generated_at: string;
  summary: string;
  confidence: number | null;
  probable_causes: DiagnosisCause[];
  recommended_actions: DiagnosisRecommendation[];
  evidence: DiagnosisEvidence[];
  human_review_required: boolean;
  next_state: string;
}

export interface DocumentSummary {
  id: string;
  name: string;
  kind: DocumentKind;
  machine_id: string | null;
  uploaded_at: string;
  status: string;
  source_uri: string | null;
  sections: string[];
}

export interface IngestDocumentRequest {
  name: string;
  kind: DocumentKind;
  machine_id?: string | null;
  source_uri?: string | null;
}

export interface IngestDocumentResponse {
  status: string;
  document_name: string;
  message: string;
}

export interface AgentTraceStep {
  name: string;
  status: AgentTraceStatus;
  started_at: string | null;
  completed_at: string | null;
  detail: string;
  inputs: Record<string, string>;
  outputs: Record<string, string>;
}

export interface AgentTrace {
  trace_id: string;
  incident_id: string | null;
  is_mock: boolean;
  message: string;
  steps: AgentTraceStep[];
}

export interface EvaluationCase {
  case_id: string;
  incident_input: string;
  expected_error_codes: string[];
  expected_retrieved_documents: string[];
  expected_root_causes: string[];
  expected_safety_notes: string[];
  should_require_human_confirmation: boolean;
}
