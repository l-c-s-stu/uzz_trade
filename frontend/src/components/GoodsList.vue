<template>
  <div class="goods-list-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container nav-content">
        <div class="logo">CampusTrade 🛒</div>
        <div class="nav-links">
          <router-link to="/" class="nav-link active">首页</router-link>
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
const username = ref('')

// 占位图
const placeholderImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuaXoOazleiDveWKoOi9vTwvdGV4dD48L3N2Zz4='

// 检查登录状态
const checkLoginStatus = () => {
  isLoggedIn.value = authAPI.isLoggedIn()
  if (isLoggedIn.value) {
    username.value = localStorage.getItem('username') || '用户'
  }
}

// 加载商品列表
const loadGoods = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await goodsAPI.getGoods()
    goodsList.value = response.data || []
  } catch (err) {
    console.error('加载商品失败:', err)
    error.value = '无法加载商品列表，请稍后重试。'
  } finally {
    loading.value = false
  }
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
  loadGoods()
})
</script>

<style scoped>
/* 使用样式预览中的 CSS 变量和样式 */
:root {
  --primary-color: #4F46E5;
  --primary-hover: #4338ca;
  --text-main: #1F2937;
  --text-secondary: #6B7280;
  --bg-body: #F3F4F6;
  --bg-card: #FFFFFF;
  --danger: #EF4444;
  --success: #28a745;
  --radius-sm: 6px;
  --radius-md: 12px;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-hover: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.goods-list-page {
  min-height: 100vh;
  background-color: var(--bg-body);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  padding-bottom: 40px;
}

/* 布局容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 导航栏 */
.navbar {
  background: var(--bg-card);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 1rem 0;
  margin-bottom: 2rem;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--primary-color);
  letter-spacing: -0.5px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 15px;
}

.nav-link {
  margin-left: 2rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active,
.nav-link.active {
  color: var(--primary-color);
}

.user-info {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

/* 按钮 */
.btn {
  display: inline-block;
  padding: 0.6rem 1.2rem;
  border-radius: var(--radius-sm);
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
  font-size: 0.95rem;
  text-decoration: none;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.btn-success {
  background-color: var(--success);
  color: white;
}

.btn-success:hover {
  background-color: #1e7e34;
}

.btn-danger {
  background-color: var(--danger);
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

/* 页面标题 */
.page-header {
  margin-bottom: 30px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: var(--text-main);
  border-left: 5px solid var(--primary-color);
  padding-left: 15px;
}

/* 商品网格 */
.goods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

/* 商品卡片 */
.goods-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid rgba(0, 0, 0, 0.02);
}

.goods-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}

.goods-img-wrapper {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f3f4f6;
  position: relative;
}

.goods-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.goods-card:hover .goods-img {
  transform: scale(1.05);
}

.goods-info {
  padding: 16px;
}

.goods-title {
  font-size: 1.05rem;
  font-weight: 600;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--text-main);
}

.goods-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 12px;
  height: 40px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
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
  color: var(--danger);
  font-size: 1.25rem;
  font-weight: 700;
}

.goods-category {
  font-size: 0.75rem;
  color: var(--primary-color);
  background: #EEF2FF;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.goods-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-bottom: 10px;
}

.wish-count {
  color: #f39c12;
}

.owner-name {
  color: var(--text-secondary);
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
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-edit {
  background-color: var(--primary-color);
  color: white;
}

.btn-edit:hover {
  background-color: var(--primary-hover);
}

.btn-delete {
  background-color: var(--danger);
  color: white;
}

.btn-delete:hover {
  background-color: #c82333;
}

/* 加载和错误状态 */
.loading,
.error,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.error {
  color: var(--danger);
}

.empty-state p {
  font-size: 1.1rem;
  margin-bottom: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .goods-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
  }

  .nav-content {
    flex-wrap: wrap;
  }

  .nav-links {
    margin-top: 10px;
    width: 100%;
    justify-content: flex-end;
  }
}
</style>

