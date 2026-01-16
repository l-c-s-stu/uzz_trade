# 快速检查命令

## 🚀 一键检查脚本

### Windows PowerShell

```powershell
# 检查组件文件是否存在
Write-Host "检查组件文件..." -ForegroundColor Green
$components = @(
    "src\components\Register.vue",
    "src\components\Login.vue",
    "src\components\GoodsList.vue",
    "src\utils\api.js"
)

foreach ($file in $components) {
    if (Test-Path $file) {
        Write-Host "✓ $file 存在" -ForegroundColor Green
    } else {
        Write-Host "✗ $file 不存在" -ForegroundColor Red
    }
}

# 检查关键导入
Write-Host "`n检查关键导入..." -ForegroundColor Green
$register = Get-Content "src\components\Register.vue" -Raw
if ($register -match "authAPI") {
    Write-Host "✓ Register.vue 使用 authAPI" -ForegroundColor Green
} else {
    Write-Host "✗ Register.vue 未使用 authAPI" -ForegroundColor Red
}

$login = Get-Content "src\components\Login.vue" -Raw
if ($login -match "authAPI") {
    Write-Host "✓ Login.vue 使用 authAPI" -ForegroundColor Green
} else {
    Write-Host "✗ Login.vue 未使用 authAPI" -ForegroundColor Red
}

$goodsList = Get-Content "src\components\GoodsList.vue" -Raw
if ($goodsList -match "goodsAPI") {
    Write-Host "✓ GoodsList.vue 使用 goodsAPI" -ForegroundColor Green
} else {
    Write-Host "✗ GoodsList.vue 未使用 goodsAPI" -ForegroundColor Red
}

Write-Host "`n检查完成！" -ForegroundColor Cyan
```

### 保存为 check-components.ps1 并运行

```powershell
.\check-components.ps1
```

---

## 📋 手动检查清单

### 1. 文件存在性检查

```bash
# 在 frontend 目录下
ls src/components/Register.vue
ls src/components/Login.vue
ls src/components/GoodsList.vue
ls src/utils/api.js
```

### 2. 导入检查

打开每个组件文件，检查：

**Register.vue**:
```javascript
import { authAPI } from '@/utils/api'  // ✓ 正确
// import axios from 'axios'  // ✗ 错误（不应直接使用）
```

**Login.vue**:
```javascript
import { authAPI } from '@/utils/api'  // ✓ 正确
```

**GoodsList.vue**:
```javascript
import { goodsAPI, authAPI } from '@/utils/api'  // ✓ 正确
```

### 3. 功能检查

在浏览器中测试：

1. **Register.vue**
   - 访问 `/register`
   - 填写表单并提交
   - 检查是否跳转到 `/login`

2. **Login.vue**
   - 访问 `/login`
   - 输入用户名密码
   - 检查是否跳转到 `/`
   - 检查 localStorage 是否有 token

3. **GoodsList.vue**
   - 访问 `/`
   - 检查商品列表是否加载
   - 检查登录状态是否正确显示

---

## 🔍 代码审查重点

### Register.vue
- [ ] 使用 `authAPI.register()` 而不是直接 `axios.post()`
- [ ] 学号验证：`/^\d+$/`
- [ ] 密码一致性验证
- [ ] 错误消息显示
- [ ] 成功跳转到 `/login`

### Login.vue
- [ ] 使用 `authAPI.login()`
- [ ] 存储 `access`、`refresh`、`username` 到 localStorage
- [ ] 登录成功后跳转到 `/`
- [ ] 错误处理

### GoodsList.vue
- [ ] 使用 `goodsAPI.getGoods()`
- [ ] 使用 `authAPI.isLoggedIn()` 检查登录状态
- [ ] 商品卡片点击跳转
- [ ] 所有者操作按钮（编辑/删除）
- [ ] 退出登录功能

---

## ⚡ 最快检查方法

1. **打开 VSCode**
2. **打开组件文件**
3. **查看是否有红色波浪线（错误）或黄色波浪线（警告）**
4. **检查 Problems 面板（Ctrl+Shift+M）**

如果没有错误提示，说明代码基本没问题！

