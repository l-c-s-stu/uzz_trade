<template>
  <div class="admin-users-page">
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
        <h1 class="section-title">用户管理</h1>
      </div>

      <!-- 搜索和筛选 -->
      <div class="filter-section">
        <div class="search-box">
          <input
            v-model="searchQuery"
            @input="handleSearch"
            type="text"
            placeholder="搜索用户名、邮箱、学号..."
            class="search-input"
          />
          <span class="search-icon">🔍</span>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <p>正在加载用户列表...</p>
      </div>

      <!-- 用户列表 -->
      <div v-else-if="users.length > 0" class="users-table">
        <div class="table-header">
          <div class="col-id">ID</div>
          <div class="col-username">用户名</div>
          <div class="col-email">邮箱</div>
          <div class="col-student-id">学号</div>
          <div class="col-college">学院</div>
          <div class="col-phone">手机号</div>
          <div class="col-status">状态</div>
          <div class="col-date">注册时间</div>
          <div class="col-actions">操作</div>
        </div>
        <div
          v-for="user in users"
          :key="user.id"
          class="table-row"
        >
          <div class="col-id">{{ user.id }}</div>
          <div class="col-username">{{ user.username }}</div>
          <div class="col-email">{{ user.email || '-' }}</div>
          <div class="col-student-id">{{ user.student_id || '-' }}</div>
          <div class="col-college">{{ user.college || '-' }}</div>
          <div class="col-phone">{{ user.phone || '-' }}</div>
          <div class="col-status">
            <span v-if="user.is_staff" class="badge badge-admin">管理员</span>
            <span v-else-if="user.is_active" class="badge badge-active">正常</span>
            <span v-else class="badge badge-inactive">禁用</span>
          </div>
          <div class="col-date">{{ formatDate(user.date_joined) }}</div>
          <div class="col-actions">
            <button
              @click="toggleUserStatus(user)"
              :class="['btn', 'btn-sm', user.is_active ? 'btn-warning' : 'btn-success']"
            >
              {{ user.is_active ? '禁用' : '启用' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <p>暂无用户数据</p>
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
const users = ref([])
const searchQuery = ref('')
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

// 加载用户列表
const loadUsers = async () => {
  loading.value = true
  try {
    const params = {}
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim()
    }
    const response = await adminAPI.getUsers(params)
    users.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (err) {
    console.error('加载用户列表失败:', err)
    alert('加载用户列表失败')
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
    loadUsers()
  }, 500)
}

// 切换用户状态
const toggleUserStatus = async (user) => {
  const action = user.is_active ? '禁用' : '启用'
  if (!confirm(`确定要${action}用户 "${user.username}" 吗？`)) {
    return
  }

  try {
    await adminAPI.updateUserStatus(user.id, !user.is_active)
    alert(`用户已${action}`)
    await loadUsers()
  } catch (err) {
    console.error('更新用户状态失败:', err)
    alert('操作失败：' + (err.response?.data?.detail || '网络错误'))
  }
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
      loadUsers()
    }
  })
})
</script>

<style scoped>
.admin-users-page {
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
  text-decoration: none;
}

.btn-sm {
  padding: 6px 12px;
  font-size: var(--ios-font-size-caption);
}

.btn-success {
  color: #FFFFFF;
  background-color: var(--ios-green);
}

.btn-warning {
  color: #FFFFFF;
  background-color: var(--ios-orange);
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

/* 搜索框 */
.filter-section {
  background: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-md);
  padding: 12px;
  margin-bottom: var(--ios-spacing-md);
  border: 0.5px solid var(--ios-separator);
  box-shadow: var(--ios-shadow-sm);
}

.search-box {
  position: relative;
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

/* 用户表格 */
.users-table {
  background: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-lg);
  overflow: hidden;
  box-shadow: var(--ios-shadow-sm);
  border: 0.5px solid var(--ios-separator);
}

.table-header,
.table-row {
  display: grid;
  grid-template-columns: 60px 120px 180px 120px 120px 120px 100px 120px 100px;
  gap: 12px;
  padding: 12px;
  align-items: center;
}

.table-header {
  background: var(--ios-bg-tertiary);
  font-weight: 600;
  font-size: var(--ios-font-size-subhead);
  color: var(--ios-text-primary);
  border-bottom: 1px solid var(--ios-separator);
}

.table-row {
  border-bottom: 0.5px solid var(--ios-separator);
  transition: background-color var(--ios-transition-fast);
}

.table-row:hover {
  background-color: var(--ios-bg-tertiary);
}

.table-row:last-child {
  border-bottom: none;
}

.col-id,
.col-username,
.col-email,
.col-student-id,
.col-college,
.col-phone,
.col-status,
.col-date,
.col-actions {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.col-email {
  font-size: var(--ios-font-size-subhead);
}

/* 徽章 */
.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: var(--ios-radius-full);
  font-size: var(--ios-font-size-caption);
  font-weight: 600;
}

.badge-admin {
  background-color: rgba(79, 70, 229, 0.1);
  color: #4F46E5;
}

.badge-active {
  background-color: rgba(52, 199, 89, 0.1);
  color: var(--ios-green);
}

.badge-inactive {
  background-color: rgba(142, 142, 147, 0.1);
  color: var(--ios-text-tertiary);
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
@media (max-width: 1200px) {
  .table-header,
  .table-row {
    grid-template-columns: 50px 100px 150px 100px 100px 100px 80px 100px 80px;
    font-size: var(--ios-font-size-caption);
  }
}

@media (max-width: 768px) {
  .users-table {
    overflow-x: auto;
  }

  .table-header,
  .table-row {
    min-width: 1000px;
  }
}
</style>



