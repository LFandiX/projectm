<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <h1 class="text-2xl font-bold mb-6">Dashboard Overview</h1>

    <!-- Info Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
      <DashboardCard title="Total Revenue" value="Rp. 45.200.000" icon="💰" color="bg-green-100" />
      <DashboardCard title="Total Users" value="3.456" icon="👤" color="bg-blue-100" />
      <DashboardCard title="Total Orders" value="1.280" icon="🧾" color="bg-yellow-100" />
      <DashboardCard title="Total Products" value="245" icon="📦" color="bg-indigo-100" />
    </div>

    <!-- Second Row -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
      <DashboardCard title="Waiting for Taking" value="230" icon="📍" color="bg-orange-100" />
      <DashboardCard title="Waiting for Paying" value="120" icon="💳" color="bg-red-100" />
      <DashboardCard title="Completed Orders" value="85%" icon="✅" color="bg-green-200" />
    </div>
  </div>
</template>

<script>
import DashboardCard from '@/components/DashboardCard.vue'

export default {
  components: {
    DashboardCard
  }
}
</script>
