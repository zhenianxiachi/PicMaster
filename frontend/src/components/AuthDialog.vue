<template>
  <el-dialog v-model="visible" width="460px" :close-on-click-modal="false" class="auth-dialog">
    <template #header>
      <div class="dialog-header">
        <p class="kicker">ACCOUNT CENTER</p>
        <h3>登录 PicMaster 账号</h3>
        <p>登录后可保存资产并获得每日免费配额。</p>
      </div>
    </template>

    <el-tabs v-model="activeTab" stretch class="dialog-tabs">
      <el-tab-pane label="登录" name="login">
        <el-form @submit.prevent>
          <el-form-item>
            <el-input v-model="loginForm.identity" placeholder="用户名或邮箱" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="loginForm.password" placeholder="密码" type="password" show-password />
          </el-form-item>
          <el-button type="primary" class="submit-btn" :loading="authStore.isLoading" @click="handleLogin">
            登录并继续
          </el-button>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="注册" name="register">
        <el-form @submit.prevent>
          <el-form-item>
            <el-input v-model="registerForm.username" placeholder="用户名" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="registerForm.email" placeholder="邮箱" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="registerForm.password" placeholder="密码（至少 6 位）" type="password" show-password />
          </el-form-item>
          <el-form-item>
            <el-input v-model="registerForm.confirmPassword" placeholder="确认密码" type="password" show-password />
          </el-form-item>
          <el-button type="primary" class="submit-btn" :loading="authStore.isLoading" @click="handleRegister">
            创建账号
          </el-button>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()

const visible = computed({
  get: () => authStore.authDialogVisible,
  set: value => {
    if (!value) {
      authStore.closeAuthDialog()
    }
  },
})

const activeTab = ref<'login' | 'register'>('login')

const loginForm = reactive({
  identity: '',
  password: '',
})

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
})

watch(
  () => authStore.authDialogMode,
  mode => {
    activeTab.value = mode
  },
  { immediate: true }
)

watch(activeTab, mode => {
  authStore.authDialogMode = mode
})

const handleLogin = async (): Promise<void> => {
  if (!loginForm.identity.trim() || !loginForm.password) {
    ElMessage.warning('请填写完整登录信息')
    return
  }

  const result = await authStore.login({
    identity: loginForm.identity,
    password: loginForm.password,
  })

  if (!result.success) {
    ElMessage.error(result.message)
    return
  }

  ElMessage.success(result.message)
  authStore.closeAuthDialog()
}

const handleRegister = async (): Promise<void> => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!registerForm.username.trim() || !registerForm.email.trim() || !registerForm.password.trim()) {
    ElMessage.warning('请填写完整注册信息')
    return
  }

  if (!emailPattern.test(registerForm.email)) {
    ElMessage.warning('请输入有效邮箱')
    return
  }

  if (registerForm.password.length < 6) {
    ElMessage.warning('密码长度至少 6 位')
    return
  }

  if (registerForm.password !== registerForm.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }

  const result = await authStore.register({
    username: registerForm.username,
    email: registerForm.email,
    password: registerForm.password,
  })

  if (!result.success) {
    ElMessage.error(result.message)
    return
  }

  ElMessage.success(result.message)
  authStore.closeAuthDialog()
}
</script>

<style scoped>
.dialog-header .kicker {
  color: var(--pm-primary);
  font-size: 11px;
  letter-spacing: 0.12em;
  font-weight: 800;
}

.dialog-header h3 {
  margin-top: 10px;
  color: var(--pm-text);
  font-size: 28px;
  letter-spacing: -0.02em;
}

.dialog-header p {
  margin-top: 8px;
  color: var(--pm-text-soft);
  font-size: 13px;
}

.dialog-tabs {
  margin-top: 2px;
}

.submit-btn {
  width: 100%;
  height: 44px;
  border: 0;
  border-radius: 12px;
  font-weight: 700;
  background: linear-gradient(130deg, var(--pm-primary), #17a4cf);
}

.submit-btn:hover {
  filter: brightness(1.04);
}
</style>
