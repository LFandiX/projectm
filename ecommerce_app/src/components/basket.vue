<template>
  <div class="max-w-4xl mx-auto px-4 py-10">
    <h1 class="text-2xl font-semibold mb-6">Keranjang Anda</h1>

    <div v-if="(basketItems.length > 0) && (userId !== null)" class="space-y-4">
      <div v-for="item in basketItems" :key="item.id" class="flex items-center justify-between border rounded-md p-4">
        <div class="flex items-center gap-4">
          <img :src="getImageUrl(item.image)" alt="Product Image" class="w-16 h-16 object-cover rounded-md" />
          <div>
            <div class="font-medium">{{ item.nama }}</div>
            <div class="text-sm text-gray-500">Quantity: {{ item.quantity }}</div>
          </div>
        </div>
        <div class="flex gap-2">
          <button @click="checkout(item.product_id, item.quantity, item.id)" class="bg-yellow-400 text-white px-4 py-2 rounded hover:bg-yellow-700">Checkout</button>
          <!-- <router-link to="/shop/address" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            Checkout
          </router-link> -->
          <button @click="deleteItem(item.id)" class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
            Hapus
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-gray-500 text-center">
      <div v-if="userId === null">
        Silakan login untuk melihat Keranjang.
      </div>
      <div v-else>
        Keranjang Anda kosong.
      </div>
    </div>
  </div>
</template>


<script>
import { useUserStore } from '@/stores/userStore';
import axios from 'axios';
export default {
  data() {
    return {
      userId: null, // Simulasi user ID, ganti dengan ID dari session atau login state
      // Simulasi hasil dari JOIN query: basket JOIN products
      basketItems: [
      ]
    };
  },
   computed: {
    store() {
      return useUserStore();
    }
  },
  mounted() {
    // Simulasi pengambilan data dari API atau store
    
 
    this.fetchBasketItems();

  },
  methods: {
    getImageUrl(fileName) {
        return `http://localhost:5000/image/${fileName}`;
      },
    async fetchBasketItems() {
      try {
 
      this.userId = this.store.user_id;
        const response = await axios.get(`http://127.0.0.1:5000/basket/${this.userId}`);
        this.basketItems = response.data;
        console.log("API response:", response.data);
        const res2 = await axios.get(`http://127.0.0.1:5000/getbasket/${this.userId}`);
        this.store.updateBasket(res2.data);

      } catch (error) {
        console.error("Error fetching basket items:", error);
      }
    },
    
  async deleteItem(itemId) {
    if (confirm('Yakin ingin menghapus item ini dari keranjang?')) {
      try {
        await axios.delete(`http://127.0.0.1:5000/basket/${itemId}`);
        // Refresh basket items
        this.fetchBasketItems();
      } catch (error) {
        console.error("Error deleting item:", error);
        alert("Gagal menghapus item. Silakan coba lagi.");
      }
    }
  },
  checkout(productid, quantity, basketid) {
      const payload = {
        productId: productid,
        quantity: quantity || 1,
        basket: basketid
      };
      localStorage.setItem("checkoutData", JSON.stringify(payload));
      this.$router.push({
        path: "/shop/address",
        state: payload,
      });
    },
  }
};
</script>

<style scoped>
</style>
