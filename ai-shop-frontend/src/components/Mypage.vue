<template>
  <div>
    <h2>我的订单</h2>

    <div v-for="o in orders" :key="o.id">
      订单号：{{ o.id }} - ¥{{ o.price }} - {{ o.status }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const token = localStorage.getItem('token')

const orders = ref([])

const loadOrders = async () => {
  const res = await axios.get('http://127.0.0.1:8000/order/list', {
    headers: { Authorization: 'Bearer ' + token }
  })
  orders.value = res.data
}

onMounted(loadOrders)
</script>