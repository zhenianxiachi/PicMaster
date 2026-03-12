<template>
  <div class="default-layout">
    <div class="utility-bar">
      <div class="utility-inner">
        <span class="utility-pill">PicMaster Studio</span>
        <span class="utility-text">商业级图像编辑与交付工作流</span>
        <button class="utility-link" @click="usageStore.openUpgradeDialog('daily', 'export-image')">查看 Pro 方案</button>
      </div>
    </div>

    <el-header class="app-header">
      <div class="header-content">
        <router-link to="/" class="brand">
          <el-icon class="brand-icon"><Picture /></el-icon>
          <div class="brand-copy">
            <strong>PicMaster</strong>
            <span>Commercial Image Suite</span>
          </div>
        </router-link>

        <nav class="nav-links">
          <router-link v-for="item in menuItems" :key="item.id" :to="item.path" class="nav-link">
            {{ item.name }}
          </router-link>
        </nav>

        <div class="header-actions">
          <div class="quota-badge" :title="usageStore.usageSummary.detail">
            {{ usageStore.usageSummary.label }}
          </div>

          <template v-if="authStore.isLoggedIn">
            <el-tag class="plan-tag" effect="plain">{{ authStore.planLabel }}</el-tag>
            <span class="username">{{ authStore.user?.username }}</span>
            <el-button
              v-if="!authStore.isPro"
              type="warning"
              size="small"
              round
              @click="usageStore.openUpgradeDialog('daily', 'export-image')"
            >
              升级
            </el-button>
            <el-button text @click="authStore.logout">退出</el-button>
          </template>

          <template v-else>
            <el-button text @click="authStore.openAuthDialog('login')">登录</el-button>
            <el-button type="primary" round size="small" @click="authStore.openAuthDialog('register')">注册</el-button>
          </template>
        </div>
      </div>
    </el-header>

    <el-main class="app-main">
      <slot />
    </el-main>

    <el-footer class="app-footer">
      <div class="footer-content">
        <div class="footer-left">
          <p class="footer-brand">PicMaster · Built for modern studios</p>
          <p class="footer-copy">© 2026 PicMaster. All rights reserved.</p>
        </div>
        <div class="footer-links">
          <a href="/privacy-policy" class="footer-link" title="隐私政策">隐私政策</a>
          <a href="/terms-of-service" class="footer-link" title="服务条款">服务条款</a>
          <a href="/business-cooperation" class="footer-link" title="商务合作">商务合作</a>
        </div>
      </div>
    </el-footer>
  </div>
</template>

<script setup lang="ts">
import { Picture } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'
import { useUsageStore } from '@/store/usage'

interface MenuItem {
  id: string
  name: string
  path: string
}

const authStore = useAuthStore()
const usageStore = useUsageStore()

const menuItems: MenuItem[] = [
  { id: 'home', name: '首页', path: '/' },
  { id: 'editor', name: '编辑', path: '/editor-intro' },
  { id: 'portfolio', name: '作品集', path: '/portfolio' },
  { id: 'viewer', name: '展示', path: '/viewer' },
]
</script>

<style scoped>
.default-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.utility-bar {
  position: sticky;
  top: 0;
  z-index: 1400;
  background: linear-gradient(110deg, #0e2f4e, #1a486f 60%, #0f7ccf);
  border-bottom: 1px solid rgba(255, 255, 255, 0.16);
}

.utility-inner {
  max-width: 1320px;
  margin: 0 auto;
  height: 44px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #e9f5ff;
  font-size: 12px;
}

.utility-pill {
  border: 1px solid rgba(255, 255, 255, 0.32);
  background: rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  padding: 4px 10px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.utility-text {
  opacity: 0.92;
}

.utility-link {
  margin-left: auto;
  border: 0;
  background: transparent;
  color: #fff2ca;
  font-weight: 700;
  cursor: pointer;
}

.utility-link:hover {
  text-decoration: underline;
}

.app-header {
  position: sticky;
  top: 44px;
  z-index: 1300;
  height: 78px;
  border-bottom: 1px solid var(--pm-border);
  background: color-mix(in srgb, #ffffff 88%, #eef5fb 12%);
  backdrop-filter: blur(14px);
}

.header-content {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  align-items: center;
  gap: 24px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
}

.brand-icon {
  width: 38px;
  height: 38px;
  border-radius: 11px;
  display: grid;
  place-items: center;
  font-size: 22px;
  color: #ffffff;
  background: linear-gradient(140deg, var(--pm-primary), #16a4cb);
  box-shadow: 0 8px 20px rgba(15, 124, 207, 0.32);
}

.brand-copy {
  display: flex;
  flex-direction: column;
  line-height: 1.12;
}

.brand-copy strong {
  color: var(--pm-text);
  font-size: 18px;
  letter-spacing: -0.01em;
}

.brand-copy span {
  color: var(--pm-text-soft);
  font-size: 11px;
  letter-spacing: 0.03em;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: 8px;
}

.nav-link {
  padding: 9px 14px;
  border-radius: 999px;
  text-decoration: none;
  color: #355475;
  font-size: 13px;
  font-weight: 700;
  transition: all 0.24s ease;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--pm-primary-deep);
  background: #e7f3ff;
}

.header-actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}

.quota-badge {
  border: 1px solid #c8ddf0;
  border-radius: 999px;
  padding: 7px 12px;
  background: #ecf6ff;
  color: #23496f;
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
}

.plan-tag {
  border-color: #efca86;
  color: #8c5f08;
  background: #fff6e6;
}

.username {
  max-width: 108px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #3a5573;
  font-size: 13px;
  font-weight: 600;
}

.app-main {
  padding: 0;
  width: 100%;
  flex: 1;
}

.app-footer {
  border-top: 1px solid var(--pm-border);
  background: #f6f9fc;
  padding: 20px 0;
  height: auto;
}

.footer-content {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.footer-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.footer-brand {
  color: #1f3d5d;
  font-size: 13px;
  font-weight: 700;
}

.footer-copy {
  color: #6a8097;
  font-size: 12px;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 18px;
}

.footer-link {
  text-decoration: none;
  color: #5c738c;
  font-size: 12px;
  font-weight: 600;
}

.footer-link:hover {
  color: var(--pm-primary);
}

@media (max-width: 1080px) {
  .nav-links {
    display: none;
  }
}

@media (max-width: 820px) {
  .utility-inner,
  .header-content,
  .footer-content {
    padding: 0 14px;
  }

  .utility-text,
  .quota-badge,
  .username {
    display: none;
  }

  .footer-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
