const fs = require('fs');
const path = require('path');

// 读取JSON数据
const jsonPath = './tender_collection_expert_20260314_152000.json';
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
  const projects = data['项目列表'];
  const meta = data['采集元数据'];
  
  // 统计数据
  const stats = calculateStats(projects);
  
  // 排序获取Top 3
  const top3 = getTopRecommendations(projects);
  
  // 生成所有项目卡片
  const projectCards = projects.map((p, index) => generateProjectCard(p, index)).join('\n');
  
  // 生成Top 3卡片
  const topRecommendations = top3.map((p, index) => 
    generateRecommendationCard(p, index + 1)
  ).join('\n');
  
  // 替换模板变量
  let html = template;
  html = html.replace('{{styles}}', styles);
  html = html.replace('{{title}}', '安徽审计招标信息仪表板 - 专业版');
  html = html.replace(/{{siteName}}/g, '安徽审计招标信息仪表板');
  html = html.replace(/{{subtitle}}/g, '合信招标网安徽地区审计项目 | 实时更新');
  html = html.replace(/{{updateTime}}/g, meta['采集时间']);
  html = html.replace(/{{totalProjects}}/g, projects.length);
  html = html.replace(/{{highAmountCount}}/g, stats.highAmount);
  html = html.replace(/{{midAmountCount}}/g, stats.midAmount);
  html = html.replace(/{{unknownAmountCount}}/g, stats.unknownAmount);
  html = html.replace('{{topRecommendations}}', topRecommendations);
  html = html.replace('{{projectCards}}', projectCards);
  
  return html;
}

function calculateStats(projects) {
  let highAmount = 0; // >=30
  let midAmount = 0;  // 10-30
  let unknownAmount = 0;
  
  projects.forEach(p => {
    const amount = parseFloat(p['项目详情']['项目金额']) || 0;
    if (amount >= 30) highAmount++;
    else if (amount >= 10) midAmount++;
    else if (amount === 0) unknownAmount++;
  });
  
  return { highAmount, midAmount, unknownAmount };
}

function getTopRecommendations(projects) {
  return projects
    .filter(p => p['评分'] && p['评分']['总分'])
    .sort((a, b) => b['评分']['总分'] - a['评分']['总分'])
    .slice(0, 3);
}

function generateRecommendationCard(project, rank) {
  const info = project['基本信息'];
  const detail = project['项目详情'];
  const score = project['评分'];
  const other = project['其他信息'];
  
  const amount = detail['项目金额'] ? `${detail['项目金额']}万元` : '金额待查';
  const amountClass = getAmountClass(detail['项目金额']);
  
  // 生成评分详情
  const scoreBreakdown = Object.entries(score['各维度得分'])
    .map(([key, value]) => {
      const percentage = (value / 20) * 100; // 假设满分20
      return `
        <div class="score-item">
          <span>${key}</span>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="color: #60a5fa; font-weight: 600;">${value}</span>
            <div class="score-bar">
              <div class="score-fill" style="width: ${percentage}%"></div>
            </div>
          </div>
        </div>
      `;
    }).join('');
  
  return `
    <div class="rec-card rank-${rank}">
      <div class="rank-badge">${rank}</div>
      <h3 class="project-title" style="padding-right: 3rem;">${info['项目名称']}</h3>
      <div class="meta-item" style="margin: 0.5rem 0;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/>
          <path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/>
          <path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/>
        </svg>
        ${project['单位信息']['招标单位']}
      </div>
      <div style="margin: 1rem 0;">
        <span class="amount-badge ${amountClass}">${amount}</span>
      </div>
      <div class="score-display">
        ${score['总分']}
        <span class="score-label">/ 100分</span>
      </div>
      <div class="score-breakdown">
        ${scoreBreakdown}
      </div>
      <a href="${other['公告原文链接']}" target="_blank" class="btn-primary" style="margin-top: 1rem;">
        查看详情
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
          <polyline points="15 3 21 3 21 9"/>
          <line x1="10" y1="14" x2="21" y2="3"/>
        </svg>
      </a>
    </div>
  `;
}

function generateProjectCard(project, index) {
  const info = project['基本信息'];
  const detail = project['项目详情'];
  const score = project['评分'];
  const other = project['其他信息'];
  const unit = project['单位信息'];
  const requirements = project['投标要求'];
  
  const amount = detail['项目金额'] ? `${detail['项目金额']}万元` : '待查';
  const amountClass = getAmountClass(detail['项目金额']);
  const scoreValue = score ? score['总分'] : 0;
  const projectId = `project-${index}`;
  
  // 生成详情字段HTML
  const detailFields = [];
  
  if (requirements['资质要求']) {
    detailFields.push(`<div class="detail-field"><strong>资质要求：</strong>${requirements['资质要求']}</div>`);
  }
  if (requirements['业绩要求']) {
    detailFields.push(`<div class="detail-field"><strong>业绩要求：</strong>${requirements['业绩要求']}</div>`);
  }
  if (requirements['人员要求']) {
    detailFields.push(`<div class="detail-field"><strong>人员要求：</strong>${requirements['人员要求']}</div>`);
  }
  if (requirements['投标保证金']) {
    detailFields.push(`<div class="detail-field"><strong>投标保证金：</strong>${requirements['投标保证金']}</div>`);
  }
  if (requirements['文件售价']) {
    detailFields.push(`<div class="detail-field"><strong>文件售价：</strong>${requirements['文件售价']}</div>`);
  }
  if (requirements['递交方式']) {
    detailFields.push(`<div class="detail-field"><strong>递交方式：</strong>${requirements['递交方式']}</div>`);
  }
  if (detail['质量标准']) {
    detailFields.push(`<div class="detail-field"><strong>质量标准：</strong>${detail['质量标准']}</div>`);
  }
  if (other['备注']) {
    detailFields.push(`<div class="detail-field" style="color: #fbbf24;"><strong>备注：</strong>${other['备注']}</div>`);
  }
  
  const detailsHtml = detailFields.length > 0 
    ? detailFields.join('') 
    : '<div class="detail-field" style="color: #64748b;">暂无详细要求信息</div>';
  
  return `
    <div class="project-card" id="${projectId}">
      <div class="card-header">
        <span class="amount-badge ${amountClass}">${amount}</span>
        <span class="score-badge">${scoreValue}分</span>
      </div>
      
      <h3 class="project-title">${info['项目名称']}</h3>
      
      <div class="tags">
        <span class="tag">${detail['服务范围'] || '审计服务'}</span>
        ${detail['服务期限'] ? `<span class="tag">${detail['服务期限']}</span>` : ''}
        ${info['发布日期'] ? `<span class="tag" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa;">发布：${info['发布日期']}</span>` : ''}
      </div>
      
      <div class="project-meta">
        <div class="meta-item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/>
            <path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/>
            <path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/>
          </svg>
          ${unit['招标单位']}
        </div>
        
        <div class="meta-item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
            <line x1="16" y1="2" x2="16" y2="6"/>
            <line x1="8" y1="2" x2="8" y2="6"/>
            <line x1="3" y1="10" x2="21" y2="10"/>
          </svg>
          截止：${info['截止时间']}
        </div>
        
        ${detail['项目地点'] ? `
        <div class="meta-item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          ${detail['项目地点']}
        </div>
        ` : ''}
      </div>
      
      ${detail['项目概况'] ? `<p style="color: #94a3b8; font-size: 0.875rem; margin: 1rem 0; line-height: 1.5;">${detail['项目概况']}</p>` : ''}
      
      <!-- Expandable Details -->
      <div class="details-section" id="details-${projectId}" style="display: none; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
        <h4 style="font-size: 0.875rem; color: #60a5fa; margin-bottom: 0.75rem; font-weight: 600;">📋 详细要求</h4>
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
        
        <a href="${other['公告原文链接']}" target="_blank" class="btn-primary" style="flex: 1;" title="需要登录：账号13167733815 / 密码dx13167733815">
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

function getAmountClass(amount) {
  const value = parseFloat(amount) || 0;
  if (value >= 30) return 'amount-high';
  if (value >= 10) return 'amount-mid';
  if (value > 0) return 'amount-low';
  return 'amount-unknown';
}
