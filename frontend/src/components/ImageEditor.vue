<template>
  <div class="image-editor-container">
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
          <el-icon-upload class="upload-icon" />
          <h3 class="upload-title">拖放文件到此处</h3>
          <p class="upload-subtitle">或点击选择文件进行上传</p>
          <p class="upload-tip">支持单张或多张图片上传</p>
          <el-button type="primary" size="large" class="upload-btn">
            选择文件
          </el-button>
        </el-upload>
      </div>
      
      <!-- 上传后的图片预览列表 -->
      <div v-else class="preview-list-section">
        <div class="preview-header">
          <h3 class="preview-title">已上传图片</h3>
          <el-button @click="clearAll" class="clear-btn">
            <el-icon-delete />
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
                  <el-icon-edit class="action-icon" />
                  <span>编辑图片</span>
                </div>
              </div>
              <div class="preview-info">
                <span class="image-name">{{ image.name }}</span>
                <span class="image-size">{{ formatSize(image.size) }}</span>
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
        @back="showFilterEditor = false"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import FilterEditor from './FilterEditor.vue'

const props = defineProps({
  quickMode: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([])

// 上传图片列表，存储已上传的图片信息
const uploadedImages = ref([])
const currentImageUrl = ref(null)
const showFilterEditor = ref(false)
const isLoading = ref(false) // 图片加载状态

// 处理文件上传
const handleFileChange = (file) => {
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
    size: file.size
  })
  
  // 自动跳转到编辑页面
  currentImageUrl.value = objectUrl
  showFilterEditor.value = true
}

// 清空所有已上传图片
const clearAll = () => {
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
const editImage = (url) => {
  currentImageUrl.value = url
  showFilterEditor.value = true
}

// 格式化文件大小
const formatSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
  else return (bytes / 1048576).toFixed(1) + ' MB'
}
</script>

<style scoped>
.image-editor-container {
  padding: 0;
  background-color: #ffffff;
  min-height: 100vh;
}

.main-content {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

/* 上传区域 */
.upload-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 140px);
}

:deep(.upload-area) {
  text-align: center;
  padding: 40px 60px;
  border: 2px dashed #e0e0e0;
  border-radius: 16px;
  background-color: #fafafa;
  transition: all 0.3s ease;
  width: 100%;
  max-width: 700px;
}

:deep(.upload-area:hover) {
  border-color: #0071e3;
  background-color: #f5f9ff;
}

.upload-icon {
  font-size: 56px;
  color: #999999;
  margin-bottom: 16px;
}

.upload-title {
  font-size: 20px;
  font-weight: 600;
  color: #333333;
  margin-bottom: 8px;
}

.upload-subtitle {
  font-size: 15px;
  color: #666666;
  margin-bottom: 8px;
}

.upload-tip {
  font-size: 13px;
  color: #999999;
  margin-bottom: 20px;
}

.upload-btn {
  background-color: #0071e3;
  border: none;
  border-radius: 20px;
  padding: 10px 20px;
  font-size: 15px;
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
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.preview-title {
  font-size: 18px;
  font-weight: 600;
  color: #333333;
  margin: 0;
}

.clear-btn {
  background-color: white;
  border: 1px solid #f0f0f0;
  color: #666666;
  transition: all 0.3s ease;
}

.clear-btn:hover {
  border-color: #ff3b30;
  color: #ff3b30;
}

/* 预览网格布局 */
.preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

.preview-item {
  background-color: #fafafa;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.preview-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.preview-wrapper {
  position: relative;
  width: 100%;
}

.preview-thumbnail {
  width: 100%;
  height: 130px;
  object-fit: cover;
  display: block;
}

.preview-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.5), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 12px;
}

.preview-item:hover .preview-overlay {
  opacity: 1;
}

.preview-action {
  display: flex;
  align-items: center;
  gap: 6px;
  color: white;
  font-size: 13px;
  font-weight: 500;
}

.action-icon {
  font-size: 14px;
}

.preview-info {
  padding: 10px;
  background-color: white;
}

.image-name {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #333333;
  margin-bottom: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.image-size {
  font-size: 11px;
  color: #666666;
}

/* 滤镜编辑页面容器 */
.filter-editor-wrapper {
  width: 100%;
  height: calc(100vh - 64px);
  overflow: hidden;
}
</style>