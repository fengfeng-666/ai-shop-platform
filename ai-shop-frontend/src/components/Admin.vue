<template>
  <div class="admin">
    <div class="admin-tabs">
      <button :class="{ active: panel === 'product' }" @click="panel = 'product'">添加商品</button>
      <button :class="{ active: panel === 'knowledge' }" @click="panel = 'knowledge'">知识库管理</button>
    </div>

    <!-- 添加商品 -->
    <div v-if="panel === 'product'" class="panel">
      <h3 class="panel-title">添加新商品</h3>
      <div class="form-grid">
        <div class="field">
          <label>商品名称</label>
          <input v-model="product.name" placeholder="请输入商品名称" />
        </div>
        <div class="field">
          <label>价格 (¥)</label>
          <input v-model.number="product.price" type="number" placeholder="0.00" />
        </div>
        <div class="field">
          <label>库存</label>
          <input v-model.number="product.stock" type="number" placeholder="0" />
        </div>
        <div class="field">
          <label>分类</label>
          <input v-model="product.category" placeholder="如：数码、服装、食品" />
        </div>
        <div class="field full">
          <label>商品描述</label>
          <textarea v-model="product.description" placeholder="请输入商品描述" rows="3"></textarea>
        </div>
      </div>
      <div v-if="productMsg" class="msg" :class="productMsgType">{{ productMsg }}</div>
      <button class="submit-btn" @click="addProduct" :disabled="productLoading">
        {{ productLoading ? '提交中...' : '添加商品' }}
      </button>
    </div>

    <!-- 知识库管理 -->
    <div v-if="panel === 'knowledge'" class="panel">
      <h3 class="panel-title">添加知识库内容</h3>
      <p class="panel-desc">每行一条知识，AI 助手将基于这些内容回答用户问题</p>
      <div class="field">
        <label>知识内容</label>
        <textarea v-model="knowledgeText" placeholder="每行输入一条知识，例如：&#10;本店主营电子产品，提供一年质保&#10;所有商品支持7天无理由退换货" rows="8"></textarea>
      </div>
      <div v-if="knowledgeMsg" class="msg" :class="knowledgeMsgType">{{ knowledgeMsg }}</div>
      <button class="submit-btn" @click="addKnowledge" :disabled="knowledgeLoading">
        {{ knowledgeLoading ? '提交中...' : '添加到知识库' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const token = localStorage.getItem('token')
const headers = { Authorization: 'Bearer ' + token }

const panel = ref('product')

// 商品
const product = ref({ name: '', price: 0, stock: 0, category: '', description: '' })
const productLoading = ref(false)
const productMsg = ref('')
const productMsgType = ref('success')

const addProduct = async () => {
  if (!product.value.name || !product.value.category) {
    productMsg.value = '请填写商品名称和分类'
    productMsgType.value = 'error'
    return
  }
  productLoading.value = true
  productMsg.value = ''
  try {
    await axios.post('/api/product/', product.value, { headers })
    productMsg.value = '商品添加成功！'
    productMsgType.value = 'success'
    product.value = { name: '', price: 0, stock: 0, category: '', description: '' }
  } catch {
    productMsg.value = '添加失败，请检查权限'
    productMsgType.value = 'error'
  } finally {
    productLoading.value = false
  }
}

// 知识库
const knowledgeText = ref('')
const knowledgeLoading = ref(false)
const knowledgeMsg = ref('')
const knowledgeMsgType = ref('success')

const addKnowledge = async () => {
  const texts = knowledgeText.value.split('\n').map(s => s.trim()).filter(Boolean)
  if (texts.length === 0) {
    knowledgeMsg.value = '请输入至少一条知识'
    knowledgeMsgType.value = 'error'
    return
  }
  knowledgeLoading.value = true
  knowledgeMsg.value = ''
  try {
    await axios.post('/api/knowledge/add', { texts }, { headers })
    knowledgeMsg.value = `成功添加 ${texts.length} 条知识`
    knowledgeMsgType.value = 'success'
    knowledgeText.value = ''
  } catch {
    knowledgeMsg.value = '添加失败，请检查权限'
    knowledgeMsgType.value = 'error'
  } finally {
    knowledgeLoading.value = false
  }
}
</script>

<style scoped>
.admin { padding: 0; }
.admin-tabs { display: flex; gap: 4px; background: rgba(255,255,255,0.04); border-radius: 12px; padding: 4px; margin-bottom: 24px; width: fit-content; }
.admin-tabs button { padding: 8px 20px; background: transparent; border: none; color: rgba(255,255,255,0.45); border-radius: 9px; cursor: pointer; font-size: 14px; transition: all 0.2s; }
.admin-tabs button.active { background: rgba(124,92,191,0.35); color: #fff; }
.panel { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 16px; padding: 28px; }
.panel-title { font-size: 17px; font-weight: 600; color: #fff; margin-bottom: 6px; }
.panel-desc { font-size: 13px; color: rgba(255,255,255,0.35); margin-bottom: 20px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field.full { grid-column: 1 / -1; }
.field label { font-size: 12px; color: rgba(255,255,255,0.45); letter-spacing: 0.5px; }
.field input, .field textarea { padding: 10px 14px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; color: #fff; font-size: 14px; outline: none; resize: vertical; font-family: inherit; transition: border-color 0.2s; }
.field input:focus, .field textarea:focus { border-color: rgba(124,92,191,0.5); }
.field input::placeholder, .field textarea::placeholder { color: rgba(255,255,255,0.2); }
.msg { padding: 10px 14px; border-radius: 8px; font-size: 13px; margin-bottom: 14px; }
.msg.success { background: rgba(74,222,128,0.1); color: #4ade80; border: 1px solid rgba(74,222,128,0.2); }
.msg.error { background: rgba(248,113,113,0.1); color: #f87171; border: 1px solid rgba(248,113,113,0.2); }
.submit-btn { padding: 11px 28px; background: linear-gradient(135deg, #7c5cbf, #5b8af0); border: none; border-radius: 10px; color: #fff; font-size: 14px; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }
.submit-btn:hover { opacity: 0.85; }
.submit-btn:disabled { opacity: 0.45; cursor: not-allowed; }
</style>