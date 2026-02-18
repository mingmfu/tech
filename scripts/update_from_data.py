import json
import re
from datetime import datetime

with open('daily_content.json', 'r') as f:
    data = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

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

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Updated: {len(data["news"])} news, {len(data["papers"])} papers')
