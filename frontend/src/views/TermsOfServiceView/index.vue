<template>
  <div class="terms-view">
    <div class="terms-header">
      <h1>服务条款</h1>
      <p>Last updated: {{ lastUpdated }}</p>
    </div>
    
    <div class="terms-content">
      <section class="terms-section">
        <h2>1. 接受条款</h2>
        <p>通过访问和使用 PicMaster 服务，您同意遵守本服务条款。如果您不同意这些条款，请勿使用我们的服务。</p>
      </section>
      
      <section class="terms-section">
        <h2>2. 服务说明</h2>
        <p>PicMaster 提供图像编辑、管理和分享服务。我们保留随时修改、暂停或终止服务的权利，恕不另行通知。</p>
      </section>
      
      <section class="terms-section">
        <h2>3. 用户账户</h2>
        <p>您需要创建账户才能使用某些服务。您负责维护账户的安全性，并对账户下的所有活动负责。</p>
        <ul>
          <li>提供真实、准确、完整的个人信息</li>
          <li>及时更新账户信息</li>
          <li>不共享账户密码或其他访问凭据</li>
          <li>在发现未经授权的账户使用时立即通知我们</li>
        </ul>
      </section>
      
      <section class="terms-section">
        <h2>4. 用户内容</h2>
        <p>您对上传到 PicMaster 的内容负责。您保证：</p>
        <ul>
          <li>您拥有内容的所有权或合法使用权限</li>
          <li>内容不违反任何法律法规</li>
          <li>内容不侵犯他人的知识产权</li>
        </ul>
        <p>通过上传内容，您授予 PicMaster 非排他性、全球性、免版税的许可，以存储、处理和展示您的内容。</p>
      </section>
      
      <section class="terms-section">
        <h2>5. 使用限制</h2>
        <p>您同意不会：</p>
        <ul>
          <li>使用服务进行非法活动</li>
          <li>干扰服务的正常运行</li>
          <li>尝试未经授权访问服务或相关系统</li>
          <li>传播恶意软件或病毒</li>
          <li>滥用或过度使用服务</li>
        </ul>
      </section>
      
      <section class="terms-section">
        <h2>6. 知识产权</h2>
        <p>PicMaster 及其相关服务的所有知识产权归我们所有。您不得复制、修改、分发或创建基于我们服务的衍生作品，除非获得我们的明确书面许可。</p>
      </section>
      
      <section class="terms-section">
        <h2>7. 免责声明</h2>
        <p>服务按"原样"提供，不提供任何形式的保证。我们不保证服务的可靠性、可用性或性能。</p>
      </section>
      
      <section class="terms-section">
        <h2>8. 责任限制</h2>
        <p>在法律允许的最大范围内，PicMaster 及其员工、董事、合作伙伴不对任何间接、附带、特殊或后果性损害负责。</p>
      </section>
      
      <section class="terms-section">
        <h2>9. 条款修改</h2>
        <p>我们可能会不时更新本服务条款。修改后的条款将在网站上公布，您继续使用服务即表示接受修改后的条款。</p>
      </section>
      
      <section class="terms-section">
        <h2>10. 终止</h2>
        <p>我们可以在任何时候终止或暂停您对服务的访问，原因包括：</p>
        <ul>
          <li>违反本服务条款</li>
          <li>法律要求</li>
          <li>服务运营需要</li>
        </ul>
      </section>
      
      <section class="terms-section">
        <h2>11. 适用法律</h2>
        <p>本服务条款受中华人民共和国法律管辖，不考虑法律冲突原则。</p>
      </section>
      
      <section class="terms-section">
        <h2>12. 联系方式</h2>
        <p>如果您对本服务条款有任何疑问，请联系我们：</p>
        <p>电子邮件：1427844359@qq.com</p>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const lastUpdated = ref('2026-03-06')

onMounted(() => {
  document.title = '服务条款 - PicMaster'
})
</script>

<style scoped>
.terms-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 24px;
}

.terms-header {
  text-align: center;
  margin-bottom: 40px;
}

.terms-header h1 {
  font-size: 32px;
  color: var(--pm-text);
  margin-bottom: 12px;
}

.terms-header p {
  color: var(--pm-text-soft);
  font-size: 14px;
}

.terms-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.terms-section {
  border: 1px solid var(--pm-border);
  border-radius: 12px;
  padding: 20px;
  background: #ffffff;
  box-shadow: var(--pm-shadow-1);
}

.terms-section h2 {
  font-size: 20px;
  color: var(--pm-text);
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e2edf7;
}

.terms-section p {
  color: #3a5573;
  line-height: 1.6;
  margin-bottom: 12px;
}

.terms-section ul {
  margin-left: 20px;
  color: #3a5573;
  line-height: 1.6;
}

.terms-section li {
  margin-bottom: 8px;
}

@media (max-width: 768px) {
  .terms-view {
    padding: 24px 16px;
  }
  
  .terms-header h1 {
    font-size: 24px;
  }
  
  .terms-section h2 {
    font-size: 18px;
  }
}
</style>