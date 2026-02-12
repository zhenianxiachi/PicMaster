<template>
  <div class="portfolio-viewer-container">
    <div class="select-section">
      <el-select
        v-model="selectedPortfolioId"
        placeholder="选择作品集"
        class="portfolio-select"
        @change="loadPortfolio"
      >
        <el-option
          v-for="portfolio in portfolios"
          :key="portfolio.id"
          :label="portfolio.name"
          :value="portfolio.id"
        />
      </el-select>

      <div class="layout-switch">
        <div class="layout-options">
          <button
            v-for="layout in layoutOptions"
            :key="layout.id"
            class="layout-btn"
            :class="{ active: layoutMode === layout.id }"
            @click="layoutMode = layout.id"
          >
            <el-icon><component :is="layout.icon" /></el-icon>
            <span>{{ layout.name }}</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="currentPortfolio" class="display-section">
      <div v-if="layoutMode === 'grid'" class="grid-layout">
        <div
          v-for="image in currentPortfolio.images"
          :key="image.id"
          class="grid-item"
          @click="showImagePreview(image)"
        >
          <img :src="image.url" alt="作品集图片" loading="lazy" />
          <div class="grid-overlay">
            <el-icon><ZoomIn /></el-icon>
          </div>
        </div>
      </div>

      <div v-else-if="layoutMode === 'carousel'" class="carousel-layout">
        <swiper :options="swiperOptions" ref="swiperRef" class="carousel-swiper">
          <swiper-slide v-for="image in currentPortfolio.images" :key="image.id">
            <div class="carousel-slide">
              <img :src="image.url" alt="作品集图片" class="carousel-image" />
            </div>
          </swiper-slide>
          <div class="swiper-pagination" slot="pagination"></div>
          <div class="swiper-button-prev" slot="button-prev">
            <el-icon><ArrowLeft /></el-icon>
          </div>
          <div class="swiper-button-next" slot="button-next">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </swiper>
      </div>

      <div v-else-if="layoutMode === 'book'" class="book-layout">
        <div class="book-container">
          <div v-for="(image, index) in currentPortfolio.images" :key="image.id" class="book-page">
            <img :src="image.url" alt="作品集图片" />
          </div>
        </div>
      </div>
    </div>

    <el-dialog
      v-model="showPreviewDialog"
      title="图片预览"
      width="80%"
      class="preview-dialog"
      :show-close="true"
      append-to-body
      center
    >
      <div class="image-preview">
        <div v-if="currentPreviewImage" class="preview-container">
          <img :src="currentPreviewImage" alt="预览图片" class="preview-image" />
          <canvas ref="annotationCanvas" class="annotation-canvas"></canvas>
        </div>
      </div>

      <div class="annotation-tools">
        <button class="tool-btn" @click="startAnnotation">
          <el-icon><Edit /></el-icon>
          开始标注
        </button>
        <button class="tool-btn" @click="clearAnnotation">
          <el-icon><Delete /></el-icon>
          清除标注
        </button>
        <button class="tool-btn primary" @click="saveAnnotation">
          <el-icon><Check /></el-icon>
          保存标注
        </button>
        <el-color-picker v-model="annotationColor" size="small" />
        <el-input-number v-model="annotationSize" :min="1" :max="20" size="small" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick, type Ref } from 'vue'
import {
  ZoomIn,
  ArrowLeft,
  ArrowRight,
  Edit,
  Delete,
  Check,
  Menu,
  View,
  Document,
} from '@element-plus/icons-vue'
import SwiperClass from 'swiper'
import 'swiper/css'
import 'viewerjs/dist/viewer.css'

/**
 * 作品集图片类型
 */
interface PortfolioImage {
  id: number
  url: string
}

/**
 * 作品集类型
 */
interface Portfolio {
  id: number
  name: string
  images: PortfolioImage[]
}

/**
 * 布局选项类型
 */
interface LayoutOption {
  id: string
  name: string
  icon: string
}

/**
 * 标注数据类型
 */
interface AnnotationData {
  id: number
  image_url: string | null
  annotation_data: string
  created_at: string
}

const portfolios: Ref<Portfolio[]> = ref([])
const selectedPortfolioId: Ref<number | null> = ref(null)
const currentPortfolio: Ref<Portfolio | null> = ref(null)
const layoutMode: Ref<string> = ref('grid')
const swiperRef: Ref<any> = ref(null)
const showPreviewDialog: Ref<boolean> = ref(false)
const currentPreviewImage: Ref<string | null> = ref(null)
const annotationCanvas: Ref<HTMLCanvasElement | null> = ref(null)
const isAnnotating: Ref<boolean> = ref(false)
const annotationColor: Ref<string> = ref('#ff3b30')
const annotationSize: Ref<number> = ref(5)
const annotations: Ref<AnnotationData[]> = ref([])

const layoutOptions: LayoutOption[] = [
  { id: 'grid', name: '网格', icon: Menu },
  { id: 'carousel', name: '轮播', icon: View },
  { id: 'book', name: '翻书', icon: Document },
]

const swiperOptions = {
  spaceBetween: 30,
  centeredSlides: true,
  autoplay: {
    delay: 4000,
    disableOnInteraction: false,
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
}

const mockPortfolios = [
  {
    id: 1,
    name: '客户A-20240101',
    images: [
      { id: 1, url: 'https://picsum.photos/800/600?random=1' },
      { id: 2, url: 'https://picsum.photos/800/600?random=2' },
      { id: 3, url: 'https://picsum.photos/800/600?random=3' },
      { id: 4, url: 'https://picsum.photos/800/600?random=4' },
      { id: 5, url: 'https://picsum.photos/800/600?random=5' },
      { id: 6, url: 'https://picsum.photos/800/600?random=6' },
    ],
  },
  {
    id: 2,
    name: '客户B-20240201',
    images: [
      { id: 7, url: 'https://picsum.photos/800/600?random=7' },
      { id: 8, url: 'https://picsum.photos/800/600?random=8' },
      { id: 9, url: 'https://picsum.photos/800/600?random=9' },
      { id: 10, url: 'https://picsum.photos/800/600?random=10' },
    ],
  },
]

const initData = () => {
  portfolios.value = mockPortfolios
  if (portfolios.value.length > 0) {
    selectedPortfolioId.value = portfolios.value[0].id
    loadPortfolio()
  }
}

const loadPortfolio = () => {
  const portfolio = portfolios.value.find(p => p.id === selectedPortfolioId.value)
  if (portfolio) {
    currentPortfolio.value = portfolio
  }
}

const showImagePreview = (image: PortfolioImage): void => {
  currentPreviewImage.value = image.url
  showPreviewDialog.value = true
  nextTick(() => {
    initAnnotationCanvas()
  })
}

const initAnnotationCanvas = (): void => {
  const canvas = annotationCanvas.value
  if (!canvas) return

  const img = document.querySelector('.preview-image')
  if (img) {
    canvas.width = img.clientWidth
    canvas.height = img.clientHeight

    canvas.style.position = 'absolute'
    canvas.style.top = '0'
    canvas.style.left = '0'

    initCanvasEvents()
  }
}

const initCanvasEvents = (): void => {
  const canvas = annotationCanvas.value
  if (!canvas) return

  let isDrawing = false
  let lastX = 0
  let lastY = 0

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  canvas.addEventListener('mousedown', e => {
    if (!isAnnotating.value) return

    isDrawing = true
    const rect = canvas.getBoundingClientRect()
    lastX = e.clientX - rect.left
    lastY = e.clientY - rect.top
  })

  canvas.addEventListener('mousemove', e => {
    if (!isDrawing || !isAnnotating.value) return

    const rect = canvas.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    ctx.beginPath()
    ctx.moveTo(lastX, lastY)
    ctx.lineTo(x, y)
    ctx.strokeStyle = annotationColor.value
    ctx.lineWidth = annotationSize.value
    ctx.lineCap = 'round'
    ctx.lineJoin = 'round'
    ctx.stroke()

    lastX = x
    lastY = y
  })

  canvas.addEventListener('mouseup', () => {
    isDrawing = false
  })

  canvas.addEventListener('mouseleave', () => {
    isDrawing = false
  })
}

const startAnnotation = () => {
  isAnnotating.value = true
}

const clearAnnotation = (): void => {
  const canvas = annotationCanvas.value
  if (canvas) {
    const ctx = canvas.getContext('2d')
    if (ctx) {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
    }
  }
}

const saveAnnotation = (): void => {
  const canvas = annotationCanvas.value
  if (canvas) {
    const dataURL = canvas.toDataURL('image/png')
    const annotation: AnnotationData = {
      id: Date.now(),
      image_url: currentPreviewImage.value,
      annotation_data: dataURL,
      created_at: new Date().toLocaleString(),
    }
    annotations.value.push(annotation)
  }
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

.layout-options {
  display: flex;
  gap: 8px;
  background-color: #f5f5f7;
  padding: 4px;
  border-radius: 980px;
}

.layout-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 20px;
  border: none;
  border-radius: 980px;
  background-color: transparent;
  color: #86868b;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.layout-btn:hover {
  color: #1d1d1f;
}

.layout-btn.active {
  background-color: white;
  color: #1d1d1f;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
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

.carousel-layout {
  max-width: 900px;
  margin: 0 auto;
}

.carousel-swiper {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.carousel-slide {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f7;
  min-height: 500px;
}

.carousel-image {
  max-width: 100%;
  max-height: 500px;
  object-fit: contain;
  border-radius: 12px;
}

:deep(.swiper-pagination) {
  bottom: 20px;
}

:deep(.swiper-pagination-bullet) {
  width: 8px;
  height: 8px;
  background-color: #86868b;
  opacity: 1;
  border-radius: 50%;
  transition: all 0.3s ease;
}

:deep(.swiper-pagination-bullet-active) {
  background-color: #0071e3;
  width: 24px;
  border-radius: 4px;
}

:deep(.swiper-button-prev),
:deep(.swiper-button-next) {
  color: white;
  background-color: rgba(0, 0, 0, 0.2);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

:deep(.swiper-button-prev:hover),
:deep(.swiper-button-next:hover) {
  background-color: rgba(0, 0, 0, 0.4);
}

:deep(.swiper-button-prev:after),
:deep(.swiper-button-next:after) {
  font-size: 16px;
  font-weight: 600;
}

.book-layout {
  max-width: 800px;
  margin: 0 auto;
}

.book-container {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding: 20px;
  scroll-snap-type: x mandatory;
}

.book-page {
  flex: 0 0 auto;
  width: 350px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  scroll-snap-align: center;
  transition: transform 0.3s ease;
}

.book-page:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.book-page img {
  width: 100%;
  height: auto;
  display: block;
}

.image-preview {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 500px;
}

.preview-container {
  position: relative;
  max-width: 100%;
}

.preview-image {
  max-width: 100%;
  max-height: 600px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.annotation-canvas {
  cursor: crosshair;
  pointer-events: auto;
}

.annotation-tools {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
  flex-wrap: wrap;
  align-items: center;
}

.tool-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border: 1px solid #e5e5ea;
  border-radius: 980px;
  background-color: white;
  font-size: 14px;
  font-weight: 500;
  color: #1d1d1f;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tool-btn:hover {
  border-color: #0071e3;
  background-color: #f0f7ff;
  color: #0071e3;
}

.tool-btn.primary {
  background-color: #0071e3;
  border-color: #0071e3;
  color: white;
}

.tool-btn.primary:hover {
  background-color: #0077ed;
  border-color: #0077ed;
}

:deep(.preview-dialog .el-dialog) {
  border-radius: 20px;
  overflow: hidden;
}

:deep(.preview-dialog .el-dialog__header) {
  padding: 24px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.preview-dialog .el-dialog__title) {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
}

@media (max-width: 768px) {
  .select-section {
    flex-direction: column;
    align-items: flex-start;
  }

  .layout-options {
    width: 100%;
    justify-content: center;
  }

  .grid-layout {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
  }

  .book-page {
    width: 280px;
  }
}
</style>
