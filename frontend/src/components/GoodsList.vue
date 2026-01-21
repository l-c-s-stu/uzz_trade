<template>
  <div class="goods-list-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container nav-content">
        <div class="logo">CampusTrade 🛒</div>
        <div class="nav-links">
          <router-link to="/" class="nav-link active">首页</router-link>
          <router-link v-if="isLoggedIn" to="/orders" class="nav-link">我的订单</router-link>
          <router-link v-if="isLoggedIn" to="/user" class="nav-link">个人中心</router-link>
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
        <h1 class="section-title">最新闲置</h1>
      </div>

      <!-- 搜索和筛选区域 -->
      <div class="filter-section">
        <div class="filter-row">
          <!-- 搜索框 -->
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

          <!-- 排序选择 -->
          <div class="sort-section">
            <select v-model="sortBy" @change="handleSortChange" class="sort-select">
              <option value="-created_at">最新发布</option>
              <option value="created_at">最早发布</option>
              <option value="-price">价格从高到低</option>
              <option value="price">价格从低到高</option>
            </select>
          </div>
        </div>

        <!-- 分类筛选 -->
        <div class="category-filter">
          <button
            @click="selectCategory(null)"
            :class="['category-tag', { active: selectedCategory === null }]"
          >
            全部
          </button>
          <button
            v-for="category in categories"
            :key="category.id"
            @click="selectCategory(category.id)"
            :class="['category-tag', { active: selectedCategory === category.id }]"
          >
            {{ category.name }}
          </button>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <p>正在加载商品...</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="loadGoods" class="btn btn-primary" style="margin-top: 10px;">
          重试
        </button>
      </div>

      <!-- 商品列表 -->
      <div v-else-if="goodsList.length > 0" class="goods-grid">
        <div
          v-for="good in goodsList"
          :key="good.id"
          class="goods-card"
          @click="goToDetail(good.id)"
        >
          <div class="goods-img-wrapper">
            <img
              :src="good.image || placeholderImage"
              :alt="good.title"
              class="goods-img"
            />
          </div>
          <div class="goods-info">
            <h3 class="goods-title">{{ good.title }}</h3>
            <p class="goods-desc">{{ good.description }}</p>
            <div class="goods-meta">
              <span class="goods-price">¥{{ good.price }}</span>
              <span v-if="good.category" class="goods-category">
                {{ good.category.name }}
              </span>
            </div>
            <div class="goods-footer">
              <span class="wish-count">❤️ {{ good.wish_count }} 人想买</span>
              <span class="owner-name">{{ good.owner_name }}</span>
            </div>
            <!-- 商品所有者操作按钮 -->
            <div v-if="good.is_owner" class="owner-actions" @click.stop>
              <button
                @click.stop="editGood(good.id)"
                class="btn-edit"
              >
                编辑
              </button>
              <button
                @click.stop="deleteGood(good.id)"
                class="btn-delete"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <p>暂无商品</p>
        <router-link v-if="isLoggedIn" to="/goods/create" class="btn btn-primary">
          发布第一个商品
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { goodsAPI, authAPI } from '@/utils/api'

const router = useRouter()

// 状态管理
const loading = ref(false)
const error = ref('')
const goodsList = ref([])
const isLoggedIn = ref(false)
const isAdmin = ref(false)
const username = ref('')
const categories = ref([])
const searchQuery = ref('')
const selectedCategory = ref(null)
const sortBy = ref('-created_at')
let searchTimeout = null

// 占位图
const placeholderImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuaXoOazleiDveWKoOi9vTwvdGV4dD48L3N2Zz4='

// 检查登录状态和管理员权限
const checkLoginStatus = async () => {
  isLoggedIn.value = authAPI.isLoggedIn()
  if (isLoggedIn.value) {
    username.value = localStorage.getItem('username') || '用户'
    // 检查是否为管理员
    try {
      const response = await authAPI.getProfile()
      if (response.data) {
        username.value = response.data.username
        isAdmin.value = response.data.is_staff || response.data.is_superuser || false
      }
    } catch (err) {
      console.error('获取用户信息失败:', err)
      isAdmin.value = false
    }
  }
}

// 加载分类列表
const loadCategories = async () => {
  try {
    const response = await goodsAPI.getCategories()
    categories.value = response.data || []
  } catch (err) {
    console.error('加载分类失败:', err)
  }
}

// 加载商品列表
const loadGoods = async () => {
  loading.value = true
  error.value = ''

  try {
    const params = {}
    
    // 搜索参数
    if (searchQuery.value.trim()) {
      params.title = searchQuery.value.trim()
    }
    
    // 分类筛选参数
    if (selectedCategory.value !== null) {
      params.category = selectedCategory.value
    }
    
    // 排序参数
    if (sortBy.value) {
      params.ordering = sortBy.value
    }

    const response = await goodsAPI.getGoods(params)
    goodsList.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (err) {
    console.error('加载商品失败:', err)
    error.value = '无法加载商品列表，请稍后重试。'
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

// 选择分类
const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
  loadGoods()
}

// 处理排序变化
const handleSortChange = () => {
  loadGoods()
}

// 跳转到商品详情
const goToDetail = (id) => {
  router.push(`/goods/${id}`)
}

// 编辑商品
const editGood = (id) => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }
  router.push(`/goods/${id}/edit`)
}

// 删除商品
const deleteGood = async (id) => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  if (!confirm('确定要删除这个商品吗？删除后无法恢复！')) {
    return
  }

  try {
    await goodsAPI.deleteGood(id)
    alert('商品删除成功')
    // 重新加载商品列表
    await loadGoods()
  } catch (err) {
    console.error('删除商品失败:', err)
    if (err.response?.data) {
      alert('删除失败：' + JSON.stringify(err.response.data))
    } else {
      alert('删除失败：网络错误')
    }
  }
}

// 退出登录
const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    authAPI.logout()
    isLoggedIn.value = false
    username.value = ''
    // 重新加载商品列表（清除所有者操作按钮）
    loadGoods()
  }
}

// 组件挂载时执行
onMounted(() => {
  checkLoginStatus()
  loadCategories()
  loadGoods()
})
</script>

<style scoped>
.goods-list-page {
  min-height: 100vh;
  background-color: var(--ios-bg-primary);
  font-family: var(--ios-font-family);
  padding-bottom: var(--ios-spacing-xl);
}

/* 布局容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

@media (max-width: 768px) {
  .container {
    padding: 0 12px;
  }
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

@media (max-width: 768px) {
  .navbar {
    padding: 10px 0;
    margin-bottom: var(--ios-spacing-md);
  }
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

@media (max-width: 768px) {
  .logo {
    font-size: 18px;
  }
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

@media (max-width: 768px) {
  .nav-link {
    margin-left: 0;
    font-size: 14px;
    padding: 4px 8px;
  }
}

.nav-link.router-link-active,
.nav-link.active {
  color: var(--ios-blue);
}

.admin-link {
  color: var(--ios-purple);
  font-weight: 600;
}

.admin-link.router-link-active {
  color: var(--ios-purple);
}

@media (hover: hover) {
  .nav-link:hover {
    color: var(--ios-blue);
  }
}

.user-info {
  color: var(--ios-text-secondary);
  font-size: var(--ios-font-size-subhead);
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
  color: var(--ios-blue);
  background-color: transparent;
  border: none;
  border-radius: var(--ios-radius-md);
  cursor: pointer;
  transition: all var(--ios-transition-fast);
  text-decoration: none;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}

@media (max-width: 768px) {
  .btn {
    padding: 10px 16px;
    font-size: 14px;
    min-height: 44px; /* iOS 推荐的最小触摸目标 */
  }
}

.btn:active:not(:disabled) {
  opacity: 0.6;
  transform: scale(0.97);
}

.btn-primary {
  color: #FFFFFF;
  background-color: var(--ios-blue);
}

.btn-primary:active:not(:disabled) {
  background-color: var(--ios-blue-dark);
}

.btn-success {
  color: #FFFFFF;
  background-color: var(--ios-green);
}

.btn-success:active:not(:disabled) {
  background-color: #2DA44E;
}

.btn-danger {
  color: #FFFFFF;
  background-color: var(--ios-red);
}

.btn-danger:active:not(:disabled) {
  background-color: #D32F2F;
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
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

@media (max-width: 768px) {
  .page-header {
    margin-bottom: 16px;
  }

  .section-title {
    font-size: 20px;
    padding-left: 10px;
    border-left-width: 2px;
  }
}

/* 搜索和筛选区域 */
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
  margin-bottom: 10px;
}

/* 搜索框 */
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

/* 分类筛选 */
.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.category-tag {
  padding: 6px 14px;
  font-size: var(--ios-font-size-caption);
  font-weight: 500;
  color: var(--ios-text-secondary);
  background-color: var(--ios-bg-tertiary);
  border: 1px solid var(--ios-separator);
  border-radius: var(--ios-radius-full);
  cursor: pointer;
  transition: all var(--ios-transition-fast);
  white-space: nowrap;
}

@media (hover: hover) {
  .category-tag:hover {
    background-color: rgba(0, 122, 255, 0.1);
    border-color: var(--ios-blue);
    color: var(--ios-blue);
  }
}

.category-tag.active {
  background-color: var(--ios-blue);
  color: #FFFFFF;
  border-color: var(--ios-blue);
}

.category-tag:active {
  transform: scale(0.95);
}

/* 排序选择 */
.sort-section {
  display: flex;
  align-items: center;
}

.sort-select {
  padding: 8px 12px;
  font-size: var(--ios-font-size-body);
  color: var(--ios-text-primary);
  background-color: var(--ios-bg-tertiary);
  border: 1px solid var(--ios-separator);
  border-radius: var(--ios-radius-md);
  cursor: pointer;
  transition: all var(--ios-transition-fast);
  min-width: 130px;
}

.sort-select:focus {
  outline: none;
  border-color: var(--ios-blue);
  background-color: var(--ios-bg-secondary);
}

/* 商品网格 */
.goods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

@media (max-width: 768px) {
  .goods-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .goods-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}

/* 商品卡片 - iOS 风格 */
.goods-card {
  background: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-lg);
  overflow: hidden;
  box-shadow: var(--ios-shadow-sm);
  transition: all var(--ios-transition-normal);
  cursor: pointer;
  border: 0.5px solid var(--ios-separator);
}

.goods-card:active {
  transform: scale(0.98);
  opacity: 0.9;
}

@media (hover: hover) {
  .goods-card:hover {
    box-shadow: var(--ios-shadow-md);
  }
}

.goods-img-wrapper {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: var(--ios-bg-tertiary);
  position: relative;
}

@media (max-width: 768px) {
  .goods-img-wrapper {
    height: 180px;
  }
}

@media (max-width: 480px) {
  .goods-img-wrapper {
    height: 200px;
  }
}

.goods-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--ios-transition-slow);
}

@media (hover: hover) {
  .goods-card:hover .goods-img {
    transform: scale(1.03);
  }
}

.goods-info {
  padding: 16px;
}

@media (max-width: 768px) {
  .goods-info {
    padding: 12px;
  }
}

.goods-title {
  font-size: var(--ios-font-size-body);
  font-weight: 600;
  margin-bottom: var(--ios-spacing-sm);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--ios-text-primary);
}

@media (max-width: 768px) {
  .goods-title {
    font-size: 14px;
    margin-bottom: 6px;
  }
}

.goods-desc {
  font-size: var(--ios-font-size-subhead);
  color: var(--ios-text-secondary);
  margin-bottom: var(--ios-spacing-md);
  height: 40px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

@media (max-width: 768px) {
  .goods-desc {
    font-size: 12px;
    height: 32px;
    margin-bottom: 8px;
    -webkit-line-clamp: 2;
  }
}

@media (max-width: 480px) {
  .goods-desc {
    height: 36px;
    -webkit-line-clamp: 2;
  }
}

.goods-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.goods-price {
  color: var(--ios-red);
  font-size: var(--ios-font-size-headline);
  font-weight: 700;
}

@media (max-width: 768px) {
  .goods-price {
    font-size: 18px;
  }
}

.goods-category {
  font-size: var(--ios-font-size-caption);
  color: var(--ios-blue);
  background: rgba(0, 122, 255, 0.1);
  padding: 4px 10px;
  border-radius: var(--ios-radius-full);
  font-weight: 600;
}

.goods-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--ios-font-size-caption);
  color: var(--ios-text-secondary);
  margin-bottom: var(--ios-spacing-sm);
}

.wish-count {
  color: var(--ios-pink);
}

.owner-name {
  color: var(--ios-text-secondary);
}

/* 所有者操作按钮 */
.owner-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #f3f4f6;
}

.btn-edit,
.btn-delete {
  flex: 1;
  padding: 8px 16px;
  border: none;
  border-radius: var(--ios-radius-sm);
  font-size: var(--ios-font-size-subhead);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--ios-transition-fast);
}

.btn-edit {
  background-color: var(--ios-blue);
  color: white;
}

.btn-edit:active {
  background-color: var(--ios-blue-dark);
  opacity: 0.8;
}

.btn-delete {
  background-color: var(--ios-red);
  color: white;
}

.btn-delete:active {
  background-color: #D32F2F;
  opacity: 0.8;
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

.empty-state p {
  font-size: 1.1rem;
  margin-bottom: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .goods-list-page {
    padding-bottom: var(--ios-spacing-md);
  }

  .nav-content {
    flex-wrap: wrap;
    gap: 8px;
  }

  .nav-links {
    margin-top: 8px;
    width: 100%;
    justify-content: flex-end;
    flex-wrap: wrap;
    gap: 8px;
  }

  .user-info {
    display: none; /* 移动端隐藏欢迎信息，节省空间 */
  }

  .filter-section {
    padding: 10px;
    margin-bottom: 12px;
  }

  .filter-row {
    flex-direction: column;
    gap: 10px;
    margin-bottom: 10px;
  }

  .search-box {
    width: 100%;
  }

  .search-input {
    padding: 10px 32px 10px 12px;
    font-size: 16px; /* 防止 iOS 自动缩放 */
  }

  .sort-select {
    width: 100%;
    min-width: auto;
    padding: 10px 12px;
    font-size: 16px; /* 防止 iOS 自动缩放 */
    min-height: 44px; /* iOS 推荐的最小触摸目标 */
  }

  .category-filter {
    gap: 6px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 2px;
  }

  .category-tag {
    padding: 8px 14px;
    font-size: 13px;
    min-height: 36px; /* 确保足够的触摸区域 */
    flex-shrink: 0;
  }

  .goods-card {
    border-radius: var(--ios-radius-md);
  }

  .goods-meta {
    margin-bottom: 8px;
    padding-bottom: 8px;
  }

  .goods-footer {
    font-size: 11px;
    margin-bottom: 8px;
  }

  .owner-actions {
    margin-top: 8px;
    padding-top: 8px;
    gap: 6px;
  }

  .btn-edit,
  .btn-delete {
    padding: 8px 12px;
    font-size: 13px;
    min-height: 36px;
  }

  .loading,
  .error,
  .empty-state {
    padding: var(--ios-spacing-lg) var(--ios-spacing-sm);
    font-size: 14px;
  }

  .empty-state p {
    font-size: 16px;
    margin-bottom: 16px;
  }
}

@media (max-width: 480px) {
  .nav-links {
    justify-content: space-between;
  }

  .nav-link {
    font-size: 13px;
    padding: 6px;
  }

  .btn {
    padding: 8px 12px;
    font-size: 13px;
  }

  .filter-section {
    padding: 8px;
  }

  .category-tag {
    padding: 6px 12px;
    font-size: 12px;
  }
}
</style>

