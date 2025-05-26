import { ref } from 'vue'

export const forceUpdate = ref(0)
export const summaryUpdateTrigger = ref(0)

export function triggerSummaryUpdate() {
  summaryUpdateTrigger.value++
}