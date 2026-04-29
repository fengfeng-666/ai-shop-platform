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
body { font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 2px; }
</style>