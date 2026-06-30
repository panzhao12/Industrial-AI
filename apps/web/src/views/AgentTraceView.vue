<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

import { api } from '../api/client';
import type { AgentTrace } from '../types/domain';

const route = useRoute();
const traceId = computed(() => String(route.params.traceId ?? 'trace-demo'));
const trace = ref<AgentTrace | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

async function loadTrace() {
  loading.value = true;
  error.value = null;
  try {
    trace.value = await api.getAgentTrace(traceId.value);
  } catch (caught) {
    error.value = caught instanceof Error ? caught.message : 'Unable to load agent trace.';
  } finally {
    loading.value = false;
  }
}

onMounted(loadTrace);
watch(traceId, loadTrace);
</script>

<template>
  <section class="page-heading">
    <div>
      <p class="eyebrow">{{ traceId }}</p>
      <h1>Agent Trace</h1>
    </div>
    <span class="pill">Mock data only</span>
  </section>

  <p v-if="error" class="error-text">{{ error }}</p>

  <section class="surface">
    <h2>Trace Steps</h2>
    <p v-if="trace" class="muted">{{ trace.message }}</p>
    <p v-else-if="loading" class="muted">Loading mock trace.</p>

    <div v-if="trace" class="timeline">
      <article v-for="step in trace.steps" :key="step.name" class="timeline-row">
        <time>{{ step.status }}</time>
        <span>
          <strong>{{ step.name }}</strong>
          <small>{{ step.detail }}</small>
        </span>
      </article>
    </div>
  </section>
</template>
