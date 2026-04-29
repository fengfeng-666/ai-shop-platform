<template>
  <div class="cart">
    <h3>购物车</h3>

    <div v-for="item in cart.items" :key="item.product_id">
      {{ item.name }} x
      <input v-model.number="item.quantity" @change="update(item)" />
      = {{ item.subtotal }}

      <button @click="remove(item.product_id)">删除</button>
    </div>

    <p>总价：{{ cart.total_price }}</p>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import axios from 'axios'

const props = defineProps(['cart'])
const emit = defineEmits(['refresh'])

const token = localStorage.getItem('token')

const update = async (item) => {
  await axios.put('http://127.0.0.1:8000/cart/update', null, {
    params: { product_id: item.product_id, quantity: item.quantity },
    headers: { Authorization: 'Bearer ' + token }
  })
  emit('refresh')
}

const remove = async (id) => {
  await axios.delete('http://127.0.0.1:8000/cart/delete', {
    params: { product_id: id },
    headers: { Authorization: 'Bearer ' + token }
  })
  emit('refresh')
}
</script>