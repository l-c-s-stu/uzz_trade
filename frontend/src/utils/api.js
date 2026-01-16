/**
 * API 工具类 - 使用 axios
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加 token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理 token 刷新
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // 如果 token 过期，尝试刷新
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/users/token/refresh/`, {
            refresh: refreshToken
          })

          if (response.data.access) {
            localStorage.setItem('access', response.data.access)
            originalRequest.headers.Authorization = `Bearer ${response.data.access}`
            return apiClient(originalRequest)
          }
        }
      } catch (refreshError) {
        // 刷新失败，清除 token 并跳转到登录页
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        localStorage.removeItem('username')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// 用户认证相关
export const authAPI = {
  // 登录
  login: (username, password) => {
    return apiClient.post('/users/login/', { username, password })
  },

  // 注册
  register: (userData) => {
    return apiClient.post('/users/register/', userData)
  },

  // 刷新 token
  refreshToken: (refresh) => {
    return apiClient.post('/users/token/refresh/', { refresh })
  },

  // 检查是否登录
  isLoggedIn: () => {
    return !!localStorage.getItem('access')
  },

  // 登出
  logout: () => {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    localStorage.removeItem('username')
  }
}

// 商品相关
export const goodsAPI = {
  // 获取商品列表
  getGoods: () => {
    return apiClient.get('/goods/')
  },

  // 获取商品详情
  getGoodDetail: (id) => {
    return apiClient.get(`/goods/${id}/`)
  },

  // 创建商品
  createGood: (formData) => {
    return apiClient.post('/goods/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 更新商品
  updateGood: (id, formData) => {
    return apiClient.put(`/goods/${id}/update/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 删除商品
  deleteGood: (id) => {
    return apiClient.delete(`/goods/${id}/delete/`)
  },

  // 获取分类列表
  getCategories: () => {
    return apiClient.get('/goods/categories/')
  }
}

// 评论相关
export const commentsAPI = {
  // 获取商品评论
  getComments: (goodsId) => {
    return apiClient.get(`/goods/${goodsId}/comments/`)
  },

  // 发表评论
  createComment: (goodsId, content) => {
    return apiClient.post(`/goods/${goodsId}/comments/`, { content })
  }
}

// 想买相关
export const wishesAPI = {
  // 添加想买
  addToWish: (goodsId) => {
    return apiClient.post(`/goods/${goodsId}/wish/`)
  },

  // 取消想买
  removeFromWish: (goodsId) => {
    return apiClient.delete(`/goods/${goodsId}/wish/`)
  }
}

// 订单相关
export const ordersAPI = {
  // 获取订单列表
  getOrders: () => {
    return apiClient.get('/orders/')
  },

  // 创建订单
  createOrder: (orderData) => {
    return apiClient.post('/orders/', orderData)
  },

  // 获取订单详情
  getOrderDetail: (id) => {
    return apiClient.get(`/orders/${id}/`)
  },

  // 支付订单
  payOrder: (id) => {
    return apiClient.post(`/orders/${id}/pay/`)
  },

  // 取消订单
  cancelOrder: (id) => {
    return apiClient.post(`/orders/${id}/cancel/`)
  }
}

export default apiClient

