<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="submitLogin">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    submitLogin() {
      console.log('Login submitted:', this.email, this.password);
    }
  }
};
</script>
