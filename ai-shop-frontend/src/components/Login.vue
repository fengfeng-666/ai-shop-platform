<template>
  <div class="login-wrap">
    <div class="login-card">
      <div class="brand">
        <span class="brand-icon">◈</span>
        <h1>AI Shop</h1>
        <p>智能购物平台</p>
      </div>

      <div class="tabs">
        <button :class="{ active: mode === 'login' }" @click="mode = 'login'">登录</button>
        <button :class="{ active: mode === 'register' }" @click="mode = 'register'">注册</button>
      </div>

      <div class="form">
        <div class="field">
          <label>用户名</label>
          <input v-model="username" placeholder="请输入用户名" @keyup.enter="submit" />
        </div>
        <div class="field">
          <label>密码</label>
          <input v-model="password" type="password" placeholder="请输入密码" @keyup.enter="submit" />
        </div>
        <div v-if="error" class="error">{{ error }}</div>
        <button class="submit-btn" @click="submit" :disabled="loading">
          <span v-if="loading">处理中...</span>
          <span v-else>{{ mode === 'login' ? '登录' : '注册' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['logged-in'])

const mode = ref('login')
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const submit = async () => {
  if (!username.value || !password.value) {
    error.value = '请填写用户名和密码'
    return
  }
  loading.value = true
  error.value = ''
  try {
    if (mode.value === 'register') {
      const res = await axios.post('/api/user/register', {
        username: username.value,
        password: password.value
      })
      if (res.data.msg === '注册成功') {
        mode.value = 'login'
        error.value = '注册成功，请登录'
      } else {
        error.value = res.data.msg || '注册失败'
      }
    } else {
      const res = await axios.post('/api/user/login', {
        username: username.value,
        password: password.value
      })
      if (res.data.access_token) {
        localStorage.setItem('token', res.data.access_token)
        localStorage.setItem('username', username.value)
        emit('logged-in')
      } else {
        error.value = res.data.msg || '登录失败'
      }
    }
  } catch (e) {
    error.value = '网络错误，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh;
  background: #0a0a0f;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: radial-gradient(ellipse at 20% 50%, rgba(99,60,180,0.15) 0%, transparent 60%),
                    radial-gradient(ellipse at 80% 20%, rgba(20,160,120,0.1) 0%, transparent 50%);
}
.login-card {
  width: 380px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 40px;
  backdrop-filter: blur(20px);
}
.brand { text-align: center; margin-bottom: 32px; }
.brand-icon { font-size: 32px; color: #7c5cbf; }
.brand h1 { color: #fff; font-size: 26px; font-weight: 700; margin: 8px 0 4px; letter-spacing: 2px; }
.brand p { color: rgba(255,255,255,0.4); font-size: 13px; }
.tabs { display: flex; gap: 4px; background: rgba(255,255,255,0.05); border-radius: 10px; padding: 4px; margin-bottom: 28px; }
.tabs button { flex: 1; padding: 8px; border: none; background: transparent; color: rgba(255,255,255,0.5); border-radius: 7px; cursor: pointer; font-size: 14px; transition: all 0.2s; }
.tabs button.active { background: rgba(124,92,191,0.5); color: #fff; }
.field { margin-bottom: 16px; }
.field label { display: block; color: rgba(255,255,255,0.5); font-size: 12px; margin-bottom: 6px; letter-spacing: 0.5px; }
.field input { width: 100%; box-sizing: border-box; padding: 11px 14px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; color: #fff; font-size: 14px; outline: none; transition: border-color 0.2s; }
.field input:focus { border-color: rgba(124,92,191,0.6); }
.field input::placeholder { color: rgba(255,255,255,0.2); }
.error { color: #f87171; font-size: 13px; margin-bottom: 12px; }
.submit-btn { width: 100%; padding: 12px; margin-top: 8px; background: linear-gradient(135deg, #7c5cbf, #5b8af0); border: none; border-radius: 10px; color: #fff; font-size: 15px; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }
.submit-btn:hover { opacity: 0.85; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>