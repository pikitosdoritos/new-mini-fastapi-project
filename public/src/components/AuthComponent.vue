<template>
  <div>
    <div>
      <h2>Регістрація</h2>
      <form @submit.prevent="register">
        <div>
          <label for="registerName">Ім'я:</label>
          <input type="text" id="registerName" v-model="registerName" required>
        </div>
        <div>
          <label for="registerAge">Вік:</label>
          <input type="number" id="registerAge" v-model.number="registerAge" required>
        </div>
        <button type="submit">Зареєструватися</button>
      </form>
    </div>

    <hr>

    <div>
      <h2>Авторизація</h2>
      <form @submit.prevent="login">
        <div>
          <label for="loginName">Ім'я:</label>
          <input type="text" id="loginName" v-model="loginName" required>
        </div>
        <button type="submit">Авторизуватися</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AuthComponent',
  data() {
    return {
      registerName: '',
      registerAge: '',
      loginName: ''
    };
  },
  methods: {
    async register() {
      if (!this.registerName || !this.registerAge) {
        alert('Будь ласка, заповніть всі поля для реєстрації');
        return;
      }
      try {
        const response = await axios.post('http://127.0.0.1:8000/users/', {
          name: this.registerName,
          age: this.registerAge
        });
        // Отправляем событие 'authenticated' наверх с данными пользователя
        this.$emit('authenticated', response.data);
      } catch (error) {
        console.error('Registration failed:', error);
        alert('Помилка реєстрації. Можливо, такий користувач вже існує.');
      }
    },
    async login() {
      if (!this.loginName) {
        alert('Будь ласка, введіть ім\'я для входу');
        return;
      }
      try {
        const response = await axios.get(`http://127.0.0.1:8000/users/${this.loginName}`);
        // Отправляем событие 'authenticated' наверх с данными пользователя
        this.$emit('authenticated', response.data);
      } catch (error) {
        if (error.response && error.response.status === 404) {
          alert('Користувача з таким ім\'ям не знайдено.');
        } else {
          console.error('Login failed:', error);
          alert('Помилка входу.');
        }
      }
    }
  }
};
</script>

<style scoped>
hr {
  margin: 20px 0;
}
div {
  margin-bottom: 10px;
}
</style>