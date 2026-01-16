# Register.vue 组件说明

## 📋 组件功能

这是一个基于 Vue3 的用户注册组件，将原来的 `register.html` 和 `register.js` 重构为现代化的 Vue 组件。

## ✨ 特性

1. **Vue3 Composition API**: 使用 `<script setup>` 语法
2. **Axios 请求**: 使用 axios 替代原来的 fetch
3. **现代化样式**: 基于样式预览 HTML 的设计系统
4. **表单验证**: 
   - 密码一致性验证
   - 学号格式验证（仅数字）
   - 实时错误提示
5. **用户体验**:
   - 加载状态显示
   - 错误消息提示
   - 成功消息提示
   - 自动跳转到登录页

## 📦 依赖

确保项目中已安装：
- `vue` (^3.0.0)
- `vue-router` (^4.0.0)
- `axios`

```bash
npm install vue vue-router axios
```

## 🔧 配置

### API 基础 URL

组件使用环境变量 `VITE_API_BASE_URL`，如果没有设置则默认使用：
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api'
```

在 `.env` 文件中配置：
```
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## 📝 表单字段

根据后端改造，注册表单包含以下字段：

1. **username** - 用户名（必填）
2. **email** - 邮箱（必填）
3. **phone** - 手机号（必填）
4. **student_id** - 学号（必填，仅数字）
5. **college** - 学院（必填）
6. **password** - 密码（必填）
7. **confirmPassword** - 确认密码（必填）

## 🎨 样式说明

组件使用了样式预览 HTML 中的设计系统：
- CSS 变量定义（颜色、阴影、圆角等）
- 响应式设计
- 现代化 UI 组件样式

## 🚀 使用方法

### 在路由中使用

```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Register from '@/components/Register.vue'

const routes = [
  {
    path: '/register',
    name: 'Register',
    component: Register
  }
]
```

### 直接使用

```vue
<template>
  <Register />
</template>

<script setup>
import Register from '@/components/Register.vue'
</script>
```

## 🔄 与原版本的对比

### 原版本 (register.html + register.js)
- 使用原生 HTML + JavaScript
- 使用 fetch API
- 简单的 alert 提示
- 基础样式

### 新版本 (Register.vue)
- ✅ Vue3 Composition API
- ✅ Axios 请求库
- ✅ 优雅的错误提示 UI
- ✅ 现代化设计系统
- ✅ 响应式布局
- ✅ 表单验证增强
- ✅ 加载状态管理
- ✅ 路由集成

## 📡 API 接口

### 注册接口
```
POST /api/users/register/
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "phone": "string",
  "student_id": "string",
  "college": "string",
  "password": "string"
}
```

### 响应
- **201 Created**: 注册成功
- **400 Bad Request**: 验证错误（返回字段错误信息）

## ⚠️ 注意事项

1. **学号验证**: 学号只能包含数字，前端和后端都会验证
2. **密码验证**: 两次输入的密码必须一致
3. **错误处理**: 组件会显示服务器返回的详细错误信息
4. **路由跳转**: 注册成功后会延迟 1.5 秒跳转到登录页

## 🎯 下一步

可以继续创建：
- `Login.vue` - 登录组件
- `GoodsList.vue` - 商品列表组件
- `GoodsDetail.vue` - 商品详情组件
- 等等...

