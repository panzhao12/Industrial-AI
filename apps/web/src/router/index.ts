import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
    },
    {
      path: '/machines/:machineId',
      name: 'machine-detail',
      component: () => import('../views/MachineDetailView.vue'),
      props: true,
    },
    {
      path: '/incidents/:incidentId',
      name: 'incident-detail',
      component: () => import('../views/IncidentDetailView.vue'),
      props: true,
    },
    {
      path: '/documents',
      name: 'documents',
      component: () => import('../views/DocumentLibraryView.vue'),
    },
    {
      path: '/diagnosis/:incidentId',
      name: 'diagnosis',
      component: () => import('../views/DiagnosisResultView.vue'),
      props: true,
    },
    {
      path: '/evaluation',
      name: 'evaluation',
      component: () => import('../views/EvaluationView.vue'),
    },
    {
      path: '/agent/traces/:traceId',
      name: 'agent-trace',
      component: () => import('../views/AgentTraceView.vue'),
      props: true,
    },
  ],
});

export default router;
