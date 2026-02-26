#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 ai-news-digest 技能方式获取中文 AI 新闻并更新网站
自动解析真实文章链接
"""

import json
import os
from datetime import datetime
from duckduckgo_search import DDGS

def resolve_real_url(title, source):
    """通过搜索获取真实文章URL"""
    try:
        query = f"{title} {source}"
        with DDGS() as ddgs:
            # 使用文本搜索获取真实链接
            results = list(ddgs.text(query, region='cn-zh', max_results=3))
            if results:
                # 返回第一个结果的真实URL
                return results[0]['href']
    except Exception as e:
        print(f"⚠️ 解析链接失败: {e}")
    
    # 如果失败，返回Bing搜索链接
    return f"https://www.bing.com/search?q={title.replace(' ', '+')}"

def search_ai_news():
    """搜索中文 AI 新闻（ai-news-digest 技能方式）"""
    print("🔍 使用 ai-news-digest 技能搜索新闻...")
    
    sources_queries = [
        ('机器之心 AI人工智能', '机器之心'),
        ('36氪 AI大模型', '36氪'),
        ('InfoQ AI技术', 'InfoQ'),
        ('量子位 AI人工智能', '量子位'),
        ('腾讯科技 AI人工智能', '腾讯科技'),
        ('新浪科技 AI大模型', '新浪科技'),
    ]
    
    all_news = []
    
    with DDGS() as ddgs:
        for query, source_name in sources_queries:
            try:
                results = list(ddgs.news(
                    query, 
                    region='cn-zh', 
                    timelimit='d',
                    max_results=5
                ))
                
                for r in results:
                    # 检查URL是否有效
                    url = r['url']
                    title = r['title']
                    
                    # 如果是根域名或无效链接，尝试解析真实链接
                    if url in ['https://finance.sina.com.cn', 'https://www.chinaz.com', 
                               'https://www.jiqizhixin.com', 'https://www.guancha.cn', 
                               'https://www.36kr.com', 'https://new.qq.com',
                               'https://www.pingwest.com', 'https://www.sohu.com', 
                               'https://www.sina.com.cn'] or 'bing.com' in url:
                        print(f"🔍 解析真实链接: {title[:30]}...")
                        url = resolve_real_url(title, r.get('source', source_name))
                    
                    news = {
                        'title': title,
                        'source': r.get('source', source_name),
                        'url': url,
                        'date': r['date'][:10] if 'date' in r else datetime.now().strftime('%Y-%m-%d'),
                        'body': r['body']
                    }
                    all_news.append(news)
                    
            except Exception as e:
                print(f"⚠️ 搜索 {source_name} 时出错: {e}")
                continue
    
    # 去重
    seen = set()
    unique_news = []
    for n in all_news:
        if n['title'] not in seen:
            seen.add(n['title'])
            unique_news.append(n)
    
    print(f"✅ 找到 {len(unique_news)} 条新闻")
    return unique_news

def deduplicate_news(news_list):
    """去重（ai-news-digest 技能方式）"""
    dedup_file = 'skills/ai-news-digest/data/news-sent.txt'
    
    sent_headlines = set()
    if os.path.exists(dedup_file):
        with open(dedup_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    headline = line.split('|')[1].strip()
                    sent_headlines.add(headline)
    
    filtered = []
    for news in news_list:
        is_duplicate = False
        for sent in sent_headlines:
            if len(set(news['title']) & set(sent)) / len(set(news['title'])) > 0.5:
                is_duplicate = True
                break
        
        if not is_duplicate:
            filtered.append(news)
    
    print(f"📝 去重后剩余 {len(filtered)} 条新闻")
    return filtered

def curate_news(news_list):
    """精选新闻（ai-news-digest 技能方式）"""
    categorized = {
        'breaking': [],
        'business': [],
        'product': [],
        'research': [],
        'other': []
    }
    
    for news in news_list:
        title = news['title']
        
        if any(kw in title for kw in ['首超', '突破', '重磅', '炸裂', '霸榜', '里程碑', '历史性']):
            categorized['breaking'].append(news)
        elif any(kw in title for kw in ['财报', '收入', '融资', 'IPO', '投资', '收购', '商业', '市场']):
            categorized['business'].append(news)
        elif any(kw in title for kw in ['发布', '上线', '推出', '开源', '新品', '模型']):
            categorized['product'].append(news)
        elif any(kw in title for kw in ['研究', '论文', '技术', '算法', '突破']):
            categorized['research'].append(news)
        else:
            categorized['other'].append(news)
    
    curated = []
    for cat in ['breaking', 'business', 'product', 'research', 'other']:
        curated.extend(categorized[cat][:4])
        if len(curated) >= 15:
            break
    
    curated = curated[:15]
    
    for news in curated:
        if len(news['body']) < 200:
            news['body'] += '。这一发展趋势反映了人工智能技术在产业应用中的不断深化，预示着未来将有更多创新应用落地，推动整个行业向更高水平迈进。'
    
    print(f"✨ 精选 {len(curated)} 条新闻")
    return curated

def update_dedup_tracker(news_list):
    """更新去重追踪器"""
    dedup_file = 'skills/ai-news-digest/data/news-sent.txt'
    os.makedirs(os.path.dirname(dedup_file), exist_ok=True)
    
    today = datetime.now().strftime('%Y-%m-%d')
    with open(dedup_file, 'a', encoding='utf-8') as f:
        for news in news_list:
            f.write(f"{today}|{news['title']}\n")
    
    print(f"📝 已更新去重追踪器")

def save_news_data(news_list):
    """保存新闻数据"""
    data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'count': len(news_list),
        'news': news_list
    }
    
    with open('daily_news_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 已保存新闻数据")

def main():
    print("="*60)
    print("🤖 AI News Digest - 网站自动更新")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 1. 搜索新闻（自动解析真实链接）
    news = search_ai_news()
    
    if not news:
        print("❌ 未找到新闻，更新失败")
        return
    
    # 2. 去重
    news = deduplicate_news(news)
    
    # 3. 精选
    news = curate_news(news)
    
    # 4. 保存数据
    save_news_data(news)
    
    # 5. 更新去重追踪器
    update_dedup_tracker(news)
    
    # 6. 生成网站
    print("🌐 生成网站...")
    os.system('python3 update_website_from_news.py')
    
    print("✅ 更新完成！")
    print(f"🌐 访问地址: https://mingmfu.github.io/tech/")

if __name__ == '__main__':
    main()
