// API工具类
class ApiClient {
    constructor() {
        this.baseURL = 'http://127.0.0.1:8000/api';
    }

    // 获取认证头（仅包含鉴权，不默认附加 Content-Type）
    getAuthHeaders() {
        const token = localStorage.getItem('access');
        return {
            ...(token && { 'Authorization': `Bearer ${token}` })
        };
    }

    // 通用API请求方法
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        let config = {
            headers: { ...this.getAuthHeaders(), ...(options.headers || {}) },
            ...options
        };

        // 仅当发送字符串JSON体时，自动添加 JSON Content-Type；
        // 若为 FormData 或无 body，则不设置，避免不必要的预检
        if (typeof config.body === 'string' && !('Content-Type' in config.headers)) {
            config.headers['Content-Type'] = 'application/json';
        }

        try {
            let response = await fetch(url, config);
            
            // 如果token过期，尝试刷新
            if (response.status === 401 && localStorage.getItem('refresh')) {
                const refreshed = await this.refreshToken();
                if (refreshed) {
                    // 重新发送请求
                    config.headers = this.getAuthHeaders();
                    response = await fetch(url, config);
                }
            }

            return response;
        } catch (error) {
            console.error('API请求错误:', error);
            throw error;
        }
    }

    // 刷新token
    async refreshToken() {
        try {
            const refreshToken = localStorage.getItem('refresh');
            if (!refreshToken) return false;

            const response = await fetch(`${this.baseURL}/users/token/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access', data.access);
                return true;
            }
            return false;
        } catch (error) {
            console.error('刷新token失败:', error);
            return false;
        }
    }

    // 用户认证相关
    async login(username, password) {
        const response = await fetch(`${this.baseURL}/users/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        return response;
    }

    async register(userData) {
        const response = await fetch(`${this.baseURL}/users/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        return response;
    }

    // 商品相关
    async getGoods() {
        const response = await this.request('/goods/');
        return response;
    }

    async getGoodDetail(id) {
        const response = await this.request(`/goods/${id}`);
        return response;
    }

    async deleteGood(id) {
        console.log('调用deleteGood，goodsId:', id);
        const response = await this.request(`/goods/${id}/delete/`, {
            method: 'DELETE'
        });
        console.log('deleteGood响应:', response.status, response.statusText);
        return response;
    }

    async createGood(goodData) {
        const formData = new FormData();
        Object.keys(goodData).forEach(key => {
            if (goodData[key] !== null && goodData[key] !== undefined) {
                formData.append(key, goodData[key]);
            }
        });

        const response = await fetch(`${this.baseURL}/goods/`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access')}` },
            body: formData
        });
        return response;
    }

    async updateGood(id, goodData) {
        console.log('调用updateGood，goodsId:', id);
        const formData = new FormData();
        Object.keys(goodData).forEach(key => {
            if (goodData[key] !== null && goodData[key] !== undefined) {
                formData.append(key, goodData[key]);
            }
        });

        const response = await fetch(`${this.baseURL}/goods/${id}/update/`, {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access')}` },
            body: formData
        });
        console.log('updateGood响应:', response.status, response.statusText);
        return response;
    }

    // 评论相关
    async getComments(goodsId) {
        const response = await this.request(`/goods/${goodsId}/comments/`);
        return response;
    }

    async createComment(goodsId, content) {
        const response = await this.request(`/goods/${goodsId}/comments/`, {
            method: 'POST',
            body: JSON.stringify({ content })
        });
        return response;
    }

    // 心愿单相关
    async addToWish(goodsId) {
        console.log('调用addToWish，goodsId:', goodsId);
        const response = await this.request(`/goods/${goodsId}/wish/`, {
            method: 'POST'
        });
        console.log('addToWish响应:', response.status, response.statusText);
        return response;
    }

    async removeFromWish(goodsId) {
        const response = await this.request(`/goods/${goodsId}/wish/`, {
            method: 'DELETE'
        });
        return response;
    }

    // 检查用户是否已登录
    isLoggedIn() {
        return !!localStorage.getItem('access');
    }

    // 登出
    logout() {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        localStorage.removeItem('username');
        window.location.href = 'login.html';
    }
}

// 创建全局API客户端实例
const apiClient = new ApiClient();
