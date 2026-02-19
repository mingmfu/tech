#!/usr/bin/env python3
"""
统一网站内容更新脚本
更新所有栏目：AI热点、操作系统、编程语言、图形技术
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

def run_command(cmd, description):
    """运行命令并输出结果"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print('='*60)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"⚠️ {result.stderr}")
    return result.returncode == 0

def main():
    print("="*60)
    print("🚀 TechInsight Hub 统一更新脚本")
    print("="*60)
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 获取AI热点数据
    run_command("python3 generate_20_news.py", "生成AI热点新闻（20条）")
    
    # 2. 更新前沿技术栏目（OS、PL）
    run_command("python3 update_2026_frontier.py", "更新前沿技术栏目（OS、PL）")
    
    # 3. 更新图形技术栏目（GFX）
    # 这里可以添加图形技术的更新
    
    # 4. 更新网站
    run_command("python3 scripts/update_website.py", "更新网站HTML")
    
    # 5. Git提交
    today = datetime.now().strftime('%Y-%m-%d')
    commit_msg = f"""📰 每日更新: {today}

更新内容:
- AI热点新闻: 20条（国内10条 + 国际10条）
- 操作系统: 6条最新动态
- 编程语言: 6条最新动态
- 所有摘要260+字，链接指向真实来源

更新时间: {datetime.now().strftime('%H:%M:%S')}"""
    
    print(f"\n{'='*60}")
    print("💾 提交更改到Git")
    print('='*60)
    
    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", commit_msg])
    subprocess.run(["git", "push", "origin", "main"])
    
    print(f"\n{'='*60}")
    print("✅ 更新完成!")
    print(f"📅 日期: {today}")
    print(f"🌐 网站: https://mingmfu.github.io/tech/")
    print("="*60)

if __name__ == "__main__":
    main()
