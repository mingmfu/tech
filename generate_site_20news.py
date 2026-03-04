#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 daily_content.json 生成完整网站 HTML，国内国外各10条，带折叠展开
"""

import json
from datetime import datetime

# HTML 模板
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI科技前沿 - 每日人工智能产业情报</title>
    <meta name="description" content="汇聚全球AI产业最新动态、技术突破、商业洞察，每日更新">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #ec4899;
            --accent: #06b6d4;
            --bg-dark: #0f0f1a;
            --bg-card: #1a1a2e;
            --bg-hover: #252545;
            --text-primary: #ffffff;
            --text-secondary: #a1a1aa;
            --text-muted: #71717a;
            --border: #2e2e4a;
            --gradient-hero: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
            --gradient-card: linear-gradient(145deg, #1a1a2e 0%, #252545 100%);
            --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.15);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            line-height: 1.8;
            min-height: 100vh;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(236, 72, 153, 0.05) 0%, transparent 50%);
        }}

        header {{
            position: sticky;
            top: 0;
            z-index: 1000;
            background: rgba(15, 15, 26, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border);
        }}

        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1.25rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .logo-icon {{
            width: 48px;
            height: 48px;
            background: var(--gradient-hero);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        }}

        .logo-text h1 {{
            font-size: 1.5rem;
            font-weight: 700;
            background: var(--gradient-hero);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }}

        .logo-text p {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: -2px;
        }}

        .update-time {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--bg-card);
            border-radius: 20px;
            font-size: 0.85rem;
            color: var(--text-secondary);
            border: 1px solid var(--border);
        }}

        .update-time .live-dot {{
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        .hero {{
            padding: 4rem 2rem;
            text-align: center;
            max-width: 900px;
            margin: 0 auto;
        }}

        .hero h2 {{
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 1rem;
            line-height: 1.2;
        }}

        .hero h2 span {{
            background: var(--gradient-hero);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero p {{
            font-size: 1.2rem;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto 2rem;
        }}

        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 3rem;
            padding: 1.5rem;
            background: var(--bg-card);
            border-radius: 16px;
            border: 1px solid var(--border);
            max-width: 600px;
            margin: 0 auto;
        }}

        .stat-item {{
            text-align: center;
        }}

        .stat-item .number {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
        }}

        .stat-item .label {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        .news-section {{
            padding: 0 2rem 4rem;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .section-title {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 2rem;
            padding-left: 1rem;
            border-left: 4px solid var(--primary);
        }}

        .section-title h3 {{
            font-size: 1.5rem;
            font-weight: 700;
        }}

        .section-title .badge {{
            padding: 0.25rem 0.75rem;
            background: var(--primary);
            color: white;
            border-radius: 20px;
            font-size: 0.8rem;
        }}

        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 1.5rem;
        }}

        .news-card {{
            background: var(--gradient-card);
            border-radius: 16px;
            border: 1px solid var(--border);
            overflow: hidden;
            transition: all 0.3s ease;
        }}

        .news-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow-glow);
            border-color: var(--primary);
        }}

        .card-header {{
            padding: 1.5rem 1.5rem 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
        }}

        .card-category {{
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}

        .cat-domestic {{ background: rgba(34, 197, 94, 0.2); color: #22c55e; }}
        .cat-international {{ background: rgba(6, 182, 212, 0.2); color: #06b6d4; }}

        .card-date {{
            font-size: 0.8rem;
            color: var(--text-muted);
        }}

        .card-body {{
            padding: 0 1.5rem 1rem;
        }}

        .card-title {{
            font-size: 1.15rem;
            font-weight: 600;
            line-height: 1.5;
            margin-bottom: 0.75rem;
            color: var(--text-primary);
            text-decoration: none;
            display: block;
        }}

        .card-title:hover {{
            color: var(--primary);
        }}

        .card-source {{
            font-size: 0.85rem;
            color: var(--accent);
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .summary-container {{
            position: relative;
        }}

        .card-summary {{
            font-size: 0.95rem;
            color: var(--text-secondary);
            line-height: 1.8;
            overflow: hidden;
            transition: max-height 0.4s ease, mask-image 0.3s ease, -webkit-mask-image 0.3s ease;
        }}

        .card-summary.collapsed {{
            max-height: 100px;
            mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
            -webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
        }}

        .card-summary.expanded {{
            max-height: 2000px;
            mask-image: none;
            -webkit-mask-image: none;
        }}

        .toggle-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            margin-top: 0.75rem;
            padding: 0.4rem 0.8rem;
            background: transparent;
            border: 1px solid var(--border);
            border-radius: 20px;
            color: var(--primary);
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .toggle-btn:hover {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }}

        .toggle-btn .arrow {{
            transition: transform 0.3s ease;
        }}

        .toggle-btn.expanded .arrow {{
            transform: rotate(180deg);
        }}

        .card-footer {{
            padding: 1rem 1.5rem;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .read-more {{
            color: var(--primary);
            font-size: 0.9rem;
            font-weight: 500;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .tag-list {{
            display: flex;
            gap: 0.5rem;
        }}

        .tag {{
            padding: 0.25rem 0.6rem;
            background: var(--bg-dark);
            border-radius: 12px;
            font-size: 0.75rem;
            color: var(--text-muted);
        }}

        footer {{
            padding: 3rem 2rem;
            text-align: center;
            border-top: 1px solid var(--border);
            background: var(--bg-card);
        }}

        .footer-content {{
            max-width: 600px;
            margin: 0 auto;
        }}

        .footer-logo {{
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }}

        .footer-text {{
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
        }}

        .copyright {{
            font-size: 0.8rem;
            color: var(--text-muted);
        }}

        @media (max-width: 768px) {{
            .hero h2 {{ font-size: 2rem; }}
            .news-grid {{ grid-template-columns: 1fr; }}
            .stats-bar {{ flex-direction: column; gap: 1rem; }}
            .header-content {{ flex-direction: column; gap: 1rem; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <div class="logo">
                <div class="logo-icon">🚀</div>
                <div class="logo-text">
                    <h1>AI科技前沿</h1>
                    <p>每日人工智能产业情报</p>
                </div>
            </div>
            <div class="update-time">
                <span class="live-dot"></span>
                <span>更新于 {update_date}</span>
            </div>
        </div>
    </header>

    <section class="hero">
        <h2>探索 <span>AI</span> 的无限可能</h2>
        <p>汇聚全球人工智能最新动态、技术突破与商业洞察，每日为您精选最有价值的产业情报</p>
        <div class="stats-bar">
            <div class="stat-item">
                <div class="number">20</div>
                <div class="label">每日精选</div>
            </div>
            <div class="stat-item">
                <div class="number">200+</div>
                <div class="label">字深度摘要</div>
            </div>
            <div class="stat-item">
                <div class="number">24h</div>
                <div class="label">实时更新</div>
            </div>
        </div>
    </section>

    {news_sections}

    <footer>
        <div class="footer-content">
            <div class="footer-logo">🚀 AI科技前沿</div>
            <p class="footer-text">每日追踪全球 AI 产业动态，为您呈现最有价值的人工智能情报</p>
            <p class="copyright">© 2026 AI科技前沿 | 每日自动更新</p>
        </div>
    </footer>

    <script>
        function toggleSummary(btn) {{
            const container = btn.closest('.summary-container');
            const summary = container.querySelector('.card-summary');
            const isExpanded = summary.classList.contains('expanded');
            
            if (isExpanded) {{
                summary.classList.remove('expanded');
                summary.classList.add('collapsed');
                btn.classList.remove('expanded');
                btn.innerHTML = '展开 <span class="arrow">▼</span>';
            }} else {{
                summary.classList.remove('collapsed');
                summary.classList.add('expanded');
                btn.classList.add('expanded');
                btn.innerHTML = '收起 <span class="arrow">▲</span>';
            }}
        }}
    </script>
</body>
</html>'''

NEWS_CARD_TEMPLATE = '''            <article class="news-card">
                <div class="card-header">
                    <span class="card-category cat-{category_class}">{category}</span>
                    <span class="card-date">{date}</span>
                </div>
                <div class="card-body">
                    <a href="{url}" class="card-title" target="_blank">{title}</a>
                    <div class="card-source">📰 {source}</div>
                    <div class="summary-container">
                        <div class="card-summary collapsed">{summary}</div>
                        <button class="toggle-btn" onclick="toggleSummary(this)">展开 <span class="arrow">▼</span></button>
                    </div>
                </div>
                <div class="card-footer">
                    <a href="{url}" class="read-more" target="_blank">阅读全文 →</a>
                    <div class="tag-list">
                        {tags}
                    </div>
                </div>
            </article>
'''

SECTION_TEMPLATE = '''    <section class="news-section">
        <div class="section-title">
            <h3>{icon} {section_name}</h3>
            <span class="badge">{count} 篇</span>
        </div>
        <div class="news-grid">
{news_cards}
        </div>
    </section>
'''


def generate_news_card(news_item, index):
    """生成单条新闻卡片 HTML"""
    title = news_item.get('title', '')
    summary = news_item.get('summary', '')
    region = news_item.get('region', '国内')
    
    category = '国内热点' if region == '国内' else '国际前沿'
    category_class = 'domestic' if region == '国内' else 'international'
    
    tags_html = ''
    tag = news_item.get('tag', '')
    if tag:
        tags_html = f'<span class="tag">{tag.split(" · ")[-1]}</span>'
    
    return NEWS_CARD_TEMPLATE.format(
        category=category,
        category_class=category_class,
        date=datetime.now().strftime('%Y-%m-%d'),
        url=news_item.get('url', '#'),
        title=title,
        source=news_item.get('source', '未知来源'),
        summary=summary,
        tags=tags_html
    )


def generate_website():
    """生成完整网站 HTML"""
    with open('daily_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    news_list = data.get('news', [])
    
    # 分离国内国际新闻
    domestic_news = [n for n in news_list if n.get('region') == '国内']
    international_news = [n for n in news_list if n.get('region') == '国际']
    
    # 生成新闻卡片
    domestic_cards = ''
    for i, news in enumerate(domestic_news[:10]):
        domestic_cards += generate_news_card(news, i)
    
    international_cards = ''
    for i, news in enumerate(international_news[:10]):
        international_cards += generate_news_card(news, i)
    
    # 生成板块
    domestic_section = SECTION_TEMPLATE.format(
        icon='🇨🇳',
        section_name='国内AI热点',
        count=len(domestic_news[:10]),
        news_cards=domestic_cards
    )
    
    international_section = SECTION_TEMPLATE.format(
        icon='🌍',
        section_name='国际AI前沿',
        count=len(international_news[:10]),
        news_cards=international_cards
    )
    
    news_sections = domestic_section + '\n' + international_section
    
    # 生成完整 HTML
    html = HTML_TEMPLATE.format(
        update_date=datetime.now().strftime('%Y-%m-%d'),
        news_sections=news_sections
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 网站已生成: index.html")
    print(f"📊 国内新闻: {len(domestic_news[:10])} 条")
    print(f"📊 国际新闻: {len(international_news[:10])} 条")
    print(f"🔧 已添加摘要折叠/展开功能")
    
    return len(domestic_news[:10]), len(international_news[:10])


if __name__ == '__main__':
    generate_website()
