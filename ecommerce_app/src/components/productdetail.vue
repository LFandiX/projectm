<template>
  <div class="container min-h-screen px-4 py-8" v-if="product">
    <!-- Breadcrumb -->
    <div class="text-sm text-gray-600 mb-4">
      <router-link to="/shop" class="hover:underline text-yellow-600">All Products</router-link>
      <span> / </span>
      <span>{{ product.nama }}</span>
    </div>

    <div class="flex flex-col lg:flex-row gap-8">
      <!-- Product Images -->
      <div class="flex flex-col items-center lg:w-1/2">
        <img :src="getImageUrl(product.image)" alt="product" class="w-96 h-auto rounded-lg shadow-md mb-4" />
      </div>

      <!-- Product Info -->
      <div class="lg:w-1/2">
        <h1 class="text-3xl font-bold mb-4">{{ product.nama }}</h1>
        <div class="text-gray-700 mb-4 whitespace-pre-line">{{ product.deskripsi }}</div>
        <p class="text-2xl font-semibold text-black mb-4">Rp {{ formatRupiah(product.harga) }}</p>

        <!-- Quantity and Buttons -->
        <div class="flex items-center space-x-2 mb-4">
          <button @click="decreaseQty" class="w-10 h-10 border rounded text-lg">-</button>
          <span class="w-10 text-center">{{ quantity }}</span>
          <button @click="increaseQty" class="w-10 h-10 border rounded text-lg">+</button>
        </div>

        <div class="flex space-x-4 mb-4">
          <button @click="addToCart"
            class="flex items-center space-x-2 bg-yellow-500 hover:bg-yellow-600 text-white font-bold px-4 py-2 rounded">
            <span class="material-icons">🛒</span>
            <span>ADD TO CART</span>
          </button>

          <button @click="buyNow"
            class="flex items-center space-x-2 border border-yellow-500 text-yellow-600 hover:bg-yellow-100 font-bold px-4 py-2 rounded">
            <span class="material-icons">⚡</span>
            <span>BUY NOW</span>
          </button>
        </div>

        <router-link to="/terms-and-condition" class="text-sm text-gray-600 hover:underline">
          Terms and Conditions
        </router-link>
      </div>
    </div>
  </div>

  <div v-else class="text-center text-gray-500 py-8">Product Not Found</div>

  <footer class="bg-[#bfb3a2] text-gray-800 py-16">
          

            <!-- Footer Bottom -->
            <div class="mt-16 text-center text-xs text-gray-700 border-t border-gray-400 pt-4">
                <p>Copyright © Sekolah Palembang Harapan Merch</p>
                <!-- <p class="mt-1">Powered by <span class="font-semibold text-[#594424]">odoo</span> - The #1 Open Source eCommerce</p> -->
            </div>
        </footer>
</template>

<script>
import axios from "axios";
import { useUserStore } from "@/stores/userStore";

export default {
  data() {
    return {
      product: null,
      quantity: 1,
      userId: null,
      errorMsg: null // Simulasi user ID, ganti dengan ID dari session atau login state
    };
  },
  mounted() {
    this.fetchProduct();
  },
  computed: {
    store() {
      return useUserStore();
    },
  },
  methods: {
    async fetchProduct() {

      this.userId = this.store.user_id;
      const id = Number(this.$route.params.id);
      try {
        const res = await axios.get("http://127.0.0.1:5000/products");
        const products = res.data;
        this.product = products.find(
          (item) => item.id === id && item.status === "Publish"
        );
      } catch (error) {
        console.error("Failed to fetch product:", error);
      }
    },
    increaseQty() {
      this.quantity++;
    },
    decreaseQty() {
      if (this.quantity > 1) this.quantity--;
    },
    formatRupiah(value) {
      return new Intl.NumberFormat("id-ID").format(value);
    },
    getImageUrl(fileName) {
      return `http://localhost:5000/image/${fileName}`;
    },
    async addToCart() {
      if (this.userId === null) {
        this.$router.push({ path: "/login" });
        return;
      }
      console.log("Adding to cart:", this.product.id, this.quantity, this.userId);
      try {
        const response = await axios.post('http://127.0.0.1:5000/basket', {
          user_id: this.userId,
          product_id: this.product.id,
          quantity: this.quantity
        })

        console.log('Item added to basket:', response.data)
        const res2 = await axios.get(`http://127.0.0.1:5000/getbasket/${this.userId}`);
        this.store.updateBasket(res2.data);
      } catch (error) {
        console.error('Error adding to basket:', error)
        this.errorMsg = 'Failed to add to basket. Please try again later.'
        return
      }
    },
    buyNow() {
      if (this.userId === null) {
        this.$router.push({ path: "/login" });
        return;
      }
      const payload = {
        productId: this.product.id,
        quantity: this.quantity || 1,
        basket: null
      };
      localStorage.setItem("checkoutData", JSON.stringify(payload));
      this.$router.push({
        path: "/shop/address",
        state: payload,
      });
    },
  },
};
</script>
