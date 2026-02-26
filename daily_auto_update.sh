#!/bin/bash
# AI科技前沿网站每日自动更新脚本

cd ~/tech

echo "🚀 开始更新 AI 科技前沿网站..."
echo "⏰ 更新时间: $(date '+%Y-%m-%d %H:%M:%S')"

# 1. 搜索最新中文 AI 新闻
echo "🔍 正在搜索今日中文 AI 新闻..."
python3 << 'EOF'
from duckduckgo_search import DDGS
import json
from datetime import datetime

news_list = []
queries = [
    '人工智能 AI 大模型 中国',
    'DeepSeek 国产大模型',
    '百度 阿里 腾讯 AI',
    '英伟达 AI 芯片 中国',
    'OpenAI 中国 AI'
]

with DDGS() as ddgs:
    for query in queries:
        results = list(ddgs.news(query, region='cn-zh', timelimit='d', max_results=5))
        for r in results:
            news_list.append({
                'title': r['title'],
                'source': r['source'],
                'url': r['url'],
                'date': r['date'],
                'body': r['body']
            })

# 去重
seen = set()
unique_news = []
for n in news_list:
    if n['title'] not in seen and len(unique_news) < 15:
        seen.add(n['title'])
        unique_news.append(n)

# 保存数据
with open('daily_news_data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'date': datetime.now().strftime('%Y-%m-%d'),
        'count': len(unique_news),
        'news': unique_news
    }, f, ensure_ascii=False, indent=2)

print(f"✅ 获取 {len(unique_news)} 条新闻")
EOF

# 2. 更新网站内容
echo "📝 正在更新网站内容..."
python3 update_website_from_news.py

# 3. 提交到 GitHub
echo "📤 正在推送到 GitHub..."
git add -A
git commit -m "📰 每日更新: $(date '+%Y-%m-%d')"
git push origin main

echo "✅ 网站更新完成！"
echo "🌐 访问地址: https://mingmfu.github.io/tech/"
