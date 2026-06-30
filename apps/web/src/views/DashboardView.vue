<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { RouterLink } from 'vue-router';

import { useIncidentStore } from '../stores/incidents';
import { useMachineStore } from '../stores/machines';

const machineStore = useMachineStore();
const incidentStore = useIncidentStore();

const openIncidents = computed(
  () => incidentStore.incidents.filter((incident) => incident.status !== 'closed').length,
);
const criticalMachines = computed(
  () => machineStore.machines.filter((machine) => machine.status === 'critical').length,
);

onMounted(async () => {
  await Promise.all([machineStore.fetchMachines(), incidentStore.fetchIncidents()]);
});

function formatDate(value: string): string {
  return new Intl.DateTimeFormat('en', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value));
}
</script>

<template>
  <section class="page-heading">
    <div>
      <p class="eyebrow">Plant 4 operations</p>
      <h1>Diagnostic Command Center</h1>
    </div>
    <span class="pill">Non-AI skeleton</span>
  </section>

  <section class="metric-grid" aria-label="Operations summary">
    <article class="metric-tile">
      <span>Machines</span>
      <strong>{{ machineStore.machines.length }}</strong>
    </article>
    <article class="metric-tile danger">
      <span>Critical assets</span>
      <strong>{{ criticalMachines }}</strong>
    </article>
    <article class="metric-tile warning">
      <span>Open incidents</span>
      <strong>{{ openIncidents }}</strong>
    </article>
  </section>

  <section class="split-layout">
    <div class="surface">
      <div class="section-title">
        <h2>Machines</h2>
      </div>
      <p v-if="machineStore.error" class="error-text">{{ machineStore.error }}</p>
      <div class="list-stack">
        <RouterLink
          v-for="machine in machineStore.machines"
          :key="machine.id"
          class="list-row"
          :to="{ name: 'machine-detail', params: { machineId: machine.id } }"
        >
          <span>
            <strong>{{ machine.name }}</strong>
            <small>{{ machine.equipment_type }} / {{ machine.location }}</small>
          </span>
          <span :class="['badge', machine.status]">{{ machine.status }}</span>
        </RouterLink>
      </div>
    </div>

    <div class="surface">
      <div class="section-title">
        <h2>Incidents</h2>
      </div>
      <p v-if="incidentStore.error" class="error-text">{{ incidentStore.error }}</p>
      <div class="list-stack">
        <RouterLink
          v-for="incident in incidentStore.incidents"
          :key="incident.id"
          class="list-row"
          :to="{ name: 'incident-detail', params: { incidentId: incident.id } }"
        >
          <span>
            <strong>{{ incident.title }}</strong>
            <small>{{ incident.owner }} / opened {{ formatDate(incident.opened_at) }}</small>
          </span>
          <span :class="['badge', incident.severity]">{{ incident.severity }}</span>
        </RouterLink>
      </div>
    </div>
  </section>
</template>
