<template>
  <div class="max-w-6xl mx-auto px-6 py-10">
    <!-- Step Indicator -->
    <div class="flex justify-between items-center mb-10">
      <div class="flex items-center space-x-2">
        <div class="text-green-500">✔</div>
        <div class="font-semibold text-green-500">Review Order</div>
      </div>
      <div class="flex items-center space-x-2">
        <div class="text-green-500">✔</div>
        <div class="font-semibold text-green-500">Address</div>
      </div>
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
        <div class="font-semibold text-gray-700">Confirm Order</div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
      <!-- Left Side -->
      <div class="md:col-span-2 space-y-6">
        <!-- Billing & Shipping Info -->
        <div class="border p-4 rounded-md shadow-sm">
          <div class="font-semibold mb-1">Billing & Shipping:</div>
          <div>{{ billingText }}</div>
          <!-- Tombol Edit Dihapus -->
        </div>

        <!-- Payment Method -->
        <div class="border p-4 rounded-md shadow-sm">
          <div class="font-semibold mb-2">Pay with</div>
          <div class="space-y-2">
            <label class="flex items-center gap-2">
              <input type="radio" value="Tunai" v-model="paymentMethod" /> Tunai
            </label>
            <label class="flex items-center gap-2">
              <input type="radio" value="Transfer" v-model="paymentMethod" /> Transfer
            </label>
          </div>
        </div>

        <!-- Buttons -->
        <div class="flex justify-between mt-6">
          <button @click="goBack" class="bg-gray-600 text-white px-4 py-2 rounded-md">
            Return to Cart
          </button>
          <button @click="submitPayment" class="bg-yellow-400 text-white px-4 py-2 rounded-md flex items-center gap-1">
            🔄 Pay Now
          </button>
        </div>
      </div>

      <!-- Order Summary -->
      <div class="border rounded-md shadow-sm p-4 text-sm space-y-4">
        <div class="font-semibold text-lg border-b pb-2">Confirm Order</div>
        <div class="flex items-center gap-2">
          <img :src="getImageUrl(product.image)" class="w-12 h-12 object-cover" />
          <div>
            <div class="font-semibold">{{ product.nama }}</div>
            <div class="text-xs text-gray-500">x{{ quantity }}</div>
          </div>
        </div>

        <div class="space-y-1 border-t pt-2">
          <div class="flex justify-between">
            <span>Subtotal:</span>
            <span>Rp {{ formatCurrency(this.total) }}</span>
          </div>
          <div class="flex justify-between">
            <span>Discount:</span>
            <span>Rp {{ formatCurrency(discount) }}</span>
          </div>
          <div class="flex justify-between font-semibold border-t pt-2">
            <span>Total:</span>
            <span>Rp {{ formatCurrency(productTotal) }}</span>
          </div>
          <!-- Voucher Toggle -->
          <div v-if=" !showVoucherInput" @click="showVoucherInput = !showVoucherInput"
            class="text-yellow-600 text-sm mt-2 cursor-pointer hover:underline">
            Discount code or gift card
          </div>

          <!-- Voucher Input -->
          <div v-if="showVoucherInput && voucherStatus !== 'applied'" class="mt-2 space-y-1">
            <div class="flex justify-between"><input v-model="voucherCode" placeholder="Enter voucher code"
              class="w-full px-3 py-1 border rounded-md text-sm" />
            <button @click="applyVoucher" class="bg-yellow-400 text-white px-3 py-1 rounded-md text-sm">
              Apply
            </button></div></div>
            <div v-if="voucherStatus === 'applied'" class="text-green-600 text-sm">Voucher Applied</div>
            <div v-else-if="voucherStatus === 'wrong'" class="text-red-600 text-sm">Wrong Voucher Code!</div>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from '@/stores/userStore';
export default {
  data() {
    return {
      form: {},
      product: {},
      productId: null,
      quantity: 1,
      total: 0,
      paymentMethod: "Tunai",
      basket_id: null,
      voucher: 0,
      voucher_Value: 0,
      errorMsg: "",
      user_id: null,
      showVoucherInput: false,
  voucherCode: "",
  voucherStatus: "", // 'applied', 'wrong', ''

    };
  },
  computed: {
    productTotal() {
      return this.total - this.discount;
    },
    discount() {
      return this.total * this.voucher_Value;
    },
    billingText() {
      return `${this.form.name}, ${this.form.class}, ${this.form.email}, ${this.form.userStatus}`;
    },
    store() {
      return useUserStore();
    }
  },
  mounted() {
    const state = JSON.parse(localStorage.getItem("checkoutData") || "{}");
    this.form = state.form || {};
    this.productId = state.productId;
    this.quantity = state.quantity || 1;
    this.total = state.total || 0;
    this.product = state.product || {};
    this.basket_id = state.basket;

    this.store.loadFromStorage();
    this.user_id = this.store.user_id;


  },
  methods: {
    goBack() {
      this.$router.push("/shop/address");
    },
    async submitPayment() {
      localStorage.removeItem("checkoutData");

      try {
        const response = await axios.post('http://127.0.0.1:5000/history', {
        user_id: this.user_id,
        product_id: this.productId,
        quantity: this.quantity,
        total_price: this.productTotal,
        payment_method: this.paymentMethod,
        kelas: this.form.class,
        voucher_id: this.voucher,
        note: this.form.note || ""
      })

        console.log('Item Purchased', response.data)
      } catch (error) {
        console.error('Error Purchased item', error)
        errorMsg.value = 'Failed to purchased item. Please try again later.'
        return
      }

      // Simpan data ke localStorage
      const payload = {
        paymentMethod: this.paymentMethod,
        product: this.product,
        productId: this.product.id,
        quantity: this.quantity,
        total: this.productTotal
      };

      localStorage.setItem("finalPaymentData", JSON.stringify(payload));

      let res = axios.delete(`http://127.0.0.1:5000/basket/${this.basket_id}`);
      res.then(() => {
        console.log("Basket deleted successfully");
      }).catch(error => {
        console.error("Error deleting basket:", error);
      });

      const res2 = await axios.get(`http://127.0.0.1:5000/getbasket/${this.user_id}`);
        this.store.updateBasket(res2.data);

      this.$router.push({
        path: "/paymentdetail",
        state: { paymentMethod: this.paymentMethod }
      });
    },
    applyVoucher() {
      if (this.voucherCode.trim().toUpperCase() === "DS2025") {
        this.voucher = 1;
        this.voucher_Value = 0.3;
        this.voucherStatus = 'applied';
      } else {
        this.voucher = 0;
        this.voucher_Value = 0;
        this.voucherStatus = 'wrong';
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
    }
  }
};
</script>

<style scoped>
input[type="radio"]:checked {
  accent-color: #facc15;
  /* yellow-400 */
}
</style>
