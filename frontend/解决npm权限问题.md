# 解决 npm 权限问题

## 问题
npm 无法在 `D:\nodejs\node_cache` 创建目录，提示 `EPERM` 权限错误。

## 解决方案

### 方案一：更改 npm 缓存目录（推荐）

在项目目录下创建本地缓存：

```powershell
# 在 frontend 目录下执行
npm config set cache ".\node_cache" --location=project
```

然后重新安装：

```powershell
npm install
```

### 方案二：使用管理员权限运行

1. 右键点击 PowerShell 或 CMD
2. 选择"以管理员身份运行"
3. 然后执行 `npm install`

### 方案三：更改全局缓存目录

```powershell
# 设置缓存目录到用户目录
npm config set cache "$env:USERPROFILE\.npm-cache"
```

### 方案四：清理缓存后重试

```powershell
# 清理缓存
npm cache clean --force

# 然后重新安装
npm install
```

## 快速解决脚本

创建一个 `install.ps1` 文件：

```powershell
# 设置本地缓存
npm config set cache ".\node_cache" --location=project

# 安装依赖
npm install
```

然后运行：
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```



