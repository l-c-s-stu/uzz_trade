<template>
  <div class="wish-list-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container nav-content">
        <router-link to="/" class="logo">CampusTrade 🛒</router-link>
        <div class="nav-links">
          <router-link to="/" class="nav-link">首页</router-link>
          <router-link to="/orders" class="nav-link">我的订单</router-link>
          <router-link to="/user" class="nav-link">个人中心</router-link>
          <router-link v-if="isAdmin" to="/admin" class="nav-link admin-link">管理后台</router-link>
          <span v-if="isLoggedIn" class="user-info">欢迎，{{ username }}</span>
          <router-link v-if="isLoggedIn" to="/goods/create" class="btn btn-success">
            发布商品
          </router-link>
          <button v-if="isLoggedIn" @click="handleLogout" class="btn btn-danger">
            退出登录
          </button>
          <router-link v-else to="/login" class="btn btn-primary">登录</router-link>
        </div>
      </div>
    </nav>

    <div class="container">
      <div class="page-header">
        <h1 class="section-title">想买列表</h1>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <div class="ios-spinner"></div>
        <p>正在加载想买列表...</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="loadWishList" class="btn btn-primary" style="margin-top: 10px;">
          重试
        </button>
      </div>

      <!-- 空状态 -->
      <div v-else-if="wishList.length === 0" class="empty-state">
        <p>暂无想买商品</p>
        <router-link to="/" class="btn btn-primary" style="margin-top: 10px;">
          去逛逛
        </router-link>
      </div>

      <!-- 想买列表 -->
      <div v-else class="wish-list">
        <div
          v-for="wish in wishList"
          :key="wish.id"
          class="wish-card ios-card"
        >
          <div class="wish-content" @click="goToDetail(wish.goods.id)">
            <img
              :src="wish.goods.image || placeholderImage"
              :alt="wish.goods.title"
              class="wish-goods-image"
              @error="handleImageError"
            />
            <div class="wish-info">
              <h3 class="wish-goods-title">{{ wish.goods.title }}</h3>
              <p class="wish-goods-price">¥{{ wish.goods.price }}</p>
              <p class="wish-goods-status">
                <span :class="['status-tag', `status-${wish.goods.status}`]">
                  {{ wish.goods.status_display }}
                </span>
              </p>
              <p class="wish-time">添加时间：{{ formatDate(wish.created_at) }}</p>
            </div>
          </div>

          <div class="wish-actions">
            <button
              @click.stop="handleRemoveWish(wish.goods.id, wish.id)"
              class="btn btn-danger btn-sm"
              :disabled="removingWishId === wish.id"
            >
              <span v-if="removingWishId === wish.id">取消中...</span>
              <span v-else>取消想买</span>
            </button>
            <router-link
              :to="`/goods/${wish.goods.id}`"
              class="btn btn-primary btn-sm"
              @click.stop
            >
              查看详情
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { wishesAPI, authAPI } from '@/utils/api'

const router = useRouter()

// 状态管理
const loading = ref(false)
const error = ref('')
const wishList = ref([])
const removingWishId = ref(null)

// 登录状态
const isLoggedIn = computed(() => authAPI.isLoggedIn())
const username = computed(() => localStorage.getItem('username') || '')
const isAdmin = ref(false)

// 占位图
const placeholderImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjQwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuaXoOazleiDveWKoOi9vTwvdGV4dD48L3N2Zz4='

// 加载想买列表
const loadWishList = async () => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await wishesAPI.getWishList()
    if (response.data) {
      wishList.value = Array.isArray(response.data) ? response.data : response.data.results || []
    }
  } catch (err) {
    console.error('加载想买列表失败:', err)
    if (err.response?.status === 401) {
      error.value = '请先登录'
      router.push('/login')
    } else {
      error.value = err.response?.data?.detail || err.response?.data?.message || '加载想买列表失败'
    }
  } finally {
    loading.value = false
  }
}

// 取消想买
const handleRemoveWish = async (goodsId, wishId) => {
  if (!confirm('确定要取消想买吗？')) {
    return
  }

  removingWishId.value = wishId
  try {
    await wishesAPI.removeFromWish(goodsId)
    alert('已取消想买')
    // 重新加载想买列表
    await loadWishList()
  } catch (err) {
    console.error('取消想买失败:', err)
    if (err.response?.status === 401) {
      alert('请先登录')
      router.push('/login')
    } else {
      alert('取消想买失败：' + (err.response?.data?.detail || err.response?.data?.message || '网络错误'))
    }
  } finally {
    removingWishId.value = null
  }
}

// 跳转到商品详情
const goToDetail = (goodsId) => {
  router.push(`/goods/${goodsId}`)
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

// 处理图片加载错误
const handleImageError = (e) => {
  e.target.src = placeholderImage
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

// 组件挂载时加载想买列表
onMounted(() => {
  if (isLoggedIn.value) {
    checkAdminStatus()
    loadWishList()
  } else {
    router.push('/login')
  }
})
</script>

<style scoped>
.wish-list-page {
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

/* 想买列表 */
.wish-list {
  display: flex;
  flex-direction: column;
  gap: var(--ios-spacing-md);
}

.wish-card {
  background-color: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-lg);
  box-shadow: var(--ios-shadow-sm);
  overflow: hidden;
  border: 0.5px solid var(--ios-separator);
  transition: all var(--ios-transition-normal);
}

.wish-card:hover {
  box-shadow: var(--ios-shadow-md);
}

.wish-content {
  display: flex;
  gap: var(--ios-spacing-md);
  padding: var(--ios-spacing-md);
  cursor: pointer;
}

.wish-goods-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: var(--ios-radius-md);
  background-color: var(--ios-bg-tertiary);
  flex-shrink: 0;
}

.wish-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--ios-spacing-xs);
}

.wish-goods-title {
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  color: var(--ios-text-primary);
  margin-bottom: var(--ios-spacing-xs);
}

.wish-goods-price {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  color: var(--ios-red);
}

.wish-goods-status {
  margin-top: var(--ios-spacing-xs);
}

.status-tag {
  padding: 2px 8px;
  border-radius: var(--ios-radius-full);
  font-size: var(--ios-font-size-caption);
  font-weight: 600;
}

.status-1 {
  background-color: rgba(52, 199, 89, 0.1);
  color: var(--ios-green);
}

.status-2 {
  background-color: rgba(142, 142, 147, 0.1);
  color: var(--ios-text-tertiary);
}

.status-3 {
  background-color: rgba(255, 149, 0, 0.1);
  color: var(--ios-orange);
}

.wish-time {
  font-size: var(--ios-font-size-caption);
  color: var(--ios-text-tertiary);
  margin-top: var(--ios-spacing-xs);
}

.wish-actions {
  display: flex;
  gap: var(--ios-spacing-sm);
  padding: var(--ios-spacing-md);
  border-top: 0.5px solid var(--ios-separator);
}

.btn-sm {
  flex: 1;
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

.btn-success {
  background-color: var(--ios-green);
  color: #FFFFFF;
}

.btn-success:hover:not(:disabled) {
  background-color: #2DA44E;
}

.btn-success:active:not(:disabled) {
  background-color: #2DA44E;
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
  .wish-content {
    flex-direction: column;
  }

  .wish-goods-image {
    width: 100%;
    height: 200px;
  }

  .wish-actions {
    flex-direction: column;
  }

  .btn-sm {
    width: 100%;
  }
}
</style>

