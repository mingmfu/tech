#!/usr/bin/env python3
"""
更新网站四个技术领域的论文内容
"""

import json
import re
from pathlib import Path

def load_papers():
    with open('api/papers.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_paper_card(paper, is_featured=False):
    """生成论文卡片HTML"""
    if is_featured:
        return f'''                <!-- Featured -->
                <article class="card featured-card ai">
                    <div class="featured-content">
                        <span class="card-tag ai">FEATURED · {paper['category']}</span>
                        <h2>{paper['title']}</h2>
                        <p>{paper['summary']}</p>
                        <div class="featured-tags">
                            <span class="featured-tag">Paper</span>
                            <span class="featured-tag">{paper['source']}</span>
                            <span class="featured-tag">Research</span>
                        </div>
                        <a href="{paper['url']}" class="card-link ai" target="_blank">阅读论文 →</a>
                    </div>
                    <div class="featured-visual">
                        <div class="code-preview">
                            <div><span class="comment">// {paper['date']} Research Paper</span></div>
                            <div><span class="keyword">source</span>: <span class="string">"{paper['source']}"</span></div>
                            <div><span class="keyword">views</span>: <span class="string">{paper['views']}</span></div>
                            <div><span class="keyword">category</span>: <span class="string">"{paper['category']}"</span></div>
                        </div>
                    </div>
                </article>'''
    else:
        return f'''                <article class="card ai">
                    <div class="card-header">
                        <span class="card-tag ai">{paper['category']}</span>
                        <span class="card-date">{paper['date']}</span>
                    </div>
                    <h3>{paper['title']}</h3>
                    <p>{paper['summary']}</p>
                    <div class="card-meta">
                        <span>📄 {paper['source']}</span>
                        <span>👁️ {paper['views']:,}</span>
                    </div>
                    <a href="{paper['url']}" class="card-link ai" target="_blank">查看详情 →</a>
                </article>'''

def generate_section_cards(papers):
    """生成一个领域的所有卡片"""
    cards = []
    for i, paper in enumerate(papers):
        cards.append(generate_paper_card(paper, is_featured=(i==0)))
    return '\n'.join(cards)

def update_section(html, section_id, papers):
    """更新特定section的内容"""
    # 找到cards-grid的位置
    pattern = rf'(<section id="{section_id}".*?<div class="cards-grid">)(.*?)(</div>\s*<div class="timeline")'
    
    new_cards = generate_section_cards(papers)
    
    replacement = rf'\1\n{new_cards}\n            \3'
    
    return re.sub(pattern, replacement, html, flags=re.DOTALL)

def main():
    papers_data = load_papers()
    
    # 读取当前HTML
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 更新四个领域
    category_map = {
        'ai': 'ai',
        'graphics': 'gfx', 
        'os': 'os',
        'pl': 'pl'
    }
    
    for cat in papers_data['categories']:
        section_id = category_map[cat['id']]
        papers = cat['articles']
        print(f"更新 {cat['icon']} {cat['name']} 部分...")
        html = update_section(html, section_id, papers)
    
    # 保存
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ 四个技术领域的论文已更新！")

if __name__ == "__main__":
    main()
