<template>
  <div class="shop">
    <!-- 顶部标题栏 -->
    <header class="topbar">
      <div class="brand" @click="tab = 'shop'">
        <svg class="brand-logo" viewBox="0 0 64 64" fill="none">
          <defs>
            <linearGradient id="lgt" x1="0" y1="0" x2="64" y2="64">
              <stop offset="0%" stop-color="#7C5CBF"/>
              <stop offset="100%" stop-color="#5B8AF0"/>
            </linearGradient>
          </defs>
          <rect x="20" y="8" width="24" height="24" rx="5" fill="url(#lgt)" transform="rotate(45 32 20)"/>
          <circle cx="22" cy="26" r="3" fill="#fff" opacity="0.9"/>
          <circle cx="32" cy="20" r="2.5" fill="#fff" opacity="0.7"/>
          <circle cx="42" cy="26" r="3" fill="#fff" opacity="0.9"/>
          <line x1="22" y1="26" x2="32" y2="20" stroke="#fff" stroke-width="1" opacity="0.5"/>
          <line x1="32" y1="20" x2="42" y2="26" stroke="#fff" stroke-width="1" opacity="0.5"/>
          <rect x="16" y="44" width="32" height="5" rx="2.5" fill="url(#lgt)"/>
        </svg>
        <span class="brand-text">灵境商坊</span>
      </div>
      <div class="user-info">
        <button class="logout-btn" @click="logout">退出</button>
      </div>
    </header>

    <transition name="fade" mode="out-in">
      <!-- 商城 -->
      <main v-if="tab === 'shop'" key="shop" class="content">
        <div class="hero">
          <div class="hero-glow"></div>
          <h2>AI 智能购物体验</h2>
          <p>搜索商品、智能推荐，让 AI 帮你找到心仪好物</p>
        </div>
        <div class="search-bar">
          <span class="search-icon">&#8981;</span>
          <input v-model="keyword" placeholder="搜索你想要的商品..." @keyup.enter="searchProducts" />
          <button class="search-btn" @click="searchProducts">搜索</button>
          <button class="reset-btn" @click="loadProducts">全部</button>
        </div>
        <div v-if="loading" class="status">
          <span class="spinner"></span>
          <span>加载中...</span>
        </div>
        <div v-else-if="products.length === 0" class="status">
          <div class="empty-icon">&#9730;</div>
          <div>暂无商品，请等待商家上架</div>
        </div>
        <div v-else class="product-grid">
          <div v-for="item in products" :key="item.id" class="product-card">
            <div class="card-img" :style="{ background: imgGradient(item.id) }">
              <span class="card-img-letter">{{ item.name.charAt(0) }}</span>
            </div>
            <div class="card-body">
              <span class="product-category">{{ item.category }}</span>
              <div class="product-name">{{ item.name }}</div>
              <div class="product-desc">{{ item.description }}</div>
              <div class="product-footer">
                <span class="product-price">&yen;{{ item.price }}</span>
                <button class="add-btn" @click="addToCart(item.id)">
                  <span>+</span> 加入购物车
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- 购物车 -->
      <main v-else-if="tab === 'cart'" key="cart" class="content">
        <h2 class="page-title">购物车</h2>
        <div v-if="!cart.items || cart.items.length === 0" class="status">
          <div class="empty-icon">&#9731;</div>
          <div>购物车是空的，去商城逛逛吧</div>
        </div>
        <div v-else>
          <div v-for="item in cart.items" :key="item.product_id" class="cart-item">
            <div class="cart-item-img" :style="{ background: imgGradient(item.product_id) }">
              {{ item.name.charAt(0) }}
            </div>
            <div class="cart-item-name">{{ item.name }}</div>
            <div class="cart-item-controls">
              <button class="qty-btn" @click="updateQty(item, item.quantity - 1)">&#8722;</button>
              <span class="qty">{{ item.quantity }}</span>
              <button class="qty-btn" @click="updateQty(item, item.quantity + 1)">+</button>
            </div>
            <div class="cart-item-price">&yen;{{ item.subtotal }}</div>
            <button class="remove-btn" @click="removeFromCart(item.product_id)">&#10005;</button>
          </div>
          <div class="cart-total">
            <span>合计</span>
            <span class="total-price">&yen;{{ cart.total_price }}</span>
          </div>
          <button class="checkout-btn" @click="tab = 'checkout'">去结算</button>
        </div>
      </main>

      <!-- 结算 -->
      <main v-else-if="tab === 'checkout'" key="checkout" class="content">
        <h2 class="page-title">确认订单</h2>
        <div class="checkout-section">
          <h3>选择收货地址</h3>
          <div v-if="addresses.length === 0" class="status" style="padding:24px">
            <div>暂无地址，请在个人主页添加</div>
          </div>
          <div v-for="a in addresses" :key="a.id" class="address-card" :class="{ selected: addressId === a.id }" @click="addressId = a.id">
            <div class="addr-radio"><span v-if="addressId === a.id"></span></div>
            <div>
              <div class="addr-name">{{ a.name }} <span class="addr-phone">{{ a.phone }}</span></div>
              <div class="addr-detail">{{ a.detail }}</div>
            </div>
          </div>
          <div class="order-summary">
            <div class="summary-row"><span>商品合计</span><span class="total-price">&yen;{{ cart.total_price }}</span></div>
          </div>
          <button class="checkout-btn" :disabled="!addressId" @click="pay">&#9745; 确认支付</button>
        </div>
      </main>

      <!-- 订单 -->
      <main v-else-if="tab === 'orders'" key="orders" class="content">
        <h2 class="page-title">我的订单</h2>
        <div v-if="orders.length === 0" class="status">
          <div class="empty-icon">&#9732;</div>
          <div>暂无订单</div>
        </div>
        <div v-for="o in orders" :key="o.id" class="order-card">
          <div class="order-left">
            <div class="order-id">订单 #{{ o.id }}</div>
          </div>
          <div class="order-right">
            <div class="order-price">&yen;{{ o.price }}</div>
            <span class="order-status" :class="o.status">{{ o.status === 'paid' ? '已支付' : '待支付' }}</span>
          </div>
        </div>
      </main>

      <!-- AI 助手 -->
      <main v-else-if="tab === 'ai'" key="ai" class="content ai-page">
        <h2 class="page-title">AI 购物助手</h2>
        <div class="chat-window" ref="chatWindow">
          <div v-if="messages.length === 0" class="chat-hint">
            <div class="hint-icon">&#9733;</div>
            <div class="hint-text">
              <p>试试这些：</p>
              <span class="hint-tag" @click="aiInput = '帮我找运动鞋'; sendAI()">帮我找运动鞋</span>
              <span class="hint-tag" @click="aiInput = '推荐一些数码产品'; sendAI()">推荐数码产品</span>
              <span class="hint-tag" @click="aiInput = '帮我下单最便宜的商品'; sendAI()">帮我下单最便宜的商品</span>
            </div>
          </div>
          <div v-for="(m, i) in messages" :key="i" class="chat-msg" :class="m.role">
            <div class="msg-bubble">{{ m.content }}</div>
          </div>
          <div v-if="aiLoading" class="chat-msg ai">
            <div class="msg-bubble typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
        <div class="chat-input-row">
          <input v-model="aiInput" placeholder="输入消息，AI 帮你购物..." @keyup.enter="sendAI" :disabled="aiLoading" />
          <button @click="sendAI" :disabled="aiLoading">
            <span v-if="!aiLoading">发送</span>
            <span v-else class="spinner-sm"></span>
          </button>
        </div>
      </main>

      <!-- 个人主页 -->
      <main v-else-if="tab === 'profile'" key="profile" class="content">
        <h2 class="page-title">我的</h2>
        <Profile :is-admin="isAdmin" />
      </main>
    </transition>

    <!-- 底部导航栏 -->
    <nav class="bottom-nav">
      <button
        v-for="item in navItems"
        :key="item.key"
        :class="{ active: tab === item.key }"
        @click="tab = item.key"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span class="nav-label">
          {{ item.label }}
          <span v-if="item.key === 'cart' && cartCount > 0" class="badge">{{ cartCount }}</span>
        </span>
      </button>
      <button :class="{ active: tab === 'profile' }" @click="tab = 'profile'">
        <span class="nav-icon">
          <span class="avatar-sm">{{ username.charAt(0) }}</span>
        </span>
        <span class="nav-label">我的</span>
      </button>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import axios from 'axios'
import Profile from './Profile.vue'

const emit = defineEmits(['logout'])
const tab = ref('shop')
const username = ref(localStorage.getItem('username') || '用户')
const token = localStorage.getItem('token')
const headers = { Authorization: 'Bearer ' + token }

const parseToken = (t) => { try { return JSON.parse(atob(t.split('.')[1])) } catch { return {} } }
const tokenPayload = parseToken(token)
const isAdmin = computed(() => tokenPayload.role === 'admin')

const navItems = [
  { key: 'shop', label: '商城', icon: '◇' },
  { key: 'cart', label: '购物车', icon: '▥' },
  { key: 'orders', label: '订单', icon: '▦' },
  { key: 'ai', label: 'AI助手', icon: '✦' },
]

const colors = ['#7c5cbf,#5b8af0', '#f093fb,#f5576c', '#4facfe,#00f2fe', '#43e97b,#38f9d7', '#fa709a,#fee140', '#a18cd1,#fbc2eb', '#fccb90,#d57eeb', '#667eea,#764ba2']
const imgGradient = (id) => { const c = colors[id % colors.length]; return `linear-gradient(135deg,${c})` }

// 商品
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

// 购物车
const cart = ref({ items: [], total_price: 0 })
const cartCount = computed(() => cart.value.items?.length || 0)
const loadCart = async () => { try { const res = await axios.get('/api/cart/detail', { headers }); cart.value = res.data } catch {} }
const addToCart = async (id) => { await axios.post('/api/cart/add', null, { params: { product_id: id, quantity: 1 }, headers }); loadCart() }
const updateQty = async (item, qty) => { if (qty <= 0) return removeFromCart(item.product_id); await axios.put('/api/cart/update', null, { params: { product_id: item.product_id, quantity: qty }, headers }); loadCart() }
const removeFromCart = async (id) => { await axios.delete('/api/cart/delete', { params: { product_id: id }, headers }); loadCart() }

// 结算
const addresses = ref([])
const addressId = ref(null)
const loadAddresses = async () => { try { const res = await axios.get('/api/address/', { headers }); addresses.value = res.data } catch {} }
const pay = async () => {
  try { await axios.post('/api/order/pay', null, { params: { address_id: addressId.value }, headers }); alert('支付成功！'); loadCart(); tab.value = 'orders'; loadOrders() }
  catch { alert('支付失败，请重试') }
}

// 订单
const orders = ref([])
const loadOrders = async () => { try { const res = await axios.get('/api/order/list', { headers }); orders.value = res.data } catch {} }

// AI
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
/* 全局 */
.shop { min-height: 100vh; background: linear-gradient(180deg, #08080F 0%, #0c0c16 100%); color: #e8e8e8; display: flex; flex-direction: column; }

/* 顶部栏 */
.topbar {
  display: flex; align-items: center; justify-content: space-between; gap: 20px;
  padding: 0 28px; height: 56px;
  background: rgba(12,12,18,0.85); border-bottom: 1px solid rgba(255,255,255,0.06);
  position: sticky; top: 0; z-index: 100; backdrop-filter: blur(16px);
}
.brand { display: flex; align-items: center; gap: 10px; cursor: pointer; flex-shrink: 0; }
.brand-logo { width: 30px; height: 30px; }
.brand-text {
  font-size: 16px; font-weight: 700; letter-spacing: 3px;
  background: linear-gradient(135deg, #c9b8f0, #8bb0f8);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.user-info { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.logout-btn {
  padding: 6px 12px; background: transparent; border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px; color: rgba(255,255,255,0.4); cursor: pointer; font-size: 12px; transition: all 0.25s;
}
.logout-btn:hover { border-color: rgba(248,113,113,0.4); color: #f87171; }

/* 内容区 */
.content { flex: 1; max-width: 1120px; width: 100%; margin: 0 auto; padding: 32px 24px 80px; }

/* 底部导航栏 */
.bottom-nav {
  display: flex; justify-content: space-around; align-items: flex-start;
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 100;
  background: rgba(14,14,22,0.92); border-top: 1px solid rgba(255,255,255,0.08);
  padding: 8px 0 max(8px, env(safe-area-inset-bottom)); backdrop-filter: blur(16px);
}
.bottom-nav button {
  display: flex; flex-direction: column; align-items: center; gap: 4px;
  padding: 6px 16px; background: transparent; border: none;
  color: rgba(255,255,255,0.4); cursor: pointer;
  font-size: 10px; font-weight: 500; transition: all 0.25s ease;
  position: relative; min-width: 56px;
}
.bottom-nav button:hover { color: rgba(255,255,255,0.6); }
.bottom-nav button.active { color: #c9b8f0; }
.nav-icon { font-size: 20px; line-height: 1; }
.nav-label { position: relative; }
.avatar-sm {
  width: 20px; height: 20px; border-radius: 50%;
  background: linear-gradient(135deg, #7C5CBF, #5B8AF0);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 10px; font-weight: 600;
}
.badge {
  position: absolute; top: -8px; right: -14px; background: #f5576c; color: #fff;
  font-size: 10px; min-width: 16px; height: 16px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center; padding: 0 4px;
  box-shadow: 0 2px 8px rgba(245,87,108,0.3);
}

/* 淡入动画 */
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.fade-enter-from { opacity: 0; transform: translateY(8px); }
.fade-leave-to { opacity: 0; transform: translateY(-8px); }

/* Hero */
.hero {
  text-align: center; padding: 48px 20px 40px; border-radius: 20px;
  background: linear-gradient(135deg, rgba(124,92,191,0.08), rgba(91,138,240,0.06));
  border: 1px solid rgba(124,92,191,0.1); margin-bottom: 28px; position: relative; overflow: hidden;
}
.hero-glow {
  position: absolute; top: -50%; left: 50%; width: 300px; height: 300px; transform: translate(-50%,0);
  background: radial-gradient(circle, rgba(124,92,191,0.15), transparent 70%); pointer-events: none;
}
.hero h2 { font-size: 28px; font-weight: 700; color: #fff; margin-bottom: 8px; position: relative; }
.hero p { color: rgba(255,255,255,0.4); font-size: 15px; position: relative; }

/* 搜索栏 */
.search-bar { display: flex; gap: 8px; margin-bottom: 28px; position: relative; }
.search-icon { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: rgba(255,255,255,0.2); font-size: 18px; z-index: 1; pointer-events: none; }
.search-bar input {
  flex: 1; padding: 12px 16px 12px 44px; background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; color: #fff; font-size: 14px; outline: none; transition: all 0.3s;
}
.search-bar input:focus { border-color: rgba(124,92,191,0.5); background: rgba(255,255,255,0.06); box-shadow: 0 0 0 3px rgba(124,92,191,0.06); }
.search-bar input::placeholder { color: rgba(255,255,255,0.2); }
.search-btn { padding: 12px 24px; background: linear-gradient(135deg, #7C5CBF, #5B8AF0); border: none; border-radius: 14px; color: #fff; cursor: pointer; font-size: 14px; font-weight: 600; transition: all 0.3s; }
.search-btn:hover { box-shadow: 0 4px 16px rgba(124,92,191,0.3); transform: translateY(-1px); }
.reset-btn { padding: 12px 20px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; color: rgba(255,255,255,0.5); cursor: pointer; font-size: 14px; transition: all 0.3s; }
.reset-btn:hover { color: #fff; background: rgba(255,255,255,0.1); }

/* 状态 */
.status { text-align: center; padding: 80px 20px; color: rgba(255,255,255,0.3); font-size: 15px; }
.empty-icon { font-size: 40px; margin-bottom: 12px; opacity: 0.4; }
.spinner { width: 20px; height: 20px; border: 2px solid rgba(124,92,191,0.2); border-top-color: #7C5CBF; border-radius: 50%; animation: spin 0.6s linear infinite; display: inline-block; vertical-align: middle; margin-right: 8px; }
@keyframes spin { to { transform: rotate(360deg); } }

/* 商品网格 */
.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(256px, 1fr)); gap: 20px; }
.product-card {
  background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06); border-radius: 18px;
  overflow: hidden; transition: all 0.35s ease; cursor: pointer;
}
.product-card:hover { border-color: rgba(124,92,191,0.35); transform: translateY(-4px); box-shadow: 0 16px 40px rgba(0,0,0,0.3), 0 0 0 1px rgba(124,92,191,0.1); }
.card-img {
  height: 140px; display: flex; align-items: center; justify-content: center;
  font-size: 48px; font-weight: 700; color: rgba(255,255,255,0.3); position: relative; overflow: hidden;
}
.card-img::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(to bottom, transparent 50%, rgba(0,0,0,0.3));
}
.card-body { padding: 16px 18px 18px; }
.product-category {
  font-size: 11px; color: #7C5CBF; text-transform: uppercase; letter-spacing: 1.5px;
  font-weight: 600; background: rgba(124,92,191,0.12); padding: 2px 10px; border-radius: 99px; display: inline-block; margin-bottom: 8px;
}
.product-name { font-size: 16px; font-weight: 600; color: #fff; margin-bottom: 6px; }
.product-desc { font-size: 13px; color: rgba(255,255,255,0.35); line-height: 1.5; margin-bottom: 12px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.product-footer { display: flex; align-items: center; justify-content: space-between; }
.product-price { font-size: 22px; font-weight: 700; color: #f0a050; }
.add-btn {
  display: flex; align-items: center; gap: 4px; padding: 8px 16px;
  background: rgba(124,92,191,0.2); border: 1px solid rgba(124,92,191,0.3); border-radius: 10px;
  color: #fff; cursor: pointer; font-size: 13px; font-weight: 500; transition: all 0.3s;
}
.add-btn:hover { background: rgba(124,92,191,0.45); border-color: rgba(124,92,191,0.6); box-shadow: 0 4px 12px rgba(124,92,191,0.2); }

/* 购物车 */
.page-title { font-size: 24px; font-weight: 700; margin-bottom: 24px; color: #fff; display: flex; align-items: center; gap: 12px; }
.admin-badge { font-size: 11px; padding: 4px 12px; background: rgba(240,160,80,0.15); color: #f0a050; border: 1px solid rgba(240,160,80,0.3); border-radius: 99px; font-weight: 500; letter-spacing: 1px; }
.cart-item {
  display: flex; align-items: center; gap: 16px; padding: 18px 20px;
  background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px; margin-bottom: 10px; transition: all 0.3s;
}
.cart-item:hover { border-color: rgba(255,255,255,0.1); background: rgba(255,255,255,0.035); }
.cart-item-img {
  width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
  font-size: 20px; font-weight: 700; color: rgba(255,255,255,0.4); flex-shrink: 0;
}
.cart-item-name { flex: 1; font-size: 15px; color: #fff; font-weight: 500; }
.cart-item-controls { display: flex; align-items: center; gap: 14px; }
.qty-btn {
  width: 32px; height: 32px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px; color: #fff; cursor: pointer; font-size: 16px; display: flex; align-items: center; justify-content: center; transition: all 0.2s;
}
.qty-btn:hover { background: rgba(124,92,191,0.3); border-color: rgba(124,92,191,0.4); }
.qty { min-width: 28px; text-align: center; font-size: 15px; font-weight: 600; }
.cart-item-price { font-size: 16px; font-weight: 600; color: #f0a050; min-width: 90px; text-align: right; }
.remove-btn {
  width: 32px; height: 32px; background: transparent; border: 1px solid rgba(248,113,113,0.2);
  border-radius: 8px; color: #f87171; cursor: pointer; font-size: 14px; display: flex; align-items: center; justify-content: center; transition: all 0.2s;
}
.remove-btn:hover { background: rgba(248,113,113,0.1); border-color: rgba(248,113,113,0.4); }
.cart-total {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 0; border-top: 1px solid rgba(255,255,255,0.06); margin-top: 8px; font-size: 16px; color: rgba(255,255,255,0.5);
}
.total-price { font-size: 28px; font-weight: 700; color: #f0a050; }
.checkout-btn {
  display: block; width: 100%; margin-top: 16px; padding: 16px;
  background: linear-gradient(135deg, #7C5CBF, #5B8AF0); border: none; border-radius: 14px;
  color: #fff; font-size: 17px; font-weight: 600; cursor: pointer; transition: all 0.3s; letter-spacing: 1px;
}
.checkout-btn:hover { box-shadow: 0 8px 24px rgba(124,92,191,0.3); transform: translateY(-1px); }
.checkout-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }

/* 结算 */
.checkout-section h3 { font-size: 14px; color: rgba(255,255,255,0.4); margin: 0 0 14px; font-weight: 500; }
.address-card {
  display: flex; align-items: center; gap: 14px; padding: 16px 18px;
  background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07);
  border-radius: 14px; margin-bottom: 10px; cursor: pointer; transition: all 0.3s;
}
.address-card:hover { border-color: rgba(124,92,191,0.3); }
.address-card.selected { border-color: #7C5CBF; background: rgba(124,92,191,0.08); box-shadow: 0 0 0 2px rgba(124,92,191,0.15); }
.addr-radio {
  width: 20px; height: 20px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.2);
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.addr-radio span { width: 10px; height: 10px; border-radius: 50%; background: #7C5CBF; }
.address-card.selected .addr-radio { border-color: #7C5CBF; }
.addr-name { font-size: 14px; font-weight: 600; color: #fff; margin-bottom: 3px; }
.addr-phone { font-weight: 400; color: rgba(255,255,255,0.4); margin-left: 8px; font-size: 13px; }
.addr-detail { font-size: 13px; color: rgba(255,255,255,0.4); }
.order-summary { padding: 18px 20px; background: rgba(255,255,255,0.025); border-radius: 14px; margin: 20px 0 0; border: 1px solid rgba(255,255,255,0.06); }
.summary-row { display: flex; justify-content: space-between; align-items: center; font-size: 16px; color: rgba(255,255,255,0.5); }

/* 订单 */
.order-card {
  display: flex; justify-content: space-between; align-items: center; padding: 18px 22px;
  background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06);
  border-radius: 14px; margin-bottom: 10px; transition: all 0.3s;
}
.order-card:hover { border-color: rgba(255,255,255,0.1); }
.order-left { display: flex; align-items: center; gap: 14px; }
.order-id { color: rgba(255,255,255,0.5); font-size: 14px; font-weight: 500; }
.order-right { display: flex; align-items: center; gap: 16px; }
.order-price { font-size: 20px; font-weight: 700; color: #f0a050; }
.order-status { padding: 5px 14px; border-radius: 99px; font-size: 12px; font-weight: 500; }
.order-status.paid { background: rgba(74,222,128,0.12); color: #4ade80; }
.order-status.pending { background: rgba(240,160,80,0.12); color: #fbbf24; }

/* AI 页面 */
.ai-page { display: flex; flex-direction: column; height: calc(100vh - 56px - 32px - 80px); }
.chat-window { flex: 1; overflow-y: auto; padding: 24px 0; display: flex; flex-direction: column; gap: 14px; }
.chat-hint { text-align: center; padding: 60px 20px; }
.hint-icon { font-size: 42px; margin-bottom: 16px; opacity: 0.3; }
.hint-text p { color: rgba(255,255,255,0.25); font-size: 14px; margin-bottom: 12px; }
.hint-tag {
  display: inline-block; padding: 8px 16px; margin: 4px;
  background: rgba(124,92,191,0.12); border: 1px solid rgba(124,92,191,0.2);
  border-radius: 99px; color: rgba(255,255,255,0.5); font-size: 13px;
  cursor: pointer; transition: all 0.3s;
}
.hint-tag:hover { background: rgba(124,92,191,0.25); color: #fff; border-color: rgba(124,92,191,0.4); }
.chat-msg { display: flex; }
.chat-msg.user { justify-content: flex-end; }
.chat-msg.ai { justify-content: flex-start; }
.msg-bubble { max-width: 72%; padding: 12px 18px; border-radius: 16px; font-size: 14px; line-height: 1.65; word-break: break-word; }
.chat-msg.user .msg-bubble { background: linear-gradient(135deg, #7C5CBF, #5B8AF0); color: #fff; border-bottom-right-radius: 6px; }
.chat-msg.ai .msg-bubble { background: rgba(255,255,255,0.06); color: #e0e0e0; border-bottom-left-radius: 6px; border: 1px solid rgba(255,255,255,0.06); }
.typing { display: flex; align-items: center; gap: 5px; padding: 14px 18px; }
.typing span { width: 7px; height: 7px; border-radius: 50%; background: rgba(255,255,255,0.3); animation: bounce 1.4s ease infinite both; }
.typing span:nth-child(1) { animation-delay: -0.32s; }
.typing span:nth-child(2) { animation-delay: -0.16s; }
.typing span:nth-child(3) { animation-delay: 0s; }
@keyframes bounce { 0%,80%,100% { transform: scale(0.6); } 40% { transform: scale(1); } }
.chat-input-row { display: flex; gap: 8px; padding: 16px 0 24px; }
.chat-input-row input {
  flex: 1; padding: 14px 18px; background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; color: #fff; font-size: 14px; outline: none; transition: all 0.3s;
}
.chat-input-row input:focus { border-color: rgba(124,92,191,0.5); box-shadow: 0 0 0 3px rgba(124,92,191,0.06); }
.chat-input-row input::placeholder { color: rgba(255,255,255,0.2); }
.chat-input-row button {
  padding: 14px 28px; background: linear-gradient(135deg, #7C5CBF, #5B8AF0); border: none;
  border-radius: 14px; color: #fff; cursor: pointer; font-size: 14px; font-weight: 600; transition: all 0.3s; min-width: 72px;
}
.chat-input-row button:hover { box-shadow: 0 4px 16px rgba(124,92,191,0.3); }
.chat-input-row button:disabled { opacity: 0.4; cursor: not-allowed; }
.spinner-sm { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.6s linear infinite; display: inline-block; }
</style>
