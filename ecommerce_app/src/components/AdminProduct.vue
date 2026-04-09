<template>
  <div class="min-h-screen bg-gray-900 text-white p-6 relative">
    <!-- Header -->
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Products</h1>
      <button
        @click="openAddForm"
        class="bg-blue-300 hover:bg-blue-400 text-black font-semibold py-2 px-4 rounded"
      >
        + Add Product
      </button>
    </div>

    <!-- Product Table -->
    <div class="bg-gray-800 rounded-lg overflow-hidden">
      <!-- Table Header -->
      <div class="grid grid-cols-[3fr_1fr_1fr] text-sm font-semibold text-gray-300 px-6 py-3 border-b border-gray-700">
        <div>Product</div>
        <div class="text-right">Price</div>
        <div class="text-right">Stock</div>
      </div>

      <!-- Product Rows -->
      <div
        v-for="item in products"
        :key="item.id"
        class="grid grid-cols-[3fr_1fr_1fr] items-center px-6 py-4 border-b border-gray-700 hover:bg-gray-700 transition"
      >
        <div class="flex gap-4 items-center">
          <img
            :src="item.image || '/placeholder.png'"
            alt="product image"
            class="w-16 h-16 rounded bg-gray-600 object-cover"
          />
          <div>
            <p class="font-semibold">{{ item.nama }}</p>
            <p class="text-gray-400 text-sm truncate max-w-xs">
              {{ item.deskripsi }}
            </p>
          </div>
        </div>

        <div class="text-right font-semibold text-white">
          {{ formatPrice(item.harga) }}
        </div>

        <div class="flex justify-end items-center gap-2 relative">
          <span
            class="px-3 py-1 rounded-full text-sm font-bold"
            :class="item.stock < 10 ? 'bg-red-500' : 'bg-blue-300 text-black'"
          >
            {{ item.stock }}
          </span>

          <!-- Dropdown -->
          <div class="relative">
            <button @click="toggleDropdown(item.id)" class="text-2xl px-2">⋮</button>
            <div
              v-if="dropdownOpen === item.id"
              class="absolute right-0 mt-2 w-32 bg-gray-800 border border-gray-600 rounded shadow-lg z-50"
            >
              <button
                @click="editProduct(item)"
                class="block w-full text-left px-4 py-2 hover:bg-blue-500"
              >
                Edit
              </button>
              <button
                @click="confirmDelete(item)"
                class="block w-full text-left px-4 py-2 text-red-500 hover:bg-gray-700"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sidebar Form -->
    <div
      class="fixed top-0 right-0 h-full w-96 bg-gray-800 text-white p-6 shadow-lg transition-transform duration-300"
      :class="{ 'translate-x-0': showForm, 'translate-x-full': !showForm }"
    >
      <div class="flex justify-between items-center mb-4">
        <div>
          <h2 class="text-lg font-semibold">
            {{ editMode ? 'Edit Product' : 'Add Product' }}
          </h2>
          <p class="text-sm text-gray-400">
            {{ editMode ? 'Edit product details below.' : 'Fill in the form to add a new product.' }}
          </p>
        </div>
        <button @click="closeForm" class="text-xl text-gray-300 hover:text-white">&times;</button>
      </div>

      <!-- FORM -->
      <form @submit.prevent="saveProduct" class="flex flex-col gap-4">
        <div>
          <label class="block mb-1 text-sm font-semibold">Product Name</label>
          <input
            v-model="form.nama"
            type="text"
            placeholder="e.g. Acoustic Guitar"
            class="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:outline-none focus:ring focus:ring-blue-400"
          />
        </div>

        <div>
          <label class="block mb-1 text-sm font-semibold">Description</label>
          <textarea
            v-model="form.deskripsi"
            placeholder="A short summary of the product..."
            class="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:outline-none focus:ring focus:ring-blue-400"
            rows="3"
          ></textarea>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block mb-1 text-sm font-semibold">Price</label>
            <input
              v-model.number="form.harga"
              type="number"
              class="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:outline-none focus:ring focus:ring-blue-400"
              min="0"
            />
          </div>
          <div>
            <label class="block mb-1 text-sm font-semibold">Stock Quantity</label>
            <input
              v-model.number="form.stock"
              type="number"
              class="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:outline-none focus:ring focus:ring-blue-400"
              min="0"
            />
          </div>
        </div>

        <div>
          <label class="block mb-1 text-sm font-semibold">Image URL</label>
          <input
            v-model="form.image"
            type="text"
            placeholder="https://..."
            class="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:outline-none focus:ring focus:ring-blue-400"
          />
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-3 mt-6">
          <button type="button" @click="closeForm" class="text-sm px-4 py-2 rounded border border-gray-500 text-gray-300 hover:bg-gray-700">
            Cancel
          </button>
          <button type="submit" class="text-sm px-4 py-2 rounded bg-blue-300 text-black font-semibold hover:bg-blue-400">
            {{ editMode ? 'Update Product' : 'Save Product' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-60 z-50"
    >
      <div class="bg-gray-800 text-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-2">Are you sure?</h2>
        <p class="text-sm text-gray-300 mb-6">
          This action cannot be undone. This will permanently delete the product
          <span class="font-semibold text-white">"{{ productToDelete?.nama }}"</span>.
        </p>
        <div class="flex justify-end gap-3">
          <button
            @click="cancelDelete"
            class="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600"
          >
            Cancel
          </button>
          <button
            @click="performDelete"
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const products = ref([
  {
    deskripsi: 'Hoodie ini memiliki bahan dengan kualitas terbaik agar dapat nyaman saat dikenakan.',
    harga: 250000,
    id: 1,
    image: 'hero.jpeg',
    nama: 'Hoodie SPH',
    status: 'Publish',
    stock: 0
  },
  {
    deskripsi: 'Keychain dengan desain logo SPH. Bahan akrilik berkualitas tinggi.',
    harga: 15000,
    id: 2,
    image: 'hero.png',
    nama: 'Keychain SPH',
    status: 'Publish',
    stock: 0
  },
  {
    deskripsi: 'Sticker karakter SPH lucu untuk dekorasi laptop dan buku.',
    harga: 2000,
    id: 3,
    image: 'hero.png',
    nama: 'Sticker SPH',
    status: 'Unpublish',
    stock: 0
  }
])

const showForm = ref(false)
const dropdownOpen = ref(null)
const editMode = ref(false)
const editedProductId = ref(null)

const form = ref({
  nama: '',
  deskripsi: '',
  harga: 0,
  stock: 0,
  image: ''
})

const showDeleteModal = ref(false)
const productToDelete = ref(null)

const openAddForm = () => {
  resetForm()
  editMode.value = false
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
  dropdownOpen.value = null
  resetForm()
  editMode.value = false
  editedProductId.value = null
}

const resetForm = () => {
  form.value = {
    nama: '',
    deskripsi: '',
    harga: 0,
    stock: 0,
    image: ''
  }
}

const saveProduct = () => {
  if (editMode.value) {
    const index = products.value.findIndex(p => p.id === editedProductId.value)
    if (index !== -1) {
      products.value[index] = {
        ...products.value[index],
        ...form.value
      }
    }
  } else {
    const newProduct = {
      ...form.value,
      id: Date.now(),
      status: 'Publish'
    }
    products.value.push(newProduct)
  }
  closeForm()
}

const toggleDropdown = (id) => {
  dropdownOpen.value = dropdownOpen.value === id ? null : id
}

const editProduct = (item) => {
  form.value = { ...item }
  editedProductId.value = item.id
  editMode.value = true
  showForm.value = true
  dropdownOpen.value = null
}

const confirmDelete = (item) => {
  productToDelete.value = item
  showDeleteModal.value = true
  dropdownOpen.value = null
}

const cancelDelete = () => {
  showDeleteModal.value = false
  productToDelete.value = null
}

const performDelete = () => {
  if (productToDelete.value) {
    products.value = products.value.filter(p => p.id !== productToDelete.value.id)
  }
  cancelDelete()
}

const formatPrice = (val) => {
  return 'Rp ' + val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.')
}
</script>
