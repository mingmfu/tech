const fs = require('fs');
const path = require('path');

// 读取新的JSON数据
const jsonPath = '/Users/brightfu/.openclaw/workspace/hxzb_spider/output/anhui_audit_full_20260314_152202.json';
const jsonData = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

// 读取模板和样式
const templatePath = './src/template.html';
const template = fs.readFileSync(templatePath, 'utf8');
const styles = fs.readFileSync('./src/styles.css', 'utf8');

// 生成HTML
const html = generateHTML(jsonData, template, styles);

// 写入index.html
fs.writeFileSync('./index.html', html, 'utf8');
console.log('✅ index.html 生成成功');

function generateHTML(data, template, styles) {
  const projects = data.projects;
  const meta = data.meta;
  
  // 统计数据
  const stats = calculateStats(projects);
  
  // 生成所有项目卡片（按截止日期排序）
  const sortedProjects = projects.sort((a, b) => {
    const dateA = new Date(a.bid_deadline || '2099-12-31');
    const dateB = new Date(b.bid_deadline || '2099-12-31');
    return dateA - dateB;
  });
  
  const projectCards = sortedProjects.map((p, index) => generateProjectCard(p, index)).join('\n');
  
  // 替换模板变量
  let html = template;
  html = html.replace('{{styles}}', styles);
  html = html.replace('{{title}}', '安徽审计招标信息仪表板 - 专业版');
  html = html.replace(/{{siteName}}/g, '安徽审计招标信息仪表板');
  html = html.replace(/{{subtitle}}/g, `合信招标网安徽地区审计项目 | 共${meta.keywords.length}类关键词 | 实时更新`);
  html = html.replace(/{{updateTime}}/g, meta.generated_at);
  html = html.replace(/{{totalProjects}}/g, projects.length);
  html = html.replace(/{{highAmountCount}}/g, stats.highAmount);
  html = html.replace(/{{midAmountCount}}/g, stats.midAmount);
  html = html.replace(/{{unknownAmountCount}}/g, stats.unknownAmount);
  html = html.replace('{{projectCards}}', projectCards);
  
  return html;
}

function calculateStats(projects) {
  let highAmount = 0; // >=30万
  let midAmount = 0;  // 10-30万
  let unknownAmount = 0;
  
  projects.forEach(p => {
    const amount = parseAmount(p.budget_amount);
    if (amount >= 30) highAmount++;
    else if (amount >= 10) midAmount++;
    else if (amount === 0) unknownAmount++;
  });
  
  return { highAmount, midAmount, unknownAmount };
}

function parseAmount(amountStr) {
  if (!amountStr || amountStr.includes('标项名称') || amountStr === '') return 0;
  
  // 提取数字
  const match = amountStr.match(/(\d+\.?\d*)/);
  if (!match) return 0;
  
  let value = parseFloat(match[1]);
  
  // 转换单位
  if (amountStr.includes('万元')) {
    return value; // 已经是万元
  } else if (amountStr.includes('元')) {
    return value / 10000; // 转换为万元
  }
  
  return value;
}

function formatAmount(amountStr) {
  const value = parseAmount(amountStr);
  if (value === 0) return '待查';
  if (value >= 10000) {
    return `${(value / 10000).toFixed(2)}亿元`;
  }
  return `${value.toFixed(2)}万元`;
}

function getAmountClass(amountStr) {
  const value = parseAmount(amountStr);
  if (value >= 30) return 'amount-high';
  if (value >= 10) return 'amount-mid';
  if (value > 0) return 'amount-low';
  return 'amount-unknown';
}

function generateProjectCard(project, index) {
  const amount = formatAmount(project.budget_amount);
  const amountClass = getAmountClass(project.budget_amount);
  const projectId = `project-${index}`;
  
  // 生成详情字段HTML
  const detailFields = [];
  
  if (project.qualification && project.qualification.trim()) {
    detailFields.push(`<div class="detail-field"><strong>资质要求：</strong>${project.qualification}</div>`);
  }
  if (project.service_period && project.service_period.trim()) {
    detailFields.push(`<div class="detail-field"><strong>服务期限：</strong>${project.service_period}</div>`);
  }
  if (project.category && project.category.trim()) {
    detailFields.push(`<div class="detail-field"><strong>项目类别：</strong>${project.category}</div>`);
  }
  if (project.keyword && project.keyword.trim()) {
    detailFields.push(`<div class="detail-field"><strong>匹配关键词：</strong>${project.keyword}</div>`);
  }
  if (project.extracted_at && project.extracted_at.trim()) {
    detailFields.push(`<div class="detail-field" style="color: #64748b; font-size: 0.75rem;"><strong>数据提取时间：</strong>${project.extracted_at}</div>`);
  }
  
  const detailsHtml = detailFields.length > 0 
    ? detailFields.join('') 
    : '<div class="detail-field" style="color: #64748b;">暂无详细信息，请查看招标原文</div>';
  
  // 判断是否即将截止（3天内）
  const isUrgent = isDeadlineUrgent(project.bid_deadline);
  const deadlineClass = isUrgent ? 'style="color: #ef4444; font-weight: 600;"' : '';
  const deadlineIcon = isUrgent ? '⚠️ ' : '';
  
  return `
    <div class="project-card" id="${projectId}">
      <div class="card-header">
        <span class="amount-badge ${amountClass}">${amount}</span>
        <span class="tag" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa;">${project.region}</span>
      </div>
      
      <h3 class="project-title">${project.project_name}</h3>
      
      <div class="tags">
        ${project.category ? `<span class="tag">${project.category}</span>` : ''}
        ${project.keyword ? `<span class="tag" style="background: rgba(139, 92, 246, 0.2); color: #a78bfa;">${project.keyword}</span>` : ''}
        ${project.publish_date ? `<span class="tag" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">发布：${project.publish_date}</span>` : ''}
      </div>
      
      <div class="project-meta">
        ${project.tender_org ? `
        <div class="meta-item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/>
            <path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/>
            <path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/>
          </svg>
          ${project.tender_org}
        </div>
        ` : ''}
        
        <div class="meta-item" ${deadlineClass}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
            <line x1="16" y1="2" x2="16" y2="6"/>
            <line x1="8" y1="2" x2="8" y2="6"/>
            <line x1="3" y1="10" x2="21" y2="10"/>
          </svg>
          ${deadlineIcon}截止：${project.bid_deadline || '待定'}
        </div>
        
        ${project.project_code ? `
        <div class="meta-item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 7V4h3M4 17v3h3M20 7V4h-3M20 17v3h-3M9 9h6v6H9z"/>
          </svg>
          编号：${project.project_code}
        </div>
        ` : ''}
      </div>
      
      <!-- Expandable Details -->
      <div class="details-section" id="details-${projectId}" style="display: none; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
        <h4 style="font-size: 0.875rem; color: #60a5fa; margin-bottom: 0.75rem; font-weight: 600;">📋 详细信息</h4>
        <div style="font-size: 0.8125rem; line-height: 1.6; color: #cbd5e1;">
          ${detailsHtml}
        </div>
      </div>
      
      <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
        <button onclick="toggleDetails('${projectId}')" class="btn-primary" style="flex: 1; background: #334155;">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          <span id="btn-text-${projectId}">查看详情</span>
        </button>
        
        <a href="${project.detail_url}" target="_blank" class="btn-primary" style="flex: 1;" 
           onclick="showLoginHelp(event)"
           title="点击后将跳转到招标网站，需要手动登录">
          招标原文
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
            <polyline points="15 3 21 3 21 9"/>
            <line x1="10" y1="14" x2="21" y2="3"/>
          </svg>
        </a>
      </div>
    </div>
  `;
}

function isDeadlineUrgent(deadlineStr) {
  if (!deadlineStr) return false;
  
  try {
    const deadline = new Date(deadlineStr);
    const now = new Date();
    const diffTime = deadline - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    return diffDays >= 0 && diffDays <= 3;
  } catch (e) {
    return false;
  }
}
