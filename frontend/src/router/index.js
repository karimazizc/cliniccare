import { createRouter, createWebHistory } from 'vue-router'
import ConsultationsList from '../views/ConsultationsList.vue'
import NewConsultation from '../views/NewConsultation.vue'

const routes = [
  {
    path: '/',
    name: 'consultations',
    component: ConsultationsList,
    meta: {
      title: 'Consultations'
    }
  },
  {
    path: '/new',
    name: 'new-consultation',
    component: NewConsultation,
    meta: {
      title: 'New Consultation'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Update page title on navigation
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || 'ClinicCare'} | ClinicCare EMR`
  next()
})

export default router
