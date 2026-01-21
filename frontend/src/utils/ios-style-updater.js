/**
 * iOS 样式更新工具
 * 用于批量更新组件样式
 */

export const iOSStyleMap = {
  // 颜色映射
  colors: {
    '--primary-color': '--ios-blue',
    '--primary-hover': '--ios-blue-dark',
    '--text-main': '--ios-text-primary',
    '--text-secondary': '--ios-text-secondary',
    '--text-tertiary': '--ios-text-tertiary',
    '--bg-body': '--ios-bg-primary',
    '--bg-card': '--ios-bg-secondary',
    '--bg-tertiary': '--ios-bg-tertiary',
    '--danger': '--ios-red',
    '--success': '--ios-green',
    '--warning': '--ios-orange',
  },
  
  // 圆角映射
  radius: {
    '--radius-sm': '--ios-radius-sm',
    '--radius-md': '--ios-radius-md',
    '--radius-lg': '--ios-radius-lg',
  },
  
  // 间距映射
  spacing: {
    'padding: 0.6rem': 'padding: 12px',
    'padding: 1rem': 'padding: var(--ios-spacing-md)',
    'margin-bottom: 20px': 'margin-bottom: var(--ios-spacing-md)',
    'margin-bottom: 30px': 'margin-bottom: var(--ios-spacing-lg)',
  },
  
  // 字体映射
  fonts: {
    'font-family: \'Inter\'': 'font-family: var(--ios-font-family)',
    'font-size: 0.95rem': 'font-size: var(--ios-font-size-body)',
    'font-size: 1rem': 'font-size: var(--ios-font-size-body)',
    'font-size: 1.5rem': 'font-size: var(--ios-font-size-headline)',
  },
  
  // 过渡映射
  transitions: {
    'transition: all 0.2s': 'transition: all var(--ios-transition-fast)',
    'transition: all 0.3s': 'transition: all var(--ios-transition-normal)',
    'transition: color 0.2s': 'transition: color var(--ios-transition-fast)',
  },
  
  // 阴影映射
  shadows: {
    'box-shadow: var(--shadow-sm)': 'box-shadow: var(--ios-shadow-sm)',
    'box-shadow: var(--shadow-md)': 'box-shadow: var(--ios-shadow-md)',
  }
}

/**
 * 更新导航栏样式
 */
export const updateNavbarStyle = (styleText) => {
  return styleText
    .replace(/background:\s*var\(--bg-card\)/g, 'background-color: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px)')
    .replace(/box-shadow:\s*var\(--shadow-sm\)/g, 'border-bottom: 0.5px solid var(--ios-separator); box-shadow: 0 0.5px 0 rgba(0, 0, 0, 0.1)')
}

/**
 * 更新按钮样式
 */
export const updateButtonStyle = (styleText) => {
  return styleText
    .replace(/\.btn\s*\{[^}]*\}/g, (match) => {
      if (match.includes('display: inline-flex')) return match
      return match.replace(/display:\s*inline-block/, 'display: inline-flex;\n  align-items: center;\n  justify-content: center')
        .replace(/transition:\s*all\s+0\.2s/g, 'transition: all var(--ios-transition-fast)')
        .replace(/transition:\s*all\s+0\.3s/g, 'transition: all var(--ios-transition-normal)')
    })
    .replace(/\.btn-primary:hover:not\(:disabled\)\s*\{[^}]*\}/g, (match) => {
      return match.replace(/transform:\s*translateY\(-1px\)/, 'opacity: 0.6;\n  transform: scale(0.97)')
    })
    .replace(/\.btn-primary\s*\{[^}]*\}/g, (match) => {
      if (match.includes('background-color: var(--ios-blue)')) return match
      return match.replace(/background-color:\s*var\(--primary-color\)/, 'background-color: var(--ios-blue)')
        .replace(/color:\s*white/, 'color: #FFFFFF')
    })
}

export default {
  iOSStyleMap,
  updateNavbarStyle,
  updateButtonStyle
}



