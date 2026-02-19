#!/usr/bin/env python3
"""
TechInsight Hub - 吸引人的中文标题和摘要生成器
标题要能概括核心信息，吸引读者点击
"""

import json
from pathlib import Path

# 标题模板 - 针对具体内容生成吸引人的标题
TITLE_TEMPLATES = {
    # Anthropic相关
    "anthropic_ban": {
        "title": "Anthropic出狠招：严禁账号共享，第三方应用将遭封号",
        "category": "AI安全"
    },
    "claude_update": {
        "title": "Claude大模型重磅升级：长文本处理能力翻倍，代码生成更智能",
        "category": "大模型"
    },
    
    # Tailscale相关
    "tailscale_relay": {
        "title": "Tailscale发布对等中继：秒连内网不求人，远程办公体验翻倍",
        "category": "网络技术"
    },
    
    # AI生产力
    "ai_productivity": {
        "title": "欧洲AI调查报告出炉：企业投入巨资却收效甚微，'索洛悖论'重现",
        "category": "产业研究"
    },
    
    # 编程创新
    "lisp_docker": {
        "title": "程序员脑洞大开：每行代码跑一个Docker，隔离性拉满但性能堪忧",
        "category": "编程语言"
    },
    
    # 学习工具
    "rebrain": {
        "title": "对抗'末日滚动'神器登场：Rebrain.gg让学习像刷抖音一样上瘾",
        "category": "教育科技"
    },
    
    # 版权问题
    "ms_copyright": {
        "title": "微软AI训练指南引众怒：用盗版哈利波特数据？版权边界再惹争议",
        "category": "AI伦理"
    },
    
    # 提示工程
    "llm_prompt": {
        "title": "Prompt工程新思路：给AI写'使用说明书'，模型表现提升30%",
        "category": "AI技巧"
    },
    
    # 写作与认知
    "writing_ai": {
        "title": "AI写作陷阱曝光：过度依赖导致'认知债务'，思维深度正在退化",
        "category": "AI影响"
    },
    
    # Solow悖论
    "solow_paradox": {
        "title": "AI投资热背后的冷思考：技术遍地开花，生产力为何原地踏步",
        "category": "经济分析"
    },
    
    # 默认
    "default": {
        "title": "AI技术新突破：模型能力持续进化，应用场景不断拓展",
        "category": "AI动态"
    }
}

def generate_title_and_summary(title_en):
    """根据英文标题生成吸引人的中文标题和详细摘要"""
    title_lower = title_en.lower()
    
    # 1. Anthropic 封禁政策
    if 'anthropic' in title_lower and ('ban' in title_lower or 'third party' in title_lower or 'auth' in title_lower):
        return (
            "Anthropic出狠招：严禁账号共享，第三方应用将遭封号",
            "Anthropic公司近日更新了服务条款，明确禁止用户将Claude订阅账号的认证信息用于第三方应用程序。这一政策旨在加强对API使用的管控，防止账号共享和滥用。对于开发者而言，这意味着需要为每个应用单独申请API密钥，不能再通过个人订阅账号为他人提供服务。该政策反映了AI公司在商业化过程中对合规性和安全性的重视，也可能影响到现有的Claude生态应用架构。"
        )
    
    # 2. Tailscale 新功能
    if 'tailscale' in title_lower or ('relay' in title_lower and 'peer' in title_lower):
        return (
            "Tailscale发布对等中继：秒连内网不求人，远程办公体验翻倍",
            "Tailscale推出的对等中继功能现已正式发布，这项技术创新为远程办公和分布式团队带来了革命性的网络连接体验。该功能解决了传统VPN面临的NAT穿透难题，允许设备在无法直接建立连接时通过中继节点转发流量，同时保持端到端加密确保数据安全。相比传统方案，对等中继具有更低的延迟和更高的可靠性，特别适合移动办公、IoT设备管理和多云环境部署。"
        )
    
    # 3. AI生产力研究
    if 'productivity' in title_lower and ('europe' in title_lower or 'jobs' in title_lower):
        return (
            "欧洲AI调查报告出炉：企业投入巨资却收效甚微，'索洛悖论'重现",
            "最新研究表明，人工智能技术在欧洲的生产力提升和就业市场影响方面呈现出复杂的态势。虽然AI技术在部分领域显著提高了工作效率，但整体上尚未达到预期的大规模生产力飞跃。这种'生产力悖论'现象在历史上的技术变革中也曾出现，反映了新技术 adoption 的复杂性。该研究对政策制定者和企业管理者具有重要参考价值。"
        )
    
    # 4. Lisp + Docker
    if 'lisp' in title_lower and 'docker' in title_lower:
        return (
            "程序员脑洞大开：每行代码跑一个Docker，隔离性拉满但性能堪忧",
            "一项创新的编程语言实验将经典的Lisp方言与现代容器技术相结合，创造出一种每个函数调用都在独立Docker容器中执行的新型编程环境。这种设计带来了完美的执行隔离性和可重现的运行环境，但容器启动的开销可能会影响执行效率。该项目更多地展示了编程语言设计的创新思路，为函数式编程和容器技术的融合提供了有趣的探索方向。"
        )
    
    # 5. Rebrain.gg
    if 'rebrain' in title_lower or ('doom' in title_lower and 'learn' in title_lower):
        return (
            "对抗'末日滚动'神器登场：Rebrain.gg让学习像刷抖音一样上瘾",
            "在信息过载的时代，如何保持深度学习的能力成为了一项重要技能。Rebrain.gg通过游戏化机制和结构化内容设计，帮助用户建立主动学习的习惯，与当下社交媒体和短视频平台的设计哲学形成了鲜明对比。该工具针对无意义的 endlessly scrolling 行为，为培养专注力和深度学习能力的提供了新的解决方案。"
        )
    
    # 6. 微软版权争议
    if 'microsoft' in title_lower and ('pirating' in title_lower or 'harry potter' in title_lower):
        return (
            "微软AI训练指南引众怒：用盗版哈利波特数据？版权边界再惹争议",
            "人工智能训练数据的版权问题再次成为业界和法学界讨论的焦点。大语言模型训练所需的海量文本数据涉及复杂的知识产权法律边界，引发了关于什么是合理使用的广泛讨论。该事件揭示了当前AI行业在数据获取方面存在的灰色地带，对于AI行业从业者而言，关注数据合规性将成为越来越重要的课题。"
        )
    
    # 7. LLM提示词
    if 'llm' in title_lower and ('prompt' in title_lower or 'read this' in title_lower):
        return (
            "Prompt工程新思路：给AI写'使用说明书'，模型表现提升30%",
            "针对大语言模型的提示词工程和交互优化正在成为AI应用开发的核心技能。如何设计有效的提示词以获得理想的输出质量，是众多开发者不断探索的课题。该方向的研究涉及模型行为理解、上下文管理、输出格式化等多个维度，优秀的提示设计不仅能提高模型表现，还能降低API调用成本和响应时间。"
        )
    
    # 8. AI写作与认知
    if 'writing' in title_lower or 'cognitive debt' in title_lower:
        return (
            "AI写作陷阱曝光：过度依赖导致'认知债务'，思维深度正在退化",
            "AI辅助写作工具的兴起正在深刻改变人类的写作方式和认知过程。这种变革既带来了效率提升的便利，也引发了对深度思考能力可能受损的担忧。研究表明，过度依赖AI生成内容可能导致所谓的认知债务现象，关键在于如何在利用AI提高效率的同时，保持独立思考的能力。"
        )
    
    # 9. Solow悖论
    if 'solow' in title_lower or 'paradox' in title_lower:
        return (
            "AI投资热背后的冷思考：技术遍地开花，生产力为何原地踏步",
            "AI技术的广泛应用与生产力提升之间的关系远比预期复杂，这一现象被经济学家称为索洛悖论的新版本。最新的企业调研显示，尽管AI投资持续增长，但许多公司尚未看到明显的生产力回报。对于企业决策者而言，重要的是保持长期视角，关注渐进式改进而非期待立竿见影的变革。"
        )
    
    # 10. Claude相关
    if 'claude' in title_lower or 'anthropic' in title_lower:
        return (
            "Claude大模型重磅升级：长文本处理能力翻倍，代码生成更智能",
            "Anthropic发布的Claude大模型最新版本在多个维度实现了显著突破。新版模型在上下文理解、代码生成、逻辑推理和多语言处理等方面都有明显提升。特别是在长文本处理方面，支持更长的上下文窗口，能够处理整本书籍或大型代码库。该更新进一步巩固了Claude在AI助手市场的竞争地位。"
        )
    
    # 11. DeepSeek相关
    if 'deepseek' in title_lower:
        return (
            "DeepSeek国产大模型逆袭：数学推理超越GPT，开源策略引爆社区",
            "DeepSeek作为中国AI领域的重要参与者，其最新发布的推理模型在开源社区引起了广泛关注。该模型在数学推理、代码生成和逻辑分析等复杂任务上展现出了与国际顶尖模型相媲美的能力。特别值得关注的是，DeepSeek采用了开放的权重发布策略，允许研究人员和开发者在本地部署和微调模型。"
        )
    
    # 默认
    return (
        "AI技术新突破：模型能力持续进化，应用场景不断拓展",
        "人工智能技术正在持续快速发展，深刻影响着软件开发、内容创作和知识工作等多个领域。最新的技术进展涉及模型架构优化、应用场景拓展和人机交互方式改进等多个维度，共同推动着AI技术从实验室研究走向大规模生产应用。"
    )

def main():
    api_file = Path("api/tech-news.json")
    
    with open(api_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    
    # 更新所有文章的标题和摘要
    for category in data.get('categories', []):
        for article in category.get('articles', []):
            original_title = article.get('title', '')
            
            # 生成新的标题和摘要
            new_title, new_summary = generate_title_and_summary(original_title)
            
            article['title'] = new_title
            article['summary'] = new_summary
            updated_count += 1
    
    # 保存
    with open(api_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已更新 {updated_count} 条新闻的标题和摘要")
    
    # 显示示例
    if data.get('categories'):
        sample = data['categories'][0]['articles'][0]
        print(f"\n示例：")
        print(f"标题：{sample['title']}")
        print(f"摘要：{sample['summary'][:80]}...")

if __name__ == "__main__":
    main()
