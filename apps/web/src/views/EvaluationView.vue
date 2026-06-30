<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';

import { api } from '../api/client';
import type { EvaluationCase } from '../types/domain';

const metrics = [
  { label: 'Diagnosis precision', value: 'Not scored', tone: 'neutral' },
  { label: 'Mean review time', value: 'Not measured', tone: 'neutral' },
  { label: 'Escalation rate', value: 'Not measured', tone: 'neutral' },
];

const cases = ref<EvaluationCase[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const confirmationCount = computed(
  () => cases.value.filter((item) => item.should_require_human_confirmation).length,
);

onMounted(async () => {
  loading.value = true;
  error.value = null;
  try {
    cases.value = await api.listEvaluationCases();
  } catch (caught) {
    error.value = caught instanceof Error ? caught.message : 'Unable to load evaluation cases.';
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section class="page-heading">
    <div>
      <p class="eyebrow">Quality loop</p>
      <h1>Evaluation</h1>
    </div>
  </section>

  <section class="metric-grid">
    <article v-for="metric in metrics" :key="metric.label" class="metric-tile">
      <span>{{ metric.label }}</span>
      <strong>{{ metric.value }}</strong>
    </article>
    <article class="metric-tile warning">
      <span>Human confirmation cases</span>
      <strong>{{ confirmationCount }}</strong>
    </article>
  </section>

  <section class="surface">
    <h2>Evaluation Cases</h2>
    <p v-if="loading" class="muted">Loading synthetic cases.</p>
    <p v-if="error" class="error-text">{{ error }}</p>
    <table class="data-table">
      <thead>
        <tr>
          <th>Case</th>
          <th>Incident input</th>
          <th>Expected codes</th>
          <th>Human confirmation</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in cases" :key="item.case_id">
          <td>{{ item.case_id }}</td>
          <td>{{ item.incident_input }}</td>
          <td>{{ item.expected_error_codes.join(', ') }}</td>
          <td>{{ item.should_require_human_confirmation ? 'Yes' : 'No' }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>
