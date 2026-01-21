# 批量更新 iOS 样式指南

## ✅ 已完成

1. ✅ 创建了 `src/assets/ios-styles.css` - iOS 设计系统
2. ✅ 创建了 `src/components/shared-styles.css` - 共享样式类
3. ✅ 更新了 `App.vue` - 引入全局样式
4. ✅ 更新了 `GoodsList.vue` - 应用 iOS 风格

## 📋 需要更新的组件

### 高优先级（核心功能）
- [ ] Register.vue
- [ ] Login.vue
- [ ] GoodsDetail.vue
- [ ] CreateGoods.vue
- [ ] EditGoods.vue

## 🔧 更新步骤

### 步骤 1: 替换 CSS 变量

在每个组件的 `<style scoped>` 中，删除 `:root` 中的旧变量定义，直接使用全局 iOS 变量。

**删除这些：**
```css
:root {
  --primary-color: #4F46E5;
  --bg-body: #F3F4F6;
  --bg-card: #FFFFFF;
  /* ... */
}
```

**使用这些：**
```css
/* 直接使用全局 iOS 变量，无需重新定义 */
```

### 步骤 2: 更新导航栏

**旧样式：**
```css
.navbar {
  background: var(--bg-card);
  box-shadow: var(--shadow-sm);
}
```

**新样式：**
```css
.navbar {
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 0.5px solid var(--ios-separator);
  box-shadow: 0 0.5px 0 rgba(0, 0, 0, 0.1);
}
```

### 步骤 3: 更新按钮

**旧样式：**
```css
.btn-primary {
  background-color: var(--primary-color);
  color: white;
}
.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
}
```

**新样式：**
```css
.btn-primary {
  color: #FFFFFF;
  background-color: var(--ios-blue);
}
.btn-primary:active:not(:disabled) {
  background-color: var(--ios-blue-dark);
  opacity: 0.6;
  transform: scale(0.97);
}
```

### 步骤 4: 更新输入框

**旧样式：**
```css
.form-input {
  border: 1px solid #E5E7EB;
  border-radius: var(--radius-sm);
}
.form-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}
```

**新样式：**
```css
.form-input {
  border: 1px solid var(--ios-separator-opaque);
  border-radius: var(--ios-radius-md);
}
.form-input:focus {
  border-color: var(--ios-blue);
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
}
```

### 步骤 5: 更新卡片

**旧样式：**
```css
.card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}
```

**新样式：**
```css
.card {
  background-color: var(--ios-bg-secondary);
  border-radius: var(--ios-radius-lg);
  box-shadow: var(--ios-shadow-sm);
  border: 0.5px solid var(--ios-separator);
}
.card:active {
  transform: scale(0.98);
  opacity: 0.9;
}
.card:hover {
  box-shadow: var(--ios-shadow-md);
}
```

### 步骤 6: 更新颜色引用

全局替换：
- `var(--primary-color)` → `var(--ios-blue)`
- `var(--bg-body)` → `var(--ios-bg-primary)`
- `var(--bg-card)` → `var(--ios-bg-secondary)`
- `var(--text-main)` → `var(--ios-text-primary)`
- `var(--text-secondary)` → `var(--ios-text-secondary)`
- `var(--danger)` → `var(--ios-red)`
- `var(--success)` → `var(--ios-green)`

### 步骤 7: 更新字体和间距

- `font-family: 'Inter'` → `font-family: var(--ios-font-family)`
- `padding: 1rem` → `padding: var(--ios-spacing-md)`
- `margin-bottom: 20px` → `margin-bottom: var(--ios-spacing-md)`
- `border-radius: var(--radius-sm)` → `border-radius: var(--ios-radius-sm)`

### 步骤 8: 更新过渡动画

- `transition: all 0.2s` → `transition: all var(--ios-transition-fast)`
- `transition: all 0.3s` → `transition: all var(--ios-transition-normal)`

## 🎯 快速更新模板

### 导航栏模板
```css
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
```

### 按钮模板
```css
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

.btn:active:not(:disabled) {
  opacity: 0.6;
  transform: scale(0.97);
}
```

### 输入框模板
```css
.form-input {
  width: 100%;
  padding: 12px 16px;
  font-family: var(--ios-font-family);
  font-size: var(--ios-font-size-body);
  color: var(--ios-text-primary);
  background-color: var(--ios-bg-secondary);
  border: 1px solid var(--ios-separator-opaque);
  border-radius: var(--ios-radius-md);
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
```

## 📝 检查清单

更新每个组件时，检查：

- [ ] 删除了旧的 `:root` 变量定义
- [ ] 导航栏使用了毛玻璃效果
- [ ] 按钮使用了 iOS 风格的 `:active` 状态
- [ ] 输入框使用了 iOS 风格的焦点效果
- [ ] 卡片使用了 iOS 风格的圆角和阴影
- [ ] 所有颜色引用都使用了 iOS 变量
- [ ] 所有过渡都使用了 iOS 过渡变量
- [ ] 字体使用了 iOS 字体变量
- [ ] 间距使用了 iOS 间距变量

## 🚀 自动化更新（可选）

可以使用 VS Code 的查找替换功能：

1. 打开组件文件
2. 按 `Ctrl+H` 打开查找替换
3. 使用正则表达式模式
4. 逐个替换上述变量和样式

## 💡 提示

1. **保持一致性**：所有组件使用相同的 iOS 设计系统
2. **测试交互**：更新后测试按钮点击、输入框焦点等交互效果
3. **响应式**：确保移动端和桌面端都有良好的体验
4. **性能**：使用 CSS 变量和硬件加速的动画

## 📱 iOS 设计原则

1. **清晰度**：清晰的视觉层次和对比度
2. **深度**：使用阴影和层次营造深度感
3. **动效**：流畅自然的动画过渡
4. **一致性**：统一的设计语言和交互模式
5. **可访问性**：足够的触摸目标和颜色对比度



