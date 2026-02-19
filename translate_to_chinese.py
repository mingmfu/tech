#!/usr/bin/env python3
"""
快速将英文标题翻译为中文
"""

import json
from pathlib import Path

# 简单的翻译映射
TRANSLATIONS = {
    "Anthropic officially bans using subscription auth for third party use": "Anthropic官方禁止将订阅授权用于第三方",
    "Tailscale Peer Relays is now generally available": "Tailscale对等中继功能正式发布",
    "How AI is affecting productivity and jobs in Europe": "AI如何影响欧洲的生产力和就业",
    "A Lisp where each function call runs a Docker container": "每个函数调用都运行Docker容器的Lisp方言",
    "Rebrain.gg – Doom learn, don't doom scroll": "Rebrain.gg – 沉浸式学习，不要无意义刷屏",
    "Microsoft guide to pirating Harry Potter for LLM training": "微软LLM训练数据获取指南引发争议",
    "Async/Await on the GPU": "GPU上的异步/等待编程",
    "Quamina and Claude, Case 1": "Quamina与Claude实战案例",
    "Reverse Engineering Sid Meier's Railroad Tycoon": "《铁路大亨》逆向工程研究",
    "Tesla Sales Down": "特斯拉销量大幅下滑",
    "Beautiful interactive explainers": "Claude生成的精美交互式教程",
    "Large Language Models": "大语言模型研究",
    "Machine Learning": "机器学习",
    "Deep Learning": "深度学习",
    "Computer Vision": "计算机视觉",
}

def translate_title(title):
    """翻译标题"""
    for eng, chn in TRANSLATIONS.items():
        if eng.lower() in title.lower():
            return chn
    
    # 简单规则翻译
    title_lower = title.lower()
    if 'claude' in title_lower:
        return f"Claude大模型: {title[:30]}"
    if 'gpt' in title_lower or 'openai' in title_lower:
        return f"OpenAI动态: {title[:30]}"
    if 'llm' in title_lower:
        return f"大语言模型: {title[:30]}"
    if 'ai' in title_lower:
        return f"AI技术: {title[:30]}"
    
    return title[:50] + "..." if len(title) > 50 else title

def main():
    api_file = Path("api/tech-news.json")
    
    with open(api_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 翻译所有标题和摘要
    for category in data.get('categories', []):
        for article in category.get('articles', []):
            # 翻译标题
            original_title = article.get('title', '')
            article['title'] = translate_title(original_title)
            
            # 生成中文摘要
            if 'summary' in article:
                article['summary'] = f"{article['tag']}: {article['title'][:40]}..."
    
    # 保存
    with open(api_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已将所有标题翻译为中文")

if __name__ == "__main__":
    main()
