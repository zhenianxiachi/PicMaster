<template>
  <div class="portfolio-manager-container">
    <div class="create-section">
      <el-button type="primary" size="large" @click="showCreateDialog = true" class="create-btn">
        <el-icon><el-icon-plus /></el-icon>
        创建作品集
      </el-button>
    </div>

    <div class="list-section">
      <el-table :data="localPortfolios" class="portfolio-table" @row-click="viewPortfolio">
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
          
          <div class="upload-section">
            <el-upload
              class="image-upload"
              :auto-upload="false"
              :multiple="true"
              :limit="20"
              :file-list="uploadFileList"
              :on-change="handleFileSelect"
              list-type="picture-card"
              ref="uploadRef"
            >
              <el-icon class="el-icon--plus"><el-icon-plus /></el-icon>
            </el-upload>
            
            <el-button 
              type="primary" 
              @click="uploadSelectedImages" 
              :disabled="uploadFileList.length === 0"
              class="upload-confirm-btn"
            >
              <el-icon><el-icon-upload /></el-icon>
              上传图片
            </el-button>
          </div>

          <div class="image-list" ref="imageListRef">
            <div
              v-for="(image, index) in (currentPortfolio.images || [])"
              :key="image.id"
              class="image-item"
              draggable="true"
              @dragstart="dragStart(index)"
              @dragover.prevent
              @drop="drop(index)"
            >
              <img :src="image.filepath" alt="作品集图片" />
              <div class="image-actions">
                <span class="image-action delete" @click.stop="deleteImage(image.id)">
                  <span class="delete-text">X</span>
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
      width="700px"
      class="create-dialog"
    >
      <el-form 
        :model="portfolioForm" 
        label-position="top" 
        class="portfolio-form"
        :rules="formRules"
        ref="formRef"
      >
        <el-form-item label="作品集名称" prop="name">
          <el-input v-model="portfolioForm.name" placeholder="请输入作品集名称" />
        </el-form-item>
        <el-form-item label="客户名称" prop="client_name">
          <el-input v-model="portfolioForm.client_name" placeholder="请输入客户名称" />
        </el-form-item>
        <el-form-item label="拍摄日期" prop="shoot_date">
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
            <el-option
              v-for="tag in tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            />
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

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { portfolioApi, imageApi } from '../api/portfolioApi'

const localPortfolios = ref([])
const categories = ref([])
const tags = ref([])
const showCreateDialog = ref(false)
const showPortfolioDialog = ref(false)
const isEditing = ref(false)
const currentPortfolio = ref({})
const currentPortfolioId = ref(null)
const dragIndex = ref(null)
const imageListRef = ref(null)
const isLoading = ref(false)
const formRef = ref(null)
const uploadFileList = ref([])
const uploadRef = ref(null)

const portfolioForm = reactive({
  name: '',
  client_name: '',
  shoot_date: '',
  category_id: '',
  tag_ids: [],
  user_id: 1 // 假设当前用户ID为1，实际应从登录状态获取
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入作品集名称', trigger: 'blur' },
    { min: 1, max: 50, message: '作品集名称长度在1到50个字符之间', trigger: 'blur' }
  ],
  client_name: [
    { required: true, message: '请输入客户名称', trigger: 'blur' },
    { min: 1, max: 50, message: '客户名称长度在1到50个字符之间', trigger: 'blur' }
  ],
  shoot_date: [
    { required: true, message: '请选择拍摄日期', trigger: 'change' }
  ]
}

// 初始化数据
const initData = async () => {
  isLoading.value = true
  try {
    // 从后端获取数据
    const [portfoliosData, categoriesData, tagsData] = await Promise.all([
      portfolioApi.getPortfolios(),
      portfolioApi.getCategories(),
      portfolioApi.getTags()
    ])
    
    localPortfolios.value = portfoliosData
    categories.value = categoriesData
    tags.value = tagsData
  } catch (error) {
    console.error('初始化数据失败:', error)
  } finally {
    isLoading.value = false
  }
}

// 保存作品集
const savePortfolio = async () => {
  try {
    // 表单验证
    await formRef.value.validate()
    
    if (isEditing.value) {
      // 更新作品集
      await portfolioApi.updatePortfolio(currentPortfolioId.value, portfolioForm)
      // 重新获取数据
      await initData()
    } else {
      // 创建作品集
      await portfolioApi.createPortfolio(portfolioForm)
      // 重新获取数据
      await initData()
    }
    showCreateDialog.value = false
    resetForm()
  } catch (error) {
    // 表单验证失败时，Element Plus会自动显示错误信息
    if (error.name !== 'Error') {
      console.error('保存作品集失败:', error)
    }
  }
}

// 编辑作品集
const editPortfolio = (portfolio) => {
  isEditing.value = true
  currentPortfolioId.value = portfolio.id
  portfolioForm.name = portfolio.name
  portfolioForm.client_name = portfolio.client_name
  portfolioForm.shoot_date = portfolio.shoot_date
  portfolioForm.category_id = portfolio.category_id
  portfolioForm.tag_ids = portfolio.tags || []
  showCreateDialog.value = true
}

// 查看作品集详情
const viewPortfolio = async (portfolio) => {
  try {
    const portfolioDetail = await portfolioApi.getPortfolioDetail(portfolio.id)
    currentPortfolio.value = portfolioDetail
    showPortfolioDialog.value = true
  } catch (error) {
    console.error('获取作品集详情失败:', error)
  }
}

// 删除作品集
const deletePortfolio = async (portfolio) => {
  try {
    await portfolioApi.deletePortfolio(portfolio.id)
    // 重新获取数据
    await initData()
  } catch (error) {
    console.error('删除作品集失败:', error)
  }
}

// 处理文件选择，只添加到列表
const handleFileSelect = (file, fileList) => {
  uploadFileList.value = fileList
}

// 上传选中的图片
const uploadSelectedImages = async () => {
  try {
    for (const file of uploadFileList.value) {
      const formData = new FormData()
      formData.append('file', file.raw)
      
      // 调用API上传图片
      await portfolioApi.uploadImageToPortfolio(currentPortfolio.value.id, formData)
    }
    
    // 重新获取作品集详情
    const updatedPortfolio = await portfolioApi.getPortfolioDetail(currentPortfolio.value.id)
    currentPortfolio.value = updatedPortfolio
    
    // 清空已选择的文件列表
    uploadFileList.value = []
    
    // 清空上传组件的文件列表
    if (uploadRef.value) {
      uploadRef.value.clearFiles()
    }
  } catch (error) {
    console.error('上传图片失败:', error)
  }
}

// 删除图片
const deleteImage = async (imageId) => {
  try {
    await imageApi.deleteImage(imageId)
    
    // 重新获取作品集详情
    const updatedPortfolio = await portfolioApi.getPortfolioDetail(currentPortfolio.value.id)
    currentPortfolio.value = updatedPortfolio
  } catch (error) {
    console.error('删除图片失败:', error)
  }
}

// 拖放开始
const dragStart = (index) => {
  dragIndex.value = index
}

// 拖放结束
const drop = async (targetIndex) => {
  if (dragIndex.value === null) return
  
  const draggedItem = currentPortfolio.value.images.splice(dragIndex.value, 1)[0]
  currentPortfolio.value.images.splice(targetIndex, 0, draggedItem)
  
  // 更新排序
  const imageOrders = currentPortfolio.value.images.map((img, i) => ({
    id: img.id,
    sort_order: i + 1
  }))
  
  try {
    await imageApi.reorderImages(currentPortfolio.value.id, imageOrders)
    
    // 重新获取作品集详情
    const updatedPortfolio = await portfolioApi.getPortfolioDetail(currentPortfolio.value.id)
    currentPortfolio.value = updatedPortfolio
  } catch (error) {
    console.error('重新排序图片失败:', error)
    // 恢复原始排序
    await viewPortfolio(currentPortfolio.value)
  } finally {
    dragIndex.value = null
  }
}

// 重置表单
const resetForm = () => {
  isEditing.value = false
  currentPortfolioId.value = null
  Object.assign(portfolioForm, {
    name: '',
    client_name: '',
    shoot_date: '',
    category_id: '',
    tag_ids: [],
    user_id: 1
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

.upload-section {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.upload-confirm-btn {
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.image-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  display: block;
}

.image-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 8px;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.image-item:hover .image-actions {
  opacity: 1;
}

.image-action {
  background: rgba(255, 0, 0, 0.7);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.image-action.delete:hover {
  background: rgba(255, 0, 0, 0.9);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(255, 0, 0, 0.3);
}

.delete-text {
  font-size: 16px;
  font-weight: bold;
  color: white;
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