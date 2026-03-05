export interface FilterParams {
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
  hsl?: Record<string, { hue: number; saturation: number; lightness: number }>
}

export function applyAllFilters(
  imageData: ImageData,
  params: FilterParams
): ImageData {
  const data = new Uint8ClampedArray(imageData.data)
  const width = imageData.width
  const height = imageData.height

  if (params.brightness !== 0) applyBrightness(data, params.brightness)
  if (params.contrast !== 100) applyContrast(data, params.contrast)
  if (params.saturation !== 100) applySaturation(data, params.saturation)
  if (params.hue !== 0) applyHueRotation(data, params.hue)
  if (params.exposure !== 0) applyExposure(data, params.exposure)
  if (params.highlights !== 0) applyHighlights(data, params.highlights)
  if (params.shadows !== 0) applyShadows(data, params.shadows)
  if (params.temperature !== 0) applyTemperature(data, params.temperature)
  if (params.tint !== 0) applyTint(data, params.tint)
  if (params.clarity !== 0) applyClarity(data, width, height, params.clarity)
  if (params.sharpness !== 0) applySharpness(data, width, height, params.sharpness)
  if (params.vignette !== 0) applyVignette(data, width, height, params.vignette)
  
  if (params.hsl) {
    applyHSLAdjustment(data, params.hsl)
  }

  return new ImageData(data, width, height)
}

function getPixel(data: Uint8ClampedArray, index: number): number {
  return data[index] ?? 0
}

function setPixel(data: Uint8ClampedArray, index: number, value: number): void {
  data[index] = clamp(value)
}

export function applyBrightness(
  data: Uint8ClampedArray,
  value: number
): void {
  const adjustment = (value / 100) * 255
  for (let i = 0; i < data.length; i += 4) {
    setPixel(data, i, getPixel(data, i) + adjustment)
    setPixel(data, i + 1, getPixel(data, i + 1) + adjustment)
    setPixel(data, i + 2, getPixel(data, i + 2) + adjustment)
  }
}

export function applyContrast(
  data: Uint8ClampedArray,
  value: number
): void {
  const factor = (value / 100)
  const intercept = 128 * (1 - factor)
  for (let i = 0; i < data.length; i += 4) {
    setPixel(data, i, getPixel(data, i) * factor + intercept)
    setPixel(data, i + 1, getPixel(data, i + 1) * factor + intercept)
    setPixel(data, i + 2, getPixel(data, i + 2) * factor + intercept)
  }
}

export function applySaturation(
  data: Uint8ClampedArray,
  value: number
): void {
  const saturation = value / 100
  for (let i = 0; i < data.length; i += 4) {
    const r = getPixel(data, i)
    const g = getPixel(data, i + 1)
    const b = getPixel(data, i + 2)
    
    const gray = 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    setPixel(data, i, gray + saturation * (r - gray))
    setPixel(data, i + 1, gray + saturation * (g - gray))
    setPixel(data, i + 2, gray + saturation * (b - gray))
  }
}

export function applyHueRotation(
  data: Uint8ClampedArray,
  degrees: number
): void {
  const angle = (degrees * Math.PI) / 180
  const cos = Math.cos(angle)
  const sin = Math.sin(angle)
  
  for (let i = 0; i < data.length; i += 4) {
    const r = getPixel(data, i)
    const g = getPixel(data, i + 1)
    const b = getPixel(data, i + 2)
    
    const y = 0.299 * r + 0.587 * g + 0.114 * b
    const cb = -0.168736 * r - 0.331264 * g + 0.5 * b
    const cr = 0.5 * r - 0.418688 * g - 0.081312 * b
    
    const newCb = cb * cos - cr * sin
    const newCr = cb * sin + cr * cos
    
    setPixel(data, i, y + 1.402 * newCr)
    setPixel(data, i + 1, y - 0.344136 * newCb - 0.714136 * newCr)
    setPixel(data, i + 2, y + 1.772 * newCb)
  }
}

export function applyExposure(
  data: Uint8ClampedArray,
  value: number
): void {
  const exposure = Math.pow(2, value / 100)
  for (let i = 0; i < data.length; i += 4) {
    setPixel(data, i, getPixel(data, i) * exposure)
    setPixel(data, i + 1, getPixel(data, i + 1) * exposure)
    setPixel(data, i + 2, getPixel(data, i + 2) * exposure)
  }
}

export function applyHighlights(
  data: Uint8ClampedArray,
  value: number
): void {
  const adjustment = value / 100
  for (let i = 0; i < data.length; i += 4) {
    const r = getPixel(data, i)
    const g = getPixel(data, i + 1)
    const b = getPixel(data, i + 2)
    const luminance = (r + g + b) / 3
    const highlightMask = smoothstep(0.5, 1.0, luminance / 255)
    
    const factor = 1 + adjustment * highlightMask
    setPixel(data, i, r * factor)
    setPixel(data, i + 1, g * factor)
    setPixel(data, i + 2, b * factor)
  }
}

export function applyShadows(
  data: Uint8ClampedArray,
  value: number
): void {
  const adjustment = value / 100
  for (let i = 0; i < data.length; i += 4) {
    const r = getPixel(data, i)
    const g = getPixel(data, i + 1)
    const b = getPixel(data, i + 2)
    const luminance = (r + g + b) / 3
    const shadowMask = 1 - smoothstep(0.0, 0.5, luminance / 255)
    
    const factor = 1 + adjustment * shadowMask
    setPixel(data, i, r * factor)
    setPixel(data, i + 1, g * factor)
    setPixel(data, i + 2, b * factor)
  }
}

export function applyTemperature(
  data: Uint8ClampedArray,
  value: number
): void {
  const temp = value / 100
  for (let i = 0; i < data.length; i += 4) {
    if (temp > 0) {
      setPixel(data, i, getPixel(data, i) + temp * 30)
      setPixel(data, i + 2, getPixel(data, i + 2) - temp * 30)
    } else {
      setPixel(data, i, getPixel(data, i) + temp * 30)
      setPixel(data, i + 2, getPixel(data, i + 2) - temp * 30)
    }
  }
}

export function applyTint(
  data: Uint8ClampedArray,
  value: number
): void {
  const tint = value / 100
  for (let i = 0; i < data.length; i += 4) {
    if (tint > 0) {
      setPixel(data, i, getPixel(data, i) + tint * 20)
      setPixel(data, i + 1, getPixel(data, i + 1) - tint * 10)
    } else {
      setPixel(data, i + 1, getPixel(data, i + 1) - tint * 20)
    }
  }
}

export function applyVignette(
  data: Uint8ClampedArray,
  width: number,
  height: number,
  value: number
): void {
  if (value === 0) return
  
  const centerX = width / 2
  const centerY = height / 2
  const maxDist = Math.sqrt(centerX * centerX + centerY * centerY)
  const intensity = value / 100
  
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const i = (y * width + x) * 4
      
      const dx = x - centerX
      const dy = y - centerY
      const dist = Math.sqrt(dx * dx + dy * dy)
      const normalizedDist = dist / maxDist
      
      const vignetteFactor = 1 - intensity * Math.pow(normalizedDist, 2)
      
      setPixel(data, i, getPixel(data, i) * vignetteFactor)
      setPixel(data, i + 1, getPixel(data, i + 1) * vignetteFactor)
      setPixel(data, i + 2, getPixel(data, i + 2) * vignetteFactor)
    }
  }
}

export function applySharpness(
  data: Uint8ClampedArray,
  width: number,
  height: number,
  value: number
): void {
  if (value === 0) return
  
  const strength = value / 50
  const kernel: number[] = [
    0, -strength, 0,
    -strength, 1 + 4 * strength, -strength,
    0, -strength, 0
  ]
  
  const tempData = new Uint8ClampedArray(data)
  
  for (let y = 1; y < height - 1; y++) {
    for (let x = 1; x < width - 1; x++) {
      for (let c = 0; c < 3; c++) {
        let sum = 0
        for (let ky = -1; ky <= 1; ky++) {
          for (let kx = -1; kx <= 1; kx++) {
            const idx = ((y + ky) * width + (x + kx)) * 4 + c
            const kernelIdx = (ky + 1) * 3 + (kx + 1)
            sum += getPixel(tempData, idx) * (kernel[kernelIdx] ?? 0)
          }
        }
        const idx = (y * width + x) * 4 + c
        setPixel(data, idx, sum)
      }
    }
  }
}

export function applyClarity(
  data: Uint8ClampedArray,
  width: number,
  height: number,
  value: number
): void {
  if (value === 0) return
  
  const strength = value / 100
  const tempData = new Uint8ClampedArray(data)
  
  for (let y = 1; y < height - 1; y++) {
    for (let x = 1; x < width - 1; x++) {
      const idx = (y * width + x) * 4
      
      for (let c = 0; c < 3; c++) {
        let sum = 0
        let count = 0
        
        for (let ky = -1; ky <= 1; ky++) {
          for (let kx = -1; kx <= 1; kx++) {
            if (kx === 0 && ky === 0) continue
            const neighborIdx = ((y + ky) * width + (x + kx)) * 4 + c
            sum += getPixel(tempData, neighborIdx)
            count++
          }
        }
        
        const avg = sum / count
        const currentVal = getPixel(tempData, idx + c)
        const diff = currentVal - avg
        setPixel(data, idx + c, currentVal + diff * strength * 0.5)
      }
    }
  }
}

function clamp(value: number): number {
  return Math.max(0, Math.min(255, Math.round(value)))
}

function smoothstep(edge0: number, edge1: number, x: number): number {
  const t = clamp01((x - edge0) / (edge1 - edge0))
  return t * t * (3 - 2 * t)
}

function clamp01(value: number): number {
  return Math.max(0, Math.min(1, value))
}

export function applyBlur(
  data: Uint8ClampedArray,
  width: number,
  height: number,
  radius: number
): void {
  if (radius <= 0) return
  
  const tempData = new Uint8ClampedArray(data)
  const kernelSize = Math.ceil(radius * 2) | 1
  const halfKernel = Math.floor(kernelSize / 2)
  
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let r = 0, g = 0, b = 0, count = 0
      
      for (let ky = -halfKernel; ky <= halfKernel; ky++) {
        for (let kx = -halfKernel; kx <= halfKernel; kx++) {
          const ny = y + ky
          const nx = x + kx
          
          if (ny >= 0 && ny < height && nx >= 0 && nx < width) {
            const idx = (ny * width + nx) * 4
            r += getPixel(tempData, idx)
            g += getPixel(tempData, idx + 1)
            b += getPixel(tempData, idx + 2)
            count++
          }
        }
      }
      
      const idx = (y * width + x) * 4
      setPixel(data, idx, r / count)
      setPixel(data, idx + 1, g / count)
      setPixel(data, idx + 2, b / count)
    }
  }
}

export async function processImageWithFilters(
  imageElement: HTMLImageElement | HTMLCanvasElement,
  params: FilterParams
): Promise<HTMLCanvasElement> {
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  
  if (!ctx) {
    throw new Error('无法创建Canvas上下文')
  }
  
  canvas.width = imageElement.width || (imageElement as HTMLImageElement).naturalWidth
  canvas.height = imageElement.height || (imageElement as HTMLImageElement).naturalHeight
  
  ctx.drawImage(imageElement, 0, 0)
  
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
  
  const processedData = applyAllFilters(imageData, params)
  
  ctx.putImageData(processedData, 0, 0)
  
  if (params.blur > 0) {
    const tempCanvas = document.createElement('canvas')
    tempCanvas.width = canvas.width
    tempCanvas.height = canvas.height
    const tempCtx = tempCanvas.getContext('2d')
    
    if (tempCtx) {
      tempCtx.drawImage(canvas, 0, 0)
      const blurData = tempCtx.getImageData(0, 0, canvas.width, canvas.height)
      applyBlur(blurData.data, canvas.width, canvas.height, params.blur)
      tempCtx.putImageData(blurData, 0, 0)
      ctx.drawImage(tempCanvas, 0, 0)
    }
  }
  
  return canvas
}

interface HSLColor {
  hue: number
  saturation: number
  lightness: number
}

function applyHSLAdjustment(
  data: Uint8ClampedArray,
  hslParams: Record<string, HSLColor>
): void {
  let hasAdjustment = false
  for (const colorName in hslParams) {
    const adj = hslParams[colorName]
    if (adj && (adj.hue !== 0 || adj.saturation !== 0 || adj.lightness !== 0)) {
      hasAdjustment = true
      break
    }
  }
  
  if (!hasAdjustment) return

  const colorRanges: Array<{name: string; min: number; max: number}> = [
    { name: 'red', min: -15, max: 15 },
    { name: 'orange', min: 15, max: 45 },
    { name: 'yellow', min: 45, max: 75 },
    { name: 'green', min: 75, max: 150 },
    { name: 'cyan', min: 150, max: 195 },
    { name: 'blue', min: 195, max: 255 },
    { name: 'purple', min: 255, max: 285 },
    { name: 'magenta', min: 285, max: 345 }
  ]

  const len = data.length
  for (let i = 0; i < len; i += 4) {
    const r = getPixel(data, i)
    const g = getPixel(data, i + 1)
    const b = getPixel(data, i + 2)

    const [h, s, l] = rgbToHsl(r, g, b)
    const hueDegrees = h * 360

    let normalizedHue = hueDegrees >= 345 ? hueDegrees - 360 : hueDegrees

    for (const range of colorRanges) {
      const hslAdjust = hslParams[range.name]
      if (!hslAdjust) continue
      if (hslAdjust.hue === 0 && hslAdjust.saturation === 0 && hslAdjust.lightness === 0) continue

      if (normalizedHue >= range.min && normalizedHue < range.max) {
        const newH = ((h * 360 + hslAdjust.hue) % 360) / 360
        const newS = Math.max(0, Math.min(1, s + hslAdjust.saturation / 100))
        const newL = Math.max(0, Math.min(1, l + hslAdjust.lightness / 100))

        const [newR, newG, newB] = hslToRgb(newH, newS, newL)

        setPixel(data, i, newR)
        setPixel(data, i + 1, newG)
        setPixel(data, i + 2, newB)
        break
      }
    }
  }
}

function rgbToHsl(r: number, g: number, b: number): [number, number, number] {
  r /= 255
  g /= 255
  b /= 255

  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  let h = 0
  let s = 0
  const l = (max + min) / 2

  if (max !== min) {
    const d = max - min
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min)

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

  return [h, s, l]
}

function hslToRgb(h: number, s: number, l: number): [number, number, number] {
  let r: number, g: number, b: number

  if (s === 0) {
    r = g = b = l
  } else {
    const hue2rgb = (p: number, q: number, t: number): number => {
      if (t < 0) t += 1
      if (t > 1) t -= 1
      if (t < 1 / 6) return p + (q - p) * 6 * t
      if (t < 1 / 2) return q
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6
      return p
    }

    const q = l < 0.5 ? l * (1 + s) : l + s - l * s
    const p = 2 * l - q
    r = hue2rgb(p, q, h + 1 / 3)
    g = hue2rgb(p, q, h)
    b = hue2rgb(p, q, h - 1 / 3)
  }

  return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)]
}
