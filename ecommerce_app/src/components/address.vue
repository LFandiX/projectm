<template>
  <div class="max-w-6xl mx-auto px-6 py-10">
    <!-- Step Indicator -->
    <div class="flex justify-between items-center mb-10">
      <div class="flex items-center space-x-2">
        <div class="text-green-500">✔</div>
        <div class="font-semibold text-green-500">Review Order</div>
      </div>
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
        <div class="font-semibold text-gray-700">Address</div>
      </div>
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 rounded-full border border-gray-400"></div>
        <div class="font-semibold text-gray-400">Confirm Order</div>
      </div>
    </div>

    <!-- Form & Summary -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
      <!-- Form -->
      <form class="space-y-4" @submit.prevent="goNext">
        <h2 class="text-3xl font-bold mb-4">Isi data Anda</h2>

        <div>
          <label class="block mb-1 font-semibold">Nama</label>
          <input v-model="form.name"
                 :class="['w-full border px-3 py-2 rounded-md', errors.name ? 'border-red-500' : '']" />
        </div>

        <div>
          <label class="block mb-1 font-semibold">Kelas</label>
          <input v-model="form.class"
                 :class="['w-full border px-3 py-2 rounded-md', errors.class ? 'border-red-500' : '']" />
        </div>

        <div>
          <label class="block mb-1 font-semibold">
            Email
            <span v-if="errors.email" class="text-red-500 text-sm">(Email tidak valid)</span>
          </label>
          <input v-model="form.email"
                 :class="['w-full border px-3 py-2 rounded-md', errors.email ? 'border-red-500' : '']" />
        </div>

        <div>
          <label class="block mb-1 font-semibold">Status Pengguna</label>
          <select v-model="form.userStatus"
                  :class="['w-full border px-3 py-2 rounded-md', errors.userStatus ? 'border-red-500' : '']">
            <option disabled value="">-- Pilih Status --</option>
            <option value="Siswa">Siswa</option>
            <option value="Orang Tua">Orang Tua</option>
            <option value="Guru">Guru</option>
          </select>
        </div>

        <div>
          <label class="block mb-1 font-semibold">Catatan (Note)</label>
          <textarea v-model="form.note"
                    rows="4"
                    class="w-full border px-3 py-2 rounded-md"
                    placeholder="Tambahkan catatan jika ada..."></textarea>
        </div>

        <!-- Buttons -->
        <div class="flex justify-between mt-8">
          <button @click="goBack" class="bg-gray-600 text-white py-2 px-4 rounded flex items-center gap-2">
            <span>&lt;</span> Back
          </button>
          <button type="submit" class="bg-yellow-400 text-white py-2 px-4 rounded flex items-center gap-2">
            Next <span>&gt;</span>
          </button>
        </div>
      </form>

      <!-- Order Summary -->
      <div>
        <table class="w-full border text-sm">
          <thead>
            <tr class="bg-gray-100">
              <th class="text-left p-2">Product</th>
              <th class="text-left p-2">Quantity</th>
              <th class="text-left p-2">Price</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="product">
              <td class="p-2 flex items-center space-x-2">
                <img :src="getImageUrl(product.image)" alt="product" class="w-12 h-12 object-cover" />
                <span>{{ product.nama }}</span>
              </td>
              <td class="p-2">{{ quantity }}</td>
              <td class="p-2">Rp {{ formatCurrency(product.harga) }}</td>
            </tr>
          </tbody>
        </table>

        <div class="border-t mt-4 pt-4 space-y-2">
          <div class="flex justify-between">
            <span>Subtotal:</span>
            <span>Rp {{ formatCurrency(productTotal) }}</span>
          </div>
          <div class="flex justify-between">
            <span>Discount:</span>
            <span>Rp 0.00</span>
          </div>
          <div class="flex justify-between font-semibold">
            <span>Total:</span>
            <span>Rp {{ formatCurrency(productTotal) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      product: null,
      quantity: 1,
      basketid: null,
      form: {
        name: "",
        class: "",
        email: "",
        userStatus: "",
        note: ""
      },
      errors: {
        name: false,
        class: false,
        email: false,
        userStatus: false
      },
      data: []
    };
  },
  computed: {
    productTotal() {
      return this.product ? this.product.harga * this.quantity : 0;
    }
  },
  mounted: async function () {
    await this.fetchdata(); // Pastikan data sudah dimuat sebelum lanjut
    const saved = JSON.parse(localStorage.getItem("checkoutData"));
    if (saved) {
      this.quantity = saved.quantity || 1;
      this.basketid = saved.basket
      const found = this.data.find(
        (p) => p.id === saved.productId && p.status === "Publish"
      );
      if (found) this.product = found;
    }
    localStorage.removeItem("checkoutData")
  },
  methods: {
    async fetchdata() {
      try {
        const res = await axios.get("http://localhost:5000/products");
        this.data = res.data;
      } catch (error) {
        console.error("Gagal mengambil data produk:", error);
      }
    },
    getImageUrl(fileName) {
      return `http://localhost:5000/image/${fileName}`;
    },
    formatCurrency(value) {
      return value.toLocaleString("id-ID", {
        style: "decimal",
        minimumFractionDigits: 2
      });
    },
    goBack() {
      if (this.product) {
        this.$router.push(`/shop/${this.product.id}`);
      }
    },
    goNext() {
      let valid = true;

      for (let key of ["name", "class", "email", "userStatus"]) {
        if (!this.form[key]?.trim()) {
          this.errors[key] = true;
          valid = false;
        } else {
          this.errors[key] = false;
        }
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.form.email)) {
        this.errors.email = true;
        valid = false;
      }

      if (!valid) return;

      const payload = {
        form: {
          name: this.form.name,
          class: this.form.class,
          email: this.form.email,
          userStatus: this.form.userStatus,
          note: this.form.note || ""
        },
        product: this.product,
        productId: this.product.id,
        quantity: this.quantity,
        total: this.productTotal,
        basket: this.basketid
      };

      localStorage.setItem("checkoutData", JSON.stringify(payload));

      this.$router.push("/shop/payment", {
        state: payload
      });
    }
  }
};
</script>

<style scoped>
input,
select,
textarea {
  outline: none;
}
</style>
