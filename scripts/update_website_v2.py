#!/usr/bin/env python3
"""
TechInsight Hub 网站更新脚本 v2.0
支持：多平台热榜数据、热点解读、推荐阅读
"""

import json
import re
from datetime import datetime
from pathlib import Path

def load_api_data():
    """加载API数据"""
    with open('api/tech-news.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_insight_section(insight_data):
    """生成今日热点解读板块HTML"""
    content = insight_data.get('content', '')
    title = insight_data.get('title', '今日AI热点解读')
    updated = insight_data.get('updatedAt', datetime.now().strftime('%Y年%m月%d日'))
    
    # 将markdown转换为HTML
    html_content = content
    html_content = re.sub(r'## (.+)', r'<h3 class="insight-title">\1</h3>', html_content)
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'- (.+)', r'<li>\1</li>', html_content)
    html_content = html_content.replace('\n\n', '</p><p>')
    html_content = html_content.replace('\n', '<br>')
    
    # 包装li元素
    if '<li>' in html_content:
        html_content = html_content.replace('<li>', '<ul class="insight-list"><li>', 1)
        # 在最后一个li后关闭ul
        parts = html_content.rsplit('</li>', 1)
        if len(parts) == 2:
            html_content = parts[0] + '</li></ul>' + parts[1]
    
    return f'''            <!-- 今日热点解读 -->
            <section class="insight-section">
                <div class="insight-header">
                    <div class="insight-icon">🔥</div>
                    <div class="insight-info">
                        <h2>{title}</h2>
                        <span class="insight-update">{updated} · 基于知乎、微博、Hacker News等多平台数据分析</span>
                    </div>
                </div>
                <div class="insight-content">
                    <p>{html_content}</p>
                </div>
                <div class="insight-tags">
                    <span class="insight-tag">📊 数据驱动</span>
                    <span class="insight-tag">🤖 AI分析</span>
                    <span class="insight-tag">🌐 多平台聚合</span>
                </div>
            </section>
'''

def generate_recommended_section(recommended):
    """生成推荐阅读板块HTML"""
    items_html = ''
    for item in recommended:
        platform_icon = {
            'zhihu': '📚',
            'hackernews': '💻',
            'weibo': '📱',
            'baidu': '🔍'
        }.get(item.get('platform', ''), '📄')
        
        items_html += f'''                    <a href="{item['url']}" target="_blank" class="recommended-item">
                        <div class="recommended-icon">{platform_icon}</div>
                        <div class="recommended-content">
                            <h4>{item['title']}</h4>
                            <span class="recommended-source">{item.get('source', 'Tech News')}</span>
                        </div>
                        <span class="recommended-arrow">→</span>
                    </a>
'''
    
    return f'''            <!-- 推荐阅读 -->
            <section class="recommended-section">
                <h3 class="section-subtitle">📖 深度阅读</h3>
                <div class="recommended-list">
{items_html}                </div>
            </section>
'''

def generate_news_card(article, index):
    """生成新闻卡片HTML"""
    is_featured = index == 0
    
    if is_featured:
        return f'''                <!-- Featured -->
                <article class="card featured-card hot">
                    <div class="featured-content">
                        <span class="card-tag hot">FEATURED · {article.get('tag', 'AI热点')}</span>
                        <h2>{article['title']}</h2>
                        <p>{article['summary']}</p>
                        <div class="featured-tags">
                            <span class="featured-tag">🔥 热门</span>
                            <span class="featured-tag">{article.get('source', 'News')}</span>
                            <span class="featured-tag">{article.get('category', 'AI')}</span>
                        </div>
                        <a href="{article['url']}" class="card-link hot" target="_blank">深度分析 →</a>
                    </div>
                    <div class="featured-visual">
                        <div class="code-preview">
                            <div><span class="comment">// {article.get('date', '今天')} AI动态</span></div>
                            <div><span class="keyword">source</span>: <span class="string">"{article.get('source', 'News')}"</span></div>
                            <div><span class="keyword">views</span>: <span class="string">{article.get('views', 5000)}</span></div>
                            <div><span class="keyword">tag</span>: <span class="string">"{article.get('tag', 'AI')}"</span></div>
                        </div>
                    </div>
                </article>'''
    else:
        return f'''                <article class="card hot">
                    <div class="card-header">
                        <span class="card-tag hot">{article.get('tag', 'AI热点')}</span>
                        <span class="card-date">{article.get('date', '今天')}</span>
                    </div>
                    <h3>{article['title']}</h3>
                    <p>{article['summary']}</p>
                    <div class="card-meta">
                        <span>🔥 {article.get('source', 'News')}</span>
                        <span>👁️ {article.get('views', 5000)}</span>
                    </div>
                    <a href="{article['url']}" class="card-link hot" target="_blank">查看详情 →</a>
                </article>'''

def add_insight_styles():
    """生成热点解读板块样式"""
    return '''
        /* 今日热点解读样式 */
        .insight-section {
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(139, 92, 246, 0.1));
            border: 1px solid rgba(236, 72, 153, 0.3);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .insight-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #ec4899, #8b5cf6, #3b82f6);
        }
        
        .insight-header {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .insight-icon {
            font-size: 2.5rem;
            line-height: 1;
        }
        
        .insight-info h2 {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            background: linear-gradient(135deg, #ec4899, #f43f5e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .insight-update {
            font-size: 0.85rem;
            color: var(--text-muted);
        }
        
        .insight-content {
            font-size: 0.95rem;
            line-height: 1.8;
            color: var(--text-secondary);
        }
        
        .insight-content h3 {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 1.5rem 0 0.75rem;
        }
        
        .insight-content ul {
            margin: 0.75rem 0;
            padding-left: 1.5rem;
        }
        
        .insight-content li {
            margin: 0.5rem 0;
            position: relative;
        }
        
        .insight-content li::before {
            content: '▸';
            position: absolute;
            left: -1rem;
            color: var(--accent-hot);
        }
        
        .insight-tags {
            display: flex;
            gap: 0.5rem;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }
        
        .insight-tag {
            padding: 0.375rem 0.75rem;
            background: rgba(236, 72, 153, 0.15);
            border-radius: 100px;
            font-size: 0.8rem;
            color: var(--accent-hot);
        }
        
        /* 推荐阅读样式 */
        .recommended-section {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .section-subtitle {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }
        
        .recommended-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
        }
        
        @media (max-width: 768px) {
            .recommended-list {
                grid-template-columns: 1fr;
            }
        }
        
        .recommended-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 1rem;
            background: var(--bg-secondary);
            border-radius: 12px;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s;
            border: 1px solid transparent;
        }
        
        .recommended-item:hover {
            background: var(--bg-hover);
            border-color: var(--border);
            transform: translateX(4px);
        }
        
        .recommended-icon {
            font-size: 1.5rem;
            flex-shrink: 0;
        }
        
        .recommended-content {
            flex: 1;
            min-width: 0;
        }
        
        .recommended-content h4 {
            font-size: 0.95rem;
            font-weight: 500;
            margin-bottom: 0.25rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .recommended-source {
            font-size: 0.8rem;
            color: var(--text-muted);
        }
        
        .recommended-arrow {
            font-size: 1.25rem;
            color: var(--text-muted);
            transition: all 0.2s;
        }
        
        .recommended-item:hover .recommended-arrow {
            color: var(--accent-ai);
            transform: translateX(4px);
        }
'''

def update_website():
    """更新网站"""
    print("🔄 加载API数据...")
    data = load_api_data()
    
    articles = data['categories'][0]['articles']
    insight = data.get('insight', {})
    recommended = data.get('recommended', [])
    
    today = datetime.now().strftime('%Y年%m月%d日')
    
    print(f"📅 更新日期: {today}")
    print(f"📰 文章数量: {len(articles)}")
    print(f"🔥 热点解读: {'有' if insight else '无'}")
    print(f"📖 推荐阅读: {len(recommended)} 条")
    
    # 读取当前index.html
    print("📝 读取 index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 更新日期
    html = re.sub(r'最后更新: \d{4}年\d{2}月\d{2}日', f'最后更新: {today}', html)
    html = re.sub(r'每日更新 · \d{4}年\d{2}月\d{2}日', f'每日更新 · {today}', html)
    
    # 添加新样式（如果不存在）
    if '.insight-section' not in html:
        print("🎨 添加新样式...")
        style_match = re.search(r'(</style>)', html)
        if style_match:
            new_styles = add_insight_styles()
            html = html[:style_match.start()] + new_styles + html[style_match.start():]
    
    # 生成热点解读板块
    insight_html = ''
    if insight:
        print("📝 生成热点解读板块...")
        insight_html = generate_insight_section(insight)
    
    # 生成推荐阅读板块
    recommended_html = ''
    if recommended:
        print("📚 生成推荐阅读板块...")
        recommended_html = generate_recommended_section(recommended)
    
    # 生成新闻卡片
    print("🔥 生成AI热点卡片...")
    news_cards = '\n\n'.join([generate_news_card(article, i) for i, article in enumerate(articles)])
    
    # 替换AI热点部分 - 保留section标签，替换内容
    # 找到AI热点section的位置
    hot_section_start = html.find('<section id="hot" class="section active">')
    if hot_section_start == -1:
        hot_section_start = html.find('<section id="hot"')
    
    if hot_section_start != -1:
        # 找到section结束位置
        section_content_start = html.find('>', hot_section_start) + 1
        
        # 找到这个section的结束（下一个</section>或下一个<section）
        next_section = html.find('<section', section_content_start)
        if next_section == -1:
            next_section = len(html)
        
        # 构建新的section内容
        new_section_content = f'''
            {insight_html}
            {recommended_html}
            <div class="section-header">
                <h2 class="section-title hot">
                    <span>🔥</span>
                    AI热点
                </h2>
                <span class="update-time">最后更新: {today}</span>
            </div>
            <div class="cards-grid">
{news_cards}
            </div>
'''
        
        # 替换
        html = html[:section_content_start] + new_section_content + html[next_section:]
    
    # 保存
    print("💾 保存更新后的 index.html...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ 网站更新完成!")
    print(f"   📰 AI热点: {len(articles)} 条")
    print(f"   🔥 热点解读: {'已添加' if insight else '无'}")
    print(f"   📖 推荐阅读: {len(recommended)} 条")

if __name__ == '__main__':
    update_website()
