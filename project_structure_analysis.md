# 📁 二手交易平台项目结构分析

## 🎯 整体架构

```
uzz-trade/
├── uzz_trade-master/          # 后端Django项目
│   ├── campus_trade/          # 项目主配置
│   ├── users/                 # 用户模块
│   ├── goods/                 # 商品模块
│   ├── comments/              # 评论模块
│   ├── wishes/                # 心愿单模块
│   ├── trade/                 # 交易模块
│   └── media/                 # 上传文件存储
└── uzz_trade_qian/            # 前端静态文件
    ├── *.html                 # 页面文件
    ├── js/                    # JavaScript文件
    └── css/                   # 样式文件(内嵌在HTML中)
```

## 🔧 后端模块详解

### 1. campus_trade/ - 项目核心配置
```
campus_trade/
├── settings.py        # 项目设置(数据库、应用、中间件等)
├── urls.py           # 主路由配置
├── wsgi.py           # 服务器接口
└── asgi.py           # 异步服务器接口
```

**作用**: 就像公司的总部，管理整个项目的配置和路由。

### 2. users/ - 用户管理模块
```
users/
├── models.py         # 用户数据模型
├── views.py          # 用户相关API视图
├── serializers.py    # 数据序列化器
├── urls.py          # 用户模块路由
└── admin.py         # 管理后台配置
```

**功能**:
- 用户注册/登录
- 用户信息管理
- JWT Token认证

### 3. goods/ - 商品管理模块
```
goods/
├── models.py         # 商品数据模型
├── views.py          # 商品相关API视图
├── serializers.py    # 数据序列化器
├── urls.py          # 商品模块路由
└── admin.py         # 管理后台配置
```

**功能**:
- 商品发布/编辑/删除
- 商品列表/详情查看
- 商品图片上传

### 4. comments/ - 评论模块
```
comments/
├── models.py         # 评论数据模型
├── views.py          # 评论相关API视图
├── serializers.py    # 数据序列化器
└── urls.py          # 评论模块路由
```

**功能**:
- 商品评论发布
- 评论列表查看

### 5. wishes/ - 心愿单模块
```
wishes/
├── models.py         # 心愿单数据模型
├── views.py          # 心愿单相关API视图
├── serializers.py    # 数据序列化器
└── urls.py          # 心愿单模块路由
```

**功能**:
- 添加/移除心愿单
- 心愿单统计

## 🎨 前端文件详解

### 1. 页面文件
```
uzz_trade_qian/
├── login.html        # 登录页面
├── register.html     # 注册页面
├── goods.html        # 商品列表页面
├── goods_detail.html # 商品详情页面
└── create_goods.html # 发布商品页面
```

### 2. JavaScript模块
```
js/
├── api.js           # API通信封装
├── login.js         # 登录功能
├── register.js      # 注册功能
├── goods.js         # 商品列表功能
├── goods_detail.js  # 商品详情功能
└── create_goods.js  # 发布商品功能
```

## 🔄 数据流向

### 1. 用户注册流程
```
register.html → register.js → api.js → Django API → 数据库
```

### 2. 商品发布流程
```
create_goods.html → create_goods.js → api.js → Django API → 数据库
```

### 3. 商品查看流程
```
goods.html → goods.js → api.js → Django API → 数据库 → 前端显示
```

## 🛠️ 开发工具和技术栈

### 后端技术
- **Django 5.2.7**: Web框架
- **Django REST Framework**: API框架
- **SQLite**: 数据库
- **JWT**: 用户认证
- **Pillow**: 图片处理

### 前端技术
- **HTML5**: 页面结构
- **CSS3**: 样式设计
- **JavaScript ES6+**: 交互逻辑
- **Fetch API**: HTTP请求

### 开发环境
- **Python 3.x**: 后端语言
- **Django开发服务器**: 本地开发
- **浏览器**: 前端运行环境

## 🚀 部署架构

### 开发环境
```
浏览器 → Django开发服务器(127.0.0.1:8000) → SQLite数据库
```

### 生产环境(建议)
```
Nginx → Gunicorn → Django → PostgreSQL
```

## 📊 数据库关系

```
User (用户表)
├── id (主键)
├── username (用户名)
├── email (邮箱)
└── password (密码)

Goods (商品表)
├── id (主键)
├── owner_id (外键 → User.id)
├── title (标题)
├── description (描述)
├── price (价格)
├── image (图片)
└── created_at (创建时间)

Comment (评论表)
├── id (主键)
├── user_id (外键 → User.id)
├── goods_id (外键 → Goods.id)
├── content (内容)
└── created_at (创建时间)

Wish (心愿单表)
├── id (主键)
├── user_id (外键 → User.id)
└── goods_id (外键 → Goods.id)
```

## 🎯 学习建议

### 初学者学习路径
1. **HTML/CSS基础** → 理解页面结构
2. **JavaScript基础** → 理解交互逻辑
3. **Python基础** → 理解后端语言
4. **Django基础** → 理解Web框架
5. **数据库基础** → 理解数据存储
6. **API概念** → 理解前后端通信

### 实践建议
1. 先运行项目，理解整体功能
2. 修改前端样式，理解CSS作用
3. 添加简单功能，理解JavaScript
4. 修改后端逻辑，理解Django
5. 添加新功能，理解全栈开发

