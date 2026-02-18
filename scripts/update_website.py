#!/usr/bin/env python3
"""
TechInsight Hub 网站自动更新脚本
使用 api/tech-news.json 更新 index.html
"""

import json
import re
from datetime import datetime
from pathlib import Path

def load_json_data():
    """加载JSON数据"""
    with open('api/tech-news.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_hot_card(article, index):
    """生成AI热点卡片HTML"""
    is_featured = index == 0
    
    if is_featured:
        return f'''                <!-- Featured -->
                <article class="card featured-card hot">
                    <div class="featured-content">
                        <span class="card-tag hot">FEATURED · {article['tag']}</span>
                        <h2>{article['title']}</h2>
                        <p>{article['summary'][:200]}...</p>
                        <div class="featured-tags">
                            <span class="featured-tag">AI</span>
                            <span class="featured-tag">热点</span>
                            <span class="featured-tag">{article['source']}</span>
                        </div>
                        <a href="{article['url']}" class="card-link hot" target="_blank">深度分析 →</a>
                    </div>
                    <div class="featured-visual">
                        <div class="code-preview">
                            <div><span class="comment">// {article['date']} AI动态</span></div>
                            <div><span class="keyword">source</span>: <span class="string">"{article['source']}"</span></div>
                            <div><span class="keyword">views</span>: <span class="string">{article['views']}</span></div>
                            <div><span class="keyword">tag</span>: <span class="string">"{article['tag']}"</span></div>
                        </div>
                    </div>
                </article>'''
    else:
        return f'''                <article class="card hot">
                    <div class="card-header">
                        <span class="card-tag hot">{article['tag']}</span>
                        <span class="card-date">{article['date']}</span>
                    </div>
                    <h3>{article['title']}</h3>
                    <p>{article['summary'][:120]}...</p>
                    <div class="card-meta">
                        <span>🔥 {article['source']}</span>
                        <span>👁️ {article['views']}</span>
                    </div>
                    <a href="{article['url']}" class="card-link hot" target="_blank">查看详情 →</a>
                </article>'''

def generate_ai_card(article, index):
    """生成AI学术卡片HTML"""
    is_featured = index == 0
    
    if is_featured:
        return f'''                <!-- Featured -->
                <article class="card featured-card ai">
                    <div class="featured-content">
                        <span class="card-tag ai">FEATURED · {article['tag']}</span>
                        <h2>{article['title']}</h2>
                        <p>{article['summary'][:200]}...</p>
                        <div class="featured-tags">
                            <span class="featured-tag">AI</span>
                            <span class="featured-tag">学术</span>
                            <span class="featured-tag">{article['source']}</span>
                        </div>
                        <a href="{article['url']}" class="card-link ai" target="_blank">阅读论文 →</a>
                    </div>
                    <div class="featured-visual">
                        <div class="code-preview">
                            <div><span class="comment">// {article['date']} 学术论文</span></div>
                            <div><span class="keyword">source</span>: <span class="string">"{article['source']}"</span></div>
                            <div><span class="keyword">views</span>: <span class="string">{article['views']}</span></div>
                            <div><span class="keyword">tag</span>: <span class="string">"{article['tag']}"</span></div>
                        </div>
                    </div>
                </article>'''
    else:
        return f'''                <article class="card ai">
                    <div class="card-header">
                        <span class="card-tag ai">{article['tag']}</span>
                        <span class="card-date">{article['date']}</span>
                    </div>
                    <h3>{article['title']}</h3>
                    <p>{article['summary'][:150]}...</p>
                    <div class="card-meta">
                        <span>📄 {article['source']}</span>
                        <span>⭐ {article['views']}</span>
                    </div>
                    <a href="{article['url']}" class="card-link ai" target="_blank">查看详情 →</a>
                </article>'''

def update_website():
    """更新网站"""
    print("🔄 加载JSON数据...")
    data = load_json_data()
    
    hot_articles = data['categories'][0]['articles']
    ai_articles = data['categories'][1]['articles']
    
    # 从JSON的lastUpdated获取日期，确保与JSON一致
    last_updated = data.get('lastUpdated', datetime.now().isoformat())
    if isinstance(last_updated, str):
        # 解析ISO格式日期
        try:
            dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
            today = dt.strftime('%Y年%m月%d日')
        except:
            today = datetime.now().strftime('%Y年%m月%d日')
    else:
        today = datetime.now().strftime('%Y年%m月%d日')
    
    # 同时获取当前时间用于显示
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"📅 JSON最后更新: {last_updated}")
    print(f"📅 网站显示日期: {today}")
    print(f"⏰ 当前时间: {current_time}")
    
    # 读取当前index.html
    print("📝 读取 index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 更新所有日期显示
    print("📅 更新所有日期显示...")
    
    # 1. 更新 hero-badge 中的日期
    html = re.sub(r'(<div class="hero-badge">.*?<span>每日更新 · )\d{4}年\d{2}月\d{2}日(</span>)', 
                  rf'\g<1>{today}\g<2>', html, flags=re.DOTALL)
    
    # 2. 更新 section-header 中的最后更新日期
    html = re.sub(r'(<span class="update-time">最后更新: )\d{4}年\d{2}月\d{2}日(</span>)', 
                  rf'\g<1>{today}\g<2>', html)
    
    # 3. 备用：直接替换所有日期格式
    html = re.sub(r'最后更新: \d{4}年\d{2}月\d{2}日', f'最后更新: {today}', html)
    html = re.sub(r'每日更新 · \d{4}年\d{2}月\d{2}日', f'每日更新 · {today}', html)
    
    # 生成AI热点卡片
    print("🔥 生成AI热点卡片...")
    hot_cards = '\n\n'.join([generate_hot_card(article, i) for i, article in enumerate(hot_articles[:9])])
    
    # 替换AI热点部分
    hot_pattern = r'(<section id="hot" class="section active">.*?<div class="cards-grid">)\s*.*?(</div>\s*<div class="timeline")'
    hot_replacement = f'\\1\n{hot_cards}\n            \\2'
    html = re.sub(hot_pattern, hot_replacement, html, flags=re.DOTALL)
    
    # 生成AI学术卡片
    print("🎓 生成AI学术卡片...")
    ai_cards = '\n\n'.join([generate_ai_card(article, i) for i, article in enumerate(ai_articles[:6])])
    
    # 替换AI学术部分
    ai_pattern = r'(<section id="ai" class="section">.*?<div class="cards-grid">)\s*.*?(</div>\s*<div class="timeline")'
    ai_replacement = f'\\1\n{ai_cards}\n            \\2'
    html = re.sub(ai_pattern, ai_replacement, html, flags=re.DOTALL)
    
    # 保存更新后的HTML
    print("💾 保存更新后的 index.html...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ 网站更新完成!")
    print(f"   📰 AI热点: {len(hot_articles[:9])} 条")
    print(f"   📄 AI学术: {len(ai_articles[:6])} 篇")
    print(f"   📅 更新日期: {today}")

if __name__ == '__main__':
    update_website()
