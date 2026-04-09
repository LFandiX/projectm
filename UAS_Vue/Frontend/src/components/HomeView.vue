<script>
import axios from 'axios'
export default {
  name: 'LoginForm',
  data() {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async login() {
      try {
        const res = await axios.post('http://localhost:5000/login', this.form);
        console.log('Login successful:', res.data);
        alert('Login successful!');
        // Redirect to dashboard or perform any other action
        this.$router.push({ name: 'Dashboard' });
      } catch (error) {
        console.error('Login failed:', error);
        alert('Login failed! Please check your credentials.');
        // Reset form
        this.form = {
          username: '',
          password: ''
        }
      }
    }

  }
}



</script>

<template>
  <div class="container-page">
    <h1>LOGIN</h1>
    <div class="login-form">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="form.username" required @keyup.enter="login">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="form.password" required @keyup.enter="login">

        <button @click="login">Submit</button>
      </div>

    </div>
  </div>
</template>

<style scoped>
* {
  font-family: Arial, Helvetica, sans-serif;
}

.container-page {
  margin: 0px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  /* Horizontal center */
  align-items: center;
  /* Vertical center */
  height: 100vh;
  /* Full viewport height */
}

h1 {
  color: #0a3200;
}

.login-form {
  /* border: 1px solid red; */
  border-radius: 4%;
  background-color: #d4ffee;
  padding: 70px;
  align-content: center;
  display: flex;
}

.form-group {
  display: flex;
  /* background-color: #bdffe5; */
  background-color: #d4ffee;
  flex-direction: column;
  align-items: center;
  margin-bottom: 15px;
}

#username {
  margin-bottom: 20px;
}

label {
  background-color: #d4ffee;
  margin-bottom: 5px;
  font-weight: bold;
  border-radius: 5px;
  color: #0a3200;
}

input {
  background-color: #d4ffee;
  padding: 8px;
  border-radius: 5px;
  border-color: #0a3200;
}

button {
  padding: 10px;
  border-radius: 5px;
  margin-top: 30px;
  /* background-color: #007bff; */
  background-color: #379634;
  color: white;
  border: none;
  cursor: pointer;
}

button:active {
  background-color: #102542;
  color: white;
}

@media (max-width: 600px) {
  .login-form {
    padding: 40px 30px;
  }

  h1 {
    font-size: 1.5rem;
  }

  button {
    font-size: 1rem;
  }
}
</style>