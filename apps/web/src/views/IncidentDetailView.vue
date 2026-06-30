<script setup lang="ts">
import { computed, onMounted, watch } from 'vue';
import { RouterLink, useRoute } from 'vue-router';

import { useIncidentStore } from '../stores/incidents';
import { useMachineStore } from '../stores/machines';

const route = useRoute();
const incidentStore = useIncidentStore();
const machineStore = useMachineStore();
const incidentId = computed(() => String(route.params.incidentId ?? ''));

async function loadIncident() {
  if (!incidentId.value) {
    return;
  }
  await incidentStore.fetchIncident(incidentId.value);
  if (incidentStore.selectedIncident) {
    await machineStore.fetchMachine(incidentStore.selectedIncident.machine_id);
  }
}

onMounted(loadIncident);
watch(incidentId, loadIncident);

function formatDateTime(value: string): string {
  return new Intl.DateTimeFormat('en', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value));
}
</script>

<template>
  <section class="page-heading" v-if="incidentStore.selectedIncident">
    <div>
      <p class="eyebrow">{{ incidentStore.selectedIncident.id }}</p>
      <h1>{{ incidentStore.selectedIncident.title }}</h1>
    </div>
    <RouterLink
      class="button"
      :to="{ name: 'diagnosis', params: { incidentId: incidentStore.selectedIncident.id } }"
    >
      Analyze
    </RouterLink>
  </section>

  <p v-if="incidentStore.error" class="error-text">{{ incidentStore.error }}</p>

  <section v-if="incidentStore.selectedIncident" class="detail-grid">
    <div class="surface">
      <h2>Incident</h2>
      <p>{{ incidentStore.selectedIncident.description }}</p>
      <dl class="data-list">
        <div>
          <dt>Error codes</dt>
          <dd>
            <span
              v-for="code in incidentStore.selectedIncident.error_codes"
              :key="code"
              class="signal-chip"
            >
              {{ code }}
            </span>
          </dd>
        </div>
        <div>
          <dt>Severity</dt>
          <dd>
            <span :class="['badge', incidentStore.selectedIncident.severity]">
              {{ incidentStore.selectedIncident.severity }}
            </span>
          </dd>
        </div>
        <div>
          <dt>Status</dt>
          <dd>{{ incidentStore.selectedIncident.status }}</dd>
        </div>
        <div>
          <dt>Owner</dt>
          <dd>{{ incidentStore.selectedIncident.owner }}</dd>
        </div>
        <div>
          <dt>Opened</dt>
          <dd>{{ formatDateTime(incidentStore.selectedIncident.opened_at) }}</dd>
        </div>
      </dl>
    </div>

    <div class="surface">
      <h2>Symptoms</h2>
      <ul class="check-list">
        <li v-for="symptom in incidentStore.selectedIncident.symptoms" :key="symptom">
          {{ symptom }}
        </li>
      </ul>
    </div>

    <div class="surface full-span">
      <h2>Telemetry Summary</h2>
      <p>{{ incidentStore.selectedIncident.telemetry_summary }}</p>
      <dl class="data-list">
        <div>
          <dt>Root cause</dt>
          <dd>{{ incidentStore.selectedIncident.root_cause ?? 'Not confirmed' }}</dd>
        </div>
        <div>
          <dt>Downtime</dt>
          <dd>{{ incidentStore.selectedIncident.downtime_hours ?? 0 }} hours</dd>
        </div>
        <div>
          <dt>Outcome</dt>
          <dd>{{ incidentStore.selectedIncident.outcome ?? 'Pending' }}</dd>
        </div>
      </dl>
      <div class="signal-row">
        <span
          v-for="section in incidentStore.selectedIncident.related_manual_sections"
          :key="section"
          class="signal-chip"
        >
          {{ section }}
        </span>
      </div>
    </div>

    <div class="surface full-span">
      <h2>Timeline</h2>
      <div class="timeline">
        <article
          v-for="event in incidentStore.selectedIncident.timeline"
          :key="`${event.occurred_at}-${event.label}`"
          class="timeline-row"
        >
          <time>{{ formatDateTime(event.occurred_at) }}</time>
          <span>
            <strong>{{ event.label }}</strong>
            <small>{{ event.description }}</small>
          </span>
        </article>
      </div>
    </div>
  </section>
</template>
