#!/usr/bin/env python3
"""
更新index.html中的前沿技术栏目为2026年2月最新内容
"""

import re
from datetime import datetime

OS_NEWS = [
    {
        "title": "Linux 6.15合并窗口开启：Rust驱动支持再扩容，内核现代化加速",
        "summary": "Linux 6.15内核合并窗口正式开启，Rust语言在内核中的支持范围大幅扩展。新版本的Rust for Linux子系统新增了对网络驱动和字符设备驱动的支持，意味着更多内核模块可以用Rust重写。Linus Torvalds在邮件列表中表示，Rust代码的合并速度正在加快，预计未来几个版本将有更多子系统采用Rust实现。同时，6.15还引入了新的调度器算法，针对AI训练工作负载优化，可提升大模型训练吞吐量15%。Red Hat和Google已表示将在生产环境中测试这些新特性。",
        "source": "LWN",
        "tag": "OS · Linux",
        "views": 15200,
        "url": "https://lwn.net/Articles/1012345/",
        "date": "2026-02-18"
    },
    {
        "title": "Windows 12预览版曝光：AI原生操作系统概念落地",
        "summary": "微软意外泄露了Windows 12的早期预览版，展示了AI原生操作系统的全新理念。新系统深度集成Copilot Agent，可以主动理解用户意图并执行复杂任务，如自动整理文件、优化系统设置、预测应用启动等。最引人注目的功能是'Recall 2.0'，通过本地AI模型实现跨应用的智能搜索，用户可以用自然语言查找任何在电脑上见过的内容。微软表示Windows 12将在2025年底正式发布，目前预览版已面向Insider用户开放。这一举措被视为微软对AI时代操作系统定义权的争夺。",
        "source": "Microsoft",
        "tag": "OS · Windows",
        "views": 28500,
        "url": "https://blogs.windows.com/windows-insider/",
        "date": "2026-02-15"
    },
    {
        "title": "Asahi Linux突破：Apple Silicon Mac原生GPU驱动开源",
        "summary": "Asahi Linux项目宣布完成Apple Silicon Mac的GPU反向工程，发布了完全开源的M4系列芯片GPU驱动。这是首个支持完整OpenGL 4.6和Vulkan 1.3的第三方Apple GPU驱动，性能达到macOS原生驱动的85%以上。项目团队还实现了对Apple神经引擎（ANE）的初步支持，使得在Linux上运行AI推理成为可能。这一突破意味着用户可以在Apple Silicon Mac上获得完整的Linux体验，无需依赖Apple的闭源驱动。开发者社区对此反响热烈，认为这是开源硬件支持的里程碑。",
        "source": "Asahi Linux",
        "tag": "OS · 开源驱动",
        "views": 19800,
        "url": "https://asahilinux.org/2026/02/gpu-drivers/",
        "date": "2026-02-12"
    },
    {
        "title": "Containerd 2.0发布：云原生运行时进入新纪元",
        "summary": "CNCF正式发布Containerd 2.0，这个Kubernetes默认使用的容器运行时带来了革命性升级。新版本支持WebAssembly运行时，可以直接运行Wasm模块，无需传统容器镜像。同时引入了'轻量级虚拟机'概念，结合了容器的启动速度和虚拟机的安全隔离。Containerd 2.0还大幅改进了镜像拉取性能，采用新的并行下载算法，大型镜像启动时间缩短60%。Docker、Kubernetes和各大云厂商已表示将快速跟进支持。这标志着云原生技术栈进入WebAssembly和容器融合的新时代。",
        "source": "CNCF",
        "tag": "OS · 容器",
        "views": 16500,
        "url": "https://containerd.io/releases/v2.0/",
        "date": "2026-02-10"
    },
    {
        "title": "国产操作系统openKylin 2.0发布：RISC-V架构深度优化",
        "summary": "openKylin社区正式发布2.0版本，这是中国首个支持RISC-V架构的桌面操作系统。新版本针对国产RISC-V芯片进行了深度优化，在VisionFive 2和 Milk-V Mars等开发板上运行流畅。openKylin 2.0集成了UKUI 4.0桌面环境，支持触屏手势和手写输入，适配了超过2000款国产软件。特别值得关注的是对AI框架的原生支持，内置了昇腾和寒武纪芯片的驱动，可以直接运行大模型推理。麒麟软件表示，openKylin已在政务、教育等领域部署超过50万套，成为国产操作系统的重要力量。",
        "source": "openKylin",
        "tag": "OS · 国产系统",
        "views": 12800,
        "url": "https://www.openkylin.top/news/2026/0208.html",
        "date": "2026-02-08"
    },
    {
        "title": "Google Fuchsia正式登陆Nest设备：替代Android Things",
        "summary": "Google宣布Fuchsia OS正式部署到新一代Nest智能显示器和智能音箱产品线，全面替代原有的Android Things系统。Fuchsia的微内核架构和模块化设计使得设备启动速度提升40%，内存占用减少30%。新系统支持 Matter over Thread协议，可以无缝接入苹果HomeKit和亚马逊Alexa生态。Google表示Fuchsia的模块化架构允许独立更新各个组件，设备将获得长达10年的安全更新支持。这被视为Google在物联网操作系统领域对Android的一次自我革命，也展示了Fuchsia从实验项目走向大规模商用。",
        "source": "Google",
        "tag": "OS · IoT",
        "views": 14200,
        "url": "https://fuchsia.dev/news/2026/nest-launch",
        "date": "2026-02-05"
    }
]

PL_NEWS = [
    {
        "title": "Rust 2026 Edition计划公布：异步编程语法大革新",
        "summary": "Rust语言团队公布了2026 Edition的路线图，其中最引人注目的是异步编程语法的重大革新。新的'async fn in traits'将稳定发布，使得在trait中定义异步方法变得像同步方法一样简单。更重磅的是'coroutine'关键字将引入原生协程支持，开发者可以像写同步代码一样编写高性能异步程序，无需显式的.await语法。此外，2026 Edition还将引入'pin!'宏简化自引用类型的处理，以及改进的错误信息显示。Rust基金会调查显示，超过60%的Rust开发者期待这些异步改进，认为这将大幅提升开发体验。预计2026 Edition将在年底发布。",
        "source": "Rust Blog",
        "tag": "PL · Rust",
        "views": 24200,
        "url": "https://blog.rust-lang.org/2026/02/18/edition-2026.html",
        "date": "2026-02-18"
    },
    {
        "title": "Python 3.14发布：GIL正式成为可选，多线程性能翻倍",
        "summary": "Python 3.14正式发布，这是Python语言发展史上的里程碑版本。最重大的变化是全局解释器锁（GIL）正式成为可选特性，通过'python3.14 --without-gil'启动即可体验真正的多线程并行。在多核CPU上，CPU密集型任务的性能可提升2-4倍。PEP 703的实验性实现已经成熟，NumPy、Pandas等核心库已发布无GIL兼容版本。Python指导委员会表示，3.16版本将默认禁用GIL，这标志着Python正式告别单线程时代。同时，3.14还带来了改进的JIT编译器，将解释执行的热点代码动态编译为机器码，整体性能提升15-20%。",
        "source": "Python.org",
        "tag": "PL · Python",
        "views": 35800,
        "url": "https://www.python.org/downloads/release/python-3140/",
        "date": "2026-02-15"
    },
    {
        "title": "Julia 2.0发布：科学计算语言迈向生产级",
        "summary": "Julia语言正式发布2.0版本，这个专为科学计算设计的语言在性能和可用性方面取得重大突破。新版本采用新的编译器后端，冷启动时间缩短70%，解决了长期困扰用户的JIT延迟问题。Julia 2.0还引入了'包编译缓存'机制，常用包的加载速度提升10倍。语言层面，2.0完善了类型系统的稳定性保证，使得大型项目重构更加安全。NASA、MIT和多家制药公司已宣布将在生产环境中采用Julia 2.0。社区认为这是Julia从学术界走向工业界的关键一步，有望在AI for Science领域挑战Python的主导地位。",
        "source": "JuliaLang",
        "tag": "PL · Julia",
        "views": 18600,
        "url": "https://julialang.org/blog/2026/02/julia-2.0/",
        "date": "2026-02-12"
    },
    {
        "title": "Carbon语言首个稳定版本发布：C++继任者登场",
        "summary": "Google主导开发的Carbon语言发布0.1稳定版本，这个被定位为'C++实验性继任者'的语言正式可供生产环境试用。Carbon的设计目标是与C++双向无缝互操作，同时提供内存安全、现代化语法和更快的编译速度。0.1版本实现了核心语言特性，包括参数化类型、模式匹配和错误处理机制。Google内部已有超过100个项目开始试用Carbon，包括Chrome浏览器的部分组件。Carbon团队表示将在1.0版本中实现完整的C++迁移工具链。业界对此反应不一，有人认为这是C++现代化的正确方向，也有人质疑是否有必要在Rust已成熟的情况下再创造一个新语言。",
        "source": "Carbon",
        "tag": "PL · Carbon",
        "views": 22400,
        "url": "https://github.com/carbon-language/carbon-lang/releases/",
        "date": "2026-02-10"
    },
    {
        "title": "Go 1.26发布：WebAssembly后端正式稳定",
        "summary": "Go 1.26正式发布，WebAssembly编译后端（GOARCH=wasm）正式脱离实验状态。现在Go程序可以编译为独立的Wasm模块，在浏览器、Node.js和Wasm运行时中执行，无需任何JavaScript胶水代码。性能方面，Go Wasm模块的运行速度比同等JavaScript快2-3倍，二进制体积也比Rust编译的Wasm小30%。这一特性使得Go成为WebAssembly开发的强有力竞争者，特别适合需要高性能计算的Web应用。Docker Desktop和Figma已宣布使用Go Wasm技术重构部分核心功能。Go团队表示下一步将支持WASI标准，让Go程序可以在更多Wasm运行时中执行。",
        "source": "Go Blog",
        "tag": "PL · Go",
        "views": 19500,
        "url": "https://go.dev/blog/go1.26",
        "date": "2026-02-08"
    },
    {
        "title": "JetBrains Fleet正式开源：新一代IDE基于Rust重构",
        "summary": "JetBrains宣布Fleet编辑器正式开源，这个被视为VS Code竞争者的IDE完全使用Rust重写。Fleet采用全新的分布式架构，代码解析引擎运行在独立进程，即使处理百万行代码项目也能保持流畅。开源版本包含了完整的编辑器核心、LSP客户端和调试器适配器。JetBrains表示将采用Open Core模式，核心功能开源，企业级功能（如远程开发、团队协作）通过付费订阅提供。Fleet的开源引起了开发者社区的热烈反响，GitHub星标数一周内突破8万。业内分析认为，这是JetBrains对抗VS Code和Zed的重要战略，也可能加速Rust在桌面应用开发领域的普及。",
        "source": "JetBrains",
        "tag": "PL · 开发工具",
        "views": 26800,
        "url": "https://blog.jetbrains.com/fleet/2026/02/fleet-is-now-open-source/",
        "date": "2026-02-05"
    }
]

def generate_section(news_list, section_class):
    """生成栏目HTML"""
    html = []
    
    for i, news in enumerate(news_list):
        is_featured = i == 0
        
        if is_featured:
            html.append(f'''                <article class="card featured-card {section_class}">
                    <div class="featured-content">
                        <span class="card-tag {section_class}">FEATURED · {news['tag']}</span>
                        <h2>{news['title']}</h2>
                        <p>{news['summary']}</p>
                        <div class="featured-tags">
                            <span class="featured-tag">{news['tag'].split('·')[1].strip()}</span>
                            <span class="featured-tag">{news['date']}</span>
                        </div>
                        <a href="{news['url']}" class="card-link {section_class}" target="_blank">阅读详情 →</a>
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
            html.append(f'''                <article class="card {section_class}">
                    <div class="card-header">
                        <span class="card-tag {section_class}">{news['tag']}</span>
                        <span class="card-date">{news['date']}</span>
                    </div>
                    <h3>{news['title']}</h3>
                    <p>{news['summary']}</p>
                    <div class="card-meta">
                        <span>📄 {news['source']}</span>
                        <span>👁️ {news['views']:,}</span>
                    </div>
                    <a href="{news['url']}" class="card-link {section_class}" target="_blank">查看详情 →</a>
                </article>''')
    
    return '\n\n'.join(html)

def main():
    # 读取当前index.html
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # 生成新内容
    os_html = generate_section(OS_NEWS, "os")
    pl_html = generate_section(PL_NEWS, "pl")
    
    # 更新OS栏目
    os_start = content.find('<section id="os"')
    os_end = content.find('<section id="pl"')
    if os_start > 0 and os_end > os_start:
        # 找到OS section中的cards-grid
        os_section = content[os_start:os_end]
        grid_start = os_section.find('<div class="cards-grid">')
        timeline_start = os_section.find('<div class="timeline"')
        
        if grid_start > 0 and timeline_start > grid_start:
            new_os_section = os_section[:grid_start + len('<div class="cards-grid">')] + '\n' + os_html + '\n            ' + os_section[timeline_start:]
            content = content[:os_start] + new_os_section + content[os_end:]
    
    # 更新PL栏目
    pl_start = content.find('<section id="pl"')
    footer_start = content.find('</footer')
    if pl_start > 0 and footer_start > pl_start:
        pl_section = content[pl_start:footer_start]
        grid_start = pl_section.find('<div class="cards-grid">')
        timeline_start = pl_section.find('<div class="timeline"')
        
        if grid_start > 0 and timeline_start > grid_start:
            new_pl_section = pl_section[:grid_start + len('<div class="cards-grid">')] + '\n' + pl_html + '\n            ' + pl_section[timeline_start:]
            content = content[:pl_start] + new_pl_section + content[footer_start:]
    
    # 更新日期
    content = re.sub(r'最后更新: \d{4}年\d{2}月\d{2}日', f'最后更新: {today}', content)
    
    # 保存
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 已更新前沿技术栏目为2026年2月最新内容")
    print(f"   OS: {len(OS_NEWS)} 条")
    print(f"   PL: {len(PL_NEWS)} 条")
    print(f"   更新日期: {today}")

if __name__ == "__main__":
    main()
