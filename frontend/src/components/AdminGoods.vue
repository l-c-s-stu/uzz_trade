<template>
  <div class="admin-goods-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container nav-content">
        <router-link to="/" class="logo">CampusTrade 🛒</router-link>
        <div class="nav-links">
          <router-link to="/admin" class="nav-link">管理后台</router-link>
          <router-link to="/" class="nav-link">首页</router-link>
          <span v-if="isLoggedIn" class="user-info">欢迎，{{ username }}</span>
          <button v-if="isLoggedIn" @click="handleLogout" class="btn btn-danger">
            退出登录
          </button>
        </div>
      </div>
    </nav>

    <div class="container">
      <div class="page-header">
        <h1 class="section-title">商品管理</h1>
      </div>

      <!-- 搜索和筛选 -->
      <div class="filter-section">
        <div class="filter-row">
          <div class="search-box">
            <input
              v-model="searchQuery"
              @input="handleSearch"
              type="text"
              placeholder="搜索商品标题..."
              class="search-input"
            />
            <span class="search-icon">🔍</span>
          </div>
          <select v-model="statusFilter" @change="loadGoods" class="status-select">
            <option value="">全部状态</option>
            <option value="1">在售</option>
            <option value="2">已出</option>
            <option value="3">下架</option>
          </select>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <p>正在加载商品列表...</p>
      </div>

      <!-- 商品列表 -->
      <div v-else-if="goodsList.length > 0" class="goods-list">
        <div
          v-for="good in goodsList"
          :key="good.id"
          class="goods-item"
        >
          <div class="goods-image">
            <img
              :src="good.image || '/placeholder.png'"
              :alt="good.title"
              @error="handleImageError"
            />
          </div>
          <div class="goods-info">
            <h3 class="goods-title">{{ good.title }}</h3>
            <p class="goods-desc">{{ good.description }}</p>
            <div class="goods-meta">
              <span class="goods-price">¥{{ good.price }}</span>
              <span v-if="good.category" class="goods-category">{{ good.category.name }}</span>
              <span class="goods-owner">发布者：{{ good.owner_name }}</span>
            </div>
            <div class="goods-status-row">
              <span class="goods-status" :class="`status-${good.status}`">
                {{ good.status_display }}
              </span>
              <span class="goods-date">{{ formatDate(good.created_at) }}</span>
            </div>
          </div>
          <div class="goods-actions">
            <select
              v-model="good.status"
              @change="updateGoodStatus(good)"
              class="status-select-small"
            >
              <option :value="1">在售</option>
              <option :value="2">已出</option>
              <option :value="3">下架</option>
            </select>
            <button
              @click="deleteGood(good)"
              class="btn btn-danger btn-sm"
            >
              删除
            </button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <p>暂无商品数据</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI, adminAPI } from '@/utils/api'

const router = useRouter()

// 状态管理
const loading = ref(false)
const isLoggedIn = ref(false)
const username = ref('')
const goodsList = ref([])
const searchQuery = ref('')
const statusFilter = ref('')
let searchTimeout = null

// 检查登录状态和权限
const checkAuth = async () => {
  isLoggedIn.value = authAPI.isLoggedIn()
  if (isLoggedIn.value) {
    try {
      const response = await authAPI.getProfile()
      if (response.data) {
        username.value = response.data.username
        const isAdmin = response.data.is_staff || response.data.is_superuser || false
        if (!isAdmin) {
          router.push('/')
        }
      }
    } catch (err) {
      console.error('获取用户信息失败:', err)
      router.push('/')
    }
  } else {
    router.push('/login')
  }
}

// 加载商品列表
const loadGoods = async () => {
  loading.value = true
  try {
    const params = {}
    if (searchQuery.value.trim()) {
      params.title = searchQuery.value.trim()
    }
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    const response = await adminAPI.getGoods(params)
    goodsList.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (err) {
    console.error('加载商品列表失败:', err)
    alert('加载商品列表失败')
  } finally {
    loading.value = false
  }
}

// 处理搜索（防抖）
const handleSearch = () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  searchTimeout = setTimeout(() => {
    loadGoods()
  }, 500)
}

// 更新商品状态
const updateGoodStatus = async (good) => {
  try {
    await adminAPI.updateGoodStatus(good.id, good.status)
    alert('商品状态已更新')
  } catch (err) {
    console.error('更新商品状态失败:', err)
    alert('操作失败：' + (err.response?.data?.detail || '网络错误'))
    // 重新加载以恢复原状态
    await loadGoods()
  }
}

// 删除商品
const deleteGood = async (good) => {
  if (!confirm(`确定要删除商品 "${good.title}" 吗？此操作不可恢复！`)) {
    return
  }

  try {
    await adminAPI.deleteGood(good.id)
    alert('商品已删除')
    await loadGoods()
  } catch (err) {
    console.error('删除商品失败:', err)
    alert('操作失败：' + (err.response?.data?.detail || '网络错误'))
  }
}

// 处理图片加载错误
const handleImageError = (e) => {
  e.target.src = '/placeholder.png'
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 退出登录
const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    authAPI.logout()
    router.push('/')
  }
}

// 组件挂载时执行
onMounted(() => {
  checkAuth().then(() => {
    if (isLoggedIn.value) {
      loadGoods()
    }
  })
})
</script>

<style scoped>
.admin-goods-page {
  min-height: 100vh;
  background-color: var(--ios-bg-primary);
  font-family: var(--ios-font-family);
  padding-bottom: var(--ios-spacing-xl);
}

.container {
  max-width: 1400px;
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
  padding: 8px 16px;
  font-family: var(--ios-font-family);
  font-size: var(--ios-font-size-subhead);
  font-weight: 600;
  border: none;
  border-radius: var(--ios-radius-md);
  cursor: pointer;
  transition: all var(--ios-transition-fast);
}

.btn-sm {
  padding: 6px 12px;
  font-size: var(--ios-font-size-caption);
}

.btn-danger {
  color: #FFFFFF;
  background-color: var(--ios-red);
}

.btn:hover {
  opacity: 0.8;
}

/* 页面标题 */
.page-header {
  margin-bottom: 20px;
}

.section-title {
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
  margin-bottom: var(--ios-spacing-md);
  color: var(--ios-text-primary);
  border-left: 3px solid var(--ios-blue);
  padding-left: var(--ios-spacing-md);
}

/* 搜索和筛选 */
.filter-section {
  background: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-md);
  padding: 12px;
  margin-bottom: var(--ios-spacing-md);
  border: 0.5px solid var(--ios-separator);
  box-shadow: var(--ios-shadow-sm);
}

.filter-row {
  display: flex;
  gap: 12px;
}

.search-box {
  position: relative;
  flex: 1;
}

.search-input {
  width: 100%;
  padding: 8px 36px 8px 12px;
  font-size: var(--ios-font-size-body);
  border: 1px solid var(--ios-separator);
  border-radius: var(--ios-radius-md);
  background-color: var(--ios-bg-tertiary);
  color: var(--ios-text-primary);
  transition: all var(--ios-transition-fast);
}

.search-input:focus {
  outline: none;
  border-color: var(--ios-blue);
  background-color: var(--ios-bg-secondary);
}

.search-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
  pointer-events: none;
}

.status-select {
  padding: 8px 12px;
  font-size: var(--ios-font-size-body);
  color: var(--ios-text-primary);
  background-color: var(--ios-bg-tertiary);
  border: 1px solid var(--ios-separator);
  border-radius: var(--ios-radius-md);
  cursor: pointer;
  min-width: 150px;
}

.status-select-small {
  padding: 6px 10px;
  font-size: var(--ios-font-size-caption);
  color: var(--ios-text-primary);
  background-color: var(--ios-bg-tertiary);
  border: 1px solid var(--ios-separator);
  border-radius: var(--ios-radius-sm);
  cursor: pointer;
}

/* 商品列表 */
.goods-list {
  display: flex;
  flex-direction: column;
  gap: var(--ios-spacing-md);
}

.goods-item {
  background: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-lg);
  padding: var(--ios-spacing-md);
  display: flex;
  gap: var(--ios-spacing-md);
  box-shadow: var(--ios-shadow-sm);
  border: 0.5px solid var(--ios-separator);
  transition: all var(--ios-transition-fast);
}

.goods-item:hover {
  box-shadow: var(--ios-shadow-md);
}

.goods-image {
  width: 120px;
  height: 120px;
  flex-shrink: 0;
  border-radius: var(--ios-radius-md);
  overflow: hidden;
  background: var(--ios-bg-tertiary);
}

.goods-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.goods-info {
  flex: 1;
  min-width: 0;
}

.goods-title {
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  margin-bottom: 6px;
  color: var(--ios-text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.goods-desc {
  font-size: var(--ios-font-size-subhead);
  color: var(--ios-text-secondary);
  margin-bottom: 8px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.goods-meta {
  display: flex;
  gap: var(--ios-spacing-md);
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.goods-price {
  color: var(--ios-red);
  font-size: var(--ios-font-size-body);
  font-weight: 700;
}

.goods-category {
  font-size: var(--ios-font-size-caption);
  color: var(--ios-blue);
  background: rgba(0, 122, 255, 0.1);
  padding: 2px 8px;
  border-radius: var(--ios-radius-full);
}

.goods-owner {
  font-size: var(--ios-font-size-caption);
  color: var(--ios-text-secondary);
}

.goods-status-row {
  display: flex;
  gap: var(--ios-spacing-md);
  align-items: center;
}

.goods-status {
  padding: 4px 8px;
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
  background-color: rgba(255, 59, 48, 0.1);
  color: var(--ios-red);
}

.goods-date {
  font-size: var(--ios-font-size-caption);
  color: var(--ios-text-tertiary);
}

.goods-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
  justify-content: center;
}

/* 加载和空状态 */
.loading,
.empty-state {
  text-align: center;
  padding: var(--ios-spacing-xl) var(--ios-spacing-md);
  color: var(--ios-text-secondary);
  font-size: var(--ios-font-size-body);
}

/* 响应式 */
@media (max-width: 768px) {
  .filter-row {
    flex-direction: column;
  }

  .goods-item {
    flex-direction: column;
  }

  .goods-image {
    width: 100%;
    height: 200px;
  }

  .goods-actions {
    flex-direction: row;
    width: 100%;
    justify-content: space-between;
  }

  .status-select-small {
    flex: 1;
  }
}
</style>



