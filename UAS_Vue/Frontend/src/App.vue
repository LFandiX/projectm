<script>
import Dashboard from './components/Dasboard.vue';

export default {
  name: 'App',
  components: {
    Dashboard,

  },
  methods: {
    handleLoginSuccess(payload) {
      console.log('Login berhasil untuk user:', payload.username)
      // Navigasi ke halaman dashboard setelah login sukses
      this.$router.push('/dashboard')
    },
  // },
  // components: {Dashboard}
}
}
</script>

<template>
  <!-- Menampilkan halaman berdasarkan route -->
  <div id="app">
    
    <router-view @login-success="handleLoginSuccess" />
  </div>
  <!-- <router-view/> -->
  <!-- <Dashboard/> -->
 
</template>


<style>
/* Gaya dasar untuk App */
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
  padding: 1rem;
} */
</style>
