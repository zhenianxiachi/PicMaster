<template>
  <div class="hsl-editor">
    <div class="hsl-header">
      <h4>HSL 精细调色</h4>
      <p>按颜色分区调整色相、饱和度、明度。</p>
    </div>

    <div class="color-tabs">
      <button
        v-for="color in hslColors"
        :key="color.name"
        type="button"
        class="color-tab"
        :class="{ active: selectedColorName === color.name }"
        @click="selectedColorName = color.name"
      >
        <span class="dot" :style="{ backgroundColor: color.hex }"></span>
        <span>{{ color.displayName }}</span>
      </button>
    </div>

    <div class="sliders">
      <div class="slider-row">
        <div class="slider-head">
          <span>色相</span>
          <strong>{{ currentValues.hue > 0 ? '+' : '' }}{{ currentValues.hue }}°</strong>
        </div>
        <el-slider
          :model-value="currentValues.hue"
          :min="-180"
          :max="180"
          :step="1"
          @update:model-value="value => updateValue('hue', Number(value))"
        />
      </div>

      <div class="slider-row">
        <div class="slider-head">
          <span>饱和度</span>
          <strong>{{ currentValues.saturation > 0 ? '+' : '' }}{{ currentValues.saturation }}%</strong>
        </div>
        <el-slider
          :model-value="currentValues.saturation"
          :min="-100"
          :max="100"
          :step="1"
          @update:model-value="value => updateValue('saturation', Number(value))"
        />
      </div>

      <div class="slider-row">
        <div class="slider-head">
          <span>明度</span>
          <strong>{{ currentValues.lightness > 0 ? '+' : '' }}{{ currentValues.lightness }}%</strong>
        </div>
        <el-slider
          :model-value="currentValues.lightness"
          :min="-100"
          :max="100"
          :step="1"
          @update:model-value="value => updateValue('lightness', Number(value))"
        />
      </div>
    </div>

    <div class="preset-row">
      <span>预设</span>
      <el-tag
        v-for="preset in hslPresets"
        :key="preset.name"
        effect="plain"
        class="preset-tag"
        @click="applyPreset(preset.values)"
      >
        {{ preset.name }}
      </el-tag>
    </div>

    <div class="action-row">
      <el-button size="small" @click="resetAll">重置 HSL</el-button>
      <el-button size="small" type="primary" @click="emitChange">应用</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'

export interface HSLValue {
  hue: number
  saturation: number
  lightness: number
}

export type HSLData = Record<string, HSLValue>

const emit = defineEmits<{
  applyHSL: [hslData: HSLData]
}>()

const hslColors = [
  { name: 'red', displayName: '红色', hex: '#ff4d4f' },
  { name: 'orange', displayName: '橙色', hex: '#ff9f43' },
  { name: 'yellow', displayName: '黄色', hex: '#ffd93d' },
  { name: 'green', displayName: '绿色', hex: '#2ecc71' },
  { name: 'cyan', displayName: '青色', hex: '#00c9d7' },
  { name: 'blue', displayName: '蓝色', hex: '#3f8cff' },
  { name: 'purple', displayName: '紫色', hex: '#8b5cf6' },
  { name: 'magenta', displayName: '洋红', hex: '#ff4da6' },
] as const

const createDefaultHslValues = (): HSLData => ({
  red: { hue: 0, saturation: 0, lightness: 0 },
  orange: { hue: 0, saturation: 0, lightness: 0 },
  yellow: { hue: 0, saturation: 0, lightness: 0 },
  green: { hue: 0, saturation: 0, lightness: 0 },
  cyan: { hue: 0, saturation: 0, lightness: 0 },
  blue: { hue: 0, saturation: 0, lightness: 0 },
  purple: { hue: 0, saturation: 0, lightness: 0 },
  magenta: { hue: 0, saturation: 0, lightness: 0 },
})

const hslValues = reactive<HSLData>(createDefaultHslValues())
const selectedColorName = ref<keyof HSLData>('red')

const currentValues = computed(() => hslValues[selectedColorName.value])

const hslPresets: Array<{ name: string; values: HSLData }> = [
  {
    name: '暖色增强',
    values: {
      red: { hue: 4, saturation: 12, lightness: 2 },
      orange: { hue: 6, saturation: 16, lightness: 4 },
      yellow: { hue: -6, saturation: 8, lightness: 0 },
      green: { hue: 0, saturation: -10, lightness: 0 },
      cyan: { hue: 0, saturation: -18, lightness: 0 },
      blue: { hue: 0, saturation: -14, lightness: 0 },
      purple: { hue: 0, saturation: -8, lightness: 0 },
      magenta: { hue: 0, saturation: -8, lightness: 0 },
    },
  },
  {
    name: '冷调电影',
    values: {
      red: { hue: 0, saturation: -12, lightness: 0 },
      orange: { hue: 0, saturation: -16, lightness: 0 },
      yellow: { hue: 0, saturation: -12, lightness: -2 },
      green: { hue: -5, saturation: 6, lightness: 0 },
      cyan: { hue: 6, saturation: 14, lightness: 0 },
      blue: { hue: 6, saturation: 18, lightness: 4 },
      purple: { hue: 0, saturation: 10, lightness: 0 },
      magenta: { hue: 0, saturation: 0, lightness: 0 },
    },
  },
  {
    name: '高饱和',
    values: {
      red: { hue: 0, saturation: 24, lightness: 4 },
      orange: { hue: 0, saturation: 20, lightness: 4 },
      yellow: { hue: 0, saturation: 18, lightness: 0 },
      green: { hue: 0, saturation: 22, lightness: 4 },
      cyan: { hue: 0, saturation: 20, lightness: 0 },
      blue: { hue: 0, saturation: 24, lightness: 4 },
      purple: { hue: 0, saturation: 20, lightness: 0 },
      magenta: { hue: 0, saturation: 18, lightness: 4 },
    },
  },
]

const cloneHslValues = (): HSLData => JSON.parse(JSON.stringify(hslValues)) as HSLData

const emitChange = (): void => {
  emit('applyHSL', cloneHslValues())
}

const updateValue = (field: keyof HSLValue, value: number): void => {
  hslValues[selectedColorName.value][field] = value
  emitChange()
}

const applyPreset = (values: HSLData): void => {
  for (const key of Object.keys(hslValues) as Array<keyof HSLData>) {
    hslValues[key] = { ...values[key] }
  }
  emitChange()
}

const resetAll = (): void => {
  const defaults = createDefaultHslValues()
  for (const key of Object.keys(hslValues) as Array<keyof HSLData>) {
    hslValues[key] = defaults[key]
  }
  emitChange()
}
</script>

<style scoped>
.hsl-editor {
  border: 1px solid var(--pm-border);
  border-radius: 12px;
  background: #ffffff;
  padding: 12px;
}

.hsl-header h4 {
  color: #1f4a73;
  font-size: 14px;
}

.hsl-header p {
  margin-top: 4px;
  color: #607b96;
  font-size: 12px;
}

.color-tabs {
  margin-top: 10px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 6px;
}

.color-tab {
  border: 1px solid #cfe0ef;
  border-radius: 10px;
  background: #f8fbff;
  color: #395a79;
  font-size: 12px;
  font-weight: 700;
  padding: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  cursor: pointer;
}

.color-tab.active {
  border-color: #1493dc;
  background: #ebf6ff;
  color: #1b4c77;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.sliders {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.slider-row {
  border: 1px solid #d9e7f3;
  border-radius: 10px;
  background: #fbfdff;
  padding: 8px;
}

.slider-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.slider-head span {
  color: #406381;
  font-size: 12px;
  font-weight: 700;
}

.slider-head strong {
  color: #5c7894;
  font-size: 12px;
}

.preset-row {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
}

.preset-row > span {
  color: #627b95;
  font-size: 12px;
  font-weight: 700;
}

.preset-tag {
  cursor: pointer;
}

.action-row {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

@media (max-width: 760px) {
  .color-tabs {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
