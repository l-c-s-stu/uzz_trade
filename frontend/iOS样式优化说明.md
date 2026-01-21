# iOS 风格样式优化说明

## ✅ 已完成的优化

### 1. 创建了全局 iOS 样式文件
- `src/assets/ios-styles.css` - 包含完整的 iOS 设计系统

### 2. 更新了 App.vue
- 引入了 iOS 样式文件
- 更新了全局样式重置

### 3. 更新了 GoodsList.vue
- ✅ 导航栏：添加了毛玻璃效果（backdrop-filter）
- ✅ 按钮：使用 iOS 风格的按钮样式和交互
- ✅ 卡片：使用 iOS 风格的圆角和阴影
- ✅ 颜色：使用 iOS 系统颜色
- ✅ 字体：使用 iOS 系统字体
- ✅ 动画：使用 iOS 风格的过渡动画

## 🎨 iOS 设计特点

### 1. 毛玻璃效果
```css
background-color: rgba(255, 255, 255, 0.8);
backdrop-filter: blur(20px);
-webkit-backdrop-filter: blur(20px);
```

### 2. 圆角设计
- 小圆角：8px
- 中圆角：12px
- 大圆角：16px
- 超大圆角：20px

### 3. 柔和的阴影
- 使用多层阴影营造深度感
- 阴影颜色较淡，不会过于突兀

### 4. 流畅的动画
- 使用 `cubic-bezier(0.4, 0.0, 0.2, 1)` 缓动函数
- 按钮点击使用 `scale(0.97)` 和 `opacity` 变化

### 5. 系统颜色
- 蓝色：`#007AFF`（iOS 系统蓝）
- 绿色：`#34C759`（成功）
- 红色：`#FF3B30`（错误/危险）
- 背景：`#F2F2F7`（iOS 浅色背景）

## 📋 待更新的组件

需要更新以下组件的样式：

1. **Register.vue** - 注册页面
2. **Login.vue** - 登录页面
3. **GoodsDetail.vue** - 商品详情页
4. **CreateGoods.vue** - 发布商品页
5. **EditGoods.vue** - 编辑商品页

## 🔧 更新步骤

对于每个组件，需要：

1. **替换 CSS 变量**
   - `--primary-color` → `--ios-blue`
   - `--bg-body` → `--ios-bg-primary`
   - `--bg-card` → `--ios-bg-secondary`
   - `--text-main` → `--ios-text-primary`
   - `--text-secondary` → `--ios-text-secondary`

2. **更新导航栏**
   - 添加毛玻璃效果
   - 使用 `border-bottom: 0.5px solid var(--ios-separator)`

3. **更新按钮**
   - 使用 iOS 风格的按钮样式
   - 添加 `:active` 状态的 `scale` 和 `opacity` 效果

4. **更新卡片**
   - 使用 iOS 风格的圆角（`--ios-radius-lg`）
   - 使用 iOS 风格的阴影

5. **更新输入框**
   - 使用 iOS 风格的输入框样式
   - 添加焦点状态的蓝色边框和阴影

6. **更新动画**
   - 使用 `--ios-transition-fast` 或 `--ios-transition-normal`
   - 使用 iOS 风格的缓动函数

## 💡 使用建议

1. **保持一致性**：所有组件使用相同的 iOS 设计系统
2. **响应式设计**：确保在移动端和桌面端都有良好的体验
3. **可访问性**：确保颜色对比度符合 WCAG 标准
4. **性能优化**：使用 CSS 变量和硬件加速的动画

## 🌙 深色模式

iOS 样式文件已包含深色模式支持，会自动根据系统设置切换。

## 📱 移动端优化

- 更大的触摸目标（至少 44x44px）
- 使用 `-webkit-tap-highlight-color: transparent` 移除默认高亮
- 使用 `user-select: none` 防止意外选择文本



