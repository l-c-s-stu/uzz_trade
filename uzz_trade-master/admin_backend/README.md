# 管理后台 API 文档

## 概述

管理后台 API 提供了对用户和商品的管理功能，只有管理员（`is_staff=True` 或 `is_superuser=True`）才能访问。

## 认证

所有 API 都需要 JWT Token 认证，请在请求头中添加：
```
Authorization: Bearer <access_token>
```

## API 端点

### 1. 获取统计数据
**GET** `/api/admin/stats/`

返回系统统计数据：
```json
{
  "total_users": 100,
  "total_goods": 50,
  "total_orders": 200,
  "total_wishes": 150
}
```

### 2. 用户管理

#### 2.1 获取用户列表
**GET** `/api/admin/users/`

查询参数：
- `search`: 搜索关键词（用户名、邮箱、学号、学院、手机号）

响应示例：
```json
[
  {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com",
    "phone": "13800138000",
    "student_id": "202212190213",
    "college": "信科院",
    "is_active": true,
    "is_staff": false,
    "is_superuser": false,
    "date_joined": "2026-01-19T00:00:00Z"
  }
]
```

#### 2.2 更新用户状态
**PATCH** `/api/admin/users/{id}/`

请求体：
```json
{
  "is_active": false
}
```

响应示例：
```json
{
  "message": "用户状态已更新",
  "data": {
    "id": 1,
    "username": "user1",
    "is_active": false,
    ...
  }
}
```

### 3. 商品管理

#### 3.1 获取商品列表
**GET** `/api/admin/goods/`

查询参数：
- `search`: 搜索关键词（商品标题、描述）
- `status`: 商品状态（1=在售, 2=已出, 3=下架）

响应示例：
```json
[
  {
    "id": 1,
    "title": "商品标题",
    "description": "商品描述",
    "price": "99.00",
    "image": "/media/goods_image/image.jpg",
    "status": 1,
    "status_display": "在售",
    "owner": 1,
    "owner_name": "user1",
    "category": 1,
    "category_name": "数码",
    "created_at": "2026-01-19T00:00:00Z"
  }
]
```

#### 3.2 更新商品状态
**PATCH** `/api/admin/goods/{id}/`

请求体：
```json
{
  "status": 2
}
```

响应示例：
```json
{
  "message": "商品状态已更新",
  "data": {
    "id": 1,
    "status": 2,
    "status_display": "已出",
    ...
  }
}
```

#### 3.3 删除商品
**DELETE** `/api/admin/goods/{id}/delete/`

响应示例：
```json
{
  "message": "商品已删除"
}
```

## 权限说明

- 所有 API 都需要管理员权限（`is_staff=True` 或 `is_superuser=True`）
- 非管理员用户访问将返回 403 Forbidden

## 错误响应

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```



