<template>
 <div class="flex flex-col items-center justify-center my-15 bg-white">
 
    <div class="w-full max-w-sm p-6 bg-white rounded shadow-md">
      <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
      <input
        v-model="email"
        type="email"
        placeholder="you@example.com"
        class="w-full px-4 py-2 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-yellow-400"
      />

      <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
      <input
        v-model="password"
        type="password"
        placeholder="••••••••"
        class="w-full px-4 py-2 mb-2 border rounded focus:outline-none focus:ring-2 focus:ring-yellow-400"
      />

      <!-- Error Box -->
      <div v-if="loginError" class="w-full p-3 mb-4 text-sm text-red-700 bg-red-100 border border-red-300 rounded">
        Wrong login/password
      </div>

      <button
        @click="handleLogin"
        class="w-full bg-yellow-400 hover:bg-yellow-500 text-white font-semibold py-2 px-4 rounded"
      >
        Log in
      </button>

      <div class="mt-4 text-center text-sm text-gray-600">
        <router-link to="/signin" class="text-yellow-500 hover:underline mr-4">Don't have an account?</router-link>
        <router-link to="/resetpassword" class="text-yellow-500 hover:underline">Reset Password</router-link>
      </div>
    </div>
  </div>
<footer class="bg-[#bfb3a2] text-gray-800 py-16">
  <div class="max-w-6xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-10 text-sm">
    
    <!-- Useful Links -->
    <div>
  <h3 class="text-lg font-semibold mb-4">Useful Links</h3>
  <ul class="space-y-2 text-[#594424] font-medium">
    <li><router-link to="/" class="hover:underline">Home</router-link></li>
    <li><router-link to="/shop" class="hover:underline">Products</router-link></li>
    <li><router-link to="/privacy" class="hover:underline">Privacy Policy</router-link></li>
    <li><router-link to="/contactus" class="hover:underline">Contact us</router-link></li>
  </ul>
</div>

    <!-- About Us -->
    <div>
      <h3 class="text-lg font-semibold mb-4">About us</h3>
      <p class="text-justify leading-relaxed text-gray-700">
        Kami adalah OSIS sebagai perwakilan dari sekolah untuk menjual barang-barang yang dapat kalian beli.
        Kami merancang seluruh produk dengan penuh kasih agar dapat digunakan dengan baik, nyaman, dan bermanfaat bagi seluruh siswa/i Sekolah Palembang Harapan.
      </p>
    </div>

    <!-- Connect With Us -->
    <div>
      <h3 class="text-lg font-semibold mb-4">Connect with us</h3>
      <ul class="space-y-3 text-[#594424] font-medium">
        <li class="flex items-center gap-2">
          💬 <a href="#" class="hover:underline">Contact us by Teams</a>
        </li>
        <li class="flex items-center gap-2">
          ✉️ <a href="mailto:osismerchandise@gmail.com" class="hover:underline">osismerchandise@gmail.com</a>
        </li>
        <li class="flex items-center gap-2">
          📞 Call us on Teams
        </li>
      </ul>
    </div>
  </div>

  <!-- Footer Bottom -->
  <div class="mt-16 text-center text-xs text-gray-700 border-t border-gray-400 pt-4">
    <p>Copyright © Sekolah Palembang Harapan Merch</p>
    <!-- <p class="mt-1">Powered by <span class="font-semibold text-[#594424]">odoo</span> - The #1 Open Source eCommerce</p> -->
  </div>
</footer>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '@/stores/userStore';


const store = useUserStore()
const router = useRouter()
const route = useRoute()

const email = ref('')
const password = ref('')
const loginError = ref(false)

const handleLogin = async () => {
  // Simulasi login
  
  try {
    console.log('Attempting to login with:', email.value, password.value);
    const res = await axios.post('http://127.0.0.1:5000/login', {
        username: email.value,
        password: password.value
    });
    const data = res.data;
    console.log('Login response:', data);
    console.log('Login response:', data.message);
    if (data.message === 'Login successful') {
      loginError.value = false;
      let res2 = await axios.get(`http://127.0.0.1:5000/getbasket/${data.user.id}`);
      store.login({
        user_id: data.user.id,
        role: data.user.role,
        name: data.user.name,
        basket: res2.data
      });
      if  (data.user.role === 'admin') {
        const redirectTo = '/admin-dashboard';
        router.push(redirectTo);
      } else {
        const redirectTo =  '/';
        router.push(redirectTo);
      }
      
    } 
  } catch (error) {
    console.error('Login failed:', error);
    loginError.value = true;
  }

}
</script>

<style scoped>
input {
  background-color: #edf2ff;
}
</style>
