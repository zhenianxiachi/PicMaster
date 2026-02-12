# PicMaster - 图片编辑管理系统

## 项目简介
PicMaster是一款专业的图片编辑管理系统，专为摄影师、修图师设计，支持快速导入、批量编辑、网红滤镜复刻与自定义、作品集管理、客户预览等功能。

## 技术栈

### 前端
- 框架：Vue3 + Vite
- 组件库：Element Plus
- 核心工具：Fabric.js (v5+)、Canvas API
- 辅助库：viewer.js、vue-awesome-swiper、turn.js、axios、qrcodejs2

### 后端
- 框架：Python Flask
- 数据库：MySQL / SQLite
- 核心工具：PIL/Pillow、自定义滤镜参数解析
- 辅助工具：reportlab、zipfile、Flask-CORS、PyJWT、qrcode

## 核心功能

### 图片编辑模块
- 快速导入：文件夹批量导入、拖拽导入
- 快编模式：一键切换，简化界面，适配笔记本触控板
- 网红滤镜：12项参数调节，3层滤镜叠加，实时渲染
- 预设管理：预设→微调→复刻流程，支持对比功能
- 客户预览：生成24小时有效期二维码，实时更新

### 作品集管理模块
- 作品集CRUD：按客户名称/拍摄日期自动命名
- 图片管理：批量添加（最多20张）、拖拽排序
- 标签分类：支持分类和标签管理

### 作品集展示与导出
- 三种布局：网格、轮播、分页翻书
- 客户标注：基于Canvas的标注功能
- 导出功能：PDF生成、ZIP打包、滤镜参数导出

## 安装与运行

### 前端

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

4. 构建生产版本
```bash
npm run build
```

### 后端

1. 进入后端目录
```bash
cd backend
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 初始化数据库
```bash
python init_db.py
```

4. 启动后端服务
```bash
python app.py
```

## 项目结构

```
PicMaster/
├── frontend/              # 前端代码
│   ├── src/
│   │   ├── components/    # Vue组件
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 入口文件
│   ├── index.html         # HTML模板
│   ├── vite.config.js     # Vite配置
│   └── package.json       # 前端依赖
├── backend/               # 后端代码
│   ├── routes/            # API路由
│   ├── models.py          # 数据库模型
│   ├── app.py             # Flask应用入口
│   ├── init_db.py         # 数据库初始化
│   ├── requirements.txt   # 后端依赖
│   └── .env               # 环境变量配置
└── README.md              # 项目说明
```

## 配置说明

### 后端配置
编辑 `backend/.env` 文件：

```
# 数据库配置
DATABASE_URL=sqlite:///picmaster.db  # 或使用MySQL
# DATABASE_URL=mysql+pymysql://username:password@localhost:3306/picmaster

# 应用配置
SECRET_KEY=dev-secret-key-1234567890
UPLOAD_FOLDER=uploads
TEMP_FOLDER=temp

# 应用运行配置
FLASK_ENV=development
DEBUG=True
```

## 使用说明

1. **图片编辑流程**：
   - 导入图片（文件夹或拖拽）
   - 选择滤镜预设或手动调节参数
   - 使用对比功能查看效果
   - 生成客户预览二维码
   - 保存编辑结果

2. **作品集管理**：
   - 创建作品集
   - 添加图片（批量或单个）
   - 拖拽排序图片
   - 设置分类和标签

3. **客户预览**：
   - 生成预览二维码
   - 客户扫描二维码查看作品
   - 客户可以进行标注反馈

## 性能优化

- 图片懒加载
- 滤镜参数实时渲染优化
- 大图片压缩处理
- 数据库索引优化

## 兼容性

- 浏览器：Chrome、Edge
- 设备：PC端（重点笔记本）、移动端（屏幕宽度≥360px）

## 开发注意事项

- 前端端口：3000
- 后端端口：5000
- API前缀：/api
- 跨域已配置，无需额外设置

## License

MIT
