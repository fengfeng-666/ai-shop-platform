<template>
  <div>
    <button class="btn" @click="show = !show">AI助手</button>

    <div v-if="show" class="box">
      <div v-for="(m, i) in messages" :key="i">
        {{ m.role }}: {{ m.content }}
      </div>

      <input v-model="input" @keyup.enter="send" />
      <button @click="send">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const show = ref(false)
const input = ref('')
const messages = ref([])

const token = localStorage.getItem('token')

const send = async () => {
  messages.value.push({ role: '我', content: input.value })

  const res = await axios.post(
    'http://127.0.0.1:8000/ai/chat',
    { message: input.value },
    { headers: { Authorization: 'Bearer ' + token } }
  )

  messages.value.push({ role: 'AI', content: res.data.reply })
  input.value = ''
}
</script>