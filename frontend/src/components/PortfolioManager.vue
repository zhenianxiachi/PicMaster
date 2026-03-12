<template>
  <section class="portfolio-manager">
    <div class="summary-grid">
      <article class="summary-card">
        <span>作品集总数</span>
        <strong>{{ portfolioCount }}</strong>
      </article>
      <article class="summary-card">
        <span>图片总量</span>
        <strong>{{ totalImageCount }}</strong>
      </article>
      <article class="summary-card">
        <span>最近更新</span>
        <strong>{{ latestUpdate }}</strong>
      </article>
    </div>

    <div class="toolbar-card">
      <div class="toolbar-left">
        <h2>作品集列表</h2>
        <p>点击行可进入详情管理，支持图片上传与拖拽排序。</p>
      </div>
      <div class="toolbar-right">
        <el-button class="ghost-btn" @click="refreshAll" :loading="isLoading">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
        <el-button class="primary-btn" @click="openCreateDialog">
          <el-icon><Plus /></el-icon>
          新建作品集
        </el-button>
      </div>
    </div>

    <div class="table-card">
      <el-table :data="portfolios" v-loading="isLoading" @row-click="openDetail" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="作品集名称" min-width="220" show-overflow-tooltip>
          <template #default="{ row }">
            <div class="name-cell">
              <el-icon><FolderOpened /></el-icon>
              <span>{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="client_name" label="客户" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">
            <div class="meta-cell">
              <el-icon><User /></el-icon>
              <span>{{ row.client_name || '-' }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="shoot_date" label="拍摄日期" width="140">
          <template #default="{ row }">
            <div class="meta-cell compact">
              <el-icon><Calendar /></el-icon>
              <span>{{ formatDate(row.shoot_date) }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="image_count" label="图片数量" width="120" align="center">
          <template #default="{ row }">
            <el-tag effect="plain" class="count-tag">{{ getImageCount(row) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="170">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right" align="right">
          <template #default="{ row }">
            <div class="actions" @click.stop>
              <el-button link type="primary" @click="openDetail(row)">
                <el-icon><View /></el-icon>
                详情
              </el-button>
              <el-button link type="primary" @click="openEditDialog(row)">
                <el-icon><EditPen /></el-icon>
                编辑
              </el-button>
              <el-button link type="danger" @click="removePortfolio(row)">
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog
      v-model="showCreateDialog"
      :title="isEditing ? '编辑作品集' : '新建作品集'"
      width="min(720px, 92vw)"
      class="portfolio-dialog"
      @closed="resetForm"
    >
      <el-form ref="formRef" :model="portfolioForm" :rules="formRules" label-position="top" class="form-grid">
        <el-form-item label="作品集名称" prop="name">
          <el-input v-model="portfolioForm.name" placeholder="例如：春季婚礼主片" maxlength="50" show-word-limit />
        </el-form-item>
        <el-form-item label="客户名称" prop="client_name">
          <el-input v-model="portfolioForm.client_name" placeholder="请输入客户名称" maxlength="50" show-word-limit />
        </el-form-item>
        <el-form-item label="拍摄日期" prop="shoot_date">
          <el-date-picker
            v-model="portfolioForm.shoot_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="选择拍摄日期"
            class="full-width"
          />
        </el-form-item>
        <el-form-item label="作品分类">
          <el-select v-model="portfolioForm.category_id" placeholder="选择分类" clearable class="full-width">
            <el-option v-for="category in categories" :key="category.id" :label="category.name" :value="category.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="portfolioForm.tag_ids" multiple collapse-tags collapse-tags-tooltip placeholder="选择标签" class="full-width">
            <el-option v-for="tag in tags" :key="tag.id" :label="tag.name" :value="tag.id" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" :loading="isSubmitting" @click="savePortfolio">保存</el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog
      v-model="showDetailDialog"
      title="作品详情管理"
      width="min(1160px, 94vw)"
      class="portfolio-dialog"
      @closed="onCloseDetail"
    >
      <div v-loading="isDetailLoading" class="detail-layout">
        <template v-if="currentPortfolio">
          <header class="detail-header">
            <div>
              <h3>{{ currentPortfolio.name }}</h3>
              <p>{{ currentPortfolio.client_name || '未填写客户' }} · {{ formatDate(currentPortfolio.shoot_date) }}</p>
            </div>
            <el-tag class="image-tag" type="info" effect="plain">
              {{ currentPortfolio.images.length }} 张图片
            </el-tag>
          </header>

          <section class="upload-panel">
            <div class="upload-heading">
              <h4>上传图片</h4>
              <p>支持多图选择，上传后可直接拖拽调整展示顺序。</p>
            </div>
            <div class="upload-body">
              <el-upload
                ref="uploadRef"
                class="upload-area"
                list-type="picture-card"
                :auto-upload="false"
                :multiple="true"
                :limit="24"
                :file-list="uploadFileList"
                :on-change="handleFileSelect"
                :on-remove="handleFileRemove"
                accept="image/*"
              >
                <el-icon><Plus /></el-icon>
              </el-upload>

              <el-button
                type="primary"
                class="upload-btn"
                :disabled="uploadFileList.length === 0"
                :loading="isUploading"
                @click="uploadSelectedImages"
              >
                <el-icon><UploadFilled /></el-icon>
                上传已选图片
              </el-button>
            </div>
          </section>

          <section class="gallery-panel">
            <div class="gallery-header">
              <h4>图片管理</h4>
              <p>拖拽卡片即可调整排序，排序会实时同步。</p>
            </div>

            <div v-if="currentPortfolio.images.length" class="image-grid">
              <article
                v-for="(image, index) in currentPortfolio.images"
                :key="image.id"
                class="image-card"
                draggable="true"
                @dragstart="dragStart(index)"
                @dragover.prevent
                @drop="drop(index)"
              >
                <img :src="image.thumbnail_path || image.filepath" :alt="image.filename || `image-${image.id}`" />
                <div class="image-info">
                  <span>#{{ index + 1 }}</span>
                  <button type="button" class="remove-btn" @click.stop="deleteImage(image.id)">
                    删除
                  </button>
                </div>
              </article>
            </div>
            <div v-else class="empty-gallery">
              当前还没有图片，先上传一些素材吧。
            </div>
          </section>
        </template>
      </div>
    </el-dialog>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import {
  ElMessage,
  ElMessageBox,
  type FormInstance,
  type FormRules,
  type UploadProps,
  type UploadUserFile,
  type UploadInstance,
} from 'element-plus'
import {
  Calendar,
  CollectionTag,
  Delete,
  EditPen,
  FolderOpened,
  Plus,
  Refresh,
  UploadFilled,
  User,
  View,
} from '@element-plus/icons-vue'
import { imageApi, portfolioApi } from '@/api/portfolioApi'

interface Category {
  id: number
  name: string
}

interface Tag {
  id: number
  name: string
}

interface PortfolioImage {
  id: number
  filename?: string
  filepath: string
  thumbnail_path?: string
  sort_order?: number
}

interface PortfolioItem {
  id: number
  name: string
  client_name?: string
  shoot_date?: string
  image_count?: number
  created_at?: string
  category_id?: number | null
  tags?: Array<number | Tag>
  images?: PortfolioImage[]
}

interface PortfolioDetail extends PortfolioItem {
  images: PortfolioImage[]
}

interface PortfolioForm {
  name: string
  client_name: string
  shoot_date: string
  category_id: number | null
  tag_ids: number[]
  user_id: number
}

const portfolios = ref<PortfolioItem[]>([])
const categories = ref<Category[]>([])
const tags = ref<Tag[]>([])

const isLoading = ref(false)
const isSubmitting = ref(false)
const isDetailLoading = ref(false)
const isUploading = ref(false)

const showCreateDialog = ref(false)
const showDetailDialog = ref(false)
const isEditing = ref(false)
const currentPortfolioId = ref<number | null>(null)
const currentPortfolio = ref<PortfolioDetail | null>(null)

const formRef = ref<FormInstance>()
const uploadRef = ref<UploadInstance>()
const uploadFileList = ref<UploadUserFile[]>([])
const dragIndex = ref<number | null>(null)

const portfolioForm = reactive<PortfolioForm>({
  name: '',
  client_name: '',
  shoot_date: '',
  category_id: null,
  tag_ids: [],
  user_id: 1,
})

const formRules: FormRules<PortfolioForm> = {
  name: [
    { required: true, message: '请输入作品集名称', trigger: 'blur' },
    { min: 1, max: 50, message: '名称长度需在 1-50 个字符内', trigger: 'blur' },
  ],
  client_name: [
    { required: true, message: '请输入客户名称', trigger: 'blur' },
    { min: 1, max: 50, message: '客户名称长度需在 1-50 个字符内', trigger: 'blur' },
  ],
  shoot_date: [{ required: true, message: '请选择拍摄日期', trigger: 'change' }],
}

const portfolioCount = computed(() => portfolios.value.length)

const totalImageCount = computed(() => {
  return portfolios.value.reduce((total, item) => total + getImageCount(item), 0)
})

const latestUpdate = computed(() => {
  if (!portfolios.value.length) {
    return '暂无数据'
  }

  const latest = [...portfolios.value]
    .map(item => item.created_at || item.shoot_date || '')
    .filter(Boolean)
    .sort((a, b) => (a > b ? -1 : 1))[0]

  return latest ? formatDate(latest) : '暂无数据'
})

const formatDate = (value?: string): string => {
  if (!value) {
    return '-'
  }

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}

const getImageCount = (portfolio: PortfolioItem): number => {
  if (typeof portfolio.image_count === 'number') {
    return portfolio.image_count
  }

  if (Array.isArray(portfolio.images)) {
    return portfolio.images.length
  }

  return 0
}

const resetForm = (): void => {
  portfolioForm.name = ''
  portfolioForm.client_name = ''
  portfolioForm.shoot_date = ''
  portfolioForm.category_id = null
  portfolioForm.tag_ids = []
  portfolioForm.user_id = 1
  isEditing.value = false
  currentPortfolioId.value = null
  formRef.value?.clearValidate()
}

const refreshAll = async (): Promise<void> => {
  isLoading.value = true
  try {
    const [portfolioList, categoryList, tagList] = await Promise.all([
      portfolioApi.getPortfolios(),
      portfolioApi.getCategories(),
      portfolioApi.getTags(),
    ])

    portfolios.value = Array.isArray(portfolioList) ? portfolioList : []
    categories.value = Array.isArray(categoryList) ? categoryList : []
    tags.value = Array.isArray(tagList) ? tagList : []
  } catch (error) {
    console.error('Failed to initialize portfolio data:', error)
    ElMessage.error('加载作品集数据失败')
  } finally {
    isLoading.value = false
  }
}

const openCreateDialog = (): void => {
  resetForm()
  showCreateDialog.value = true
}

const openEditDialog = (portfolio: PortfolioItem): void => {
  resetForm()
  isEditing.value = true
  currentPortfolioId.value = portfolio.id

  portfolioForm.name = portfolio.name
  portfolioForm.client_name = portfolio.client_name || ''
  portfolioForm.shoot_date = portfolio.shoot_date || ''
  portfolioForm.category_id = portfolio.category_id ?? null

  const resolvedTags = Array.isArray(portfolio.tags)
    ? portfolio.tags
        .map(item => (typeof item === 'number' ? item : item.id))
        .filter((id): id is number => Number.isFinite(id))
    : []

  portfolioForm.tag_ids = resolvedTags
  showCreateDialog.value = true
}

const savePortfolio = async (): Promise<void> => {
  if (!formRef.value) {
    return
  }

  try {
    await formRef.value.validate()
    isSubmitting.value = true

    const payload = {
      ...portfolioForm,
      tag_ids: [...portfolioForm.tag_ids],
    }

    if (isEditing.value && currentPortfolioId.value !== null) {
      await portfolioApi.updatePortfolio(currentPortfolioId.value, payload)
      ElMessage.success('作品集已更新')
    } else {
      await portfolioApi.createPortfolio(payload)
      ElMessage.success('作品集已创建')
    }

    showCreateDialog.value = false
    await refreshAll()
  } catch (error) {
    if (error) {
      console.error('Failed to save portfolio:', error)
    }
  } finally {
    isSubmitting.value = false
  }
}

const loadPortfolioDetail = async (portfolioId: number): Promise<void> => {
  isDetailLoading.value = true
  try {
    const detail = await portfolioApi.getPortfolioDetail(portfolioId)
    currentPortfolio.value = {
      ...(detail || {}),
      images: Array.isArray(detail?.images) ? detail.images : [],
    }
    currentPortfolioId.value = portfolioId
  } catch (error) {
    console.error('Failed to load portfolio detail:', error)
    ElMessage.error('加载作品详情失败')
  } finally {
    isDetailLoading.value = false
  }
}

const openDetail = async (portfolio: PortfolioItem): Promise<void> => {
  showDetailDialog.value = true
  await loadPortfolioDetail(portfolio.id)
}

const onCloseDetail = (): void => {
  uploadFileList.value = []
  uploadRef.value?.clearFiles()
  currentPortfolio.value = null
  currentPortfolioId.value = null
  dragIndex.value = null
}

const removePortfolio = async (portfolio: PortfolioItem): Promise<void> => {
  try {
    await ElMessageBox.confirm(`确认删除作品集「${portfolio.name}」吗？此操作不可撤销。`, '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    })

    await portfolioApi.deletePortfolio(portfolio.id)
    ElMessage.success('作品集已删除')

    if (currentPortfolioId.value === portfolio.id) {
      showDetailDialog.value = false
      onCloseDetail()
    }

    await refreshAll()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete portfolio:', error)
    }
  }
}

const handleFileSelect: UploadProps['onChange'] = (_file, fileList) => {
  uploadFileList.value = fileList
}

const handleFileRemove: UploadProps['onRemove'] = (_file, fileList) => {
  uploadFileList.value = fileList
}

const uploadSelectedImages = async (): Promise<void> => {
  if (!currentPortfolio.value || !uploadFileList.value.length) {
    return
  }

  isUploading.value = true
  try {
    for (const file of uploadFileList.value) {
      if (!file.raw) {
        continue
      }

      const formData = new FormData()
      formData.append('file', file.raw)
      await portfolioApi.uploadImageToPortfolio(currentPortfolio.value.id, formData)
    }

    ElMessage.success('图片上传成功')
    uploadFileList.value = []
    uploadRef.value?.clearFiles()

    await loadPortfolioDetail(currentPortfolio.value.id)
    await refreshAll()
  } catch (error) {
    console.error('Failed to upload images:', error)
    ElMessage.error('图片上传失败')
  } finally {
    isUploading.value = false
  }
}

const deleteImage = async (imageId: number): Promise<void> => {
  if (!currentPortfolio.value) {
    return
  }

  try {
    await ElMessageBox.confirm('确认删除这张图片吗？', '删除图片', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    })

    await imageApi.deleteImage(imageId)
    ElMessage.success('图片已删除')

    await loadPortfolioDetail(currentPortfolio.value.id)
    await refreshAll()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete image:', error)
      ElMessage.error('删除图片失败')
    }
  }
}

const dragStart = (index: number): void => {
  dragIndex.value = index
}

const drop = async (targetIndex: number): Promise<void> => {
  if (dragIndex.value === null || !currentPortfolio.value) {
    return
  }

  if (dragIndex.value === targetIndex) {
    dragIndex.value = null
    return
  }

  const images = [...currentPortfolio.value.images]
  const [moved] = images.splice(dragIndex.value, 1)

  if (!moved) {
    dragIndex.value = null
    return
  }

  images.splice(targetIndex, 0, moved)
  currentPortfolio.value.images = images

  const imageOrders = images.map((item, index) => ({
    id: item.id,
    sort_order: index + 1,
  }))

  try {
    await imageApi.reorderImages(currentPortfolio.value.id, imageOrders)
    await loadPortfolioDetail(currentPortfolio.value.id)
    ElMessage.success('排序已更新')
  } catch (error) {
    console.error('Failed to reorder images:', error)
    ElMessage.error('更新排序失败')
    await loadPortfolioDetail(currentPortfolio.value.id)
  } finally {
    dragIndex.value = null
  }
}

onMounted(() => {
  refreshAll()
})
</script>

<style scoped>
.portfolio-manager {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.summary-card {
  border: 1px solid var(--pm-border);
  border-radius: 14px;
  background: var(--pm-surface);
  padding: 16px;
  box-shadow: var(--pm-shadow-1);
}

.summary-card span {
  display: block;
  color: #5d7590;
  font-size: 12px;
  font-weight: 700;
}

.summary-card strong {
  display: block;
  margin-top: 8px;
  color: var(--pm-text);
  font-size: clamp(24px, 4vw, 34px);
  line-height: 1.1;
}

.toolbar-card {
  border: 1px solid var(--pm-border);
  border-radius: var(--pm-radius-md);
  background: var(--pm-surface);
  box-shadow: var(--pm-shadow-1);
  padding: 18px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 12px;
}

.toolbar-left h2 {
  font-size: 22px;
  color: var(--pm-text);
}

.toolbar-left p {
  margin-top: 6px;
  color: var(--pm-text-soft);
  font-size: 13px;
}

.toolbar-right {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.primary-btn,
.ghost-btn {
  height: 40px;
  border-radius: 12px;
  font-weight: 700;
}

.primary-btn {
  border: 0;
  color: #ffffff;
  background: linear-gradient(126deg, var(--pm-primary), #17a4cf);
}

.primary-btn:hover {
  filter: brightness(1.04);
}

.ghost-btn {
  border-color: #bfd8ec;
  background: #eff7ff;
  color: #20517c;
}

.table-card {
  border: 1px solid var(--pm-border);
  border-radius: var(--pm-radius-md);
  background: var(--pm-surface);
  box-shadow: var(--pm-shadow-1);
  padding: 8px;
}

:deep(.el-table) {
  --el-table-header-bg-color: #f2f8ff;
  --el-table-border-color: #e2edf7;
  --el-table-row-hover-bg-color: #f6fbff;
  border-radius: 12px;
}

.name-cell,
.meta-cell {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #284c72;
}

.meta-cell.compact {
  color: #45617f;
}

.count-tag {
  border-color: #b9d8ef;
  color: #1e547f;
  background: #edf7ff;
}

.actions {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px 14px;
}

.form-grid :deep(.el-form-item:nth-child(1)),
.form-grid :deep(.el-form-item:nth-child(5)) {
  grid-column: span 2;
}

.full-width {
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.detail-layout {
  min-height: 420px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.detail-header {
  border: 1px solid var(--pm-border);
  border-radius: 12px;
  background: #f5faff;
  padding: 14px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.detail-header h3 {
  color: var(--pm-text);
  font-size: 24px;
}

.detail-header p {
  margin-top: 4px;
  color: var(--pm-text-soft);
  font-size: 13px;
}

.image-tag {
  display: inline-flex;
  align-items: center;
  padding: 10px 16px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  background: linear-gradient(135deg, #e6f7ff 0%, #f0f9ff 100%);
  border: 1px solid #91d5ff;
  color: #1890ff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.15);
  transition: all 0.3s ease;
}

.image-tag:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.2);
  border-color: #69c0ff;
}

.image-tag .el-tag__content {
  font-weight: 600;
  color: #1890ff;
}

.upload-panel,
.gallery-panel {
  border: 1px solid var(--pm-border);
  border-radius: 12px;
  background: #ffffff;
  padding: 14px;
}

.upload-heading h4,
.gallery-header h4 {
  font-size: 16px;
  color: var(--pm-text);
}

.upload-heading p,
.gallery-header p {
  margin-top: 4px;
  color: var(--pm-text-soft);
  font-size: 12px;
}

.upload-body {
  margin-top: 12px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.upload-btn {
  border-radius: 12px;
  height: 40px;
  font-weight: 700;
}

:deep(.upload-area .el-upload--picture-card) {
  border-radius: 12px;
  border-color: #bad6ea;
  background: #f7fbff;
}

:deep(.upload-area .el-upload-list--picture-card .el-upload-list__item) {
  border-radius: 12px;
}

.image-grid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(168px, 1fr));
  gap: 12px;
}

.image-card {
  border: 1px solid #d9e6f2;
  border-radius: 12px;
  overflow: hidden;
  background: #ffffff;
  cursor: grab;
  box-shadow: 0 10px 24px rgba(17, 37, 61, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.image-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 28px rgba(17, 37, 61, 0.12);
}

.image-card img {
  display: block;
  width: 100%;
  height: 142px;
  object-fit: cover;
}

.image-info {
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.image-info span {
  color: #4a6481;
  font-size: 12px;
  font-weight: 700;
}

.remove-btn {
  border: 0;
  border-radius: 8px;
  background: #fff1f1;
  color: #b93232;
  font-size: 12px;
  font-weight: 700;
  padding: 6px 10px;
  cursor: pointer;
}

.remove-btn:hover {
  background: #ffe4e4;
}

.empty-gallery {
  margin-top: 10px;
  border: 1px dashed #c9d9e8;
  border-radius: 12px;
  background: #f8fbff;
  color: #61809f;
  padding: 22px;
  text-align: center;
}

:deep(.portfolio-dialog .el-dialog) {
  border-radius: 18px;
}

:deep(.portfolio-dialog .el-dialog__header) {
  border-bottom: 1px solid #e2edf7;
  margin-right: 0;
  padding: 18px 20px;
}

:deep(.portfolio-dialog .el-dialog__body) {
  padding: 18px 20px;
}

@media (max-width: 980px) {
  .summary-grid,
  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-grid :deep(.el-form-item:nth-child(1)),
  .form-grid :deep(.el-form-item:nth-child(5)) {
    grid-column: span 1;
  }

  .toolbar-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .toolbar-right {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
