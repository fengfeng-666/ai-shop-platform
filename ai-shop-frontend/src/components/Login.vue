<template>
  <div class="login-wrap">
    <!-- 背景粒子 -->
    <div class="particles">
      <span v-for="n in 20" :key="n" class="particle" :style="{
        left: rand(n,0) + '%', top: rand(n,1) + '%',
        animationDelay: rand(n,2) + 's', animationDuration: 3 + rand(n,3) + 's'
      }"></span>
    </div>

    <div class="card">
      <!-- 品牌区 -->
      <div class="brand">
        <svg class="logo-svg" viewBox="0 0 64 64" fill="none">
          <defs>
            <linearGradient id="lgg" x1="0" y1="0" x2="64" y2="64">
              <stop offset="0%" stop-color="#7C5CBF"/>
              <stop offset="100%" stop-color="#5B8AF0"/>
            </linearGradient>
          </defs>
          <rect x="20" y="8" width="24" height="24" rx="5" fill="url(#lgg)" transform="rotate(45 32 20)"/>
          <circle cx="22" cy="26" r="3" fill="#fff" opacity="0.9"/>
          <circle cx="32" cy="20" r="2.5" fill="#fff" opacity="0.7"/>
          <circle cx="42" cy="26" r="3" fill="#fff" opacity="0.9"/>
          <line x1="22" y1="26" x2="32" y2="20" stroke="#fff" stroke-width="1" opacity="0.5"/>
          <line x1="32" y1="20" x2="42" y2="26" stroke="#fff" stroke-width="1" opacity="0.5"/>
          <rect x="16" y="44" width="32" height="5" rx="2.5" fill="url(#lgg)"/>
        </svg>
        <h1>灵境商坊</h1>
        <p>LingMart AI · 智能购物平台</p>
      </div>

      <!-- 切换 -->
      <div class="tabs">
        <button :class="{ active: mode === 'login' }" @click="mode = 'login'">登录</button>
        <button :class="{ active: mode === 'register' }" @click="mode = 'register'">注册</button>
      </div>

      <!-- 表单 -->
      <div class="form">
        <div class="field">
          <span class="field-icon">&#9903;</span>
          <input v-model="username" placeholder="用户名" @keyup.enter="submit" />
        </div>
        <div class="field">
          <span class="field-icon">&#9906;</span>
          <input v-model="password" type="password" placeholder="密码" @keyup.enter="submit" />
        </div>
        <div v-if="error" class="error" :class="{ success: error.includes('成功') }">{{ error }}</div>
        <button class="submit-btn" @click="submit" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          <span>{{ loading ? '' : mode === 'login' ? '登 录' : '注 册' }}</span>
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

const rand = (seed, offset) => {
  const x = Math.sin(seed * 9301 + offset * 4921) * 49297
  return Math.abs(x - Math.floor(x))
}

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
  background: linear-gradient(135deg, #08080F 0%, #0f0f1a 50%, #08081a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

/* 粒子动画 */
.particles { position: absolute; inset: 0; pointer-events: none; }
.particle {
  position: absolute;
  width: 3px; height: 3px;
  background: rgba(124,92,191,0.3);
  border-radius: 50%;
  animation: float linear infinite;
}
@keyframes float {
  0% { transform: translateY(0) scale(1); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(-100vh) scale(0); opacity: 0; }
}

.card {
  width: 420px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 24px;
  padding: 48px 44px;
  backdrop-filter: blur(24px);
  position: relative;
  z-index: 1;
  box-shadow: 0 24px 80px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
}
.brand { text-align: center; margin-bottom: 36px; }
.logo-svg { width: 52px; height: 52px; display: block; margin: 0 auto 14px; }
.brand h1 {
  color: #fff;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: 4px;
  background: linear-gradient(135deg, #c9b8f0, #8bb0f8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.brand p {
  color: rgba(255,255,255,0.3);
  font-size: 13px;
  margin-top: 6px;
  letter-spacing: 1px;
}

.tabs {
  display: flex;
  gap: 0;
  background: rgba(255,255,255,0.05);
  border-radius: 12px;
  padding: 4px;
  margin-bottom: 28px;
  position: relative;
}
.tabs button {
  flex: 1;
  padding: 10px;
  border: none;
  background: transparent;
  color: rgba(255,255,255,0.45);
  border-radius: 9px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}
.tabs button.active {
  background: rgba(124,92,191,0.35);
  color: #fff;
  box-shadow: 0 2px 8px rgba(124,92,191,0.2);
}

.form { display: flex; flex-direction: column; gap: 14px; }
.field {
  position: relative;
  display: flex;
  align-items: center;
}
.field-icon {
  position: absolute;
  left: 14px;
  font-size: 14px;
  color: rgba(255,255,255,0.25);
  pointer-events: none;
}
.field input {
  width: 100%;
  box-sizing: border-box;
  padding: 13px 14px 13px 38px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;
}
.field input:focus {
  border-color: rgba(124,92,191,0.5);
  background: rgba(255,255,255,0.08);
  box-shadow: 0 0 0 3px rgba(124,92,191,0.08);
}
.field input::placeholder { color: rgba(255,255,255,0.2); }

.error {
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 13px;
  text-align: center;
  background: rgba(248,113,113,0.1);
  color: #f87171;
  border: 1px solid rgba(248,113,113,0.15);
}
.error.success {
  background: rgba(74,222,128,0.1);
  color: #4ade80;
  border: 1px solid rgba(74,222,128,0.15);
}

.submit-btn {
  width: 100%;
  padding: 14px;
  margin-top: 4px;
  background: linear-gradient(135deg, #7C5CBF, #5B8AF0);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}
.submit-btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s;
}
.submit-btn:hover::after { opacity: 1; }
.submit-btn:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(124,92,191,0.3); }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.spinner {
  width: 20px; height: 20px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
