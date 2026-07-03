<template>
  <div id="app">
    <transition name="page-fade" mode="out-in">
      <Login v-if="!loggedIn" @logged-in="loggedIn = true" />
      <Shop v-else @logout="loggedIn = false" />
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Login from './components/Login.vue'
import Shop from './components/Shop.vue'

const loggedIn = ref(!!localStorage.getItem('token'))
</script>

<style>
/* Design Tokens */
:root {
  /* Colors - Modern Purple-Blue Gradient System */
  --color-primary: #7C5CBF;
  --color-primary-light: #9B7FD4;
  --color-primary-dark: #5A3D9A;
  --color-accent: #5B8AF0;
  --color-accent-light: #7DA4F5;
  --color-gradient: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  --color-gradient-hover: linear-gradient(135deg, var(--color-primary-light), var(--color-accent-light));

  /* Background System */
  --bg-base: #08080F;
  --bg-surface: rgba(255, 255, 255, 0.025);
  --bg-surface-hover: rgba(255, 255, 255, 0.04);
  --bg-elevated: rgba(255, 255, 255, 0.06);

  /* Text System */
  --text-primary: #ffffff;
  --text-secondary: rgba(255, 255, 255, 0.65);
  --text-tertiary: rgba(255, 255, 255, 0.4);
  --text-muted: rgba(255, 255, 255, 0.2);

  /* Border System */
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.1);
  --border-hover: rgba(255, 255, 255, 0.15);
  --border-focus: rgba(124, 92, 191, 0.5);

  /* Semantic Colors */
  --color-success: #4ade80;
  --color-success-bg: rgba(74, 222, 128, 0.1);
  --color-error: #f87171;
  --color-error-bg: rgba(248, 113, 113, 0.1);
  --color-warning: #fbbf24;
  --color-warning-bg: rgba(251, 191, 36, 0.1);
  --color-price: #f0a050;

  /* Spacing Scale */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 16px;
  --space-xl: 20px;
  --space-2xl: 24px;
  --space-3xl: 32px;
  --space-4xl: 40px;
  --space-5xl: 48px;

  /* Border Radius */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 14px;
  --radius-xl: 16px;
  --radius-2xl: 20px;
  --radius-full: 99px;

  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.25);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.3);
  --shadow-xl: 0 16px 40px rgba(0, 0, 0, 0.35);
  --shadow-glow: 0 4px 16px rgba(124, 92, 191, 0.25);
  --shadow-glow-lg: 0 8px 32px rgba(124, 92, 191, 0.35);

  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-base: 0.25s ease;
  --transition-slow: 0.35s ease;
  --transition-bounce: 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

  /* Typography */
  --font-sans: 'PingFang SC', 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', monospace;
}

/* Reset & Base */
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

body {
  font-family: var(--font-sans);
  background: var(--bg-base);
  color: var(--text-primary);
  line-height: 1.5;
  overflow-x: hidden;
}

#app {
  min-height: 100vh;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.18);
}

/* Selection */
::selection {
  background: rgba(124, 92, 191, 0.35);
  color: #fff;
}

/* Focus Outline */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Page Transition */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: scale(0.98);
}

.page-fade-leave-to {
  opacity: 0;
  transform: scale(1.02);
}

/* Utility Classes */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>
