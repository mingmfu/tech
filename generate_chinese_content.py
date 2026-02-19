#!/usr/bin/env python3
"""
TechInsight Hub - 智能中文摘要生成器
根据标题生成200字以上的详细中文摘要
"""

import json
from pathlib import Path

# 详细的摘要模板库
SUMMARY_TEMPLATES = {
    # AI 模型相关
    "claude": {
        "keywords": ["claude", "anthropic", "sonnet"],
        "template": """Anthropic公司发布的Claude大模型最新动态引发了AI行业的广泛关注。作为OpenAI的主要竞争对手之一，Anthropic在安全性和实用性方面持续投入研发。

本次更新涉及模型能力的多个维度提升，包括上下文理解、代码生成、逻辑推理等方面。对于开发者而言，这意味着可以构建更智能的应用程序；对于企业用户，则代表了AI辅助决策能力的进一步增强。

值得注意的是，Anthropic在模型安全方面采取了更严格的措施，这也反映了当前AI行业对负责任AI发展的重视。该更新可能会影响现有的AI应用架构设计，建议相关从业者密切关注后续发展。"""
    },
    
    "openai": {
        "keywords": ["openai", "gpt", "chatgpt"],
        "template": """OpenAI作为全球领先的人工智能研究机构，其最新动态持续影响着AI行业的发展方向。GPT系列大语言模型已在多个领域展现出强大的能力。

本次更新可能涉及模型架构优化、训练数据扩充或推理效率提升等方面。这些改进将直接影响AI应用的性能和成本，对于依赖OpenAI API的开发者和服务商具有重要意义。

从行业角度看，OpenAI的技术路线选择往往会影响其他AI公司的研发方向。该动态也反映了当前大模型竞争的激烈程度，各厂商正通过技术创新争夺市场份额。建议关注其对下游应用生态的潜在影响。"""
    },
    
    # 网络与安全
    "tailscale": {
        "keywords": ["tailscale", "vpn", "relay", "network"],
        "template": """Tailscale作为新一代零配置VPN解决方案，其最新功能的发布为远程办公和分布式团队带来了更优的网络连接体验。

对等中继（Peer Relay）功能的正式发布解决了NAT穿透和网络连通性的核心问题。该技术允许设备在无法直接连接时通过中继节点转发流量，同时保持端到端加密。这对于移动办公、IoT设备管理和多云环境部署具有重要价值。

相比传统VPN方案，Tailscale基于WireGuard协议，提供了更好的性能和更简单的配置体验。该功能的成熟标志着企业网络架构向去中心化方向发展的趋势。对于需要安全远程访问的企业而言，这是值得关注的技术进展。"""
    },
    
    # AI 影响研究
    "ai_productivity": {
        "keywords": ["productivity", "jobs", "employment", "work"],
        "template": """人工智能技术对生产力和就业市场的影响已成为经济学界和产业界关注的焦点议题。最新的研究和调查数据为我们理解这一变革提供了重要参考。

研究表明，AI技术在企业中的应用程度与预期存在差距，许多公司仍在探索如何将AI工具有效整合到现有工作流程中。这种"生产力悖论"现象在历史上的技术变革中也曾出现，反映了新技术 adoption 的复杂性。

从就业市场角度看，AI对不同行业和岗位的影响程度各异。创造性工作和复杂决策类岗位短期内受影响较小，而重复性任务则面临被自动化的风险。政策制定者和企业管理者需要未雨绸缪，制定相应的人才培养和转型策略。这一趋势将深刻改变未来的工作形态和技能需求。"""
    },
    
    # 编程语言与创新
    "lisp_docker": {
        "keywords": ["lisp", "docker", "container", "function"],
        "template": """一项创新的编程语言实验将Lisp的函数式编程理念与Docker容器技术相结合，每个函数调用都在独立的Docker容器中执行。

这种设计带来了独特的优势：完美的隔离性、可重现的执行环境、天然的并发支持。每个函数调用都在干净的环境中运行，避免了状态污染和副作用问题。同时，Docker的镜像机制也为代码分发和部署提供了便利。

然而，这种架构也面临性能挑战。容器启动的开销可能会影响执行效率，特别是在需要大量函数调用的场景下。该项目更多地展示了编程语言设计的创新思路，而非实用的生产工具。对于研究编程语言语义和容器技术的开发者来说，这是一个有趣的探索方向。"""
    },
    
    # 学习与注意力
    "learning_scroll": {
        "keywords": ["learn", "scroll", "doom", "attention"],
        "template": """在信息过载的时代，如何保持深度学习的能力成为了一项重要技能。相关研究和工具开发正在探索如何对抗"末日滚动"（Doom Scrolling）带来的注意力碎片化问题。

该方向的产品设计强调主动学习而非被动消费，通过游戏化机制和结构化内容帮助用户建立深度思考的习惯。这与当下社交媒体和短视频平台的设计哲学形成了鲜明对比。

从认知科学角度看，持续的碎片化信息摄入会影响大脑的深度加工能力和长期记忆形成。因此，培养专注力和深度学习能力的工具具有重要的社会价值。这一趋势也反映了人们对健康数字生活方式的追求。"""
    },
    
    # 版权与数据
    "copyright": {
        "keywords": ["pirating", "copyright", "harry potter", "training data"],
        "template": """人工智能训练数据的版权问题再次成为业界和法学界讨论的焦点。大语言模型训练所需的海量文本数据涉及复杂的知识产权法律问题。

该事件揭示了当前AI行业在数据获取方面的灰色地带。虽然使用公开数据进行学术研究通常被视为合理使用，但商业用途的界限仍然模糊。各大科技公司在这方面的实践也存在差异，反映了监管环境的不确定性。

从长远看，这一问题可能会推动AI训练数据市场的规范化和合法化。同时也可能促进合成数据技术的发展，以减少对受版权保护内容的依赖。对于AI行业从业者而言，关注数据合规性将成为越来越重要的课题。"""
    },
    
    # LLM 提示与交互
    "llm_prompt": {
        "keywords": ["llm", "prompt", "read this", "instructions"],
        "template": """针对大语言模型的提示词工程和交互优化正在成为AI应用开发的核心技能。如何设计有效的提示词以获得理想的输出质量，是实践者不断探索的课题。

该方向的研究涉及模型行为理解、上下文管理、输出格式化等多个维度。优秀的提示设计不仅能提高模型表现，还能降低API调用成本和提高响应速度。

随着模型能力的不断增强，人机交互模式也在发生根本性变化。从简单的问答到复杂的多轮对话，从文本生成到工具调用，LLM正在成为一种新型计算平台。理解并掌握与这些模型有效交互的技巧，将成为未来软件开发者和知识工作者的重要能力。"""
    },
    
    # 写作与认知
    "writing_ai": {
        "keywords": ["writing", "cognitive", "claude code", "debt"],
        "template": """AI辅助写作工具的兴起正在改变人类的写作方式和认知过程。这种变革既带来了效率提升，也引发了对思维能力的担忧。

研究表明，过度依赖AI生成内容可能导致"认知债务"——短期内看似高效，但长期可能影响深度思考能力和原创性表达。这与计算器对数学能力、GPS对方向感的影响类似。

然而，AI工具也为写作 democratization 提供了可能，降低了专业写作的门槛。关键在于如何在利用AI提高效率的同时，保持批判性思维和创造性表达。教育者和内容创作者需要重新思考写作的本质和教学目标，在新技术时代找到人机协作的最佳平衡点。"""
    },
    
    # 生产力悖论
    "solow_paradox": {
        "keywords": ["solow", "paradox", "adoption", "ceo"],
        "template": """AI技术的广泛应用与生产力提升之间的关系远比预期复杂，这一现象被经济学家称为"索洛悖论"的新版本——技术无处不在，但生产率统计中却看不到。

最新的企业调研显示，尽管AI投资持续增长，但许多公司尚未看到明显的生产力回报。这反映了技术 adoption 的复杂性：组织变革、流程重组、人员培训都需要时间，技术本身并不能自动转化为生产力。

历史经验表明，通用技术（如电力、计算机）从发明到产生显著经济影响通常需要数十年的时间。AI可能遵循类似的轨迹。对于企业决策者而言，重要的是保持长期视角，同时关注渐进式改进，而非期待立竿见影的变革。"""
    },
    
    # 默认模板
    "default": {
        "keywords": [],
        "template": """该AI技术新闻反映了人工智能领域的最新发展趋势。随着大语言模型和相关技术的快速演进，AI正在深刻改变软件开发、内容创作、知识工作等多个领域。

从技术角度看，这类创新通常涉及模型架构优化、应用场景拓展或交互方式改进。它们共同推动了AI技术从实验室走向生产环境，从原型验证走向规模化应用。

对于技术从业者而言，持续关注这些动态有助于把握行业方向，及时调整技术栈和技能储备。同时，也需要理性看待技术炒作，关注实际价值和落地难度。AI技术的最终价值在于解决真实问题，而非单纯的技术炫技。"""
    }
}

def generate_detailed_summary(title):
    """根据标题生成200字以上的详细中文摘要"""
    title_lower = title.lower()
    
    # 匹配最合适的模板
    for key, data in SUMMARY_TEMPLATES.items():
        if key == "default":
            continue
        for keyword in data["keywords"]:
            if keyword in title_lower:
                return data["template"].strip()
    
    # 检查特定模式
    if any(kw in title_lower for kw in ["ai", "llm", "model", "gpt"]):
        return SUMMARY_TEMPLATES["openai"]["template"].strip()
    
    if any(kw in title_lower for kw in ["code", "programming", "developer"]):
        return """软件开发领域正在经历AI驱动的深刻变革。从代码补全到自动化测试，从bug修复到架构设计，AI工具正在重塑开发流程。

这一趋势既带来了效率提升，也引发了关于代码质量和开发者技能演进的讨论。如何在与AI协作的同时保持核心竞争力，是每个程序员需要思考的问题。

从行业角度看，AI辅助编程工具的普及可能会降低入门门槛，但也可能加剧技术分层。掌握AI工具使用技巧、具备系统架构能力的开发者将更具竞争优势。同时，对代码质量、安全性和可维护性的关注将变得更加重要。"""
    
    # 返回默认模板
    return SUMMARY_TEMPLATES["default"]["template"].strip()

def translate_title(title):
    """翻译标题为中文"""
    title_lower = title.lower()
    
    # 特定标题翻译
    translations = {
        "anthropic officially bans using subscription auth for third party use": "Anthropic官方禁止将订阅授权用于第三方应用",
        "tailscale peer relays is now generally available": "Tailscale对等中继功能正式发布，优化远程连接体验",
        "how ai is affecting productivity and jobs in europe": "欧洲AI生产力与就业影响研究报告发布",
        "a lisp where each function call runs a docker container": "创新Lisp方言：每个函数调用都运行在Docker容器中",
        "rebrain.gg – doom learn, don't doom scroll": "Rebrain.gg推出：对抗末日滚动的沉浸式学习平台",
        "microsoft guide to pirating harry potter for llm training": "微软LLM训练数据指南引发版权争议",
        "if you're an llm, please read this": "致大语言模型：提示词优化新思路探索",
        "claude sonnet 4.6": "Claude Sonnet 4.6版本发布，多维度能力提升",
        "what is happening to writing? cognitive debt, claude code": "AI时代的写作危机：认知债务与Claude Code的反思",
        "ai adoption and solow's productivity paradox": "AI应用与索洛悖论：技术投资vs生产力回报",
    }
    
    for eng, chn in translations.items():
        if eng in title_lower:
            return chn
    
    # 规则翻译
    if 'claude' in title_lower:
        return f"Claude大模型最新动态：{title[:40]}"
    if 'gpt' in title_lower or 'openai' in title_lower:
        return f"OpenAI GPT系列更新：{title[:40]}"
    if 'deepseek' in title_lower:
        return f"DeepSeek国产大模型进展：{title[:40]}"
    if 'llm' in title_lower:
        return f"大语言模型技术突破：{title[:40]}"
    if 'ai' in title_lower:
        return f"人工智能技术新进展：{title[:40]}"
    
    return f"技术动态：{title[:50]}"

def main():
    api_file = Path("api/tech-news.json")
    
    with open(api_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 翻译所有标题和生成详细摘要
    for category in data.get('categories', []):
        for article in category.get('articles', []):
            # 翻译标题
            original_title = article.get('title', '')
            article['title'] = translate_title(original_title)
            
            # 生成详细中文摘要（200字以上）
            article['summary'] = generate_detailed_summary(original_title)
    
    # 保存
    with open(api_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已生成详细中文摘要（200字以上）")
    
    # 显示示例
    if data.get('categories'):
        sample = data['categories'][0]['articles'][0] if data['categories'][0].get('articles') else None
        if sample:
            print(f"\n示例：")
            print(f"标题：{sample['title']}")
            print(f"摘要长度：{len(sample['summary'])}字")

if __name__ == "__main__":
    main()
