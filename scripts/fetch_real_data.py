#!/usr/bin/env python3
"""
TechInsight Hub - 真实数据获取模块
支持多个免费数据源：Hacker News, arXiv, GitHub
"""

import requests
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

class DataFetcher:
    """数据获取器基类"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TechInsight-Hub/1.0 (Research Bot)'
        })
    
    def fetch(self):
        raise NotImplementedError

class HackerNewsFetcher(DataFetcher):
    """Hacker News AI热点获取"""
    
    AI_KEYWORDS = [
        'AI', 'artificial intelligence', 'machine learning', 'deep learning',
        'LLM', 'GPT', 'Claude', 'OpenAI', 'Anthropic', 'Google AI', 'Gemini',
        'neural network', 'transformer', 'DeepSeek', 'Mistral', 'Llama'
    ]
    
    def fetch(self, limit=5):
        """获取AI相关的HN热门故事"""
        try:
            print("📡 正在获取 Hacker News 数据...")
            
            # 获取top stories
            resp = self.session.get(
                'https://hacker-news.firebaseio.com/v0/topstories.json',
                timeout=10
            )
            story_ids = resp.json()[:50]  # 检查前50个
            
            stories = []
            for story_id in story_ids:
                if len(stories) >= limit:
                    break
                    
                try:
                    story_resp = self.session.get(
                        f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json',
                        timeout=5
                    )
                    story = story_resp.json()
                    
                    if not story or 'title' not in story:
                        continue
                    
                    title = story['title']
                    
                    # 检查AI关键词
                    if any(kw.lower() in title.lower() for kw in self.AI_KEYWORDS):
                        stories.append({
                            'title': title,
                            'url': story.get('url') or f"https://news.ycombinator.com/item?id={story_id}",
                            'source': 'Hacker News',
                            'score': story.get('score', 0),
                            'comments': story.get('descendants', 0),
                            'date': datetime.fromtimestamp(story.get('time', 0)).strftime('%b %d')
                        })
                        
                    time.sleep(0.1)  # 避免请求过快
                    
                except Exception as e:
                    continue
            
            print(f"✅ HN: 获取 {len(stories)} 条AI相关热点")
            return stories
            
        except Exception as e:
            print(f"❌ HN获取失败: {e}")
            return []

class ArxivFetcher(DataFetcher):
    """arXiv最新论文获取"""
    
    CATEGORIES = ['cs.AI', 'cs.LG', 'cs.CL', 'cs.CV', 'cs.RO']
    
    def fetch(self, limit_per_cat=3):
        """获取最新AI论文"""
        try:
            print("📡 正在获取 arXiv 论文...")
            
            all_papers = []
            
            for cat in self.CATEGORIES:
                try:
                    url = (
                        f'http://export.arxiv.org/api/query?'
                        f'search_query=cat:{cat}&'
                        f'sortBy=submittedDate&'
                        f'sortOrder=descending&'
                        f'max_results={limit_per_cat}'
                    )
                    
                    resp = self.session.get(url, timeout=15)
                    
                    # 解析Atom feed
                    entries = re.findall(r'<entry>(.*?)\u003c/entry>', resp.text, re.DOTALL)
                    
                    for entry in entries:
                        title_match = re.search(r'<title>(.*?)\u003c/title>', entry, re.DOTALL)
                        id_match = re.search(r'<id>.*?/(\d+\.\d+)\u003c/id>', entry)
                        published_match = re.search(r'<published>(.*?)\u003c/published>', entry)
                        
                        if title_match and id_match:
                            title = re.sub(r'\s+', ' ', title_match.group(1)).strip()
                            arxiv_id = id_match.group(1)
                            
                            # 清理标题
                            title = title.replace('\n', ' ')
                            
                            all_papers.append({
                                'title': title,
                                'arxiv_id': arxiv_id,
                                'url': f'https://arxiv.org/abs/{arxiv_id}',
                                'category': cat,
                                'date': datetime.now().strftime('%b %d')
                            })
                    
                    time.sleep(0.5)  # 尊重arXiv速率限制
                    
                except Exception as e:
                    print(f"   ⚠️ {cat} 获取失败: {e}")
                    continue
            
            print(f"✅ arXiv: 获取 {len(all_papers)} 篇论文")
            return all_papers[:10]  # 返回前10篇
            
        except Exception as e:
            print(f"❌ arXiv获取失败: {e}")
            return []

class GitHubFetcher(DataFetcher):
    """GitHub热门AI项目获取"""
    
    def fetch(self, limit=3):
        """获取GitHub Trending AI项目"""
        try:
            print("📡 正在获取 GitHub 数据...")
            
            # 搜索最近一周创建的AI项目，按star排序
            last_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            queries = [
                'machine learning stars:>100',
                'deep learning stars:>100',
                'LLM stars:>50',
                'AI tool stars:>50'
            ]
            
            all_repos = []
            
            for query in queries[:2]:  # 限制查询数量避免频率限制
                try:
                    url = (
                        f'https://api.github.com/search/repositories?'
                        f'q={requests.utils.quote(query)}+created:>{last_week}&'
                        f'sort=stars&order=desc&per_page=5'
                    )
                    
                    resp = self.session.get(url, timeout=10)
                    
                    if resp.status_code == 200:
                        data = resp.json()
                        for item in data.get('items', []):
                            all_repos.append({
                                'title': f"{item['full_name']}",
                                'description': item.get('description', 'No description') or 'No description',
                                'url': item['html_url'],
                                'stars': item['stargazers_count'],
                                'language': item.get('language', 'Unknown'),
                                'source': 'GitHub',
                                'date': datetime.now().strftime('%b %d')
                            })
                    
                    time.sleep(1)  # GitHub API频率限制
                    
                except Exception as e:
                    continue
            
            # 去重并按stars排序
            seen = set()
            unique_repos = []
            for repo in sorted(all_repos, key=lambda x: x['stars'], reverse=True):
                if repo['url'] not in seen:
                    seen.add(repo['url'])
                    unique_repos.append(repo)
            
            print(f"✅ GitHub: 获取 {len(unique_repos[:limit])} 个项目")
            return unique_repos[:limit]
            
        except Exception as e:
            print(f"❌ GitHub获取失败: {e}")
            return []

class ContentGenerator:
    """内容生成器"""
    
    @staticmethod
    def generate_news_card(story, index):
        """生成新闻卡片HTML"""
        tags = ['热点讨论', '开源项目', '研究突破', '产品发布', '产业动态', '技术趋势']
        tag = tags[index % len(tags)]
        
        return {
            'title': story['title'],
            'date': story.get('date', datetime.now().strftime('%b %d')),
            'tag': tag,
            'summary': story.get('description', f"来自{story.get('source', 'Unknown')}的最新动态"),
            'meta': [
                f"🔥 {story.get('source', 'News')}",
                f"⭐ {story.get('score', story.get('stars', 'N/A'))}"
            ],
            'url': story['url']
        }
    
    @staticmethod
    def generate_paper_card(paper):
        """生成论文卡片HTML"""
        return {
            'title': paper['title'],
            'arxiv_id': paper['arxiv_id'],
            'category': paper['category'],
            'url': paper['url'],
            'date': paper.get('date', datetime.now().strftime('%b %d'))
        }

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 TechInsight Hub 数据获取器")
    print("=" * 60)
    print()
    
    # 初始化获取器
    fetchers = {
        'hackernews': HackerNewsFetcher(),
        'arxiv': ArxivFetcher(),
        'github': GitHubFetcher()
    }
    
    all_data = {
        'news': [],
        'papers': [],
        'updated_at': datetime.now().isoformat()
    }
    
    # 获取数据
    print("🔄 开始获取最新数据...\n")
    
    # Hacker News
    hn_stories = fetchers['hackernews'].fetch(limit=3)
    for i, story in enumerate(hn_stories):
        all_data['news'].append(ContentGenerator.generate_news_card(story, i))
    
    # GitHub
    repos = fetchers['github'].fetch(limit=2)
    for i, repo in enumerate(repos):
        all_data['news'].append(ContentGenerator.generate_news_card(repo, i + 3))
    
    # arXiv
    papers = fetchers['arxiv'].fetch(limit_per_cat=2)
    all_data['papers'] = [ContentGenerator.generate_paper_card(p) for p in papers[:5]]
    
    # 保存数据
    output_file = Path('daily_content.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 60)
    print(f"✅ 数据获取完成!")
    print(f"   📰 新闻: {len(all_data['news'])} 条")
    print(f"   📄 论文: {len(all_data['papers'])} 篇")
    print(f"   💾 保存至: {output_file}")
    print("=" * 60)

if __name__ == '__main__':
    main()
