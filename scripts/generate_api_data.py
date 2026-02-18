#!/usr/bin/env python3
"""
生成 tech-news.json API 数据文件
供手机端应用访问
"""

import json
import uuid
from datetime import datetime
from pathlib import Path

def generate_id(title):
    """从标题生成ID"""
    return title.lower().replace(' ', '-').replace(':', '').replace('(', '').replace(')', '')[:50]

def generate_tech_news():
    """生成 tech-news.json"""
    
    # 读取抓取的数据
    with open('daily_content.json', 'r', encoding='utf-8') as f:
        daily_data = json.load(f)
    
    # 构建API数据结构
    tech_news = {
        "version": "1.0",
        "lastUpdated": datetime.now().isoformat() + "Z",
        "categories": [
            {
                "id": "hot",
                "name": "AI热点",
                "articles": []
            },
            {
                "id": "ai",
                "name": "AI学术", 
                "articles": []
            }
        ]
    }
    
    # 处理热点新闻
    for i, news in enumerate(daily_data.get('news', [])[:6]):
        article = {
            "id": generate_id(news['title']),
            "title": news['title'],
            "summary": news.get('summary', news['title']),
            "category": "hot",
            "tag": news.get('tag', '热点'),
            "source": news.get('source', news.get('meta', ['Unknown'])[0].replace('🔥 ', '').replace('⭐ ', '')),
            "date": datetime.now().strftime('%Y-%m-%d'),
            "url": news['url'],
            "isHot": i < 3,  # 前3条标记为热门
            "views": news.get('score', 0) * 10 if 'score' in news else 5000
        }
        tech_news["categories"][0]["articles"].append(article)
    
    # 处理学术内容（如果没有论文，使用默认内容）
    default_academic = [
        {
            "title": "DeepSeek-R1: 推理模型的开源突破",
            "summary": "DeepSeek 发布的 R1 模型在数学推理和代码生成任务上媲美 OpenAI o1，以极低的训练成本实现了惊人的性能。",
            "tag": "LLM",
            "source": "arXiv",
            "url": "https://arxiv.org/abs/2501.12948",
            "isHot": True,
            "views": 25678
        },
        {
            "title": "Mixture of Experts (MoE) 架构新进展",
            "summary": "最新的研究表明，通过动态路由和专家选择策略的优化，MoE 模型可以在保持性能的同时将推理成本降低 40%。",
            "tag": "LLM · Efficiency",
            "source": "arXiv",
            "url": "https://arxiv.org/abs/2502.08934",
            "isHot": False,
            "views": 5432
        },
        {
            "title": "Sora 之后：视频生成模型的技术演进",
            "summary": "OpenAI Sora 展示了 Transformer 在视频生成中的潜力。最新研究聚焦于时空一致性、长视频生成和可控性。",
            "tag": "Vision · Multimodal",
            "source": "arXiv",
            "url": "https://arxiv.org/abs/2502.07652",
            "isHot": False,
            "views": 7654
        },
        {
            "title": "Agent 系统的记忆机制设计",
            "summary": "如何让 AI Agent 拥有长期记忆？最新的记忆架构结合了向量检索、知识图谱和参数记忆。",
            "tag": "Agents · RAG",
            "source": "arXiv",
            "url": "https://arxiv.org/abs/2502.06731",
            "isHot": False,
            "views": 4321
        },
        {
            "title": "AI 芯片的存算一体新架构",
            "summary": "存内计算 (Compute-in-Memory) 技术正在成熟，可将 Transformer 推理能耗降低 10 倍。",
            "tag": "MLOps · Hardware",
            "source": "ISSCC",
            "url": "https://arxiv.org/abs/2501.18485",
            "isHot": False,
            "views": 3456
        }
    ]
    
    papers = daily_data.get('papers', [])
    if papers:
        # 使用实际获取的论文
        for i, paper in enumerate(papers[:5]):
            article = {
                "id": generate_id(paper['title']),
                "title": paper['title'],
                "summary": f"{paper['category']} 最新论文研究",
                "category": "ai",
                "tag": paper.get('category', 'AI').replace('cs.', ''),
                "source": "arXiv",
                "date": paper.get('date', datetime.now().strftime('%Y-%m-%d')),
                "url": paper.get('url', f"https://arxiv.org/abs/{paper.get('arxiv_id', '')}"),
                "isHot": i < 1,
                "views": 5000 + i * 1000
            }
            tech_news["categories"][1]["articles"].append(article)
    else:
        # 使用默认学术内容
        for i, article_data in enumerate(default_academic):
            article = {
                "id": generate_id(article_data['title']),
                "title": article_data['title'],
                "summary": article_data['summary'],
                "category": "ai",
                "tag": article_data['tag'],
                "source": article_data['source'],
                "date": datetime.now().strftime('%Y-%m-%d'),
                "url": article_data['url'],
                "isHot": article_data['isHot'],
                "views": article_data['views']
            }
            tech_news["categories"][1]["articles"].append(article)
    
    # 保存到api文件夹
    api_dir = Path('api')
    api_dir.mkdir(exist_ok=True)
    
    output_file = api_dir / 'tech-news.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tech_news, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已生成 {output_file}")
    print(f"   - AI热点: {len(tech_news['categories'][0]['articles'])} 条")
    print(f"   - AI学术: {len(tech_news['categories'][1]['articles'])} 条")
    
    return tech_news

if __name__ == '__main__':
    generate_tech_news()
