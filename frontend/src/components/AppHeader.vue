<template>
  <header class="app-header">
    <div class="header-content">
      <div class="header-left">
        <router-link to="/" class="logo">
          <div class="logo-icon">
            <el-icon :size="28"><PictureFilled /></el-icon>
          </div>
          <span class="logo-text">PicMaster</span>
        </router-link>
      </div>

      <nav class="header-nav">
        <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </router-link>
        <router-link to="/portfolios" class="nav-item" :class="{ active: $route.path === '/portfolios' }">
          <el-icon><FolderOpened /></el-icon>
          <span>作品集</span>
        </router-link>
        <router-link to="/editor" class="nav-item" :class="{ active: $route.path === '/editor' }">
          <el-icon><Edit /></el-icon>
          <span>图片编辑</span>
        </router-link>
      </nav>

      <div class="header-right">
        <template v-if="userStore.isLoggedIn">
          <div class="user-usage">
            <el-tooltip content="今日剩余编辑次数" placement="bottom">
              <div class="usage-badge">
                <el-icon><Edit /></el-icon>
                <span>{{ userStore.getRemainingCount('edit') }}</span>
              </div>
            </el-tooltip>
            <el-tooltip content="今日剩余保存次数" placement="bottom">
              <div class="usage-badge">
                <el-icon><Download /></el-icon>
                <span>{{ userStore.getRemainingCount('save') }}</span>
              </div>
            </el-tooltip>
          </div>

          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-info">
              <el-avatar :size="36" :src="userStore.user?.avatar">
                {{ userStore.user?.username?.charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="username">{{ userStore.user?.username }}</span>
              <el-tag v-if="userStore.isPremium" type="warning" size="small" effect="dark">会员</el-tag>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item command="upgrade" v-if="!userStore.isPremium">
                  <el-icon><StarFilled /></el-icon>
                  升级会员
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>

        <template v-else>
          <el-button type="primary" plain @click="showAuthDialog = true">
            登录 / 注册
          </el-button>
        </template>
      </div>
    </div>

    <AuthDialog v-model:visible="showAuthDialog" @success="handleAuthSuccess" />
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  PictureFilled,
  HomeFilled,
  FolderOpened,
  Edit,
  Download,
  User,
  StarFilled,
  SwitchButton
} from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'
import AuthDialog from './AuthDialog.vue'

const router = useRouter()
const userStore = useUserStore()
const showAuthDialog = ref(false)

const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'upgrade':
      ElMessage.info('会员功能开发中，敬请期待！')
      break
    case 'logout':
      ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        userStore.logout()
        ElMessage.success('已退出登录')
        router.push('/')
      }).catch(() => {})
      break
  }
}

const handleAuthSuccess = () => {
  userStore.fetchProfile()
}
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #e5e5ea;
  z-index: 1000;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.logo-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  color: white;
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  text-decoration: none;
  color: #666;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background: #f5f5f7;
  color: #1d1d1f;
}

.nav-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-usage {
  display: flex;
  align-items: center;
  gap: 12px;
}

.usage-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: #f5f5f7;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  color: #666;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 24px;
  transition: all 0.3s ease;
}

.user-info:hover {
  background: #f5f5f7;
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: #1d1d1f;
}
</style>
