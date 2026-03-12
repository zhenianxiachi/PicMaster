<template>
  <el-dialog
    v-model="visible"
    title="使用限制"
    width="480px"
    class="limit-dialog"
    :close-on-click-modal="false"
  >
    <div class="limit-content">
      <div class="limit-icon">
        <el-icon :size="64" color="#f56c6c"><WarningFilled /></el-icon>
      </div>
      
      <h3 class="limit-title">{{ title }}</h3>
      <p class="limit-desc">{{ message }}</p>
      
      <div class="limit-stats">
        <div class="stat-item">
          <span class="stat-label">今日已用</span>
          <span class="stat-value">{{ used }}</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-label">每日限额</span>
          <span class="stat-value">{{ limit }}</span>
        </div>
      </div>

      <div class="upgrade-benefits">
        <h4>升级会员享受更多权益</h4>
        <ul>
          <li><el-icon><Check /></el-icon> 每日编辑次数提升至 100 次</li>
          <li><el-icon><Check /></el-icon> 每日保存次数提升至 50 次</li>
          <li><el-icon><Check /></el-icon> 每日导出次数提升至 30 次</li>
          <li><el-icon><Check /></el-icon> 支持批量处理更多图片</li>
          <li><el-icon><Check /></el-icon> 专属客服支持</li>
        </ul>
      </div>
    </div>

    <template #footer>
      <div class="limit-footer">
        <el-button size="large" @click="visible = false">稍后再说</el-button>
        <el-button type="primary" size="large" class="upgrade-btn" @click="handleUpgrade">
          <el-icon><StarFilled /></el-icon>
          立即升级
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { WarningFilled, Check, StarFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const visible = defineModel<boolean>('visible')

const props = defineProps<{
  actionType: 'edit' | 'save' | 'export'
  used: number
  limit: number
  message: string
}>()

const emit = defineEmits<{
  upgrade: []
}>()

const title = computed(() => {
  const typeNames = {
    edit: '编辑',
    save: '保存',
    export: '导出'
  }
  return `今日${typeNames[props.actionType]}次数已达上限`
})

const handleUpgrade = () => {
  ElMessage.info('会员功能开发中，敬请期待！')
  emit('upgrade')
}
</script>

<style scoped>
.limit-dialog :deep(.el-dialog__body) {
  padding: 20px 30px;
}

.limit-content {
  text-align: center;
}

.limit-icon {
  margin-bottom: 16px;
}

.limit-title {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 8px;
}

.limit-desc {
  font-size: 14px;
  color: #86868b;
  margin-bottom: 24px;
}

.limit-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 24px;
  padding: 20px;
  background: #f5f5f7;
  border-radius: 12px;
  margin-bottom: 24px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 13px;
  color: #86868b;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #1d1d1f;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: #d2d2d7;
}

.upgrade-benefits {
  text-align: left;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.upgrade-benefits h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.upgrade-benefits ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.upgrade-benefits li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  margin-bottom: 8px;
}

.upgrade-benefits li:last-child {
  margin-bottom: 0;
}

.limit-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.upgrade-btn {
  display: flex;
  align-items: center;
  gap: 6px;
}
</style>
