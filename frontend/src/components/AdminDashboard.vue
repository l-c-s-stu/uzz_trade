<template>
  <div class="admin-dashboard-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container nav-content">
        <router-link to="/" class="logo">CampusTrade 🛒</router-link>
        <div class="nav-links">
          <router-link to="/" class="nav-link">首页</router-link>
          <router-link v-if="isLoggedIn" to="/user" class="nav-link">个人中心</router-link>
          <span v-if="isLoggedIn" class="user-info">欢迎，{{ username }}</span>
          <button v-if="isLoggedIn" @click="handleLogout" class="btn btn-danger">
            退出登录
          </button>
          <router-link v-else to="/login" class="btn btn-primary">登录</router-link>
        </div>
      </div>
    </nav>

    <div class="container">
      <!-- 权限检查 -->
      <div v-if="!isLoggedIn" class="error-card">
        <h3>请先登录</h3>
        <p>访问管理后台需要先登录</p>
        <router-link to="/login" class="btn btn-primary">去登录</router-link>
      </div>

      <div v-else-if="!isAdmin" class="error-card">
        <h3>权限不足</h3>
        <p>您没有权限访问管理后台</p>
        <router-link to="/" class="btn btn-primary">返回首页</router-link>
      </div>

      <!-- 管理后台内容 -->
      <div v-else class="admin-content">
        <div class="page-header">
          <h1 class="section-title">管理后台</h1>
        </div>

        <!-- 统计卡片 -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-info">
              <div class="stat-value">{{ loadingStats ? '加载中...' : (stats.totalUsers !== undefined ? stats.totalUsers : 0) }}</div>
              <div class="stat-label">总用户数</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📦</div>
            <div class="stat-info">
              <div class="stat-value">{{ loadingStats ? '加载中...' : (stats.totalGoods !== undefined ? stats.totalGoods : 0) }}</div>
              <div class="stat-label">总商品数</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🛒</div>
            <div class="stat-info">
              <div class="stat-value">{{ loadingStats ? '加载中...' : (stats.totalOrders !== undefined ? stats.totalOrders : 0) }}</div>
              <div class="stat-label">总订单数</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">❤️</div>
            <div class="stat-info">
              <div class="stat-value">{{ loadingStats ? '加载中...' : (stats.totalWishes !== undefined ? stats.totalWishes : 0) }}</div>
              <div class="stat-label">想买总数</div>
            </div>
          </div>
        </div>

        <!-- 管理菜单 -->
        <div class="admin-menu">
          <router-link to="/admin/users" class="menu-item">
            <div class="menu-icon">👥</div>
            <div class="menu-content">
              <h3>用户管理</h3>
              <p>管理所有用户账户</p>
            </div>
            <div class="menu-arrow">›</div>
          </router-link>
          <router-link to="/admin/goods" class="menu-item">
            <div class="menu-icon">📦</div>
            <div class="menu-content">
              <h3>商品管理</h3>
              <p>管理所有商品信息</p>
            </div>
            <div class="menu-arrow">›</div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI, adminAPI } from '@/utils/api'

const router = useRouter()

// 状态管理
const isLoggedIn = ref(false)
const username = ref('')
const isAdmin = ref(false)
const loadingStats = ref(false)
const stats = ref({
  totalUsers: 0,
  totalGoods: 0,
  totalOrders: 0,
  totalWishes: 0
})

// 检查登录状态和权限
const checkAuth = async () => {
  isLoggedIn.value = authAPI.isLoggedIn()
  if (isLoggedIn.value) {
    username.value = localStorage.getItem('username') || '用户'
    try {
      const response = await authAPI.getProfile()
      if (response.data) {
        username.value = response.data.username
        // 检查是否为管理员（is_staff 或 is_superuser）
        isAdmin.value = response.data.is_staff || response.data.is_superuser || false
        if (isAdmin.value) {
          loadStats()
        }
      }
    } catch (err) {
      console.error('获取用户信息失败:', err)
      isAdmin.value = false
    }
  }
}

// 加载统计数据
const loadStats = async () => {
  loadingStats.value = true
  try {
    console.log('开始加载统计数据...')
    const response = await adminAPI.getStats()
    console.log('统计数据完整响应:', response)
    console.log('响应状态:', response.status)
    console.log('响应数据:', response.data)
    console.log('响应数据类型:', typeof response.data)
    
    // 处理响应数据
    let data = null
    if (response && response.data) {
      data = response.data
    } else if (response && response.data === null) {
      console.warn('响应数据为 null')
    } else {
      console.warn('响应格式异常:', response)
    }
    
    if (data) {
      // 后端返回的是下划线格式：total_users, total_goods 等
      stats.value = {
        totalUsers: data.total_users !== undefined ? data.total_users : (data.totalUsers !== undefined ? data.totalUsers : 0),
        totalGoods: data.total_goods !== undefined ? data.total_goods : (data.totalGoods !== undefined ? data.totalGoods : 0),
        totalOrders: data.total_orders !== undefined ? data.total_orders : (data.totalOrders !== undefined ? data.totalOrders : 0),
        totalWishes: data.total_wishes !== undefined ? data.total_wishes : (data.totalWishes !== undefined ? data.totalWishes : 0)
      }
      console.log('统计数据已更新:', stats.value)
    } else {
      console.warn('无法解析统计数据，使用默认值 0')
      stats.value = {
        totalUsers: 0,
        totalGoods: 0,
        totalOrders: 0,
        totalWishes: 0
      }
    }
  } catch (err) {
    console.error('加载统计数据失败:', err)
    console.error('错误对象:', err)
    console.error('错误状态码:', err.response?.status)
    console.error('错误详情:', err.response?.data)
    console.error('错误消息:', err.message)
    
    // 如果 API 调用失败，显示错误信息
    if (err.response?.status === 403) {
      console.error('权限不足，请确认用户是否为管理员')
    } else if (err.response?.status === 401) {
      console.error('未授权，请先登录')
    }
    
    // 保持默认值 0
    stats.value = {
      totalUsers: 0,
      totalGoods: 0,
      totalOrders: 0,
      totalWishes: 0
    }
  } finally {
    loadingStats.value = false
  }
}

// 退出登录
const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    authAPI.logout()
    isLoggedIn.value = false
    isAdmin.value = false
    router.push('/')
  }
}

// 组件挂载时执行
onMounted(() => {
  checkAuth()
})
</script>

<style scoped>
.admin-dashboard-page {
  min-height: 100vh;
  background-color: var(--ios-bg-primary);
  font-family: var(--ios-font-family);
  padding-bottom: var(--ios-spacing-xl);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 导航栏 */
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
  gap: 15px;
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

.user-info {
  color: var(--ios-text-secondary);
  font-size: var(--ios-font-size-subhead);
}

/* 按钮 */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 24px;
  font-family: var(--ios-font-family);
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  border: none;
  border-radius: var(--ios-radius-md);
  cursor: pointer;
  transition: all var(--ios-transition-fast);
  text-decoration: none;
}

.btn-primary {
  color: #FFFFFF;
  background-color: var(--ios-blue);
}

.btn-primary:hover {
  background-color: var(--ios-blue-dark);
}

.btn-danger {
  color: #FFFFFF;
  background-color: var(--ios-red);
}

.btn-danger:hover {
  background-color: #D32F2F;
}

/* 错误卡片 */
.error-card {
  background: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-lg);
  padding: 60px 40px;
  text-align: center;
  margin-top: 40px;
  box-shadow: var(--ios-shadow-sm);
  border: 0.5px solid var(--ios-separator);
}

.error-card h3 {
  font-size: var(--ios-font-size-headline);
  color: var(--ios-red);
  margin-bottom: 10px;
}

.error-card p {
  color: var(--ios-text-secondary);
  margin-bottom: 20px;
}

/* 页面标题 */
.page-header {
  margin-bottom: 30px;
}

.section-title {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  margin-bottom: var(--ios-spacing-md);
  color: var(--ios-text-primary);
  border-left: 3px solid var(--ios-blue);
  padding-left: var(--ios-spacing-md);
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--ios-spacing-md);
  margin-bottom: var(--ios-spacing-lg);
}

.stat-card {
  background: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-lg);
  padding: var(--ios-spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--ios-spacing-md);
  box-shadow: var(--ios-shadow-sm);
  border: 0.5px solid var(--ios-separator);
  transition: transform var(--ios-transition-fast);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--ios-shadow-md);
}

.stat-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 122, 255, 0.1);
  border-radius: var(--ios-radius-md);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  color: var(--ios-text-primary);
  margin-bottom: 4px;
}

.stat-label {
  font-size: var(--ios-font-size-subhead);
  color: var(--ios-text-secondary);
}

/* 管理菜单 */
.admin-menu {
  display: flex;
  flex-direction: column;
  gap: var(--ios-spacing-md);
}

.menu-item {
  background: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-lg);
  padding: var(--ios-spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--ios-spacing-md);
  text-decoration: none;
  color: var(--ios-text-primary);
  box-shadow: var(--ios-shadow-sm);
  border: 0.5px solid var(--ios-separator);
  transition: all var(--ios-transition-fast);
}

.menu-item:hover {
  background: rgba(0, 122, 255, 0.05);
  transform: translateX(4px);
}

.menu-item:active {
  transform: scale(0.98);
}

.menu-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 122, 255, 0.1);
  border-radius: var(--ios-radius-md);
}

.menu-content {
  flex: 1;
}

.menu-content h3 {
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--ios-text-primary);
}

.menu-content p {
  font-size: var(--ios-font-size-subhead);
  color: var(--ios-text-secondary);
}

.menu-arrow {
  font-size: 24px;
  color: var(--ios-text-tertiary);
}

/* 加载状态 */
.loading {
  text-align: center;
  padding: var(--ios-spacing-xl) var(--ios-spacing-md);
  color: var(--ios-text-secondary);
  font-size: var(--ios-font-size-body);
}

/* 响应式 */
@media (max-width: 768px) {
  .container {
    padding: 0 12px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .stat-card {
    padding: var(--ios-spacing-md);
  }

  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 24px;
  }

  .menu-item {
    padding: var(--ios-spacing-md);
  }

  .menu-icon {
    width: 50px;
    height: 50px;
    font-size: 24px;
  }
}
</style>

