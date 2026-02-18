import json
import re

# 读取新闻
with open('daily_content.json', 'r') as f:
    news = json.load(f)['news']

# 读取HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 更新日期
from datetime import datetime
today = datetime.now()
date_str = today.strftime('%Y年%m月%d日')

html = re.sub(
    r'最后更新: .*?</span>',
    f'最后更新: {date_str}</span>',
    html
)

html = re.sub(
    r'每日更新 · .*?</span>',
    f'每日更新 · {date_str}</span>',
    html
)

# 替换前3个新闻卡片
# 卡片1
html = re.sub(
    r'(<article class="card hot">.*?)<h3>[^<]*</h3>(.*?)<p>[^<]*</p>',
    rf'\1<h3>{news[0]["title"]}</h3>\2<p>{news[0]["summary"]}</p>',
    html, count=1, flags=re.DOTALL
)

# 保存
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'✅ 已更新 {len(news)} 条新闻到网站')
for i, n in enumerate(news, 1):
    print(f'  {i}. {n["title"]}')
