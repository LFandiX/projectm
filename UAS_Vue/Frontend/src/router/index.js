import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../components/HomeView.vue'
import Dashboard from '../components/Dasboard.vue'


const routes = [
  {
    path: '/',
    name: 'Login',
    component: HomeView
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
