// stores/userStore.js
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    user_id: null,
    name: '',
    role: 'guest', // default role
    basket: [],
    history: []
  }),
  getters: {
    isLoggedIn: (state) => state.user_id !== null,
    basketCount: (state) => state.basket.length,
  },
  actions: {
    login(payload) {
      this.user_id = payload.user_id;
      this.name = payload.name;
        this.role = payload.role; // set role, default to 'guest'
      this.basket = payload.basket || [];
      localStorage.setItem("loginData", JSON.stringify(this.$state));
    },
    updateBasket(newBasket) {
      this.basket = newBasket;
    },
    logout() {
      this.user_id = null;
      this.name = '';
      this.role = 'guest'; // reset role to default
      this.basket = [];
      localStorage.removeItem("loginData");
    },
    loadFromStorage() {
      const stored = localStorage.getItem("loginData");
      if (stored) {
        const parsed = JSON.parse(stored);
        this.$patch(parsed);
      }
    }
  }
});
