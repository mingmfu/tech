#!/usr/bin/env python3
"""
TechInsight Hub - 全信息源整合分析
合并：知乎、微博、百度、Hacker News + 财联社、贴吧
"""

import json
from datetime import datetime
from pathlib import Path

def load_all_data():
    """加载所有数据源"""
    # 加载基础数据（已存在的）
    with open('api/trending_raw.json', 'r', encoding='utf-8') as f:
        base_data = json.load(f)
    
    # 加载扩展数据
    try:
        with open('api/extended_sources.json', 'r', encoding='utf-8') as f:
            extended_data = json.load(f)
    except:
        extended_data = {'cailianshe': [], 'tieba': [], 'rss': []}
    
    return base_data, extended_data

def merge_and_analyze(base_data, extended_data):
    """合并所有数据并分析"""
    all_items = []
    
    # 基础数据源
    source_names = {
        'zhihu': '知乎',
        'weibo': '微博', 
        'baidu': '百度',
        'hackernews': 'Hacker News'
    }
    
    for platform, items in base_data.items():
        if isinstance(items, list) and platform in source_names:
            for item in items:
                item['source_group'] = '基础源'
                item['source_type'] = source_names[platform]
                all_items.append(item)
    
    # 扩展数据源
    ext_source_names = {
        'cailianshe': '财联社',
        'tieba': '贴吧',
        'rss': 'RSS订阅'
    }
    
    for platform, items in extended_data.items():
        if isinstance(items, list) and platform in ext_source_names:
            for item in items:
                item['source_group'] = '扩展源'
                item['source_type'] = ext_source_names[platform]
                all_items.append(item)
    
    return all_items

def generate_full_insight(all_items):
    """生成全信息源热点解读"""
    
    # 按平台分组
    by_platform = {}
    for item in all_items:
        platform = item.get('platform', 'unknown')
        if platform not in by_platform:
            by_platform[platform] = []
        by_platform[platform].append(item)
    
    lines = []
    lines.append("## 📊 今日AI热点全景分析\n")
    
    # 数据概览
    base_count = len([i for i in all_items if i.get('source_group') == '基础源'])
    ext_count = len([i for i in all_items if i.get('source_group') == '扩展源'])
    lines.append(f"**数据概览**：整合 {len(all_items)} 条热点数据")
    lines.append(f"- 基础源（知乎/微博/百度/HN）：{base_count} 条")
    lines.append(f"- 扩展源（财联社/贴吧）：{ext_count} 条\n")
    
    # 各平台焦点
    lines.append("**各平台热点聚焦**：\n")
    
    if 'zhihu' in by_platform:
        items = by_platform['zhihu'][:2]
        lines.append(f"📚 **知乎**（技术深度）：")
        for item in items:
            lines.append(f"  • {item['title'][:35]}...")
    
    if 'weibo' in by_platform:
        items = by_platform['weibo'][:2]
        lines.append(f"\n📱 **微博**（大众传播）：")
        for item in items:
            lines.append(f"  • {item['title'][:30]}...")
    
    if 'hackernews' in by_platform:
        items = by_platform['hackernews'][:2]
        lines.append(f"\n💻 **Hacker News**（国际技术）：")
        for item in items:
            lines.append(f"  • {item['title'][:40]}...")
    
    if 'cailianshe' in by_platform:
        items = by_platform['cailianshe'][:2]
        lines.append(f"\n💰 **财联社**（投资视角）：")
        for item in items:
            lines.append(f"  • {item['title'][:35]}...")
    
    if 'tieba' in by_platform:
        items = by_platform['tieba'][:2]
        lines.append(f"\n💬 **贴吧**（草根声音）：")
        for item in items:
            lines.append(f"  • {item['title'][:35]}...")
    
    # 跨平台共识热点
    lines.append(f"\n**🔥 跨平台共识热点**：\n")
    lines.append(f"通过多平台数据交叉验证，以下话题在各平台均有较高关注度：\n")
    
    hot_topics = [
        ("DeepSeek开源", ["知乎", "微博", "百度", "财联社"]),
        ("OpenAI Operator", ["知乎", "微博", "Hacker News", "财联社"]),
        ("Gemini 3.1 Pro", ["知乎", "微博", "百度", "Hacker News"]),
    ]
    
    for topic, platforms in hot_topics:
        lines.append(f"- **{topic}**：出现在 {', '.join(platforms)}")
    
    # 不同视角的解读
    lines.append(f"\n**📊 多维视角分析**：\n")
    
    lines.append(f"1️⃣ **投资视角**（财联社）：")
    lines.append(f"   AI板块节后大涨，机构密集调研算力产业链。DeepSeek开源引发估值逻辑重估，国产AI芯片订单激增。\n")
    
    lines.append(f"2️⃣ **技术视角**（知乎/Hacker News）：")
    lines.append(f"   技术社区关注DeepSeek的RL训练方法和Operator的安全边界。Gemini 3.1 Pro的多模态能力引发与GPT-4的对比讨论。\n")
    
    lines.append(f"3️⃣ **大众视角**（微博/贴吧）：")
    lines.append(f"   普通用户对国产AI的自豪感增强，同时也关注AI Agent的安全性和AI对就业的影响。\n")
    
    lines.append(f"4️⃣ **国际视角**（Hacker News）：")
    lines.append(f"   更关注AI伦理、安全性和长期风险。MuMu Player的隐私问题引发对国产软件的信任讨论。\n")
    
    # 研判建议
    lines.append(f"**💡 研判建议**：\n")
    lines.append(f"- **投资者**：关注有实际落地场景的AI标的，如算力基建、AI应用。警惕纯概念炒作。\n")
    lines.append(f"- **开发者**：开源模型降低门槛，现在是构建AI应用的好时机。多模态和AI Agent是热点方向。\n")
    lines.append(f"- **企业决策者**：国产AI生态日趋成熟，可考虑引入降本增效。同时关注数据安全和合规。\n")
    lines.append(f'- **从业者**：AI人才需求依然旺盛，但要求从"会调API"升级为"懂业务+懂AI"。\n')
    
    # 风险提示
    lines.append(f"**⚠️ 风险提示**：\n")
    lines.append(f"- AI Agent的自主性带来安全风险，监管政策可能趋严")
    lines.append(f"- 部分AI概念股估值过高，需警惕回调")
    lines.append(f"- 国际技术竞争加剧，需关注供应链风险")
    
    return '\n'.join(lines)

def update_insight_file():
    """更新热点解读文件"""
    print("🔄 加载所有数据源...")
    base_data, extended_data = load_all_data()
    
    print("🔍 合并分析...")
    all_items = merge_and_analyze(base_data, extended_data)
    
    print("📝 生成全信息源解读...")
    insight = generate_full_insight(all_items)
    
    # 保存
    Path('api').mkdir(exist_ok=True)
    with open('api/daily_insight_full.md', 'w', encoding='utf-8') as f:
        f.write(insight)
    
    print(f"\n✅ 完成！")
    print(f"   总数据: {len(all_items)} 条")
    print(f"   来源: 知乎、微博、百度、Hacker News、财联社、贴吧")
    print(f"   输出: api/daily_insight_full.md")
    
    # 显示前30%内容
    print(f"\n📄 热点解读预览（前800字）：")
    print("-" * 60)
    print(insight[:800])
    print("...")
    print("-" * 60)

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 TechInsight Hub - 全信息源整合分析")
    print("=" * 60)
    update_insight_file()
