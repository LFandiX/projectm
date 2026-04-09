<template>
  <div class="max-w-6xl mx-auto px-6 py-10">
    <!-- Header -->
    <h1 class="text-3xl font-semibold mb-4">Pesanan anda telah ditambahkan dalam server!</h1>

    <!-- Payment Info -->
    <div class="bg-blue-100 p-4 rounded-md mb-6">
      <div class="text-lg font-semibold mb-2">Payment Information:</div>
      <div class="flex justify-between">
        <div>{{ paymentData.paymentMethod }}</div>
        <div>Total: <strong>Rp {{ formatCurrency(paymentData.total) }}</strong></div>
      </div>
    </div>

    <!-- Instruction Box -->
    <div class="bg-cyan-700 text-white p-6 rounded-md mb-6">
      <h2 class="text-xl font-bold mb-2">Please use the following details</h2>
      <p v-if="paymentData.paymentMethod === 'Tunai'" class="mb-4">
        Silahkan siapkan uang anda dan bayar ke toko fisik kami di Lt 4 gedung utama (402) agar pesanan anda dapat di proses!
        <br /><br />
        Silahkan bayar 48 Jam dari pemesanan! Apabila kami tidak menerima uang anda dalam waktu tersebut maka pesanan anda akan dibatalkan.
      </p>
      <p v-else class="mb-4">
        Silahkan transfer ke rekening BCA 1234567890 a/n Toko Online SPH. 
        Kirim bukti transfer ke email kami di pembayaran@sph.com dengan subjek: Pembayaran Order.
        <br /><br />
        Pembayaran harus dilakukan dalam waktu 48 Jam atau pesanan akan dibatalkan.
      </p>

      <div class="mt-2"><strong>Communication:</strong> {{ referenceCode }}</div>
    </div>

    <!-- Order Summary -->
    <div v-if="paymentData.product" class="border rounded-md p-4">
      <div class="font-semibold text-lg border-b pb-2 mb-2">Order Summary</div>
      <div class="flex items-center gap-2 mb-2">
        <img :src="getImageUrl(paymentData.product.image)" class="w-12 h-12 object-cover" />
        <div>
          <div class="font-semibold">{{ paymentData.product.nama }}</div>
          <div class="text-sm text-gray-500">x{{ paymentData.quantity }}</div>
        </div>
      </div>

      <div class="text-sm space-y-1 border-t pt-2">
        <div class="flex justify-between">
          <span>Subtotal:</span>
          <span>Rp {{ formatCurrency(paymentData.total) }}</span>
        </div>
        <div class="flex justify-between">
          <span>Taxes:</span>
          <span>Rp 0.00</span>
        </div>
        <div class="flex justify-between font-semibold border-t pt-2">
          <span>Total:</span>
          <span>Rp {{ formatCurrency(paymentData.total) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      paymentData: {},
      referenceCode: ""
    };
  },
  mounted() {
    const stored = JSON.parse(localStorage.getItem("finalPaymentData") || "{}");
    this.paymentData = stored;

    
    this.referenceCode = "S00002";
  },
  methods: {
    formatCurrency(value) {
      return value?.toLocaleString("id-ID", {
        style: "decimal",
        minimumFractionDigits: 2
      }) || "0,00";
    },
    getImageUrl(fileName) {
      return `http://localhost:5000/image/${fileName}`;
    }
  }
};
</script>

<style scoped>
</style>
