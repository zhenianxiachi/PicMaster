<template>
  <div class="filter-editor">
    <div class="editor-main">
      <section class="preview-stage">
        <div
          ref="previewContainerRef"
          class="preview-canvas-wrap"
          :class="{ movable: previewScale > 1, dragging: isDragging }"
          @wheel.prevent="handlePreviewWheel"
          @pointerdown="startPreviewDrag"
        >
          <canvas ref="canvasRef" class="preview-canvas" :style="previewCanvasStyle"></canvas>
          <div class="preview-toolbar">
            <el-button class="toolbar-btn" :disabled="previewScale <= minPreviewScale" @click="zoomOut">
              <el-icon><ZoomOut /></el-icon>
            </el-button>
            <span class="zoom-text">{{ Math.round(previewScale * 100) }}%</span>
            <el-button class="toolbar-btn" :disabled="previewScale >= maxPreviewScale" @click="zoomIn">
              <el-icon><ZoomIn /></el-icon>
            </el-button>
            <el-button class="toolbar-btn" @click="resetPreviewView">
              <el-icon><RefreshLeft /></el-icon>
            </el-button>
          </div>
          <div v-if="isLoading" class="loading-mask">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <span>图片处理中...</span>
          </div>
        </div>
      </section>

      <aside class="side-panel" :class="{ collapsed: !isPanelExpanded }">
        <header class="panel-header">
          <h3>专业调色面板</h3>
          <p>参数实时预览，可直接导出或保存至作品集</p>
        </header>

        <section class="ai-card">
          <div class="ai-title">
            <el-icon><MagicStick /></el-icon>
            <span>AI 智能调整</span>
          </div>
          <div class="ai-input-row">
            <el-input
              v-model="aiInputText"
              type="textarea"
              :rows="2"
              placeholder="例如：提亮一点、增加对比、冷暖平衡、电影感"
              class="ai-textarea"
              @keydown.enter.ctrl="applyAIAdjustment"
            />
            <el-button type="primary" class="ai-btn" :loading="isAILoading" @click="applyAIAdjustment">应用</el-button>
          </div>
          <div v-if="aiExplanation" class="ai-result">
            <el-icon><InfoFilled /></el-icon>
            <span>{{ aiExplanation }}</span>
          </div>
          <div class="suggestions">
            <span class="label">快捷建议：</span>
            <el-tag v-for="item in aiSuggestions" :key="item" class="tag" effect="plain" @click="setSuggestion(item)">
              {{ item }}
            </el-tag>
          </div>
        </section>

        <section class="slider-list">
          <article v-for="item in filterItems" :key="item.key" class="slider-item">
            <div class="slider-head">
              <span>{{ item.config.label }}</span>
              <strong>{{ filterParams[item.key] }}</strong>
            </div>
            <el-slider
              v-model="filterParams[item.key]"
              :min="item.config.min"
              :max="item.config.max"
              :step="item.config.step"
              @input="debouncedApplyPreview"
            />
          </article>
        </section>

        <section class="hsl-section">
          <HSLEditor @applyHSL="applyHSLValues" />
        </section>

        <section class="actions">
          <el-button class="btn-soft" @click="resetFilters">重置</el-button>
          <el-button class="btn-soft" @click="showSaveToPortfolioDialog = true">保存到作品集</el-button>
          <el-button type="primary" class="btn-primary" @click="showSaveOptionsDialog = true">保存图片</el-button>
        </section>

        <section class="quota-card">
          <el-icon><InfoFilled /></el-icon>
          <span>{{ usageStore.usageSummary.label }} · 游客试用 {{ usageStore.trialLimit }} 次，免费账号每日 {{ usageStore.dailyLimit }} 次。</span>
        </section>
      </aside>
    </div>

    <el-dialog v-model="showSaveOptionsDialog" title="保存选项" width="430px">
      <div class="save-options">
        <div class="save-option" @click="saveImage('lossless')">
          <strong>无损保存</strong>
          <p>PNG 格式，适合后续再编辑。</p>
        </div>
        <div class="save-option" @click="saveImage('compressed')">
          <strong>压缩保存</strong>
          <p>JPEG 格式，文件更轻量，适合快速交付。</p>
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="showSaveToPortfolioDialog" title="保存到作品集" width="500px">
      <div class="portfolio-list">
        <article
          v-for="portfolio in portfolios"
          :key="portfolio.id"
          class="portfolio-item"
          :class="{ active: selectedSavePortfolioId === portfolio.id }"
          @click="selectSavePortfolio(portfolio.id)"
        >
          <strong>{{ portfolio.name }}</strong>
          <p>{{ portfolio.client_name }} · {{ portfolio.image_count || 0 }} 张图片</p>
        </article>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showSaveToPortfolioDialog = false">取消</el-button>
          <el-button type="primary" :disabled="!selectedSavePortfolioId" @click="saveToPortfolio">确认保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch, onMounted, onUnmounted, type Ref } from 'vue'
import { ElMessage } from 'element-plus'
import { InfoFilled, Loading, MagicStick, RefreshLeft, ZoomIn, ZoomOut } from '@element-plus/icons-vue'
import HSLEditor from '../../components/HSLEditor.vue'
import { portfolioApi } from '../../api/portfolioApi.js'
import { applyAllFilters, applyBlur, type FilterParams as CustomFilterParams } from '../../utils/imageFilters'
import { useUsageStore } from '../../store/usage'
import config from '../../config'

interface FilterEditorProps {
  imageUrl?: string | null
  isPanelExpanded?: boolean
}

interface PortfolioItem {
  id: number
  name: string
  client_name: string
  image_count?: number
}

type SaveMode = 'lossless' | 'compressed'

interface FilterConfigItem {
  label: string
  min: number
  max: number
  step: number
}

interface LocalFilterParams {
  brightness: number
  contrast: number
  saturation: number
  hue: number
  blur: number
  sharpness: number
  exposure: number
  highlights: number
  shadows: number
  temperature: number
  tint: number
  vignette: number
  clarity: number
}

interface HSLValue {
  hue: number
  saturation: number
  lightness: number
}

type HSLData = Record<string, HSLValue>

type FilterKey = keyof LocalFilterParams

const props = withDefaults(defineProps<FilterEditorProps>(), {
  imageUrl: null,
  isPanelExpanded: true,
})

const usageStore = useUsageStore()

const canvasRef: Ref<HTMLCanvasElement | null> = ref(null)
const previewContainerRef: Ref<HTMLDivElement | null> = ref(null)
const originalImageElement: Ref<HTMLImageElement | null> = ref(null)
const originalWidth = ref(0)
const originalHeight = ref(0)
const isLoading = ref(false)
const isAILoading = ref(false)
const minPreviewScale = 0.5
const maxPreviewScale = 4
const previewScale = ref(1)
const previewOffsetX = ref(0)
const previewOffsetY = ref(0)
const isDragging = ref(false)
const activePointerId = ref<number | null>(null)
const dragStartX = ref(0)
const dragStartY = ref(0)
const dragOriginOffsetX = ref(0)
const dragOriginOffsetY = ref(0)

const previewCanvasStyle = computed(() => ({
  transform: `translate(${previewOffsetX.value}px, ${previewOffsetY.value}px) scale(${previewScale.value})`,
  transformOrigin: 'center center',
  transition: isDragging.value ? 'none' : 'transform 0.08s ease-out',
}))

const showSaveOptionsDialog = ref(false)
const showSaveToPortfolioDialog = ref(false)
const selectedSavePortfolioId = ref<number | null>(null)
const portfolios = ref<PortfolioItem[]>([])

const aiInputText = ref('')
const aiExplanation = ref('')
const aiSuggestions = ['更亮一点', '增加对比度', '冷暖平衡', '电影质感', '人像优化', '风景增强']

const createDefaultFilterParams = (): LocalFilterParams => ({
  brightness: 0,
  contrast: 100,
  saturation: 100,
  hue: 0,
  blur: 0,
  sharpness: 0,
  exposure: 0,
  highlights: 0,
  shadows: 0,
  temperature: 0,
  tint: 0,
  vignette: 0,
  clarity: 0,
})

const createDefaultHslParams = (): HSLData => ({
  red: { hue: 0, saturation: 0, lightness: 0 },
  orange: { hue: 0, saturation: 0, lightness: 0 },
  yellow: { hue: 0, saturation: 0, lightness: 0 },
  green: { hue: 0, saturation: 0, lightness: 0 },
  cyan: { hue: 0, saturation: 0, lightness: 0 },
  blue: { hue: 0, saturation: 0, lightness: 0 },
  purple: { hue: 0, saturation: 0, lightness: 0 },
  magenta: { hue: 0, saturation: 0, lightness: 0 },
})

const filterParams = reactive<LocalFilterParams>(createDefaultFilterParams())
const hslParams = reactive<HSLData>(createDefaultHslParams())

const filterConfig: Record<FilterKey, FilterConfigItem> = {
  brightness: { label: '亮度', min: -100, max: 100, step: 1 },
  contrast: { label: '对比度', min: 0, max: 200, step: 1 },
  saturation: { label: '饱和度', min: -100, max: 100, step: 1 },
  hue: { label: '色相', min: 0, max: 360, step: 5 },
  sharpness: { label: '锐化', min: -50, max: 50, step: 1 },
  exposure: { label: '曝光', min: -100, max: 100, step: 1 },
  highlights: { label: '高光', min: -100, max: 100, step: 1 },
  shadows: { label: '阴影', min: -100, max: 100, step: 1 },
  temperature: { label: '色温', min: -50, max: 50, step: 1 },
  tint: { label: '色调', min: -50, max: 50, step: 1 },
  vignette: { label: '暗角', min: 0, max: 100, step: 1 },
  clarity: { label: '清晰度', min: -100, max: 100, step: 1 },
  blur: { label: '模糊', min: 0, max: 20, step: 1 },
}

const filterItems: Array<{ key: FilterKey; config: FilterConfigItem }> = (
  Object.entries(filterConfig) as Array<[FilterKey, FilterConfigItem]>
).map(([key, item]) => ({ key, config: item }))

let applyTimer: number | null = null

const cloneHslParams = (): HSLData => JSON.parse(JSON.stringify(hslParams)) as HSLData

const toCustomParams = (): CustomFilterParams => ({
  brightness: filterParams.brightness,
  contrast: filterParams.contrast,
  saturation: filterParams.saturation,
  hue: filterParams.hue,
  blur: filterParams.blur,
  sharpness: filterParams.sharpness,
  exposure: filterParams.exposure,
  highlights: filterParams.highlights,
  shadows: filterParams.shadows,
  temperature: filterParams.temperature,
  tint: filterParams.tint,
  vignette: filterParams.vignette,
  clarity: filterParams.clarity,
  hsl: cloneHslParams(),
})

const clampScale = (value: number): number => {
  return Math.max(minPreviewScale, Math.min(maxPreviewScale, value))
}

const resetPreviewTransform = (): void => {
  previewScale.value = 1
  previewOffsetX.value = 0
  previewOffsetY.value = 0
  isDragging.value = false
  activePointerId.value = null
  window.removeEventListener('pointermove', handlePreviewDrag)
  window.removeEventListener('pointerup', endPreviewDrag)
  window.removeEventListener('pointercancel', endPreviewDrag)
}

const getPreviewRect = (): { width: number; height: number; left: number; top: number } | null => {
  if (!previewContainerRef.value || !originalWidth.value || !originalHeight.value) {
    return null
  }
  const containerWidth = previewContainerRef.value.clientWidth
  const containerHeight = previewContainerRef.value.clientHeight
  if (!containerWidth || !containerHeight) {
    return null
  }

  const scale = Math.min(containerWidth / originalWidth.value, containerHeight / originalHeight.value, 1)
  const width = Math.max(1, Math.round(originalWidth.value * scale))
  const height = Math.max(1, Math.round(originalHeight.value * scale))
  const left = Math.round((containerWidth - width) / 2)
  const top = Math.round((containerHeight - height) / 2)
  return { width, height, left, top }
}

const clampPreviewOffset = (): void => {
  // Keep unrestricted panning to match legacy editor behavior.
}

const applyZoom = (nextScale: number, anchorX?: number, anchorY?: number): void => {
  const normalizedScale = clampScale(nextScale)
  const currentScale = previewScale.value
  if (normalizedScale === currentScale) {
    return
  }

  const container = previewContainerRef.value
  if (container && currentScale > 0) {
    const centerX = container.clientWidth / 2
    const centerY = container.clientHeight / 2
    const pointX = anchorX ?? centerX
    const pointY = anchorY ?? centerY
    const ratio = normalizedScale / currentScale

    previewOffsetX.value = previewOffsetX.value * ratio + (pointX - centerX) * (1 - ratio)
    previewOffsetY.value = previewOffsetY.value * ratio + (pointY - centerY) * (1 - ratio)
  }

  previewScale.value = normalizedScale
  clampPreviewOffset()
}

const zoomIn = (): void => {
  applyZoom(previewScale.value + 0.25)
}

const zoomOut = (): void => {
  applyZoom(previewScale.value - 0.25)
}

const resetPreviewView = (): void => {
  resetPreviewTransform()
}

const handlePreviewWheel = (event: WheelEvent): void => {
  const container = previewContainerRef.value
  if (!container) {
    return
  }

  const rect = container.getBoundingClientRect()
  const anchorX = event.clientX - rect.left
  const anchorY = event.clientY - rect.top
  const delta = event.deltaY > 0 ? -0.1 : 0.1
  applyZoom(previewScale.value + delta, anchorX, anchorY)
}

const startPreviewDrag = (event: PointerEvent): void => {
  if (event.button !== 0) {
    return
  }

  const container = previewContainerRef.value
  if (!container) {
    return
  }

  isDragging.value = true
  activePointerId.value = event.pointerId
  dragStartX.value = event.clientX
  dragStartY.value = event.clientY
  dragOriginOffsetX.value = previewOffsetX.value
  dragOriginOffsetY.value = previewOffsetY.value

  try {
    container.setPointerCapture(event.pointerId)
  } catch {
    // ignore capture failure
  }

  window.addEventListener('pointermove', handlePreviewDrag)
  window.addEventListener('pointerup', endPreviewDrag)
  window.addEventListener('pointercancel', endPreviewDrag)
  event.preventDefault()
}

const handlePreviewDrag = (event: PointerEvent): void => {
  if (!isDragging.value) {
    return
  }
  if (activePointerId.value !== null && event.pointerId !== activePointerId.value) {
    return
  }

  previewOffsetX.value = dragOriginOffsetX.value + (event.clientX - dragStartX.value)
  previewOffsetY.value = dragOriginOffsetY.value + (event.clientY - dragStartY.value)
  clampPreviewOffset()
  event.preventDefault()
}

const endPreviewDrag = (event?: PointerEvent): void => {
  if (event && activePointerId.value !== null && event.pointerId !== activePointerId.value) {
    return
  }

  const pointerId = activePointerId.value
  const container = previewContainerRef.value

  if (container && pointerId !== null) {
    try {
      if (container.hasPointerCapture(pointerId)) {
        container.releasePointerCapture(pointerId)
      }
    } catch {
      // ignore release failure
    }
  }

  isDragging.value = false
  activePointerId.value = null
  window.removeEventListener('pointermove', handlePreviewDrag)
  window.removeEventListener('pointerup', endPreviewDrag)
  window.removeEventListener('pointercancel', endPreviewDrag)
}

const createProcessedCanvas = (width: number, height: number): HTMLCanvasElement | null => {
  if (!originalImageElement.value) {
    return null
  }
  const tempCanvas = document.createElement('canvas')
  tempCanvas.width = width
  tempCanvas.height = height
  const tempCtx = tempCanvas.getContext('2d')
  if (!tempCtx) {
    return null
  }

  tempCtx.drawImage(originalImageElement.value, 0, 0, width, height)
  const imageData = tempCtx.getImageData(0, 0, width, height)
  const processedData = applyAllFilters(imageData, toCustomParams())
  tempCtx.putImageData(processedData, 0, 0)

  if (filterParams.blur > 0) {
    const blurData = tempCtx.getImageData(0, 0, width, height)
    applyBlur(blurData.data, width, height, filterParams.blur)
    tempCtx.putImageData(blurData, 0, 0)
  }

  return tempCanvas
}

const renderPreview = (): void => {
  if (!canvasRef.value || !previewContainerRef.value || !originalImageElement.value) {
    return
  }

  const baseRect = getPreviewRect()
  if (!baseRect) {
    return
  }

  const canvas = canvasRef.value
  canvas.width = previewContainerRef.value.clientWidth
  canvas.height = previewContainerRef.value.clientHeight
  const ctx = canvas.getContext('2d')
  if (!ctx) {
    return
  }

  clampPreviewOffset()

  ctx.clearRect(0, 0, canvas.width, canvas.height)
  const processed = createProcessedCanvas(baseRect.width, baseRect.height)
  if (!processed) {
    return
  }

  ctx.imageSmoothingEnabled = true
  ctx.imageSmoothingQuality = 'high'
  ctx.drawImage(processed, baseRect.left, baseRect.top)
}

const debouncedApplyPreview = (): void => {
  if (applyTimer) {
    window.clearTimeout(applyTimer)
  }
  applyTimer = window.setTimeout(() => {
    renderPreview()
  }, 40)
}

const loadImageToCanvas = (url: string): void => {
  if (!url) {
    return
  }
  isLoading.value = true
  const img = new Image()
  img.crossOrigin = 'anonymous'

  img.onload = () => {
    originalImageElement.value = img
    originalWidth.value = img.naturalWidth
    originalHeight.value = img.naturalHeight
    resetPreviewTransform()
    isLoading.value = false
    renderPreview()
  }

  img.onerror = () => {
    isLoading.value = false
    ElMessage.error('图片加载失败，请更换图片后重试')
  }

  img.src = url
}

const fetchPortfolios = async (): Promise<void> => {
  try {
    const list = await portfolioApi.getPortfolios()
    portfolios.value = Array.isArray(list) ? (list as PortfolioItem[]) : []
  } catch {
    ElMessage.error('获取作品集列表失败')
  }
}

const resetFilters = (): void => {
  Object.assign(filterParams, createDefaultFilterParams())
  Object.assign(hslParams, createDefaultHslParams())
  aiExplanation.value = ''
  renderPreview()
}

const applyHSLValues = (values: HSLData): void => {
  Object.assign(hslParams, values)
  debouncedApplyPreview()
}

const setSuggestion = (suggestion: string): void => {
  aiInputText.value = suggestion
  void applyAIAdjustment()
}

const applyAIAdjustment = async (): Promise<void> => {
  if (!aiInputText.value.trim()) {
    ElMessage.warning('请输入要调整的描述')
    return
  }
  if (!usageStore.consume('ai-adjust')) {
    return
  }

  isAILoading.value = true
  aiExplanation.value = ''

  try {
    const apiBase = config.apiBaseUrl.replace('/api', '')
    const response = await fetch(`${apiBase}/api/ai/parse-intent`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: aiInputText.value,
        current_params: toCustomParams(),
        use_ai: false,
      }),
    })

    if (!response.ok) {
      throw new Error('request failed')
    }

    const data = (await response.json()) as {
      params?: Partial<LocalFilterParams>
      explanation?: string
    }

    if (data.params) {
      Object.assign(filterParams, {
        ...createDefaultFilterParams(),
        ...data.params,
      })
      aiExplanation.value = data.explanation || '已根据描述自动调整参数'
      renderPreview()
      ElMessage.success('AI 调整已应用')
    }
  } catch {
    ElMessage.error('AI 调整失败，请稍后再试')
  } finally {
    isAILoading.value = false
  }
}

const canvasToBlob = (canvas: HTMLCanvasElement, mode: SaveMode): Promise<Blob | null> =>
  new Promise(resolve => {
    if (mode === 'lossless') {
      canvas.toBlob(blob => resolve(blob), 'image/png', 1)
      return
    }
    canvas.toBlob(blob => resolve(blob), 'image/jpeg', 0.92)
  })

const saveImage = async (mode: SaveMode): Promise<void> => {
  showSaveOptionsDialog.value = false
  if (!usageStore.consume('export-image')) {
    return
  }
  const processedCanvas = createProcessedCanvas(originalWidth.value, originalHeight.value)
  if (!processedCanvas) {
    ElMessage.error('图片处理失败')
    return
  }

  const blob = await canvasToBlob(processedCanvas, mode)
  if (!blob) {
    ElMessage.error('保存失败，请重试')
    return
  }
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `edited_image_${Date.now()}.${mode === 'lossless' ? 'png' : 'jpg'}`
  link.click()
  URL.revokeObjectURL(url)
  ElMessage.success('图片已保存到本地')
}

const selectSavePortfolio = (portfolioId: number): void => {
  selectedSavePortfolioId.value = portfolioId
}

const saveToPortfolio = async (): Promise<void> => {
  if (!selectedSavePortfolioId.value) {
    return
  }
  if (!usageStore.consume('save-portfolio')) {
    return
  }

  const processedCanvas = createProcessedCanvas(originalWidth.value, originalHeight.value)
  if (!processedCanvas) {
    ElMessage.error('图片处理失败')
    return
  }
  const blob = await canvasToBlob(processedCanvas, 'lossless')
  if (!blob) {
    ElMessage.error('保存失败，请重试')
    return
  }

  try {
    const formData = new FormData()
    formData.append('file', blob, `edited_image_${Date.now()}.png`)
    await portfolioApi.uploadImageToPortfolio(selectedSavePortfolioId.value, formData)
    showSaveToPortfolioDialog.value = false
    selectedSavePortfolioId.value = null
    ElMessage.success('已保存到作品集')
  } catch {
    ElMessage.error('保存到作品集失败')
  }
}

const handleResize = (): void => {
  clampPreviewOffset()
  renderPreview()
}

watch(
  () => props.imageUrl,
  newUrl => {
    if (newUrl) {
      loadImageToCanvas(newUrl)
    }
  },
  { immediate: true }
)

onMounted(() => {
  window.addEventListener('resize', handleResize)
  void fetchPortfolios()
})

onUnmounted(() => {
  endPreviewDrag()
  window.removeEventListener('resize', handleResize)
  if (applyTimer) {
    window.clearTimeout(applyTimer)
  }
})
</script>

<style scoped>
.filter-editor {
  width: 100%;
  height: 100%;
}

.editor-main {
  position: relative;
  height: calc(100vh - 70px);
}

.preview-stage {
  height: 100%;
  background:
    linear-gradient(160deg, rgba(15, 124, 207, 0.08), rgba(19, 181, 168, 0.08)),
    #eef4fa;
}

.preview-canvas-wrap {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  user-select: none;
  touch-action: none;
  cursor: default;
}

.preview-canvas-wrap.movable {
  cursor: grab;
}

.preview-canvas-wrap.dragging {
  cursor: grabbing;
}

.preview-canvas {
  width: 100%;
  height: 100%;
  display: block;
  pointer-events: none;
  will-change: transform;
}

.preview-toolbar {
  position: absolute;
  left: 50%;
  bottom: 16px;
  transform: translateX(-50%);
  border: 1px solid #c7daec;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 10px 20px rgba(17, 37, 61, 0.16);
  padding: 6px 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 4;
}

.toolbar-btn {
  border: 1px solid #c6d9ea;
  background: #ffffff;
  width: 32px;
  height: 32px;
  padding: 0;
}

.zoom-text {
  min-width: 52px;
  text-align: center;
  color: #35597d;
  font-size: 12px;
  font-weight: 700;
}

.loading-mask {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  gap: 10px;
  color: #23496f;
  background: rgba(255, 255, 255, 0.8);
}

.loading-icon {
  font-size: 42px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.side-panel {
  position: absolute;
  right: 0;
  top: 0;
  width: 400px;
  height: 100%;
  overflow-y: auto;
  border-left: 1px solid var(--pm-border);
  background: #ffffff;
  padding: 18px;
  transition: transform 0.25s ease;
  box-shadow: -12px 0 30px rgba(17, 37, 61, 0.08);
}

.side-panel.collapsed {
  transform: translateX(100%);
}

.panel-header h3 {
  font-size: 24px;
  color: var(--pm-text);
}

.panel-header p {
  margin-top: 6px;
  color: var(--pm-text-soft);
  font-size: 12px;
}

.ai-card {
  margin-top: 16px;
  border: 1px solid var(--pm-border);
  border-radius: 14px;
  background: #f8fbff;
  padding: 12px;
}

.ai-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 700;
  color: #1e4d78;
}

.ai-input-row {
  margin-top: 8px;
  display: flex;
  gap: 8px;
}

.ai-textarea {
  flex: 1;
}

.ai-btn {
  border-radius: 10px;
  border: 0;
  background: linear-gradient(125deg, var(--pm-primary), #17a4cf);
}

.ai-result {
  margin-top: 8px;
  border: 1px solid #b9e3d6;
  border-radius: 10px;
  background: #edfef7;
  padding: 8px;
  color: #167f5f;
  display: flex;
  align-items: flex-start;
  gap: 6px;
  font-size: 12px;
}

.suggestions {
  margin-top: 8px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
}

.suggestions .label {
  color: #627b95;
  font-size: 12px;
}

.tag {
  cursor: pointer;
}

.slider-list {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hsl-section {
  margin-top: 14px;
}

.slider-item {
  border: 1px solid var(--pm-border);
  border-radius: 12px;
  background: #ffffff;
  padding: 10px;
}

.slider-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.slider-head span {
  color: #274d74;
  font-size: 13px;
  font-weight: 700;
}

.slider-head strong {
  color: #5b7691;
  font-size: 12px;
}

.actions {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.btn-soft {
  border: 1px solid #c6d9ea;
}

.btn-primary {
  border: 0;
  background: linear-gradient(125deg, var(--pm-primary), #17a4cf);
}

.quota-card {
  margin-top: 12px;
  border: 1px solid #c7dcec;
  border-radius: 12px;
  background: #edf7ff;
  padding: 10px;
  color: #315574;
  font-size: 12px;
  line-height: 1.55;
  display: flex;
  align-items: flex-start;
  gap: 6px;
}

.save-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.save-option {
  border: 1px solid var(--pm-border);
  border-radius: 12px;
  padding: 14px;
  cursor: pointer;
}

.save-option:hover {
  background: #f4f9ff;
  border-color: #abcbe4;
}

.save-option strong {
  color: var(--pm-text);
  font-size: 15px;
}

.save-option p {
  margin-top: 6px;
  color: #647f9a;
  font-size: 12px;
}

.portfolio-list {
  max-height: 300px;
  overflow-y: auto;
}

.portfolio-item {
  border: 1px solid var(--pm-border);
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 8px;
  background: #f9fcff;
  cursor: pointer;
}

.portfolio-item:hover {
  border-color: #b7d5eb;
}

.portfolio-item.active {
  border-color: var(--pm-primary);
  background: #e9f6ff;
}

.portfolio-item strong {
  color: var(--pm-text);
  font-size: 14px;
}

.portfolio-item p {
  margin-top: 4px;
  color: #667f9b;
  font-size: 12px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

@media (max-width: 760px) {
  .editor-main {
    height: auto;
    min-height: calc(100vh - 108px);
  }

  .preview-stage {
    height: 52vh;
  }

  .side-panel {
    position: relative;
    width: 100%;
    height: auto;
    border-left: 0;
    border-top: 1px solid var(--pm-border);
    box-shadow: none;
  }

  .side-panel.collapsed {
    transform: none;
  }
}
</style>
