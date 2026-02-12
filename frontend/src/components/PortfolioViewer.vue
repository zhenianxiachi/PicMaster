<template>
  <div class="portfolio-viewer-container">
    <div class="select-section">
      <el-select v-model="selectedPortfolioId" placeholder="选择作品集" class="portfolio-select" @change="loadPortfolio">
        <el-option
          v-for="portfolio in portfolios"
          :key="portfolio.id"
          :label="portfolio.name"
          :value="portfolio.id"
        />
      </el-select>
      <el-button type="primary" @click="generatePortfolioQRCode" :disabled="!currentPortfolio">
        <el-icon><el-icon-scan /></el-icon>
        生成二维码
      </el-button>
    </div>

    <div v-if="currentPortfolio" class="display-section">
      <div class="grid-layout">
        <div
          v-for="image in currentPortfolio.images"
          :key="image.id"
          class="grid-item"
          :class="{ 'selected': currentPreviewImage?.id === image.id }"
          @click="showImagePreview(image)"
        >
          <img :src="image.thumbnail_path" alt="作品集图片" loading="lazy" />
          <div class="grid-overlay">
            <el-icon><el-icon-zoom-in /></el-icon>
          </div>
        </div>
      </div>
    </div>

    <el-dialog
      v-model="showPreviewDialog"
      title="图片预览"
      width="90%"
      class="preview-dialog"
      :show-close="true"
      :lock-scroll="false"
      :close-on-click-modal="true"
    >
      <div class="preview-content">
        <div class="image-preview-area" ref="imagePreviewArea">
          <div v-if="currentPreviewImage" class="preview-container">
            <img 
              :src="processedImageUrl || currentPreviewImage.filepath" 
              alt="预览图片" 
              class="preview-image"
              :class="{ 'processing': isProcessing }"
              :style="imageTransformStyle"
              @wheel="handleImageWheel"
              @mousedown="startImageDrag"
              @mousemove="handleImageDrag"
              @mouseup="endImageDrag"
              @mouseleave="endImageDrag"
            />
            <div v-if="isProcessing" class="processing-overlay">
              <el-icon class="loading-icon"><el-icon-loading /></el-icon>
              <span>处理中...</span>
            </div>
          </div>
          <div class="zoom-controls">
            <el-button-group>
              <el-button @click="zoomOut" :disabled="imageScale <= 0.5" size="small">
                <el-icon><el-icon-zoom-out /></el-icon>
              </el-button>
              <el-button size="small" disabled>{{ Math.round(imageScale * 100) }}%</el-button>
              <el-button @click="zoomIn" :disabled="imageScale >= 3" size="small">
                <el-icon><el-icon-zoom-in /></el-icon>
              </el-button>
              <el-button @click="resetZoom" size="small">
                <el-icon><el-icon-refresh-left /></el-icon>
              </el-button>
            </el-button-group>
          </div>
        </div>
        
        <div class="ai-adjust-section">
          <div class="ai-header">
            <el-icon class="ai-icon"><el-icon-magic-stick /></el-icon>
            <span class="ai-title">AI智能调整</span>
          </div>
          
          <div class="ai-input-area">
            <el-input
              v-model="aiInputText"
              type="textarea"
              :rows="3"
              placeholder="描述您想要的效果，如：让照片更亮一点、增加对比度、调成暖色调、添加电影感..."
              class="ai-textarea"
              @keydown.enter.ctrl="applyAIAdjustment"
            />
            <div class="ai-actions">
              <el-button 
                type="primary" 
                @click="applyAIAdjustment" 
                :loading="isAILoading"
                class="apply-btn"
              >
                <el-icon v-if="!isAILoading"><el-icon-magic-stick /></el-icon>
                {{ isAILoading ? '处理中...' : '应用调整' }}
              </el-button>
              <el-button 
                v-if="processedImageUrl"
                @click="resetImage"
                class="reset-btn"
              >
                <el-icon><el-icon-refresh-left /></el-icon>
                还原原图
              </el-button>
              <el-button 
                v-if="processedImageUrl"
                type="success"
                @click="downloadProcessedImage"
                class="download-btn"
              >
                <el-icon><el-icon-download /></el-icon>
                下载图片
              </el-button>
            </div>
          </div>
          
          <div v-if="aiExplanation" class="ai-explanation">
            <el-icon><el-icon-info-filled /></el-icon>
            <span>{{ aiExplanation }}</span>
          </div>
          
          <div class="ai-suggestions">
            <span class="suggestion-label">快捷建议：</span>
            <el-tag 
              v-for="suggestion in aiSuggestions" 
              :key="suggestion"
              @click="applyQuickSuggestion(suggestion)"
              class="suggestion-tag"
              effect="plain"
            >
              {{ suggestion }}
            </el-tag>
          </div>
          
          <div v-if="currentFilterParams" class="filter-params-display">
            <div class="params-header" @click="showParamsDetail = !showParamsDetail">
              <span>当前参数</span>
              <el-icon :class="{ 'rotated': showParamsDetail }"><el-icon-arrow-down /></el-icon>
            </div>
            <div v-if="showParamsDetail" class="params-detail">
              <div v-for="(value, key) in currentFilterParams" :key="key" class="param-item">
                <span class="param-name">{{ getFilterParamLabel(key) }}</span>
                <span class="param-value">{{ formatParamValue(key, value) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
    
    <el-dialog
      v-model="showQRCodeDialog"
      title="作品集二维码"
      width="400px"
      class="qrcode-dialog"
    >
      <div class="qrcode-container">
        <div v-if="qrcodeDataUrl" class="qrcode-content">
          <img :src="qrcodeDataUrl" alt="作品集二维码" class="qrcode-image" />
          <p class="qrcode-tip">使用微信扫码查看作品集</p>
          <p class="qrcode-url">{{ qrcodeUrl }}</p>
        </div>
        <div v-else class="qrcode-loading">
          <el-icon class="loading-icon"><el-icon-loading /></el-icon>
          <span>生成二维码中...</span>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showQRCodeDialog = false">关闭</el-button>
          <el-button type="primary" @click="downloadQRCode">
            <el-icon><el-icon-download /></el-icon>
            下载二维码
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, type CSSProperties } from 'vue'
import { ElMessage } from 'element-plus'
import { portfolioApi, type Portfolio, type Image as PortfolioImage } from '../api/portfolioApi.js'
import config from '../config'
import { errorHandler } from '../utils/errorHandler'
import { logger } from '../utils/logger'
import { 
  applyAllFilters, 
  applyBlur
} from '../utils/imageFilters'

interface FilterParamsResult {
  brightness: number
  contrast: number
  saturation: number
  hue: number
  sharpness: number
  exposure: number
  highlights: number
  shadows: number
  temperature: number
  tint: number
  vignette: number
  clarity: number
  blur: number
  [key: string]: number
}

const props = defineProps({
  initialPortfolioId: {
    type: Number,
    default: null
  }
})

const portfolios = ref<Portfolio[]>([])
const selectedPortfolioId = ref<number | null>(null)
const currentPortfolio = ref<Portfolio | null>(null)
const showPreviewDialog = ref(false)
const currentPreviewImage = ref<PortfolioImage | null>(null)

const aiInputText = ref('')
const isAILoading = ref(false)
const aiExplanation = ref('')
const aiSuggestions: string[] = [
  '更亮一点',
  '增加对比度',
  '暖色调',
  '电影感',
  '人像美化',
  '风景增强',
]

const isProcessing = ref(false)
const processedImageUrl = ref('')
const currentFilterParams = ref<FilterParamsResult | null>(null)
const showParamsDetail = ref(false)

const imageScale = ref(1)
const imageTranslateX = ref(0)
const imageTranslateY = ref(0)
const isDragging = ref(false)
const dragStartX = ref(0)
const dragStartY = ref(0)
const dragTranslateX = ref(0)
const dragTranslateY = ref(0)

const imageTransformStyle = ref<CSSProperties>({
  transform: 'scale(1) translate(0px, 0px)',
  cursor: 'grab'
})

const showQRCodeDialog = ref(false)
const qrcodeDataUrl = ref('')
const qrcodeUrl = ref('')

const filterParamLabels: Record<string, string> = {
  brightness: '亮度',
  contrast: '对比度',
  saturation: '饱和度',
  hue: '色相',
  sharpness: '锐化',
  exposure: '曝光',
  highlights: '高光',
  shadows: '阴影',
  temperature: '色温',
  tint: '色调',
  vignette: '暗角',
  clarity: '清晰度',
  blur: '模糊'
}

const getFilterParamLabel = (key: string): string => filterParamLabels[key] || key

const formatParamValue = (key: string, value: number): string => {
  if (key === 'contrast') {
    return value > 100 ? `+${value - 100}` : value < 100 ? `-${100 - value}` : '0'
  }
  return value > 0 ? `+${value}` : String(value)
}

const initData = async (): Promise<void> => {
  try {
    const portfolioList = await portfolioApi.getPortfolios()
    portfolios.value = portfolioList
    
    if (props.initialPortfolioId) {
      selectedPortfolioId.value = props.initialPortfolioId
      loadPortfolio()
    } else if (portfolios.value.length > 0 && portfolios.value[0]) {
      selectedPortfolioId.value = portfolios.value[0].id
      loadPortfolio()
    }
  } catch (error) {
    errorHandler.handleApiError(error, '初始化数据失败')
  }
}

const loadPortfolio = async (): Promise<void> => {
  if (!selectedPortfolioId.value) return
  
  try {
    const portfolio = await portfolioApi.getPortfolioDetail(selectedPortfolioId.value)
    if (portfolio) {
      currentPortfolio.value = portfolio
    }
  } catch (error) {
    errorHandler.handleApiError(error, '加载作品集失败')
  }
}

const showImagePreview = (image: PortfolioImage): void => {
  currentPreviewImage.value = image
  processedImageUrl.value = ''
  currentFilterParams.value = null
  aiExplanation.value = ''
  aiInputText.value = ''
  resetZoom()
  showPreviewDialog.value = true
}

const resetZoom = () => {
  imageScale.value = 1
  imageTranslateX.value = 0
  imageTranslateY.value = 0
  updateImageTransform()
}

const updateImageTransform = () => {
  imageTransformStyle.value = {
    transform: `scale(${imageScale.value}) translate(${imageTranslateX.value}px, ${imageTranslateY.value}px)`,
    cursor: isDragging.value ? 'grabbing' : 'grab'
  }
}

const zoomIn = () => {
  if (imageScale.value < 3) {
    imageScale.value = Math.min(3, imageScale.value + 0.25)
    updateImageTransform()
  }
}

const zoomOut = () => {
  if (imageScale.value > 0.5) {
    imageScale.value = Math.max(0.5, imageScale.value - 0.25)
    updateImageTransform()
  }
}

const handleImageWheel = (e: WheelEvent) => {
  e.preventDefault()
  const delta = e.deltaY > 0 ? -0.1 : 0.1
  const newScale = Math.max(0.5, Math.min(3, imageScale.value + delta))
  imageScale.value = newScale
  updateImageTransform()
}

const startImageDrag = (e: MouseEvent) => {
  if (imageScale.value > 1) {
    isDragging.value = true
    dragStartX.value = e.clientX
    dragStartY.value = e.clientY
    dragTranslateX.value = imageTranslateX.value
    dragTranslateY.value = imageTranslateY.value
    updateImageTransform()
  }
}

const handleImageDrag = (e: MouseEvent) => {
  if (!isDragging.value) return
  
  const deltaX = (e.clientX - dragStartX.value) / imageScale.value
  const deltaY = (e.clientY - dragStartY.value) / imageScale.value
  
  imageTranslateX.value = dragTranslateX.value + deltaX
  imageTranslateY.value = dragTranslateY.value + deltaY
  updateImageTransform()
}

const endImageDrag = () => {
  isDragging.value = false
  updateImageTransform()
}

const applyQuickSuggestion = (suggestion: string): void => {
  aiInputText.value = suggestion
  applyAIAdjustment()
}

const applyAIAdjustment = async (): Promise<void> => {
  if (!aiInputText.value.trim()) {
    ElMessage.warning('请输入修改意见')
    return
  }

  isAILoading.value = true
  aiExplanation.value = ''

  try {
    const apiBase = config.apiBaseUrl.replace('/api', '')
    const response = await fetch(`${apiBase}/api/ai/parse-intent`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: aiInputText.value,
        current_params: currentFilterParams.value || {
          brightness: 0,
          contrast: 100,
          saturation: 100,
          hue: 0,
          sharpness: 0,
          exposure: 0,
          highlights: 0,
          shadows: 0,
          temperature: 0,
          tint: 0,
          vignette: 0,
          clarity: 0,
          blur: 0,
        },
        use_ai: false
      })
    })

    if (!response.ok) {
      throw new Error('AI服务请求失败')
    }

    const data = await response.json()
    
    if (data.params) {
      currentFilterParams.value = data.params
      aiExplanation.value = data.explanation || '已根据您的描述调整参数'
      
      await applyFiltersToImage(data.params)
      ElMessage.success('AI已调整参数')
    }
  } catch (error) {
    logger.error('AI调整失败:', error)
    ElMessage.error('AI调整失败，请重试')
  } finally {
    isAILoading.value = false
  }
}

const applyFiltersToImage = async (params: FilterParamsResult): Promise<void> => {
  if (!currentPreviewImage.value) return
  
  isProcessing.value = true
  
  try {
    const img = new Image()
    img.crossOrigin = 'anonymous'
    
    await new Promise<void>((resolve, reject) => {
      img.onload = () => resolve()
      img.onerror = reject
      img.src = currentPreviewImage.value!.filepath
    })
    
    const canvas = document.createElement('canvas')
    canvas.width = img.naturalWidth
    canvas.height = img.naturalHeight
    const ctx = canvas.getContext('2d')
    
    if (!ctx) {
      throw new Error('无法获取Canvas上下文')
    }
    
    ctx.drawImage(img, 0, 0)
    
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
    
    const filterParams = {
      brightness: params.brightness ?? 0,
      contrast: params.contrast ?? 100,
      saturation: params.saturation ?? 100,
      hue: params.hue ?? 0,
      blur: 0,
      sharpness: params.sharpness ?? 0,
      exposure: params.exposure ?? 0,
      highlights: params.highlights ?? 0,
      shadows: params.shadows ?? 0,
      temperature: params.temperature ?? 0,
      tint: params.tint ?? 0,
      vignette: params.vignette ?? 0,
      clarity: params.clarity ?? 0,
    }
    
    const processedData = applyAllFilters(imageData, filterParams)
    ctx.putImageData(processedData, 0, 0)
    
    if (params.blur > 0) {
      const blurCanvas = document.createElement('canvas')
      blurCanvas.width = canvas.width
      blurCanvas.height = canvas.height
      const blurCtx = blurCanvas.getContext('2d')
      if (blurCtx) {
        blurCtx.drawImage(canvas, 0, 0)
        const blurData = blurCtx.getImageData(0, 0, canvas.width, canvas.height)
        applyBlur(blurData.data, canvas.width, canvas.height, params.blur)
        blurCtx.putImageData(blurData, 0, 0)
        ctx.drawImage(blurCanvas, 0, 0)
      }
    }
    
    processedImageUrl.value = canvas.toDataURL('image/png', 1.0)
    
  } catch (error) {
    logger.error('图片处理失败:', error)
    ElMessage.error('图片处理失败')
  } finally {
    isProcessing.value = false
  }
}

const resetImage = (): void => {
  processedImageUrl.value = ''
  currentFilterParams.value = null
  aiExplanation.value = ''
  aiInputText.value = ''
  ElMessage.success('已还原原图')
}

const downloadProcessedImage = (): void => {
  if (!processedImageUrl.value || !currentPreviewImage.value) return
  
  const link = document.createElement('a')
  link.href = processedImageUrl.value
  link.download = `edited_${currentPreviewImage.value.filename}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  ElMessage.success('图片下载成功')
}

const generatePortfolioQRCode = async (): Promise<void> => {
  if (!currentPortfolio.value) return
  
  try {
    const portfolioId = currentPortfolio.value.id
    const currentOrigin = window.location.origin
    const portfolioUrl = `${currentOrigin}/viewer?portfolio_id=${portfolioId}`
    qrcodeUrl.value = portfolioUrl
    
    qrcodeDataUrl.value = ''
    showQRCodeDialog.value = true
    
    const apiBase = config.apiBaseUrl.replace('/api', '')
    const response = await fetch(`${apiBase}/api/previews/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        portfolio_id: portfolioId,
        preview_url: portfolioUrl
      })
    })
    
    if (!response.ok) {
      throw new Error('生成二维码失败')
    }
    
    const data = await response.json()
    qrcodeDataUrl.value = data.qr_code
    
  } catch (error) {
    logger.error('生成二维码失败:', error)
    errorHandler.handleApiError(error, '生成二维码失败')
  }
}

const downloadQRCode = (): void => {
  if (!qrcodeDataUrl.value || !currentPortfolio.value) return
  
  const link = document.createElement('a')
  link.href = qrcodeDataUrl.value
  link.download = `portfolio_${currentPortfolio.value.id}_qrcode.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(() => {
  initData()
})
</script>

<style scoped>
.portfolio-viewer-container {
  padding: 24px;
}

.select-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

:deep(.portfolio-select .el-input__wrapper) {
  border-radius: 12px;
  box-shadow: 0 0 0 1px #e5e5ea;
  padding: 4px 16px;
  min-width: 240px;
}

:deep(.portfolio-select .el-input__wrapper:hover) {
  box-shadow: 0 0 0 2px rgba(0, 113, 227, 0.2);
}

.display-section {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.grid-layout {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.grid-item {
  position: relative;
  cursor: pointer;
  overflow: hidden;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s ease;
  aspect-ratio: 4 / 3;
}

.grid-item:hover {
  transform: scale(1.02);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.16);
}

.grid-item.selected {
  box-shadow: 0 0 0 3px #0071e3, 0 12px 40px rgba(0, 113, 227, 0.3);
}

.grid-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}

.grid-item:hover img {
  transform: scale(1.05);
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.grid-item:hover .grid-overlay {
  opacity: 1;
}

.grid-overlay .el-icon {
  font-size: 48px;
  color: white;
}

.preview-content {
  display: flex;
  gap: 24px;
  min-height: 500px;
}

.image-preview-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f7;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
}

.preview-container {
  position: relative;
  max-width: 100%;
  max-height: 600px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
}

.preview-image {
  max-width: 100%;
  max-height: 600px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.1s ease-out, opacity 0.3s ease;
  user-select: none;
  -webkit-user-drag: none;
}

.preview-image.processing {
  opacity: 0.5;
}

.zoom-controls {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  padding: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  z-index: 10;
}

.zoom-controls :deep(.el-button-group) {
  display: flex;
}

.zoom-controls :deep(.el-button) {
  padding: 8px 12px;
}

.processing-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  gap: 12px;
}

.processing-overlay .loading-icon {
  font-size: 36px;
  color: #0071e3;
  animation: spin 1s linear infinite;
}

.processing-overlay span {
  font-size: 14px;
  color: #666;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.ai-adjust-section {
  width: 380px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border-radius: 16px;
  border: 1px solid #e0e7ff;
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ai-icon {
  font-size: 22px;
  color: #6366f1;
}

.ai-title {
  font-size: 16px;
  font-weight: 600;
  color: #4f46e5;
}

.ai-input-area {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ai-textarea {
  width: 100%;
}

.ai-textarea :deep(.el-textarea__inner) {
  border-radius: 12px;
  border-color: #c7d2fe;
  font-size: 14px;
  resize: none;
}

.ai-textarea :deep(.el-textarea__inner:focus) {
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
}

.ai-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.apply-btn {
  flex: 1;
  border-radius: 10px;
  font-weight: 500;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
}

.apply-btn:hover {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
}

.reset-btn,
.download-btn {
  border-radius: 10px;
  font-weight: 500;
}

.ai-explanation {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px;
  background-color: #ecfdf5;
  border-radius: 10px;
  font-size: 13px;
  color: #059669;
  border: 1px solid #a7f3d0;
}

.ai-explanation .el-icon {
  margin-top: 2px;
  flex-shrink: 0;
}

.ai-suggestions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.suggestion-label {
  font-size: 12px;
  color: #6b7280;
}

.suggestion-tag {
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 12px;
  border-radius: 16px;
}

.suggestion-tag:hover {
  background-color: #6366f1;
  color: white;
  border-color: #6366f1;
}

.filter-params-display {
  background-color: white;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.params-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  background-color: #f9fafb;
}

.params-header .el-icon {
  transition: transform 0.3s ease;
}

.params-header .el-icon.rotated {
  transform: rotate(180deg);
}

.params-detail {
  padding: 12px 16px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  border-top: 1px solid #e5e7eb;
}

.param-item {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.param-name {
  color: #6b7280;
}

.param-value {
  color: #374151;
  font-weight: 500;
}

:deep(.preview-dialog .el-dialog) {
  border-radius: 20px;
  overflow: hidden;
  max-width: 1200px;
}

:deep(.preview-dialog .el-dialog__header) {
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.preview-dialog .el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: #1d1d1f;
}

:deep(.preview-dialog .el-dialog__body) {
  padding: 24px;
}

@media (max-width: 900px) {
  .preview-content {
    flex-direction: column;
  }
  
  .ai-adjust-section {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .select-section {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .grid-layout {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
  }
}

.qrcode-dialog .el-dialog__body {
  padding: 30px;
}

.qrcode-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.qrcode-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
}

.qrcode-image {
  width: 300px;
  height: 300px;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.qrcode-tip {
  font-size: 16px;
  font-weight: 500;
  color: #333333;
  margin: 0;
}

.qrcode-url {
  font-size: 14px;
  color: #666666;
  margin: 0;
  word-break: break-all;
  max-width: 100%;
  overflow-wrap: break-word;
}

.qrcode-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 40px 0;
}

.qrcode-loading .loading-icon {
  font-size: 48px;
  color: #0071e3;
  animation: spin 1s linear infinite;
}

.qrcode-loading span {
  font-size: 16px;
  color: #666666;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
