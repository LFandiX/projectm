<template>
  <div class="max-w-6xl mx-auto px-6 py-10">
    <h1 class="text-2xl font-semibold mb-6">Riwayat Pesanan</h1>

    <div v-if="(orders.length > 0) && (userId !== null)" class="space-y-4">
      <div
        v-for="order in orders"
        :key="order.id"
        class="border rounded-md p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4"
      >
        <div class="flex items-center gap-4">
          <img
            :src="getImageUrl(order.image)"
            alt="product"
            class="w-16 h-16 object-cover rounded-md"
          />
          <div>
            <div class="font-semibold">Order ID: {{ order.id }}</div>
            <div class="text-sm">{{ order.nama }}</div>
            <div class="text-sm text-gray-500">Qty: {{ order.quantity }}</div>
            <div class="text-sm text-gray-500">Total: Rp {{ formatCurrency(order.total_price) }}</div>
          </div>
        </div>
        <div class="text-right space-y-1">
          <div
            class="inline-block text-xs px-2 py-1 rounded-full"
            :class="statusClass(order.status)"
          >
            {{ order.status }}
          </div>
          <div class="text-sm">Metode: {{ formatMethod(order.payment_method) }}</div>
          <div class="text-sm text-gray-500">{{ formatDate(order.purchase_date) }}</div>
        </div>
      </div>
    </div>

    <div v-else class="text-center text-gray-500 mt-10">
      <div v-if="userId === null">
        Silakan login untuk melihat riwayat pesanan.
      </div>
      <div v-else>
        Belum ada riwayat pesanan.
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
      // Ganti null dengan user ID dari session atau login state
      userId: null,
      orders: [{
          id: 'S00023',
          product_name: 'Sticker SPH',
          product_image: 'sticker-sph.jpg',
          quantity: 1,
          total_price: 2000,
          status: 'pending',
          payment_method: 'cash',
          purchase_date: '2025-05-25T15:30:00'
        },
        {
          id: 'S00022',
          product_name: 'Notebook SPH',
          product_image: 'notebook.jpg',
          quantity: 2,
          total_price: 10000,
          status: 'completed',
          payment_method: 'bank_transfer',
          purchase_date: '2025-05-24T10:00:00'
        }] // Kosong untuk testing kondisi
    };
  },
  computed: {
    store() {
      return useUserStore();
    }
  },
  mounted() {
    // Simulasi pengambilan data dari API atau store
    this.fetchOrders();
    
 
  },
  methods: {
    async fetchOrders() {
      try {
        this.userId = this.store.user_id;
        const response = await axios.get(`http://127.0.0.1:5000/history/${this.userId}`);
        this.orders = response.data;
      }
      catch (error) {
        console.error("Error fetching orders:", error);
      }
    },

    getImageUrl(fileName) {
      return `http://localhost:5000/image/${fileName}`;
    },
    formatCurrency(value) {
      return value?.toLocaleString("id-ID", {
        style: "decimal",
        minimumFractionDigits: 2
      }) || "0,00";
    },
    formatDate(isoDate) {
      const date = new Date(isoDate);
      return date.toLocaleString("id-ID", {
        dateStyle: "medium",
        timeStyle: "short"
      });
    },
    formatMethod(method) {
      return method === "cash" ? "Tunai" : "Transfer Bank";
    },
    statusClass(status) {
      const classes = {
        pending: "bg-yellow-200 text-yellow-800",
        Paid: "bg-blue-200 text-blue-800",
        completed: "bg-green-200 text-green-800",
        cancelled: "bg-red-200 text-red-800"
      };
      return classes[status] || "bg-gray-200 text-gray-800";
    }
  }
};
</script>

<style scoped>
</style>
