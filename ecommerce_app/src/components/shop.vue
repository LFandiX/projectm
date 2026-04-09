    <template>
        <div class="p-4 min-h-screen bg-[#f5f5f5]">
            <div class="flex flex-col md:flex-row gap-4 mb-6">
                <!-- Filter Sidebar -->
                <div class="w-full md:w-1/4">
                    <h2 class="font-bold text-lg mb-2">Price Range</h2>
                    <input type="range" :min="2000" :max="maxPrice" step="1000" v-model="priceRange"
                        class="w-full mb-2 accent-yellow-500" />
                    <div class="text-sm text-gray-600">
                        Rp {{ formatRupiah(2000) }} - Rp {{ formatRupiah(priceRange) }}
                    </div>
                </div>

                <!-- Shop Items -->
                <div class="w-full md:w-3/4">
                    <div class="flex justify-between mb-4">
                        <input v-model="search" placeholder="Search..." class="border px-4 py-2 rounded w-1/2" />
                        <select v-model="sortBy" class="border px-2 py-2 rounded">
                            <option value="featured">Featured</option>
                            <option value="lowest">Lowest Price</option>
                            <option value="highest">Highest Price</option>
                        </select>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                        <div v-if="filteredItems.length === 0" class="text-center text-gray-500 col-span-full">
                            No Product Defined
                        </div>
                        <div v-for="item in filteredItems" :key="item.id"
                            class="border rounded-lg shadow hover:shadow-md transition cursor-pointer"
                            @click="$router.push(`/shop/${item.id}`)">

                            <img :src="getImageUrl(item.image)" alt="product"
                                class="w-full h-48 object-cover rounded-t-lg" />
                            <div class="p-4">
                                <h3 class="font-semibold text-lg">{{ item.nama }}</h3>
                                <p class="text-sm text-gray-600 mb-2">Rp {{ formatRupiah(item.harga) }}</p>
                                <p class="text-xs text-gray-500 line-clamp-3 whitespace-pre-line">{{ item.deskripsi }}
                                </p>
                            </div>
                        </div>
                    </div>
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
                        Kami adalah OSIS sebagai perwakilan dari sekolah untuk menjual barang-barang yang dapat kalian
                        beli.
                        Kami merancang seluruh produk dengan penuh kasih agar dapat digunakan dengan baik, nyaman, dan
                        bermanfaat bagi seluruh siswa/i Sekolah Palembang Harapan.
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
                            ✉️ <a href="mailto:osismerchandise@gmail.com"
                                class="hover:underline">osismerchandise@gmail.com</a>
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

import axios from 'axios';

export default {
    data() {
        return {
            search: "",
            sortBy: "featured",
            data: [],
            priceRange: 0,
        };
    },
    computed: {
        maxPrice() {
            const published = this.data.filter(item => item.status === "Publish");
            return Math.max(...published.map(item => item.harga));
        },
        filteredItems() {
            let items = this.data.filter((item) => item.status === "Publish");

            items = items.filter((item) => item.harga <= this.priceRange);

            if (this.search.trim() !== "") {
                const term = this.search.toLowerCase();
                items = items.filter((item) => item.nama.toLowerCase().includes(term));
            }

            if (this.sortBy === "lowest") {
                items.sort((a, b) => a.harga - b.harga);
            } else if (this.sortBy === "highest") {
                items.sort((a, b) => b.harga - a.harga);
            }

            return items;
        }
    },
    mounted() {

        this.fetchData();

    },
    methods: {
        formatRupiah(value) {
            return value.toLocaleString("id-ID");
        },
        async fetchData() {
            try {
                const res = await axios.get('http://127.0.0.1:5000/products');
                this.data = res.data;
                this.priceRange = this.maxPrice;  // ← atur ulang setelah data di-set
                console.log("Data fetched successfully:", res.data);
                console.log("Filtered items:", this.filteredItems);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        },

        getImageUrl(fileName) {
            return `http://localhost:5000/image/${fileName}`;
            // return new URL(`../assets/${fileName}`, import.meta.url).href;
        },
    }
};
</script>

<style scoped>
.line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>
