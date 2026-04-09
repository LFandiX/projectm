// main.js
import './assets/style.css'
import { VueReCaptcha } from 'vue-recaptcha-v3'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// 1) Pinia dulu
const pinia = createPinia()
app.use(pinia)

// 2) Plugin lain (reCAPTCHA, dsb.)
app.use(VueReCaptcha, {
  siteKey: '6LcttUArAAAAAJWO1pgN0D5xRirK83Iz7oVB4VFO',
  loaderOptions: { autoHideBadge: true }
})

// 3) Terakhir router
app.use(router)

app.mount('#app')
