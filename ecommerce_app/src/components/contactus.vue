<template>
  <section class="max-w-5xl mx-auto px-6 py-12">
    <h1 class="text-5xl font-bold mb-8">Contact us</h1>
    <p class="mb-8 max-w-2xl">
      Contact us about anything related to our company or services.
      We'll do our best to get back to you as soon as possible.
    </p>

    <div class="grid md:grid-cols-3 gap-8">
      <!-- FORM -->
      <form @submit.prevent="handleSubmit" class="md:col-span-2 space-y-4">
        <BaseInput label="Name *" v-model="form.name" required />
        <BaseInput label="Email *" v-model="form.email" type="email" required />
        <BaseInput label="Subject *" v-model="form.subject" required />
        <BaseTextarea label="Message" v-model="form.message" rows="4" />

        <button
          type="submit"
          class="px-8 py-2 bg-yellow-500 hover:bg-yellow-600 text-white rounded disabled:opacity-50"
          :disabled="sending"
        >
          {{ sending ? 'Sending…' : 'Submit' }}
        </button>

        <p v-if="statusMsg" :class="statusClass" class="mt-2 text-sm">
          {{ statusMsg }}
        </p>
      </form>

      <!-- INFO -->
      <aside>
        <div class="pt-10">
        <p class="font-semibold mb-2">Our Store</p>
        <p class="flex items-center"><span class="mr-2">📍</span>Sekolah Palembang Harapan</p>
        <p class="flex items-center"><span class="mr-2">📧</span>osismerchandise@gmail.com</p>
      </div>
      </aside>
    </div>
  </section>
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
import { reactive, ref, computed } from 'vue'
import emailjs from '@emailjs/browser'

// Form state
const form = reactive({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const sending = ref(false)
const statusMsg = ref('')
const statusClass = computed(() =>
  statusMsg.value.startsWith('Thank') ? 'text-green-600' : 'text-red-600'
)

// EmailJS config
const SERVICE_ID = 'service_zk0bkph'
const TEMPLATE_ID = 'template_ytvgbix'
const PUBLIC_KEY = 'IYCHNCoClq6NnpZlZ'

const handleSubmit = async () => {
  sending.value = true
  statusMsg.value = ''

  if (!form.name || !form.email || !form.subject) {
    statusMsg.value = 'Please fill all required fields.'
    sending.value = false
    return
  }

  try {
    await emailjs.send(
      SERVICE_ID,
      TEMPLATE_ID,
      {
        from_name: form.name,
        from_email: form.email,
        subject: form.subject,
        message: form.message
      },
      PUBLIC_KEY
    )
    statusMsg.value = 'Thank you! Your message has been sent.'
    Object.keys(form).forEach(k => (form[k] = ''))
  } catch (e) {
    console.error('EmailJS error:', e)
    statusMsg.value = 'Failed to send. Please try again later.'
  } finally {
    sending.value = false
  }
}

// Base input components
const BaseInput = {
  props: { modelValue: String, label: String, type: { default: 'text' }, required: Boolean },
  emits: ['update:modelValue'],
  template: `
    <div>
      <label class="block mb-1 font-medium">{{ label }}</label>
      <input
        :type="type"
        :required="required"
        v-bind="$attrs"
        class="w-full border rounded px-3 py-2"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
      />
    </div>`
}

const BaseTextarea = {
  props: { modelValue: String, label: String, rows: { default: 3 } },
  emits: ['update:modelValue'],
  template: `
    <div>
      <label class="block mb-1 font-medium">{{ label }}</label>
      <textarea
        :rows="rows"
        class="w-full border rounded px-3 py-2"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
      ></textarea>
    </div>`
}

</script>

