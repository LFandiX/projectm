<template>
  <div class="min-h-screen flex flex-col">

    <!-- Hero Section -->
    <div class="relative h-[90vh] w-full">
      <!-- Background image -->
      <img src="@/assets/hero.png " alt="Hero" class="absolute top-0 left-0 w-full h-full object-cover" />

      <!-- Overlay text -->

      <div
        class="absolute top-0 left-0 w-full h-full flex flex-col justify-center items-center text-white bg-[rgba(35,55,74,0.6)] px-4">
        <h1 class="text-4xl md:text-6xl font-bold mb-2 text-center">WELCOME TO SPH MERCH</h1>
        <p class="text-md md:text-lg mb-6 text-center">Powered by Student Council Sekolah Palembang Harapan</p>
        <router-link to="/shop" class="bg-yellow-500 text-black font-semibold px-6 py-3 rounded hover:bg-yellow-600">
          Shop Now!
        </router-link>
      </div>
    </div>
    <!-- Contact Section -->
    <section class="bg-[#ecb25d] py-20 relative overflow-hidden">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-10">
          Would you like more information about a product?
        </h2>
        <router-link to="/contactus"
          class="bg-white text-[#ecb25d] hover:bg-[#f5d08a] hover:text-black font-semibold py-3 mb-12 px-6 rounded-lg shadow transition duration-300">
          Contact Us
        </router-link>

      </div>

      <!-- Wave Effect -->
      <div class="absolute bottom-0 left-0 w-full overflow-hidden leading-[0]">
        <svg class="relative block w-[100%] h-15" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"
          viewBox="0 0 2000 100">
          <path d="M0,0 C300,50 700,0 1000,30 C1300,60 1700,10 2000,30 L2000,100 L0,100 Z" fill="#bfb3a2"></path>
        </svg>
      </div>
    </section>

    <!-- Footer -->
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
            Kami merancang seluruh produk dengan penuh kasih agar dapat digunakan dengan baik, nyaman, dan bermanfaat
            bagi seluruh siswa/i Sekolah Palembang Harapan.
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

  </div>
</template>

<script>
export default {
  name: "HomeView",
  data() {
    return {};
  },
};
</script>
