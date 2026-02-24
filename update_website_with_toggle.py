#!/usr/bin/env python3
"""更新网站热点内容 - 带展开/折叠样式"""
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

# 生成分布式展开/折叠的卡片HTML
cards_html = ""
for i, article in enumerate(articles):
    tag_class = "ai"
    tag_text = article.get('tag', 'AI热点')
    if '国内' in tag_text:
        tag_display = tag_text.replace('国内 · ', '')
    elif '国际' in tag_text:
        tag_display = tag_text.replace('国际 · ', '')
    else:
        tag_display = tag_text
    
    summary = article['summary']
    short_summary = summary[:120] + "..." if len(summary) > 120 else summary
    
    cards_html += f'''                <article class="card">
                    <span class="card-tag {tag_class}">{tag_display}</span>
                    <h3>{article['title']}</h3>
                    <div class="news-summary">
                        <p class="summary-short">{short_summary}</p>
                        <div class="summary-full" id="summary-{i}" style="display: none;">
                            <p>{summary}</p>
                        </div>
                        <button class="toggle-btn" onclick="toggleSummary({i})" data-target="{i}">展开 ▼</button>
                    </div>
                    <div class="card-meta">
                        <span>{article.get('source', 'Tech News')}</span>
                        <a href="{article['url']}" class="card-link" target="_blank">查看原文 →</a>
                    </div>
                </article>
'''

# 找到"本周热点速览"部分并替换
pattern = r'(<h2 class="section-title">🔥 本周热点速览</h2>.*?<span class="update-time">)(.*?)(</span>.*?</div>.*?<div class="cards-grid">)(.*?)(</div>\s*</div>\s*<!-- Featured Tech Report -->)'

new_section = rf'''<div class="section-header">
                <h2 class="section-title">🔥 AI热点（国内10条 + 国际10条）</h2>
                <span class="update-time">最后更新: {today}</span>
            </div>
            
            <div class="cards-grid">
{cards_html}            </div>
            
            <!-- Featured Tech Report -->'''

html_new = re.sub(pattern, new_section, html, flags=re.DOTALL)

# 添加展开/折叠的CSS样式
toggle_css = '''        .news-summary {
            position: relative;
        }
        .summary-short {
            margin: 0;
        }
        .summary-full {
            margin-top: 0.5rem;
        }
        .summary-full p {
            margin: 0;
            line-height: 1.8;
        }
        .toggle-btn {
            background: transparent;
            border: none;
            color: var(--accent-ai);
            cursor: pointer;
            font-size: 0.85rem;
            padding: 0.25rem 0;
            margin-top: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        .toggle-btn:hover {
            text-decoration: underline;
        }
'''

# 在 </style> 前添加CSS
html_new = html_new.replace('</style>', toggle_css + '</style>')

# 添加展开/折叠的JavaScript
toggle_js = '''
    <script>
        function toggleSummary(id) {
            const fullSummary = document.getElementById('summary-' + id);
            const btn = document.querySelector('button[data-target="' + id + '"]');
            if (fullSummary.style.display === 'none') {
                fullSummary.style.display = 'block';
                btn.textContent = '收起 ▲';
            } else {
                fullSummary.style.display = 'none';
                btn.textContent = '展开 ▼';
            }
        }
    </script>
'''

# 在 </body> 前添加JS
html_new = html_new.replace('</body>', toggle_js + '</body>')

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

# 检查摘要字数
min_len = min(len(a.get('summary', '')) for a in articles)
max_len = max(len(a.get('summary', '')) for a in articles)
all_ok = all(len(a.get('summary', '')) >= 200 for a in articles)
print(f"\n📏 摘要字数统计:")
print(f"   最短: {min_len} 字")
print(f"   最长: {max_len} 字")
print(f"   全部达标: {'✅' if all_ok else '❌'} (200字以上)")
print(f"\n📐 展开/折叠样式: ✅ 已添加")
