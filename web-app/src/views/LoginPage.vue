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
import { useUserStore } from '../stores/usuarioStore';
import api from '../axios';

export default {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async submitLogin() {
      try {
        const response = await api.post('/login', {
          email: this.email,
          password: this.password
        });

        const userStore = useUserStore();
        userStore.setUser(response.data);

        this.$router.push({ name: 'Home' });
      } catch (error) {
        console.error('Erro ao fazer login', error);
      }
    }
  }
};
</script>
