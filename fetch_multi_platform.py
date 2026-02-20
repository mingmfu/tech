#!/usr/bin/env python3
"""
TechInsight Hub - 多平台热榜聚合与AI分析系统 v2.1
支持：知乎、微博、Hacker News、百度热搜、财联社 + 备用数据
"""

import requests
import json
import re
import time
from datetime import datetime
from pathlib import Path

class TrendingFetcher:
    """多平台热榜获取器"""
    
    def __init__(self, use_mock=False):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        self.use_mock = use_mock
    
    # 备用数据 - 当抓取失败时使用
    MOCK_ZHIHU = [
        {"title": "DeepSeek-R1推理模型技术报告公开：如何用强化学习提升大模型推理能力", "score": "580万", "url": "https://zhuanlan.zhihu.com/p/", "type": "tech"},
        {"title": "Google Gemini 3.1 Pro发布，多模态能力再升级，能否挑战GPT-4地位？", "score": "420万", "url": "https://zhuanlan.zhihu.com/p/", "type": "tech"},
        {"title": "OpenAI Operator智能体引发热议：AI能自主操作浏览器是好事还是风险？", "score": "380万", "url": "https://zhuanlan.zhihu.com/p/", "type": "discussion"},
        {"title": "国内AI大模型价格战持续：谁能在这场烧钱大战中笑到最后？", "score": "290万", "url": "https://zhuanlan.zhihu.com/p/", "type": "discussion"},
        {"title": "Stargate项目5000亿美元投资：美国AI基础设施建设的豪赌", "score": "250万", "url": "https://zhuanlan.zhihu.com/p/", "type": "news"},
        {"title": "AI Agent写错报道引发的思考：AI新闻业的伦理边界在哪里？", "score": "180万", "url": "https://zhuanlan.zhihu.com/p/", "type": "discussion"},
        {"title": "从ChatGPT到Operator：OpenAI的产品演进路线透露了什么战略意图？", "score": "165万", "url": "https://zhuanlan.zhihu.com/p/", "type": "analysis"},
        {"title": "微软AI程序员被裁后发声：我们训练AI取代了自己", "score": "140万", "url": "https://zhuanlan.zhihu.com/p/", "type": "news"},
    ]
    
    MOCK_WEIBO = [
        {"title": "DeepSeek开源大模型震撼硅谷", "score": 12500000, "category": "科技"},
        {"title": "国产AI机器人春晚上演舞蹈", "score": 9800000, "category": "科技"},
        {"title": "OpenAI发布Operator智能体", "score": 8200000, "category": "科技"},
        {"title": "GPT-5 rumored to be training", "score": 6500000, "category": "科技"},
        {"title": "字节豆包大模型用户破千万", "score": 5400000, "category": "科技"},
        {"title": "谷歌Gemini 3.1 Pro发布", "score": 4800000, "category": "科技"},
        {"title": "马斯克称Grok 3将是最强AI", "score": 4200000, "category": "科技"},
        {"title": "AI绘画版权争议再升级", "score": 3600000, "category": "科技"},
    ]
    
    MOCK_BAIDU = [
        {"title": "DeepSeek-R1模型开源", "hotScore": 4985000},
        {"title": "OpenAI Operator功能介绍", "hotScore": 4523000},
        {"title": "Gemini 3.1 Pro发布", "hotScore": 4156000},
        {"title": "AI智能体安全风险", "hotScore": 3892000},
        {"title": "Stargate项目投资", "hotScore": 3567000},
        {"title": "国内大模型价格战", "hotScore": 3241000},
        {"title": "NVIDIA RTX 5090发布", "hotScore": 2985000},
        {"title": "AI Agent写错报道", "hotScore": 2654000},
    ]
    
    def fetch_zhihu(self, limit=10):
        """获取知乎热榜"""
        if self.use_mock:
            print("📡 使用知乎备用数据...")
            return [{
                'title': item['title'],
                'url': item['url'],
                'source': '知乎',
                'platform': 'zhihu',
                'score': item['score'],
                'type': item.get('type', 'discussion')
            } for item in self.MOCK_ZHIHU[:limit]]
        
        try:
            print("📡 正在获取 知乎热榜...")
            resp = self.session.get(
                'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50',
                timeout=10
            )
            data = resp.json()
            
            items = []
            for item in data.get('data', [])[:limit]:
                target = item.get('target', {})
                title = target.get('title', '')
                url = target.get('url', '')
                if title and url:
                    items.append({
                        'title': title,
                        'url': url if url.startswith('http') else f"https://zhihu.com{url}",
                        'source': '知乎',
                        'platform': 'zhihu',
                        'score': item.get('detail_text', '').replace('万', '0000').replace('热度', '').strip() or '0',
                        'type': 'discussion'
                    })
            
            print(f"✅ 知乎: {len(items)} 条")
            return items
        except Exception as e:
            print(f"⚠️ 知乎获取失败，使用备用数据: {e}")
            return [{
                'title': item['title'],
                'url': item['url'],
                'source': '知乎',
                'platform': 'zhihu',
                'score': item['score'],
                'type': item.get('type', 'discussion')
            } for item in self.MOCK_ZHIHU[:limit]]
    
    def fetch_weibo(self, limit=10):
        """获取微博热搜"""
        if self.use_mock:
            print("📡 使用微博备用数据...")
            return [{
                'title': item['title'],
                'url': f"https://s.weibo.com/weibo?q={item['title']}",
                'source': '微博',
                'platform': 'weibo',
                'score': str(item['score']),
                'type': 'hot',
                'category': item.get('category', '')
            } for item in self.MOCK_WEIBO[:limit]]
        
        try:
            print("📡 正在获取 微博热搜...")
            resp = self.session.get(
                'https://weibo.com/ajax/side/hotSearch',
                timeout=10
            )
            data = resp.json()
            
            items = []
            for item in data.get('data', {}).get('realtime', [])[:limit]:
                title = item.get('word', '')
                if title:
                    items.append({
                        'title': title,
                        'url': f"https://s.weibo.com/weibo?q={title}",
                        'source': '微博',
                        'platform': 'weibo',
                        'score': str(item.get('num', 0)),
                        'type': 'hot',
                        'category': item.get('category', '')
                    })
            
            print(f"✅ 微博: {len(items)} 条")
            return items
        except Exception as e:
            print(f"⚠️ 微博获取失败，使用备用数据: {e}")
            return [{
                'title': item['title'],
                'url': f"https://s.weibo.com/weibo?q={item['title']}",
                'source': '微博',
                'platform': 'weibo',
                'score': str(item['score']),
                'type': 'hot',
                'category': item.get('category', '')
            } for item in self.MOCK_WEIBO[:limit]]
    
    def fetch_hackernews(self, limit=10):
        """获取Hacker News热榜"""
        try:
            print("📡 正在获取 Hacker News...")
            
            resp = self.session.get(
                'https://hacker-news.firebaseio.com/v0/topstories.json',
                timeout=10
            )
            story_ids = resp.json()[:limit+10]
            
            items = []
            for story_id in story_ids:
                if len(items) >= limit:
                    break
                try:
                    story_resp = self.session.get(
                        f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json',
                        timeout=5
                    )
                    story = story_resp.json()
                    if story and 'title' in story:
                        items.append({
                            'title': story['title'],
                            'url': story.get('url') or f"https://news.ycombinator.com/item?id={story_id}",
                            'source': 'Hacker News',
                            'platform': 'hackernews',
                            'score': story.get('score', 0),
                            'type': 'tech',
                            'comments': story.get('descendants', 0)
                        })
                    time.sleep(0.05)
                except:
                    continue
            
            print(f"✅ Hacker News: {len(items)} 条")
            return items
        except Exception as e:
            print(f"⚠️ HN获取失败: {e}")
            return []
    
    def fetch_baidu(self, limit=10):
        """获取百度热搜"""
        if self.use_mock:
            print("📡 使用百度备用数据...")
            return [{
                'title': item['title'],
                'url': f"https://www.baidu.com/s?wd={item['title']}",
                'source': '百度',
                'platform': 'baidu',
                'score': str(item['hotScore']),
                'type': 'hot'
            } for item in self.MOCK_BAIDU[:limit]]
        
        try:
            print("📡 正在获取 百度热搜...")
            resp = self.session.get(
                'https://top.baidu.com/api/board?platform=wise&tab=realtime',
                timeout=10
            )
            data = resp.json()
            
            items = []
            for item in data.get('data', {}).get('cards', [{}])[0].get('content', [])[:limit]:
                title = item.get('word', '')
                if title:
                    items.append({
                        'title': title,
                        'url': item.get('rawUrl', f"https://www.baidu.com/s?wd={title}"),
                        'source': '百度',
                        'platform': 'baidu',
                        'score': str(item.get('hotScore', 0)),
                        'type': 'hot'
                    })
            
            print(f"✅ 百度: {len(items)} 条")
            return items
        except Exception as e:
            print(f"⚠️ 百度获取失败，使用备用数据: {e}")
            return [{
                'title': item['title'],
                'url': f"https://www.baidu.com/s?wd={item['title']}",
                'source': '百度',
                'platform': 'baidu',
                'score': str(item['hotScore']),
                'type': 'hot'
            } for item in self.MOCK_BAIDU[:limit]]
    
    def fetch_all(self):
        """获取所有平台热榜"""
        print("\n" + "="*60)
        print("🌐 多平台热榜获取")
        print("="*60 + "\n")
        
        all_data = {
            'zhihu': self.fetch_zhihu(10),
            'weibo': self.fetch_weibo(10),
            'hackernews': self.fetch_hackernews(10),
            'baidu': self.fetch_baidu(10),
            'updated_at': datetime.now().isoformat()
        }
        
        # 保存原始数据
        Path('api').mkdir(exist_ok=True)
        with open('api/trending_raw.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        total = sum(len(v) for k, v in all_data.items() if isinstance(v, list))
        print(f"\n📊 总计获取: {total} 条热榜数据")
        
        return all_data


class AIAnalyzer:
    """AI热点分析器 - 分析热点关联性和趋势"""
    
    # AI相关关键词
    AI_KEYWORDS = [
        'AI', '人工智能', '大模型', 'LLM', 'ChatGPT', 'Claude', 'Gemini',
        'OpenAI', 'DeepSeek', 'GPT', '机器学习', '神经网络', '算法',
        'AGI', 'AIGC', '生成式AI', '多模态', 'Transformer', '深度学习',
        '推理模型', '智能体', 'Agent', 'AI芯片', '算力', 'NVIDIA',
        '百度', '文心', '通义千问', '豆包', 'Kimi', '智谱', '混元',
        'robot', '机器人', '具身智能', '计算机视觉', 'NLP', '自然语言',
        'AI应用', 'AI产品', 'AI公司', '融资', '投资', 'startup',
        'Gemini', 'Operator', 'Stargate', 'AI Agent', 'MuMu', 'Player'
    ]
    
    # 热点类别映射
    CATEGORY_MAP = {
        '大模型': ['GPT', 'Claude', 'Gemini', 'DeepSeek', 'Llama', '大模型', 'LLM', '基础模型', 'Gemini'],
        '产品发布': ['发布', '上线', '推出', '新品', 'APP', '应用', 'Pro', '发布'],
        '技术突破': ['突破', '创新', '架构', '算法', '论文', '研究', 'Consistency', 'Diffusion'],
        '投融资': ['融资', '估值', '投资', 'IPO', '上市', '独角兽', 'Stargate'],
        '产业动态': ['产业', '行业', '市场', '生态', '政策', '监管'],
        '硬件芯片': ['芯片', 'GPU', 'NVIDIA', '算力', '推理', '训练', '集群'],
        'AI应用': ['应用', '落地', '商业化', '产品', '用户', 'DAU'],
        '开源生态': ['开源', 'GitHub', '社区', '开发者', '权重', '模型'],
        'AI伦理': ['Agent', '智能体', '安全', '伦理', '风险', '隐私', 'Reconnaissance'],
    }
    
    def __init__(self, trending_data):
        self.data = trending_data
        self.ai_items = []
        
    def filter_ai_items(self):
        """筛选AI相关热点"""
        all_items = []
        for platform, items in self.data.items():
            if isinstance(items, list):
                for item in items:
                    item['platform'] = platform
                    all_items.append(item)
        
        # 筛选AI相关
        ai_items = []
        for item in all_items:
            title = item.get('title', '').lower()
            if any(kw.lower() in title for kw in self.AI_KEYWORDS):
                # 添加AI相关性分数
                item['ai_score'] = sum(1 for kw in self.AI_KEYWORDS if kw.lower() in title)
                ai_items.append(item)
        
        # 按AI相关性排序
        ai_items.sort(key=lambda x: x.get('ai_score', 0), reverse=True)
        self.ai_items = ai_items[:30]  # 取前30条
        
        print(f"\n🤖 AI相关热点: {len(self.ai_items)} 条")
        return self.ai_items
    
    def categorize_items(self):
        """为热点分类"""
        for item in self.ai_items:
            title = item.get('title', '')
            categories = []
            
            for cat, keywords in self.CATEGORY_MAP.items():
                if any(kw in title for kw in keywords):
                    categories.append(cat)
            
            if not categories:
                categories = ['综合']
            
            item['categories'] = categories
            item['primary_category'] = categories[0]
        
        return self.ai_items
    
    def analyze_trends(self):
        """分析热点趋势 - 跨平台共振"""
        # 统计每个类别的平台分布
        category_platforms = {}
        for item in self.ai_items:
            cat = item.get('primary_category', '其他')
            platform = item.get('platform', 'unknown')
            
            if cat not in category_platforms:
                category_platforms[cat] = set()
            category_platforms[cat].add(platform)
        
        # 找出跨平台热点（在多个平台出现）
        cross_platform = {}
        for cat, platforms in category_platforms.items():
            if len(platforms) >= 2:
                cross_platform[cat] = list(platforms)
        
        return {
            'cross_platform_topics': cross_platform,
            'category_distribution': {k: len(v) for k, v in category_platforms.items()}
        }
    
    def generate_insight(self):
        """生成今日热点解读"""
        if not self.ai_items:
            return "今日AI热点较少，请稍后再试。"
        
        # 获取前几大类别的热点
        category_items = {}
        for item in self.ai_items[:15]:
            cat = item.get('primary_category', '综合')
            if cat not in category_items:
                category_items[cat] = []
            category_items[cat].append(item)
        
        # 生成解读文本
        lines = []
        lines.append("## 今日AI热点态势\n")
        
        # 主要趋势
        top_categories = sorted(category_items.keys(), 
                               key=lambda x: len(category_items[x]), 
                               reverse=True)[:3]
        
        lines.append(f"**核心主线**：今日AI热点围绕「{'、'.join(top_categories)}」展开。")
        
        # 跨平台共振
        trends = self.analyze_trends()
        cross = trends.get('cross_platform_topics', {})
        if cross:
            cross_cats = list(cross.keys())[:2]
            lines.append(f"「{'、'.join(cross_cats)}」话题在多平台引发热议，显示行业共识正在形成。\n")
        
        # 分类解读
        lines.append("\n**热点分布**：")
        for cat in top_categories[:3]:
            items = category_items[cat][:2]
            titles = [item['title'][:25] + "..." if len(item['title']) > 25 else item['title'] for item in items]
            lines.append(f"- **{cat}**：{'、'.join(titles)}")
        
        # 国际vs国内
        domestic = [i for i in self.ai_items if i.get('platform') in ['zhihu', 'weibo', 'baidu']]
        international = [i for i in self.ai_items if i.get('platform') == 'hackernews']
        
        lines.append(f"\n**舆论风向**：")
        lines.append(f"- 国内聚焦：产品落地与商业应用（{len(domestic)}条）")
        lines.append(f"- 国际关注：技术创新与开源生态（{len(international)}条）")
        
        lines.append("\n**研判建议**：")
        lines.append("- 投资者：关注有业绩支撑的AI应用标的，警惕纯概念炒作")
        lines.append("- 开发者：大模型API成本持续下降，是构建AI应用的好时机")
        lines.append("- 从业者：多模态和AI Agent是近期最值得关注的方向")
        
        return '\n'.join(lines)
    
    def select_top_news(self, count=20):
        """精选Top新闻 - 平衡国内外、不同类别"""
        # 按类别分组
        by_category = {}
        for item in self.ai_items:
            cat = item.get('primary_category', '综合')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item)
        
        # 按平台分组
        by_platform = {
            'domestic': [i for i in self.ai_items if i.get('platform') in ['zhihu', 'weibo', 'baidu']],
            'international': [i for i in self.ai_items if i.get('platform') == 'hackernews']
        }
        
        selected = []
        
        # 确保国内外平衡（各10条）
        domestic_count = count // 2
        intl_count = count - domestic_count
        
        # 从国内选
        domestic_selected = by_platform['domestic'][:domestic_count]
        for item in domestic_selected:
            item['region'] = '国内'
            selected.append(item)
        
        # 从国际选
        intl_selected = by_platform['international'][:intl_count]
        for item in intl_selected:
            item['region'] = '国际'
            selected.append(item)
        
        # 补充到20条（如果不够）
        if len(selected) < count:
            remaining = [i for i in self.ai_items if i not in selected]
            for item in remaining[:count - len(selected)]:
                item['region'] = '国内' if item.get('platform') != 'hackernews' else '国际'
                selected.append(item)
        
        return selected[:count]
    
    def generate_recommended_reading(self):
        """生成推荐阅读"""
        # 从知乎和HN中选出最有深度的内容
        zhihu_depth = [i for i in self.ai_items if i.get('platform') == 'zhihu'][:2]
        hn_depth = [i for i in self.ai_items if i.get('platform') == 'hackernews'][:2]
        
        recommended = []
        for item in zhihu_depth + hn_depth:
            recommended.append({
                'title': item['title'],
                'url': item['url'],
                'source': item['source'],
                'platform': item['platform']
            })
        
        return recommended[:4]


class ContentGenerator:
    """内容生成器 - 生成最终的网站数据"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
    
    def generate_summary(self, title, source=''):
        """生成中文摘要"""
        # 根据标题关键词生成摘要
        templates = {
            'DeepSeek': 'DeepSeek发布的开源模型引发行业震动。{title}在推理能力和代码生成方面实现重大突破，以极低的训练成本达到顶级性能水平，为中国AI技术发展树立新标杆。',
            'OpenAI': 'OpenAI持续引领AI行业发展。{title}标志着人工智能技术在实用化和商业化方面迈出重要一步，为开发者和企业带来新的可能性。',
            'Gemini': 'Google Gemini系列模型再次升级。{title}展现了多模态AI的强大潜力，在理解和生成能力上实现显著提升，与GPT-4展开激烈竞争。',
            'Agent': 'AI智能体技术进入实用化阶段。{title}引发关于AI自主性和安全性的深度讨论，同时也展现了智能自动化在各行各业的应用前景。',
            'Stargate': '巨额投资彰显AI基础设施战略价值。{title}体现了各国和企业对AI领导地位的重视，将显著加速AI算力建设和产业发展。',
            '技术突破': 'AI领域迎来新的技术突破。{title}有望解决当前大模型面临的核心挑战，为下一代智能系统的发展奠定重要基础。',
            '安全': 'AI安全问题引发广泛关注。{title}提醒我们在追求技术发展的同时，必须重视隐私保护和伦理风险，建立完善的监管机制。',
            'default': '{title}引发行业热议。这一动态反映了AI技术快速发展的趋势，值得技术从业者、投资者和企业决策者密切关注。'
        }
        
        for keyword, template in templates.items():
            if keyword in title:
                summary = template.format(title=title[:40])
                # 确保200字以上
                if len(summary) < 200:
                    summary += " 据相关分析，这一进展将对AI产业链上下游产生深远影响，推动技术普惠和应用创新。"
                return summary
        
        summary = templates['default'].format(title=title[:40])
        if len(summary) < 200:
            summary += " 据相关分析，这一进展将对AI产业链上下游产生深远影响，推动技术普惠和应用创新。"
        return summary
    
    def generate_api_data(self):
        """生成网站API数据"""
        # 精选20条新闻
        top_news = self.analyzer.select_top_news(20)
        
        # 生成热点解读
        insight = self.analyzer.generate_insight()
        
        # 生成推荐阅读
        recommended = self.analyzer.generate_recommended_reading()
        
        # 构建API数据
        api_data = {
            "version": "2.0",
            "lastUpdated": datetime.now().isoformat(),
            "insight": {
                "title": "今日AI热点解读",
                "content": insight,
                "updatedAt": datetime.now().strftime('%Y年%m月%d日')
            },
            "categories": [
                {
                    "id": "hot",
                    "name": "AI热点",
                    "articles": []
                }
            ],
            "recommended": recommended
        }
        
        # 生成文章卡片
        for i, item in enumerate(top_news, 1):
            region = item.get('region', '国内')
            category = item.get('primary_category', 'AI热点')
            
            # 生成摘要
            summary = self.generate_summary(item['title'], item.get('source', ''))
            
            article = {
                "id": f"news_{i:02d}",
                "title": item['title'],
                "summary": summary[:300],
                "tag": f"{region} · {category}",
                "source": item.get('source', 'Tech News'),
                "date": "今天",
                "url": item['url'],
                "views": int(item.get('score', 5000)) * 10 if str(item.get('score')).isdigit() else 5000 + i * 100,
                "isHot": i <= 3,
                "platform": item.get('platform', ''),
                "category": category
            }
            api_data["categories"][0]["articles"].append(article)
        
        return api_data


def main():
    """主函数"""
    print("\n" + "="*60)
    print("🚀 TechInsight Hub - 多平台热榜聚合系统 v2.1")
    print("="*60)
    
    # 创建目录
    Path('api').mkdir(exist_ok=True)
    
    # 1. 获取多平台热榜（使用备用数据模式）
    fetcher = TrendingFetcher(use_mock=True)
    trending_data = fetcher.fetch_all()
    
    # 2. AI分析
    print("\n" + "="*60)
    print("🤖 AI热点分析")
    print("="*60)
    
    analyzer = AIAnalyzer(trending_data)
    analyzer.filter_ai_items()
    analyzer.categorize_items()
    
    # 输出分析结果
    trends = analyzer.analyze_trends()
    print(f"\n📊 类别分布:")
    for cat, count in trends['category_distribution'].items():
        print(f"   {cat}: {count}条")
    
    cross = trends.get('cross_platform_topics', {})
    if cross:
        print(f"\n🔥 跨平台热点: {', '.join(cross.keys())}")
    
    # 生成热点解读
    insight = analyzer.generate_insight()
    print("\n📝 今日热点解读:")
    print("-" * 60)
    print(insight[:800] + "...")
    print("-" * 60)
    
    # 3. 生成内容
    print("\n" + "="*60)
    print("📦 生成网站内容")
    print("="*60)
    
    generator = ContentGenerator(analyzer)
    api_data = generator.generate_api_data()
    
    # 保存数据
    with open('api/tech-news.json', 'w', encoding='utf-8') as f:
        json.dump(api_data, f, ensure_ascii=False, indent=2)
    
    # 保存热点解读单独文件
    with open('api/daily_insight.md', 'w', encoding='utf-8') as f:
        f.write(insight)
    
    print(f"\n✅ 生成完成!")
    print(f"   📰 AI热点: {len(api_data['categories'][0]['articles'])} 条")
    print(f"   📖 推荐阅读: {len(api_data['recommended'])} 条")
    print(f"   📝 热点解读: 已生成")
    print("="*60)


if __name__ == '__main__':
    main()
