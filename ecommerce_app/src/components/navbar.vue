<template>
  <header v-if="userRole == 'user' || userRole == 'guest'" class="bg-white shadow-md relative z-30">
    <!-- Desktop Navbar -->
    <nav class="hidden lg:flex justify-between items-center px-8 py-4 bg-white">
      <!-- Left Menu -->
      <div class="flex space-x-6 text-gray-700 font-semibold">
        <router-link to="/" class="hover:text-yellow-500" exact>Home</router-link>
        <router-link to="/shop" class="hover:text-yellow-500">Shop</router-link>
        <router-link to="/history" class="hover:text-yellow-500">History</router-link>
      </div>

      <!-- Logo -->
      <div>
        <img src="@/assets/osismerch.jpg" alt="Logo" class="h-10 w-auto" />
      </div>

      <!-- Right Menu -->
      <div class="flex items-center space-x-4 relative">
        <router-link to="/basket" class="text-gray-700 hover:text-yellow-500 flex items-center">
          <span class="text-xl">🛒</span>
          <span class="ml-1">{{ basketCount }}</span>
        </router-link>

        <!-- Login State -->
        <div v-if="isLoggedIn" class="relative">
          <button @click="toggleDropdown" class="text-gray-700 hover:text-yellow-500 text-2xl focus:outline-none">
            <i class="fas fa-user-circle text-xl">{{ userName }}</i>
          </button>
          <transition name="fade">
            <div v-if="dropdownOpen" class="absolute right-0 mt-2 w-40 bg-white border rounded shadow-md py-2 z-50">
              <router-link to="/account" class="flex items-center px-4 py-2 hover:bg-gray-100">
                <i class="fas fa-id-card mr-2"></i> My Account
              </router-link>
              <button @click="logout" class="w-full text-left flex items-center px-4 py-2 hover:bg-gray-100">
                <i class="fas fa-sign-out-alt mr-2"></i> Logout
              </button>
            </div>
          </transition>
        </div>
        <router-link v-else to="/login" class="text-gray-700 hover:text-yellow-500">Sign in</router-link>

        <router-link to="/contactus" class="bg-yellow-500 text-white px-4 py-2 rounded-md hover:bg-yellow-600">
          Contact Us
        </router-link>
      </div>
    </nav>

    <!-- Mobile Navbar (unchanged, can be upgraded later similarly) -->
    <nav class="lg:hidden flex justify-between items-center px-4 py-3 bg-white">
      <div class="flex items-center space-x-4">
        <button @click="toggleMenu" class="text-2xl text-gray-700 focus:outline-none">
          &#9776;
        </button>
        <img src="@/assets/osismerch.jpg" alt="Logo" class="h-8 w-auto" />
      </div>
      <div class="flex items-center space-x-4">
        <router-link to="/basket" class="text-gray-700 hover:text-yellow-500 flex items-center">
          <span class="text-xl">🛒</span>
          <span class="ml-1">{{ basketCount }}</span>
        </router-link>
        <div v-if="isLoggedIn" class="relative">
          <button @click="toggleDropdown" class="text-gray-700 hover:text-yellow-500 text-xl focus:outline-none">
            <i class="fas fa-user-circle mr-1"></i> {{ userName }}
          </button>
          <transition name="fade">
            <div v-if="dropdownOpen" class="absolute right-0 mt-2 w-40 bg-white border rounded shadow-md py-2 z-50">
              <router-link to="/account" class="flex items-center px-4 py-2 hover:bg-gray-100">
                <i class="fas fa-id-card mr-2"></i> My Account
              </router-link>
              <button @click="logout" class="w-full text-left flex items-center px-4 py-2 hover:bg-gray-100">
                <i class="fas fa-sign-out-alt mr-2"></i> Logout
              </button>
            </div>
          </transition>
        </div>
        <router-link v-else to="/login" class="text-gray-700 hover:text-yellow-500">Sign in</router-link>
      </div>

    </nav>

    <!-- Mobile Dropdown Menu -->
    <transition name="fade">
      <div v-if="isOpen"
        class="absolute top-full left-0 w-full bg-white border-t border-gray-200 lg:hidden shadow-md z-20">
        <router-link to="/" @click.native="isOpen = false"
          class="block px-4 py-2 hover:bg-yellow-100">Home</router-link>
        <router-link to="/shop" @click.native="isOpen = false"
          class="block px-4 py-2 hover:bg-yellow-100">Shop</router-link>
        <router-link to="/contactus" @click.native="isOpen = false" class="block px-4 py-2 hover:bg-yellow-100">Contact
          us</router-link>
      </div>
    </transition>
    
    <!-- Main content -->
    <main>
      <router-view />
    </main>
  
 
  </header>


  <header v-if="userRole === 'admin'" class="flex h-screen bg-gray-800">
    <!-- Sidebar -->
    <aside class="w-55 bg-black-800">
      <div class="p-6 text-2xl font-bold text-[#c3961a] border-b">
        Admin Panel
      </div>
      <nav class="mt-6 space-y-2 text-white font-medium">
        <router-link
          to="/admin-dashboard"
          class="flex items-center px-6 py-3 hover:bg-gray-700"
          active-class="bg-indigo-100 text-indigo-400"
        >
          <i class="fas fa-tachometer-alt mr-3"></i> Dashboard
        </router-link>
        <router-link
          to="/admin-product"
          class="flex items-center px-6 py-3 hover:bg-gray-700"
          active-class="bg-indigo-100 text-indigo-600"
        >
          <i class="fas fa-box-open mr-3"></i> Product
        </router-link>
        <router-link
          to="/admin-orders"
          class="flex items-center px-6 py-3 hover:bg-gray-700"
          active-class="bg-indigo-100 text-indigo-600"
        >
          <i class="fas fa-receipt mr-3"></i> Orders
        </router-link>
        <router-link
          to="/admin-voucher"
          class="flex items-center px-6 py-3 hover:bg-gray-700"
          active-class="bg-indigo-100 text-indigo-600"
        >
          <i class="fas fa-ticket-alt mr-3"></i> Voucher
        </router-link>
        <button
          @click="logout"
          class="flex items-center w-full px-6 py-3 text-left hover:bg-red-100 text-red-600"
        >
          <i class="fas fa-sign-out-alt mr-3"></i> Logout
        </button>
      </nav>
    </aside>

    <!-- Main content -->
    <main class="flex-1 p-6 overflow-auto">
      <router-view />
    </main>
  </header>





</template>

<script>
import { useUserStore } from '@/stores/userStore';

export default {
  data() {
    return {
      isOpen: false,
      dropdownOpen: false,
      role: '' // Default role, can be changed based on user state

    };
  },
  computed: {
    store() {
      return useUserStore();
    },
    userName() {
      return this.store.name;
    },
    isLoggedIn() {
      return this.store.isLoggedIn;
    },
    basketCount() {
      return this.store.basketCount;
    },
    userRole() {
      return this.store.role; // Assuming role is stored in userStore
    }
  },
  mounted() {
    this.store.loadFromStorage();
    this.isOpen = false;
    this.dropdownOpen = false;
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen;
    },
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    logout() {
      this.store.logout();
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<!-- Include font awesome icons -->
<!-- You can include this in your index.html or main.js -->
<!-- <script src="https://kit.fontawesome.com/your-fontawesome-kit.js" crossorigin="anonymous"></script> -->
