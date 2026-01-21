<template>
  <div class="goods-detail-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container nav-content">
        <router-link to="/" class="logo">CampusTrade 🛒</router-link>
        <div class="nav-links">
          <router-link to="/" class="nav-link">首页</router-link>
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
      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <p>正在加载商品详情...</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <div class="error-actions">
          <button @click="loadGoodsDetail" class="btn btn-primary">重试</button>
          <router-link to="/" class="btn btn-outline">返回首页</router-link>
        </div>
      </div>

      <!-- 商品详情 -->
      <div v-else-if="goods" class="goods-detail-wrapper">
        <!-- 商品信息卡片 -->
        <div class="goods-detail-card">
          <div class="goods-info-grid">
            <!-- 商品图片区域 -->
            <div class="goods-image-section">
              <div class="main-image-wrapper">
                <img
                  :src="currentImage || goods.image || placeholderImage"
                  :alt="goods.title"
                  class="main-image"
                  @error="handleImageError"
                />
              </div>
              <!-- 详情图片列表 -->
              <div v-if="allImages.length > 1" class="image-thumbnails">
                <div
                  v-for="(img, index) in allImages"
                  :key="index"
                  class="thumbnail"
                  :class="{ active: currentImage === img.url || (!currentImage && index === 0) }"
                  @click="currentImage = img.url"
                >
                  <img :src="img.url" :alt="`商品图片 ${index + 1}`" @error="handleImageError" />
                </div>
              </div>
            </div>

            <!-- 商品信息区域 -->
            <div class="goods-meta-section">
              <h1 class="goods-title">{{ goods.title }}</h1>
              
              <div class="goods-price">¥{{ goods.price }}</div>
              
              <div class="goods-stats">
                <div class="stat-item">
                  <div class="stat-label">想买人数</div>
                  <div class="stat-value">❤️ {{ goods.wish_count || 0 }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">发布人</div>
                  <div class="stat-value">{{ goods.owner_name }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">发布时间</div>
                  <div class="stat-value">{{ formatDate(goods.created_at) }}</div>
                </div>
                <div v-if="goods.category" class="stat-item">
                  <div class="stat-label">分类</div>
                  <div class="stat-value">{{ goods.category.name }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">状态</div>
                  <div class="stat-value">
                    <span class="status-badge" :class="getStatusClass(goods.status)">
                      {{ goods.status_display || getStatusText(goods.status) }}
                    </span>
                  </div>
                </div>
              </div>

              <div class="goods-description">
                <h3>商品描述</h3>
                <p>{{ goods.description }}</p>
              </div>

              <!-- 操作按钮 -->
              <div class="action-buttons">
                <button
                  v-if="!goods.is_owner && goods.status === 1"
                  @click="handleWish"
                  class="btn btn-wish"
                  :disabled="wishLoading"
                >
                  <span v-if="wishLoading">处理中...</span>
                  <span v-else>❤️ 想买</span>
                </button>
                
                <button
                  v-if="!goods.is_owner && goods.status === 1"
                  @click="handleBuy"
                  class="btn btn-buy"
                  :disabled="buyLoading"
                >
                  <span v-if="buyLoading">处理中...</span>
                  <span v-else>💰 立即购买</span>
                </button>

                <button
                  v-if="!goods.is_owner"
                  @click="handleContact"
                  class="btn btn-contact"
                >
                  📞 联系卖家
                </button>

                <!-- 所有者操作按钮 -->
                <template v-if="goods.is_owner">
                  <router-link
                    :to="`/goods/${goods.id}/edit`"
                    class="btn btn-edit"
                  >
                    ✏️ 编辑商品
                  </router-link>
                  <button
                    @click="handleDelete"
                    class="btn btn-delete"
                  >
                    🗑️ 删除商品
                  </button>
                </template>
              </div>
            </div>
          </div>
        </div>

        <!-- 评论区域 -->
        <div class="comments-section">
          <div class="comments-header">
            <h2>评论 ({{ comments.length }})</h2>
          </div>

          <!-- 评论表单 -->
          <div v-if="isLoggedIn" class="comment-form">
            <textarea
              v-model="commentContent"
              class="comment-textarea"
              placeholder="写下你的评论..."
              rows="4"
            ></textarea>
            <button
              @click="handleSubmitComment"
              class="btn btn-primary"
              :disabled="commentLoading || !commentContent.trim()"
            >
              <span v-if="commentLoading">发表中...</span>
              <span v-else>发表评论</span>
            </button>
          </div>
          <div v-else class="comment-login-prompt">
            <p>请先 <router-link to="/login">登录</router-link> 后发表评论</p>
          </div>

          <!-- 评论列表 -->
          <div v-if="commentsLoading" class="loading">
            <p>加载评论中...</p>
          </div>
          <div v-else-if="comments.length === 0" class="empty-comments">
            <p>暂无评论，快来发表第一条评论吧！</p>
          </div>
          <div v-else class="comments-list">
            <div
              v-for="comment in comments"
              :key="comment.id"
              class="comment-item"
            >
              <div class="comment-header">
                <span class="comment-user">{{ comment.user_name }}</span>
                <span class="comment-time">{{ formatDateTime(comment.created_at) }}</span>
              </div>
              <div class="comment-content">{{ comment.content }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { goodsAPI, commentsAPI, wishesAPI, ordersAPI, authAPI } from '@/utils/api'

const route = useRoute()
const router = useRouter()

// 商品ID
const goodsId = computed(() => parseInt(route.params.id))

// 状态管理
const loading = ref(false)
const commentsLoading = ref(false)
const wishLoading = ref(false)
const buyLoading = ref(false)
const commentLoading = ref(false)
const error = ref('')
const goods = ref(null)
const comments = ref([])
const commentContent = ref('')
const currentImage = ref(null)
const isLoggedIn = ref(false)
const isAdmin = ref(false)
const username = ref('')

// 占位图
const placeholderImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjQwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuaXoOazleiDveWKoOi9vTwvdGV4dD48L3N2Zz4='

// 所有图片（主图 + 详情图）
const allImages = computed(() => {
  const images = []
  if (goods.value?.image) {
    images.push({ url: goods.value.image, type: 'main' })
  }
  if (goods.value?.images && Array.isArray(goods.value.images) && goods.value.images.length > 0) {
    goods.value.images.forEach(img => {
      if (img.image) {
        images.push({ url: img.image, type: 'detail' })
      }
    })
  }
  return images
})

// 监听路由变化，重新加载数据
watch(() => route.params.id, (newId) => {
  if (newId) {
    loadGoodsDetail()
    loadComments()
  }
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

// 图片加载错误处理
const handleImageError = (event) => {
  event.target.src = placeholderImage
}

// 加载商品详情
const loadGoodsDetail = async () => {
  if (!goodsId.value || isNaN(goodsId.value)) {
    error.value = '商品ID无效'
    return
  }

  loading.value = true
  error.value = ''
  currentImage.value = null

  try {
    const response = await goodsAPI.getGoodDetail(goodsId.value)
    goods.value = response.data
    
    // 设置默认显示图片
    if (goods.value.image) {
      currentImage.value = goods.value.image
    } else if (goods.value.images && Array.isArray(goods.value.images) && goods.value.images.length > 0) {
      const firstImage = goods.value.images.find(img => img.image)
      if (firstImage) {
        currentImage.value = firstImage.image
      }
    }
  } catch (err) {
    console.error('加载商品详情失败:', err)
    if (err.response?.status === 404) {
      error.value = '商品不存在'
    } else if (err.response?.status === 403) {
      error.value = '无权访问此商品'
    } else {
      error.value = '加载商品详情失败，请稍后重试'
    }
  } finally {
    loading.value = false
  }
}

// 加载评论
const loadComments = async () => {
  if (!goodsId.value || isNaN(goodsId.value)) return

  commentsLoading.value = true
  try {
    const response = await commentsAPI.getComments(goodsId.value)
    comments.value = response.data || []
  } catch (err) {
    console.error('加载评论失败:', err)
    // 评论加载失败不影响页面显示
  } finally {
    commentsLoading.value = false
  }
}

// 处理想买
const handleWish = async () => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  wishLoading.value = true
  try {
    const response = await wishesAPI.addToWish(goodsId.value)
    alert(response.data?.message || '已添加到想买列表')
    // 重新加载商品详情以更新想买人数
    await loadGoodsDetail()
  } catch (err) {
    console.error('添加想买失败:', err)
    if (err.response?.status === 400) {
      const errorMsg = err.response.data?.detail || err.response.data?.message || '你已经想买过这个商品了'
      alert(errorMsg)
    } else if (err.response?.status === 401) {
      alert('请先登录')
      router.push('/login')
    } else {
      alert('操作失败：' + (err.response?.data?.detail || err.response?.data?.message || '网络错误'))
    }
  } finally {
    wishLoading.value = false
  }
}

// 处理购买
const handleBuy = async () => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  if (goods.value.status !== 1) {
    alert('该商品已下架或已售出')
    return
  }

  if (goods.value.is_owner) {
    alert('不能购买自己发布的商品')
    return
  }

  if (!confirm(`确定要购买 "${goods.value.title}" 吗？\n价格：¥${goods.value.price}`)) {
    return
  }

  // 验证商品ID
  if (!goodsId.value || isNaN(goodsId.value)) {
    alert('商品ID无效，请刷新页面重试')
    return
  }

  // 验证商品状态
  if (goods.value && goods.value.status !== 1) {
    alert(`商品状态为${goods.value.status_display || '不可购买'}，无法购买`)
    return
  }

  buyLoading.value = true
  
  // 准备请求数据
  // 后端需要 goods_id（不是 goods）和 order_mount
  // order_mount 会在后端自动设置为商品价格，但前端也需要提供
  const requestData = {
    goods_id: goodsId.value,
    order_mount: goods.value?.price || 0,  // 提供订单金额（后端会自动验证）
    post_script: ''
  }
  
  console.log('准备创建订单，数据:', requestData)
  console.log('商品ID类型:', typeof goodsId.value, '值:', goodsId.value)
  console.log('商品信息:', goods.value)
  console.log('订单金额:', requestData.order_mount)
  
  try {
    const response = await ordersAPI.createOrder(requestData)
    
    console.log('订单创建响应:', response)
    console.log('响应数据:', response.data)
    
    // 后端返回格式：{ message: '订单创建成功', data: {...} }
    const responseOrderData = response.data?.data || response.data
    const orderId = responseOrderData?.id
    
    console.log('订单数据:', responseOrderData)
    console.log('订单ID:', orderId)
    
    if (orderId) {
      alert('订单创建成功！')
      router.push(`/orders/${orderId}`)
    } else {
      console.warn('订单创建成功但未返回订单ID，跳转到订单列表')
      alert('订单创建成功！')
      router.push('/orders')
    }
  } catch (err) {
    console.error('创建订单失败 - 完整错误对象:', err)
    console.error('错误响应:', err.response)
    console.error('错误数据:', err.response?.data)
    console.error('错误状态:', err.response?.status)
    console.error('请求配置:', err.config)
    
    // 详细的错误处理
    if (err.response) {
      const status = err.response.status
      const errorData = err.response.data
      
      if (status === 400) {
        // 400 Bad Request - 通常是验证错误
        let errorMsg = '创建订单失败'
        let errorDetails = []
        
        // 打印完整的错误数据用于调试
        console.log('400错误 - 完整错误数据:', JSON.stringify(errorData, null, 2))
        
        if (errorData?.detail) {
          // DRF 标准错误格式
          if (typeof errorData.detail === 'string') {
            errorMsg = errorData.detail
            errorDetails.push(errorData.detail)
          } else if (Array.isArray(errorData.detail)) {
            errorMsg = errorData.detail.join(', ')
            errorDetails = errorData.detail
          } else if (typeof errorData.detail === 'object') {
            // 字段级错误
            const fieldErrors = Object.entries(errorData.detail)
              .map(([field, errors]) => {
                const errorText = Array.isArray(errors) ? errors.join(', ') : String(errors)
                errorDetails.push(`${field}: ${errorText}`)
                return `${field}: ${errorText}`
              })
            errorMsg = fieldErrors.join('\n') || '创建订单失败'
          }
        } else if (errorData?.message) {
          errorMsg = errorData.message
          errorDetails.push(errorData.message)
        } else if (errorData?.goods_id) {
          // 商品相关错误（最常见）
          const goodsError = Array.isArray(errorData.goods_id) 
            ? errorData.goods_id.join(', ') 
            : errorData.goods_id
          errorMsg = goodsError
          errorDetails.push(`商品错误: ${goodsError}`)
        } else if (typeof errorData === 'object') {
          // 尝试提取所有错误消息
          Object.entries(errorData).forEach(([field, errors]) => {
            if (Array.isArray(errors)) {
              errors.forEach(err => errorDetails.push(`${field}: ${err}`))
            } else if (typeof errors === 'string') {
              errorDetails.push(`${field}: ${errors}`)
            } else if (typeof errors === 'object') {
              errorDetails.push(`${field}: ${JSON.stringify(errors)}`)
            }
          })
          
          if (errorDetails.length > 0) {
            errorMsg = errorDetails.join('\n')
          } else {
            // 如果无法解析，显示原始数据
            errorMsg = JSON.stringify(errorData)
          }
        } else if (typeof errorData === 'string') {
          errorMsg = errorData
          errorDetails.push(errorData)
        }
        
        // 显示详细的错误信息
        console.error('400错误详情:', errorDetails)
        alert(`创建订单失败：\n\n${errorMsg}\n\n请检查：\n1. 商品状态是否为"在售"\n2. 商品是否存在\n3. 是否已登录`)
      } else if (status === 401) {
        alert('请先登录')
        router.push('/login')
      } else if (status === 403) {
        alert('无权创建订单')
      } else if (status === 404) {
        alert('商品不存在')
      } else {
        const errorMsg = errorData?.detail || errorData?.message || `服务器错误 (${status})`
        alert(`创建订单失败：${errorMsg}`)
      }
    } else if (err.request) {
      // 请求已发送但没有收到响应
      alert('创建订单失败：网络错误，请检查网络连接')
    } else {
      // 其他错误
      alert('创建订单失败：' + (err.message || '未知错误'))
    }
  } finally {
    buyLoading.value = false
  }
}

// 处理联系卖家
const handleContact = () => {
  alert('联系卖家功能开发中...\n\n你可以通过以下方式联系卖家：\n1. 在评论区留言\n2. 查看卖家联系方式')
}

// 处理删除商品
const handleDelete = async () => {
  if (!confirm('确定要删除这个商品吗？删除后无法恢复！')) {
    return
  }

  try {
    await goodsAPI.deleteGood(goodsId.value)
    alert('商品删除成功')
    router.push('/')
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
  }
}

// 处理发表评论
const handleSubmitComment = async () => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  const content = commentContent.value.trim()
  if (!content) {
    alert('请输入评论内容')
    return
  }

  commentLoading.value = true
  try {
    await commentsAPI.createComment(goodsId.value, content)
    commentContent.value = ''
    alert('评论发表成功！')
    // 重新加载评论
    await loadComments()
  } catch (err) {
    console.error('发表评论失败:', err)
    if (err.response?.status === 401) {
      alert('请先登录')
      router.push('/login')
    } else {
      alert('发表评论失败：' + (err.response?.data?.detail || err.response?.data?.message || '网络错误'))
    }
  } finally {
    commentLoading.value = false
  }
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

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (e) {
    return dateString
  }
}

// 格式化日期时间
const formatDateTime = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (e) {
    return dateString
  }
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    1: '在售',
    2: '已出',
    3: '下架'
  }
  return statusMap[status] || '未知'
}

// 获取状态样式类
const getStatusClass = (status) => {
  const classMap = {
    1: 'status-onsale',
    2: 'status-sold',
    3: 'status-offline'
  }
  return classMap[status] || ''
}

// 组件挂载时执行
onMounted(() => {
  checkLoginStatus()
  loadGoodsDetail()
  loadComments()
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
  --warning: #ffc107;
  --radius-sm: 6px;
  --radius-md: 12px;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-hover: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.goods-detail-page {
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
  text-decoration: none;
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
.nav-link.router-link-active {
  color: var(--primary-color);
}

.admin-link {
  color: var(--ios-purple);
  font-weight: 600;
}

.admin-link.router-link-active {
  color: var(--ios-purple);
}

.user-info {
  color: var(--text-secondary);
  font-size: 0.9rem;
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

.btn-outline {
  background-color: transparent;
  border: 1px solid var(--ios-blue);
  color: var(--ios-blue);
  margin-left: 10px;
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

.btn-wish {
  background-color: var(--ios-orange);
  color: #FFFFFF;
}

.btn-wish:hover:not(:disabled) {
  background-color: #E68900;
}

.btn-wish:active:not(:disabled) {
  background-color: #E68900;
  opacity: 0.8;
  transform: scale(0.97);
}

.btn-buy {
  background-color: var(--ios-red);
  color: #FFFFFF;
}

.btn-buy:hover:not(:disabled) {
  background-color: #D32F2F;
}

.btn-buy:active:not(:disabled) {
  background-color: #D32F2F;
  opacity: 0.8;
  transform: scale(0.97);
}

.btn-contact {
  background-color: var(--ios-green);
  color: #FFFFFF;
}

.btn-contact:hover:not(:disabled) {
  background-color: #2DA44E;
}

.btn-contact:active:not(:disabled) {
  background-color: #2DA44E;
  opacity: 0.8;
  transform: scale(0.97);
}

.btn-edit {
  background-color: var(--ios-blue);
  color: #FFFFFF;
}

.btn-edit:hover:not(:disabled) {
  background-color: var(--ios-blue-dark);
}

.btn-edit:active:not(:disabled) {
  background-color: var(--ios-blue-dark);
  opacity: 0.8;
  transform: scale(0.97);
}

.btn-delete {
  background-color: var(--ios-red);
  color: #FFFFFF;
}

.btn-delete:hover:not(:disabled) {
  background-color: #D32F2F;
}

.btn-delete:active:not(:disabled) {
  background-color: #D32F2F;
  opacity: 0.8;
  transform: scale(0.97);
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 商品详情卡片 */
.goods-detail-wrapper {
  margin-top: 20px;
}

.goods-detail-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  padding: 30px;
  margin-bottom: 30px;
}

.goods-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

/* 商品图片区域 */
.goods-image-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.main-image-wrapper {
  width: 100%;
  height: 500px;
  overflow: hidden;
  border-radius: var(--radius-md);
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-thumbnails {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 5px 0;
}

.thumbnail {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
  flex-shrink: 0;
}

.thumbnail:hover {
  border-color: var(--primary-color);
}

.thumbnail.active {
  border-color: var(--primary-color);
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 商品信息区域 */
.goods-meta-section {
  display: flex;
  flex-direction: column;
}

.goods-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 20px;
  line-height: 1.2;
}

.goods-price {
  font-size: 2.5rem;
  color: var(--danger);
  font-weight: 700;
  margin-bottom: 25px;
}

.goods-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: var(--radius-sm);
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 5px;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-main);
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.9rem;
  display: inline-block;
}

.status-onsale {
  background-color: #D1FAE5;
  color: #065F46;
}

.status-sold {
  background-color: #FEE2E2;
  color: #991B1B;
}

.status-offline {
  background-color: #F3F4F6;
  color: #6B7280;
}

.goods-description {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: var(--radius-sm);
}

.goods-description h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 10px;
  color: var(--text-main);
}

.goods-description p {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text-secondary);
  white-space: pre-wrap;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.action-buttons .btn {
  flex: 1;
  min-width: 120px;
}

/* 评论区域 */
.comments-section {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  padding: 30px;
}

.comments-header {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f3f4f6;
}

.comments-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-main);
}

.comment-form {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: var(--radius-sm);
}

.comment-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #E5E7EB;
  border-radius: var(--radius-sm);
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  margin-bottom: 12px;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.comment-textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.comment-login-prompt {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: var(--radius-sm);
  text-align: center;
  color: var(--text-secondary);
}

.comment-login-prompt a {
  color: var(--primary-color);
  font-weight: 600;
  text-decoration: none;
}

.comment-login-prompt a:hover {
  text-decoration: underline;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  padding: 20px;
  background: #f8f9fa;
  border-radius: var(--radius-sm);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.comment-user {
  font-weight: 600;
  color: var(--text-main);
}

.comment-time {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.comment-content {
  color: var(--text-secondary);
  line-height: 1.6;
  white-space: pre-wrap;
}

.empty-comments {
  text-align: center;
  padding: 40px;
  color: var(--text-secondary);
}

/* 加载和错误状态 */
.loading,
.error {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.error {
  color: var(--danger);
}

.error-actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .goods-info-grid {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .main-image-wrapper {
    height: 300px;
  }

  .goods-title {
    font-size: 1.5rem;
  }

  .goods-price {
    font-size: 2rem;
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
    margin-top: 10px;
    width: 100%;
    justify-content: flex-end;
  }

  .error-actions {
    flex-direction: column;
  }

  .error-actions .btn {
    width: 100%;
    margin-left: 0;
  }
}
</style>
