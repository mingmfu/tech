#!/bin/bash
# AI科技前沿网站每日自动更新脚本
# 使用 ai-news-digest 技能方式获取新闻

cd ~/tech

echo "🚀 开始更新 AI 科技前沿网站..."
echo "⏰ 更新时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "🔧 使用 ai-news-digest 技能获取新闻..."

# 使用 ai-news-digest 方式更新
python3 update_with_ai_news_digest.py

# 推送到 GitHub
echo "📤 正在推送到 GitHub..."
git add -A
git commit -m "📰 每日更新: $(date '+%Y-%m-%d') | ai-news-digest"
git push origin main

echo "✅ 网站更新完成！"
echo "🌐 访问地址: https://mingmfu.github.io/tech/"
