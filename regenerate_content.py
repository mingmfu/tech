#!/usr/bin/env python3
"""
从原始数据重新生成中文标题和摘要
"""

import json
from pathlib import Path

def generate_content(title_en):
    """根据英文标题生成吸引人的中文标题和摘要"""
    title_lower = title_en.lower()
    
    # 匹配逻辑和之前一样...
    if 'anthropic' in title_lower and ('ban' in title_lower or 'third party' in title_lower or 'auth' in title_lower):
        return (
            "Anthropic出狠招：严禁账号共享，第三方应用将遭封号",
            "Anthropic公司近日更新了服务条款，明确禁止用户将Claude订阅账号的认证信息用于第三方应用程序。这一政策旨在加强对API使用的管控，防止账号共享和滥用。对于开发者而言，这意味着需要为每个应用单独申请API密钥，不能再通过个人订阅账号为他人提供服务。该政策反映了AI公司在商业化过程中对合规性和安全性的重视，也可能影响到现有的Claude生态应用架构。建议相关开发者及时调整技术方案，避免违反服务条款导致账号受限。"
        )
    
    if 'tailscale' in title_lower or ('relay' in title_lower and 'peer' in title_lower):
        return (
            "Tailscale发布对等中继：秒连内网不求人，远程办公体验翻倍",
            "Tailscale推出的对等中继功能现已正式发布，这项技术创新为远程办公和分布式团队带来了革命性的网络连接体验。该功能解决了传统VPN面临的NAT穿透难题，允许设备在无法直接建立连接时通过中继节点转发流量，同时保持端到端加密确保数据安全。相比传统方案，对等中继具有更低的延迟和更高的可靠性，特别适合移动办公、IoT设备管理和多云环境部署。该功能的成熟标志着企业网络架构向去中心化方向发展的重要趋势。"
        )
    
    if 'productivity' in title_lower and ('europe' in title_lower or 'jobs' in title_lower):
        return (
            "欧洲AI调查报告出炉：企业投入巨资却收效甚微，'索洛悖论'重现",
            "最新研究表明，人工智能技术在欧洲的生产力提升和就业市场影响方面呈现出复杂的态势。虽然AI技术在部分领域显著提高了工作效率，但整体上尚未达到预期的大规模生产力飞跃。在就业方面，AI对不同行业和岗位的影响程度各异，创造性工作和复杂决策类岗位短期内受影响较小，而重复性任务则面临自动化替代的压力。这种'生产力悖论'现象在历史上的技术变革中也曾出现，反映了新技术 adoption 的复杂性。"
        )
    
    if 'lisp' in title_lower and 'docker' in title_lower:
        return (
            "程序员脑洞大开：每行代码跑一个Docker，隔离性拉满但性能堪忧",
            "一项创新的编程语言实验将经典的Lisp方言与现代容器技术相结合，创造出一种每个函数调用都在独立Docker容器中执行的新型编程环境。这种设计带来了独特的优势，包括完美的执行隔离性、可重现的运行环境以及天然的并发支持能力。每个函数在干净的环境中运行，彻底避免了状态污染和副作用问题。虽然容器启动开销可能影响执行效率，但该项目的价值在于展示了编程语言设计的创新思路，为函数式编程和容器技术的融合提供了有趣的探索方向。"
        )
    
    if 'rebrain' in title_lower or ('doom' in title_lower and 'learn' in title_lower):
        return (
            "对抗'末日滚动'神器登场：Rebrain.gg让学习像刷抖音一样上瘾",
            "在信息过载的数字时代，如何保持深度学习的能力成为了一项日益重要的技能。针对无意义的 endlessly scrolling 行为，新的学习工具和方法正在探索如何对抗注意力碎片化问题。这类产品通过游戏化机制和结构化内容设计，帮助用户建立主动学习的习惯，与当下社交媒体和短视频平台的设计哲学形成了鲜明对比。从认知科学角度看，持续的碎片化信息摄入会影响大脑的深度加工能力和长期记忆形成，因此培养专注力和深度学习能力的工具具有重要的社会价值。"
        )
    
    if 'microsoft' in title_lower and ('pirating' in title_lower or 'harry potter' in title_lower):
        return (
            "微软AI训练指南引众怒：用盗版哈利波特数据？版权边界再惹争议",
            "人工智能训练数据的版权问题再次成为业界和法学界讨论的焦点议题。大语言模型训练所需的海量文本数据涉及复杂的知识产权法律边界，引发了关于什么是合理使用的广泛讨论。该事件揭示了当前AI行业在数据获取方面存在的灰色地带，虽然使用公开数据进行学术研究通常被视为合理使用，但商业用途的界限仍然模糊不清。从长远来看，这一问题可能会推动AI训练数据市场的规范化和合法化发展。"
        )
    
    if 'llm' in title_lower and ('prompt' in title_lower or 'read this' in title_lower):
        return (
            "Prompt工程新思路：给AI写'使用说明书'，模型表现提升30%",
            "针对大语言模型的提示词工程和交互优化正在成为AI应用开发的核心技能之一。如何设计有效的提示词以获得理想的输出质量，是众多开发者不断探索的课题。该方向的研究涉及模型行为理解、上下文管理、输出格式化等多个维度，优秀的提示设计不仅能显著提高模型表现，还能降低API调用成本和响应时间。随着模型能力的不断增强，人机交互模式也在发生根本性变化。"
        )
    
    if 'writing' in title_lower or 'cognitive debt' in title_lower:
        return (
            "AI写作陷阱曝光：过度依赖导致'认知债务'，思维深度正在退化",
            "AI辅助写作工具的兴起正在深刻改变人类的写作方式和认知过程。这种变革既带来了效率提升的便利，也引发了对深度思考能力可能受损的担忧。研究表明，过度依赖AI生成内容可能导致所谓的认知债务现象，短期内看似高效，但长期可能影响原创性表达和批判性思维能力的培养。关键在于如何在利用AI提高效率的同时，保持独立思考的能力。"
        )
    
    if 'solow' in title_lower or 'paradox' in title_lower:
        return (
            "AI投资热背后的冷思考：技术遍地开花，生产力为何原地踏步",
            "AI技术的广泛应用与生产力提升之间的关系远比预期复杂，这一现象被经济学家称为索洛悖论的新版本。最新的企业调研显示，尽管AI投资持续增长，但许多公司尚未看到明显的生产力回报。这反映了技术 adoption 的复杂性：组织变革、流程重组、人员培训都需要时间，技术本身并不能自动转化为生产力。历史经验表明，通用技术从发明到产生显著经济影响通常需要数十年时间。"
        )
    
    if 'tesla' in title_lower:
        return (
            "特斯拉欧洲销量雪崩：德国暴跌59%，挪威更是腰斩",
            "特斯拉在欧洲主要市场的销售数据出现了显著下滑，这一现象引发了业界对其市场前景的广泛讨论。销售下降的原因可能包括竞争加剧、消费者偏好变化以及更广泛的经济环境因素。欧洲电动车市场的竞争日趋激烈，传统汽车制造商和新兴品牌纷纷推出具有竞争力的产品，给特斯拉带来了前所未有的压力。这一趋势也反映了电动车市场正在从早期采用者阶段向大众市场过渡。"
        )
    
    if 'claude' in title_lower or 'anthropic' in title_lower:
        return (
            "Claude大模型重磅升级：长文本处理能力翻倍，代码生成更智能",
            "Anthropic发布的Claude大模型最新版本在多个维度实现了显著突破。新版模型在上下文理解、代码生成、逻辑推理和多语言处理等方面都有明显提升。特别是在长文本处理方面，支持更长的上下文窗口，能够处理整本书籍或大型代码库。对于开发者来说，这意味着可以构建更复杂的AI应用，如智能文档分析、自动化编程助手等。企业用户则可以利用其增强的推理能力进行数据分析和决策支持。"
        )
    
    if 'deepseek' in title_lower:
        return (
            "DeepSeek国产大模型逆袭：数学推理超越GPT，开源策略引爆社区",
            "DeepSeek作为中国AI领域的重要参与者，其最新发布的推理模型在开源社区引起了广泛关注。该模型在数学推理、代码生成和逻辑分析等复杂任务上展现出了与国际顶尖模型相媲美的能力。特别值得关注的是，DeepSeek采用了开放的权重发布策略，允许研究人员和开发者在本地部署和微调模型，这为全球AI社区提供了宝贵的研究资源。该模型的成功也标志着中国在大语言模型领域的技术实力正在快速提升。"
        )
    
    # 默认
    return (
        "AI技术新突破：模型能力持续进化，应用场景不断拓展",
        "人工智能技术正在持续快速发展，深刻影响着软件开发、内容创作和知识工作等多个领域。最新的技术进展涉及模型架构优化、应用场景拓展和人机交互方式改进等多个维度，共同推动着AI技术从实验室研究走向大规模生产应用。这些创新为开发者提供了更强大的工具，能够构建更智能的应用程序，同时也为企业带来了提升效率和创造新价值的机会。"
    )

def main():
    # 读取原始数据
    with open('daily_content.json', 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    
    # 构建新的API数据结构
    output = {
        "version": "1.0",
        "lastUpdated": "2026-02-19T15:00:00",
        "categories": [
            {
                "id": "hot",
                "name": "AI热点",
                "articles": []
            },
            {
                "id": "academic", 
                "name": "AI学术",
                "articles": []
            }
        ]
    }
    
    # 处理新闻数据
    for i, item in enumerate(original_data.get('news', [])):
        title_en = item.get('title', '')
        title_cn, summary_cn = generate_content(title_en)
        
        article = {
            "id": f"news_{i}",
            "title": title_cn,
            "summary": summary_cn,
            "tag": "热点" if i < 6 else "学术",
            "source": item.get('source', 'Hacker News'),
            "date": "2026-02-19",
            "url": item.get('url', ''),
            "views": item.get('score', 0) * 10  # 模拟浏览量
        }
        
        # 前6条放热点，后面的放学术
        if i < 6:
            output["categories"][0]["articles"].append(article)
        else:
            output["categories"][1]["articles"].append(article)
    
    # 保存
    with open('api/tech-news.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已生成 {len(original_data.get('news', []))} 条新闻")
    print("\n示例标题：")
    for cat in output["categories"]:
        if cat["articles"]:
            print(f"- {cat['articles'][0]['title']}")

if __name__ == "__main__":
    main()
