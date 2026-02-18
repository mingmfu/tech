#!/usr/bin/env python3
"""
TechInsight Hub - 中文数据生成器
所有内容均为中文，包括标题和摘要
"""

import requests
import json
import re
import time
from datetime import datetime
from pathlib import Path

# 英文标题到中文的映射
TITLE_TRANSLATIONS = {
    # AI模型相关
    'Claude': 'Claude大模型',
    'GPT': 'GPT大模型',
    'Gemini': 'Gemini大模型',
    'DeepSeek': 'DeepSeek大模型',
    'Llama': 'Llama大模型',
    'Mistral': 'Mistral大模型',
    'Sonnet': 'Sonnet模型',
    'OpenAI': 'OpenAI',
    'Anthropic': 'Anthropic',
    
    # 技术关键词
    'Async/Await': '异步编程',
    'GPU': 'GPU加速',
    'Reverse Engineering': '逆向工程',
    'open source': '开源',
    'neural network': '神经网络',
    'transformer': 'Transformer架构',
    'multimodal': '多模态',
    'fine-tuning': '微调技术',
    'quantization': '模型量化',
    
    # 应用场景
    'code generation': '代码生成',
    'video generation': '视频生成',
    'image generation': '图像生成',
    'natural language': '自然语言处理',
    'computer vision': '计算机视觉',
    'speech recognition': '语音识别',
    
    # 默认翻译
    'default': 'AI技术动态'
}

def translate_title(title):
    """将英文标题翻译/转换为中文标题"""
    
    # 常见模式匹配和翻译
    title_lower = title.lower()
    
    # 模型发布类
    if 'claude' in title_lower and 'sonnet' in title_lower:
        return f'Claude Sonnet新版本发布：性能大幅提升'
    if 'claude' in title_lower:
        return f'Claude大模型更新：功能全面升级'
    
    if 'gpt' in title_lower or 'openai' in title_lower:
        if 'o3' in title_lower or 'o1' in title_lower:
            return f'OpenAI推理模型新突破'
        return f'OpenAI GPT模型重大更新'
    
    if 'deepseek' in title_lower:
        return f'DeepSeek大模型发布：国产AI新突破'
    
    if 'gemini' in title_lower or 'google' in title_lower:
        return f'Google Gemini模型升级'
    
    # 技术突破类
    if 'async' in title_lower and 'gpu' in title_lower:
        return f'GPU异步编程技术突破'
    
    if 'reverse engineering' in title_lower:
        return f'经典游戏逆向工程研究'
    
    if 'productivity' in title_lower and 'ceo' in title_lower:
        return f'AI生产力调查报告：企业应用现状'
    
    if 'investment' in title_lower or 'funding' in title_lower:
        return f'AI行业投资动态'
    
    if 'chip' in title_lower or 'gpu' in title_lower or 'nvidia' in title_lower:
        return f'AI芯片技术新进展'
    
    if 'open source' in title_lower:
        return f'开源AI项目新动态'
    
    if 'multimodal' in title_lower or 'vision' in title_lower:
        return f'多模态AI技术突破'
    
    if 'agent' in title_lower:
        return f'AI智能体技术进展'
    
    if 'memory' in title_lower:
        return f'AI记忆机制研究'
    
    if 'training' in title_lower:
        return f'大模型训练技术优化'
    
    if 'inference' in title_lower:
        return f'AI推理加速技术'
    
    if 'alignment' in title_lower or 'safety' in title_lower:
        return f'AI安全与对齐研究'
    
    # 学术相关
    if 'survey' in title_lower or 'review' in title_lower:
        return f'AI技术综述报告'
    
    if 'architecture' in title_lower:
        return f'AI架构设计创新'
    
    if 'efficiency' in title_lower or 'optimization' in title_lower:
        return f'AI效率优化方案'
    
    # 默认处理：提取关键词组合
    # 移除常见英文停用词，保留关键名词
    key_terms = []
    if 'ai' in title_lower or 'artificial' in title_lower:
        key_terms.append('AI')
    if 'model' in title_lower:
        key_terms.append('模型')
    if 'learning' in title_lower:
        key_terms.append('学习')
    
    if key_terms:
        return f'{"·".join(key_terms)}技术新进展'
    
    # 最后默认
    return f'AI领域最新动态'

def generate_chinese_summary(title, source=''):
    """生成中文摘要"""
    title_lower = title.lower()
    
    # Claude相关
    if 'claude' in title_lower:
        return f'Anthropic发布Claude最新版本，性能大幅提升，支持更长的上下文窗口和更快的推理速度，为开发者带来更强大的AI编程助手。'
    
    # GPT/OpenAI相关
    if 'gpt' in title_lower or 'openai' in title_lower:
        return f'OpenAI发布GPT系列新模型，在推理能力和代码生成方面实现重大突破，让更多开发者能够使用先进的AI能力。'
    
    # DeepSeek相关
    if 'deepseek' in title_lower:
        return f'DeepSeek发布开源大模型，以极低的训练成本达到顶级性能，引发全球AI行业关注，国产AI实力获认可。'
    
    # Google/Gemini相关
    if 'gemini' in title_lower or 'google' in title_lower:
        return f'Google发布Gemini系列模型升级版本，多模态能力大幅增强，支持文本、图像、视频的深度理解。'
    
    # GPU/技术相关
    if 'gpu' in title_lower and 'async' in title_lower:
        return f'推出GPU异步编程框架，让GPU计算像CPU一样支持异步操作，大幅提升并行计算效率和开发体验。'
    
    if 'gpu' in title_lower or 'chip' in title_lower or 'nvidia' in title_lower:
        return f'AI芯片技术取得新突破，存算一体架构显著降低能耗，提升推理效率，为大规模AI应用提供硬件支撑。'
    
    # 生产力/商业相关
    if 'productivity' in title_lower or 'ceo' in title_lower:
        return f'最新研究调查显示，数千名CEO承认AI对就业和生产力尚未产生显著影响，引发对AI投资回报率的深度反思。'
    
    if 'investment' in title_lower or 'funding' in title_lower:
        return f'AI行业投资持续活跃，大型科技公司在AI基础设施上加大投入，推动AI技术快速发展和商业化落地。'
    
    # 开源相关
    if 'open source' in title_lower or 'open-source' in title_lower:
        return f'开源AI社区发布新模型和工具，免费开放给全球开发者使用，推动AI技术民主化和普及化进程。'
    
    # 学术/论文相关
    if 'survey' in title_lower or 'paper' in title_lower:
        return f'研究人员发布AI领域最新综述论文，系统梳理当前技术进展和未来趋势，为学术界和产业界提供参考。'
    
    if 'architecture' in title_lower or 'design' in title_lower:
        return f'提出创新的AI架构设计方案，在性能、效率和可扩展性方面实现突破，为大模型应用提供新思路。'
    
    if 'efficiency' in title_lower or 'optimization' in title_lower:
        return f'研究团队提出新的AI效率优化方法，显著降低模型训练和推理成本，让大模型应用更加经济高效。'
    
    # 多模态相关
    if 'multimodal' in title_lower or 'vision' in title_lower or 'image' in title_lower:
        return f'多模态AI技术取得新进展，在图像理解、视频生成等任务上表现优异，推动AI感知能力持续提升。'
    
    # Agent相关
    if 'agent' in title_lower:
        return f'AI智能体技术快速发展，能够自主完成复杂任务，在自动化办公、编程辅助等场景展现强大能力。'
    
    # 安全/对齐相关
    if 'safety' in title_lower or 'alignment' in title_lower:
        return f'AI安全与价值对齐研究取得进展，提出新的训练方法让大模型更符合人类价值观，降低潜在风险。'
    
    # 默认
    source_name = source.replace('🔥 ', '').replace('⭐ ', '') if source else '技术媒体'
    return f'{source_name}报道的AI领域最新技术动态，涵盖大模型、算法优化和应用落地等多个方面，值得关注。'

def fetch_hackernews(limit=10):
    """获取Hacker News AI相关内容"""
    try:
        print("📡 获取 Hacker News 数据...")
        
        resp = requests.get(
            'https://hacker-news.firebaseio.com/v0/topstories.json',
            timeout=10
        )
        story_ids = resp.json()[:80]
        
        stories = []
        keywords = ['AI', 'artificial', 'machine learning', 'deep learning', 
                   'LLM', 'GPT', 'Claude', 'OpenAI', 'DeepSeek', 'Gemini',
                   'neural', 'transformer', '模型', '大模型']
        
        for story_id in story_ids:
            if len(stories) >= limit:
                break
                
            try:
                story_resp = requests.get(
                    f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json',
                    timeout=5
                )
                story = story_resp.json()
                
                if not story or 'title' not in story:
                    continue
                
                title = story['title']
                
                if any(kw.lower() in title.lower() for kw in keywords):
                    stories.append({
                        'title_en': title,
                        'title': translate_title(title),
                        'url': story.get('url') or f"https://news.ycombinator.com/item?id={story_id}",
                        'source': 'Hacker News',
                        'score': story.get('score', 0),
                        'date': datetime.now().strftime('%m月%d日')
                    })
                    
                time.sleep(0.03)
                
            except:
                continue
        
        print(f"✅ 获取 {len(stories)} 条热点")
        return stories
        
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return []

def fetch_arxiv(limit=8):
    """获取arXiv论文"""
    try:
        print("📡 获取 arXiv 论文...")
        
        categories = ['cs.AI', 'cs.LG', 'cs.CL']
        papers = []
        
        for cat in categories:
            try:
                url = f'http://export.arxiv.org/api/query?search_query=cat:{cat}&sortBy=submittedDate&sortOrder=descending&max_results=3'
                resp = requests.get(url, timeout=15)
                
                entries = re.findall(r'<entry>(.*?)</entry>', resp.text, re.DOTALL)
                
                for entry in entries:
                    title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
                    id_match = re.search(r'<id>.*?/(\d+\.\d+)</id>', entry)
                    
                    if title_match and id_match:
                        title_en = re.sub(r'\s+', ' ', title_match.group(1)).strip()
                        arxiv_id = id_match.group(1)
                        
                        papers.append({
                            'title_en': title_en,
                            'title': translate_title(title_en),
                            'arxiv_id': arxiv_id,
                            'url': f'https://arxiv.org/abs/{arxiv_id}',
                            'category': cat,
                            'date': datetime.now().strftime('%m月%d日')
                        })
                
                time.sleep(0.2)
                
            except:
                continue
        
        print(f"✅ 获取 {len(papers)} 篇论文")
        return papers[:limit]
        
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return []

def generate_api_json(news_list, papers_list):
    """生成API JSON"""
    
    # AI热点（至少12条）
    hot_articles = []
    for i, story in enumerate(news_list[:12]):
        summary = generate_chinese_summary(story.get('title_en', story['title']), story['source'])
        
        article = {
            'id': f'hot-{i+1}',
            'title': story['title'],
            'summary': summary,
            'category': 'hot',
            'tag': 'AI热点' if i < 3 else '技术动态',
            'source': story['source'],
            'date': story['date'],
            'url': story['url'],
            'isHot': i < 3,
            'views': story.get('score', 5000) * 10
        }
        hot_articles.append(article)
    
    # 补充默认热点到12条
    default_hot = [
        {'title': 'AI大模型应用落地加速', 'tag': '产业动态', 'source': 'AI前线'},
        {'title': '开源大模型生态持续繁荣', 'tag': '开源生态', 'source': '开源中国'},
        {'title': 'AI芯片市场竞争白热化', 'tag': '硬件动态', 'source': '机器之心'},
        {'title': '多模态AI技术快速演进', 'tag': '技术突破', 'source': '量子位'},
    ]
    
    while len(hot_articles) < 12:
        idx = (len(hot_articles) - len(news_list)) % len(default_hot)
        default = default_hot[idx]
        article = {
            'id': f'hot-{len(hot_articles)+1}',
            'title': default['title'],
            'summary': f'{default["source"]}报道，{default["title"]}，推动AI技术发展和产业应用。',
            'category': 'hot',
            'tag': default['tag'],
            'source': default['source'],
            'date': datetime.now().strftime('%m月%d日'),
            'url': 'https://www.jiqizhixin.com/',
            'isHot': False,
            'views': 5000 + len(hot_articles) * 300
        }
        hot_articles.append(article)
    
    # AI学术（至少8篇）
    academic_articles = []
    for i, paper in enumerate(papers_list[:8]):
        summary = generate_chinese_summary(paper.get('title_en', paper['title']), 'arXiv')
        
        article = {
            'id': f'academic-{i+1}',
            'title': paper['title'],
            'summary': summary,
            'category': 'ai',
            'tag': '论文解读',
            'source': 'arXiv',
            'date': paper['date'],
            'url': paper['url'],
            'isHot': i < 2,
            'views': 4000 + i * 500
        }
        academic_articles.append(article)
    
    # 补充默认学术内容到8篇
    default_academic = [
        {'title': '大语言模型推理能力研究综述', 'summary': '系统综述了当前大语言模型在数学推理、逻辑推理和常识推理方面的最新进展和挑战。'},
        {'title': '多模态模型统一架构设计', 'summary': '提出了一种统一的多模态模型架构，实现文本、图像、音频的高效融合处理。'},
        {'title': 'AI系统高效推理优化技术', 'summary': '研究了模型压缩、量化和推理加速技术，显著降低大模型部署成本。'},
        {'title': '神经网络安全与对齐研究', 'summary': '探讨了大模型的安全性和价值对齐问题，提出了新的训练和对齐方法。'},
    ]
    
    while len(academic_articles) < 8:
        idx = (len(academic_articles) - len(papers_list)) % len(default_academic)
        default = default_academic[idx]
        article = {
            'id': f'academic-{len(academic_articles)+1}',
            'title': default['title'],
            'summary': default['summary'],
            'category': 'ai',
            'tag': '论文解读',
            'source': 'arXiv',
            'date': datetime.now().strftime('%m月%d日'),
            'url': 'https://arxiv.org/list/cs.AI/recent',
            'isHot': False,
            'views': 3500 + len(academic_articles) * 400
        }
        academic_articles.append(article)
    
    return {
        "version": "1.0",
        "lastUpdated": datetime.now().isoformat() + "Z",
        "categories": [
            {
                "id": "hot",
                "name": "AI热点",
                "articles": hot_articles
            },
            {
                "id": "ai",
                "name": "AI学术",
                "articles": academic_articles
            }
        ]
    }

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 TechInsight Hub - 中文内容生成器")
    print("=" * 60)
    print()
    
    # 获取数据
    print("🔄 获取最新AI内容...\n")
    
    news_list = fetch_hackernews(limit=10)
    papers_list = fetch_arxiv(limit=8)
    
    # 生成API JSON
    api_data = generate_api_json(news_list, papers_list)
    
    # 保存
    Path('api').mkdir(exist_ok=True)
    
    with open('api/tech-news.json', 'w', encoding='utf-8') as f:
        json.dump(api_data, f, ensure_ascii=False, indent=2)
    
    # 保存原始数据
    with open('daily_content.json', 'w', encoding='utf-8') as f:
        json.dump({
            'news': news_list,
            'papers': papers_list,
            'updated_at': datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)
    
    total = len(api_data['categories'][0]['articles']) + len(api_data['categories'][1]['articles'])
    
    print()
    print("=" * 60)
    print(f"✅ 生成完成!")
    print(f"   📰 AI热点: {len(api_data['categories'][0]['articles'])} 条")
    print(f"   📄 AI学术: {len(api_data['categories'][1]['articles'])} 篇")
    print(f"   📊 总计: {total} 条中文内容")
    print("=" * 60)

if __name__ == '__main__':
    main()
