<template>
  <div class="batch-processor">
    <div class="batch-header">
      <span class="batch-title">批量处理</span>
      <div class="batch-actions">
        <el-button size="small" @click="selectAll">全选</el-button>
        <el-button size="small" @click="deselectAll">取消全选</el-button>
      </div>
    </div>
    
    <div class="batch-images">
      <div 
        v-for="image in images" 
        :key="image.id"
        class="batch-image-item"
        :class="{ 'selected': selectedImages.includes(image.id) }"
        @click="toggleImageSelection(image.id)"
      >
        <img :src="image.thumbnail_path" alt="图片" />
        <div class="selection-overlay">
          <el-icon v-if="selectedImages.includes(image.id)" class="check-icon"><Check /></el-icon>
        </div>
      </div>
    </div>
    
    <div class="batch-info">
      <span>已选择 {{ selectedImages.length }} 张图片</span>
    </div>
    
    <div class="batch-filters">
      <h4 class="section-title">批量滤镜设置</h4>
      
      <div class="filter-presets">
        <el-tag 
          v-for="preset in filterPresets" 
          :key="preset.name"
          @click="applyBatchPreset(preset)"
          class="preset-tag"
          effect="plain"
        >
          {{ preset.name }}
        </el-tag>
      </div>
      
      <div class="filter-controls">
        <div class="filter-item" v-for="(config, key) in filterConfig" :key="key">
          <div class="filter-header">
            <span class="filter-name">{{ config.label }}</span>
            <span class="filter-value">{{ batchParams[key] }}</span>
          </div>
          <el-slider
            v-model="batchParams[key]"
            :min="config.min"
            :max="config.max"
            :step="config.step || 1"
          />
        </div>
      </div>
    </div>
    
    <div class="watermark-section">
      <h4 class="section-title">水印设置</h4>
      <el-checkbox v-model="enableWatermark">添加水印</el-checkbox>
      
      <div v-if="enableWatermark" class="watermark-options">
        <div class="watermark-type">
          <el-radio-group v-model="watermarkType">
            <el-radio label="text">文字水印</el-radio>
            <el-radio label="image">图片水印</el-radio>
          </el-radio-group>
        </div>
        
        <div v-if="watermarkType === 'text'" class="watermark-text">
          <el-input v-model="watermarkText" placeholder="输入水印文字" />
        </div>
        
        <div v-else class="watermark-image">
          <el-upload
            :show-file-list="false"
            :before-upload="handleWatermarkUpload"
            accept="image/*,.raf,.cr2,.nef,.arw,.dng,.raw"
          >
            <el-button size="small">上传水印图片</el-button>
          </el-upload>
          <div v-if="watermarkImage" class="watermark-preview">
            <img :src="watermarkImage" alt="水印预览" />
          </div>
        </div>
        
        <div class="watermark-position">
          <span class="position-label">位置：</span>
          <el-select v-model="watermarkPosition" size="small">
            <el-option label="左上角" value="top-left" />
            <el-option label="右上角" value="top-right" />
            <el-option label="左下角" value="bottom-left" />
            <el-option label="右下角" value="bottom-right" />
            <el-option label="居中" value="center" />
          </el-select>
        </div>
        
        <div class="watermark-opacity">
          <span class="opacity-label">透明度：</span>
          <el-slider v-model="watermarkOpacity" :min="0" :max="100" />
        </div>
      </div>
    </div>
    
    <div class="export-options">
      <h4 class="section-title">导出选项</h4>
      
      <div class="export-format">
        <span class="format-label">格式：</span>
        <el-select v-model="exportFormat" size="small">
          <el-option label="PNG" value="png" />
          <el-option label="JPEG" value="jpeg" />
          <el-option label="WebP" value="webp" />
        </el-select>
      </div>
      
      <div class="export-quality" v-if="exportFormat !== 'png'">
        <span class="quality-label">质量：</span>
        <el-slider v-model="exportQuality" :min="1" :max="100" />
        <span class="quality-value">{{ exportQuality }}%</span>
      </div>
      
      <div class="export-size">
        <el-checkbox v-model="resizeImages">调整尺寸</el-checkbox>
        <div v-if="resizeImages" class="size-inputs">
          <el-input-number v-model="exportWidth" :min="1" :max="10000" size="small" placeholder="宽度" />
          <span>×</span>
          <el-input-number v-model="exportHeight" :min="1" :max="10000" size="small" placeholder="高度" />
          <el-checkbox v-model="keepAspectRatio">保持比例</el-checkbox>
        </div>
      </div>
    </div>
    
    <div class="batch-footer">
      <el-button @click="cancelBatch">取消</el-button>
      <el-button type="primary" @click="startBatchProcess" :loading="isProcessing">
        {{ isProcessing ? `处理中 ${processingProgress}%` : '开始批量处理' }}
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Check } from '@element-plus/icons-vue'
import { 
  applyAllFilters, 
  applyBlur,
  type FilterParams 
} from '../utils/imageFilters'

interface Image {
  id: number
  filename: string
  filepath: string
  thumbnail_path: string
}

interface FilterPreset {
  name: string
  params: Record<string, number>
}

const props = defineProps<{
  images: Image[]
}>()

const emit = defineEmits<{
  cancel: []
  complete: [processedImages: any[]]
}>()

const selectedImages = ref<number[]>([])
const isProcessing = ref(false)
const processingProgress = ref(0)

interface FilterConfigItem {
  label: string
  min: number
  max: number
  step?: number
}

const filterConfig: Record<string, FilterConfigItem> = {
  brightness: { label: '亮度', min: -100, max: 100 },
  contrast: { label: '对比度', min: 0, max: 200 },
  saturation: { label: '饱和度', min: -100, max: 100 },
  hue: { label: '色相', min: 0, max: 360 },
  sharpness: { label: '锐化', min: -50, max: 50 },
  exposure: { label: '曝光', min: -100, max: 100 },
  highlights: { label: '高光', min: -100, max: 100 },
  shadows: { label: '阴影', min: -100, max: 100 },
  temperature: { label: '色温', min: -50, max: 50 },
  tint: { label: '色调', min: -50, max: 50 },
  vignette: { label: '暗角', min: 0, max: 100 },
  clarity: { label: '清晰度', min: -100, max: 100 },
  blur: { label: '模糊', min: 0, max: 20 }
}

const batchParams = ref<Record<string, number>>({
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
  blur: 0
})

const filterPresets: FilterPreset[] = [
  { name: '原图', params: { brightness: 0, contrast: 100, saturation: 100, hue: 0, sharpness: 0, exposure: 0, highlights: 0, shadows: 0, temperature: 0, tint: 0, vignette: 0, clarity: 0, blur: 0 } },
  { name: '清新', params: { brightness: 5, contrast: 105, saturation: 90, hue: 5, sharpness: 10, exposure: 5, highlights: -10, shadows: 10, temperature: -5, tint: 0, vignette: 0, clarity: 15, blur: 0 } },
  { name: '复古', params: { brightness: -5, contrast: 115, saturation: 70, hue: 20, sharpness: -5, exposure: -5, highlights: -15, shadows: 10, temperature: 15, tint: 5, vignette: 25, clarity: -10, blur: 0 } },
  { name: '电影感', params: { brightness: 0, contrast: 120, saturation: 80, hue: 5, sharpness: 15, exposure: 0, highlights: -5, shadows: 5, temperature: 5, tint: 5, vignette: 20, clarity: 10, blur: 0 } }
]

const enableWatermark = ref(false)
const watermarkType = ref('text')
const watermarkText = ref('')
const watermarkImage = ref('')
const watermarkPosition = ref('bottom-right')
const watermarkOpacity = ref(50)

const exportFormat = ref('png')
const exportQuality = ref(90)
const resizeImages = ref(false)
const exportWidth = ref(1920)
const exportHeight = ref(1080)
const keepAspectRatio = ref(true)

const toggleImageSelection = (imageId: number) => {
  const index = selectedImages.value.indexOf(imageId)
  if (index > -1) {
    selectedImages.value.splice(index, 1)
  } else {
    selectedImages.value.push(imageId)
  }
}

const selectAll = () => {
  selectedImages.value = props.images.map(img => img.id)
}

const deselectAll = () => {
  selectedImages.value = []
}

const applyBatchPreset = (preset: FilterPreset) => {
  batchParams.value = { ...preset.params }
}

const handleWatermarkUpload = (file: File) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    watermarkImage.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
  return false
}

const processImage = async (image: Image): Promise<Blob> => {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.crossOrigin = 'anonymous'
    
    img.onload = () => {
      let width = img.naturalWidth
      let height = img.naturalHeight
      
      if (resizeImages.value) {
        width = exportWidth.value
        height = exportHeight.value
      }
      
      const canvas = document.createElement('canvas')
      canvas.width = width
      canvas.height = height
      const ctx = canvas.getContext('2d')
      
      if (!ctx) {
        reject(new Error('无法创建Canvas上下文'))
        return
      }
      
      ctx.drawImage(img, 0, 0, width, height)
      
      const imageData = ctx.getImageData(0, 0, width, height)
      const filterParams: FilterParams = {
        brightness: batchParams.value.brightness ?? 0,
        contrast: batchParams.value.contrast ?? 100,
        saturation: batchParams.value.saturation ?? 100,
        hue: batchParams.value.hue ?? 0,
        sharpness: batchParams.value.sharpness ?? 0,
        exposure: batchParams.value.exposure ?? 0,
        highlights: batchParams.value.highlights ?? 0,
        shadows: batchParams.value.shadows ?? 0,
        temperature: batchParams.value.temperature ?? 0,
        tint: batchParams.value.tint ?? 0,
        vignette: batchParams.value.vignette ?? 0,
        clarity: batchParams.value.clarity ?? 0,
        blur: 0
      }
      
      const processedData = applyAllFilters(imageData, filterParams)
      ctx.putImageData(processedData, 0, 0)
      
      if ((batchParams.value.blur ?? 0) > 0) {
        const blurCanvas = document.createElement('canvas')
        blurCanvas.width = width
        blurCanvas.height = height
        const blurCtx = blurCanvas.getContext('2d')
        if (blurCtx) {
          blurCtx.drawImage(canvas, 0, 0)
          const blurData = blurCtx.getImageData(0, 0, width, height)
          applyBlur(blurData.data, width, height, batchParams.value.blur ?? 0)
          blurCtx.putImageData(blurData, 0, 0)
          ctx.drawImage(blurCanvas, 0, 0)
        }
      }
      
      if (enableWatermark.value) {
        applyWatermarkToCanvas(ctx, width, height)
      }
      
      const mimeType = `image/${exportFormat.value}`
      const quality = exportFormat.value === 'png' ? undefined : exportQuality.value / 100
      
      canvas.toBlob((blob) => {
        if (blob) {
          resolve(blob)
        } else {
          reject(new Error('图片转换失败'))
        }
      }, mimeType, quality)
    }
    
    img.onerror = () => reject(new Error('图片加载失败'))
    img.src = image.filepath
  })
}

const applyWatermarkToCanvas = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
  ctx.globalAlpha = watermarkOpacity.value / 100
  
  if (watermarkType.value === 'text' && watermarkText.value) {
    const fontSize = Math.max(16, width / 40)
    ctx.font = `${fontSize}px Arial`
    ctx.fillStyle = '#ffffff'
    ctx.strokeStyle = '#000000'
    ctx.lineWidth = 2
    
    const textWidth = ctx.measureText(watermarkText.value).width
    const padding = 20
    
    let x = padding
    let y = fontSize + padding
    
    switch (watermarkPosition.value) {
      case 'top-right':
        x = width - textWidth - padding
        break
      case 'bottom-left':
        y = height - padding
        break
      case 'bottom-right':
        x = width - textWidth - padding
        y = height - padding
        break
      case 'center':
        x = (width - textWidth) / 2
        y = height / 2
        break
    }
    
    ctx.strokeText(watermarkText.value, x, y)
    ctx.fillText(watermarkText.value, x, y)
  } else if (watermarkType.value === 'image' && watermarkImage.value) {
    const watermarkImg = new Image()
    watermarkImg.src = watermarkImage.value
    
    const wmWidth = width / 5
    const wmHeight = (watermarkImg.height / watermarkImg.width) * wmWidth
    
    let x = 20
    let y = 20
    
    switch (watermarkPosition.value) {
      case 'top-right':
        x = width - wmWidth - 20
        break
      case 'bottom-left':
        y = height - wmHeight - 20
        break
      case 'bottom-right':
        x = width - wmWidth - 20
        y = height - wmHeight - 20
        break
      case 'center':
        x = (width - wmWidth) / 2
        y = (height - wmHeight) / 2
        break
    }
    
    ctx.drawImage(watermarkImg, x, y, wmWidth, wmHeight)
  }
  
  ctx.globalAlpha = 1
}

const startBatchProcess = async () => {
  if (selectedImages.value.length === 0) {
    ElMessage.warning('请先选择要处理的图片')
    return
  }
  
  isProcessing.value = true
  processingProgress.value = 0
  
  const processedImages: { id: number; filename: string; blob: Blob }[] = []
  const selectedImageObjs = props.images.filter(img => selectedImages.value.includes(img.id))
  
  for (let i = 0; i < selectedImageObjs.length; i++) {
    const image = selectedImageObjs[i]
    if (!image) continue
    
    try {
      const blob = await processImage(image)
      processedImages.push({
        id: image.id,
        filename: image.filename,
        blob
      })
      
      processingProgress.value = Math.round(((i + 1) / selectedImageObjs.length) * 100)
    } catch (error) {
      console.error(`处理图片 ${image.filename} 失败:`, error)
    }
  }
  
  isProcessing.value = false
  ElMessage.success(`成功处理 ${processedImages.length} 张图片`)
  
  downloadProcessedImages(processedImages)
  emit('complete', processedImages)
}

const downloadProcessedImages = (images: { id: number; filename: string; blob: Blob }[]): void => {
  images.forEach((img, index) => {
    const url = URL.createObjectURL(img.blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `edited_${img.filename}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  })
}

const cancelBatch = () => {
  emit('cancel')
}
</script>

<style scoped>
.batch-processor {
  background-color: #1a1a1a;
  border-radius: 12px;
  padding: 20px;
  color: #ffffff;
  max-height: 80vh;
  overflow-y: auto;
}

.batch-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.batch-title {
  font-size: 16px;
  font-weight: 600;
}

.batch-actions {
  display: flex;
  gap: 8px;
}

.batch-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
  max-height: 200px;
  overflow-y: auto;
  padding: 8px;
  background-color: #252525;
  border-radius: 8px;
}

.batch-image-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}

.batch-image-item:hover {
  border-color: #409eff;
}

.batch-image-item.selected {
  border-color: #67c23a;
}

.batch-image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.selection-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(103, 194, 58, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.batch-image-item.selected .selection-overlay {
  opacity: 1;
}

.check-icon {
  font-size: 24px;
  color: #67c23a;
}

.batch-info {
  font-size: 13px;
  color: #999;
  margin-bottom: 16px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #fff;
}

.batch-filters,
.watermark-section,
.export-options {
  background-color: #252525;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.filter-presets {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.preset-tag {
  cursor: pointer;
}

.preset-tag:hover {
  background-color: #409eff;
  color: #fff;
  border-color: #409eff;
}

.filter-controls {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.filter-name {
  color: #ccc;
}

.filter-value {
  color: #409eff;
}

.watermark-options {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.watermark-preview {
  margin-top: 8px;
}

.watermark-preview img {
  max-width: 150px;
  max-height: 50px;
  border-radius: 4px;
}

.watermark-position,
.watermark-opacity {
  display: flex;
  align-items: center;
  gap: 12px;
}

.position-label,
.opacity-label {
  font-size: 12px;
  color: #999;
  min-width: 60px;
}

.export-format,
.export-quality,
.export-size {
  margin-bottom: 12px;
}

.format-label,
.quality-label {
  font-size: 12px;
  color: #999;
  margin-right: 12px;
}

.export-quality {
  display: flex;
  align-items: center;
  gap: 12px;
}

.export-quality :deep(.el-slider) {
  width: 200px;
}

.quality-value {
  font-size: 12px;
  color: #ccc;
  min-width: 40px;
}

.size-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.size-inputs span {
  color: #999;
}

.batch-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #333;
}
</style>
