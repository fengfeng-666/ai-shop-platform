<template>
  <div>
    <h2>结算</h2>

    <p>选择地址：</p>
    <select v-model="addressId">
      <option v-for="a in addresses" :value="a.id">
        {{ a.detail }}
      </option>
    </select>

    <button @click="pay">支付</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const token = localStorage.getItem('token')

const addresses = ref([])
const addressId = ref(null)

const loadAddress = async () => {
  const res = await axios.get('http://127.0.0.1:8000/address/list', {
    headers: { Authorization: 'Bearer ' + token }
  })
  addresses.value = res.data
}

const pay = async () => {
  await axios.post('http://127.0.0.1:8000/order/create', null, {
    params: { address_id: addressId.value },
    headers: { Authorization: 'Bearer ' + token }
  })
  alert('支付成功')
}

onMounted(loadAddress)
</script>