<script setup lang="ts">
import { computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

import { useMachineStore } from '../stores/machines';

const route = useRoute();
const machineStore = useMachineStore();
const machineId = computed(() => String(route.params.machineId ?? ''));

async function loadMachine() {
  if (machineId.value) {
    await machineStore.fetchMachine(machineId.value);
  }
}

onMounted(loadMachine);
watch(machineId, loadMachine);

function formatDate(value: string): string {
  return new Intl.DateTimeFormat('en', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(new Date(value));
}
</script>

<template>
  <section class="page-heading" v-if="machineStore.selectedMachine">
    <div>
      <p class="eyebrow">{{ machineStore.selectedMachine.asset_tag }}</p>
      <h1>{{ machineStore.selectedMachine.name }}</h1>
    </div>
    <span :class="['badge large', machineStore.selectedMachine.status]">
      {{ machineStore.selectedMachine.status }}
    </span>
  </section>

  <p v-if="machineStore.error" class="error-text">{{ machineStore.error }}</p>

  <section v-if="machineStore.selectedMachine" class="detail-grid">
    <div class="surface">
      <h2>Asset Profile</h2>
      <dl class="data-list">
        <div>
          <dt>Type</dt>
          <dd>{{ machineStore.selectedMachine.equipment_type }}</dd>
        </div>
        <div>
          <dt>Line</dt>
          <dd>{{ machineStore.selectedMachine.line }}</dd>
        </div>
        <div>
          <dt>Location</dt>
          <dd>{{ machineStore.selectedMachine.location }}</dd>
        </div>
        <div>
          <dt>Manufacturer</dt>
          <dd>{{ machineStore.selectedMachine.manufacturer }}</dd>
        </div>
        <div>
          <dt>Model</dt>
          <dd>{{ machineStore.selectedMachine.model }}</dd>
        </div>
        <div>
          <dt>Last service</dt>
          <dd>{{ formatDate(machineStore.selectedMachine.last_service_at) }}</dd>
        </div>
      </dl>
    </div>

    <div class="surface">
      <h2>Current Telemetry</h2>
      <p v-if="machineStore.telemetry?.summary" class="muted">
        {{ machineStore.telemetry.summary }}
      </p>
      <div class="reading-grid" v-if="machineStore.telemetry">
        <article
          v-for="reading in machineStore.telemetry.readings"
          :key="reading.name"
          class="reading-tile"
        >
          <span>{{ reading.name }}</span>
          <strong>{{ reading.value }} {{ reading.unit }}</strong>
          <small :class="['badge', reading.status]">{{ reading.status }} / {{ reading.trend }}</small>
        </article>
      </div>
    </div>

    <div class="surface full-span">
      <h2>Maintenance Window</h2>
      <p>{{ machineStore.selectedMachine.next_maintenance.description }}</p>
      <p class="muted">
        {{ formatDate(machineStore.selectedMachine.next_maintenance.starts_at) }}
        to
        {{ formatDate(machineStore.selectedMachine.next_maintenance.ends_at) }}
      </p>
      <div class="signal-row">
        <span
          v-for="signal in machineStore.selectedMachine.monitored_signals"
          :key="signal"
          class="signal-chip"
        >
          {{ signal }}
        </span>
      </div>
    </div>
  </section>
</template>
