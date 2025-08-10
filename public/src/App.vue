<template>
  <div id="app">
    <!-- Если пользователь вошел, показываем приветствие -->
    <div v-if="currentUser">
      <h1>Вітаємо, {{ currentUser.name }}!</h1>
      <p>Ваш ID: {{ currentUser.id }}</p>
      <p>Ваш вік: {{ currentUser.age }}</p>
      <button @click="logout">Вийти</button>
    </div>

    <!-- Иначе, показываем компонент аутентификации -->
    <AuthComponent v-else @authenticated="onUserAuthenticated" />
  </div>
</template>

<script>
import AuthComponent from './components/AuthComponent.vue';

export default {
  name: 'App',
  components: {
    AuthComponent
  },
  data() {
    return {
      // Это свойство хранит информацию о вошедшем пользователе.
      // Изначально null, что означает, что пользователь не вошел.
      currentUser: null
    };
  },
  methods: {
    // Этот метод вызывается, когда дочерний компонент (AuthComponent)
    // отправляет событие 'authenticated'.
    onUserAuthenticated(userData) {
      // Мы получаем данные пользователя (userData) и сохраняем их.
      this.currentUser = userData;
    },
    // Метод для выхода из системы.
    logout() {
      // Просто сбрасываем данные пользователя.
      // Vue автоматически переключит отображение обратно на AuthComponent.
      this.currentUser = null;
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

button {
  margin-top: 10px;
  padding: 8px 16px;
  cursor: pointer;
}
</style>