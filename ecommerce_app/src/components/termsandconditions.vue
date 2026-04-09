<template>
  
  <div class="px-6 py-10 max-w-4xl mx-auto text-gray-800">
    <h1 class="text-3xl font-bold mb-6 text-yellow-500">Terms and Conditions</h1>

    <p class="mb-4">
      These Terms and Conditions govern your use of our website and services. By accessing or using our website, you
      agree to comply with these terms.
    </p>

    <section class="mb-6">
      <h2 class="text-xl font-semibold mb-2">1. Acceptance of Terms</h2>
      <p>
        By using our website, you confirm that you accept these Terms and Conditions in full. If you do not agree with
        these terms, you must not use our website.
      </p>
    </section>

    <section class="mb-6">
      <h2 class="text-xl font-semibold mb-2">2. How We Use Your Information</h2>
      <p>
        We may use your personal information to:
      </p>
      <ul class="list-disc list-inside mt-2 space-y-1">
        <li>Provide and maintain our services</li>
        <li>Communicate with you about updates or promotions</li>
        <li>Improve our website and user experience</li>
      </ul>
    </section>

    <section class="mb-6">
      <h2 class="text-xl font-semibold mb-2">3. Sharing Your Information</h2>
      <p>
        We do not sell or rent your personal information to third parties. We may share it only with trusted service
        providers to help us operate our business, as required by law.
      </p>
    </section>

    <section class="mb-6">
      <h2 class="text-xl font-semibold mb-2">4. Cookies</h2>
      <p>
        We use cookies to enhance your browsing experience. You can choose to disable cookies through your browser
        settings.
      </p>
    </section>

    <section class="mb-6">
      <h2 class="text-xl font-semibold mb-2">5. Data Security</h2>
      <p>
        We implement reasonable security measures to protect your personal data. However, no method of transmission over
        the Internet is 100% secure.
      </p>
    </section>

    <section class="mb-6">
      <h2 class="text-xl font-semibold mb-2">6. Your Rights</h2>
      <p>
        You have the right to access, correct, or delete your personal information. To do so, please contact us using
        the information below.
      </p>
    </section>

    <section class="mb-6">
      <h2 class="text-xl font-semibold mb-2">7. Changes to This Policy</h2>
      <p>
        We may update this Privacy Policy from time to time. Any changes will be posted on this page with an updated
        revision date.
      </p>
    </section>

    <section class="mb-6">
      <h2 class="text-xl font-semibold mb-2">8. Contact Us</h2>
      <p>
        If you have any questions about this Privacy Policy, please contact us at
        <strong>osismerchandise@gmail.com</strong>.
      </p>
    </section>

    <p class="text-sm text-gray-500 mt-10">
      Last updated: May 2025
    </p>
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
          Kami merancang seluruh produk dengan penuh kasih agar dapat digunakan dengan baik, nyaman, dan bermanfaat bagi
          seluruh siswa/i Sekolah Palembang Harapan.
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

<script>
export default {
  name: "TermsAndConditions",
  data() {
    return {};
  },
};
</script>

<style scoped>
/* Tailwind is already assumed to be available */
</style>
