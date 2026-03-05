<template>
  <div class="curves-editor">
    <div class="curves-header">
      <span class="curves-title">曲线调整</span>
      <div class="channel-selector">
        <el-radio-group v-model="currentChannel" size="small">
          <el-radio-button label="rgb">RGB</el-radio-button>
          <el-radio-button label="r">R</el-radio-button>
          <el-radio-button label="g">G</el-radio-button>
          <el-radio-button label="b">B</el-radio-button>
        </el-radio-group>
      </div>
    </div>
    
    <div class="curves-canvas-container">
      <canvas 
        ref="curvesCanvas" 
        class="curves-canvas"
        @mousedown="startDrag"
        @mousemove="handleDrag"
        @mouseup="endDrag"
        @mouseleave="endDrag"
      ></canvas>
      <div class="curves-grid">
        <div class="grid-line horizontal" v-for="i in 4" :key="'h'+i" :style="{top: (i * 25) + '%'}"></div>
        <div class="grid-line vertical" v-for="i in 4" :key="'v'+i" :style="{left: (i * 25) + '%'}"></div>
      </div>
    </div>
    
    <div class="curves-presets">
      <span class="preset-label">预设：</span>
      <el-tag 
        v-for="preset in curvePresets" 
        :key="preset.name"
        @click="applyPreset(preset)"
        class="preset-tag"
        effect="plain"
      >
        {{ preset.name }}
      </el-tag>
    </div>
    
    <div class="curves-actions">
      <el-button size="small" @click="resetCurve">重置</el-button>
      <el-button size="small" type="primary" @click="applyCurve">应用</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'

interface CurvePoint {
  x: number
  y: number
}

interface CurvePreset {
  name: string
  points: CurvePoint[]
}

const props = defineProps<{
  currentParams?: Record<string, number>
}>()

const emit = defineEmits<{
  applyCurve: [curveData: { channel: string; points: CurvePoint[]; lut: number[] }]
}>()

const curvesCanvas = ref<HTMLCanvasElement | null>(null)
const currentChannel = ref<string>('rgb')

const curvePoints = ref<Record<string, CurvePoint[]>>({
  rgb: [{ x: 0, y: 255 }, { x: 255, y: 0 }],
  r: [{ x: 0, y: 255 }, { x: 255, y: 0 }],
  g: [{ x: 0, y: 255 }, { x: 255, y: 0 }],
  b: [{ x: 0, y: 255 }, { x: 255, y: 0 }]
})

const isDragging = ref(false)
const dragPointIndex = ref<number>(-1)

const curvePresets: CurvePreset[] = [
  { name: '线性', points: [{ x: 0, y: 255 }, { x: 255, y: 0 }] },
  { name: '高对比', points: [{ x: 0, y: 255 }, { x: 64, y: 200 }, { x: 192, y: 55 }, { x: 255, y: 0 }] },
  { name: '低对比', points: [{ x: 0, y: 230 }, { x: 255, y: 25 }] },
  { name: '提亮', points: [{ x: 0, y: 230 }, { x: 128, y: 100 }, { x: 255, y: 0 }] },
  { name: '压暗', points: [{ x: 0, y: 255 }, { x: 128, y: 155 }, { x: 255, y: 25 }] },
  { name: '反相', points: [{ x: 0, y: 0 }, { x: 255, y: 255 }] },
  { name: 'S曲线', points: [{ x: 0, y: 255 }, { x: 64, y: 210 }, { x: 192, y: 45 }, { x: 255, y: 0 }] }
]

const channelColors: Record<string, string> = {
  rgb: '#ffffff',
  r: '#ff4444',
  g: '#44ff44',
  b: '#4444ff'
}

const drawCurve = () => {
  if (!curvesCanvas.value) return
  
  const canvas = curvesCanvas.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  
  const width = canvas.width
  const height = canvas.height
  
  ctx.clearRect(0, 0, width, height)
  
  ctx.strokeStyle = '#333333'
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.moveTo(0, height)
  ctx.lineTo(width, 0)
  ctx.stroke()
  
  const points = curvePoints.value[currentChannel.value]
  const color = channelColors[currentChannel.value]
  
  ctx.strokeStyle = color
  ctx.lineWidth = 2
  ctx.beginPath()
  
  const sortedPoints = [...points].sort((a, b) => a.x - b.x)
  
  if (sortedPoints.length >= 2) {
    const lut = calculateLUT(sortedPoints)
    
    ctx.moveTo(0, height - lut[0])
    for (let i = 1; i < 256; i++) {
      ctx.lineTo(i, height - lut[i])
    }
  }
  
  ctx.stroke()
  
  sortedPoints.forEach((point, index) => {
    ctx.beginPath()
    ctx.arc(point.x, height - point.y, 6, 0, Math.PI * 2)
    ctx.fillStyle = index === dragPointIndex.value ? '#ffffff' : color
    ctx.fill()
    ctx.strokeStyle = '#000000'
    ctx.lineWidth = 1
    ctx.stroke()
  })
}

const calculateLUT = (points: CurvePoint[]): number[] => {
  const lut: number[] = new Array(256)
  const sortedPoints = [...points].sort((a, b) => a.x - b.x)
  
  for (let i = 0; i < 256; i++) {
    let y = 255 - i
    
    for (let j = 0; j < sortedPoints.length - 1; j++) {
      const p1 = sortedPoints[j]
      const p2 = sortedPoints[j + 1]
      
      if (i >= p1.x && i <= p2.x) {
        const t = (i - p1.x) / (p2.x - p1.x)
        y = 255 - (p1.y + t * (p2.y - p1.y))
        break
      }
    }
    
    lut[i] = Math.max(0, Math.min(255, Math.round(y)))
  }
  
  return lut
}

const getCanvasPoint = (e: MouseEvent): CurvePoint => {
  if (!curvesCanvas.value) return { x: 0, y: 0 }
  
  const rect = curvesCanvas.value.getBoundingClientRect()
  const x = Math.round(e.clientX - rect.left)
  const y = Math.round(rect.height - (e.clientY - rect.top))
  
  return { 
    x: Math.max(0, Math.min(255, x)), 
    y: Math.max(0, Math.min(255, y)) 
  }
}

const findNearestPoint = (point: CurvePoint): number => {
  const points = curvePoints.value[currentChannel.value]
  let nearestIndex = -1
  let minDistance = 15
  
  points.forEach((p, index) => {
    const distance = Math.sqrt(Math.pow(p.x - point.x, 2) + Math.pow(p.y - point.y, 2))
    if (distance < minDistance) {
      minDistance = distance
      nearestIndex = index
    }
  })
  
  return nearestIndex
}

const startDrag = (e: MouseEvent) => {
  const point = getCanvasPoint(e)
  const nearestIndex = findNearestPoint(point)
  
  if (nearestIndex >= 0) {
    isDragging.value = true
    dragPointIndex.value = nearestIndex
  } else if (curvePoints.value[currentChannel.value].length < 14) {
    curvePoints.value[currentChannel.value].push(point)
    isDragging.value = true
    dragPointIndex.value = curvePoints.value[currentChannel.value].length - 1
    drawCurve()
  }
}

const handleDrag = (e: MouseEvent) => {
  if (!isDragging.value || dragPointIndex.value < 0) return
  
  const point = getCanvasPoint(e)
  curvePoints.value[currentChannel.value][dragPointIndex.value] = point
  drawCurve()
}

const endDrag = () => {
  isDragging.value = false
  dragPointIndex.value = -1
}

const applyPreset = (preset: CurvePreset) => {
  curvePoints.value[currentChannel.value] = JSON.parse(JSON.stringify(preset.points))
  drawCurve()
}

const resetCurve = () => {
  curvePoints.value[currentChannel.value] = [{ x: 0, y: 255 }, { x: 255, y: 0 }]
  drawCurve()
}

const applyCurve = () => {
  const points = curvePoints.value[currentChannel.value]
  const lut = calculateLUT(points)
  
  emit('applyCurve', {
    channel: currentChannel.value,
    points: JSON.parse(JSON.stringify(points)),
    lut
  })
}

onMounted(() => {
  nextTick(() => {
    if (curvesCanvas.value) {
      curvesCanvas.value.width = 256
      curvesCanvas.value.height = 256
      drawCurve()
    }
  })
})

watch(currentChannel, () => {
  drawCurve()
})
</script>

<style scoped>
.curves-editor {
  background-color: #1a1a1a;
  border-radius: 12px;
  padding: 16px;
  color: #ffffff;
}

.curves-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.curves-title {
  font-size: 14px;
  font-weight: 600;
}

.channel-selector :deep(.el-radio-button__inner) {
  background-color: #333;
  border-color: #444;
  color: #fff;
  padding: 6px 12px;
}

.channel-selector :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background-color: #409eff;
  border-color: #409eff;
}

.curves-canvas-container {
  position: relative;
  width: 256px;
  height: 256px;
  margin: 0 auto 16px;
  background-color: #0a0a0a;
  border-radius: 8px;
  overflow: hidden;
}

.curves-canvas {
  position: absolute;
  top: 0;
  left: 0;
  cursor: crosshair;
  z-index: 2;
}

.curves-grid {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.grid-line {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.1);
}

.grid-line.horizontal {
  width: 100%;
  height: 1px;
}

.grid-line.vertical {
  width: 1px;
  height: 100%;
}

.curves-presets {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.preset-label {
  font-size: 12px;
  color: #999;
}

.preset-tag {
  cursor: pointer;
  font-size: 12px;
  border-radius: 4px;
}

.preset-tag:hover {
  background-color: #409eff;
  color: #fff;
  border-color: #409eff;
}

.curves-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.curves-actions :deep(.el-button) {
  border-radius: 6px;
}
</style>
