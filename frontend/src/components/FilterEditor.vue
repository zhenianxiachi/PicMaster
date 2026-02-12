<template>
  <div class="filter-editor-container">
    <!-- 顶部导航栏 -->
    <div class="editor-header">
      <el-button 
        type="text" 
        class="back-btn"
        @click="$emit('back')"
      >
        <el-icon-arrow-left />
      </el-button>
      <div class="header-title">图片编辑</div>
      <div class="header-actions">
        <el-button 
          type="default" 
          class="portfolio-btn"
          @click="showPortfolioDialog = true"
        >
          导入作品集
        </el-button>
        <el-button 
          type="default" 
          class="portfolio-btn"
          @click="showSaveToPortfolioDialog = true"
        >
          保存到作品集
        </el-button>
        <el-button 
          type="primary" 
          class="save-btn"
          @click="saveImage"
        >
          保存
        </el-button>
      </div>
    </div>
    
    <div class="editor-content">
      <!-- 左侧：图片预览区 -->
      <div class="preview-area">
        <div class="preview-wrapper">
          <img 
            ref="imageRef" 
            :src="imageUrl" 
            :style="imageStyle" 
            class="preview-image"
          />
        </div>
      </div>
      
      <!-- 右侧：编辑工具区 -->
      <div class="tools-area">
        <!-- 滤镜选择 -->
        <div class="tool-section">
          <h3 class="tool-title">滤镜</h3>
          <div class="filter-grid">
            <div 
              v-for="filter in filters" 
              :key="filter.name"
              class="filter-item"
              :class="{ active: activeFilter === filter.name }"
              @click="applyFilter(filter)"
            >
              <div class="filter-preview">
                <img :src="imageUrl" :style="getFilterStyle(filter)" class="filter-thumbnail" />
              </div>
              <span class="filter-name">{{ filter.name }}</span>
            </div>
          </div>
        </div>
        
        <!-- 基础调整 -->
        <div class="tool-section">
          <h3 class="tool-title">调整</h3>
          
          <!-- 亮度 -->
          <div class="adjust-item">
            <div class="adjust-label">亮度</div>
            <el-slider 
              v-model="adjustments.brightness" 
              :min="-100" 
              :max="100" 
              :step="1"
              @change="updateAdjustments"
            />
            <div class="adjust-value">{{ adjustments.brightness }}</div>
          </div>
          
          <!-- 对比度 -->
          <div class="adjust-item">
            <div class="adjust-label">对比度</div>
            <el-slider 
              v-model="adjustments.contrast" 
              :min="-100" 
              :max="100" 
              :step="1"
              @change="updateAdjustments"
            />
            <div class="adjust-value">{{ adjustments.contrast }}</div>
          </div>
          
          <!-- 饱和度 -->
          <div class="adjust-item">
            <div class="adjust-label">饱和度</div>
            <el-slider 
              v-model="adjustments.saturation" 
              :min="-100" 
              :max="100" 
              :step="1"
              @change="updateAdjustments"
            />
            <div class="adjust-value">{{ adjustments.saturation }}</div>
          </div>
          
          <!-- 锐化 -->
          <div class="adjust-item">
            <div class="adjust-label">锐化</div>
            <el-slider 
              v-model="adjustments.sharpness" 
              :min="0" 
              :max="100" 
              :step="1"
              @change="updateAdjustments"
            />
            <div class="adjust-value">{{ adjustments.sharpness }}</div>
          </div>
          
          <!-- 曝光 -->
          <div class="adjust-item">
            <div class="adjust-label">曝光</div>
            <el-slider 
              v-model="adjustments.exposure" 
              :min="-50" 
              :max="50" 
              :step="1"
              @change="updateAdjustments"
            />
            <div class="adjust-value">{{ adjustments.exposure }}</div>
          </div>
          
          <!-- 高光 -->
          <div class="adjust-item">
            <div class="adjust-label">高光</div>
            <el-slider 
              v-model="adjustments.highlights" 
              :min="-100" 
              :max="100" 
              :step="1"
              @change="updateAdjustments"
            />
            <div class="adjust-value">{{ adjustments.highlights }}</div>
          </div>
          
          <!-- 阴影 -->
          <div class="adjust-item">
            <div class="adjust-label">阴影</div>
            <el-slider 
              v-model="adjustments.shadows" 
              :min="-100" 
              :max="100" 
              :step="1"
              @change="updateAdjustments"
            />
            <div class="adjust-value">{{ adjustments.shadows }}</div>
          </div>
          
          <!-- 色温 -->
          <div class="adjust-item">
            <div class="adjust-label">色温</div>
            <el-slider 
              v-model="adjustments.temperature" 
              :min="-100" 
              :max="100" 
              :step="1"
              @change="updateAdjustments"
            />
            <div class="adjust-value">{{ adjustments.temperature }}</div>
          </div>
          
          <!-- 色调 -->
          <div class="adjust-item">
            <div class="adjust-label">色调</div>
            <el-slider 
              v-model="adjustments.tint" 
              :min="-100" 
              :max="100" 
              :step="1"
              @change="updateAdjustments"
            />
            <div class="adjust-value">{{ adjustments.tint }}</div>
          </div>
          
          <!-- 暗角 -->
          <div class="adjust-item">
            <div class="adjust-label">暗角</div>
            <el-slider 
              v-model="adjustments.vignette" 
              :min="0" 
              :max="100" 
              :step="1"
              @change="updateAdjustments"
            />
            <div class="adjust-value">{{ adjustments.vignette }}</div>
          </div>
          
          <!-- 清晰度 -->
          <div class="adjust-item">
            <div class="adjust-label">清晰度</div>
            <el-slider 
              v-model="adjustments.clarity" 
              :min="-50" 
              :max="50" 
              :step="1"
              @change="updateAdjustments"
            />
            <div class="adjust-value">{{ adjustments.clarity }}</div>
          </div>
          
          <!-- 重置按钮 -->
          <el-button 
            type="text" 
            class="reset-btn"
            @click="resetAdjustments"
          >
            重置
          </el-button>
        </div>
      </div>
    </div>
    
    <!-- 作品集选择对话框 -->
    <el-dialog
      v-model="showPortfolioDialog"
      title="选择作品集"
      width="500px"
      class="portfolio-dialog"
    >
      <div class="portfolio-selector">
        <div class="portfolio-list">
          <div 
            v-for="portfolio in portfolios" 
            :key="portfolio.id"
            class="portfolio-item"
            :class="{ active: selectedPortfolioId === portfolio.id }"
            @click="selectPortfolio(portfolio.id)"
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
          <el-button @click="showPortfolioDialog = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="importToPortfolio"
            :disabled="!selectedPortfolioId"
          >
            确定导入
          </el-button>
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
                <span>{{ (portfolio.images?.length || 0) }}张图片</span>
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

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { portfolioApi } from '../api/portfolioApi'

const props = defineProps({
  imageUrl: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['back'])

const imageRef = ref(null)
const activeFilter = ref('原图')
const currentFilter = ref(null)

// 作品集相关
const portfolios = ref([])
const showPortfolioDialog = ref(false)
const selectedPortfolioId = ref(null)
const showSaveToPortfolioDialog = ref(false)
const selectedSavePortfolioId = ref(null)
const isLoading = ref(false)

// 滤镜列表
const filters = ref([
  { name: '原图', value: { brightness: 0, contrast: 0, saturation: 0, sharpness: 0 } },
  { name: '清新', value: { brightness: 10, contrast: 5, saturation: 15, sharpness: 10 } },
  { name: '复古', value: { brightness: -5, contrast: 10, saturation: -20, sharpness: 5 } },
  { name: '日系', value: { brightness: 15, contrast: -5, saturation: 5, sharpness: 0 } },
  { name: '胶片', value: { brightness: -10, contrast: 15, saturation: 20, sharpness: 15 } },
  { name: '黑白', value: { brightness: 0, contrast: 10, saturation: -100, sharpness: 5 } }
])

// 调整参数
const adjustments = ref({
  brightness: 0,
  contrast: 0,
  saturation: 0,
  sharpness: 0,
  exposure: 0,
  highlights: 0,
  shadows: 0,
  temperature: 0,
  tint: 0,
  vignette: 0,
  clarity: 0
})

// 计算图片样式
const imageStyle = computed(() => {
  // 确保所有属性都有默认值，避免undefined导致NaN
  const adj = {
    brightness: adjustments.value.brightness || 0,
    contrast: adjustments.value.contrast || 0,
    saturation: adjustments.value.saturation || 0,
    sharpness: adjustments.value.sharpness || 0,
    exposure: adjustments.value.exposure || 0,
    highlights: adjustments.value.highlights || 0,
    shadows: adjustments.value.shadows || 0,
    temperature: adjustments.value.temperature || 0,
    tint: adjustments.value.tint || 0,
    vignette: adjustments.value.vignette || 0,
    clarity: adjustments.value.clarity || 0
  }
  
  // 基础滤镜计算
  const brightness = 1 + adj.brightness / 100
  const contrast = 1 + adj.contrast / 100
  const saturation = 1 + adj.saturation / 100
  
  // 组合计算：曝光影响亮度
  const finalBrightness = brightness * (1 + adj.exposure / 100)
  
  // 色温转换为色相旋转
  const hueRotate = (adj.temperature / 100) * 60 // 限制在 -60 到 60 度
  
  // 色调使用 sepia + 反相来模拟
  const sepia = Math.abs(adj.tint) / 100
  const invert = adj.tint < 0 ? Math.abs(adj.tint) / 200 : 0
  
  // 清晰度：使用锐化滤镜模拟
  const sharpen = adj.clarity > 0 ? adj.clarity / 50 : 0
  const blur = adj.clarity < 0 ? Math.abs(adj.clarity) / 100 : 0
  
  return {
    filter: `
      brightness(${finalBrightness}) 
      contrast(${contrast}) 
      saturate(${saturation}) 
      hue-rotate(${hueRotate}deg) 
      sepia(${sepia}) 
      invert(${invert}) 
      ${sharpen > 0 ? `url('data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\'><filter id=\'sharpen\'><feConvolveMatrix kernelMatrix=\'0 -${sharpen} 0 -${sharpen} ${4 * sharpen + 1} -${sharpen} 0 -${sharpen} 0\'/></filter></svg>#sharpen')` : ''} 
      blur(${blur}px) 
    `,
    transform: `scale(${1 + adj.sharpness / 200})`,
    boxShadow: adj.vignette !== 0 
      ? `inset 0 0 ${Math.abs(adj.vignette) * 5}px ${Math.abs(adj.vignette) * 2}px rgba(0, 0, 0, ${Math.abs(adj.vignette) / 100})` 
      : 'none'
  }
})

// 获取滤镜样式
const getFilterStyle = (filter) => {
  // 基础滤镜计算
  const brightness = 1 + filter.value.brightness / 100
  const contrast = 1 + filter.value.contrast / 100
  const saturation = 1 + filter.value.saturation / 100
  
  // 组合计算：曝光影响亮度
  const finalBrightness = brightness * (1 + (filter.value.exposure || 0) / 100)
  
  // 色温转换为色相旋转
  const hueRotate = ((filter.value.temperature || 0) / 100) * 60 // 限制在 -60 到 60 度
  
  // 色调使用 sepia + 反相来模拟
  const tint = (filter.value.tint || 0) / 100
  const sepia = Math.abs(tint) / 100
  const invert = tint < 0 ? Math.abs(tint) / 200 : 0
  
  // 清晰度：使用锐化滤镜模拟
  const clarity = (filter.value.clarity || 0)
  const sharpen = clarity > 0 ? clarity / 50 : 0
  const blur = clarity < 0 ? Math.abs(clarity) / 100 : 0
  
  return {
    filter: `
      brightness(${finalBrightness}) 
      contrast(${contrast}) 
      saturate(${saturation}) 
      hue-rotate(${hueRotate}deg) 
      sepia(${sepia}) 
      invert(${invert}) 
      ${sharpen > 0 ? `url('data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\'><filter id=\'sharpen\'><feConvolveMatrix kernelMatrix=\'0 -${sharpen} 0 -${sharpen} ${4 * sharpen + 1} -${sharpen} 0 -${sharpen} 0\'/></filter></svg>#sharpen')` : ''} 
      blur(${blur}px) 
    `,
    transform: `scale(${1 + filter.value.sharpness / 200})`,
    boxShadow: ((filter.value.vignette || 0) !== 0) 
      ? `inset 0 0 ${Math.abs(filter.value.vignette) * 5}px ${Math.abs(filter.value.vignette) * 2}px rgba(0, 0, 0, ${Math.abs(filter.value.vignette) / 100})` 
      : 'none'
  }
}

// 应用滤镜
const applyFilter = (filter) => {
  activeFilter.value = filter.name
  // 确保adjustments包含所有必需的属性，为缺少的属性提供默认值
  adjustments.value = {
    brightness: filter.value.brightness || 0,
    contrast: filter.value.contrast || 0,
    saturation: filter.value.saturation || 0,
    sharpness: filter.value.sharpness || 0,
    exposure: filter.value.exposure || 0,
    highlights: filter.value.highlights || 0,
    shadows: filter.value.shadows || 0,
    temperature: filter.value.temperature || 0,
    tint: filter.value.tint || 0,
    vignette: filter.value.vignette || 0,
    clarity: filter.value.clarity || 0
  }
  currentFilter.value = filter
}

// 更新调整
const updateAdjustments = () => {
  activeFilter.value = '自定义'
  currentFilter.value = null
}

// 重置调整
const resetAdjustments = () => {
  adjustments.value = {
    brightness: 0,
    contrast: 0,
    saturation: 0,
    sharpness: 0,
    exposure: 0,
    highlights: 0,
    shadows: 0,
    temperature: 0,
    tint: 0,
    vignette: 0,
    clarity: 0
  }
  activeFilter.value = '原图'
  currentFilter.value = null
}

// 保存图片
const saveImage = () => {
  const image = imageRef.value
  if (!image) return
  
  // 创建canvas元素
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  
  // 设置canvas尺寸
  canvas.width = image.naturalWidth
  canvas.height = image.naturalHeight
  
  // 应用滤镜效果
  // 基础滤镜计算
  const brightness = 1 + adjustments.value.brightness / 100
  const contrast = 1 + adjustments.value.contrast / 100
  const saturation = 1 + adjustments.value.saturation / 100
  
  // 组合计算：曝光影响亮度
  const finalBrightness = brightness * (1 + adjustments.value.exposure / 100)
  
  // 色温转换为色相旋转
  const hueRotate = (adjustments.value.temperature / 100) * 60 // 限制在 -60 到 60 度
  
  // 色调使用 sepia + 反相来模拟
  const sepia = Math.abs(adjustments.value.tint) / 100
  const invert = adjustments.value.tint < 0 ? Math.abs(adjustments.value.tint) / 200 : 0
  
  // 清晰度：使用锐化滤镜模拟
  const clarity = adjustments.value.clarity
  const sharpen = clarity > 0 ? clarity / 50 : 0
  const blur = clarity < 0 ? Math.abs(clarity) / 100 : 0
  
  // 构建单一滤镜字符串
  ctx.filter = `
    brightness(${finalBrightness}) 
    contrast(${contrast}) 
    saturate(${saturation}) 
    hue-rotate(${hueRotate}deg) 
    sepia(${sepia}) 
    invert(${invert}) 
    ${sharpen > 0 ? `url('data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\'><filter id=\'sharpen\'><feConvolveMatrix kernelMatrix=\'0 -${sharpen} 0 -${sharpen} ${4 * sharpen + 1} -${sharpen} 0 -${sharpen} 0\'/></filter></svg>#sharpen')` : ''} 
    blur(${blur}px) 
  `
  
  // 暗角效果需要在绘制图片后单独处理
  const drawVignette = adjustments.value.vignette > 0
  
  // 绘制图片
  ctx.drawImage(image, 0, 0)
  
  // 应用暗角效果
  if (drawVignette) {
    const vignetteIntensity = adjustments.value.vignette / 100
    const centerX = canvas.width / 2
    const centerY = canvas.height / 2
    const radius = Math.max(canvas.width, canvas.height) * 0.75
    
    const gradient = ctx.createRadialGradient(centerX, centerY, radius * 0.5, centerX, centerY, radius)
    gradient.addColorStop(0, 'rgba(0, 0, 0, 0)')
    gradient.addColorStop(1, `rgba(0, 0, 0, ${vignetteIntensity})`)
    
    ctx.globalCompositeOperation = 'multiply'
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    ctx.globalCompositeOperation = 'source-over'
  }
  
  // 将canvas转换为blob并下载
  canvas.toBlob((blob) => {
    if (blob) {
      // 创建下载链接
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `edited_image_${Date.now()}.jpg`
      
      // 触发下载
      document.body.appendChild(a)
      a.click()
      
      // 清理资源
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
      
      // 返回上一页
      emit('back')
    }
  }, 'image/jpeg')
}

// 选择作品集
const selectPortfolio = (portfolioId) => {
  selectedPortfolioId.value = portfolioId
}

// 选择保存作品集
const selectSavePortfolio = (portfolioId) => {
  selectedSavePortfolioId.value = portfolioId
}

// 获取作品集列表
const fetchPortfolios = async () => {
  isLoading.value = true
  try {
    const portfoliosData = await portfolioApi.getPortfolios()
    portfolios.value = portfoliosData
  } catch (error) {
    console.error('获取作品集列表失败:', error)
    ElMessage.error('获取作品集列表失败')
  } finally {
    isLoading.value = false
  }
}

// 导入到作品集
const importToPortfolio = async () => {
  if (!selectedPortfolioId.value) return
  
  const image = imageRef.value
  if (!image) return
  
  // 创建canvas元素
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  
  // 设置canvas尺寸
  canvas.width = image.naturalWidth
  canvas.height = image.naturalHeight
  
  // 应用滤镜效果
  // 基础滤镜计算
  const brightness = 1 + adjustments.value.brightness / 100
  const contrast = 1 + adjustments.value.contrast / 100
  const saturation = 1 + adjustments.value.saturation / 100
  
  // 组合计算：曝光影响亮度
  const finalBrightness = brightness * (1 + adjustments.value.exposure / 100)
  
  // 色温转换为色相旋转
  const hueRotate = (adjustments.value.temperature / 100) * 60 // 限制在 -60 到 60 度
  
  // 色调使用 sepia + 反相来模拟
  const sepia = Math.abs(adjustments.value.tint) / 100
  const invert = adjustments.value.tint < 0 ? Math.abs(adjustments.value.tint) / 200 : 0
  
  // 清晰度：使用锐化滤镜模拟
  const clarity = adjustments.value.clarity
  const sharpen = clarity > 0 ? clarity / 50 : 0
  const blur = clarity < 0 ? Math.abs(clarity) / 100 : 0
  
  // 构建单一滤镜字符串
  ctx.filter = `
    brightness(${finalBrightness}) 
    contrast(${contrast}) 
    saturate(${saturation}) 
    hue-rotate(${hueRotate}deg) 
    sepia(${sepia}) 
    invert(${invert}) 
    ${sharpen > 0 ? `url('data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\'><filter id=\'sharpen\'><feConvolveMatrix kernelMatrix=\'0 -${sharpen} 0 -${sharpen} ${4 * sharpen + 1} -${sharpen} 0 -${sharpen} 0\'/></filter></svg>#sharpen')` : ''} 
    blur(${blur}px) 
  `
  
  // 暗角效果需要在绘制图片后单独处理
  const drawVignette = adjustments.value.vignette > 0
  
  // 绘制图片
  ctx.drawImage(image, 0, 0)
  
  try {
    // 将canvas转换为blob
    canvas.toBlob(async (blob) => {
      if (blob) {
        // 创建FormData对象，使用正确的字段名'file'
        const formData = new FormData()
        formData.append('file', blob, `edited_image_${Date.now()}.jpg`)
        
        // 上传图片到后端
        await portfolioApi.uploadImageToPortfolio(selectedPortfolioId.value, formData)
        
        // 关闭对话框
        showPortfolioDialog.value = false
        selectedPortfolioId.value = null
        
        // 显示成功提示
        ElMessage.success('图片已成功导入作品集')
        
        // 返回上一页
        emit('back')
      }
    }, 'image/jpeg')
  } catch (error) {
    console.error('导入图片到作品集失败:', error)
    ElMessage.error('导入图片到作品集失败')
  }
}

// 保存到作品集
const saveToPortfolio = async () => {
  if (!selectedSavePortfolioId.value) return
  
  const image = imageRef.value
  if (!image) return
  
  // 创建canvas元素
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  
  // 设置canvas尺寸
  canvas.width = image.naturalWidth
  canvas.height = image.naturalHeight
  
  // 应用滤镜效果
  // 基础滤镜计算
  const brightness = 1 + adjustments.value.brightness / 100
  const contrast = 1 + adjustments.value.contrast / 100
  const saturation = 1 + adjustments.value.saturation / 100
  
  // 组合计算：曝光影响亮度
  const finalBrightness = brightness * (1 + adjustments.value.exposure / 100)
  
  // 色温转换为色相旋转
  const hueRotate = (adjustments.value.temperature / 100) * 60 // 限制在 -60 到 60 度
  
  // 色调使用 sepia + 反相来模拟
  const sepia = Math.abs(adjustments.value.tint) / 100
  const invert = adjustments.value.tint < 0 ? Math.abs(adjustments.value.tint) / 200 : 0
  
  // 清晰度：使用锐化滤镜模拟
  const clarity = adjustments.value.clarity
  const sharpen = clarity > 0 ? clarity / 50 : 0
  const blur = clarity < 0 ? Math.abs(clarity) / 100 : 0
  
  // 构建单一滤镜字符串
  ctx.filter = `
    brightness(${finalBrightness}) 
    contrast(${contrast}) 
    saturate(${saturation}) 
    hue-rotate(${hueRotate}deg) 
    sepia(${sepia}) 
    invert(${invert}) 
    ${sharpen > 0 ? `url('data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\'><filter id=\'sharpen\'><feConvolveMatrix kernelMatrix=\'0 -${sharpen} 0 -${sharpen} ${4 * sharpen + 1} -${sharpen} 0 -${sharpen} 0\'/></filter></svg>#sharpen')` : ''} 
    blur(${blur}px) 
  `
  
  // 暗角效果需要在绘制图片后单独处理
  const drawVignette = adjustments.value.vignette > 0
  
  // 绘制图片
  ctx.drawImage(image, 0, 0)
  
  // 应用暗角效果
  if (drawVignette) {
    const vignetteIntensity = adjustments.value.vignette / 100
    const centerX = canvas.width / 2
    const centerY = canvas.height / 2
    const radius = Math.max(canvas.width, canvas.height) * 0.75
    
    const gradient = ctx.createRadialGradient(centerX, centerY, radius * 0.5, centerX, centerY, radius)
    gradient.addColorStop(0, 'rgba(0, 0, 0, 0)')
    gradient.addColorStop(1, `rgba(0, 0, 0, ${vignetteIntensity})`)
    
    ctx.globalCompositeOperation = 'multiply'
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    ctx.globalCompositeOperation = 'source-over'
  }
  
  try {
    // 将canvas转换为blob
    canvas.toBlob(async (blob) => {
      if (blob) {
        // 创建FormData对象，使用正确的字段名'file'
        const formData = new FormData()
        formData.append('file', blob, `edited_image_${Date.now()}.jpg`)
        
        // 上传图片到后端
        await portfolioApi.uploadImageToPortfolio(selectedSavePortfolioId.value, formData)
        
        // 关闭对话框
        showSaveToPortfolioDialog.value = false
        selectedSavePortfolioId.value = null
        
        // 显示成功提示
        ElMessage.success('图片已成功保存到作品集')
        
        // 返回上一页
        emit('back')
      }
    }, 'image/jpeg')
  } catch (error) {
    console.error('保存图片到作品集失败:', error)
    ElMessage.error('保存图片到作品集失败')
  }
}

onMounted(() => {
  // 初始化时加载原图
  applyFilter(filters.value[0])
  // 获取作品集列表
  fetchPortfolios()
})
</script>

<style scoped>
.filter-editor-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #fff;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', Roboto, sans-serif;
}

/* 顶部导航栏 */
.editor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
  background-color: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
}

.back-btn,
.save-btn {
  font-size: 16px;
}

.back-btn {
  color: #666;
  padding: 8px;
}

.back-btn:hover {
  color: #333;
}

.header-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.save-btn {
  background-color: #0071e3;
  border: none;
  border-radius: 20px;
  padding: 8px 16px;
}

.save-btn:hover {
  background-color: #0077ed;
}

/* 编辑内容区 */
.editor-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 左侧：图片预览区 */
.preview-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fafafa;
  padding: 20px;
  overflow: auto;
}

.preview-wrapper {
  max-width: 100%;
  max-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
  transition: all 0.3s ease;
}

/* 右侧：编辑工具区 */
.tools-area {
  width: 320px;
  background-color: #fff;
  border-left: 1px solid #f0f0f0;
  overflow-y: auto;
  padding: 20px;
}

.tool-section {
  margin-bottom: 32px;
}

.tool-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

/* 滤镜选择 */
.filter-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.filter-item {
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 8px;
  overflow: hidden;
}

.filter-item:hover {
  transform: scale(1.05);
}

.filter-item.active {
  outline: 2px solid #0071e3;
}

.filter-preview {
  width: 100%;
  height: 80px;
  overflow: hidden;
  border-radius: 6px;
}

.filter-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.filter-name {
  display: block;
  text-align: center;
  font-size: 12px;
  color: #666;
  margin-top: 6px;
}

/* 调整工具 */
.adjust-item {
  margin-bottom: 24px;
}

.adjust-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
}

.adjust-value {
  font-size: 12px;
  color: #999;
  text-align: right;
  margin-top: 4px;
}

/* 重置按钮 */
.reset-btn {
  color: #0071e3;
  font-size: 12px;
  padding: 0;
}

.reset-btn:hover {
  color: #0077ed;
}

/* 作品集选择对话框 */
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

/* 顶部操作按钮 */
.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.portfolio-btn {
  background-color: white;
  border: 1px solid #e0e0e0;
  color: #666666;
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.portfolio-btn:hover {
  border-color: #0071e3;
  color: #0071e3;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .editor-content {
    flex-direction: column;
  }
  
  .tools-area {
    width: 100%;
    border-left: none;
    border-top: 1px solid #f0f0f0;
  }
  
  .filter-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .header-actions {
    gap: 8px;
  }
  
  .portfolio-btn,
  .save-btn {
    padding: 6px 12px;
    font-size: 13px;
  }
}
</style>