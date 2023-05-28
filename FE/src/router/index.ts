import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from "@/views/DashboardView.vue";
import PatientAView from "@/views/PatientAView.vue";
import PatientBView from "@/views/PatientBView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/Patient-A',
      name: 'patient-a',
      component: PatientAView
    },
    {
      path: '/Patient-B',
      name: 'patient-b',
      component: PatientBView
    }
  ]
})

export default router
