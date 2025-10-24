
# 🧾 二手交易平台 API 接口文档

## 基础信息

| 项目 | 内容 |
|------|------|
| 后端框架 | Django + Django REST Framework |
| 数据格式 | JSON |
| 接口前缀 | `http://127.0.0.1:8000/api/` |
| 认证方式 | JWT Token（Bearer Token） |

---

## 1️⃣ 用户模块

### 1.1 用户注册
**URL:** `/api/users/register/`  
**方法:** `POST`  
**说明:** 用户注册账号。

#### 请求参数
| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| username | string | ✅ | 用户名 |
| password | string | ✅ | 密码 |
| email | string | ❌ | 邮箱 |

#### 请求示例
```json
{
  "username": "test",
  "email": "test@example.com",
  "password": "mypassword123"
}
```

#### 响应示例
```json
{
    "username": "test",
    "email": "test@example.com"
}
```

---

### 1.2 用户登录
**URL:** `/api/users/login/`  
**方法:** `POST`  
**说明:** 用户登录并返回 JWT Token。

#### 请求参数
| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| username | string | ✅ | 用户名 |
| password | string | ✅ | 密码 |

#### 请求示例
```json
{
  "username": "test",
  "password": "mypassword123"
}
```

#### 响应示例
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 1.3 刷新Token
**URL:** `/api/users/token/refresh/`  
**方法:** `POST`  
**说明:** 使用refresh token获取新的access token。

#### 请求参数
| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| refresh | string | ✅ | refresh token |

#### 请求示例
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 响应示例
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 2️⃣ 商品模块（Goods）

### 2.1 上架商品
**URL:** `/api/goods/`  
**方法:** `POST`  
**说明:** 用户上传新商品。  
**认证:** 需要登录

#### 请求参数（multipart/form-data）
| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| title | string | ✅ | 商品标题 |
| description | string | ✅ | 商品描述 |
| price | decimal | ✅ | 商品价格 |
| image | file | ❌ | 商品图片 |

#### 请求头
```
Authorization: Bearer <access_token>
```

#### 响应示例
```json
{
    "id": 5,
    "title": "二手iPhone",
    "description": "几乎全新，功能正常",
    "price": "2500.00",
    "image": "http://127.0.0.1:8000/media/goods_image/iphone.jpg",
    "created_at": "2025-10-22T11:56:39.443014Z",
    "wish_count": 0,
    "owner": 4,
    "owner_name": "test",
    "is_owner": true
}
```

---

### 2.2 查看所有商品
**URL:** `/api/goods/`  
**方法:** `GET`  
**说明:** 获取全部上架商品列表。

#### 响应示例
```json
[
    {
        "id": 5,
        "title": "二手iPhone",
        "description": "几乎全新，功能正常",
        "price": "2500.00",
        "image": "http://127.0.0.1:8000/media/goods_image/iphone.jpg",
        "created_at": "2025-10-22T11:56:39.443014Z",
        "wish_count": 0,
        "owner": 4,
        "owner_name": "test",
        "is_owner": false
    },
    {
        "id": 4,
        "title": "二手耳机",
        "description": "音质很好",
        "price": "120.00",
        "image": "http://127.0.0.1:8000/media/goods_image/headphone.jpg",
        "created_at": "2025-10-21T06:51:59.561879Z",
        "wish_count": 2,
        "owner": 3,
        "owner_name": "alice",
        "is_owner": true
    }
]
```

---

### 2.3 查看单个商品
**URL:** `/api/goods/<id>`  
**方法:** `GET`  
**说明:** 根据商品ID查看详细信息。

#### 示例
```
GET http://127.0.0.1:8000/api/goods/1
```

#### 响应示例
```json
{
    "id": 1,
    "title": "二手耳机",
    "description": "几乎全新，音质很好",
    "price": "120.00",
    "image": "http://127.0.0.1:8000/media/goods_image/1000030451.jpg",
    "created_at": "2025-10-20T11:30:09.509016Z",
    "wish_count": 2,
    "owner": 1,
    "owner_name": "alice",
    "is_owner": false
}
```

---

### 2.4 修改商品
**URL:** `/api/goods/<id>/update/`  
**方法:** `PUT`  
**说明:** 修改指定商品信息。  
**认证:** 需要登录  
**权限:** 只有商品所有者或管理员可以修改

#### 请求参数（multipart/form-data）
| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| title | string | ❌ | 商品标题 |
| description | string | ❌ | 商品描述 |
| price | decimal | ❌ | 商品价格 |
| image | file | ❌ | 商品图片 |

#### 请求头
```
Authorization: Bearer <access_token>
```

#### 请求示例
```json
{
    "title": "更新后的商品标题",
    "price": "150.00"
}
```

#### 响应示例
```json
{
    "message": "商品修改成功",
    "data": {
        "id": 1,
        "title": "更新后的商品标题",
        "description": "几乎全新，音质很好",
        "price": "150.00",
        "image": "http://127.0.0.1:8000/media/goods_image/1000030451.jpg",
        "created_at": "2025-10-20T11:30:09.509016Z",
        "wish_count": 2,
        "owner": 1,
        "owner_name": "alice",
        "is_owner": true
    }
}
```

---

### 2.5 删除商品
**URL:** `/api/goods/<id>/delete/`  
**方法:** `DELETE`  
**说明:** 删除指定商品。  
**认证:** 需要登录  
**权限:** 只有商品所有者或管理员可以删除

#### 请求头
```
Authorization: Bearer <access_token>
```

#### 响应示例
```json
{
    "message": "商品删除成功"
}
```

---

## 3️⃣ 评论模块（Comments）

### 3.1 对商品发表评论
**URL:** `/api/comments/goods/<goods_id>/comments/`  
**方法:** `POST`  
**说明:** 给指定商品添加评论。  
**认证:** 需要登录

#### 请求参数
| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| content | string | ✅ | 评论内容 |

#### 请求头
```
Authorization: Bearer <access_token>
```

#### 请求示例
```json
{
    "content": "这个商品看起来不错，我想买"
}
```

#### 响应示例
```json
{
    "id": 6,
    "user": 4,
    "user_name": "test",
    "goods": 1,
    "content": "这个商品看起来不错，我想买",
    "created_at": "2025-10-22T11:59:10.560431Z"
}
```

---

### 3.2 查看商品评论
**URL:** `/api/comments/goods/<goods_id>/comments/`  
**方法:** `GET`  
**说明:** 查看某个商品下的所有评论。

#### 响应示例
```json
[
    {
        "id": 6,
        "user": 4,
        "user_name": "test",
        "goods": 1,
        "content": "这个商品看起来不错，我想买",
        "created_at": "2025-10-22T11:59:10.560431Z"
    },
    {
        "id": 5,
        "user": 3,
        "user_name": "zefeng",
        "goods": 1,
        "content": "我是泽风我想买这个",
        "created_at": "2025-10-21T08:47:06.318090Z"
    }
]
```

---

## 4️⃣ 想买模块（Wishes）

### 4.1 添加/取消想买
**URL:** `/api/wishes/goods/<goods_id>/wish/`  
**方法:** `POST` / `DELETE`  
**说明:** 添加或取消对商品的想买。  
**认证:** 需要登录

#### 请求头
```
Authorization: Bearer <access_token>
```

#### POST 请求（添加想买）
**响应示例**
```json
{
    "message": "已添加到想买列表"
}
```

#### DELETE 请求（取消想买）
**响应示例**
```json
{
    "message": "已取消想买"
}
```

---

## 5️⃣ 认证说明

### 5.1 Token 使用方式
在需要认证的接口中，需要在请求头中添加：
```
Authorization: Bearer <access_token>
```

### 5.2 Token 刷新机制
- `access` token 有效期较短（通常1小时）
- `refresh` token 有效期较长（通常7天）
- 当 access token 过期时，使用 refresh token 获取新的 access token

### 5.3 权限说明
- **商品所有者**: 可以修改、删除自己发布的商品
- **管理员**: 可以修改、删除任何商品
- **普通用户**: 只能查看商品，发表评论，添加想买

---

## 6️⃣ 错误码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证或Token无效 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 7️⃣ 响应字段说明

### 商品字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | int | 商品ID |
| title | string | 商品标题 |
| description | string | 商品描述 |
| price | decimal | 商品价格 |
| image | string | 商品图片URL |
| created_at | datetime | 创建时间 |
| wish_count | int | 想买人数 |
| owner | int | 发布者ID |
| owner_name | string | 发布者用户名 |
| is_owner | boolean | 当前用户是否为商品所有者 |

### 评论字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | int | 评论ID |
| user | int | 评论者ID |
| user_name | string | 评论者用户名 |
| goods | int | 商品ID |
| content | string | 评论内容 |
| created_at | datetime | 评论时间 |

---

## ✅ 使用建议

1. **开发环境**: 使用 `http://127.0.0.1:8000` 作为基础URL
2. **生产环境**: 替换为实际的域名
3. **图片上传**: 使用 `multipart/form-data` 格式
4. **Token管理**: 建议在前端实现自动刷新机制
5. **错误处理**: 根据HTTP状态码进行相应的错误处理
