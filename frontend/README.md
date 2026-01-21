# 校园二手交易平台 - 前端

Vue3 + Vite + Vue Router + Axios

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 3. 构建生产版本

```bash
npm run build
```

## 项目结构

```
frontend/
├── src/
│   ├── components/      # Vue 组件
│   │   ├── Register.vue
│   │   ├── Login.vue
│   │   └── GoodsList.vue
│   ├── utils/          # 工具函数
│   │   └── api.js      # API 请求封装
│   ├── router/         # 路由配置
│   │   └── index.js
│   ├── App.vue         # 根组件
│   └── main.js         # 入口文件
├── index.html
├── vite.config.js      # Vite 配置
└── package.json
```

## 环境变量

创建 `.env` 文件（可选）：

```
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## 开发说明

- 使用 Vue3 Composition API (`<script setup>`)
- 使用 Vue Router 进行路由管理
- 使用 Axios 进行 HTTP 请求
- API 请求统一封装在 `src/utils/api.js`

## 检查组件

运行检查脚本：

```powershell
powershell -ExecutionPolicy Bypass -File check-components.ps1
```



