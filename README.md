# TechInsight Hub

一个专注于 **AI、计算机图形、操作系统、编译器与编程语言** 领域前沿技术洞察的静态网站。

![TechInsight Hub](screenshot.png)

## 🌟 特色

- **🤖 AI 前沿** - LLM、多模态、Agent、AI Agent 系统最新研究
- **🎨 计算机图形** - 3D Gaussian Splatting、光线追踪、神经渲染
- **🖥️ 操作系统** - eBPF、Rust for Linux、云原生虚拟化
- **⚡ 编译器与编程语言** - MLIR、Rust、类型系统、GC 优化

## 🚀 快速使用

### 方式一：直接打开
双击 `index.html` 文件，即可在浏览器中预览。

### 方式二：本地服务器（推荐）
```bash
cd tech-insight-hub

# Python 3
python -m http.server 8080

# Node.js
npx serve .

# 或使用 VS Code Live Server 插件
```

访问 http://localhost:8080

### 方式三：部署到 GitCode Pages
```bash
# 1. 创建 GitCode 仓库并上传文件
# 2. 开启 Pages 功能
# 3. 访问 https://用户名.gitcode.io/仓库名
```

## 📁 文件结构

```
tech-insight-hub/
├── index.html          # 主文件（所有内容集成）
├── README.md           # 本文件
└── screenshot.png      # 截图（可选）
```

## 🎨 设计特点

- **深色主题** - 护眼的暗色系设计
- **响应式布局** - 完美适配手机、平板、桌面
- **单页应用体验** - Tab 切换，无刷新浏览
- **代码高亮** - 精心设计的语法预览区
- **渐变配色** - 每个领域独特的色彩标识

## 📝 内容来源

| 领域 | 主要来源 |
|------|----------|
| AI | arXiv (cs.AI, cs.LG, cs.CL), OpenAI, DeepSeek |
| 图形 | SIGGRAPH, CVPR, NVIDIA, Unreal Engine |
| OS | USENIX, Linux Kernel, eBPF Community |
| 编译器/PL | PLDI, POPL, LLVM, Rust Lang |

## 🔄 更新内容

要更新网站内容，编辑 `index.html` 文件中的相应 section：

```html
<section id="ai" class="section active">
    <!-- 添加新的 card -->
    <article class="card ai">
        ...
    </article>
</section>
```

## 🛠️ 技术栈

- **纯 HTML5** - 无需构建工具
- **CSS 变量** - 主题配色系统
- **原生 JavaScript** - 轻量交互
- **Google Fonts** - Inter + JetBrains Mono

## 📱 浏览器支持

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🔮 未来增强（可选）

- [ ] 添加 RSS 订阅功能
- [ ] 接入自动化脚本获取最新论文
- [ ] 添加搜索功能
- [ ] 暗黑/明亮模式切换
- [ ] 添加评论系统

## 📄 License

MIT License - 自由使用和修改

---

**Enjoy exploring the tech frontier!** 🚀