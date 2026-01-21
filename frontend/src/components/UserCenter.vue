<template>
  <div class="user-center-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container nav-content">
        <router-link to="/" class="logo">CampusTrade 🛒</router-link>
        <div class="nav-links">
          <router-link to="/" class="nav-link">首页</router-link>
          <router-link to="/goods/create" class="nav-link">发布商品</router-link>
          <router-link to="/orders" class="nav-link">我的订单</router-link>
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
        <p>正在加载...</p>
      </div>

      <!-- 未登录状态 -->
      <div v-else-if="!isLoggedIn" class="not-logged-in">
        <div class="empty-state">
          <p>请先登录</p>
          <router-link to="/login" class="btn btn-primary" style="margin-top: 10px;">
            去登录
          </router-link>
        </div>
      </div>

      <!-- 用户中心内容 -->
      <div v-else class="user-center-content">
        <!-- 用户信息卡片 -->
        <div class="user-info-card ios-card">
          <div class="user-header">
            <div class="avatar-section">
              <div class="avatar-placeholder">
                <span>{{ username.charAt(0).toUpperCase() }}</span>
              </div>
            </div>
            <div class="user-details">
              <h2 class="username">{{ username }}</h2>
              <p class="user-email">{{ userInfo.email || '未设置邮箱' }}</p>
            </div>
          </div>
          
          <!-- 个人信息按钮 -->
          <div class="user-info-button-wrapper">
            <button 
              @click="showUserDetails = !showUserDetails" 
              class="btn btn-info-details"
            >
              <span>{{ showUserDetails ? '收起' : '查看' }}个人信息</span>
              <span class="toggle-icon" :class="{ 'expanded': showUserDetails }">▼</span>
            </button>
          </div>
          
          <!-- 个人信息详情 -->
          <div v-show="showUserDetails" class="user-info-details">
            <div class="info-row">
              <span class="info-label">学号：</span>
              <span class="info-value">{{ userInfo.student_id || '未设置' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">学院：</span>
              <span class="info-value">{{ userInfo.college || '未设置' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">手机号：</span>
              <span class="info-value">{{ userInfo.phone || '未设置' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">注册时间：</span>
              <span class="info-value">{{ formatDate(userInfo.date_joined) }}</span>
            </div>
          </div>
          
          <div class="user-stats">
            <div class="stat-item">
              <span class="stat-value">{{ myGoodsCount }}</span>
              <span class="stat-label">发布的商品</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ myOrdersCount }}</span>
              <span class="stat-label">我的订单</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ myWishesCount }}</span>
              <span class="stat-label">想买列表</span>
            </div>
          </div>
        </div>

        <!-- 快捷操作卡片 -->
        <div class="quick-actions-card ios-card">
          <h3 class="card-title">快捷操作</h3>
          <div class="action-grid">
            <router-link to="/goods/create" class="action-item">
              <div class="action-icon">➕</div>
              <span class="action-label">发布商品</span>
            </router-link>
            <router-link to="/orders" class="action-item">
              <div class="action-icon">📦</div>
              <span class="action-label">我的订单</span>
            </router-link>
            <router-link to="/user/goods" class="action-item">
              <div class="action-icon">📋</div>
              <span class="action-label">我的商品</span>
            </router-link>
            <router-link to="/user/wishes" class="action-item">
              <div class="action-icon">❤️</div>
              <span class="action-label">想买列表</span>
            </router-link>
          </div>
        </div>

        <!-- 订单状态概览 -->
        <div class="orders-overview-card ios-card">
          <div class="card-header">
            <h3 class="card-title">订单概览</h3>
            <router-link to="/orders" class="view-all-link">查看全部</router-link>
          </div>
          <div class="orders-stats">
            <div class="order-stat-item">
              <span class="order-stat-value">{{ orderStats.wait }}</span>
              <span class="order-stat-label">待支付</span>
            </div>
            <div class="order-stat-item">
              <span class="order-stat-value">{{ orderStats.success }}</span>
              <span class="order-stat-label">已支付</span>
            </div>
            <div class="order-stat-item">
              <span class="order-stat-value">{{ orderStats.cancel }}</span>
              <span class="order-stat-label">已取消</span>
            </div>
          </div>
        </div>

        <!-- 最近订单 -->
        <div v-if="recentOrders.length > 0" class="recent-orders-card ios-card">
          <div class="card-header">
            <h3 class="card-title">最近订单</h3>
            <router-link to="/orders" class="view-all-link">查看全部</router-link>
          </div>
          <div class="recent-orders-list">
            <div
              v-for="order in recentOrders"
              :key="order.id"
              class="recent-order-item"
              @click="goToOrderDetail(order.id)"
            >
              <img
                :src="order.goods_image || '/placeholder.png'"
                :alt="order.goods_title"
                class="order-goods-image"
                @error="handleImageError"
              />
              <div class="order-info">
                <h4 class="order-goods-title">{{ order.goods_title }}</h4>
                <p class="order-meta">
                  <span class="order-sn">{{ order.order_sn }}</span>
                  <span class="order-status" :class="`status-${order.pay_status.toLowerCase()}`">
                    {{ order.pay_status_display }}
                  </span>
                </p>
              </div>
              <div class="order-amount">¥{{ order.order_mount }}</div>
            </div>
          </div>
        </div>

        <!-- 空状态提示 -->
        <div v-else-if="!loadingOrders" class="empty-orders">
          <p>暂无订单</p>
          <router-link to="/" class="btn btn-primary" style="margin-top: 10px;">
            去逛逛
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ordersAPI, authAPI, goodsAPI, wishesAPI } from '@/utils/api'

const router = useRouter()

// 状态管理
const loading = ref(false)
const loadingOrders = ref(false)
const orders = ref([])
const myGoods = ref([])
const wishesList = ref([])
const showUserDetails = ref(false)
const userInfo = ref({
  username: '',
  email: '',
  phone: '',
  student_id: '',
  college: '',
  avatar: null,
  date_joined: null
})

// 登录状态
const isLoggedIn = computed(() => authAPI.isLoggedIn())
const username = computed(() => userInfo.value.username || localStorage.getItem('username') || '')

// 统计数据
const myGoodsCount = computed(() => myGoods.value.length)
const myOrdersCount = computed(() => orders.value.length)
const myWishesCount = computed(() => wishesList.value.length)

// 订单统计
const orderStats = computed(() => {
  return {
    wait: orders.value.filter(o => o.pay_status === 'WAIT').length,
    success: orders.value.filter(o => o.pay_status === 'SUCCESS').length,
    cancel: orders.value.filter(o => o.pay_status === 'CANCEL').length
  }
})

// 最近订单（最多5条）
const recentOrders = computed(() => {
  return orders.value.slice(0, 5)
})

// 加载订单列表
const loadOrders = async () => {
  if (!isLoggedIn.value) return

  loadingOrders.value = true
  try {
    const response = await ordersAPI.getOrders()
    if (response.data) {
      orders.value = Array.isArray(response.data) ? response.data : response.data.results || []
    }
  } catch (err) {
    console.error('加载订单失败:', err)
  } finally {
    loadingOrders.value = false
  }
}

// 加载用户信息
const loadUserInfo = async () => {
  if (!isLoggedIn.value) return

  try {
    const response = await authAPI.getProfile()
    if (response.data) {
      userInfo.value = response.data
      // 检查是否为管理员
      isAdmin.value = response.data.is_staff || response.data.is_superuser || false
      // 更新localStorage中的用户名（如果API返回了用户名）
      if (response.data.username) {
        localStorage.setItem('username', response.data.username)
      }
    }
  } catch (err) {
    console.error('加载用户信息失败:', err)
    // 如果API失败，至少使用localStorage中的用户名
    userInfo.value.username = localStorage.getItem('username') || ''
    isAdmin.value = false
  }
}

// 加载我的商品
const loadMyGoods = async () => {
  if (!isLoggedIn.value) return

  try {
    const response = await goodsAPI.getGoods()
    if (response.data) {
      const allGoods = Array.isArray(response.data) ? response.data : response.data.results || []
      // 过滤当前用户的商品（通过is_owner字段）
      myGoods.value = allGoods.filter(good => good.is_owner === true)
    }
  } catch (err) {
    console.error('加载我的商品失败:', err)
  }
}

// 加载想买列表
const loadWishList = async () => {
  if (!isLoggedIn.value) return

  try {
    const response = await wishesAPI.getWishList()
    if (response.data) {
      wishesList.value = Array.isArray(response.data) ? response.data : response.data.results || []
    }
  } catch (err) {
    console.error('加载想买列表失败:', err)
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 跳转到订单详情
const goToOrderDetail = (orderId) => {
  router.push(`/orders/${orderId}`)
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

// 组件挂载时加载数据
onMounted(() => {
  if (isLoggedIn.value) {
    loading.value = true
    Promise.all([
      loadUserInfo(),
      loadOrders(),
      loadMyGoods(),
      loadWishList()
    ]).finally(() => {
      loading.value = false
    })
  }
})
</script>

<style scoped>
.user-center-page {
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--ios-spacing-md);
}

.view-all-link {
  font-size: var(--ios-font-size-subhead);
  color: var(--ios-blue);
  text-decoration: none;
  transition: opacity var(--ios-transition-fast);
}

.view-all-link:hover {
  opacity: 0.7;
}

/* 用户信息卡片 */
.user-info-card {
  text-align: center;
}

.user-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: var(--ios-spacing-lg);
}

.avatar-section {
  margin-bottom: var(--ios-spacing-md);
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--ios-blue), var(--ios-purple));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 700;
  color: #FFFFFF;
  margin: 0 auto;
}

.user-details {
  text-align: center;
}

.username {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  color: var(--ios-text-primary);
  margin-bottom: var(--ios-spacing-xs);
}

.user-email {
  font-size: var(--ios-font-size-subhead);
  color: var(--ios-text-secondary);
}

/* 个人信息按钮 */
.user-info-button-wrapper {
  display: flex;
  justify-content: center;
  margin: var(--ios-spacing-md) 0;
}

.btn-info-details {
  display: flex;
  align-items: center;
  gap: var(--ios-spacing-sm);
  padding: 10px 20px;
  background-color: var(--ios-blue);
  color: #FFFFFF;
  border: none;
  border-radius: var(--ios-radius-md);
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--ios-transition-fast);
}

.btn-info-details:hover {
  background-color: var(--ios-blue-dark);
  transform: translateY(-1px);
}

.btn-info-details:active {
  opacity: 0.8;
  transform: scale(0.97);
}

.toggle-icon {
  display: inline-block;
  transition: transform var(--ios-transition-fast);
  font-size: 12px;
}

.toggle-icon.expanded {
  transform: rotate(180deg);
}

/* 个人信息详情 */
.user-info-details {
  background-color: rgba(0, 122, 255, 0.1);
  border: 1px solid rgba(0, 122, 255, 0.2);
  border-radius: var(--ios-radius-md);
  padding: var(--ios-spacing-md);
  margin: var(--ios-spacing-md) 0;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--ios-spacing-sm) 0;
  border-bottom: 0.5px solid rgba(0, 122, 255, 0.1);
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  color: var(--ios-text-primary);
}

.info-value {
  font-size: var(--ios-font-size-body);
  color: var(--ios-text-secondary);
}

.user-stats {
  display: flex;
  justify-content: space-around;
  padding-top: var(--ios-spacing-lg);
  border-top: 0.5px solid var(--ios-separator);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--ios-spacing-xs);
}

.stat-value {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  color: var(--ios-blue);
}

.stat-label {
  font-size: var(--ios-font-size-subhead);
  color: var(--ios-text-secondary);
}

/* 快捷操作 */
.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: var(--ios-spacing-md);
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--ios-spacing-sm);
  padding: var(--ios-spacing-md);
  background-color: var(--ios-bg-tertiary);
  border-radius: var(--ios-radius-md);
  text-decoration: none;
  color: var(--ios-text-primary);
  transition: all var(--ios-transition-fast);
}

.action-item:hover {
  background-color: rgba(0, 122, 255, 0.1);
  transform: translateY(-2px);
}

.action-icon {
  font-size: 32px;
}

.action-label {
  font-size: var(--ios-font-size-subhead);
  font-weight: 500;
}

/* 订单概览 */
.orders-stats {
  display: flex;
  justify-content: space-around;
  padding-top: var(--ios-spacing-md);
}

.order-stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--ios-spacing-xs);
}

.order-stat-value {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  color: var(--ios-blue);
}

.order-stat-label {
  font-size: var(--ios-font-size-subhead);
  color: var(--ios-text-secondary);
}

/* 最近订单 */
.recent-orders-list {
  display: flex;
  flex-direction: column;
  gap: var(--ios-spacing-md);
}

.recent-order-item {
  display: flex;
  align-items: center;
  gap: var(--ios-spacing-md);
  padding: var(--ios-spacing-md);
  background-color: var(--ios-bg-tertiary);
  border-radius: var(--ios-radius-md);
  cursor: pointer;
  transition: all var(--ios-transition-fast);
}

.recent-order-item:hover {
  background-color: rgba(0, 122, 255, 0.05);
}

.order-goods-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: var(--ios-radius-sm);
  background-color: var(--ios-bg-secondary);
}

.order-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--ios-spacing-xs);
}

.order-goods-title {
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  color: var(--ios-text-primary);
}

.order-meta {
  display: flex;
  gap: var(--ios-spacing-md);
  font-size: var(--ios-font-size-caption);
  color: var(--ios-text-secondary);
}

.order-status {
  padding: 2px 8px;
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

.order-amount {
  font-size: var(--ios-font-size-body);
  font-weight: 700;
  color: var(--ios-red);
}

/* 加载和错误状态 */
.loading,
.empty-state,
.empty-orders {
  text-align: center;
  padding: var(--ios-spacing-xl) var(--ios-spacing-md);
  color: var(--ios-text-secondary);
  font-size: var(--ios-font-size-body);
}

.not-logged-in {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
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

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 响应式 */
@media (max-width: 768px) {
  .action-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .user-stats,
  .orders-stats {
    flex-direction: column;
    gap: var(--ios-spacing-md);
  }
}
</style>

