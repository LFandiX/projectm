<template>
   
  <div class="flex flex-col items-center justify-center my-15 bg-white">
    <div class="w-full max-w-sm p-6 bg-white rounded shadow-md">
      <label class="block text-sm font-medium text-gray-700 mb-1">Your Email</label>
      <input
        v-model="email"
        type="email"
        placeholder="you@example.com"
        class="w-full px-4 py-2 mb-3 border rounded"
      />

      <label class="block text-sm font-medium text-gray-700 mb-1">Your Name</label>
      <input
        v-model="name"
        type="text"
        placeholder="e.g. John Doe"
        class="w-full px-4 py-2 mb-3 border rounded"
      />

      <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
      <input
        v-model="password"
        type="password"
        class="w-full px-4 py-2 mb-3 border rounded"
      />

      <label class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
      <input
        v-model="confirmPassword"
        type="password"
        class="w-full px-4 py-2 mb-3 border rounded"
      />

      <!-- Error -->
      <div v-if="errorMsg" class="w-full p-3 mb-4 text-sm text-red-700 bg-red-100 border border-red-300 rounded">
        {{ errorMsg }}
      </div>

      <button
        @click="handleSignUp"
        class="w-full bg-yellow-400 hover:bg-yellow-500 text-white font-semibold py-2 px-4 rounded"
      >
        Sign up
      </button>

      <div class="mt-4 text-center text-sm text-gray-600">
        <router-link to="/login" class="text-yellow-500 hover:underline">Already have an account?</router-link>
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
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
onMounted(() => {
  document.title = 'Sign Up - Sekolah Palembang Harapan Merch'
  fetchUsers()
})
const router = useRouter()

const email = ref('')
const name = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMsg = ref('')


// Simulasi data dari database
let existingUsers = [
  { id: 1, nama: 'John', email: 'jjj@gmail.com', password: 'ssss', role: 'user' }
]

// Fungsi validasi email
const isValidEmail = (emailStr) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(emailStr)
}
const fetchUsers = async () => {
  const res = await axios.get('http://127.0.0.1:5000/users')
  existingUsers = res.data
  console.log('Fetched users:', existingUsers)
  return 
}
const handleSignUp = async () => {
  errorMsg.value = ''

  if (!email.value || !name.value || !password.value || !confirmPassword.value) {
    errorMsg.value = 'Please fill in all fields.'
    return
  }

  if (!isValidEmail(email.value)) {
    errorMsg.value = 'Invalid email format.'
    return
  }

  const isEmailTaken = existingUsers.some(user => user.email === email.value)
  if (isEmailTaken) {
    errorMsg.value = 'Email is already registered.'
    return
  }

  if (password.value !== confirmPassword.value) {
    errorMsg.value = 'Passwords do not match.'
    return
  }


  try {
    const response = await axios.post('http://127.0.0.1:5000/createusers', {
    name: name.value,
    email: email.value,
    password: password.value
  })

    console.log('New user created:', response.data)
  } catch (error) {
    console.error('Error creating user:', error)
    errorMsg.value = 'Failed to create user. Please try again later.'
    return
  }
  
  // Simulasi register berhasil
  console.log('User registered:', { name: name.value, email: email.value })

  // Redirect ke login
  router.push('/login')
}
</script>
