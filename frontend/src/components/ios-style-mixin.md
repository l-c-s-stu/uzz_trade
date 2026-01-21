# iOS 风格样式使用指南

## CSS 变量

所有组件都可以使用以下 iOS 风格的 CSS 变量：

### 颜色
```css
--ios-blue: #007AFF
--ios-green: #34C759
--ios-red: #FF3B30
--ios-bg-primary: #F2F2F7
--ios-bg-secondary: #FFFFFF
--ios-text-primary: #000000
--ios-text-secondary: #3C3C43
```

### 圆角
```css
--ios-radius-sm: 8px
--ios-radius-md: 12px
--ios-radius-lg: 16px
--ios-radius-xl: 20px
```

### 间距
```css
--ios-spacing-sm: 8px
--ios-spacing-md: 16px
--ios-spacing-lg: 24px
```

### 动画
```css
--ios-transition-fast: 0.15s cubic-bezier(0.4, 0.0, 0.2, 1)
--ios-transition-normal: 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)
```

## 使用示例

### 按钮
```vue
<button class="ios-btn ios-btn-primary">主要按钮</button>
<button class="ios-btn ios-btn-success">成功按钮</button>
<button class="ios-btn ios-btn-danger">危险按钮</button>
```

### 输入框
```vue
<input type="text" class="ios-input" placeholder="请输入">
<textarea class="ios-textarea" placeholder="请输入"></textarea>
```

### 卡片
```vue
<div class="ios-card">
  <!-- 内容 -->
</div>
```

### 导航栏
```vue
<nav class="ios-navbar">
  <!-- 导航内容 -->
</nav>
```

## 组件更新建议

1. 将所有 `--primary-color` 替换为 `--ios-blue`
2. 将所有 `--bg-card` 替换为 `--ios-bg-secondary`
3. 将所有 `--bg-body` 替换为 `--ios-bg-primary`
4. 使用 `--ios-radius-md` 替代自定义圆角
5. 使用 `--ios-transition-normal` 替代自定义过渡
6. 添加毛玻璃效果到导航栏
7. 优化按钮的 active 状态（使用 opacity 和 scale）
8. 使用 iOS 风格的阴影



