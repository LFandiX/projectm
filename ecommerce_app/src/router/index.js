
import { useUserStore } from '@/stores/userStore'
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../components/Homeview.vue'
import Login from '../components/Login.vue'
import Signin from '../components/Signin.vue'
import Unauthorized from '../components/unouthorized.vue' 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/signin',
      name: 'Signin',
      component: Signin,
    },
    {
      path: '/privacy',
      name: 'PrivacyPolicy',
      component: () => import('../components/privacypolicy.vue'),
    },
    {
      path: '/contactus',
      name: 'ContactUs',
      component: () => import('../components/contactus.vue'),
    },
     {
      path: '/shop',
      name: 'Shop',
      component: () => import('../components/shop.vue'),
    },
    {
      path: '/basket',
      name: 'Basket',
      component: () => import('../components/basket.vue'),
    },
    {
      path: '/shop/:id',
      name: 'ProductDetail',
      component: () => import('../components/productdetail.vue'),
    },
    {
      path: '/terms-and-condition',
      name: 'TermsAndConditions',
      component: () => import('../components/termsandconditions.vue'),
    },
    {
      path: '/shop/address',
      name: 'Address',
      component: () => import('../components/address.vue'),
    },
    {
      path: '/shop/payment',
      name: 'Payment',
      component: () => import('../components/payment.vue'),
    },
    {
      path: '/paymentdetail',
      name: 'PaymentDetail',
      component: () => import('../components/paymentconfirmation.vue'),
    },
    {
      path: '/history',
      name: 'OrderHistory',
      component: () => import('../components/history.vue'),
    },
      {
      path: '/admin-dashboard',
      name: 'AdminDashboard',
      component: () => import('../components/AdminDashboard.vue'),
       meta: { requiresAuth: true, requiresAdmin: true }
    },
     {
      path: '/admin-product',
      name: 'AdminProducts',
      component: () => import('../components/AdminProduct.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/unauthorized',
      name: 'Unauthorized',
      component: Unauthorized
    }

    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue'),
    // },
  ],
  
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (!userStore.isLoggedIn) {
    userStore.loadFromStorage()
  }

  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)

  if (requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (requiresAdmin && userStore.role !== 'admin') {
    next('/unauthorized')
  } else {
    next()
  }
})



export default router
