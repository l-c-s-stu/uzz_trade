<template>
  <div class="order-detail-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container nav-content">
        <router-link to="/" class="logo">CampusTrade 🛒</router-link>
        <div class="nav-links">
          <router-link to="/orders" class="nav-link">我的订单</router-link>
          <router-link to="/goods/create" class="nav-link">发布商品</router-link>
          <router-link to="/user" class="nav-link">个人中心</router-link>
          <router-link v-if="isAdmin" to="/admin" class="nav-link admin-link">管理后台</router-link>
          <span v-if="isLoggedIn" class="user-info">欢迎，{{ username }}</span>
          <button v-if="isLoggedIn" @click="handleLogout" class="btn btn-danger">
            退出登录
          </button>
          <router-link v-else to="/login" class="btn btn-primary">登录</router-link>
        </div>
      </div>
    </nav>

    <div class="container">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <div class="ios-spinner"></div>
        <p>正在加载订单详情...</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <div class="error-actions">
          <button @click="loadOrderDetail" class="btn btn-primary">重试</button>
          <router-link to="/orders" class="btn btn-outline">返回订单列表</router-link>
        </div>
      </div>

      <!-- 订单详情 -->
      <div v-else-if="order" class="order-detail">
        <!-- 订单状态卡片 -->
        <div class="status-card ios-card">
          <div class="status-header">
            <h2 class="status-title">订单状态</h2>
            <span :class="['status-badge', `status-${order.pay_status.toLowerCase()}`]">
              {{ order.pay_status_display }}
            </span>
          </div>
          <div class="status-info">
            <p v-if="order.pay_status === 'WAIT'" class="status-tip">
              订单已创建，请尽快完成支付
            </p>
            <p v-else-if="order.pay_status === 'SUCCESS'" class="status-tip success">
              订单已支付成功，商品状态已更新为"已出"
            </p>
            <p v-else class="status-tip">
              订单已取消
            </p>
          </div>
        </div>

        <!-- 订单信息卡片 -->
        <div class="info-card ios-card">
          <h3 class="card-title">订单信息</h3>
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">订单号：</span>
              <span class="info-value">{{ order.order_sn }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">创建时间：</span>
              <span class="info-value">{{ formatDate(order.add_time) }}</span>
            </div>
            <div v-if="order.pay_time" class="info-item">
              <span class="info-label">支付时间：</span>
              <span class="info-value">{{ formatDate(order.pay_time) }}</span>
            </div>
            <div v-if="order.trade_no" class="info-item">
              <span class="info-label">交易流水号：</span>
              <span class="info-value">{{ order.trade_no }}</span>
            </div>
            <div v-if="order.post_script" class="info-item">
              <span class="info-label">订单留言：</span>
              <span class="info-value">{{ order.post_script }}</span>
            </div>
          </div>
        </div>

        <!-- 商品信息卡片 -->
        <div class="goods-card ios-card">
          <h3 class="card-title">商品信息</h3>
          <div class="goods-content">
            <router-link :to="`/goods/${order.goods}`" class="goods-link">
              <img
                :src="order.goods_image || '/placeholder.png'"
                :alt="order.goods_title"
                class="goods-image"
                @error="handleImageError"
              />
              <div class="goods-info">
                <h4 class="goods-title">{{ order.goods_title }}</h4>
                <p class="goods-price">¥{{ order.order_mount }}</p>
              </div>
            </router-link>
          </div>
        </div>

        <!-- 金额信息卡片 -->
        <div class="amount-card ios-card">
          <div class="amount-row">
            <span class="amount-label">商品金额：</span>
            <span class="amount-value">¥{{ order.order_mount }}</span>
          </div>
          <div class="amount-row total">
            <span class="amount-label">订单总额：</span>
            <span class="amount-value">¥{{ order.order_mount }}</span>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <button
            v-if="order.pay_status === 'WAIT'"
            @click="handlePayOrder"
            class="btn btn-primary btn-large"
            :disabled="paying"
          >
            <span v-if="paying">支付中...</span>
            <span v-else>立即支付</span>
          </button>
          <button
            v-if="order.pay_status === 'WAIT'"
            @click="handleCancelOrder"
            class="btn btn-outline btn-large"
            :disabled="canceling"
          >
            <span v-if="canceling">取消中...</span>
            <span v-else>取消订单</span>
          </button>
          <router-link to="/orders" class="btn btn-outline btn-large">
            返回订单列表
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ordersAPI, authAPI } from '@/utils/api'

const router = useRouter()
const route = useRoute()

// 状态管理
const loading = ref(false)
const error = ref('')
const order = ref(null)
const paying = ref(false)
const canceling = ref(false)

// 登录状态
const isLoggedIn = computed(() => authAPI.isLoggedIn())
const username = computed(() => localStorage.getItem('username') || '')
const isAdmin = ref(false)

// 获取订单ID
const orderId = computed(() => route.params.id)

// 加载订单详情
const loadOrderDetail = async () => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await ordersAPI.getOrderDetail(orderId.value)
    if (response.data) {
      order.value = response.data
    }
  } catch (err) {
    console.error('加载订单详情失败:', err)
    if (err.response?.status === 401) {
      error.value = '请先登录'
      router.push('/login')
    } else if (err.response?.status === 404) {
      error.value = '订单不存在'
    } else {
      error.value = err.response?.data?.detail || err.response?.data?.message || '加载订单详情失败'
    }
  } finally {
    loading.value = false
  }
}

// 支付订单
const handlePayOrder = async () => {
  if (!confirm('确认支付此订单？')) {
    return
  }

  paying.value = true
  try {
    const response = await ordersAPI.payOrder(orderId.value)
    if (response.data) {
      alert('支付成功！')
      // 重新加载订单详情
      await loadOrderDetail()
    }
  } catch (err) {
    console.error('支付失败:', err)
    const errorMsg = err.response?.data?.detail || err.response?.data?.message || '支付失败'
    alert(errorMsg)
  } finally {
    paying.value = false
  }
}

// 取消订单
const handleCancelOrder = async () => {
  if (!confirm('确认取消此订单？取消后无法恢复。')) {
    return
  }

  canceling.value = true
  try {
    const response = await ordersAPI.cancelOrder(orderId.value)
    if (response.data) {
      alert('订单已取消')
      // 重新加载订单详情
      await loadOrderDetail()
    }
  } catch (err) {
    console.error('取消订单失败:', err)
    const errorMsg = err.response?.data?.detail || err.response?.data?.message || '取消订单失败'
    alert(errorMsg)
  } finally {
    canceling.value = false
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 处理图片加载错误
const handleImageError = (e) => {
  e.target.src = '/placeholder.png'
}

// 退出登录
const handleLogout = () => {
  if (confirm('确认退出登录？')) {
    authAPI.logout()
    router.push('/')
  }
}

// 检查管理员权限
const checkAdminStatus = async () => {
  if (isLoggedIn.value) {
    try {
      const response = await authAPI.getProfile()
      if (response.data) {
        isAdmin.value = response.data.is_staff || response.data.is_superuser || false
      }
    } catch (err) {
      console.error('获取用户信息失败:', err)
      isAdmin.value = false
    }
  }
}

// 组件挂载时加载订单详情
onMounted(() => {
  if (isLoggedIn.value) {
    checkAdminStatus()
    loadOrderDetail()
  } else {
    router.push('/login')
  }
})
</script>

<style scoped>
.order-detail-page {
  min-height: 100vh;
  background-color: var(--ios-bg-primary);
  font-family: var(--ios-font-family);
  padding-bottom: var(--ios-spacing-xl);
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 var(--ios-spacing-md);
}

/* 导航栏 - iOS 风格 */
.navbar {
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 0.5px solid var(--ios-separator);
  position: sticky;
  top: 0;
  z-index: 1000;
  padding: var(--ios-spacing-md) 0;
  margin-bottom: var(--ios-spacing-lg);
  box-shadow: 0 0.5px 0 rgba(0, 0, 0, 0.1);
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  color: var(--ios-blue);
  letter-spacing: -0.3px;
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: var(--ios-spacing-md);
}

.nav-link {
  margin-left: var(--ios-spacing-lg);
  font-weight: 500;
  color: var(--ios-text-secondary);
  text-decoration: none;
  transition: color var(--ios-transition-fast);
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--ios-blue);
}

.admin-link {
  color: var(--ios-purple);
  font-weight: 600;
}

.admin-link.router-link-active {
  color: var(--ios-purple);
}

.user-info {
  color: var(--ios-text-secondary);
  font-size: var(--ios-font-size-subhead);
}

/* 卡片通用样式 */
.ios-card {
  background-color: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-lg);
  box-shadow: var(--ios-shadow-sm);
  padding: var(--ios-spacing-lg);
  margin-bottom: var(--ios-spacing-md);
  border: 0.5px solid var(--ios-separator);
}

.card-title {
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  color: var(--ios-text-primary);
  margin-bottom: var(--ios-spacing-md);
}

/* 状态卡片 */
.status-card {
  text-align: center;
}

.status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--ios-spacing-md);
}

.status-title {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  color: var(--ios-text-primary);
}

.status-badge {
  padding: 6px 16px;
  border-radius: var(--ios-radius-full);
  font-size: var(--ios-font-size-body);
  font-weight: 600;
}

.status-wait {
  background-color: rgba(255, 149, 0, 0.1);
  color: var(--ios-orange);
}

.status-success {
  background-color: rgba(52, 199, 89, 0.1);
  color: var(--ios-green);
}

.status-cancel {
  background-color: rgba(142, 142, 147, 0.1);
  color: var(--ios-text-tertiary);
}

.status-tip {
  font-size: var(--ios-font-size-body);
  color: var(--ios-text-secondary);
}

.status-tip.success {
  color: var(--ios-green);
}

/* 信息列表 */
.info-list {
  display: flex;
  flex-direction: column;
  gap: var(--ios-spacing-md);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: var(--ios-spacing-md);
  border-bottom: 0.5px solid var(--ios-separator);
}

.info-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.info-label {
  font-size: var(--ios-font-size-body);
  color: var(--ios-text-secondary);
  font-weight: 500;
}

.info-value {
  font-size: var(--ios-font-size-body);
  color: var(--ios-text-primary);
  text-align: right;
  flex: 1;
  margin-left: var(--ios-spacing-md);
}

/* 商品信息 */
.goods-content {
  margin-top: var(--ios-spacing-md);
}

.goods-link {
  display: flex;
  gap: var(--ios-spacing-md);
  text-decoration: none;
  color: inherit;
  transition: opacity var(--ios-transition-fast);
}

.goods-link:hover {
  opacity: 0.8;
}

.goods-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: var(--ios-radius-md);
  background-color: var(--ios-bg-tertiary);
}

.goods-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.goods-title {
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  color: var(--ios-text-primary);
  margin-bottom: var(--ios-spacing-sm);
}

.goods-price {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  color: var(--ios-red);
}

/* 金额信息 */
.amount-card {
  background-color: rgba(0, 122, 255, 0.05);
}

.amount-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--ios-spacing-sm) 0;
}

.amount-row.total {
  border-top: 1px solid var(--ios-separator);
  margin-top: var(--ios-spacing-sm);
  padding-top: var(--ios-spacing-md);
}

.amount-label {
  font-size: var(--ios-font-size-body);
  color: var(--ios-text-secondary);
}

.amount-value {
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  color: var(--ios-text-primary);
}

.amount-row.total .amount-value {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  color: var(--ios-red);
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: var(--ios-spacing-md);
  margin-top: var(--ios-spacing-lg);
}

.btn-large {
  width: 100%;
  padding: 14px 28px;
  font-size: var(--ios-font-size-body);
}

/* 加载和错误状态 */
.loading,
.error {
  text-align: center;
  padding: var(--ios-spacing-xl) var(--ios-spacing-md);
  color: var(--ios-text-secondary);
  font-size: var(--ios-font-size-body);
}

.error {
  color: var(--ios-red);
}

.error-actions {
  display: flex;
  gap: var(--ios-spacing-md);
  justify-content: center;
  margin-top: var(--ios-spacing-md);
}

/* 按钮 - iOS 风格 */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 24px;
  font-family: var(--ios-font-family);
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  line-height: 1.47059;
  border: none;
  border-radius: var(--ios-radius-md);
  cursor: pointer;
  transition: all var(--ios-transition-fast);
  text-decoration: none;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}

.btn-primary {
  background-color: var(--ios-blue);
  color: #FFFFFF;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--ios-blue-dark);
}

.btn-primary:active:not(:disabled) {
  background-color: var(--ios-blue-dark);
  opacity: 0.8;
  transform: scale(0.97);
}

.btn-outline {
  background-color: transparent;
  border: 1px solid var(--ios-blue);
  color: var(--ios-blue);
}

.btn-outline:hover:not(:disabled) {
  background-color: var(--ios-blue);
  color: #FFFFFF;
}

.btn-outline:active:not(:disabled) {
  background-color: var(--ios-blue);
  color: #FFFFFF;
  opacity: 0.8;
  transform: scale(0.97);
}

.btn-danger {
  background-color: var(--ios-red);
  color: #FFFFFF;
}

.btn-danger:hover:not(:disabled) {
  background-color: #D32F2F;
}

.btn-danger:active:not(:disabled) {
  background-color: #D32F2F;
  opacity: 0.8;
  transform: scale(0.97);
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 响应式 */
@media (max-width: 768px) {
  .status-header {
    flex-direction: column;
    gap: var(--ios-spacing-sm);
  }

  .goods-link {
    flex-direction: column;
  }

  .goods-image {
    width: 100%;
    height: 200px;
  }

  .error-actions {
    flex-direction: column;
  }
}
</style>

