import { defineStore } from 'pinia';

import { api } from '../api/client';
import type { CurrentTelemetry, MachineDetail, MachineSummary } from '../types/domain';

interface MachineState {
  machines: MachineSummary[];
  selectedMachine: MachineDetail | null;
  telemetry: CurrentTelemetry | null;
  loading: boolean;
  error: string | null;
}

export const useMachineStore = defineStore('machines', {
  state: (): MachineState => ({
    machines: [],
    selectedMachine: null,
    telemetry: null,
    loading: false,
    error: null,
  }),
  actions: {
    async fetchMachines() {
      this.loading = true;
      this.error = null;
      try {
        this.machines = await api.listMachines();
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Unable to load machines.';
      } finally {
        this.loading = false;
      }
    },
    async fetchMachine(machineId: string) {
      this.loading = true;
      this.error = null;
      try {
        const [machine, telemetry] = await Promise.all([
          api.getMachine(machineId),
          api.getMachineTelemetry(machineId),
        ]);
        this.selectedMachine = machine;
        this.telemetry = telemetry;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Unable to load machine.';
      } finally {
        this.loading = false;
      }
    },
  },
});
