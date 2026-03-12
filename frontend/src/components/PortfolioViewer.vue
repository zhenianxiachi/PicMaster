<template>
  <section class="portfolio-viewer">
    <div class="control-card">
      <div class="control-head">
        <h2>作品展示控制台</h2>
        <p>选择作品集后可进行客户预览、AI 快速调色与二维码分享。</p>
      </div>

      <div class="control-actions">
        <el-select
          v-model="selectedPortfolioId"
          placeholder="请选择作品集"
          class="portfolio-select"
          @change="loadPortfolio"
        >
          <el-option v-for="portfolio in portfolios" :key="portfolio.id" :label="portfolio.name" :value="portfolio.id" />
        </el-select>

        <el-button type="primary" class="share-btn" :disabled="!currentPortfolio" @click="generatePortfolioQRCode">
          <el-icon><Promotion /></el-icon>
          生成分享二维码
        </el-button>
      </div>
    </div>

    <div v-if="currentPortfolio" class="meta-strip">
      <span>名称：{{ currentPortfolio.name }}</span>
      <span>客户：{{ currentPortfolio.client_name || '未填写' }}</span>
      <span>拍摄日期：{{ formatDate(currentPortfolio.shoot_date) }}</span>
      <span>图片数：{{ currentPortfolio.images.length }}</span>
    </div>

    <div v-if="currentPortfolio && currentPortfolio.images.length" class="gallery-grid">
      <article
        v-for="image in currentPortfolio.images"
        :key="image.id"
        class="gallery-item"
        :class="{ selected: currentPreviewImage?.id === image.id }"
        @click="showImagePreview(image)"
      >
        <img :src="image.thumbnail_path || image.filepath" :alt="image.filename || `image-${image.id}`" loading="lazy" />
        <div class="overlay">
          <el-icon><ZoomIn /></el-icon>
          <span>预览与调色</span>
        </div>
      </article>
    </div>

    <div v-else class="empty-state">
      <el-icon><Picture /></el-icon>
      <h3>暂无可展示内容</h3>
      <p>请先创建作品集并上传图片后再进行展示。</p>
    </div>

    <el-dialog
      v-model="showPreviewDialog"
      title="图片预览与 AI 调整"
      width="min(1200px, 96vw)"
      class="preview-dialog"
      :lock-scroll="false"
      :close-on-click-modal="true"
    >
      <div class="preview-layout">
        <div class="preview-stage">
          <div v-if="currentPreviewImage" class="preview-image-wrap">
            <img
              :src="processedImageUrl || currentPreviewImage.filepath"
              alt="preview"
              class="preview-image"
              :class="{ processing: isProcessing }"
              :style="imageTransformStyle"
              @wheel="handleImageWheel"
              @mousedown="startImageDrag"
              @mousemove="handleImageDrag"
              @mouseup="endImageDrag"
              @mouseleave="endImageDrag"
            />

            <div v-if="isProcessing" class="processing-mask">
              <el-icon class="spin"><Loading /></el-icon>
              <span>正在处理图片...</span>
            </div>
          </div>

          <div class="zoom-toolbar">
            <el-button-group>
              <el-button @click="zoomOut" :disabled="imageScale <= 0.5">
                <el-icon><ZoomOut /></el-icon>
              </el-button>
              <el-button disabled>{{ Math.round(imageScale * 100) }}%</el-button>
              <el-button @click="zoomIn" :disabled="imageScale >= 3">
                <el-icon><ZoomIn /></el-icon>
              </el-button>
              <el-button @click="resetZoom">
                <el-icon><RefreshLeft /></el-icon>
              </el-button>
            </el-button-group>
          </div>
        </div>

        <aside class="ai-panel">
          <header class="ai-header">
            <el-icon><MagicStick /></el-icon>
            <div>
              <h4>AI 调色助手</h4>
              <p>输入目标效果，自动生成参数并预览。</p>
            </div>
          </header>

          <el-input
            v-model="aiInputText"
            type="textarea"
            :rows="4"
            placeholder="例如：整体更亮、增强对比、偏暖电影感、肤色更自然"
            @keydown.enter.ctrl="applyAIAdjustment"
          />

          <div class="ai-actions">
            <el-button type="primary" :loading="isAILoading" class="apply-btn" @click="applyAIAdjustment">
              <el-icon v-if="!isAILoading"><MagicStick /></el-icon>
              {{ isAILoading ? '处理中...' : '应用调整' }}
            </el-button>
            <el-button v-if="processedImageUrl" @click="resetImage">
              <el-icon><RefreshLeft /></el-icon>
              还原
            </el-button>
            <el-button v-if="processedImageUrl" type="success" @click="downloadProcessedImage">
              <el-icon><Download /></el-icon>
              下载
            </el-button>
          </div>

          <div v-if="aiExplanation" class="ai-note">
            <el-icon><InfoFilled /></el-icon>
            <span>{{ aiExplanation }}</span>
          </div>

          <div class="ai-suggestions">
            <span>快捷建议：</span>
            <el-tag v-for="suggestion in aiSuggestions" :key="suggestion" effect="plain" @click="applyQuickSuggestion(suggestion)">
              {{ suggestion }}
            </el-tag>
          </div>

          <div v-if="currentFilterParams" class="params-box">
            <button type="button" class="params-head" @click="showParamsDetail = !showParamsDetail">
              <span>当前参数</span>
              <el-icon :class="{ rotated: showParamsDetail }"><ArrowDown /></el-icon>
            </button>
            <div v-if="showParamsDetail" class="params-grid">
              <div v-for="(value, key) in currentFilterParams" :key="key" class="param-row">
                <span>{{ getFilterParamLabel(key) }}</span>
                <strong>{{ formatParamValue(key, value) }}</strong>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </el-dialog>

    <el-dialog v-model="showQRCodeDialog" title="作品分享二维码" width="420px" class="qrcode-dialog">
      <div class="qrcode-wrap">
        <div v-if="qrcodeDataUrl" class="qrcode-content">
          <img :src="qrcodeDataUrl" alt="qrcode" class="qrcode-image" />
          <p>扫码即可访问该作品集在线展示页面</p>
          <a :href="qrcodeUrl" target="_blank" rel="noopener noreferrer">{{ qrcodeUrl }}</a>
        </div>

        <div v-else class="qrcode-loading">
          <el-icon class="spin"><Loading /></el-icon>
          <span>二维码生成中...</span>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showQRCodeDialog = false">关闭</el-button>
          <el-button type="primary" :disabled="!qrcodeDataUrl" @click="downloadQRCode">
            <el-icon><Download /></el-icon>
            下载二维码
          </el-button>
        </div>
      </template>
    </el-dialog>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref, type CSSProperties } from 'vue'
import { ElMessage } from 'element-plus'
import {
  ArrowDown,
  Download,
  InfoFilled,
  Loading,
  MagicStick,
  Picture,
  RefreshLeft,
  Promotion,
  ZoomIn,
  ZoomOut,
} from '@element-plus/icons-vue'
import { portfolioApi } from '@/api/portfolioApi'
import config from '@/config'
import { errorHandler } from '@/utils/errorHandler'
import { logger } from '@/utils/logger'
import { applyAllFilters, applyBlur } from '@/utils/imageFilters'

interface PortfolioImage {
  id: number
  filename?: string
  filepath: string
  thumbnail_path?: string
}

interface Portfolio {
  id: number
  name: string
  client_name?: string
  shoot_date?: string
  images: PortfolioImage[]
}

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
    default: null,
  },
})

const portfolios = ref<Portfolio[]>([])
const selectedPortfolioId = ref<number | null>(null)
const currentPortfolio = ref<Portfolio | null>(null)

const showPreviewDialog = ref(false)
const currentPreviewImage = ref<PortfolioImage | null>(null)

const aiInputText = ref('')
const isAILoading = ref(false)
const aiExplanation = ref('')
const aiSuggestions = ['整体更亮', '增强对比', '暖色胶片感', '人像清透', '风景增强']

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
  cursor: 'grab',
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
  blur: '模糊',
}

const defaultFilterParams = (): FilterParamsResult => ({
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
})

const formatDate = (value?: string): string => {
  if (!value) {
    return '-'
  }

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}

const getFilterParamLabel = (key: string): string => filterParamLabels[key] || key

const formatParamValue = (key: string, value: number): string => {
  if (key === 'contrast') {
    if (value > 100) {
      return `+${value - 100}`
    }
    if (value < 100) {
      return `-${100 - value}`
    }
    return '0'
  }

  return value > 0 ? `+${value}` : `${value}`
}

const initData = async (): Promise<void> => {
  try {
    const list = await portfolioApi.getPortfolios()
    portfolios.value = Array.isArray(list) ? list : []

    if (!portfolios.value.length) {
      currentPortfolio.value = null
      selectedPortfolioId.value = null
      return
    }

    const preferredId = props.initialPortfolioId ?? portfolios.value[0]?.id ?? null
    selectedPortfolioId.value = preferredId
    await loadPortfolio()
  } catch (error) {
    errorHandler.handleApiError(error, '加载作品集失败')
  }
}

const loadPortfolio = async (): Promise<void> => {
  if (!selectedPortfolioId.value) {
    currentPortfolio.value = null
    return
  }

  try {
    const detail = await portfolioApi.getPortfolioDetail(selectedPortfolioId.value)
    currentPortfolio.value = {
      ...(detail || {}),
      images: Array.isArray(detail?.images) ? detail.images : [],
    }
  } catch (error) {
    errorHandler.handleApiError(error, '加载作品详情失败')
  }
}

const showImagePreview = (image: PortfolioImage): void => {
  currentPreviewImage.value = image
  processedImageUrl.value = ''
  currentFilterParams.value = null
  aiExplanation.value = ''
  aiInputText.value = ''
  showParamsDetail.value = false
  resetZoom()
  showPreviewDialog.value = true
}

const updateImageTransform = (): void => {
  imageTransformStyle.value = {
    transform: `scale(${imageScale.value}) translate(${imageTranslateX.value}px, ${imageTranslateY.value}px)`,
    cursor: isDragging.value ? 'grabbing' : 'grab',
  }
}

const resetZoom = (): void => {
  imageScale.value = 1
  imageTranslateX.value = 0
  imageTranslateY.value = 0
  updateImageTransform()
}

const zoomIn = (): void => {
  if (imageScale.value >= 3) {
    return
  }
  imageScale.value = Math.min(3, imageScale.value + 0.25)
  updateImageTransform()
}

const zoomOut = (): void => {
  if (imageScale.value <= 0.5) {
    return
  }
  imageScale.value = Math.max(0.5, imageScale.value - 0.25)
  updateImageTransform()
}

const handleImageWheel = (event: WheelEvent): void => {
  event.preventDefault()
  const delta = event.deltaY > 0 ? -0.1 : 0.1
  imageScale.value = Math.max(0.5, Math.min(3, imageScale.value + delta))
  updateImageTransform()
}

const startImageDrag = (event: MouseEvent): void => {
  if (imageScale.value <= 1) {
    return
  }

  isDragging.value = true
  dragStartX.value = event.clientX
  dragStartY.value = event.clientY
  dragTranslateX.value = imageTranslateX.value
  dragTranslateY.value = imageTranslateY.value
  updateImageTransform()
}

const handleImageDrag = (event: MouseEvent): void => {
  if (!isDragging.value) {
    return
  }

  const deltaX = (event.clientX - dragStartX.value) / imageScale.value
  const deltaY = (event.clientY - dragStartY.value) / imageScale.value
  imageTranslateX.value = dragTranslateX.value + deltaX
  imageTranslateY.value = dragTranslateY.value + deltaY
  updateImageTransform()
}

const endImageDrag = (): void => {
  if (!isDragging.value) {
    return
  }

  isDragging.value = false
  updateImageTransform()
}

const applyQuickSuggestion = (suggestion: string): void => {
  aiInputText.value = suggestion
  void applyAIAdjustment()
}

const applyAIAdjustment = async (): Promise<void> => {
  if (!currentPreviewImage.value) {
    return
  }

  if (!aiInputText.value.trim()) {
    ElMessage.warning('请先输入调整意图')
    return
  }

  isAILoading.value = true
  aiExplanation.value = ''

  try {
    const apiBase = config.apiBaseUrl.replace('/api', '')
    const response = await fetch(`${apiBase}/api/ai/parse-intent`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: aiInputText.value,
        current_params: currentFilterParams.value || defaultFilterParams(),
        use_ai: false,
      }),
    })

    if (!response.ok) {
      throw new Error('AI 请求失败')
    }

    const data = await response.json()
    if (!data?.params) {
      ElMessage.warning('未识别到可执行参数')
      return
    }

    currentFilterParams.value = data.params as FilterParamsResult
    aiExplanation.value = data.explanation || '已根据你的描述生成参数并应用到图片。'

    await applyFiltersToImage(currentFilterParams.value)
    ElMessage.success('AI 调整已应用')
  } catch (error) {
    logger.error('Failed to apply AI adjustment:', error)
    ElMessage.error('AI 调整失败，请稍后重试')
  } finally {
    isAILoading.value = false
  }
}

const applyFiltersToImage = async (params: FilterParamsResult): Promise<void> => {
  if (!currentPreviewImage.value) {
    return
  }

  isProcessing.value = true

  try {
    const image = new Image()
    image.crossOrigin = 'anonymous'

    await new Promise<void>((resolve, reject) => {
      image.onload = () => resolve()
      image.onerror = () => reject(new Error('图片加载失败'))
      image.src = currentPreviewImage.value!.filepath
    })

    const canvas = document.createElement('canvas')
    canvas.width = image.naturalWidth
    canvas.height = image.naturalHeight

    const context = canvas.getContext('2d')
    if (!context) {
      throw new Error('无法获取 Canvas 上下文')
    }

    context.drawImage(image, 0, 0)
    const sourceData = context.getImageData(0, 0, canvas.width, canvas.height)

    const processedData = applyAllFilters(sourceData, {
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
    })

    context.putImageData(processedData, 0, 0)

    if ((params.blur ?? 0) > 0) {
      const blurCanvas = document.createElement('canvas')
      blurCanvas.width = canvas.width
      blurCanvas.height = canvas.height

      const blurContext = blurCanvas.getContext('2d')
      if (blurContext) {
        blurContext.drawImage(canvas, 0, 0)
        const blurData = blurContext.getImageData(0, 0, canvas.width, canvas.height)
        applyBlur(blurData.data, canvas.width, canvas.height, params.blur)
        blurContext.putImageData(blurData, 0, 0)
        context.drawImage(blurCanvas, 0, 0)
      }
    }

    processedImageUrl.value = canvas.toDataURL('image/png', 1)
  } catch (error) {
    logger.error('Failed to process image:', error)
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
  showParamsDetail.value = false
  ElMessage.success('已恢复原图')
}

const downloadProcessedImage = (): void => {
  if (!processedImageUrl.value || !currentPreviewImage.value) {
    return
  }

  const link = document.createElement('a')
  link.href = processedImageUrl.value
  link.download = `edited_${currentPreviewImage.value.filename || currentPreviewImage.value.id}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)

  ElMessage.success('图片下载成功')
}

const generatePortfolioQRCode = async (): Promise<void> => {
  if (!currentPortfolio.value) {
    return
  }

  try {
    const portfolioId = currentPortfolio.value.id
    const portfolioUrl = `${window.location.origin}/viewer?portfolio_id=${portfolioId}`

    qrcodeUrl.value = portfolioUrl
    qrcodeDataUrl.value = ''
    showQRCodeDialog.value = true

    const apiBase = config.apiBaseUrl.replace('/api', '')
    const response = await fetch(`${apiBase}/api/previews/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        portfolio_id: portfolioId,
        preview_url: portfolioUrl,
      }),
    })

    if (!response.ok) {
      throw new Error('生成二维码失败')
    }

    const data = await response.json()
    qrcodeDataUrl.value = data.qr_code
  } catch (error) {
    logger.error('Failed to generate qrcode:', error)
    errorHandler.handleApiError(error, '二维码生成失败')
  }
}

const downloadQRCode = (): void => {
  if (!qrcodeDataUrl.value || !currentPortfolio.value) {
    return
  }

  const link = document.createElement('a')
  link.href = qrcodeDataUrl.value
  link.download = `portfolio_${currentPortfolio.value.id}_qrcode.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(() => {
  void initData()
})
</script>

<style scoped>
.portfolio-viewer {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.control-card {
  border: 1px solid var(--pm-border);
  border-radius: var(--pm-radius-md);
  background:
    radial-gradient(circle at 100% 0%, rgba(15, 124, 207, 0.12), transparent 42%),
    var(--pm-surface);
  box-shadow: var(--pm-shadow-1);
  padding: 18px;
  display: grid;
  gap: 14px;
}

.control-head h2 {
  color: var(--pm-text);
  font-size: 24px;
}

.control-head p {
  margin-top: 6px;
  color: var(--pm-text-soft);
  font-size: 13px;
}

.control-actions {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.portfolio-select {
  min-width: 260px;
}

.share-btn {
  border: 0;
  border-radius: 12px;
  font-weight: 700;
  height: 40px;
  background: linear-gradient(128deg, #0f7ccf, #13b5a8);
}

.meta-strip {
  border: 1px solid var(--pm-border);
  border-radius: 12px;
  background: #f4f9ff;
  padding: 12px 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px 14px;
}

.meta-strip span {
  color: #30577e;
  font-size: 12px;
  font-weight: 700;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}

.gallery-item {
  position: relative;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid #d5e5f4;
  box-shadow: 0 10px 24px rgba(17, 37, 61, 0.1);
  aspect-ratio: 4 / 3;
  cursor: pointer;
  transition: transform 0.24s ease, box-shadow 0.24s ease;
}

.gallery-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 18px 30px rgba(17, 37, 61, 0.16);
}

.gallery-item.selected {
  border-color: #1493dc;
  box-shadow: 0 0 0 3px rgba(20, 147, 220, 0.2), 0 18px 30px rgba(17, 37, 61, 0.16);
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #ffffff;
  background: linear-gradient(to top, rgba(8, 24, 40, 0.72), rgba(8, 24, 40, 0.2));
  opacity: 0;
  transition: opacity 0.2s ease;
}

.gallery-item:hover .overlay {
  opacity: 1;
}

.overlay .el-icon {
  font-size: 24px;
}

.overlay span {
  font-size: 12px;
  font-weight: 700;
}

.empty-state {
  border: 1px dashed #bfd4e6;
  border-radius: 14px;
  background: #f8fcff;
  color: #68839d;
  padding: 34px;
  text-align: center;
}

.empty-state .el-icon {
  font-size: 42px;
}

.empty-state h3 {
  margin-top: 10px;
  color: #36587b;
  font-size: 18px;
}

.empty-state p {
  margin-top: 6px;
  font-size: 13px;
}

.preview-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 14px;
  min-height: 540px;
}

.preview-stage {
  position: relative;
  border: 1px solid #d7e7f5;
  border-radius: 14px;
  background: #f6f9fc;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-image-wrap {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  position: relative;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  user-select: none;
  -webkit-user-drag: none;
  transition: opacity 0.2s ease;
}

.preview-image.processing {
  opacity: 0.5;
}

.zoom-toolbar {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 10px;
  padding: 4px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 10px 26px rgba(17, 37, 61, 0.2);
}

.processing-mask {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.72);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #234e77;
}

.spin {
  animation: spin 1s linear infinite;
}

.ai-panel {
  border: 1px solid #d7e7f5;
  border-radius: 14px;
  background: linear-gradient(165deg, #f8fbff, #f2f8ff);
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ai-header {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.ai-header .el-icon {
  margin-top: 2px;
  color: #0f7ccf;
  font-size: 20px;
}

.ai-header h4 {
  color: var(--pm-text);
  font-size: 16px;
}

.ai-header p {
  margin-top: 4px;
  color: var(--pm-text-soft);
  font-size: 12px;
}

.ai-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.apply-btn {
  border: 0;
  border-radius: 10px;
  font-weight: 700;
  background: linear-gradient(130deg, #0f7ccf, #17a4cf);
}

.ai-note {
  border: 1px solid #c7e5d8;
  border-radius: 10px;
  background: #eefbf4;
  color: #2f7b58;
  padding: 10px;
  display: flex;
  gap: 8px;
  font-size: 12px;
  line-height: 1.6;
}

.ai-suggestions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
}

.ai-suggestions span {
  color: #597895;
  font-size: 12px;
  font-weight: 700;
}

.ai-suggestions :deep(.el-tag) {
  cursor: pointer;
}

.params-box {
  border: 1px solid #d7e7f5;
  border-radius: 10px;
  background: #ffffff;
  overflow: hidden;
}

.params-head {
  width: 100%;
  border: 0;
  background: #f4f9ff;
  color: #35597f;
  font-weight: 700;
  font-size: 12px;
  padding: 10px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.params-head .el-icon {
  transition: transform 0.2s ease;
}

.params-head .el-icon.rotated {
  transform: rotate(180deg);
}

.params-grid {
  padding: 10px 12px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.param-row {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  color: #486685;
  font-size: 12px;
}

.param-row strong {
  color: #1d456d;
}

.qrcode-wrap {
  min-height: 280px;
  display: grid;
  place-items: center;
}

.qrcode-content {
  text-align: center;
}

.qrcode-image {
  width: 280px;
  height: 280px;
  border-radius: 14px;
  border: 1px solid #d7e7f5;
  box-shadow: 0 12px 26px rgba(17, 37, 61, 0.14);
}

.qrcode-content p {
  margin-top: 14px;
  color: #4a6987;
  font-size: 13px;
}

.qrcode-content a {
  margin-top: 8px;
  display: block;
  color: #0f7ccf;
  font-size: 12px;
  word-break: break-all;
}

.qrcode-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #42698e;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

:deep(.preview-dialog .el-dialog),
:deep(.qrcode-dialog .el-dialog) {
  border-radius: 18px;
}

:deep(.preview-dialog .el-dialog__header),
:deep(.qrcode-dialog .el-dialog__header) {
  border-bottom: 1px solid #e2edf7;
  margin-right: 0;
  padding: 18px 20px;
}

:deep(.preview-dialog .el-dialog__body),
:deep(.qrcode-dialog .el-dialog__body) {
  padding: 18px 20px;
}

@media (max-width: 980px) {
  .preview-layout {
    grid-template-columns: 1fr;
  }

  .preview-stage {
    min-height: 360px;
  }
}

@media (max-width: 760px) {
  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }

  .portfolio-select {
    min-width: 100%;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
