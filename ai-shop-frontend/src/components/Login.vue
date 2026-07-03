<template>
  <div class="login-page">
    <!-- Animated Background -->
    <div class="bg-effects">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="grid-pattern"></div>
    </div>

    <!-- Main Card -->
    <div class="login-container">
      <div class="login-card">
        <!-- Brand Header -->
        <header class="brand">
          <div class="logo-wrapper">
            <svg class="logo" viewBox="0 0 64 64" fill="none">
              <defs>
                <linearGradient id="logoGrad" x1="0" y1="0" x2="64" y2="64">
                  <stop offset="0%" stop-color="#7C5CBF"/>
                  <stop offset="100%" stop-color="#5B8AF0"/>
                </linearGradient>
              </defs>
              <rect x="20" y="8" width="24" height="24" rx="5" fill="url(#logoGrad)" transform="rotate(45 32 20)"/>
              <circle cx="22" cy="26" r="3" fill="#fff" opacity="0.9"/>
              <circle cx="32" cy="20" r="2.5" fill="#fff" opacity="0.7"/>
              <circle cx="42" cy="26" r="3" fill="#fff" opacity="0.9"/>
              <line x1="22" y1="26" x2="32" y2="20" stroke="#fff" stroke-width="1.5" opacity="0.5"/>
              <line x1="32" y1="20" x2="42" y2="26" stroke="#fff" stroke-width="1.5" opacity="0.5"/>
              <rect x="16" y="44" width="32" height="5" rx="2.5" fill="url(#logoGrad)"/>
            </svg>
          </div>
          <h1 class="brand-name">灵境商坊</h1>
          <p class="brand-subtitle">LingMart AI · 智能购物平台</p>
        </header>

        <!-- Tab Switcher -->
        <div class="tab-switcher">
          <button
            v-for="t in tabs"
            :key="t.value"
            :class="['tab-btn', { active: mode === t.value }]"
            @click="mode = t.value"
          >
            {{ t.label }}
          </button>
        </div>

        <!-- Form -->
        <form class="form" @submit.prevent="handleSubmit">
          <div class="input-group">
            <div class="input-wrapper">
              <span class="input-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </span>
              <input
                v-model="username"
                type="text"
                placeholder="请输入用户名"
                autocomplete="username"
                :disabled="loading"
              />
            </div>
          </div>

          <div class="input-group">
            <div class="input-wrapper">
              <span class="input-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
              </span>
              <input
                v-model="password"
                type="password"
                placeholder="请输入密码"
                autocomplete="current-password"
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Error/Success Message -->
          <transition name="slide-fade">
            <div v-if="error" :class="['message', error.includes('成功') ? 'success' : 'error']">
              <span class="message-icon">{{ error.includes('成功') ? '✓' : '!' }}</span>
              {{ error }}
            </div>
          </transition>

          <!-- Submit Button -->
          <button type="submit" class="submit-btn" :disabled="loading || !username || !password">
            <span v-if="loading" class="loader"></span>
            <span v-else>{{ mode === 'login' ? '登 录' : '注 册' }}</span>
          </button>
        </form>

        <!-- Footer -->
        <footer class="card-footer">
          <p>{{ mode === 'login' ? '还没有账号？' : '已有账号？' }}
            <a href="#" @click.prevent="mode = mode === 'login' ? 'register' : 'login'">
              {{ mode === 'login' ? '立即注册' : '立即登录' }}
            </a>
          </p>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['logged-in'])

const tabs = [
  { value: 'login', label: '登录' },
  { value: 'register', label: '注册' }
]

const mode = ref('login')
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleSubmit = async () => {
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
    error.value = e.response?.data?.detail || '网络错误，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: var(--bg-base);
  padding: var(--space-xl);
}

/* Animated Background */
.bg-effects {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: var(--color-primary);
  top: -10%;
  left: -10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: var(--color-accent);
  bottom: -10%;
  right: -10%;
  animation-delay: -7s;
}

.orb-3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #f093fb, #f5576c);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.05); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
}

.grid-pattern {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse at center, black 30%, transparent 70%);
}

/* Login Container */
.login-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
}

.login-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-2xl);
  padding: var(--space-4xl) var(--space-3xl);
  backdrop-filter: blur(20px);
  box-shadow: var(--shadow-xl), inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

/* Brand */
.brand {
  text-align: center;
  margin-bottom: var(--space-3xl);
}

.logo-wrapper {
  width: 64px;
  height: 64px;
  margin: 0 auto var(--space-lg);
  background: var(--color-gradient);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-glow);
}

.logo {
  width: 40px;
  height: 40px;
}

.brand-name {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: 4px;
  background: linear-gradient(135deg, #c9b8f0, #8bb0f8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: var(--space-xs);
}

.brand-subtitle {
  color: var(--text-muted);
  font-size: 14px;
  letter-spacing: 1px;
}

/* Tab Switcher */
.tab-switcher {
  display: flex;
  background: var(--bg-surface);
  border-radius: var(--radius-md);
  padding: 4px;
  margin-bottom: var(--space-2xl);
  border: 1px solid var(--border-subtle);
}

.tab-btn {
  flex: 1;
  padding: 10px 16px;
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  color: var(--text-tertiary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-base);
}

.tab-btn:hover {
  color: var(--text-secondary);
}

.tab-btn.active {
  background: rgba(124, 92, 191, 0.25);
  color: var(--text-primary);
  box-shadow: var(--shadow-sm);
}

/* Form */
.form {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.input-group {
  position: relative;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
  overflow: hidden;
}

.input-wrapper:focus-within {
  border-color: var(--border-focus);
  background: var(--bg-surface-hover);
  box-shadow: 0 0 0 3px rgba(124, 92, 191, 0.1);
}

.input-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  color: var(--text-muted);
  flex-shrink: 0;
}

.input-wrapper input {
  flex: 1;
  padding: 14px 16px 14px 0;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 15px;
  outline: none;
  width: 100%;
}

.input-wrapper input::placeholder {
  color: var(--text-muted);
}

.input-wrapper input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Message */
.message {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md) var(--space-lg);
  border-radius: var(--radius-md);
  font-size: 14px;
}

.message.success {
  background: var(--color-success-bg);
  color: var(--color-success);
  border: 1px solid rgba(74, 222, 128, 0.2);
}

.message.error {
  background: var(--color-error-bg);
  color: var(--color-error);
  border: 1px solid rgba(248, 113, 113, 0.2);
}

.message-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}

.success .message-icon {
  background: rgba(74, 222, 128, 0.2);
}

.error .message-icon {
  background: rgba(248, 113, 113, 0.2);
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Submit Button */
.submit-btn {
  width: 100%;
  padding: 14px 24px;
  margin-top: var(--space-sm);
  background: var(--color-gradient);
  border: none;
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 4px;
  cursor: pointer;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.submit-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--color-gradient-hover);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow-lg);
}

.submit-btn:hover:not(:disabled)::before {
  opacity: 1;
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.submit-btn span {
  position: relative;
  z-index: 1;
}

/* Loader */
.loader {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Footer */
.card-footer {
  text-align: center;
  margin-top: var(--space-2xl);
  padding-top: var(--space-2xl);
  border-top: 1px solid var(--border-subtle);
}

.card-footer p {
  color: var(--text-muted);
  font-size: 14px;
}

.card-footer a {
  color: var(--color-primary-light);
  text-decoration: none;
  font-weight: 500;
  transition: color var(--transition-fast);
}

.card-footer a:hover {
  color: var(--color-accent-light);
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 480px) {
  .login-card {
    padding: var(--space-3xl) var(--space-xl);
  }

  .brand-name {
    font-size: 24px;
    letter-spacing: 2px;
  }
}
</style>
