<script setup lang="ts">
import { RouterLink } from 'vue-router';

const links = [
  { label: 'Dashboard', to: { name: 'dashboard' } },
  { label: 'Documents', to: { name: 'documents' } },
  { label: 'Agent Trace', to: { name: 'agent-trace', params: { traceId: 'trace-demo' } } },
  { label: 'Evaluation', to: { name: 'evaluation' } },
];
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <RouterLink class="brand" :to="{ name: 'dashboard' }">
        <span class="brand-mark">IA</span>
        <span>
          <strong>Industrial AI</strong>
          <small>Troubleshooting Copilot</small>
        </span>
      </RouterLink>

      <nav class="nav-list" aria-label="Primary navigation">
        <RouterLink v-for="link in links" :key="link.label" class="nav-link" :to="link.to">
          {{ link.label }}
        </RouterLink>
      </nav>

      <div class="system-strip">
        <span class="status-dot"></span>
        Local RAG MVP
      </div>
    </aside>

    <main class="main-panel">
      <slot />
    </main>
  </div>
</template>
