<template>
  <div class="portfolio-manager-container">
    <div class="create-section">
      <el-button type="primary" size="large" @click="showCreateDialog = true" class="create-btn">
        <el-icon><Plus /></el-icon>
        创建作品集
      </el-button>
    </div>

    <div class="list-section">
      <el-table :data="portfolios" class="portfolio-table" @row-click="viewPortfolio">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="作品集名称">
          <template #default="scope">
            <span class="portfolio-name">{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="client_name" label="客户名称"></el-table-column>
        <el-table-column prop="shoot_date" label="拍摄日期"></el-table-column>
        <el-table-column prop="image_count" label="图片数量"></el-table-column>
        <el-table-column prop="created_at" label="创建时间"></el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <span class="action-links" @click.stop>
              <span class="action-link" @click="editPortfolio(scope.row)">编辑</span>
              <span class="action-link delete" @click="deletePortfolio(scope.row)">删除</span>
            </span>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog
      v-model="showPortfolioDialog"
      title="作品集详情"
      width="80%"
      class="portfolio-dialog"
      :show-close="true"
      append-to-body
    >
      <div class="portfolio-detail">
        <div class="portfolio-info">
          <h3>{{ currentPortfolio.name }}</h3>
          <div class="info-tags">
            <span class="info-tag">客户：{{ currentPortfolio.client_name }}</span>
            <span class="info-tag">拍摄日期：{{ currentPortfolio.shoot_date }}</span>
          </div>
        </div>

        <div class="image-management">
          <h4>图片管理</h4>

          <el-upload
            class="image-upload"
            :auto-upload="true"
            :multiple="true"
            :limit="20"
            :http-request="handleImageUpload"
            list-type="picture-card"
          >
            <el-icon class="el-icon--plus"><Plus /></el-icon>
          </el-upload>

          <div class="image-list" ref="imageListRef">
            <div
              v-for="(image, index) in currentPortfolio.images"
              :key="image.id"
              class="image-item"
              draggable="true"
              @dragstart="dragStart(index)"
              @dragover.prevent
              @drop="drop(index)"
            >
              <img :src="image.url" alt="作品集图片" />
              <div class="image-actions">
                <span class="image-action delete" @click.stop="deleteImage(index)">
                  <el-icon><Delete /></el-icon>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>

    <el-dialog
      v-model="showCreateDialog"
      :title="isEditing ? '编辑作品集' : '创建作品集'"
      width="500px"
      class="create-dialog"
      append-to-body
    >
      <el-form :model="portfolioForm" label-position="top" class="portfolio-form">
        <el-form-item label="作品集名称">
          <el-input v-model="portfolioForm.name" placeholder="请输入作品集名称" />
        </el-form-item>
        <el-form-item label="客户名称">
          <el-input v-model="portfolioForm.client_name" placeholder="请输入客户名称" />
        </el-form-item>
        <el-form-item label="拍摄日期">
          <el-date-picker
            v-model="portfolioForm.shoot_date"
            type="date"
            format="YYYY年MM月DD日"
            value-format="YYYY-MM-DD"
            placeholder="选择拍摄日期"
          />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="portfolioForm.category_id" placeholder="选择分类" class="full-width">
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select
            v-model="portfolioForm.tag_ids"
            multiple
            placeholder="选择标签"
            class="full-width"
          >
            <el-option v-for="tag in tags" :key="tag.id" :label="tag.name" :value="tag.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="savePortfolio">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, type Ref } from 'vue'
import { Plus, Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { portfolioApi } from '../../api/portfolioApi.js'

/**
 * 作品集类型
 */
interface Portfolio {
  id: number
  name: string
  client_name: string
  shoot_date: string
  image_count: number
  created_at: string
  images: PortfolioImage[]
}

/**
 * 作品集图片类型
 */
interface PortfolioImage {
  id: number
  url: string
  sort_order: number
}

/**
 * 分类类型
 */
interface Category {
  id: number
  name: string
}

/**
 * 标签类型
 */
interface Tag {
  id: number
  name: string
}

/**
 * 作品集表单类型
 */
interface PortfolioForm {
  name: string
  client_name: string
  shoot_date: string
  category_id: string
  tag_ids: number[]
}

const portfolios: Ref<Portfolio[]> = ref([])
const categories: Ref<Category[]> = ref([])
const tags: Ref<Tag[]> = ref([])
const showCreateDialog: Ref<boolean> = ref(false)
const showPortfolioDialog: Ref<boolean> = ref(false)
const isEditing: Ref<boolean> = ref(false)
const currentPortfolio: Ref<Partial<Portfolio>> = ref({})
const currentPortfolioId: Ref<number | null> = ref(null)
const dragIndex: Ref<number | null> = ref(null)
const imageListRef: Ref<HTMLElement | null> = ref(null)

const portfolioForm = reactive<PortfolioForm>({
  name: '',
  client_name: '',
  shoot_date: '',
  category_id: '',
  tag_ids: [],
})

const mockPortfolios = [
  {
    id: 1,
    name: '客户A-20240101',
    client_name: '客户A',
    shoot_date: '2024-01-01',
    image_count: 15,
    created_at: '2024-01-02 10:30:00',
    images: [
      { id: 1, url: 'https://picsum.photos/200/200?random=1', sort_order: 1 },
      { id: 2, url: 'https://picsum.photos/200/200?random=2', sort_order: 2 },
      { id: 3, url: 'https://picsum.photos/200/200?random=3', sort_order: 3 },
    ],
  },
  {
    id: 2,
    name: '客户B-20240201',
    client_name: '客户B',
    shoot_date: '2024-02-01',
    image_count: 10,
    created_at: '2024-02-02 14:20:00',
    images: [
      { id: 4, url: 'https://picsum.photos/200/200?random=4', sort_order: 1 },
      { id: 5, url: 'https://picsum.photos/200/200?random=5', sort_order: 2 },
    ],
  },
]

const mockCategories = [
  { id: 1, name: '婚礼' },
  { id: 2, name: '人像' },
  { id: 3, name: '商业' },
  { id: 4, name: '风景' },
]

const mockTags = [
  { id: 1, name: '高清' },
  { id: 2, name: '精选' },
  { id: 3, name: '原图' },
  { id: 4, name: '修图' },
]

const initData = () => {
  portfolios.value = mockPortfolios
  categories.value = mockCategories
  tags.value = mockTags
}

const savePortfolio = () => {
  if (isEditing.value) {
    const index = portfolios.value.findIndex(p => p.id === currentPortfolioId.value)
    if (index !== -1) {
      const existingPortfolio = portfolios.value[index]
      portfolios.value[index] = { 
        ...existingPortfolio, 
        name: portfolioForm.name,
        client_name: portfolioForm.client_name,
        shoot_date: portfolioForm.shoot_date,
        category_id: portfolioForm.category_id,
        tags: portfolioForm.tag_ids
      }
    }
  } else {
    const newPortfolio: Portfolio = {
      id: portfolios.value.length + 1,
      name: portfolioForm.name,
      client_name: portfolioForm.client_name,
      shoot_date: portfolioForm.shoot_date,
      category_id: portfolioForm.category_id,
      tags: portfolioForm.tag_ids,
      cover_image: null,
      user_id: 1,
      images: [],
      created_at: new Date().toLocaleString(),
      updated_at: new Date().toLocaleString(),
      image_count: 0
    }
    portfolios.value.push(newPortfolio)
  }
  showCreateDialog.value = false
  resetForm()
}

const editPortfolio = (portfolio: Portfolio): void => {
  isEditing.value = true
  currentPortfolioId.value = portfolio.id
  portfolioForm.name = portfolio.name
  portfolioForm.client_name = portfolio.client_name
  portfolioForm.shoot_date = portfolio.shoot_date
  showCreateDialog.value = true
}

const viewPortfolio = (portfolio: Portfolio): void => {
  currentPortfolio.value = portfolio
  showPortfolioDialog.value = true
}

const deletePortfolio = (portfolio: Portfolio): void => {
  const index = portfolios.value.findIndex(p => p.id === portfolio.id)
  if (index !== -1) {
    portfolios.value.splice(index, 1)
  }
}

const handleImageUpload = async (options: any): Promise<void> => {
  const { file, onSuccess, onError } = options
  
  if (!currentPortfolio.value.id) {
    ElMessage.warning('请先保存作品集')
    onError?.(new Error('请先保存作品集'))
    return
  }

  const formData = new FormData()
  formData.append('file', file)
  formData.append('portfolio_id', String(currentPortfolio.value.id))

  try {
    const response = await portfolioApi.uploadImageToPortfolio(currentPortfolio.value.id, formData)
    
    if (response.images && response.images.length > 0) {
      const uploadedImage = response.images[0]
      
      if (!currentPortfolio.value.images) {
        currentPortfolio.value.images = []
      }

      const newImage: PortfolioImage = {
        id: uploadedImage.id,
        url: uploadedImage.filepath,
        thumbnail_path: uploadedImage.thumbnail_path,
        sort_order: uploadedImage.sort_order,
      }
      currentPortfolio.value.images.push(newImage)
      currentPortfolio.value.image_count = currentPortfolio.value.images.length
      
      ElMessage.success('图片上传成功')
      onSuccess?.(response)
    }
  } catch (error) {
    console.error('上传图片失败:', error)
    ElMessage.error('上传图片失败')
    onError?.(error)
  }
}

const deleteImage = (index: number): void => {
  if (currentPortfolio.value.images) {
    currentPortfolio.value.images.splice(index, 1)
    currentPortfolio.value.image_count = currentPortfolio.value.images.length
    currentPortfolio.value.images.forEach((img, i) => {
      img.sort_order = i + 1
    })
  }
}

const dragStart = (index: number): void => {
  dragIndex.value = index
}

const drop = (targetIndex: number): void => {
  if (dragIndex.value === null || !currentPortfolio.value.images) return

  const draggedItem = currentPortfolio.value.images.splice(dragIndex.value, 1)[0]
  currentPortfolio.value.images.splice(targetIndex, 0, draggedItem)

  currentPortfolio.value.images.forEach((img, i) => {
    img.sort_order = i + 1
  })

  dragIndex.value = null
}

const resetForm = () => {
  isEditing.value = false
  currentPortfolioId.value = null
  Object.assign(portfolioForm, {
    name: '',
    client_name: '',
    shoot_date: '',
    category_id: '',
    tag_ids: [],
  })
}

onMounted(() => {
  initData()
})
</script>

<style scoped>
.portfolio-manager-container {
  padding: 24px;
}

.create-section {
  margin-bottom: 24px;
}

.create-btn {
  background-color: #0071e3;
  border: none;
  border-radius: 980px;
  padding: 12px 24px;
  font-size: 17px;
  font-weight: 400;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.create-btn:hover {
  background-color: #0077ed;
}

.list-section {
  background-color: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

:deep(.portfolio-table) {
  border-radius: 12px;
  overflow: hidden;
}

:deep(.portfolio-table .el-table__header-wrapper) {
  background-color: #fbfbfd;
}

:deep(.portfolio-table .el-table__header th) {
  background-color: #fbfbfd;
  color: #86868b;
  font-weight: 600;
  border-bottom: none;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

:deep(.portfolio-table .el-table__body tr) {
  transition: all 0.3s ease;
  cursor: pointer;
}

:deep(.portfolio-table .el-table__body tr:hover) {
  background-color: #f5f5f7;
}

:deep(.portfolio-table .el-table__body td) {
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
  color: #1d1d1f;
}

.portfolio-name {
  font-weight: 500;
  color: #1d1d1f;
}

.action-links {
  display: flex;
  gap: 16px;
}

.action-link {
  font-size: 14px;
  font-weight: 500;
  color: #0071e3;
  cursor: pointer;
  transition: color 0.3s ease;
}

.action-link:hover {
  color: #0077ed;
}

.action-link.delete {
  color: #ff3b30;
}

.action-link.delete:hover {
  color: #ff453a;
}

.portfolio-detail {
  padding: 24px;
}

.portfolio-info {
  margin-bottom: 32px;
}

.portfolio-info h3 {
  font-size: 28px;
  font-weight: 700;
  color: #1d1d1f;
  margin-bottom: 16px;
}

.info-tags {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.info-tag {
  font-size: 14px;
  color: #86868b;
  background-color: #f5f5f7;
  padding: 8px 16px;
  border-radius: 980px;
}

.image-management h4 {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 24px;
}

:deep(.image-upload .el-upload--picture-card) {
  width: 100px;
  height: 100px;
  border-radius: 12px;
  border: 2px dashed #d2d2d7;
  transition: all 0.3s ease;
}

:deep(.image-upload .el-upload--picture-card:hover) {
  border-color: #0071e3;
  background-color: #f0f7ff;
}

:deep(.image-upload .el-icon-plus) {
  font-size: 24px;
  color: #86868b;
}

.image-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  margin-top: 24px;
  padding: 24px;
  background-color: #fbfbfd;
  border-radius: 16px;
}

.image-item {
  position: relative;
  cursor: move;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.image-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.image-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  display: block;
}

.image-actions {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 10px 10px 10px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.6), transparent);
  display: flex;
  justify-content: flex-end;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-item:hover .image-actions {
  opacity: 1;
}

.image-action {
  padding: 8px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.image-action.delete:hover {
  color: #ff3b30;
}

:deep(.create-dialog .el-dialog),
:deep(.portfolio-dialog .el-dialog) {
  border-radius: 20px;
  overflow: hidden;
}

:deep(.create-dialog .el-dialog__header),
:deep(.portfolio-dialog .el-dialog__header) {
  padding: 24px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.create-dialog .el-dialog__title),
:deep(.portfolio-dialog .el-dialog__title) {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
}

:deep(.portfolio-form .el-form-item__label) {
  color: #1d1d1f;
  font-weight: 500;
  font-size: 14px;
}

:deep(.el-input__wrapper),
:deep(.el-select__wrapper) {
  border-radius: 12px;
  box-shadow: 0 0 0 1px #e5e5ea;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover),
:deep(.el-select__wrapper:hover) {
  box-shadow: 0 0 0 2px rgba(0, 113, 227, 0.2);
}

.full-width {
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
}

:deep(.dialog-footer .el-button) {
  border-radius: 980px;
  padding: 10px 24px;
  font-weight: 500;
}

:deep(.dialog-footer .el-button--primary) {
  background-color: #0071e3;
  border-color: #0071e3;
}

:deep(.dialog-footer .el-button--primary:hover) {
  background-color: #0077ed;
  border-color: #0077ed;
}
</style>
