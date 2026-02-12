<template>
  <div class="image-editor-container">
    <!-- 头部导航栏 -->
    <div class="header-section">
      <el-button @click="handleBack" class="back-btn">
        <el-icon><ArrowLeft /></el-icon>
        返回首页
      </el-button>
      <el-button @click="handleList" class="back-btn">
        图片列表
      </el-button>
      <!-- <h2 class="page-title">滤镜调节</h2> -->
      <el-button @click="toggleFullscreen" class="fullscreen-btn" :title="isFullscreen ? '退出全屏' : '全屏显示'">
        <el-icon><FullScreen v-if="!isFullscreen" /><Close v-else /></el-icon>
        {{ isFullscreen ? '退出全屏' : '全屏' }}
      </el-button>
      <el-button v-if="showFilterEditor" @click="togglePanel" class="toggle-panel-btn">
        <el-icon><ArrowRight v-if="isPanelExpanded" /><ArrowLeft v-else /></el-icon>
        {{ isPanelExpanded ? '收起面板' : '展开面板' }}
      </el-button>
    </div>

    <!-- 主页面：上传区域 -->
    <div v-if="!showFilterEditor" class="main-content">
      <div class="upload-section" v-if="!uploadedImages.length">
        <el-upload
          class="upload-area"
          :auto-upload="false"
          :multiple="true"
          :drag="true"
          accept=".jpg,.jpeg,.png,.gif,.bmp"
          :on-change="handleFileChange"
        >
          <el-icon><Upload class="upload-icon" /></el-icon>
          <h3 class="upload-title">拖放文件到此处</h3>
          <p class="upload-subtitle">或点击选择文件进行上传</p>
          <p class="upload-tip">支持单张或多张图片上传</p>
          <el-button type="primary" size="large" class="upload-btn"> 选择文件 </el-button>
        </el-upload>
      </div>

      <!-- 上传后的图片预览列表 -->
      <div v-else class="preview-list-section">
        <div class="preview-header">
          <h3 class="preview-title">已上传图片</h3>
          <el-button @click="clearAll" class="clear-btn">
            <el-icon><Delete /></el-icon>
            清空
          </el-button>
        </div>

        <div class="preview-grid">
          <div
            v-for="(image, index) in uploadedImages"
            :key="index"
            class="preview-item"
            @click="editImage(image.url)"
          >
            <div class="preview-wrapper">
              <img :src="image.url" :alt="image.name" class="preview-thumbnail" />
              <div class="preview-overlay">
                <div class="preview-action">
                  <el-icon><Edit class="action-icon" /></el-icon>
                </div>
              </div>
            </div>
            <div class="preview-info">
              <span class="image-name">{{ image.name }}</span>
              <span class="image-size">{{ formatSize(image.size) }}</span>
              <div class="preview-edit-hint">
                <el-icon><Edit /></el-icon>
                <span>点击编辑</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 单独的滤镜编辑页面 -->
    <div v-else class="filter-editor-wrapper">
      <FilterEditor 
        :image-url="currentImageUrl" 
        :is-panel-expanded="isPanelExpanded" 
        @back="showFilterEditor = false" 
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Upload, Delete, Edit, ArrowLeft, ArrowRight, FullScreen, Close } from '@element-plus/icons-vue'
import FilterEditor from './FilterEditor.vue'
import { useRouter } from 'vue-router'

/**
 * 组件Props类型定义
 */
interface ImageEditorProps {
  quickMode?: boolean
}

const props = withDefaults(defineProps<ImageEditorProps>(), {
  quickMode: false,
})

/**
 * 图片信息类型
 */
interface ImageInfo {
  name: string
  url: string
  size: number
}

/**
 * Element Plus 上传文件类型
 */
interface UploadFile {
  name: string
  raw: File
  size: number
}

// 上传图片列表，存储已上传的图片信息
const uploadedImages = ref<ImageInfo[]>([])
const currentImageUrl = ref<string | null>(null)
const showFilterEditor = ref<boolean>(false)
const isLoading = ref<boolean>(false)
const isPanelExpanded = ref<boolean>(true)
const isFullscreen = ref<boolean>(false)
const router = useRouter()

// 处理文件上传
const handleFileChange = (file: UploadFile): void => {
  console.log('文件上传:', file)
  if (!file || !file.raw) {
    console.error('无效的文件:', file)
    return
  }

  // 优化：使用createObjectURL代替DataURL，提高性能
  const objectUrl = URL.createObjectURL(file.raw)

  // 添加到已上传图片列表
  uploadedImages.value.push({
    name: file.name,
    url: objectUrl,
    size: file.size,
  })

  // 自动跳转到编辑页面
  currentImageUrl.value = objectUrl
  showFilterEditor.value = true
}

// 清空所有已上传图片
const clearAll = (): void => {
  // 释放所有object URLs，避免内存泄漏
  uploadedImages.value.forEach(image => {
    if (image.url.startsWith('blob:')) {
      URL.revokeObjectURL(image.url)
    }
  })
  uploadedImages.value = []

  // 重置当前图片和编辑器状态
  currentImageUrl.value = null
  showFilterEditor.value = false
}

// 编辑指定图片
const editImage = (url: string): void => {
  currentImageUrl.value = url
  showFilterEditor.value = true
}

// 返回按钮处理
const handleBack = (): void => {
  router.push('/editor-intro')
}

// 返回列表
const handleList = (): void => {
  showFilterEditor.value = false
}

// 切换控制面板
const togglePanel = (): void => {
  isPanelExpanded.value = !isPanelExpanded.value
}

// 切换全屏模式
const toggleFullscreen = (): void => {
  if (!document.fullscreenElement) {
    const element = document.querySelector('.image-editor-container') as HTMLElement
    if (element) {
      element.requestFullscreen().then(() => {
        isFullscreen.value = true
      }).catch(err => {
        console.error('进入全屏失败:', err)
      })
    }
  } else {
    document.exitFullscreen().then(() => {
      isFullscreen.value = false
    }).catch(err => {
      console.error('退出全屏失败:', err)
    })
  }
}

// 格式化文件大小
const formatSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + ' B'
  else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
  else return (bytes / 1048576).toFixed(1) + ' MB'
}
</script>

<style scoped>
.image-editor-container {
  width: 100%;
  min-height: 100vh;
  padding: 0;
  background-color: #fbfbfd;
  display: flex;
  flex-direction: column;
}

/* 头部导航栏 */
.header-section {
  display: flex;
  align-items: center;
  padding: 0 24px;
  height: 65px;
  margin-bottom: 0;
  border-bottom: 1px solid #e5e5ea;
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.back-btn {
  margin-right: 24px;
  background-color: white;
  border: 1px solid #e5e5ea;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0;
}

.fullscreen-btn {
  background-color: white;
  border: 1px solid #e5e5ea;
  border-radius: 980px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-left: auto;
}

.fullscreen-btn:hover {
  border-color: #0071e3;
  background-color: #f0f7ff;
  color: #0071e3;
}

.toggle-panel-btn {
  margin-left: auto;
  background-color: white;
  border: 1px solid #e5e5ea;
  border-radius: 980px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-panel-btn:hover {
  border-color: #0071e3;
  background-color: #f0f7ff;
  color: #0071e3;
}

.main-content {
  width: 100%;
  height: 100%;
}

/* 上传区域 */
.upload-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 65px);
}

:deep(.upload-area) {
  text-align: center;
  padding: 60px 80px;
  border: 2px dashed #d2d2d7;
  border-radius: 24px;
  background-color: #fbfbfd;
  transition: all 0.3s ease;
  width: 100%;
  max-width: 800px;
}

:deep(.upload-area:hover) {
  border-color: #0071e3;
  background-color: #f5f5f7;
}

.upload-icon {
  font-size: 64px;
  color: #86868b;
  margin-bottom: 16px;
}

.upload-title {
  font-size: 24px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 8px;
}

.upload-subtitle {
  font-size: 17px;
  color: #86868b;
  margin-bottom: 8px;
}

.upload-tip {
  font-size: 14px;
  color: #a1a1a6;
  margin-bottom: 24px;
}

.upload-btn {
  background-color: #0071e3;
  border: none;
  border-radius: 980px;
  padding: 12px 24px;
  font-size: 17px;
  font-weight: 400;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-btn:hover {
  background-color: #0077ed;
}

/* 预览列表区域 */
.preview-list-section {
  background-color: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  max-height: calc(100vh - 120px);
  overflow-y: auto;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e5ea;
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 10;
}

.preview-title {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0;
}

.clear-btn {
  background-color: white;
  border: 1px solid #e5e5ea;
  color: #86868b;
  transition: all 0.3s ease;
}

.clear-btn:hover {
  border-color: #ff3b30;
  color: #ff3b30;
}

/* 预览网格布局 - 改为水平卡片布局 */
.preview-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.preview-item {
  background-color: #fbfbfd;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  padding: 12px;
  gap: 16px;
}

.preview-item:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.preview-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  flex-shrink: 0;
}

.preview-thumbnail {
  width: 80px;
  height: 80px;
  object-fit: cover;
  display: block;
  border-radius: 8px;
}

.preview-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-item:hover .preview-overlay {
  opacity: 1;
}

.preview-action {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: white;
  font-size: 12px;
  font-weight: 500;
}

.action-icon {
  font-size: 20px;
}

.preview-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.image-name {
  font-size: 15px;
  font-weight: 500;
  color: #1d1d1f;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.image-size {
  font-size: 13px;
  color: #86868b;
}

/* 添加编辑提示文字 */
.preview-edit-hint {
  font-size: 13px;
  color: #0071e3;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 滤镜编辑页面容器 */
.filter-editor-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  padding-top: 65px;
}
</style>
