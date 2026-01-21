<template>
  <router-view />
</template>

<script setup>
// 根组件，只负责路由视图
</script>

<style>
@import './assets/ios-styles.css';
@import './components/shared-styles.css';

/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--ios-font-family);
  font-size: var(--ios-font-size-body);
  line-height: 1.47059;
  color: var(--ios-text-primary);
  background-color: var(--ios-bg-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-tap-highlight-color: transparent;
}

#app {
  min-height: 100vh;
}

/* 全局链接样式 */
a {
  color: var(--ios-blue);
  text-decoration: none;
  transition: opacity var(--ios-transition-fast);
}

a:active {
  opacity: 0.6;
}

/* 全局按钮基础样式 */
button {
  font-family: var(--ios-font-family);
  -webkit-tap-highlight-color: transparent;
}

/* 全局输入框基础样式 */
input,
textarea,
select {
  font-family: var(--ios-font-family);
}

/* 全局滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: var(--ios-radius-full);
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.3);
}
</style>

