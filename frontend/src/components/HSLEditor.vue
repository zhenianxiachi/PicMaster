<template>
  <div class="hsl-editor">
    <div class="hsl-header">
      <span class="hsl-title">HSL 高级调节</span>
      <el-switch v-model="targetMode" active-text="目标调整" inactive-text="滑块调整" />
    </div>
    
    <div v-if="targetMode" class="target-mode">
      <p class="target-hint">点击图片中的颜色区域进行选择</p>
      <div class="target-color" v-if="selectedColor">
        <span class="color-label">已选颜色：</span>
        <span class="color-preview" :style="{ backgroundColor: selectedColorHex }"></span>
        <span class="color-name">{{ selectedColorName }}</span>
      </div>
    </div>
    
    <div class="hsl-controls">
      <div 
        v-for="color in hslColors" 
        :key="color.name" 
        class="color-control"
        :class="{ 'active': selectedColorName === color.name }"
        @click="selectColor(color.name)"
      >
        <div class="color-header">
          <span class="color-preview" :style="{ backgroundColor: color.hex }"></span>
          <span class="color-name">{{ color.displayName }}</span>
        </div>
        
        <div class="slider-group">
          <div class="slider-item">
            <span class="slider-label">色相</span>
            <el-slider 
              v-model="hslValues[color.name].hue"
              :min="-180"
              :max="180"
              :step="1"
              @input="emitChange"
            />
            <span class="slider-value">{{ hslValues[color.name].hue > 0 ? '+' : '' }}{{ hslValues[color.name].hue }}°</span>
          </div>
          
          <div class="slider-item">
            <span class="slider-label">饱和度</span>
            <el-slider 
              v-model="hslValues[color.name].saturation"
              :min="-100"
              :max="100"
              :step="1"
              @input="emitChange"
            />
            <span class="slider-value">{{ hslValues[color.name].saturation > 0 ? '+' : '' }}{{ hslValues[color.name].saturation }}%</span>
          </div>
          
          <div class="slider-item">
            <span class="slider-label">明度</span>
            <el-slider 
              v-model="hslValues[color.name].lightness"
              :min="-100"
              :max="100"
              :step="1"
              @input="emitChange"
            />
            <span class="slider-value">{{ hslValues[color.name].lightness > 0 ? '+' : '' }}{{ hslValues[color.name].lightness }}%</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="hsl-presets">
      <span class="preset-label">预设：</span>
      <el-tag 
        v-for="preset in hslPresets" 
        :key="preset.name"
        @click="applyPreset(preset)"
        class="preset-tag"
        effect="plain"
      >
        {{ preset.name }}
      </el-tag>
    </div>
    
    <div class="hsl-actions">
      <el-button size="small" @click="resetAll">重置全部</el-button>
      <el-button size="small" type="primary" @click="applyHSL">应用</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

interface HSLValue {
  hue: number
  saturation: number
  lightness: number
}

interface HSLPreset {
  name: string
  values: Record<string, HSLValue>
}

const emit = defineEmits<{
  applyHSL: [hslData: Record<string, HSLValue>]
}>()

const targetMode = ref(false)
const selectedColorName = ref<string | null>(null)
const selectedColorHex = ref<string>('#ffffff')

const hslColors = [
  { name: 'red', displayName: '红色', hex: '#ff0000', hueRange: [-15, 15] },
  { name: 'orange', displayName: '橙色', hex: '#ff8000', hueRange: [15, 45] },
  { name: 'yellow', displayName: '黄色', hex: '#ffff00', hueRange: [45, 75] },
  { name: 'green', displayName: '绿色', hex: '#00ff00', hueRange: [75, 150] },
  { name: 'cyan', displayName: '青色', hex: '#00ffff', hueRange: [150, 195] },
  { name: 'blue', displayName: '蓝色', hex: '#0000ff', hueRange: [195, 255] },
  { name: 'purple', displayName: '紫色', hex: '#8000ff', hueRange: [255, 285] },
  { name: 'magenta', displayName: '洋红', hex: '#ff00ff', hueRange: [285, 345] }
]

const hslValues = reactive<Record<string, HSLValue>>({
  red: { hue: 0, saturation: 0, lightness: 0 },
  orange: { hue: 0, saturation: 0, lightness: 0 },
  yellow: { hue: 0, saturation: 0, lightness: 0 },
  green: { hue: 0, saturation: 0, lightness: 0 },
  cyan: { hue: 0, saturation: 0, lightness: 0 },
  blue: { hue: 0, saturation: 0, lightness: 0 },
  purple: { hue: 0, saturation: 0, lightness: 0 },
  magenta: { hue: 0, saturation: 0, lightness: 0 }
})

const hslPresets: HSLPreset[] = [
  {
    name: '暖色调',
    values: {
      red: { hue: 5, saturation: 10, lightness: 0 },
      orange: { hue: 5, saturation: 15, lightness: 5 },
      yellow: { hue: -5, saturation: 10, lightness: 0 },
      green: { hue: 0, saturation: -10, lightness: 0 },
      cyan: { hue: 0, saturation: -20, lightness: 0 },
      blue: { hue: 0, saturation: -15, lightness: 0 },
      purple: { hue: 0, saturation: -10, lightness: 0 },
      magenta: { hue: 0, saturation: -10, lightness: 0 }
    }
  },
  {
    name: '冷色调',
    values: {
      red: { hue: 0, saturation: -10, lightness: 0 },
      orange: { hue: 0, saturation: -15, lightness: 0 },
      yellow: { hue: 0, saturation: -10, lightness: 0 },
      green: { hue: -5, saturation: 5, lightness: 0 },
      cyan: { hue: 5, saturation: 15, lightness: 0 },
      blue: { hue: 5, saturation: 20, lightness: 5 },
      purple: { hue: 0, saturation: 10, lightness: 0 },
      magenta: { hue: 0, saturation: 0, lightness: 0 }
    }
  },
  {
    name: '复古胶片',
    values: {
      red: { hue: 0, saturation: -10, lightness: 5 },
      orange: { hue: 5, saturation: -5, lightness: 5 },
      yellow: { hue: 0, saturation: -15, lightness: 0 },
      green: { hue: -10, saturation: -20, lightness: -5 },
      cyan: { hue: 0, saturation: -15, lightness: 0 },
      blue: { hue: 10, saturation: -10, lightness: -5 },
      purple: { hue: 0, saturation: -10, lightness: 0 },
      magenta: { hue: 0, saturation: -5, lightness: 0 }
    }
  },
  {
    name: '鲜艳色彩',
    values: {
      red: { hue: 0, saturation: 25, lightness: 5 },
      orange: { hue: 0, saturation: 20, lightness: 5 },
      yellow: { hue: 0, saturation: 20, lightness: 0 },
      green: { hue: 0, saturation: 25, lightness: 5 },
      cyan: { hue: 0, saturation: 20, lightness: 0 },
      blue: { hue: 0, saturation: 25, lightness: 5 },
      purple: { hue: 0, saturation: 20, lightness: 0 },
      magenta: { hue: 0, saturation: 20, lightness: 5 }
    }
  }
]

const selectColor = (colorName: string) => {
  selectedColorName.value = colorName
  const color = hslColors.find(c => c.name === colorName)
  if (color) {
    selectedColorHex.value = color.hex
  }
}

const applyPreset = (preset: HSLPreset) => {
  Object.keys(preset.values).forEach(colorName => {
    hslValues[colorName] = { ...preset.values[colorName] }
  })
  emitChange()
}

const resetAll = () => {
  Object.keys(hslValues).forEach(colorName => {
    hslValues[colorName] = { hue: 0, saturation: 0, lightness: 0 }
  })
  emitChange()
}

const emitChange = () => {
  emit('applyHSL', JSON.parse(JSON.stringify(hslValues)))
}

const applyHSL = () => {
  emit('applyHSL', JSON.parse(JSON.stringify(hslValues)))
}

const detectColorFromPixel = (r: number, g: number, b: number) => {
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  const l = (max + min) / 2 / 255
  
  let h = 0
  let s = 0
  
  if (max !== min) {
    const d = max - min
    s = l > 0.5 ? d / (510 - max - min) : d / (max + min)
    
    switch (max) {
      case r:
        h = ((g - b) / d + (g < b ? 6 : 0)) / 6
        break
      case g:
        h = ((b - r) / d + 2) / 6
        break
      case b:
        h = ((r - g) / d + 4) / 6
        break
    }
  }
  
  const hue = h * 360
  
  for (const color of hslColors) {
    if (hue >= color.hueRange[0] && hue < color.hueRange[1]) {
      return color.name
    }
  }
  
  return 'red'
}

defineExpose({
  detectColorFromPixel,
  selectColor
})
</script>

<style scoped>
.hsl-editor {
  background-color: #1a1a1a;
  border-radius: 12px;
  padding: 16px;
  color: #ffffff;
}

.hsl-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.hsl-title {
  font-size: 14px;
  font-weight: 600;
}

.target-mode {
  background-color: #252525;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
}

.target-hint {
  font-size: 12px;
  color: #999;
  margin: 0 0 8px 0;
}

.target-color {
  display: flex;
  align-items: center;
  gap: 8px;
}

.color-label {
  font-size: 12px;
  color: #ccc;
}

.color-preview {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 1px solid #444;
}

.color-name {
  font-size: 12px;
  font-weight: 500;
}

.hsl-controls {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 400px;
  overflow-y: auto;
}

.color-control {
  background-color: #252525;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.color-control:hover {
  background-color: #303030;
}

.color-control.active {
  border-color: #409eff;
  background-color: #2a3a4a;
}

.color-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.color-header .color-preview {
  width: 16px;
  height: 16px;
}

.color-header .color-name {
  font-size: 13px;
  font-weight: 500;
}

.slider-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.slider-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.slider-label {
  width: 50px;
  font-size: 11px;
  color: #999;
}

.slider-item :deep(.el-slider) {
  flex: 1;
}

.slider-item :deep(.el-slider__runway) {
  background-color: #333;
  height: 4px;
}

.slider-item :deep(.el-slider__bar) {
  background-color: #409eff;
  height: 4px;
}

.slider-item :deep(.el-slider__button) {
  width: 14px;
  height: 14px;
  border-color: #409eff;
}

.slider-value {
  width: 40px;
  font-size: 11px;
  color: #ccc;
  text-align: right;
}

.hsl-presets {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
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

.hsl-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.hsl-actions :deep(.el-button) {
  border-radius: 6px;
}
</style>
