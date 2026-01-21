<template>
  <div class="create-goods-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container nav-content">
        <div class="logo">CampusTrade 🛒</div>
        <div class="nav-links">
          <router-link to="/" class="nav-link">首页</router-link>
          <router-link v-if="isLoggedIn" to="/orders" class="nav-link">我的订单</router-link>
          <router-link v-if="isLoggedIn" to="/user" class="nav-link">个人中心</router-link>
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
      <!-- 未登录提示 -->
      <div v-if="!isLoggedIn" class="error-card">
        <h3>请先登录</h3>
        <p>发布商品需要先登录账号</p>
        <router-link to="/login" class="btn btn-primary">去登录</router-link>
      </div>

      <!-- 发布表单 -->
      <div v-else class="form-card">
        <div class="page-header">
          <h1 class="section-title">发布商品</h1>
        </div>

        <!-- 错误提示 -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <!-- 成功提示 -->
        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>

        <form @submit.prevent="handleSubmit" v-if="!success">
          <div class="form-group">
            <label for="title">
              商品标题 <span class="required">*</span>
            </label>
            <input
              id="title"
              v-model="formData.title"
              type="text"
              class="form-input"
              placeholder="请输入商品标题"
              maxlength="100"
              required
              :disabled="loading"
            />
            <small>简洁明了地描述你的商品</small>
          </div>

          <div class="form-group">
            <label for="description">
              商品描述 <span class="required">*</span>
            </label>
            <textarea
              id="description"
              v-model="formData.description"
              class="form-textarea"
              placeholder="详细描述商品的特点、使用情况、购买时间等信息"
              rows="6"
              required
              :disabled="loading"
            ></textarea>
            <small>详细的描述有助于买家了解商品</small>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="price">
                价格 <span class="required">*</span>
              </label>
              <input
                id="price"
                v-model.number="formData.price"
                type="number"
                class="form-input"
                placeholder="0.00"
                step="0.01"
                min="0"
                max="999999.99"
                required
                :disabled="loading"
              />
              <small>请输入合理的价格（元）</small>
            </div>

            <div class="form-group">
              <label for="category">
                商品分类
              </label>
              <select
                id="category"
                v-model.number="formData.category_id"
                class="form-input"
                :disabled="loading || categoriesLoading"
              >
                <option value="">请选择分类</option>
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
              <small>选择商品所属分类</small>
            </div>
          </div>

          <div class="form-group">
            <label for="image">
              商品主图
            </label>
            <input
              id="image"
              type="file"
              accept="image/*"
              class="form-input"
              @change="handleImageChange"
              :disabled="loading"
            />
            <small>支持 JPG、PNG、GIF 格式，建议尺寸 800x600 以上</small>
            <div v-if="imagePreview" class="image-preview">
              <img :src="imagePreview" alt="预览图片" />
              <button
                type="button"
                @click="clearImage"
                class="btn-remove-image"
              >
                ✕ 移除
              </button>
            </div>
          </div>

          <div class="form-actions">
            <button
              type="submit"
              class="btn btn-primary btn-large"
              :disabled="loading || !isFormValid"
            >
              <span v-if="loading">发布中...</span>
              <span v-else>发布商品</span>
            </button>
            <button
              type="button"
              @click="handleReset"
              class="btn btn-outline btn-large"
              :disabled="loading"
            >
              重置表单
            </button>
          </div>
        </form>

        <!-- 成功后的操作 -->
        <div v-if="success && createdGoods" class="success-actions">
          <h3>🎉 商品发布成功！</h3>
          <p>你的商品《{{ createdGoods.title }}》已成功发布</p>
          <div class="action-buttons">
            <router-link
              :to="`/goods/${createdGoods.id}`"
              class="btn btn-primary"
            >
              查看商品
            </router-link>
            <router-link to="/" class="btn btn-success">
              返回列表
            </router-link>
            <button @click="handleContinue" class="btn btn-outline">
              继续发布
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
const categoriesLoading = ref(false)
const isLoggedIn = ref(false)
const isAdmin = ref(false)
const username = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const success = ref(false)
const createdGoods = ref(null)
const categories = ref([])

// 表单数据
const formData = ref({
  title: '',
  description: '',
  price: '',
  category_id: null,
  image: null
})

const imagePreview = ref(null)

// 表单验证
const isFormValid = computed(() => {
  return (
    formData.value.title.trim() &&
    formData.value.description.trim() &&
    formData.value.price &&
    formData.value.price > 0 &&
    formData.value.price <= 999999.99
  )
})

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
  categoriesLoading.value = true
  try {
    const response = await goodsAPI.getCategories()
    // 处理分类数据（可能是嵌套结构）
    const flattenCategories = (cats) => {
      let result = []
      cats.forEach(cat => {
        result.push(cat)
        if (cat.sub_cat && cat.sub_cat.length > 0) {
          result = result.concat(flattenCategories(cat.sub_cat))
        }
      })
      return result
    }
    categories.value = flattenCategories(response.data || [])
  } catch (err) {
    console.error('加载分类失败:', err)
    // 分类加载失败不影响发布商品
  } finally {
    categoriesLoading.value = false
  }
}

// 处理图片选择
const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    // 验证文件类型
    if (!file.type.startsWith('image/')) {
      errorMessage.value = '请选择图片文件'
      event.target.value = ''
      return
    }
    // 验证文件大小（5MB）
    if (file.size > 5 * 1024 * 1024) {
      errorMessage.value = '图片大小不能超过 5MB'
      event.target.value = ''
      return
    }
    formData.value.image = file
    // 显示预览
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 清除图片
const clearImage = () => {
  formData.value.image = null
  imagePreview.value = null
  const fileInput = document.getElementById('image')
  if (fileInput) {
    fileInput.value = ''
  }
}

// 重置表单
const handleReset = () => {
  if (confirm('确定要重置表单吗？所有输入的内容将被清空。')) {
    formData.value = {
      title: '',
      description: '',
      price: '',
      category_id: null,
      image: null
    }
    imagePreview.value = null
    errorMessage.value = ''
    successMessage.value = ''
    success.value = false
    createdGoods.value = null
  }
}

// 提交表单
const handleSubmit = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  // 验证表单
  if (!formData.value.title.trim()) {
    errorMessage.value = '请输入商品标题'
    return
  }

  if (!formData.value.description.trim()) {
    errorMessage.value = '请输入商品描述'
    return
  }

  if (!formData.value.price || formData.value.price <= 0) {
    errorMessage.value = '请输入有效的价格'
    return
  }

  if (formData.value.price > 999999.99) {
    errorMessage.value = '价格不能超过999999.99元'
    return
  }

  loading.value = true

  try {
    // 构建 FormData
    const submitData = new FormData()
    submitData.append('title', formData.value.title.trim())
    submitData.append('description', formData.value.description.trim())
    submitData.append('price', formData.value.price)
    
    if (formData.value.category_id) {
      submitData.append('category_id', formData.value.category_id)
    }
    
    if (formData.value.image) {
      submitData.append('image', formData.value.image)
    }

    const response = await goodsAPI.createGood(submitData)
    
    if (response.data) {
      createdGoods.value = response.data
      success.value = true
      successMessage.value = '商品发布成功！'
    } else {
      errorMessage.value = '发布失败，请重试'
    }
  } catch (err) {
    console.error('发布商品失败:', err)
    if (err.response?.data) {
      const errorData = err.response.data
      if (typeof errorData === 'object') {
        const errorMessages = []
        for (const [field, messages] of Object.entries(errorData)) {
          if (Array.isArray(messages)) {
            errorMessages.push(`${field}: ${messages.join(', ')}`)
          } else {
            errorMessages.push(`${field}: ${messages}`)
          }
        }
        errorMessage.value = errorMessages.join('; ') || '发布失败，请检查输入信息'
      } else {
        errorMessage.value = errorData || '发布失败，请检查输入信息'
      }
    } else if (err.response?.status === 401) {
      errorMessage.value = '请先登录'
      router.push('/login')
    } else {
      errorMessage.value = '发布失败：网络错误'
    }
  } finally {
    loading.value = false
  }
}

// 继续发布
const handleContinue = () => {
  success.value = false
  createdGoods.value = null
  formData.value = {
    title: '',
    description: '',
    price: '',
    category_id: null,
    image: null
  }
  imagePreview.value = null
  errorMessage.value = ''
  successMessage.value = ''
}

// 退出登录
const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    authAPI.logout()
    isLoggedIn.value = false
    username.value = ''
    router.push('/')
  }
}

// 组件挂载时执行
onMounted(() => {
  checkLoginStatus().then(() => {
    if (isLoggedIn.value) {
      loadCategories()
    }
  })
})
</script>

<style scoped>
.create-goods-page {
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

.user-info {
  color: var(--ios-text-secondary);
  font-size: var(--ios-font-size-subhead);
}

/* 卡片 */
.form-card,
.error-card {
  background: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-lg);
  box-shadow: var(--ios-shadow-sm);
  padding: var(--ios-spacing-xl);
  margin-top: var(--ios-spacing-md);
}

.error-card {
  text-align: center;
  padding: 60px 40px;
}

.error-card h3 {
  font-size: var(--ios-font-size-headline);
  color: var(--ios-red);
  margin-bottom: var(--ios-spacing-sm);
}

.error-card p {
  color: var(--ios-text-secondary);
  margin-bottom: var(--ios-spacing-md);
}

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

@media (max-width: 768px) {
  .page-header {
    margin-bottom: var(--ios-spacing-md);
  }

  .section-title {
    font-size: 20px;
    padding-left: 10px;
    border-left-width: 2px;
  }
}

/* 表单 */
.form-group {
  margin-bottom: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group label {
  display: block;
  margin-bottom: var(--ios-spacing-sm);
  font-weight: 600;
  color: var(--ios-text-primary);
  font-size: var(--ios-font-size-body);
}

.required {
  color: var(--ios-red);
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--ios-separator);
  border-radius: var(--ios-radius-md);
  font-size: var(--ios-font-size-body);
  font-family: var(--ios-font-family);
  transition: all var(--ios-transition-fast);
  box-sizing: border-box;
  background-color: var(--ios-bg-secondary);
  color: var(--ios-text-primary);
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--ios-blue);
  background-color: var(--ios-bg-secondary);
}

.form-input:disabled,
.form-textarea:disabled {
  background-color: var(--ios-bg-tertiary);
  cursor: not-allowed;
  opacity: 0.6;
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
}

.form-group small {
  display: block;
  margin-top: var(--ios-spacing-xs);
  color: var(--ios-text-secondary);
  font-size: var(--ios-font-size-footnote);
}

/* 图片预览 */
.image-preview {
  margin-top: var(--ios-spacing-md);
  text-align: center;
  position: relative;
  display: inline-block;
}

.image-preview img {
  max-width: 200px;
  max-height: 200px;
  border-radius: var(--ios-radius-md);
  box-shadow: var(--ios-shadow-sm);
}

.btn-remove-image {
  display: block;
  margin-top: var(--ios-spacing-sm);
  padding: var(--ios-spacing-xs) var(--ios-spacing-md);
  background-color: var(--ios-red);
  color: white;
  border: none;
  border-radius: var(--ios-radius-md);
  cursor: pointer;
  font-size: var(--ios-font-size-footnote);
  transition: all var(--ios-transition-fast);
}

.btn-remove-image:hover {
  background-color: var(--ios-red);
  opacity: 0.8;
}

.btn-remove-image:active {
  transform: scale(0.97);
  opacity: 0.6;
}

/* 按钮 */
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

.btn-large {
  padding: 14px 28px;
  font-size: var(--ios-font-size-body);
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 表单操作 */
.form-actions {
  display: flex;
  gap: var(--ios-spacing-md);
  justify-content: center;
  margin-top: var(--ios-spacing-lg);
  padding-top: var(--ios-spacing-lg);
  border-top: 0.5px solid var(--ios-separator);
}

/* 成功消息 */
.success-message {
  background-color: rgba(52, 199, 89, 0.1);
  color: var(--ios-green);
  padding: var(--ios-spacing-md);
  border-radius: var(--ios-radius-md);
  margin-bottom: var(--ios-spacing-md);
  font-size: var(--ios-font-size-body);
  border-left: 3px solid var(--ios-green);
}

.error-message {
  background-color: rgba(255, 59, 48, 0.1);
  color: var(--ios-red);
  padding: var(--ios-spacing-md);
  border-radius: var(--ios-radius-md);
  margin-bottom: var(--ios-spacing-md);
  font-size: var(--ios-font-size-body);
  border-left: 3px solid var(--ios-red);
}

.success-actions {
  text-align: center;
  padding: var(--ios-spacing-xl) var(--ios-spacing-md);
}

.success-actions h3 {
  font-size: var(--ios-font-size-headline);
  color: var(--ios-green);
  margin-bottom: var(--ios-spacing-sm);
}

.success-actions p {
  color: var(--ios-text-secondary);
  margin-bottom: var(--ios-spacing-lg);
}

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .form-card {
    padding: var(--ios-spacing-lg) var(--ios-spacing-md);
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: var(--ios-spacing-md);
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions .btn {
    width: 100%;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-buttons .btn {
    width: 100%;
  }

  .nav-content {
    flex-wrap: wrap;
  }

  .nav-links {
    margin-top: var(--ios-spacing-sm);
    width: 100%;
    justify-content: flex-end;
  }
}
</style>

