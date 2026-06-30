<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
import { RouterLink, useRoute } from 'vue-router';

import { diagnosisEventsUrl } from '../api/client';
import { useIncidentStore } from '../stores/incidents';

const route = useRoute();
const incidentStore = useIncidentStore();
const incidentId = computed(() => String(route.params.incidentId ?? ''));
const operatorNotes = ref('');
const streamMessage = ref('Waiting for stream event');
let eventSource: EventSource | null = null;

async function load() {
  if (!incidentId.value) {
    return;
  }
  await incidentStore.fetchIncident(incidentId.value);
  openEventStream();
}

function openEventStream() {
  eventSource?.close();
  eventSource = new EventSource(diagnosisEventsUrl(incidentId.value));
  eventSource.addEventListener('diagnosis_status', (event) => {
    const payload = JSON.parse((event as MessageEvent).data) as { message: string };
    streamMessage.value = payload.message;
  });
  eventSource.onerror = () => {
    eventSource?.close();
  };
}

async function analyze() {
  await incidentStore.analyzeIncident(incidentId.value, operatorNotes.value);
}

onMounted(load);
watch(incidentId, load);
onUnmounted(() => eventSource?.close());
</script>

<template>
  <section class="page-heading">
    <div>
      <p class="eyebrow">{{ incidentId }}</p>
      <h1>Diagnosis Result</h1>
    </div>
    <span class="pill">{{ streamMessage }}</span>
  </section>

  <section class="detail-grid">
    <div class="surface">
      <h2>Analysis Request</h2>
      <label class="field-block">
        Operator notes
        <textarea v-model="operatorNotes" rows="6" placeholder="Observed noise, smell, alarms, or recent work orders"></textarea>
      </label>
      <button class="button" type="button" :disabled="incidentStore.analyzing" @click="analyze">
        {{ incidentStore.analyzing ? 'Running' : 'Run Analysis' }}
      </button>
      <RouterLink
        class="button secondary"
        :to="{ name: 'agent-trace', params: { traceId: `trace-${incidentId}` } }"
      >
        View Mock Trace
      </RouterLink>
      <p v-if="incidentStore.error" class="error-text">{{ incidentStore.error }}</p>
    </div>

    <div class="surface">
      <h2>Result</h2>
      <template v-if="incidentStore.diagnosisResult">
        <p>{{ incidentStore.diagnosisResult.summary }}</p>
        <dl class="data-list">
          <div>
            <dt>Status</dt>
            <dd>{{ incidentStore.diagnosisResult.status }}</dd>
          </div>
          <div>
            <dt>Human review</dt>
            <dd>{{ incidentStore.diagnosisResult.human_review_required ? 'required' : 'not required' }}</dd>
          </div>
          <div>
            <dt>Next state</dt>
            <dd>{{ incidentStore.diagnosisResult.next_state }}</dd>
          </div>
        </dl>
      </template>
      <p v-else class="muted">No analysis result yet.</p>
    </div>

    <div class="surface full-span">
      <h2>Evidence Trail</h2>
      <p class="muted">
        Retrieved documents, telemetry references, and tool outputs will appear here when the AI
        workflow is implemented.
      </p>
    </div>
  </section>
</template>
