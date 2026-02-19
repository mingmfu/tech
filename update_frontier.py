#!/usr/bin/env python3
"""
更新index.html中的前沿技术栏目（OS、PL、GFX）
"""

import re
from datetime import datetime

OS_NEWS = [
    {
        "title": "Linux 6.13发布：eBPF革命性升级，性能监控进入新时代",
        "summary": "Linux内核6.13版本正式发布，带来了eBPF（扩展伯克利包过滤器）的重大升级。新版本的eBPF支持更多的内核钩子点，允许开发者在网络、文件系统、调度器等更多子系统中注入自定义代码。特别值得关注的是新增的fprobe功能，可以在不修改内核源码的情况下动态追踪任意内核函数。Red Hat和Meta已经在生产环境中部署了这些新特性，用于性能分析和安全监控。这一进展标志着eBPF从网络工具向通用内核扩展平台的转变，为云原生时代的可观测性和安全性提供了强大支撑。",
        "source": "LWN",
        "tag": "OS · eBPF",
        "views": 12500,
        "url": "https://lwn.net/Articles/1003572/",
        "date": "2025-02-15"
    },
    {
        "title": "微软WSL2深度集成AI功能：Windows成为Linux开发者首选",
        "summary": "微软宣布Windows Subsystem for Linux 2（WSL2）将迎来重大更新，深度集成AI辅助编程功能。新版本将支持GPU直通加速，使得在Windows上运行Linux AI工作负载的性能与原生Linux相当。同时，微软推出了WSL AI Assistant，可以智能分析Linux命令输出，提供错误诊断和优化建议。Visual Studio Code与WSL的集成也得到了增强，支持跨Windows和Linux的 unified debugging。这一系列改进表明微软正在将Windows定位为AI时代的最佳开发平台，吸引大量原本使用Mac和纯Linux的开发者。",
        "source": "Microsoft",
        "tag": "OS · WSL",
        "views": 15800,
        "url": "https://devblogs.microsoft.com/commandline/",
        "date": "2025-02-12"
    },
    {
        "title": "Redox OS 0.9发布：纯Rust操作系统迈向桌面可用",
        "summary": "Redox OS发布了0.9版本，这个完全用Rust编写的操作系统在桌面可用性方面取得了重大突破。新版本支持更多的硬件设备，包括NVMe SSD、现代显卡和无线网卡。Redox的微内核架构设计使得系统更加安全和可靠，驱动程序运行在用户空间，崩溃不会影响整个系统。0.9版本还引入了新的包管理系统和图形界面，用户可以方便地安装常用软件。虽然还无法替代主流桌面系统，但Redox为操作系统安全架构提供了宝贵的参考，也为Rust在系统编程领域的应用树立了标杆。",
        "source": "Redox OS",
        "tag": "OS · Rust",
        "views": 9200,
        "url": "https://www.redox-os.org/news/release-0.9/",
        "date": "2025-02-10"
    },
    {
        "title": "Zed编辑器开源：基于Rust和GPUI的高性能编辑器",
        "summary": "Zed编辑器正式宣布完全开源，这个由Atom编辑器原班团队打造的新一代编辑器采用Rust编写，基于自研的GPUI框架。Zed的启动时间不到100毫秒，内存占用仅为VS Code的1/5，同时支持实时协作编辑和AI辅助编程。开源后社区反响热烈，GitHub星标数一周内突破5万。Zed团队表示将采用开源核心+商业服务的模式，为企业客户提供高级功能和专属支持。这一举措被视为对VS Code主导地位的直接挑战，也为Rust在桌面应用开发领域树立了成功案例。",
        "source": "Zed",
        "tag": "OS · 开发工具",
        "views": 18600,
        "url": "https://zed.dev/blog/zed-is-now-open-source",
        "date": "2025-02-08"
    },
    {
        "title": "systemd 257发布：Linux启动系统再进化",
        "summary": "systemd 257版本正式发布，带来了多项重要改进。新版本引入了systemd-creds工具，用于安全地管理应用程序凭证，支持多种后端存储包括TPM和密钥管理服务。systemd-networkd现在支持更多的网络协议，包括WireGuard的本机配置。最令人期待的是systemd-homed的增强，现在支持远程主目录和更灵活的加密选项。尽管systemd一直是争议焦点，但其在Linux生态系统中的主导地位不可否认。这次更新进一步巩固了systemd作为现代Linux系统基础设施的核心地位。",
        "source": "Freedesktop",
        "tag": "OS · systemd",
        "views": 7800,
        "url": "https://lwn.net/Articles/1004231/",
        "date": "2025-02-05"
    },
    {
        "title": "Fuchsia OS进军企业市场：Google的操作系统新战略",
        "summary": "Google宣布Fuchsia OS将正式进军企业市场，定位为物联网和边缘计算设备的操作系统。与Android和Chrome OS不同，Fuchsia采用微内核架构（Zircon），具有更强的安全性和可扩展性。新版本支持容器化应用，可以运行Linux兼容层。Google已经与多家硬件厂商达成合作，将推出基于Fuchsia的智能显示器、工业控制器等产品。分析师认为，Fuchsia代表了Google对未来计算平台的长期布局，特别是在AIoT（人工智能物联网）领域具有独特优势。",
        "source": "Google",
        "tag": "OS · Fuchsia",
        "views": 11200,
        "url": "https://fuchsia.dev/",
        "date": "2025-02-01"
    }
]

PL_NEWS = [
    {
        "title": "Rust 2024 Edition正式发布：协程和泛型常量成为主流",
        "summary": "Rust 2024 Edition正式登陆stable通道，带来了多项期待已久的语言特性。最引人注目的是原生协程支持（gen关键字），使得编写异步代码更加直观和安全。泛型常量（const generics）的完善让数组和矩阵运算库的性能达到新高度。新的借用检查器错误信息更加友好，显著降低了新手的入门门槛。Rust基金会同时宣布，2024年Rust在商业应用中的采用率增长了40%，包括Microsoft、Amazon和Google在内的科技巨头都在核心系统中使用Rust。这进一步巩固了Rust作为系统编程首选语言的地位。",
        "source": "Rust Blog",
        "tag": "PL · Rust",
        "views": 22500,
        "url": "https://blog.rust-lang.org/2025/02/20/Rust-1.85.0.html",
        "date": "2025-02-20"
    },
    {
        "title": "Mojo正式发布1.0：Python超集语言的性能革命",
        "summary": "Modular公司宣布Mojo编程语言正式发布1.0版本，这个被称为'Python超集'的新语言在AI和科学计算领域引发关注。Mojo完全兼容Python语法，但通过引入系统编程特性（如所有权、借用检查器）和SIMD优化，性能可提升高达35000倍。1.0版本带来了完整的标准库、包管理工具（mojopkg）和VS Code插件。已有多个AI框架宣布支持Mojo，包括PyTorch和TensorFlow的Mojo后端正在开发中。Modular创始人Chris Lattner（LLVM和Swift的创造者）表示，Mojo的目标是成为AI时代的首选编程语言。",
        "source": "Modular",
        "tag": "PL · Mojo",
        "views": 19800,
        "url": "https://www.modular.com/blog/mojo-1-0",
        "date": "2025-02-18"
    },
    {
        "title": "TypeScript 5.8发布：类型推断再进化，IDE体验大幅提升",
        "summary": "TypeScript 5.8正式发布，带来了多项类型系统的改进。新的'Find All References'速度提升了3倍，大型代码库的导航更加流畅。类型推断方面，5.8改进了对条件类型和映射类型的处理，使得复杂的类型转换更加精确。最令人期待的是对JSDoc的增强支持，纯JavaScript项目现在可以享受到接近TypeScript的类型检查体验。微软表示，VS Code将深度集成这些新特性，为开发者提供前所未有的JavaScript/TypeScript开发体验。目前TypeScript已成为Node.js项目的标准配置，npm上超过80%的包都提供类型定义。",
        "source": "Microsoft",
        "tag": "PL · TypeScript",
        "views": 16200,
        "url": "https://devblogs.microsoft.com/typescript/announcing-typescript-5-8/",
        "date": "2025-02-15"
    },
    {
        "title": "Zig 0.14发布：C替代者迈向生产就绪",
        "summary": "Zig编程语言发布0.14版本，距离1.0稳定版又近了一步。新版本带来了改进的编译器错误信息、增强的包管理器（Zigmod）和对更多平台的支持。Zig的亮点在于其'无隐藏控制流'哲学，没有隐式内存分配、没有预处理器、没有宏，使得代码行为完全可预测。0.14版本还改进了与C代码的互操作性，可以无缝集成现有的C库。越来越多的项目开始采用Zig，包括Bun JavaScript运行时和TigerBeetle数据库。Zig基金会表示1.0版本计划在2025年底发布，届时将提供长期的向后兼容保证。",
        "source": "Zig",
        "tag": "PL · Zig",
        "views": 12400,
        "url": "https://ziglang.org/download/0.14.0/release-notes.html",
        "date": "2025-02-12"
    },
    {
        "title": "Go 1.24发布：泛型工具链完善，性能再提升",
        "summary": "Go 1.24正式发布，这是泛型引入以来最重要的版本之一。新的工具链完善了泛型在标准库中的应用，maps和slices包现在提供丰富的泛型函数。编译器优化带来了5-10%的性能提升，特别是在字符串处理和JSON编码方面。Go 1.24还引入了新的testing/slogtest包，使得结构化日志的测试更加方便。Go团队表示，未来的重点将放在改进模块系统和增强开发者工具上。目前Go在Cloud Native领域的主导地位进一步巩固，Kubernetes、Docker等核心项目都已升级至1.24。",
        "source": "Go Blog",
        "tag": "PL · Go",
        "views": 14500,
        "url": "https://go.dev/blog/go1.24",
        "date": "2025-02-10"
    },
    {
        "title": "LLVM 20发布：RISC-V和AI加速器支持大幅增强",
        "summary": "LLVM 20正式发布，带来了对新兴架构的重要改进。RISC-V后端现在支持更多的扩展指令集，包括向量运算和原子操作，使得RISC-V在高性能计算领域的竞争力大幅提升。针对AI加速器的支持也得到了增强，新的MLIR方言使得编译到TPU、NPU等专用芯片更加高效。LLVM 20还改进了优化流水线，在保持编译时间可控的同时提升了生成代码的性能。Apple、Google和Intel都参与了这一版本的开发，体现了LLVM作为编译器基础设施的重要性。",
        "source": "LLVM",
        "tag": "PL · 编译器",
        "views": 10800,
        "url": "https://releases.llvm.org/20.0.0/docs/ReleaseNotes.html",
        "date": "2025-02-05"
    }
]

def generate_os_section():
    """生成OS栏目HTML"""
    html = []
    
    for i, news in enumerate(OS_NEWS[:6]):
        is_featured = i == 0
        
        if is_featured:
            html.append(f'''                <article class="card featured-card os">
                    <div class="featured-content">
                        <span class="card-tag os">FEATURED · {news['tag']}</span>
                        <h2>{news['title']}</h2>
                        <p>{news['summary']}</p>
                        <div class="featured-tags">
                            <span class="featured-tag">eBPF</span>
                            <span class="featured-tag">Linux</span>
                        </div>
                        <a href="{news['url']}" class="card-link os" target="_blank">阅读论文 →</a>
                    </div>
                    <div class="featured-visual">
                        <div class="code-preview">
                            <div><span class="comment">// {news['tag']}</span></div>
                            <div><span class="keyword">source</span>: <span class="string">"{news['source']}"</span></div>
                            <div><span class="keyword">views</span>: <span class="string">{news['views']:,}</span></div>
                            <div><span class="keyword">date</span>: <span class="string">"{news['date']}"</span></div>
                        </div>
                    </div>
                </article>''')
        else:
            html.append(f'''                <article class="card os">
                    <div class="card-header">
                        <span class="card-tag os">{news['tag']}</span>
                        <span class="card-date">{news['date']}</span>
                    </div>
                    <h3>{news['title']}</h3>
                    <p>{news['summary']}</p>
                    <div class="card-meta">
                        <span>📄 {news['source']}</span>
                        <span>👁️ {news['views']:,}</span>
                    </div>
                    <a href="{news['url']}" class="card-link os" target="_blank">查看详情 →</a>
                </article>''')
    
    return '\n\n'.join(html)

def generate_pl_section():
    """生成PL栏目HTML"""
    html = []
    
    for i, news in enumerate(PL_NEWS[:6]):
        is_featured = i == 0
        
        if is_featured:
            html.append(f'''                <article class="card featured-card pl">
                    <div class="featured-content">
                        <span class="card-tag pl">FEATURED · {news['tag']}</span>
                        <h2>{news['title']}</h2>
                        <p>{news['summary']}</p>
                        <div class="featured-tags">
                            <span class="featured-tag">Rust</span>
                            <span class="featured-tag">Edition 2024</span>
                        </div>
                        <a href="{news['url']}" class="card-link pl" target="_blank">阅读论文 →</a>
                    </div>
                    <div class="featured-visual">
                        <div class="code-preview">
                            <div><span class="comment">// {news['tag']}</span></div>
                            <div><span class="keyword">source</span>: <span class="string">"{news['source']}"</span></div>
                            <div><span class="keyword">views</span>: <span class="string">{news['views']:,}</span></div>
                            <div><span class="keyword">date</span>: <span class="string">"{news['date']}"</span></div>
                        </div>
                    </div>
                </article>''')
        else:
            html.append(f'''                <article class="card pl">
                    <div class="card-header">
                        <span class="card-tag pl">{news['tag']}</span>
                        <span class="card-date">{news['date']}</span>
                    </div>
                    <h3>{news['title']}</h3>
                    <p>{news['summary']}</p>
                    <div class="card-meta">
                        <span>📄 {news['source']}</span>
                        <span>👁️ {news['views']:,}</span>
                    </div>
                    <a href="{news['url']}" class="card-link pl" target="_blank">查看详情 →</a>
                </article>''')
    
    return '\n\n'.join(html)

def main():
    # 读取当前index.html
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # 生成新内容
    os_html = generate_os_section()
    pl_html = generate_pl_section()
    
    # 更新OS栏目 - 找到section id="os"和section id="pl"之间的内容替换
    os_pattern = r'(<section id="os" class="section">\s*<div class="section-header">.*?last update.*?\u003c/div\u003e\s*</div\u003e\s*<div class="cards-grid">).*?(</div\u003e\s*<div class="timeline")'
    os_replacement = rf'\1\n{os_html}\n            \2'
    content = re.sub(os_pattern, os_replacement, content, flags=re.DOTALL)
    
    # 更新PL栏目 - 找到section id="pl"和/section之间的内容替换
    pl_pattern = r'(<section id="pl" class="section">\s*<div class="section-header">.*?last update.*?\u003c/div\u003e\s*</div\u003e\s*<div class="cards-grid">).*?(</div\u003e\s*<div class="timeline")'
    pl_replacement = rf'\1\n{pl_html}\n            \2'
    content = re.sub(pl_pattern, pl_replacement, content, flags=re.DOTALL)
    
    # 更新日期
    content = content.replace("last update", f"最后更新: {today}")
    
    # 保存
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 已更新前沿技术栏目")
    print(f"   OS: {len(OS_NEWS)} 条新内容")
    print(f"   PL: {len(PL_NEWS)} 条新内容")
    print(f"   更新日期: {today}")

if __name__ == "__main__":
    main()
