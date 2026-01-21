<template>
  <div class="my-goods-page">
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
        <h1 class="section-title">我的商品</h1>
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
        <p>正在加载商品...</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="loadMyGoods" class="btn btn-primary" style="margin-top: 10px;">
          重试
        </button>
      </div>

      <!-- 空状态 -->
      <div v-else-if="filteredGoods.length === 0" class="empty-state">
        <p>{{ currentFilter === 'all' ? '暂无商品' : `暂无${getStatusLabel(currentFilter)}商品` }}</p>
        <router-link to="/goods/create" class="btn btn-primary" style="margin-top: 10px;">
          发布商品
        </router-link>
      </div>

      <!-- 商品列表 -->
      <div v-else class="goods-grid">
        <div
          v-for="good in filteredGoods"
          :key="good.id"
          class="goods-card ios-card"
        >
          <div class="goods-img-wrapper" @click="goToDetail(good.id)">
            <img
              :src="good.image || placeholderImage"
              :alt="good.title"
              class="goods-image"
              @error="handleImageError"
            />
            <div v-if="good.status === 2" class="status-badge sold">已出</div>
            <div v-else-if="good.status === 3" class="status-badge off-shelf">下架</div>
          </div>

          <div class="goods-info" @click="goToDetail(good.id)">
            <h3 class="goods-title">{{ good.title }}</h3>
            <p class="goods-price">¥{{ good.price }}</p>
            <p class="goods-status">
              <span :class="['status-tag', `status-${good.status}`]">
                {{ good.status_display }}
              </span>
              <span class="goods-time">{{ formatDate(good.created_at) }}</span>
            </p>
          </div>

          <div class="goods-actions">
            <router-link :to="`/goods/${good.id}/edit`" class="btn btn-primary btn-sm">
              编辑
            </router-link>
            <button @click="handleDelete(good.id)" class="btn btn-danger btn-sm">
              删除
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { goodsAPI, authAPI } from '@/utils/api'

const router = useRouter()

// 状态管理
const loading = ref(false)
const error = ref('')
const goodsList = ref([])
const currentFilter = ref('all')
const deletingGoodId = ref(null)

// 登录状态
const isLoggedIn = computed(() => authAPI.isLoggedIn())
const username = computed(() => localStorage.getItem('username') || '')
const isAdmin = ref(false)

// 状态筛选选项
const statusFilters = [
  { label: '全部', value: 'all' },
  { label: '在售', value: 1 },
  { label: '已出', value: 2 },
  { label: '下架', value: 3 }
]

// 筛选后的商品列表
const filteredGoods = computed(() => {
  if (currentFilter.value === 'all') {
    return goodsList.value
  }
  return goodsList.value.filter(good => good.status === currentFilter.value)
})

// 占位图
const placeholderImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjQwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuaXoOazleiDveWKoOi9vTwvdGV4dD48L3N2Zz4='

// 加载我的商品
const loadMyGoods = async () => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  loading.value = true
  error.value = ''

  try {
    // 获取所有商品，然后在前端过滤当前用户的商品
    // 注意：这里需要后端支持owner过滤，或者前端过滤
    const response = await goodsAPI.getGoods()
    if (response.data) {
      const allGoods = Array.isArray(response.data) ? response.data : response.data.results || []
      // 过滤当前用户的商品（通过is_owner字段）
      goodsList.value = allGoods.filter(good => good.is_owner === true)
    }
  } catch (err) {
    console.error('加载我的商品失败:', err)
    if (err.response?.status === 401) {
      error.value = '请先登录'
      router.push('/login')
    } else {
      error.value = err.response?.data?.detail || err.response?.data?.message || '加载商品失败'
    }
  } finally {
    loading.value = false
  }
}

// 跳转到商品详情
const goToDetail = (goodsId) => {
  router.push(`/goods/${goodsId}`)
}

// 删除商品
const handleDelete = async (goodsId) => {
  if (!confirm('确定要删除这个商品吗？删除后无法恢复！')) {
    return
  }

  deletingGoodId.value = goodsId
  try {
    await goodsAPI.deleteGood(goodsId)
    alert('商品删除成功')
    // 重新加载商品列表
    await loadMyGoods()
  } catch (err) {
    console.error('删除商品失败:', err)
    if (err.response?.status === 403) {
      alert('无权删除此商品')
    } else if (err.response?.status === 401) {
      alert('请先登录')
      router.push('/login')
    } else {
      alert('删除失败：' + (err.response?.data?.detail || err.response?.data?.message || '网络错误'))
    }
  } finally {
    deletingGoodId.value = null
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

// 获取状态标签
const getStatusLabel = (status) => {
  const filter = statusFilters.find(f => f.value === status)
  return filter ? filter.label : ''
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

// 组件挂载时加载商品
onMounted(() => {
  if (isLoggedIn.value) {
    checkAdminStatus()
    loadMyGoods()
  } else {
    router.push('/login')
  }
})
</script>

<style scoped>
.my-goods-page {
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

/* 商品网格 */
.goods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--ios-spacing-md);
}

.goods-card {
  background-color: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-lg);
  box-shadow: var(--ios-shadow-sm);
  overflow: hidden;
  border: 0.5px solid var(--ios-separator);
  transition: all var(--ios-transition-normal);
}

.goods-card:hover {
  box-shadow: var(--ios-shadow-md);
}

.goods-img-wrapper {
  position: relative;
  width: 100%;
  padding-top: 75%; /* 4:3 比例 */
  overflow: hidden;
  background-color: var(--ios-bg-tertiary);
  cursor: pointer;
}

.goods-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-badge {
  position: absolute;
  top: var(--ios-spacing-sm);
  right: var(--ios-spacing-sm);
  padding: 4px 8px;
  border-radius: var(--ios-radius-sm);
  font-size: var(--ios-font-size-caption);
  font-weight: 600;
  color: #FFFFFF;
}

.status-badge.sold {
  background-color: var(--ios-gray);
}

.status-badge.off-shelf {
  background-color: var(--ios-text-tertiary);
}

.goods-info {
  padding: var(--ios-spacing-md);
  cursor: pointer;
}

.goods-title {
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  color: var(--ios-text-primary);
  margin-bottom: var(--ios-spacing-xs);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.goods-price {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  color: var(--ios-red);
  margin-bottom: var(--ios-spacing-xs);
}

.goods-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--ios-font-size-caption);
  color: var(--ios-text-secondary);
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

.goods-time {
  font-size: var(--ios-font-size-caption);
  color: var(--ios-text-tertiary);
}

.goods-actions {
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
  .goods-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: var(--ios-spacing-sm);
  }

  .goods-actions {
    flex-direction: column;
  }

  .btn-sm {
    width: 100%;
  }
}
</style>

