<template>
  <div class="business-view">
    <div class="business-header">
      <h1>商务合作</h1>
      <p>与 PicMaster 建立合作伙伴关系</p>
    </div>
    
    <div class="business-content">
      <section class="business-section hero">
        <div class="hero-content">
          <h2>为什么选择与 PicMaster 合作？</h2>
          <p>PicMaster 是领先的图像编辑和管理平台，为专业摄影师、设计师和企业提供强大的工具和服务。我们致力于通过创新技术和优质服务，帮助合作伙伴实现业务增长。</p>
        </div>
      </section>
      
      <section class="business-section">
        <h2>合作模式</h2>
        <div class="cooperation-grid">
          <div class="cooperation-card">
            <div class="card-icon">
              <el-icon><OfficeBuilding /></el-icon>
            </div>
            <h3>企业合作</h3>
            <p>为企业客户提供定制化的图像解决方案，包括批量处理、品牌管理和工作流程优化。</p>
          </div>
          
          <div class="cooperation-card">
            <div class="card-icon">
              <el-icon><Shop /></el-icon>
            </div>
            <h3>渠道合作</h3>
            <p>成为我们的渠道合作伙伴，通过推广 PicMaster 服务获得丰厚的佣金回报。</p>
          </div>
          
          <div class="cooperation-card">
            <div class="card-icon">
              <el-icon><Monitor /></el-icon>
            </div>
            <h3>技术集成</h3>
            <p>将 PicMaster 的图像编辑能力集成到您的应用或服务中，为用户提供更丰富的功能。</p>
          </div>
          
          <div class="cooperation-card">
            <div class="card-icon">
              <el-icon><Camera /></el-icon>
            </div>
            <h3>行业合作</h3>
            <p>与摄影工作室、设计机构等行业伙伴建立深度合作，共同拓展市场。</p>
          </div>
        </div>
      </section>
      
      <section class="business-section">
        <h2>合作优势</h2>
        <ul class="advantages-list">
          <li>
            <el-icon><Check /></el-icon>
            <span>强大的技术支持和产品研发能力</span>
          </li>
          <li>
            <el-icon><Check /></el-icon>
            <span>灵活的合作模式和定制化解决方案</span>
          </li>
          <li>
            <el-icon><Check /></el-icon>
            <span>有竞争力的价格和利润空间</span>
          </li>
          <li>
            <el-icon><Check /></el-icon>
            <span>专业的市场推广和客户服务</span>
          </li>
          <li>
            <el-icon><Check /></el-icon>
            <span>持续的产品更新和功能迭代</span>
          </li>
        </ul>
      </section>
      
      <section class="business-section contact">
        <h2>联系我们</h2>
        <p>如果您对与 PicMaster 的合作感兴趣，请通过以下方式联系我们：</p>
        
        <div class="contact-info">
          <div class="contact-item">
            <el-icon><Phone /></el-icon>
            <span>商务热线：400-123-4567</span>
          </div>
          <div class="contact-item">
            <el-icon><Message /></el-icon>
            <span>电子邮件：1427844359@qq.com</span>
          </div>
          <div class="contact-item">
            <el-icon><Position /></el-icon>
            <span>公司地址：北京市朝阳区创意园区 A 座 1001</span>
          </div>
        </div>
        
        <el-button type="primary" class="contact-btn">
          <el-icon><ChatLineSquare /></el-icon>
          立即咨询
        </el-button>
      </section>
      
      <section class="business-section faq">
        <h2>常见问题</h2>
        <el-collapse>
          <el-collapse-item title="如何成为 PicMaster 的渠道合作伙伴？" name="1">
            <div class="faq-content">
              <p>您可以通过商务邮箱 1427844359@qq.com 联系我们，提交合作申请。我们的商务团队会在 2-3 个工作日内与您联系，详细了解您的业务情况并提供合作方案。</p>
            </div>
          </el-collapse-item>
          
          <el-collapse-item title="技术集成需要哪些条件？" name="2">
            <div class="faq-content">
              <p>技术集成需要您的应用或服务具备基本的 API 调用能力。我们提供详细的 API 文档和技术支持，帮助您快速完成集成。具体技术要求可以联系我们的技术支持团队获取。</p>
            </div>
          </el-collapse-item>
          
          <el-collapse-item title="企业合作的定制化范围包括哪些？" name="3">
            <div class="faq-content">
              <p>企业合作的定制化范围包括：品牌定制、功能定制、工作流程优化、数据集成等。我们会根据企业客户的具体需求，提供个性化的解决方案。</p>
            </div>
          </el-collapse-item>
          
          <el-collapse-item title="合作周期和费用如何计算？" name="4">
            <div class="faq-content">
              <p>合作周期和费用根据合作模式和具体需求而定。我们提供灵活的合作方案，包括短期项目合作和长期战略伙伴关系。具体费用会在商务洽谈中根据实际情况确定。</p>
            </div>
          </el-collapse-item>
        </el-collapse>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { OfficeBuilding, Shop, Monitor, Camera, Check, Phone, Message, Position, ChatLineSquare } from '@element-plus/icons-vue'

onMounted(() => {
  document.title = '商务合作 - PicMaster'
})
</script>

<style scoped>
.business-view {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 24px;
}

.business-header {
  text-align: center;
  margin-bottom: 40px;
}

.business-header h1 {
  font-size: 32px;
  color: var(--pm-text);
  margin-bottom: 12px;
}

.business-header p {
  color: var(--pm-text-soft);
  font-size: 16px;
}

.business-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.business-section {
  border: 1px solid var(--pm-border);
  border-radius: 12px;
  padding: 24px;
  background: #ffffff;
  box-shadow: var(--pm-shadow-1);
}

.business-section.hero {
  background: linear-gradient(135deg, #e6f7ff 0%, #f0f9ff 100%);
  border-color: #91d5ff;
  text-align: center;
}

.hero-content h2 {
  font-size: 24px;
  color: var(--pm-text);
  margin-bottom: 16px;
}

.hero-content p {
  color: #3a5573;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

.business-section h2 {
  font-size: 20px;
  color: var(--pm-text);
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e2edf7;
}

.cooperation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.cooperation-card {
  border: 1px solid #e2edf7;
  border-radius: 12px;
  padding: 20px;
  background: #f8fbff;
  text-align: center;
  transition: all 0.3s ease;
}

.cooperation-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(15, 124, 207, 0.15);
  border-color: #91d5ff;
}

.card-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 16px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1890ff 0%, #69c0ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.cooperation-card h3 {
  font-size: 16px;
  color: var(--pm-text);
  margin-bottom: 12px;
}

.cooperation-card p {
  color: #3a5573;
  font-size: 14px;
  line-height: 1.5;
}

.advantages-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.advantages-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #e2edf7;
  color: #3a5573;
}

.advantages-list li:last-child {
  border-bottom: none;
}

.advantages-list el-icon {
  color: #52c41a;
  font-size: 18px;
}

.business-section.contact {
  text-align: center;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin: 24px 0;
}

.contact-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #3a5573;
}

.contact-btn {
  margin-top: 16px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
}

.faq-content {
  padding: 16px 0;
  color: #3a5573;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .business-view {
    padding: 24px 16px;
  }
  
  .business-header h1 {
    font-size: 24px;
  }
  
  .business-section h2 {
    font-size: 18px;
  }
  
  .cooperation-grid {
    grid-template-columns: 1fr;
  }
  
  .contact-info {
    align-items: flex-start;
  }
  
  .contact-item {
    justify-content: flex-start;
  }
}
</style>
