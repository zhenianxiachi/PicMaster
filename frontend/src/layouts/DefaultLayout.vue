<template>
  <div class="default-layout">
    <el-container>
      <el-header class="app-header">
        <div class="header-content">
          <h1 class="app-title">
            <el-icon><Picture class="title-icon" /></el-icon>
            <router-link to="/" class="app-title-link">PicMaster</router-link>
          </h1>
          <div class="header-nav">
            <router-link v-for="item in menuItems" :key="item.id" :to="item.path" class="nav-item">
              {{ item.name }}
            </router-link>
          </div>
          <div class="header-actions">
            <div v-if="authStore.isLoggedIn" class="user-info">
              <span>{{ authStore.user?.username }}</span>
              <el-button size="small" @click="authStore.logout">退出</el-button>
            </div>
            <el-button v-else link @click="handleLogin">登录</el-button>

            <!-- <el-button type="primary" size="large" @click="toggleQuickMode" class="quick-mode-btn">
              <el-icon><SwitchButton /></el-icon>
              {{ quickMode ? '退出快编' : '快编模式' }}
            </el-button> -->
          </div>
        </div>
      </el-header>

      <el-container>
        <el-main class="app-main">
          <slot />
        </el-main>
        <el-footer class="app-footer">
          <div class="footer-content">
            <p class="footer-text">&copy; 2025 PicMaster. All rights reserved.</p>
            <div class="footer-links">
              <a href="#" class="footer-link">隐私政策</a>
              <a href="#" class="footer-link">使用条款</a>
              <a href="#" class="footer-link">联系我们</a>
            </div>
          </div>
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Picture, SwitchButton } from '@element-plus/icons-vue'
import { useAuthStore } from '../store/auth'

/**
 * 菜单项接口
 */
interface MenuItem {
  id: string
  name: string
  path: string
}

const authStore = useAuthStore()
const quickMode = ref<boolean>(false)

const menuItems: MenuItem[] = [
  { id: '0', name: '首页', path: '/' },
  { id: '1', name: '图片编辑', path: '/editor-intro' },
  { id: '2', name: '作品集管理', path: '/portfolio' },
  { id: '3', name: '作品集展示', path: '/viewer' },
]

const toggleQuickMode = (): void => {
  quickMode.value = !quickMode.value
}

const handleLogin = async (): Promise<void> => {
  // 模拟登录
  const success = await authStore.login({
    username: 'testuser',
    password: 'password',
  })

  if (success) {
    console.log('登录成功')
  } else {
    console.log('登录失败')
  }
}
</script>

<style scoped>
.default-layout {
  min-height: 100vh;
  background-color: #fbfbfd;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', Roboto, sans-serif;
}

.app-header {
  background-color: rgba(251, 251, 253, 0.8);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  height: 72px;
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #1d1d1f;
}

.app-title {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
  display: flex;
  align-items: center;
  gap: 8px;
  letter-spacing: -0.02em;
}

.title-icon {
  font-size: 24px;
  color: #0071e3;
}

.header-nav {
  display: flex;
  gap: 32px;
}

.nav-item {
  font-size: 14px;
  font-weight: 400;
  color: #86868b;
  text-decoration: none;
  padding: 8px 0;
  transition: color 0.3s ease;
}

.nav-item:hover,
.nav-item.router-link-active {
  color: #1d1d1f;
}

.quick-mode-btn {
  background-color: #0071e3;
  border: none;
  border-radius: 980px;
  padding: 8px 20px;
  font-size: 14px;
  font-weight: 400;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.quick-mode-btn:hover {
  background-color: #0077ed;
  transform: scale(1.02);
}

.app-main {
  padding: 0;
  /* max-width: 1200px; */
  margin: 0 auto;
  width: 100%;
  min-height: calc(100vh - 72px);
}

.app-footer {
  background-color: #ffffff;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  padding: 20px 0;
  height: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-text {
  font-size: 14px;
  color: #86868b;
  margin: 0;
}

.footer-links {
  display: flex;
  gap: 24px;
}

.footer-link {
  font-size: 14px;
  color: #86868b;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-link:hover {
  color: #0071e3;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }

  .footer-links {
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
  }

  .header-nav {
    display: none;
  }
}
</style>
