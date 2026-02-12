# PicMaster - 专业图片编辑管理平台

<div align="center">

![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC3F7?style=flat-square&logo=vue.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)

**一款功能强大的图片编辑与作品集管理系统，专为摄影师和设计师打造**

[功能特性](#功能特性) • [快速开始](#快速开始) • [技术架构](#技术架构) • [项目结构](#项目结构)

</div>

---

## 功能特性

### 🎨 图片编辑

- **滤镜参数调节** - 13种专业滤镜参数
  - 亮度、对比度、饱和度、色相
  - 锐化、曝光、高光、阴影
  - 色温、色调、暗角、清晰度、模糊
- **预设滤镜** - 一键应用清新、复古、日系、胶片、黑白等风格
- **实时预览** - 滤镜效果即时渲染，所见即所得
- **原图保护** - 保存时输出原始尺寸，不受预览缩放影响

### 🤖 AI智能调整

- **自然语言输入** - 输入"让照片更亮一点"、"增加电影感"等描述
- **智能参数解析** - 自动将自然语言转换为滤镜参数
- **场景优化** - 支持人像美化、风景增强、电影感等场景预设
- **快捷建议** - 一键应用常用调整效果

### 📁 作品集管理

- **作品集CRUD** - 创建、查看、编辑、删除作品集
- **图片管理** - 批量上传、拖拽排序、快速删除
- **分类标签** - 支持分类和标签管理
- **封面设置** - 自定义作品集封面图片

### 📱 作品集展示

- **网格布局** - 响应式网格展示，适配各种屏幕
- **图片预览** - 点击放大查看，支持缩放和拖拽
- **AI调整** - 展示页面直接使用AI调整图片
- **下载功能** - 一键下载处理后的图片

### 📲 分享功能

- **二维码生成** - 为作品集生成访问二维码
- **动态地址** - 自动适配当前访问地址
- **移动端适配** - 手机扫码即可查看作品集

---

## 技术架构

### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue.js | 3.x | 前端框架 |
| TypeScript | 5.x | 类型安全 |
| Vite | 6.x | 构建工具 |
| Element Plus | 2.x | UI组件库 |
| Fabric.js | 6.x | Canvas图像处理 |
| Vue Router | 4.x | 路由管理 |
| Axios | 1.x | HTTP请求 |

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 后端语言 |
| Flask | 3.x | Web框架 |
| SQLAlchemy | 2.x | ORM框架 |
| SQLite | 3 | 数据库 |
| Pillow | 10.x | 图像处理 |
| qrcode | 7.x | 二维码生成 |
| Flask-CORS | 4.x | 跨域支持 |

---

## 快速开始

### 环境要求

- Node.js >= 18.0
- Python >= 3.10
- npm >= 9.0

### 前端安装与运行

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

前端默认运行在 `http://localhost:3000`

### 后端安装与运行

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动后端服务
python app.py
```

后端默认运行在 `http://localhost:5000`

### 配置文件

**前端配置** (`frontend/.env`)：
```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_FRONTEND_URL=http://localhost:3000
```

**后端配置** (`backend/.env`)：
```env
SERVER_HOST=localhost
SERVER_PORT=5000
FRONTEND_URL=http://localhost:3000
```

---

## 项目结构

```
PicMaster/
├── frontend/                    # 前端项目
│   ├── src/
│   │   ├── api/                 # API接口封装
│   │   │   ├── index.ts         # Axios实例配置
│   │   │   └── portfolioApi.js  # 作品集API
│   │   ├── components/          # 公共组件
│   │   │   ├── FilterEditor.vue # 滤镜编辑器
│   │   │   ├── ImageEditor.vue  # 图片编辑器
│   │   │   ├── PortfolioManager.vue
│   │   │   └── PortfolioViewer.vue
│   │   ├── config/              # 配置文件
│   │   │   └── index.ts         # 环境配置
│   │   ├── layouts/             # 布局组件
│   │   ├── router/              # 路由配置
│   │   ├── store/               # 状态管理
│   │   ├── styles/              # 全局样式
│   │   ├── types/               # TypeScript类型定义
│   │   ├── utils/               # 工具函数
│   │   │   ├── errorHandler.ts  # 错误处理
│   │   │   ├── imageFilters.ts  # 图像滤镜算法
│   │   │   └── logger.ts        # 日志工具
│   │   └── views/               # 页面视图
│   │       ├── EditorView/      # 编辑器页面
│   │       ├── HomeView/        # 首页
│   │       ├── PortfolioView/   # 作品集管理
│   │       └── ViewerView/      # 作品集展示
│   ├── index.html
│   ├── vite.config.ts
│   └── package.json
│
├── backend/                     # 后端项目
│   ├── routes/                  # API路由
│   │   ├── ai.py                # AI意图解析API
│   │   ├── images.py            # 图片处理API
│   │   ├── portfolios.py        # 作品集API
│   │   └── previews.py          # 预览/二维码API
│   ├── app.py                   # Flask应用入口
│   ├── models.py                # 数据库模型
│   ├── init_db.py               # 数据库初始化
│   ├── requirements.txt         # Python依赖
│   └── .env                     # 环境配置
│
└── README.md
```

---

## API接口

### 作品集管理

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/portfolios` | 获取作品集列表 |
| GET | `/api/portfolios/:id` | 获取作品集详情 |
| POST | `/api/portfolios` | 创建作品集 |
| PUT | `/api/portfolios/:id` | 更新作品集 |
| DELETE | `/api/portfolios/:id` | 删除作品集 |
| POST | `/api/portfolios/:id/images` | 上传图片 |

### AI功能

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/ai/parse-intent` | 解析自然语言调整意图 |
| GET | `/api/ai/presets` | 获取预设风格列表 |

### 预览功能

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/previews/generate` | 生成预览二维码 |

---

## 核心算法

### 图像滤镜处理

所有滤镜均在Canvas像素级别实现，确保效果精确可控：

```typescript
// 滤镜参数接口
interface FilterParams {
  brightness: number   // 亮度: -100 ~ 100
  contrast: number     // 对比度: 0 ~ 200
  saturation: number   // 饱和度: -100 ~ 100
  hue: number          // 色相: 0 ~ 360
  sharpness: number    // 锐化: -50 ~ 50
  exposure: number     // 曝光: -100 ~ 100
  highlights: number   // 高光: -100 ~ 100
  shadows: number      // 阴影: -100 ~ 100
  temperature: number  // 色温: -50 ~ 50
  tint: number         // 色调: -50 ~ 50
  vignette: number     // 暗角: 0 ~ 100
  clarity: number      // 清晰度: -100 ~ 100
  blur: number         // 模糊: 0 ~ 20
}
```

### AI意图解析

基于规则的自然语言解析，支持：
- 关键词识别：亮度、对比度、饱和度等
- 方向词识别：增加、减少、提高、降低等
- 程度词识别：稍微、一点、很多、大幅等
- 风格预设：清新、复古、日系、胶片、黑白等
- 场景优化：人像、风景、电影感等

---

## 性能优化

- **图片懒加载** - 按需加载图片，减少初始加载时间
- **滤镜防抖** - 参数调整时50ms防抖，避免频繁重绘
- **Canvas优化** - 使用Fabric.js优化渲染性能
- **请求拦截** - 统一的错误处理和日志记录

---

## 浏览器支持

| 浏览器 | 支持版本 |
|--------|----------|
| Chrome | 最新版本 |
| Edge | 最新版本 |
| Firefox | 最新版本 |
| Safari | 最新版本 |

---

## 开发团队

**作者**: zhenianxiachi

**项目地址**: [https://github.com/zhenianxiachi/PicMaster](https://github.com/zhenianxiachi/PicMaster)

---

## License

[MIT License](LICENSE)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个Star支持一下！**

</div>
