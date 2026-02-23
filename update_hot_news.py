#!/usr/bin/env python3
"""更新网站热点内容"""
import json
import re
from datetime import datetime

# 加载新闻数据
with open('api/tech-news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

articles = data['categories'][0]['articles']
today = datetime.now().strftime('%Y-%m-%d')

# 读取当前index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 生成新的热点卡片HTML
cards_html = ""
for article in articles:
    tag_class = "ai"
    tag_text = article.get('tag', 'AI热点')
    if '国内' in tag_text:
        tag_display = tag_text.replace('国内 · ', '')
    elif '国际' in tag_text:
        tag_display = tag_text.replace('国际 · ', '')
    else:
        tag_display = tag_text
    
    cards_html += f'''                <article class="card">
                    <span class="card-tag {tag_class}">{tag_display}</span>
                    <h3>{article['title']}</h3>
                    <p>{article['summary'][:220]}...</p>
                    <div class="card-meta">
                        <span>{article.get('source', 'Tech News')}</span>
                        <a href="{article['url']}" class="card-link" target="_blank">查看 →</a>
                    </div>
                </article>
'''

# 找到"本周热点速览"部分并替换
pattern = r'(<h2 class="section-title">🔥 本周热点速览</h2>.*?<span class="update-time">)(.*?)(</span>.*?</div>.*?<div class="cards-grid">)(.*?)(</div>)'

new_section = rf'''\1最后更新: {today}\3
{cards_html}            \5'''

html_new = re.sub(pattern, new_section, html, flags=re.DOTALL)

# 保存更新后的HTML
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_new)

print(f"✅ 已更新 index.html")
print(f"   - 替换为 {len(articles)} 条AI热点")
print(f"   - 更新日期: {today}")

# 统计
domestic = len([a for a in articles if '国内' in a.get('tag', '')])
international = len([a for a in articles if '国际' in a.get('tag', '')])
print(f"   - 国内: {domestic} 条")
print(f"   - 国际: {international} 条")
