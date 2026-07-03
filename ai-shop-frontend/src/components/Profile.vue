<template>
  <div class="profile">
    <div class="profile-sections">

      <!-- 账户信息 -->
      <div class="section">
        <div class="section-header">
          <span class="section-icon">&#9678;</span>
          <h3>账户信息</h3>
        </div>
        <div class="field">
          <label>用户名</label>
          <div class="field-row">
            <input v-model="newUsername" :placeholder="currentUsername" />
            <button @click="updateUsername" :disabled="!newUsername || usernameLoading">
              {{ usernameLoading ? '保存中...' : '保存' }}
            </button>
          </div>
        </div>
        <div v-if="usernameMsg" class="msg" :class="usernameMsgType">{{ usernameMsg }}</div>
      </div>

      <!-- 修改密码 -->
      <div class="section">
        <div class="section-header">
          <span class="section-icon">&#9733;</span>
          <h3>修改密码</h3>
        </div>
        <div class="form-group">
          <div class="field">
            <label>当前密码</label>
            <input v-model="pwd.old" type="password" placeholder="请输入当前密码" />
          </div>
          <div class="field">
            <label>新密码</label>
            <input v-model="pwd.new1" type="password" placeholder="请输入新密码" />
          </div>
          <div class="field">
            <label>确认新密码</label>
            <input v-model="pwd.new2" type="password" placeholder="再次输入新密码" />
          </div>
        </div>
        <div v-if="pwdMsg" class="msg" :class="pwdMsgType">{{ pwdMsg }}</div>
        <button class="action-btn" @click="updatePassword" :disabled="pwdLoading">
          {{ pwdLoading ? '修改中...' : '修改密码' }}
        </button>
      </div>

      <!-- 收货地址 -->
      <div class="section">
        <div class="section-header">
          <span class="section-icon">&#9737;</span>
          <h3>收货地址</h3>
        </div>

        <div v-if="addresses.length === 0" class="empty-addr">暂无收货地址</div>
        <div v-for="a in addresses" :key="a.id" class="addr-card">
          <div class="addr-info">
            <span class="addr-name">{{ a.name }}</span>
            <span class="addr-phone">{{ a.phone }}</span>
            <span class="addr-detail">{{ a.detail }}</span>
          </div>
        </div>

        <div class="add-addr-form">
          <p class="add-addr-label">添加新地址</p>
          <div class="addr-inputs">
            <input v-model="newAddr.name" placeholder="收件人姓名" />
            <input v-model="newAddr.phone" placeholder="手机号" />
            <input v-model="newAddr.detail" placeholder="详细地址" class="full" />
          </div>
          <div v-if="addrMsg" class="msg" :class="addrMsgType">{{ addrMsg }}</div>
          <button class="action-btn" @click="addAddress" :disabled="addrLoading">
            {{ addrLoading ? '添加中...' : '添加地址' }}
          </button>
        </div>
      </div>

    </div>

      <!-- 管理员面板 -->
      <div v-if="isAdmin" class="section">
        <div class="section-header">
          <span class="section-icon">&#9881;</span>
          <h3>后台管理</h3>
          <span class="admin-badge">管理员</span>
        </div>
        <Admin />
      </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Admin from './Admin.vue'

const props = defineProps({
  isAdmin: Boolean
})

const token = localStorage.getItem('token')
const headers = { Authorization: 'Bearer ' + token }

const currentUsername = ref(localStorage.getItem('username') || '')

// 用户名
const newUsername = ref('')
const usernameLoading = ref(false)
const usernameMsg = ref('')
const usernameMsgType = ref('success')

const updateUsername = async () => {
  usernameLoading.value = true
  usernameMsg.value = ''
  try {
    await axios.put('/api/user/update', null, { params: { username: newUsername.value }, headers })
    localStorage.setItem('username', newUsername.value)
    currentUsername.value = newUsername.value
    newUsername.value = ''
    usernameMsg.value = '用户名修改成功'
    usernameMsgType.value = 'success'
  } catch {
    usernameMsg.value = '修改失败，用户名可能已被使用'
    usernameMsgType.value = 'error'
  } finally {
    usernameLoading.value = false
  }
}

// 密码
const pwd = ref({ old: '', new1: '', new2: '' })
const pwdLoading = ref(false)
const pwdMsg = ref('')
const pwdMsgType = ref('success')

const updatePassword = async () => {
  if (!pwd.value.old || !pwd.value.new1) {
    pwdMsg.value = '请填写所有密码字段'
    pwdMsgType.value = 'error'
    return
  }
  if (pwd.value.new1 !== pwd.value.new2) {
    pwdMsg.value = '两次输入的新密码不一致'
    pwdMsgType.value = 'error'
    return
  }
  pwdLoading.value = true
  pwdMsg.value = ''
  try {
    await axios.put('/api/user/change-password', null, {
      params: { old_password: pwd.value.old, new_password: pwd.value.new1 }, headers
    })
    pwdMsg.value = '密码修改成功，请重新登录'
    pwdMsgType.value = 'success'
    pwd.value = { old: '', new1: '', new2: '' }
  } catch (e) {
    pwdMsg.value = e.response?.data?.detail || '修改失败，请检查当前密码'
    pwdMsgType.value = 'error'
  } finally {
    pwdLoading.value = false
  }
}

// 地址
const addresses = ref([])
const newAddr = ref({ name: '', phone: '', detail: '' })
const addrLoading = ref(false)
const addrMsg = ref('')
const addrMsgType = ref('success')

const loadAddresses = async () => { try { const res = await axios.get('/api/address/', { headers }); addresses.value = res.data } catch {} }

const addAddress = async () => {
  if (!newAddr.value.name || !newAddr.value.phone || !newAddr.value.detail) {
    addrMsg.value = '请填写完整地址信息'
    addrMsgType.value = 'error'
    return
  }
  addrLoading.value = true
  addrMsg.value = ''
  try {
    await axios.post('/api/address/add', null, { params: newAddr.value, headers })
    addrMsg.value = '地址添加成功'
    addrMsgType.value = 'success'
    newAddr.value = { name: '', phone: '', detail: '' }
    loadAddresses()
  } catch {
    addrMsg.value = '添加失败，请重试'
    addrMsgType.value = 'error'
  } finally {
    addrLoading.value = false
  }
}

onMounted(loadAddresses)
</script>

<style scoped>
.profile { padding: 0; }
.profile-sections { display: flex; flex-direction: column; gap: 22px; }
.section { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07); border-radius: 20px; padding: 28px; }
.section-header { display: flex; align-items: center; gap: 10px; margin-bottom: 22px; }
.section-icon { font-size: 16px; color: #7C5CBF; }
.section-header h3 { font-size: 17px; font-weight: 600; color: #fff; }
.admin-badge { font-size: 10px; padding: 3px 10px; background: rgba(240,160,80,0.15); color: #f0a050; border: 1px solid rgba(240,160,80,0.3); border-radius: 99px; font-weight: 500; letter-spacing: 1px; margin-left: auto; }
.form-group { display: flex; flex-direction: column; gap: 16px; margin-bottom: 16px; }
.field { display: flex; flex-direction: column; gap: 7px; margin-bottom: 14px; }
.field label { font-size: 12px; color: rgba(255,255,255,0.35); letter-spacing: 0.5px; font-weight: 500; }
.field-row { display: flex; gap: 10px; }
.field-row input { flex: 1; }
.field-row button {
  padding: 10px 20px; background: rgba(124,92,191,0.2); border: 1px solid rgba(124,92,191,0.3);
  border-radius: 10px; color: #fff; cursor: pointer; font-size: 13px; font-weight: 500;
  white-space: nowrap; transition: all 0.3s;
}
.field-row button:hover { background: rgba(124,92,191,0.4); }
.field-row button:disabled { opacity: 0.4; cursor: not-allowed; }
input {
  padding: 11px 15px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px; color: #fff; font-size: 14px; outline: none; transition: all 0.3s;
  width: 100%; box-sizing: border-box;
}
input:focus { border-color: rgba(124,92,191,0.5); background: rgba(255,255,255,0.07); box-shadow: 0 0 0 3px rgba(124,92,191,0.06); }
input::placeholder { color: rgba(255,255,255,0.15); }
.msg { padding: 10px 14px; border-radius: 10px; font-size: 13px; margin-bottom: 12px; }
.msg.success { background: rgba(74,222,128,0.08); color: #4ade80; border: 1px solid rgba(74,222,128,0.15); }
.msg.error { background: rgba(248,113,113,0.08); color: #f87171; border: 1px solid rgba(248,113,113,0.15); }
.action-btn {
  padding: 11px 28px; background: linear-gradient(135deg, #7C5CBF, #5B8AF0); border: none;
  border-radius: 12px; color: #fff; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s;
}
.action-btn:hover { box-shadow: 0 4px 16px rgba(124,92,191,0.3); transform: translateY(-1px); }
.action-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
.empty-addr { color: rgba(255,255,255,0.25); font-size: 14px; margin-bottom: 16px; padding: 12px 0; }
.addr-card { display: flex; justify-content: space-between; align-items: center; padding: 14px 18px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; margin-bottom: 8px; transition: all 0.3s; }
.addr-card:hover { border-color: rgba(255,255,255,0.1); }
.addr-info { display: flex; gap: 14px; align-items: center; flex-wrap: wrap; }
.addr-name { font-size: 14px; font-weight: 600; color: #fff; }
.addr-phone { font-size: 13px; color: rgba(255,255,255,0.4); }
.addr-detail { font-size: 13px; color: rgba(255,255,255,0.4); }
.add-addr-label { font-size: 13px; color: rgba(255,255,255,0.3); margin: 20px 0 10px; font-weight: 500; }
.addr-inputs { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }
.addr-inputs input.full { grid-column: 1 / -1; }
</style>
