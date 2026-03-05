<template>
  <div class="filter-editor-container">
    <div class="editor-main">
      <div class="large-preview-section">
        <div class="preview-container" @wheel="handleWheel">
          <canvas
            ref="canvasRef"
            class="preview-canvas"
          ></canvas>

          <div v-if="isLoading" class="loading-overlay">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <span class="loading-text">加载中...</span>
          </div>
        </div>
      </div>

      <div class="filter-panel" :class="{ collapsed: !isPanelExpanded }">
        <h3 class="panel-title">
          <el-icon><MagicStick /></el-icon>
          滤镜参数
        </h3>

        <!-- 滤镜预览区域 -->
        <div class="filter-preview-section">
          <div
            v-for="preset in filterPresets"
            :key="preset.name"
            @click="applyPreset(preset)"
            class="filter-preview-item"
            :class="{ active: isPresetActive(preset) }"
          >
            <canvas :ref="el => setPreviewCanvasRef(el, preset.name)" class="filter-preview-canvas"></canvas>
            <span class="filter-preview-label">{{ preset.name }}</span>
          </div>
        </div>

        <!-- AI修改意见区域 -->
        <div class="ai-input-section">
          <div class="ai-input-header">
            <el-icon class="ai-icon"><MagicStick /></el-icon>
            <span class="ai-title">AI智能调整</span>
          </div>
          <div class="ai-input-container">
            <el-input
              v-model="aiInputText"
              type="textarea"
              :rows="2"
              placeholder="描述您想要的效果，如：让照片更亮一点、增加对比度、调成暖色调、添加电影感..."
              class="ai-textarea"
              @keydown.enter.ctrl="applyAIAdjustment"
            />
            <el-button 
              type="primary" 
              @click="applyAIAdjustment" 
              :loading="isAILoading"
              class="ai-apply-btn"
            >
              <el-icon v-if="!isAILoading"><MagicStick /></el-icon>
              {{ isAILoading ? '处理中...' : '应用' }}
            </el-button>
          </div>
          <div v-if="aiExplanation" class="ai-explanation">
            <el-icon><InfoFilled /></el-icon>
            <span>{{ aiExplanation }}</span>
          </div>
          <div class="ai-suggestions">
            <span class="suggestion-label">快捷建议：</span>
            <el-tag 
              v-for="suggestion in aiSuggestions" 
              :key="suggestion"
              @click="aiInputText = suggestion; applyAIAdjustment()"
              class="suggestion-tag"
              effect="plain"
            >
              {{ suggestion }}
            </el-tag>
          </div>
        </div>

        <div class="filter-controls">
          <div class="filter-item" v-for="(config, key) in filterConfig" :key="key">
            <div class="filter-header">
              <span class="filter-name">{{ config.label }}</span>
              <span class="filter-value">{{ filterParams[key] }}</span>
            </div>
            <el-slider
              v-model="filterParams[key]"
              :min="config.min"
              :max="config.max"
              :step="config.step || 1"
              @input="debouncedApplyFilters"
            />
          </div>
        </div>

        <div class="action-buttons">
          <el-button @click="resetFilters" class="action-btn">重置</el-button>
          <el-button @click="showSaveToPortfolioDialog = true" class="action-btn">
            保存到作品集
          </el-button>
 <el-button type="primary" @click="showSaveOptionsDialog = true" class="action-btn primary">
            保存图片
          </el-button>
        </div>
        
        <!-- HSL高级调节开关 -->
        <div class="hsl-section">
          <div class="hsl-toggle">
            <h4 class="section-title">HSL 高级调节</h4>
            <el-switch v-model="hslEnabled" active-text="开启" inactive-text="关闭" />
          </div>
          <HSLEditor v-if="hslEnabled" ref="hslEditorRef" @apply-h-s-l="applyHSL" />
        </div>
      </div>
    </div>
  
    <!-- 保存选项对话框 -->
    <el-dialog
      v-model="showSaveOptionsDialog"
      title="保存选项"
      width="400px"
      class="save-options-dialog"
    >
      <div class="save-options">
        <div class="option-item" @click="saveImage('lossless')">
          <div class="option-icon">📷</div>
          <div class="option-content">
            <div class="option-title">无损保存</div>
            <div class="option-desc">PNG格式，保留完整画质，文件较大</div>
          </div>
        </div>
        <div class="option-item" @click="saveImage('compressed')">
          <div class="option-icon">📦</div>
          <div class="option-content">
            <div class="option-title">压缩保存</div>
            <div class="option-desc">JPEG格式，文件较小，画质略有损失</div>
          </div>
        </div>
      </div>
    </el-dialog>
  
    <!-- 保存到作品集对话框 -->
    <el-dialog
      v-model="showSaveToPortfolioDialog"
      title="保存到作品集"
      width="500px"
      class="portfolio-dialog"
    >
      <div class="portfolio-selector">
        <div class="portfolio-list">
          <div 
            v-for="portfolio in portfolios" 
            :key="portfolio.id"
            class="portfolio-item"
            :class="{ active: selectedSavePortfolioId === portfolio.id }"
            @click="selectSavePortfolio(portfolio.id)"
          >
            <div class="portfolio-item-content">
              <div class="portfolio-item-title">{{ portfolio.name }}</div>
              <div class="portfolio-item-meta">
                <span>{{ portfolio.client_name }}</span>
                <span>{{ portfolio.image_count || 0 }}张图片</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="dialog-footer">
          <el-button @click="showSaveToPortfolioDialog = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="saveToPortfolio"
            :disabled="!selectedSavePortfolioId"
          >
            确定保存
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick, onUnmounted, type Ref } from 'vue'
import { fabric } from 'fabric'
import { ElMessage } from 'element-plus'
import { MagicStick, Loading, InfoFilled } from '@element-plus/icons-vue'
import { portfolioApi } from '../../api/portfolioApi.js'
import { errorHandler } from '../../utils/errorHandler'
import { logger } from '../../utils/logger'
import { 
  applyAllFilters, 
  applyBlur, 
  type FilterParams as CustomFilterParams 
} from '../../utils/imageFilters'
import config from '../../config'
import HSLEditor from '../../components/HSLEditor.vue'

interface FilterEditorProps {
  imageUrl?: string | null
  isPanelExpanded?: boolean
}

const props = withDefaults(defineProps<FilterEditorProps>(), {
  imageUrl: '',
  isPanelExpanded: true,
})

const emit = defineEmits<{
  back: []
}>()

interface FilterConfigItem {
  label: string
  min: number
  max: number
  step?: number
}

interface FilterConfig {
  [key: string]: FilterConfigItem
}

interface FilterPreset {
  name: string
  params: Record<string, number>
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
  [key: string]: number
}

const canvasRef: Ref<HTMLCanvasElement | null> = ref(null)
const canvas: Ref<fabric.Canvas | null> = ref(null)
const isLoading = ref<boolean>(false)

const originalImageElement: Ref<HTMLImageElement | null> = ref(null)
const originalWidth = ref<number>(0)
const originalHeight = ref<number>(0)

const portfolios = ref<any[]>([])
const showSaveToPortfolioDialog = ref<boolean>(false)
const showSaveOptionsDialog = ref<boolean>(false)
const selectedSavePortfolioId = ref<number | null>(null)

const previewCanvasRefs: Ref<Map<string, HTMLCanvasElement>> = ref(new Map())
const activePresetName: Ref<string> = ref('原图')

const filterConfig: FilterConfig = {
  brightness: { label: '亮度', min: -100, max: 100, step: 1 },
  contrast: { label: '对比度', min: 0, max: 200, step: 1 },
  saturation: { label: '饱和度', min: -100, max: 100, step: 1 },
  hue: { label: '色相', min: 0, max: 360, step: 10 },
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

const filterParams = ref<LocalFilterParams>({
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

const filterPresets: FilterPreset[] = [
  { name: '原图', params: { brightness: 0, contrast: 100, saturation: 100, hue: 0, blur: 0, sharpness: 0, exposure: 0, highlights: 0, shadows: 0, temperature: 0, tint: 0, vignette: 0, clarity: 0 } },
  { name: '清新', params: { brightness: 5, contrast: 105, saturation: 90, hue: 5, blur: 0, sharpness: 10, exposure: 5, highlights: -10, shadows: 10, temperature: -5, tint: 0, vignette: 0, clarity: 15 } },
  { name: '复古', params: { brightness: -5, contrast: 115, saturation: 70, hue: 20, blur: 0, sharpness: -5, exposure: -5, highlights: -15, shadows: 10, temperature: 15, tint: 5, vignette: 25, clarity: -10 } },
  { name: '日系', params: { brightness: 10, contrast: 95, saturation: 85, hue: -5, blur: 0, sharpness: -5, exposure: 5, highlights: 10, shadows: 5, temperature: -10, tint: -5, vignette: 10, clarity: -5 } },
  { name: '胶片', params: { brightness: 0, contrast: 120, saturation: 110, hue: 5, blur: 0, sharpness: 15, exposure: 0, highlights: -5, shadows: 5, temperature: 5, tint: 5, vignette: 20, clarity: 10 } },
  { name: '黑白', params: { brightness: 5, contrast: 120, saturation: 0, hue: 0, blur: 0, sharpness: 10, exposure: 0, highlights: 0, shadows: 0, temperature: 0, tint: 0, vignette: 15, clarity: 5 } },
]

const aiInputText = ref<string>('')
const isAILoading = ref<boolean>(false)
const aiExplanation = ref<string>('')
const aiSuggestions = [
  '更亮一点',
  '增加对比度',
  '暖色调',
  '电影感',
  '人像美化',
  '风景增强',
]

const hslEditorRef = ref<InstanceType<typeof HSLEditor> | null>(null)
const hslValues = ref<Record<string, { hue: number; saturation: number; lightness: number }>>({})
const hslEnabled = ref(false)

let applyFiltersTimeout: number | null = null

const debouncedApplyFilters = () => {
  if (applyFiltersTimeout) {
    clearTimeout(applyFiltersTimeout)
  }
  applyFiltersTimeout = window.setTimeout(() => {
    applyFilters()
  }, 50)
}

const initCanvas = (): void => {
  if (!canvasRef.value) {
    return
  }

  logger.log('Canvas初始化')
  
  fabric.textureSize = 4096
  
  fabric.Object.prototype.objectCaching = false
  fabric.Object.prototype.statefullCache = false
  fabric.Object.prototype.noScaleCache = true
  
  canvas.value = new fabric.Canvas(canvasRef.value, {
    preserveObjectStacking: true,
    backgroundColor: 'transparent',
    isDrawingMode: false,
    skipTargetFind: false,
    allowTouchScrolling: false,
    stopContextMenu: true,
    fireRightClick: true,
    fireMiddleClick: true,
  })
}

const loadImageToCanvas = async (url: string): Promise<void> => {
  if (!url) {
    return
  }

  isLoading.value = true

  try {
    if (!canvas.value) {
      initCanvas()
      if (!canvas.value) {
        logger.error('Canvas初始化失败')
        isLoading.value = false
        return
      }
    }

    const img = new Image()
    img.crossOrigin = 'anonymous'
    
    img.onload = () => {
      originalImageElement.value = img
      originalWidth.value = img.naturalWidth
      originalHeight.value = img.naturalHeight

      logger.log(`[loadImageToCanvas] 原始尺寸: ${originalWidth.value} x ${originalHeight.value}`)

      const previewContainer = document.querySelector('.preview-container') as HTMLElement
      const containerWidth = previewContainer.clientWidth
      const containerHeight = previewContainer.clientHeight

      const widthScale = containerWidth / originalWidth.value
      const heightScale = containerHeight / originalHeight.value
      const displayScale = Math.min(widthScale, heightScale, 1)

      const displayWidth = Math.round(originalWidth.value * displayScale)
      const displayHeight = Math.round(originalHeight.value * displayScale)

      canvas.value!.setWidth(containerWidth)
      canvas.value!.setHeight(containerHeight)

      const processedCanvas = createProcessedPreviewCanvas(img, displayWidth, displayHeight)

      fabric.Image.fromURL(
        processedCanvas.toDataURL(),
        (fabricImg) => {
          if (!fabricImg) {
            logger.error('Fabric图片创建失败')
            isLoading.value = false
            return
          }

          fabricImg.set({
            left: (containerWidth - displayWidth) / 2,
            top: (containerHeight - displayHeight) / 2,
            selectable: true,
          })

          canvas.value!.clear()
          canvas.value!.add(fabricImg)
          canvas.value!.renderAll()

          nextTick(() => {
            generateAllFilterPreviews()
          })

          isLoading.value = false
        },
        { crossOrigin: 'anonymous' }
      )
    }

    img.onerror = () => {
      logger.error('图片加载失败')
      isLoading.value = false
      ElMessage.error('图片加载失败')
    }

    img.src = url

  } catch (error) {
    logger.error('图片加载失败:', error)
    isLoading.value = false
    ElMessage.error('图片加载失败，请重试')
  }
}

const createProcessedPreviewCanvas = (
  img: HTMLImageElement, 
  targetWidth: number, 
  targetHeight: number
): HTMLCanvasElement => {
  const tempCanvas = document.createElement('canvas')
  tempCanvas.width = targetWidth
  tempCanvas.height = targetHeight
  const tempCtx = tempCanvas.getContext('2d')!
  
  tempCtx.drawImage(img, 0, 0, targetWidth, targetHeight)
  
  const imageData = tempCtx.getImageData(0, 0, targetWidth, targetHeight)
  const customParams: CustomFilterParams = {
    brightness: filterParams.value.brightness,
    contrast: filterParams.value.contrast,
    saturation: filterParams.value.saturation,
    hue: filterParams.value.hue,
    blur: 0,
    sharpness: filterParams.value.sharpness,
    exposure: filterParams.value.exposure,
    highlights: filterParams.value.highlights,
    shadows: filterParams.value.shadows,
    temperature: filterParams.value.temperature,
    tint: filterParams.value.tint,
    vignette: filterParams.value.vignette,
    clarity: filterParams.value.clarity,
    hsl: hslEnabled.value ? hslValues.value : undefined
  }
  
  const processedData = applyAllFilters(imageData, customParams)
  tempCtx.putImageData(processedData, 0, 0)
  
  if (filterParams.value.blur > 0) {
    const blurCanvas = document.createElement('canvas')
    blurCanvas.width = targetWidth
    blurCanvas.height = targetHeight
    const blurCtx = blurCanvas.getContext('2d')!
    blurCtx.drawImage(tempCanvas, 0, 0)
    const blurData = blurCtx.getImageData(0, 0, targetWidth, targetHeight)
    applyBlur(blurData.data, targetWidth, targetHeight, filterParams.value.blur)
    blurCtx.putImageData(blurData, 0, 0)
    tempCtx.drawImage(blurCanvas, 0, 0)
  }
  
  return tempCanvas
}

const setPreviewCanvasRef = (el: any, presetName: string): void => {
  if (el) {
    previewCanvasRefs.value.set(presetName, el)
  }
}

const isPresetActive = (preset: FilterPreset): boolean => {
  return activePresetName.value === preset.name
}

const generateFilterPreview = async (
  preset: FilterPreset,
  targetCanvas: HTMLCanvasElement
): Promise<void> => {
  if (!originalImageElement.value) return

  const width = 200
  const height = 150
  targetCanvas.width = width
  targetCanvas.height = height

  const tempCanvas = document.createElement('canvas')
  tempCanvas.width = width
  tempCanvas.height = height
  const tempCtx = tempCanvas.getContext('2d')!

  const img = originalImageElement.value
  const imgWidth = originalWidth.value
  const imgHeight = originalHeight.value

  const scale = Math.min(width / imgWidth, height / imgHeight)
  const scaledWidth = imgWidth * scale
  const scaledHeight = imgHeight * scale
  const offsetX = (width - scaledWidth) / 2
  const offsetY = (height - scaledHeight) / 2

  tempCtx.drawImage(img, offsetX, offsetY, scaledWidth, scaledHeight)

  const imageData = tempCtx.getImageData(0, 0, width, height)
  const customParams: CustomFilterParams = {
    brightness: preset.params.brightness ?? 0,
    contrast: preset.params.contrast ?? 100,
    saturation: preset.params.saturation ?? 100,
    hue: preset.params.hue ?? 0,
    blur: 0,
    sharpness: preset.params.sharpness ?? 0,
    exposure: preset.params.exposure ?? 0,
    highlights: preset.params.highlights ?? 0,
    shadows: preset.params.shadows ?? 0,
    temperature: preset.params.temperature ?? 0,
    tint: preset.params.tint ?? 0,
    vignette: preset.params.vignette ?? 0,
    clarity: preset.params.clarity ?? 0,
  }

  const processedData = applyAllFilters(imageData, customParams)
  tempCtx.putImageData(processedData, 0, 0)

  const targetCtx = targetCanvas.getContext('2d')
  if (targetCtx) {
    targetCtx.drawImage(tempCanvas, 0, 0)
  }
}

const generateAllFilterPreviews = async (): Promise<void> => {
  if (!originalImageElement.value) return

  for (const preset of filterPresets) {
    const previewCanvas = previewCanvasRefs.value.get(preset.name)
    if (previewCanvas) {
      await generateFilterPreview(preset, previewCanvas)
    }
  }
}

const applyFilters = (): void => {
  if (!canvas.value || !originalImageElement.value) return

  const objects = canvas.value.getObjects()
  if (objects.length === 0) return

  const fabricImg = objects[0] as fabric.Image

  const previewContainer = document.querySelector('.preview-container') as HTMLElement
  const containerWidth = previewContainer.clientWidth
  const containerHeight = previewContainer.clientHeight

  const widthScale = containerWidth / originalWidth.value
  const heightScale = containerHeight / originalHeight.value
  const displayScale = Math.min(widthScale, heightScale, 1)

  const displayWidth = Math.round(originalWidth.value * displayScale)
  const displayHeight = Math.round(originalHeight.value * displayScale)

  const processedCanvas = createProcessedPreviewCanvas(
    originalImageElement.value, 
    displayWidth, 
    displayHeight
  )

  fabricImg.setSrc(processedCanvas.toDataURL(), () => {
    canvas.value?.renderAll()
  }, { crossOrigin: 'anonymous' })
}

const applyPreset = (preset: FilterPreset): void => {
  filterParams.value = {
    brightness: preset.params.brightness ?? 0,
    contrast: preset.params.contrast ?? 100,
    saturation: preset.params.saturation ?? 100,
    hue: preset.params.hue ?? 0,
    blur: preset.params.blur ?? 0,
    sharpness: preset.params.sharpness ?? 0,
    exposure: preset.params.exposure ?? 0,
    highlights: preset.params.highlights ?? 0,
    shadows: preset.params.shadows ?? 0,
    temperature: preset.params.temperature ?? 0,
    tint: preset.params.tint ?? 0,
    vignette: preset.params.vignette ?? 0,
    clarity: preset.params.clarity ?? 0,
  }
  activePresetName.value = preset.name
  applyFilters()
}

const resetFilters = (): void => {
  filterParams.value = {
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
  }
  activePresetName.value = '原图'
  aiExplanation.value = ''
  applyFilters()
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
        current_params: {
          brightness: filterParams.value.brightness,
          contrast: filterParams.value.contrast,
          saturation: filterParams.value.saturation,
          hue: filterParams.value.hue,
          sharpness: filterParams.value.sharpness,
          exposure: filterParams.value.exposure,
          highlights: filterParams.value.highlights,
          shadows: filterParams.value.shadows,
          temperature: filterParams.value.temperature,
          tint: filterParams.value.tint,
          vignette: filterParams.value.vignette,
          clarity: filterParams.value.clarity,
          blur: filterParams.value.blur,
        },
        use_ai: false
      })
    })

    if (!response.ok) {
      throw new Error('AI服务请求失败')
    }

    const data = await response.json()
    
    if (data.params) {
      filterParams.value = {
        brightness: data.params.brightness ?? 0,
        contrast: data.params.contrast ?? 100,
        saturation: data.params.saturation ?? 100,
        hue: data.params.hue ?? 0,
        blur: data.params.blur ?? 0,
        sharpness: data.params.sharpness ?? 0,
        exposure: data.params.exposure ?? 0,
        highlights: data.params.highlights ?? 0,
        shadows: data.params.shadows ?? 0,
        temperature: data.params.temperature ?? 0,
        tint: data.params.tint ?? 0,
        vignette: data.params.vignette ?? 0,
        clarity: data.params.clarity ?? 0,
      }
      
      aiExplanation.value = data.explanation || '已根据您的描述调整参数'
      activePresetName.value = 'AI调整'
      
      applyFilters()
      ElMessage.success('AI已调整参数')
    }
  } catch (error) {
    logger.error('AI调整失败:', error)
    ElMessage.error('AI调整失败，请重试')
  } finally {
    isAILoading.value = false
  }
}

const applyHSL = (data: Record<string, { hue: number; saturation: number; lightness: number }>): void => {
  hslValues.value = { ...data }
  applyFilters()
  ElMessage.success('HSL已应用')
}

const fetchPortfolios = async (): Promise<void> => {
  try {
    const portfoliosData = await portfolioApi.getPortfolios()
    portfolios.value = portfoliosData
  } catch (error) {
    errorHandler.handleApiError(error, '获取作品集列表失败')
  }
}

const selectSavePortfolio = (portfolioId: number): void => {
  selectedSavePortfolioId.value = portfolioId
}

const createOriginalSizeProcessedImage = async (maxSize: number = 0): Promise<HTMLCanvasElement | null> => {
  if (!originalImageElement.value) return null

  let processWidth = originalWidth.value
  let processHeight = originalHeight.value
  
  if (maxSize > 0 && (originalWidth.value > maxSize || originalHeight.value > maxSize)) {
    const scale = maxSize / Math.max(originalWidth.value, originalHeight.value)
    processWidth = Math.round(originalWidth.value * scale)
    processHeight = Math.round(originalHeight.value * scale)
  }

  const tempCanvas = document.createElement('canvas')
  tempCanvas.width = processWidth
  tempCanvas.height = processHeight
  const tempCtx = tempCanvas.getContext('2d')!
  
  tempCtx.drawImage(originalImageElement.value, 0, 0, processWidth, processHeight)
  
  const imageData = tempCtx.getImageData(0, 0, processWidth, processHeight)
  const customParams: CustomFilterParams = {
    brightness: filterParams.value.brightness,
    contrast: filterParams.value.contrast,
    saturation: filterParams.value.saturation,
    hue: filterParams.value.hue,
    blur: 0,
    sharpness: filterParams.value.sharpness,
    exposure: filterParams.value.exposure,
    highlights: filterParams.value.highlights,
    shadows: filterParams.value.shadows,
    temperature: filterParams.value.temperature,
    tint: filterParams.value.tint,
    vignette: filterParams.value.vignette,
    clarity: filterParams.value.clarity,
    hsl: hslEnabled.value ? hslValues.value : undefined
  }
  
  const processedData = applyAllFilters(imageData, customParams)
  tempCtx.putImageData(processedData, 0, 0)
  
  if (filterParams.value.blur > 0) {
    const blurCanvas = document.createElement('canvas')
    blurCanvas.width = originalWidth.value
    blurCanvas.height = originalHeight.value
    const blurCtx = blurCanvas.getContext('2d')!
    blurCtx.drawImage(tempCanvas, 0, 0)
    const blurData = blurCtx.getImageData(0, 0, originalWidth.value, originalHeight.value)
    applyBlur(blurData.data, originalWidth.value, originalHeight.value, filterParams.value.blur)
    blurCtx.putImageData(blurData, 0, 0)
    tempCtx.drawImage(blurCanvas, 0, 0)
  }
  
  return tempCanvas
}

const saveToPortfolio = async (): Promise<void> => {
  if (!selectedSavePortfolioId.value) return
  
  try {
    const processedCanvas = await createOriginalSizeProcessedImage()
    if (!processedCanvas) {
      ElMessage.error('图片处理失败')
      return
    }
    
    const dataURL = processedCanvas.toDataURL('image/png', 1.0)
    
    const response = await fetch(dataURL)
    const blob = await response.blob()
    
    const formData = new FormData()
    formData.append('file', blob, `edited_image_${Date.now()}.png`)
    
    await portfolioApi.uploadImageToPortfolio(selectedSavePortfolioId.value, formData)
    
    showSaveToPortfolioDialog.value = false
    selectedSavePortfolioId.value = null
    
    ElMessage.success('图片已成功保存到作品集')
    
  } catch (error) {
    errorHandler.handleApiError(error, '保存图片到作品集失败')
  }
}

const saveImage = async (mode: 'lossless' | 'compressed'): Promise<void> => {
  showSaveOptionsDialog.value = false
  
  const loadingMsg = ElMessage({
    message: '正在处理图片，请稍候...',
    type: 'info',
    duration: 0,
    iconClass: 'el-icon-loading'
  })
  
  try {
    await new Promise(resolve => setTimeout(resolve, 50))
    
    let maxSize = 0
    if (mode === 'compressed') {
      maxSize = 4000
    }
    
    const processedCanvas = await createOriginalSizeProcessedImage(maxSize)
    if (!processedCanvas) {
      loadingMsg.close()
      ElMessage.error('图片处理失败')
      return
    }

    const outputWidth = processedCanvas.width
    const outputHeight = processedCanvas.height

    if (mode === 'lossless') {
      loadingMsg.close()
      
      const dataURL = processedCanvas.toDataURL('image/png', 1.0)
      const link = document.createElement('a')
      link.download = `edited_image_${outputWidth}x${outputHeight}_lossless.png`
      link.href = dataURL
      link.click()

      ElMessage.success(`无损保存成功 (${outputWidth}x${outputHeight})`)
    } else {
      loadingMsg.close()
      
      const dataURL = processedCanvas.toDataURL('image/jpeg', 0.92)
      const link = document.createElement('a')
      link.download = `edited_image_${outputWidth}x${outputHeight}.jpg`
      link.href = dataURL
      link.click()

      ElMessage.success(`压缩保存成功 (${outputWidth}x${outputHeight})`)
    }
  } catch (error) {
    loadingMsg.close()
    logger.error('保存图片失败:', error)
    ElMessage.error('保存图片失败')
  }
}

const handleWheel = (event: WheelEvent): void => {
  if (!canvas.value) return

  event.preventDefault()
  
  const canvasBounds = canvasRef.value?.getBoundingClientRect()
  if (!canvasBounds) return
  
  const mouseX = event.clientX - canvasBounds.left
  const mouseY = event.clientY - canvasBounds.top
  
  const delta = event.deltaY
  const scaleFactor = delta > 0 ? 0.9 : 1.1
  
  const point = new fabric.Point(mouseX, mouseY)
  canvas.value.zoomToPoint(point, canvas.value.getZoom() * scaleFactor)
  canvas.value.renderAll()
}

const handleResize = (): void => {
  if (props.imageUrl) {
    nextTick(() => {
      loadImageToCanvas(props.imageUrl!)
    })
  }
}

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  
  if (applyFiltersTimeout) {
    clearTimeout(applyFiltersTimeout)
  }
  
  if (canvas.value) {
    canvas.value.clear()
    canvas.value.dispose()
    canvas.value = null
  }
  
  originalImageElement.value = null
  
  if (canvasRef.value) {
    canvasRef.value = null
  }
  
  logger.log('FilterEditor组件已清理，释放内存资源')
})

watch(
  () => props.imageUrl,
  newUrl => {
    if (newUrl) {
      setTimeout(() => {
        loadImageToCanvas(newUrl)
      }, 100)
    }
  }
)

onMounted(() => {
  initCanvas()
  window.addEventListener('resize', handleResize)

  if (props.imageUrl) {
    setTimeout(() => {
      loadImageToCanvas(props.imageUrl!)
    }, 200)
  }
  
  fetchPortfolios()
})
</script>

<style scoped>
.filter-editor-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
}

.filter-preview-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: 2px;
  padding: 6px 0;
  background-color: white;
  border-bottom: 1px solid #e5e5ea;
  margin-bottom: 24px;
}

.filter-preview-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  padding: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.filter-preview-item:hover {
  background-color: #f5f5f7;
  border-color: #d1d1d6;
}

.filter-preview-item.active {
  border-color: #0071e3;
  background-color: #f0f7ff;
  box-shadow: 0 2px 8px rgba(0, 113, 227, 0.15);
}

.filter-preview-canvas {
  width: 100%;
  height: 80px;
  border-radius: 6px;
  object-fit: cover;
  background-color: #f5f5f7;
}

.filter-preview-label {
  margin-top: 6px;
  font-size: 12px;
  font-weight: 500;
  color: #1d1d1f;
}

.filter-preview-item.active .filter-preview-label {
  color: #0071e3;
}

.ai-input-section {
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
  border: 1px solid #e0e7ff;
}

.ai-input-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.ai-icon {
  font-size: 20px;
  color: #6366f1;
}

.ai-title {
  font-size: 15px;
  font-weight: 600;
  color: #4f46e5;
}

.ai-input-container {
  display: flex;
  gap: 10px;
  align-items: flex-start;
}

.ai-textarea {
  flex: 1;
}

.ai-textarea :deep(.el-textarea__inner) {
  border-radius: 8px;
  border-color: #c7d2fe;
  font-size: 13px;
}

.ai-textarea :deep(.el-textarea__inner:focus) {
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
}

.ai-apply-btn {
  border-radius: 8px;
  padding: 10px 16px;
  font-size: 13px;
  font-weight: 500;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  height: auto;
}

.ai-apply-btn:hover {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
}

.ai-explanation {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-top: 12px;
  padding: 10px 12px;
  background-color: #ecfdf5;
  border-radius: 8px;
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
  margin-top: 12px;
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

.editor-main {
  position: relative;
  flex: 1;
  width: 100%;
  height: 100%;
}

.large-preview-section {
  width: 100%;
  background-color: #fbfbfd;
  position: relative;
  height: calc(100vh - 65px);
}

.preview-container {
  position: relative;
  background-color: white;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  box-sizing: border-box;
  width: 100%;
  height: 100%;
}

.preview-canvas {
  display: block;
  background-color: transparent;
  cursor: grab;
  width: 100%;
  height: 100%;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 12px;
  z-index: 20;
  gap: 12px;
}

.loading-icon {
  font-size: 48px;
  color: #0071e3;
  animation: spin 1s linear infinite;
}

.loading-text {
  font-size: 18px;
  font-weight: 500;
  color: #1d1d1f;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.filter-panel {
  position: absolute;
  overflow-y: scroll;
  width: 400px;
  background-color: white;
  box-shadow: -5px 0 25px rgba(0, 0, 0, 0.1);
  padding: 24px;
  max-height: 100%;
  right: 0;
  top: 0;
  height: 100%;
  z-index: 100;
  transition: transform 0.3s ease;
}

.filter-panel.collapsed {
  transform: translateX(100%);
}

.panel-title {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e5ea;
}

.filter-controls {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-name {
  font-size: 14px;
  font-weight: 500;
  color: #1d1d1f;
}

.filter-value {
  font-size: 14px;
  color: #86868b;
  font-weight: 500;
}

:deep(.el-slider__runway) {
  background-color: #e5e5ea;
  height: 4px;
  border-radius: 2px;
}

:deep(.el-slider__bar) {
  background-color: #0071e3;
  height: 4px;
  border-radius: 2px;
}

:deep(.el-slider__button) {
  border-color: #0071e3;
  background-color: white;
  width: 20px;
  height: 20px;
  box-shadow: 0 2px 8px rgba(0, 113, 227, 0.3);
  transition: all 0.2s ease;
}

:deep(.el-slider__button:hover) {
  transform: scale(1.1);
}

.preset-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e5ea;
}

.preset-title {
  font-size: 16px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 16px;
}

.preset-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.preset-btn {
  padding: 8px 16px;
  border: 1px solid #e5e5ea;
  border-radius: 980px;
  background-color: white;
  font-size: 14px;
  font-weight: 500;
  color: #1d1d1f;
  cursor: pointer;
  transition: all 0.3s ease;
}

.preset-btn:hover {
  border-color: #0071e3;
  background-color: #f0f7ff;
  color: #0071e3;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e5ea;
  flex-wrap: wrap;
}

.action-btn {
  border-radius: 980px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  border: 1px solid #e5e5ea;
  background-color: white;
  color: #1d1d1f;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  border-color: #0071e3;
  background-color: #f0f7ff;
  color: #0071e3;
}

.action-btn.primary {
  background-color: #0071e3;
  border-color: #0071e3;
  color: white;
}

.action-btn.primary:hover {
  background-color: #0077ed;
  border-color: #0077ed;
}

.hsl-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e5ea;
}

.hsl-toggle {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.hsl-section .section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 0;
}

.save-options-dialog {
  .save-options {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .option-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    border: 1px solid #e5e5ea;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      border-color: #0071e3;
      background-color: #f0f7ff;
    }
  }

  .option-icon {
    font-size: 32px;
  }

  .option-content {
    flex: 1;
  }

  .option-title {
    font-size: 16px;
    font-weight: 600;
    color: #1d1d1f;
    margin-bottom: 4px;
  }

  .option-desc {
    font-size: 13px;
    color: #86868b;
  }
}

@media (max-width: 1024px) {
  .filter-panel {
    width: 350px;
  }
}

@media (max-width: 768px) {
  .editor-main {
    flex-direction: column;
  }

  .large-preview-section {
    width: 100%;
    height: 50vh;
  }

  .filter-panel {
    width: 100%;
    position: relative;
    transform: none;
    height: 50vh;
    box-shadow: 0 -5px 25px rgba(0, 0, 0, 0.1);
  }

  .filter-panel.collapsed {
    transform: translateY(100%);
  }
}

.portfolio-dialog {
  .el-dialog__body {
    padding: 20px;
  }
}

.portfolio-selector {
  padding: 10px 0;
}

.portfolio-list {
  max-height: 300px;
  overflow-y: auto;
}

.portfolio-item {
  padding: 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 12px;
  background-color: #fafafa;
  border: 1px solid transparent;
}

.portfolio-item:hover {
  background-color: #f0f7ff;
}

.portfolio-item.active {
  background-color: #e6f2ff;
  border-color: #0071e3;
}

.portfolio-item-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.portfolio-item-title {
  font-size: 15px;
  font-weight: 500;
  color: #333333;
}

.portfolio-item-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #666666;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 20px;
  margin-top: 20px;
  border-top: 1px solid #f0f0f0;
}
</style>
