<template>
  <div class="register-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container nav-content">
        <div class="logo">CampusTrade 🛒</div>
        <div class="nav-links">
          <router-link to="/" class="nav-link">首页</router-link>
          <router-link to="/login" class="btn btn-primary" style="color: white; margin-left: 20px;">
            去登录
          </router-link>
        </div>
      </div>
    </nav>

    <div class="container">
      <div class="auth-demo-wrapper">
        <div class="auth-card">
          <div class="auth-header">
            <h3 class="auth-title">创建账号</h3>
            <p class="auth-subtitle">注册你的校园账号</p>
          </div>

          <!-- 错误提示 -->
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <!-- 成功提示 -->
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>

          <form @submit.prevent="handleRegister">
            <input
              v-model="formData.username"
              type="text"
              class="form-input"
              placeholder="用户名"
              required
              :disabled="loading"
            />
            
            <input
              v-model="formData.email"
              type="email"
              class="form-input"
              placeholder="邮箱"
              required
              :disabled="loading"
            />
            
            <input
              v-model="formData.phone"
              type="tel"
              class="form-input"
              placeholder="手机号"
              required
              :disabled="loading"
            />
            
            <input
              v-model="formData.student_id"
              type="text"
              class="form-input"
              placeholder="学号（仅数字）"
              required
              :disabled="loading"
              @input="validateStudentId"
            />
            <small v-if="studentIdError" class="error-text">{{ studentIdError }}</small>
            
            <input
              v-model="formData.college"
              type="text"
              class="form-input"
              placeholder="学院"
              required
              :disabled="loading"
            />
            
            <input
              v-model="formData.password"
              type="password"
              class="form-input"
              placeholder="密码"
              required
              :disabled="loading"
              @input="validatePassword"
            />
            
            <input
              v-model="formData.confirmPassword"
              type="password"
              class="form-input"
              placeholder="确认密码"
              required
              :disabled="loading"
              @input="validatePassword"
            />
            <small v-if="passwordError" class="error-text">{{ passwordError }}</small>

            <button
              type="submit"
              class="btn btn-primary btn-block"
              :disabled="loading || !isFormValid"
            >
              <span v-if="loading">注册中...</span>
              <span v-else>立即注册</span>
            </button>
          </form>

          <div class="auth-footer">
            <p>
              已有账号？
              <router-link to="/login" class="auth-link">去登录</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '@/utils/api'

const router = useRouter()

// 表单数据
const formData = ref({
  username: '',
  email: '',
  phone: '',
  student_id: '',
  college: '',
  password: '',
  confirmPassword: ''
})

// 状态管理
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const passwordError = ref('')
const studentIdError = ref('')

// 验证学号格式（仅数字）
const validateStudentId = () => {
  const studentId = formData.value.student_id
  if (studentId && !/^\d+$/.test(studentId)) {
    studentIdError.value = '学号只能包含数字'
  } else {
    studentIdError.value = ''
  }
}

// 验证密码一致性
const validatePassword = () => {
  // 如果确认密码为空，清除错误（允许用户正在输入）
  if (!formData.value.confirmPassword) {
    passwordError.value = ''
    return true
  }
  
  // 如果密码为空，清除错误
  if (!formData.value.password) {
    passwordError.value = ''
    return true
  }
  
  // 两个密码都有值时，检查是否一致
  if (formData.value.password !== formData.value.confirmPassword) {
    passwordError.value = '两次输入的密码不一致'
    return false
  } else {
    passwordError.value = ''
    return true
  }
}

// 表单验证
const isFormValid = computed(() => {
  // 基础字段验证
  const hasBasicFields = (
    formData.value.username &&
    formData.value.email &&
    formData.value.phone &&
    formData.value.student_id &&
    formData.value.college &&
    formData.value.password &&
    formData.value.confirmPassword
  )
  
  // 如果没有基础字段，直接返回false
  if (!hasBasicFields) {
    return false
  }
  
  // 检查是否有错误
  const hasNoErrors = !passwordError.value && !studentIdError.value
  
  // 检查密码是否一致（只有当两个密码都有值时才检查）
  const passwordsMatch = formData.value.password === formData.value.confirmPassword
  
  return hasBasicFields && hasNoErrors && passwordsMatch
})

// 处理注册
const handleRegister = async () => {
  // 清除之前的错误信息
  errorMessage.value = ''
  successMessage.value = ''

  // 验证密码一致性
  if (!validatePassword()) {
    errorMessage.value = '两次输入的密码不一致，请重新输入。'
    return
  }

  // 验证学号格式
  if (!/^\d+$/.test(formData.value.student_id)) {
    errorMessage.value = '学号只能包含数字'
    return
  }

  loading.value = true

  try {
    // 准备注册数据（不包含 confirmPassword）
    const { confirmPassword, ...registerData } = formData.value

    // 发送注册请求
    const response = await authAPI.register(registerData)

    if (response.status === 201 || response.status === 200) {
      successMessage.value = '注册成功！正在跳转到登录页面...'
      
      // 延迟跳转到登录页
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    }
  } catch (error) {
    console.error('注册错误:', error)
    
    if (error.response) {
      // 服务器返回了错误响应
      const errorData = error.response.data
      
      if (typeof errorData === 'object') {
        // 处理字段验证错误
        const errorMessages = []
        for (const [field, messages] of Object.entries(errorData)) {
          if (Array.isArray(messages)) {
            errorMessages.push(`${field}: ${messages.join(', ')}`)
          } else {
            errorMessages.push(`${field}: ${messages}`)
          }
        }
        errorMessage.value = errorMessages.join('; ') || '注册失败，请检查输入信息'
      } else {
        errorMessage.value = errorData || '注册失败，请检查输入信息'
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      errorMessage.value = '网络错误，请检查网络连接'
    } else {
      // 其他错误
      errorMessage.value = '注册失败：' + (error.message || '未知错误')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* iOS 风格样式 - 使用全局 iOS 变量 */

.register-page {
  min-height: 100vh;
  background-color: var(--ios-bg-primary);
  font-family: var(--ios-font-family);
}

/* 布局容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
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

.btn-primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background-color: var(--ios-blue);
}

.btn-block {
  width: 100%;
  display: flex;
}

/* 认证卡片 */
.auth-demo-wrapper {
  display: flex;
  justify-content: center;
  padding: 40px 0;
  min-height: calc(100vh - 200px);
}

.auth-card {
  background-color: var(--ios-bg-secondary);
  padding: var(--ios-spacing-xl);
  border-radius: var(--ios-radius-lg);
  box-shadow: var(--ios-shadow-md);
  border: 0.5px solid var(--ios-separator);
  width: 100%;
  max-width: 420px;
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-title {
  font-size: var(--ios-font-size-headline);
  color: var(--ios-text-primary);
  font-weight: 700;
  margin-bottom: var(--ios-spacing-xs);
}

.auth-subtitle {
  color: var(--ios-text-secondary);
  font-size: var(--ios-font-size-subhead);
}

/* 输入框 */
.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--ios-separator-opaque);
  border-radius: var(--ios-radius-md);
  margin-bottom: var(--ios-spacing-sm);
  font-size: var(--ios-font-size-body);
  font-family: var(--ios-font-family);
  color: var(--ios-text-primary);
  background-color: var(--ios-bg-secondary);
  transition: all var(--ios-transition-fast);
  box-sizing: border-box;
  -webkit-appearance: none;
  appearance: none;
}

.form-input:focus {
  outline: none;
  border-color: var(--ios-blue);
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
}

.form-input:disabled {
  background-color: var(--ios-bg-tertiary);
  cursor: not-allowed;
  opacity: 0.6;
}

/* 错误和成功消息 */
.error-message {
  background-color: rgba(255, 59, 48, 0.1);
  color: var(--ios-red);
  padding: 12px 16px;
  border-radius: var(--ios-radius-md);
  margin-bottom: var(--ios-spacing-md);
  font-size: var(--ios-font-size-body);
  border-left: 3px solid var(--ios-red);
}

.success-message {
  background-color: rgba(52, 199, 89, 0.1);
  color: var(--ios-green);
  padding: 12px 16px;
  border-radius: var(--ios-radius-md);
  margin-bottom: var(--ios-spacing-md);
  font-size: var(--ios-font-size-body);
  border-left: 3px solid var(--ios-green);
}

.error-text {
  display: block;
  color: var(--ios-red);
  font-size: var(--ios-font-size-subhead);
  margin-top: -4px;
  margin-bottom: var(--ios-spacing-sm);
  padding-left: var(--ios-spacing-sm);
}

/* 底部链接 */
.auth-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.auth-link {
  color: var(--primary-color);
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s;
}

.auth-link:hover {
  color: var(--primary-hover);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .auth-card {
    padding: 30px 20px;
    margin: 0 10px;
  }

  .nav-content {
    flex-direction: column;
    gap: 1rem;
  }

  .nav-links {
    width: 100%;
    justify-content: center;
  }
}
</style>

