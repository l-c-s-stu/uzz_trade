<template>
  <div class="order-list-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container nav-content">
        <router-link to="/" class="logo">CampusTrade 🛒</router-link>
        <div class="nav-links">
          <router-link to="/" class="nav-link">首页</router-link>
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
      <div class="page-header">
        <h1 class="section-title">我的订单</h1>
      </div>

      <!-- 状态筛选 -->
      <div class="filter-tabs">
        <button
          v-for="status in statusFilters"
          :key="status.value"
          :class="['filter-tab', { active: currentFilter === status.value }]"
          @click="currentFilter = status.value"
        >
          {{ status.label }}
        </button>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <div class="ios-spinner"></div>
        <p>正在加载订单...</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="loadOrders" class="btn btn-primary" style="margin-top: 10px;">
          重试
        </button>
      </div>

      <!-- 空状态 -->
      <div v-else-if="filteredOrders.length === 0" class="empty-state">
        <p>{{ currentFilter === 'all' ? '暂无订单' : `暂无${getStatusLabel(currentFilter)}订单` }}</p>
        <router-link to="/" class="btn btn-primary" style="margin-top: 10px;">
          去逛逛
        </router-link>
      </div>

      <!-- 订单列表 -->
      <div v-else class="orders-list">
        <div
          v-for="order in filteredOrders"
          :key="order.id"
          class="order-card ios-card"
          @click="goToOrderDetail(order.id)"
        >
          <div class="order-header">
            <div class="order-info">
              <span class="order-sn">订单号：{{ order.order_sn }}</span>
              <span class="order-time">{{ formatDate(order.add_time) }}</span>
            </div>
            <span :class="['order-status', `status-${order.pay_status.toLowerCase()}`]">
              {{ order.pay_status_display }}
            </span>
          </div>

          <div class="order-content">
            <div class="goods-info">
              <img
                :src="order.goods_image || '/placeholder.png'"
                :alt="order.goods_title"
                class="goods-image"
                @error="handleImageError"
              />
              <div class="goods-details">
                <h3 class="goods-title">{{ order.goods_title }}</h3>
                <p class="order-amount">¥{{ order.order_mount }}</p>
              </div>
            </div>
          </div>

          <div class="order-footer">
            <div class="order-actions">
              <button
                v-if="order.pay_status === 'WAIT'"
                @click.stop="handlePayOrder(order.id)"
                class="btn btn-primary btn-sm"
                :disabled="payingOrderId === order.id"
              >
                <span v-if="payingOrderId === order.id">支付中...</span>
                <span v-else>立即支付</span>
              </button>
              <button
                v-if="order.pay_status === 'WAIT'"
                @click.stop="handleCancelOrder(order.id)"
                class="btn btn-outline btn-sm"
                :disabled="cancelingOrderId === order.id"
              >
                <span v-if="cancelingOrderId === order.id">取消中...</span>
                <span v-else>取消订单</span>
              </button>
              <router-link
                :to="`/orders/${order.id}`"
                class="btn btn-outline btn-sm"
                @click.stop
              >
                查看详情
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ordersAPI, authAPI } from '@/utils/api'

const router = useRouter()

// 状态管理
const loading = ref(false)
const error = ref('')
const orders = ref([])
const currentFilter = ref('all')
const payingOrderId = ref(null)
const cancelingOrderId = ref(null)

// 登录状态
const isLoggedIn = computed(() => authAPI.isLoggedIn())
const username = computed(() => localStorage.getItem('username') || '')
const isAdmin = ref(false)

// 状态筛选选项
const statusFilters = [
  { label: '全部', value: 'all' },
  { label: '待支付', value: 'WAIT' },
  { label: '已支付', value: 'SUCCESS' },
  { label: '已取消', value: 'CANCEL' }
]

// 筛选后的订单列表
const filteredOrders = computed(() => {
  if (currentFilter.value === 'all') {
    return orders.value
  }
  return orders.value.filter(order => order.pay_status === currentFilter.value)
})

// 加载订单列表
const loadOrders = async () => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await ordersAPI.getOrders()
    if (response.data) {
      orders.value = Array.isArray(response.data) ? response.data : response.data.results || []
    }
  } catch (err) {
    console.error('加载订单失败:', err)
    if (err.response?.status === 401) {
      error.value = '请先登录'
      router.push('/login')
    } else {
      error.value = err.response?.data?.detail || err.response?.data?.message || '加载订单失败'
    }
  } finally {
    loading.value = false
  }
}

// 支付订单
const handlePayOrder = async (orderId) => {
  if (!confirm('确认支付此订单？')) {
    return
  }

  payingOrderId.value = orderId
  try {
    const response = await ordersAPI.payOrder(orderId)
    if (response.data) {
      alert('支付成功！')
      // 重新加载订单列表
      await loadOrders()
    }
  } catch (err) {
    console.error('支付失败:', err)
    const errorMsg = err.response?.data?.detail || err.response?.data?.message || '支付失败'
    alert(errorMsg)
  } finally {
    payingOrderId.value = null
  }
}

// 取消订单
const handleCancelOrder = async (orderId) => {
  if (!confirm('确认取消此订单？')) {
    return
  }

  cancelingOrderId.value = orderId
  try {
    const response = await ordersAPI.cancelOrder(orderId)
    if (response.data) {
      alert('订单已取消')
      // 重新加载订单列表
      await loadOrders()
    }
  } catch (err) {
    console.error('取消订单失败:', err)
    const errorMsg = err.response?.data?.detail || err.response?.data?.message || '取消订单失败'
    alert(errorMsg)
  } finally {
    cancelingOrderId.value = null
  }
}

// 跳转到订单详情
const goToOrderDetail = (orderId) => {
  router.push(`/orders/${orderId}`)
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
    minute: '2-digit'
  })
}

// 获取状态标签
const getStatusLabel = (status) => {
  const filter = statusFilters.find(f => f.value === status)
  return filter ? filter.label : ''
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

// 组件挂载时加载订单
onMounted(() => {
  if (isLoggedIn.value) {
    checkAdminStatus()
    loadOrders()
  } else {
    router.push('/login')
  }
})
</script>

<style scoped>
.order-list-page {
  min-height: 100vh;
  background-color: var(--ios-bg-primary);
  font-family: var(--ios-font-family);
  padding-bottom: var(--ios-spacing-xl);
}

.container {
  max-width: 1200px;
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

/* 页面标题 */
.page-header {
  margin-bottom: var(--ios-spacing-lg);
}

.section-title {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  margin-bottom: var(--ios-spacing-md);
  color: var(--ios-text-primary);
  border-left: 3px solid var(--ios-blue);
  padding-left: var(--ios-spacing-md);
}

/* 状态筛选标签 */
.filter-tabs {
  display: flex;
  gap: var(--ios-spacing-sm);
  margin-bottom: var(--ios-spacing-lg);
  flex-wrap: wrap;
}

.filter-tab {
  padding: 8px 16px;
  font-size: var(--ios-font-size-body);
  font-weight: 500;
  color: var(--ios-text-secondary);
  background-color: var(--ios-bg-secondary);
  border: 1px solid var(--ios-separator-opaque);
  border-radius: var(--ios-radius-md);
  cursor: pointer;
  transition: all var(--ios-transition-fast);
}

.filter-tab:hover {
  background-color: var(--ios-bg-tertiary);
}

.filter-tab.active {
  color: var(--ios-blue);
  background-color: rgba(0, 122, 255, 0.1);
  border-color: var(--ios-blue);
}

/* 订单卡片 */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: var(--ios-spacing-md);
}

.order-card {
  background-color: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-lg);
  box-shadow: var(--ios-shadow-sm);
  overflow: hidden;
  transition: all var(--ios-transition-normal);
  border: 0.5px solid var(--ios-separator);
  cursor: pointer;
}

.order-card:hover {
  box-shadow: var(--ios-shadow-md);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--ios-spacing-md);
  border-bottom: 0.5px solid var(--ios-separator);
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: var(--ios-spacing-xs);
}

.order-sn {
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  color: var(--ios-text-primary);
}

.order-time {
  font-size: var(--ios-font-size-subhead);
  color: var(--ios-text-secondary);
}

.order-status {
  padding: 4px 12px;
  border-radius: var(--ios-radius-full);
  font-size: var(--ios-font-size-caption);
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

.order-content {
  padding: var(--ios-spacing-md);
}

.goods-info {
  display: flex;
  gap: var(--ios-spacing-md);
}

.goods-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: var(--ios-radius-md);
  background-color: var(--ios-bg-tertiary);
}

.goods-details {
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

.order-amount {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  color: var(--ios-red);
}

.order-footer {
  padding: var(--ios-spacing-md);
  border-top: 0.5px solid var(--ios-separator);
}

.order-actions {
  display: flex;
  gap: var(--ios-spacing-sm);
  justify-content: flex-end;
}

.btn-sm {
  padding: 8px 16px;
  font-size: var(--ios-font-size-subhead);
}

/* 加载和错误状态 */
.loading,
.error,
.empty-state {
  text-align: center;
  padding: var(--ios-spacing-xl) var(--ios-spacing-md);
  color: var(--ios-text-secondary);
  font-size: var(--ios-font-size-body);
}

.error {
  color: var(--ios-red);
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

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 响应式 */
@media (max-width: 768px) {
  .order-actions {
    flex-direction: column;
  }

  .btn-sm {
    width: 100%;
  }

  .goods-info {
    flex-direction: column;
  }

  .goods-image {
    width: 100%;
    height: 200px;
  }
}
</style>

