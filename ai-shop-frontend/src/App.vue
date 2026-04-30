<template>
  <Login v-if="!loggedIn" @logged-in="loggedIn = true" />
  <Shop v-else @logout="loggedIn = false" />
</template>

<script setup>
import { ref } from 'vue'
import Login from './components/Login.vue'
import Shop from './components/Shop.vue'

const loggedIn = ref(!!localStorage.getItem('token'))
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'PingFang SC', 'Microsoft YaHei', -apple-system, sans-serif;
  background: #08080F; color: #e8e8e8;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.18); }
::selection { background: rgba(124,92,191,0.3); color: #fff; }
</style>
