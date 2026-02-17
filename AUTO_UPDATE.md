# TechInsight Hub - 自动更新系统

## 🔄 每日自动更新（已配置真实数据源）

网站已配置 GitHub Actions 自动更新，每天北京时间 **10:00** 自动从以下数据源获取最新内容：

### 📡 数据源

| 数据源 | 类型 | 内容 | API状态 |
|--------|------|------|---------|
| **Hacker News** | 社区 | AI相关热门讨论 | 🆓 免费，无需认证 |
| **arXiv** | 学术 | AI/ML最新论文 | 🆓 免费，无需认证 |
| **GitHub** | 开源 | Trending AI项目 | 🆓 免费，有频率限制 |

### 🕐 定时任务

```
每天 10:00 (北京时间)
    ↓
获取 Hacker News AI热点
    ↓
获取 arXiv 最新论文
    ↓
获取 GitHub Trending项目
    ↓
更新 index.html
    ↓
提交到 GitHub
    ↓
自动部署到 GitHub Pages
```

## 🎮 使用方法

### 自动运行（推荐）
无需操作，每天自动更新。

### 手动触发更新
1. 进入 GitHub 仓库
2. 点击 **Actions** 标签
3. 选择 **Daily Content Update (Production)**
4. 点击 **Run workflow**

### 本地测试
```bash
cd ~/tech

# 安装依赖
pip3 install requests

# 运行数据获取
python3 scripts/fetch_real_data.py

# 查看获取的数据
cat daily_content.json
```

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `.github/workflows/daily-update.yml` | GitHub Actions 工作流 |
| `scripts/fetch_real_data.py` | 数据获取脚本 |
| `daily_content.json` | 每日获取的数据缓存 |
| `AUTO_UPDATE.md` | 本文档 |

## ⚙️ 高级配置

### 修改定时时间

编辑 `.github/workflows/daily-update.yml`：

```yaml
on:
  schedule:
    # 分 时 日 月 周 (UTC时间)
    # 当前: 每天 UTC 02:00 = 北京时间 10:00
    - cron: '0 2 * * *'
    
    # 改为北京时间 08:00
    # - cron: '0 0 * * *'
    
    # 改为每小时更新
    # - cron: '0 * * * *'
```

### 自定义关键词

编辑 `scripts/fetch_real_data.py`：

```python
# Hacker News 关键词
AI_KEYWORDS = [
    'AI', 'artificial intelligence', 'machine learning',
    'LLM', 'GPT', 'Claude', 'OpenAI', 'DeepSeek',
    # 添加你自己的关键词...
    '你的关键词'
]

# arXiv 分类
CATEGORIES = [
    'cs.AI', 'cs.LG', 'cs.CL', 'cs.CV',
    # 添加更多分类...
    'cs.RO'  # 机器人学
]
```

### 添加更多数据源

在 `scripts/fetch_real_data.py` 中添加新的Fetcher类：

```python
class RedditFetcher(DataFetcher):
    """Reddit AI社区获取"""
    def fetch(self):
        # 实现Reddit API调用
        pass

class TwitterFetcher(DataFetcher):
    """Twitter/X AI话题获取"""
    def fetch(self):
        # 实现Twitter API调用
        pass
```

## 🚨 故障排除

### 更新失败

检查 GitHub Actions 日志：
1. 进入仓库 → Actions
2. 查看失败的 workflow run
3. 查看具体错误信息

### 数据源返回空结果

这是正常现象，原因可能：
- **Hacker News**: 当天可能没有足够的AI热门话题
- **arXiv**: 周末和假期论文较少
- **GitHub**: API频率限制（每小时60次）

系统会自动使用备用内容填充。

### 添加API密钥（可选）

如果需要更高的API调用限额：

1. 获取API密钥：
   - GitHub: Settings → Developer settings → Personal access tokens
   - 其他服务: 对应平台的开发者设置

2. 添加到GitHub Secrets：
   - 仓库 → Settings → Secrets and variables → Actions
   - 添加 `GITHUB_TOKEN` 或其他密钥

3. 在工作流中使用：
```yaml
- name: Fetch data
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: python3 scripts/fetch_real_data.py
```

## 📊 更新日志格式

自动提交的信息格式：
```
📰 Daily update: 2026-02-17

Data sources:
- Hacker News (3 AI stories)
- arXiv (5 papers)
- GitHub (2 repositories)
```

## 🔒 隐私和合规

- 所有数据源均为**公开API**
- 不存储任何用户个人信息
- 遵守各平台的API使用条款
- 数据仅用于展示，不用于商业目的

## 💡 提示

- 第一次运行可能需要几分钟获取数据
- 如果某数据源暂时不可用，系统会自动跳过
- 可以通过 `daily_content.json` 查看原始获取的数据
- 网站架构和样式会**保持不变**，只更新内容

---

**上次配置更新**: 2026-02-17
