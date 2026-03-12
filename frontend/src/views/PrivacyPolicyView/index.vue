<template>
  <div class="policy-view">
    <div class="policy-header">
      <h1>隐私政策</h1>
      <p>Last updated: {{ lastUpdated }}</p>
    </div>
    
    <div class="policy-content">
      <section class="policy-section">
        <h2>1. 引言</h2>
        <p>欢迎使用 PicMaster 服务。我们致力于保护您的隐私和个人信息。本隐私政策说明了我们如何收集、使用、存储和保护您的个人信息。</p>
      </section>
      
      <section class="policy-section">
        <h2>2. 信息收集</h2>
        <p>我们可能收集以下类型的信息：</p>
        <ul>
          <li>个人识别信息（如姓名、电子邮件地址）</li>
          <li>使用数据（如访问时间、IP地址）</li>
          <li>设备信息（如浏览器类型、操作系统）</li>
        </ul>
      </section>
      
      <section class="policy-section">
        <h2>3. 信息使用</h2>
        <p>我们使用收集的信息：</p>
        <ul>
          <li>提供和维护服务</li>
          <li>改进和个性化用户体验</li>
          <li>发送重要通知和更新</li>
          <li>分析服务使用情况</li>
        </ul>
      </section>
      
      <section class="policy-section">
        <h2>4. 信息保护</h2>
        <p>我们采取各种安全措施保护您的个人信息，包括加密、访问控制和定期安全评估。</p>
      </section>
      
      <section class="policy-section">
        <h2>5. 数据共享</h2>
        <p>我们不会向第三方出售您的个人信息。我们可能在以下情况下共享信息：</p>
        <ul>
          <li>获得您的明确 consent</li>
          <li>遵守法律义务</li>
          <li>保护我们的权利和财产</li>
        </ul>
      </section>
      
      <section class="policy-section">
        <h2>6. 您的权利</h2>
        <p>您有权：</p>
        <ul>
          <li>访问和修改您的个人信息</li>
          <li>要求删除您的个人信息</li>
          <li>限制数据处理</li>
          <li>数据可携带性</li>
        </ul>
      </section>
      
      <section class="policy-section">
        <h2>7. 变更通知</h2>
        <p>我们可能会不时更新本隐私政策。任何变更将在网站上公布，并在必要时通过电子邮件通知您。</p>
      </section>
      
      <section class="policy-section">
        <h2>8. 联系方式</h2>
        <p>如果您对本隐私政策有任何疑问，请联系我们：</p>
        <p>电子邮件：1427844359@qq.com</p>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const lastUpdated = ref('2026-03-06')

onMounted(() => {
  document.title = '隐私政策 - PicMaster'
})
</script>

<style scoped>
.policy-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 24px;
}

.policy-header {
  text-align: center;
  margin-bottom: 40px;
}

.policy-header h1 {
  font-size: 32px;
  color: var(--pm-text);
  margin-bottom: 12px;
}

.policy-header p {
  color: var(--pm-text-soft);
  font-size: 14px;
}

.policy-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.policy-section {
  border: 1px solid var(--pm-border);
  border-radius: 12px;
  padding: 20px;
  background: #ffffff;
  box-shadow: var(--pm-shadow-1);
}

.policy-section h2 {
  font-size: 20px;
  color: var(--pm-text);
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e2edf7;
}

.policy-section p {
  color: #3a5573;
  line-height: 1.6;
  margin-bottom: 12px;
}

.policy-section ul {
  margin-left: 20px;
  color: #3a5573;
  line-height: 1.6;
}

.policy-section li {
  margin-bottom: 8px;
}

@media (max-width: 768px) {
  .policy-view {
    padding: 24px 16px;
  }
  
  .policy-header h1 {
    font-size: 24px;
  }
  
  .policy-section h2 {
    font-size: 18px;
  }
}
</style>