<template>
  <div class="editor-shell">
    <header class="topbar">
      <div class="left-group">
        <el-button class="btn-soft" @click="handleBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <el-button class="btn-soft" @click="handleList">图片列表</el-button>
      </div>

      <div class="right-group">
        <span class="quota-pill" :title="usageStore.usageSummary.detail">{{ usageStore.usageSummary.label }}</span>
        <span v-if="authStore.isLoggedIn" class="user-pill">{{ authStore.user?.username }} · {{ authStore.planLabel }}</span>

        <el-button v-if="!authStore.isLoggedIn" type="primary" size="small" round @click="authStore.openAuthDialog('login')">
          登录
        </el-button>
        <el-button
          v-else-if="!authStore.isPro"
          type="warning"
          size="small"
          round
          @click="usageStore.openUpgradeDialog('daily', 'export-image')"
        >
          升级 Pro
        </el-button>

        <el-button class="btn-soft" @click="toggleFullscreen">
          <el-icon><FullScreen v-if="!isFullscreen" /><Close v-else /></el-icon>
          {{ isFullscreen ? '退出全屏' : '全屏' }}
        </el-button>
        <el-button v-if="showFilterEditor" class="btn-soft" @click="togglePanel">
          <el-icon><ArrowRight v-if="isPanelExpanded" /><ArrowLeft v-else /></el-icon>
          {{ isPanelExpanded ? '收起面板' : '展开面板' }}
        </el-button>
      </div>
    </header>

    <main v-if="!showFilterEditor" class="content">
      <section v-if="!uploadedImages.length" class="upload-card">
        <div class="upload-bg-shape"></div>
        <el-upload
          class="upload-area"
          :auto-upload="false"
          :multiple="true"
          :drag="true"
          accept=".jpg,.jpeg,.png,.gif,.bmp,.raf,.cr2,.nef,.arw,.dng,.raw"
          :on-change="handleFileChange"
        >
          <el-icon><Upload class="upload-icon" /></el-icon>
          <h2>将图片拖拽到这里</h2>
          <p>支持批量上传，点击任意缩略图进入高级编辑</p>
          <el-button type="primary" size="large">选择图片</el-button>
        </el-upload>
      </section>

      <section v-else class="list-card">
        <div class="list-head">
          <h3>已上传图片</h3>
          <el-button class="btn-soft" @click="clearAll">清空全部</el-button>
        </div>
        <div class="preview-grid">
          <article v-for="(image, index) in uploadedImages" :key="index" class="preview-item" @click="editImage(image.url)">
            <img :src="image.url" :alt="image.name" />
            <div class="meta">
              <span class="name">{{ image.name }}</span>
              <span class="size">{{ formatSize(image.size) }}</span>
            </div>
          </article>
        </div>
      </section>
    </main>

    <section v-else class="editor-panel">
      <FilterEditor :image-url="currentImageUrl" :is-panel-expanded="isPanelExpanded" @back="showFilterEditor = false" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { onUnmounted, ref } from 'vue'
import { Upload, ArrowLeft, ArrowRight, FullScreen, Close } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import FilterEditor from './FilterEditor.vue'
import { useAuthStore } from '@/store/auth'
import { useUsageStore } from '@/store/usage'

interface UploadFile {
  name: string
  raw?: File
  size: number
}

interface ImageInfo {
  name: string
  url: string
  size: number
}

const uploadedImages = ref<ImageInfo[]>([])
const currentImageUrl = ref<string | null>(null)
const showFilterEditor = ref(false)
const isPanelExpanded = ref(true)
const isFullscreen = ref(false)

const router = useRouter()
const authStore = useAuthStore()
const usageStore = useUsageStore()

const handleFileChange = (file: UploadFile): void => {
  if (!file.raw) {
    return
  }

  const objectUrl = URL.createObjectURL(file.raw)
  uploadedImages.value.push({
    name: file.name,
    url: objectUrl,
    size: file.size,
  })

  currentImageUrl.value = objectUrl
  showFilterEditor.value = true
}

const clearAll = (): void => {
  uploadedImages.value.forEach(image => {
    if (image.url.startsWith('blob:')) {
      URL.revokeObjectURL(image.url)
    }
  })
  uploadedImages.value = []
  currentImageUrl.value = null
  showFilterEditor.value = false
}

const editImage = (url: string): void => {
  currentImageUrl.value = url
  showFilterEditor.value = true
}

const handleBack = (): void => {
  router.push('/editor-intro')
}

const handleList = (): void => {
  showFilterEditor.value = false
}

const togglePanel = (): void => {
  isPanelExpanded.value = !isPanelExpanded.value
}

const toggleFullscreen = (): void => {
  if (!document.fullscreenElement) {
    const element = document.querySelector('.editor-shell') as HTMLElement | null
    if (!element) {
      return
    }
    element.requestFullscreen().then(() => {
      isFullscreen.value = true
    })
    return
  }
  document.exitFullscreen().then(() => {
    isFullscreen.value = false
  })
}

const formatSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1048576).toFixed(1)} MB`
}

onUnmounted(() => {
  uploadedImages.value.forEach(image => {
    if (image.url.startsWith('blob:')) {
      URL.revokeObjectURL(image.url)
    }
  })
})
</script>

<style scoped>
.editor-shell {
  min-height: 100vh;
  background:
    radial-gradient(circle at 85% -10%, rgba(19, 181, 168, 0.14), transparent 28%),
    radial-gradient(circle at 10% 0%, rgba(15, 124, 207, 0.13), transparent 34%),
    #f4f8fc;
}

.topbar {
  position: fixed;
  inset: 0 0 auto 0;
  height: 70px;
  z-index: 1200;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 0 18px;
  border-bottom: 1px solid var(--pm-border);
  background: color-mix(in srgb, #ffffff 88%, #edf4fb 12%);
  backdrop-filter: blur(12px);
}

.left-group,
.right-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-soft {
  border: 1px solid #c6d9ea;
  background: #ffffff;
}

.quota-pill {
  border: 1px solid #c6d9ea;
  border-radius: 999px;
  padding: 7px 12px;
  font-size: 12px;
  font-weight: 700;
  color: #264a70;
  background: #ebf6ff;
}

.user-pill {
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 12px;
  color: #385a7d;
  background: #f2f8ff;
}

.content {
  padding-top: 70px;
}

.upload-card {
  min-height: calc(100vh - 70px);
  display: grid;
  place-items: center;
  padding: 24px;
  position: relative;
}

.upload-bg-shape {
  position: absolute;
  width: min(920px, 90vw);
  height: 300px;
  border-radius: 40px;
  background: linear-gradient(135deg, rgba(15, 124, 207, 0.14), rgba(19, 181, 168, 0.12));
  filter: blur(24px);
}

:deep(.upload-area) {
  width: min(960px, 96vw);
  padding: 56px 32px;
  border: 2px dashed #b4cde3;
  border-radius: 26px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: var(--pm-shadow-1);
  text-align: center;
}

.upload-icon {
  font-size: 62px;
  color: #4c759b;
}

:deep(.upload-area h2) {
  margin-top: 14px;
  font-size: clamp(28px, 5vw, 40px);
  color: var(--pm-text);
  letter-spacing: -0.02em;
}

:deep(.upload-area p) {
  margin-top: 10px;
  color: var(--pm-text-soft);
}

.list-card {
  width: min(1200px, calc(100% - 40px));
  margin: 22px auto 30px;
  border: 1px solid var(--pm-border);
  border-radius: 20px;
  background: var(--pm-surface);
  padding: 18px;
  box-shadow: var(--pm-shadow-1);
}

.list-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.list-head h3 {
  color: var(--pm-text);
  font-size: 24px;
}

.preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 12px;
}

.preview-item {
  border: 1px solid var(--pm-border);
  border-radius: 14px;
  background: #ffffff;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.22s ease;
}

.preview-item:hover {
  transform: translateY(-3px);
  box-shadow: var(--pm-shadow-1);
}

.preview-item img {
  width: 100%;
  height: 148px;
  object-fit: cover;
  display: block;
}

.meta {
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.name {
  color: #204264;
  font-size: 13px;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.size {
  color: #6a8095;
  font-size: 12px;
}

.editor-panel {
  padding-top: 70px;
}

@media (max-width: 920px) {
  .quota-pill,
  .user-pill {
    display: none;
  }
}

@media (max-width: 760px) {
  .topbar {
    height: auto;
    padding: 10px 12px;
    flex-direction: column;
    align-items: flex-start;
  }

  .content,
  .editor-panel {
    padding-top: 108px;
  }

  .upload-card {
    min-height: calc(100vh - 108px);
    padding: 12px;
  }
}
</style>
