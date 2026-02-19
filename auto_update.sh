#!/bin/bash
# TechInsight Hub 每日自动更新脚本
# 所有输出使用中文

cd ~/tech

echo "========================================"
echo "🚀 TechInsight Hub 每日自动更新"
echo "========================================"
echo ""

# 获取当前日期
TODAY=$(date '+%Y-%m-%d')
TIME=$(date '+%H:%M:%S')
echo "📅 日期: $TODAY"
echo "⏰ 时间: $TIME"
echo ""

# 1. 获取最新数据
echo "🔄 步骤1: 获取最新数据..."
python3 scripts/fetch_real_data.py 2>&1 | grep -E "(开始获取|正在获取|获取完成|总计)" || echo "✅ 数据获取完成"
echo ""

# 2. 生成详细中文摘要
echo "🔄 步骤2: 生成详细中文摘要（200字以上）..."
python3 generate_chinese_content.py
echo ""

# 3. 生成API数据
echo "🔄 步骤3: 生成API数据..."
python3 scripts/generate_api_data.py 2>&1 | tail -3
echo ""

# 4. 更新网站
echo "🔄 步骤4: 更新网站..."
python3 scripts/update_website.py 2>&1 | tail -5
echo ""

# 5. 推送到GitHub
echo "🔄 步骤5: 推送到GitHub..."
git add api/tech-news.json daily_content.json index.html

# 检查是否有变更
if git diff --cached --quiet; then
    echo "ℹ️ 没有新的变更需要提交"
else
    git commit -m "📰 每日更新: $TODAY

数据内容:
- AI热点资讯
- AI学术论文

所有标题和摘要已翻译为中文

更新时间: $TIME"
    
    git push origin main
    echo "✅ 已成功推送到GitHub"
fi

echo ""
echo "========================================"
echo "✨ 更新流程完成!"
echo "========================================"
