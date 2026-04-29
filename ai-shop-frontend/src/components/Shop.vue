<template>
  <div class="shop">
    <header class="topbar">
      <div class="logo">◈ AI Shop</div>
      <nav class="nav">
        <button :class="{ active: tab === 'shop' }" @click="tab = 'shop'">商城</button>
        <button :class="{ active: tab === 'cart' }" @click="tab = 'cart'">
          购物车<span v-if="cartCount > 0" class="badge">{{ cartCount }}</span>
        </button>
        <button :class="{ active: tab === 'orders' }" @click="tab = 'orders'">我的订单</button>
        <button :class="{ active: tab === 'ai' }" @click="tab = 'ai'">AI助手</button>
        <button v-if="isAdmin" :class="{ active: tab === 'admin' }" @click="tab = 'admin'" class="admin-btn">⚙ 管理</button>
      </nav>
      <div class="user-info">
        <button class="profile-btn" :class="{ active: tab === 'profile' }" @click="tab = 'profile'">{{ username }}</button>
        <button class="logout-btn" @click="logout">退出</button>
      </div>
    </header>

    <main v-if="tab === 'shop'" class="content">
      <div class="search-bar">
        <input v-model="keyword" placeholder="搜索商品..." @keyup.enter="searchProducts" />
        <button @click="searchProducts">搜索</button>
        <button class="reset-btn" @click="loadProducts">全部</button>
      </div>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="products.length === 0" class="empty">暂无商品</div>
      <div v-else class="product-grid">
        <div v-for="item in products" :key="item.id" class="product-card">
          <div class="product-category">{{ item.category }}</div>
          <div class="product-name">{{ item.name }}</div>
          <div class="product-desc">{{ item.description }}</div>
          <div class="product-footer">
            <span class="product-price">¥{{ item.price }}</span>
            <button class="add-btn" @click="addToCart(item.id)">加入购物车</button>
          </div>
        </div>
      </div>
    </main>

    <main v-else-if="tab === 'cart'" class="content">
      <h2 class="page-title">购物车</h2>
      <div v-if="!cart.items || cart.items.length === 0" class="empty">购物车为空</div>
      <div v-else>
        <div v-for="item in cart.items" :key="item.product_id" class="cart-item">
          <div class="cart-item-name">{{ item.name }}</div>
          <div class="cart-item-controls">
            <button class="qty-btn" @click="updateQty(item, item.quantity - 1)">−</button>
            <span class="qty">{{ item.quantity }}</span>
            <button class="qty-btn" @click="updateQty(item, item.quantity + 1)">+</button>
          </div>
          <div class="cart-item-price">¥{{ item.subtotal }}</div>
          <button class="remove-btn" @click="removeFromCart(item.product_id)">删除</button>
        </div>
        <div class="cart-total">
          <span>合计</span>
          <span class="total-price">¥{{ cart.total_price }}</span>
        </div>
        <button class="checkout-btn" @click="tab = 'checkout'">去结算</button>
      </div>
    </main>

    <main v-else-if="tab === 'checkout'" class="content">
      <h2 class="page-title">结算</h2>
      <div class="checkout-section">
        <h3>选择收货地址</h3>
        <div v-if="addresses.length === 0" class="empty">暂无地址，请在个人主页添加</div>
        <div v-for="a in addresses" :key="a.id" class="address-item" :class="{ selected: addressId === a.id }" @click="addressId = a.id">
          <div class="addr-name">{{ a.name }} {{ a.phone }}</div>
          <div class="addr-detail">{{ a.detail }}</div>
        </div>
        <div class="order-summary">
          <div class="summary-row"><span>商品合计</span><span class="total-price">¥{{ cart.total_price }}</span></div>
        </div>
        <button class="checkout-btn" :disabled="!addressId" @click="pay">确认支付</button>
      </div>
    </main>

    <main v-else-if="tab === 'orders'" class="content">
      <h2 class="page-title">我的订单</h2>
      <div v-if="orders.length === 0" class="empty">暂无订单</div>
      <div v-for="o in orders" :key="o.id" class="order-item">
        <div class="order-id">订单 #{{ o.id }}</div>
        <div class="order-price">¥{{ o.price }}</div>
        <div class="order-status" :class="o.status">{{ o.status === 'paid' ? '已支付' : '待支付' }}</div>
      </div>
    </main>

    <main v-else-if="tab === 'ai'" class="content ai-page">
      <h2 class="page-title">AI 购物助手</h2>
      <div class="chat-window" ref="chatWindow">
        <div v-if="messages.length === 0" class="chat-hint">你可以问我：<br>· 帮我找一双运动鞋<br>· 推荐一些数码产品<br>· 帮我下单最便宜的商品</div>
        <div v-for="(m, i) in messages" :key="i" class="chat-msg" :class="m.role">
          <div class="msg-bubble">{{ m.content }}</div>
        </div>
        <div v-if="aiLoading" class="chat-msg ai"><div class="msg-bubble typing">AI 正在思考...</div></div>
      </div>
      <div class="chat-input-row">
        <input v-model="aiInput" placeholder="输入消息..." @keyup.enter="sendAI" :disabled="aiLoading" />
        <button @click="sendAI" :disabled="aiLoading">发送</button>
      </div>
    </main>

    <main v-else-if="tab === 'admin' && isAdmin" class="content">
      <h2 class="page-title"><span class="admin-badge">管理员</span>后台管理</h2>
      <Admin />
    </main>

    <main v-else-if="tab === 'profile'" class="content">
      <h2 class="page-title">个人主页</h2>
      <Profile />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import axios from 'axios'
import Admin from './Admin.vue'
import Profile from './Profile.vue'

const emit = defineEmits(['logout'])
const tab = ref('shop')
const username = ref(localStorage.getItem('username') || '用户')
const token = localStorage.getItem('token')
const headers = { Authorization: 'Bearer ' + token }

const parseToken = (t) => { try { return JSON.parse(atob(t.split('.')[1])) } catch { return {} } }
const tokenPayload = parseToken(token)
const isAdmin = computed(() => tokenPayload.role === 'admin')

const products = ref([])
const keyword = ref('')
const loading = ref(false)

const loadProducts = async () => {
  loading.value = true; keyword.value = ''
  try { const res = await axios.get('/api/product/'); products.value = res.data } finally { loading.value = false }
}

const searchProducts = async () => {
  if (!keyword.value.trim()) return loadProducts()
  loading.value = true
  try { const res = await axios.get('/api/product/search', { params: { keyword: keyword.value }, headers }); products.value = res.data } finally { loading.value = false }
}

const cart = ref({ items: [], total_price: 0 })
const cartCount = computed(() => cart.value.items?.length || 0)

const loadCart = async () => { try { const res = await axios.get('/api/cart/detail', { headers }); cart.value = res.data } catch {} }
const addToCart = async (id) => { await axios.post('/api/cart/add', null, { params: { product_id: id, quantity: 1 }, headers }); loadCart() }
const updateQty = async (item, qty) => { if (qty <= 0) return removeFromCart(item.product_id); await axios.put('/api/cart/update', null, { params: { product_id: item.product_id, quantity: qty }, headers }); loadCart() }
const removeFromCart = async (id) => { await axios.delete('/api/cart/delete', { params: { product_id: id }, headers }); loadCart() }

const addresses = ref([])
const addressId = ref(null)
const loadAddresses = async () => { try { const res = await axios.get('/api/address/', { headers }); addresses.value = res.data } catch {} }

const pay = async () => {
  try { await axios.post('/api/order/pay', null, { params: { address_id: addressId.value }, headers }); alert('支付成功！'); loadCart(); tab.value = 'orders'; loadOrders() }
  catch { alert('支付失败，请重试') }
}

const orders = ref([])
const loadOrders = async () => { try { const res = await axios.get('/api/order/list', { headers }); orders.value = res.data } catch {} }

const messages = ref([])
const aiInput = ref('')
const aiLoading = ref(false)
const chatWindow = ref(null)

const sendAI = async () => {
  if (!aiInput.value.trim() || aiLoading.value) return
  messages.value.push({ role: 'user', content: aiInput.value })
  const msg = aiInput.value; aiInput.value = ''; aiLoading.value = true
  await nextTick(); scrollChat()
  try { const res = await axios.post('/api/ai/chat', { message: msg }, { headers }); messages.value.push({ role: 'ai', content: res.data.reply }) }
  catch { messages.value.push({ role: 'ai', content: '抱歉，AI 暂时无法响应' }) }
  finally { aiLoading.value = false; await nextTick(); scrollChat() }
}

const scrollChat = () => { if (chatWindow.value) chatWindow.value.scrollTop = chatWindow.value.scrollHeight }
const logout = () => { localStorage.clear(); emit('logout') }

watch(tab, (val) => {
  if (val === 'cart') loadCart()
  if (val === 'orders') loadOrders()
  if (val === 'checkout') { loadAddresses(); loadCart() }
})

onMounted(() => { loadProducts(); loadCart() })
</script>

<style scoped>
.shop{min-height:100vh;background:#0a0a0f;color:#e8e8e8;display:flex;flex-direction:column}
.topbar{display:flex;align-items:center;gap:16px;padding:0 28px;height:60px;background:rgba(255,255,255,.03);border-bottom:1px solid rgba(255,255,255,.07);position:sticky;top:0;z-index:10;backdrop-filter:blur(10px)}
.logo{font-size:18px;font-weight:700;color:#fff;letter-spacing:2px;flex-shrink:0}
.nav{display:flex;gap:2px;flex:1}
.nav button{padding:6px 14px;background:transparent;border:none;color:rgba(255,255,255,.45);border-radius:8px;cursor:pointer;font-size:14px;transition:all .2s;position:relative}
.nav button:hover{color:#fff;background:rgba(255,255,255,.06)}
.nav button.active{color:#fff;background:rgba(124,92,191,.25)}
.admin-btn{color:rgba(240,160,80,.7)!important}
.admin-btn.active{background:rgba(240,160,80,.15)!important;color:#f0a050!important}
.badge{position:absolute;top:2px;right:4px;background:#e85d24;color:#fff;font-size:10px;width:16px;height:16px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.user-info{display:flex;align-items:center;gap:8px;flex-shrink:0}
.profile-btn{padding:6px 14px;background:transparent;border:1px solid rgba(255,255,255,.12);border-radius:8px;color:rgba(255,255,255,.6);cursor:pointer;font-size:13px;transition:all .2s}
.profile-btn:hover,.profile-btn.active{border-color:rgba(124,92,191,.5);color:#fff;background:rgba(124,92,191,.15)}
.logout-btn{padding:6px 12px;background:transparent;border:1px solid rgba(255,255,255,.1);border-radius:8px;color:rgba(255,255,255,.4);cursor:pointer;font-size:13px;transition:all .2s}
.logout-btn:hover{border-color:#f87171;color:#f87171}
.content{flex:1;max-width:1100px;width:100%;margin:0 auto;padding:32px 24px}
.page-title{font-size:22px;font-weight:600;margin-bottom:24px;color:#fff;display:flex;align-items:center;gap:12px}
.admin-badge{font-size:11px;padding:3px 10px;background:rgba(240,160,80,.15);color:#f0a050;border:1px solid rgba(240,160,80,.3);border-radius:99px;font-weight:500;letter-spacing:.5px}
.loading,.empty{color:rgba(255,255,255,.35);text-align:center;padding:60px;font-size:15px}
.search-bar{display:flex;gap:8px;margin-bottom:28px}
.search-bar input{flex:1;padding:10px 16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:10px;color:#fff;font-size:14px;outline:none}
.search-bar input::placeholder{color:rgba(255,255,255,.25)}
.search-bar button{padding:10px 20px;background:rgba(124,92,191,.5);border:none;border-radius:10px;color:#fff;cursor:pointer;font-size:14px;transition:opacity .2s}
.search-bar button:hover{opacity:.8}
.reset-btn{background:rgba(255,255,255,.08)!important}
.product-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.product-card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:20px;display:flex;flex-direction:column;gap:8px;transition:border-color .2s,transform .2s}
.product-card:hover{border-color:rgba(124,92,191,.4);transform:translateY(-2px)}
.product-category{font-size:11px;color:#7c5cbf;text-transform:uppercase;letter-spacing:1px}
.product-name{font-size:16px;font-weight:600;color:#fff}
.product-desc{font-size:13px;color:rgba(255,255,255,.4);line-height:1.5;flex:1}
.product-footer{display:flex;align-items:center;justify-content:space-between;margin-top:8px}
.product-price{font-size:20px;font-weight:700;color:#f0a050}
.add-btn{padding:7px 14px;background:rgba(124,92,191,.4);border:1px solid rgba(124,92,191,.5);border-radius:8px;color:#fff;cursor:pointer;font-size:13px;transition:all .2s}
.add-btn:hover{background:rgba(124,92,191,.7)}
.cart-item{display:flex;align-items:center;gap:16px;padding:16px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:12px;margin-bottom:10px}
.cart-item-name{flex:1;font-size:15px;color:#fff}
.cart-item-controls{display:flex;align-items:center;gap:12px}
.qty-btn{width:28px;height:28px;background:rgba(255,255,255,.08);border:none;border-radius:6px;color:#fff;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center}
.qty{min-width:24px;text-align:center;font-size:15px}
.cart-item-price{font-size:16px;font-weight:600;color:#f0a050;min-width:80px;text-align:right}
.remove-btn{padding:5px 10px;background:transparent;border:1px solid rgba(248,113,113,.3);border-radius:7px;color:#f87171;cursor:pointer;font-size:12px;transition:all .2s}
.remove-btn:hover{background:rgba(248,113,113,.1)}
.cart-total{display:flex;justify-content:space-between;align-items:center;padding:16px 0;border-top:1px solid rgba(255,255,255,.07);margin-top:8px;font-size:15px;color:rgba(255,255,255,.6)}
.total-price{font-size:24px;font-weight:700;color:#f0a050}
.checkout-btn{display:block;width:100%;margin-top:16px;padding:14px;background:linear-gradient(135deg,#7c5cbf,#5b8af0);border:none;border-radius:12px;color:#fff;font-size:16px;font-weight:600;cursor:pointer;transition:opacity .2s}
.checkout-btn:hover{opacity:.85}
.checkout-btn:disabled{opacity:.4;cursor:not-allowed}
.checkout-section h3{font-size:14px;color:rgba(255,255,255,.5);margin:0 0 12px}
.address-item{padding:14px 16px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:12px;margin-bottom:8px;cursor:pointer;transition:all .2s}
.address-item:hover{border-color:rgba(124,92,191,.4)}
.address-item.selected{border-color:#7c5cbf;background:rgba(124,92,191,.1)}
.addr-name{font-size:14px;font-weight:600;color:#fff;margin-bottom:4px}
.addr-detail{font-size:13px;color:rgba(255,255,255,.5)}
.order-summary{padding:16px;background:rgba(255,255,255,.03);border-radius:12px;margin:20px 0 0}
.summary-row{display:flex;justify-content:space-between;font-size:15px;color:rgba(255,255,255,.6)}
.order-item{display:flex;align-items:center;gap:16px;padding:16px 20px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:12px;margin-bottom:10px}
.order-id{flex:1;color:rgba(255,255,255,.6);font-size:14px}
.order-price{font-size:18px;font-weight:700;color:#f0a050}
.order-status{padding:4px 12px;border-radius:99px;font-size:12px}
.order-status.paid{background:rgba(20,160,100,.2);color:#4ade80}
.order-status.pending{background:rgba(240,160,80,.2);color:#fbbf24}
.ai-page{display:flex;flex-direction:column;height:calc(100vh - 60px);padding-bottom:0}
.chat-window{flex:1;overflow-y:auto;padding:20px 0;display:flex;flex-direction:column;gap:12px}
.chat-hint{color:rgba(255,255,255,.25);font-size:14px;line-height:2.2;padding:40px 0}
.chat-msg{display:flex}
.chat-msg.user{justify-content:flex-end}
.chat-msg.ai{justify-content:flex-start}
.msg-bubble{max-width:70%;padding:12px 16px;border-radius:14px;font-size:14px;line-height:1.6}
.chat-msg.user .msg-bubble{background:rgba(124,92,191,.5);color:#fff;border-bottom-right-radius:4px}
.chat-msg.ai .msg-bubble{background:rgba(255,255,255,.06);color:#e8e8e8;border-bottom-left-radius:4px}
.typing{color:rgba(255,255,255,.4);font-style:italic}
.chat-input-row{display:flex;gap:8px;padding:16px 0 24px}
.chat-input-row input{flex:1;padding:12px 16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:12px;color:#fff;font-size:14px;outline:none}
.chat-input-row input:focus{border-color:rgba(124,92,191,.5)}
.chat-input-row input::placeholder{color:rgba(255,255,255,.25)}
.chat-input-row button{padding:12px 24px;background:rgba(124,92,191,.5);border:none;border-radius:12px;color:#fff;cursor:pointer;font-size:14px;transition:opacity .2s}
.chat-input-row button:hover{opacity:.8}
.chat-input-row button:disabled{opacity:.4;cursor:not-allowed}
</style>