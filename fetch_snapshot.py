import requests
from datetime import datetime

indices = {
    "上证指数": "sh000001",
    "深证成指": "sz399001",
    "创业板指": "sz399006",
    "沪深300": "sh000300",
    "中证500": "sh000905",
    "科创50": "sh000688",
    "北证50": "bj899050"
}

def fetch_index(code):
    url = f"https://qt.gtimg.cn/q={code}"
    try:
        res = requests.get(url, timeout=5)
        raw = res.text.split('~')
        price = float(raw[3])
        prev_close = float(raw[4])
        pct_chg = ((price - prev_close) / prev_close) * 100
        pct_chg_str = f"{pct_chg:+.2f}%"
        return f"{price:.2f}", pct_chg_str
    except Exception as e:
        print(f"错误：{code} 抓取失败 - {e}")
        return "获取失败", "--"

# 生成 Markdown 表格格式
lines = []
lines.append("| 指数 | 当前点位 | 涨跌幅 |")
lines.append("|------|-----------|--------|")

for name, code in indices.items():
    price, pct = fetch_index(code)
    lines.append(f"| {name} | {price} | {pct} |")

html_table = "\n".join(lines)
verify_code = "<p>🚀 系统验证口令：我是小龙GPT</p>"

# 构造 HTML 页面
final_html = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>A股指数快照</title>
    <style>
        body {{
            font-family: "Segoe UI", sans-serif;
            background-color: #f7f9fa;
            color: #333;
            padding: 2em;
        }}
        h1 {{
            color: #005aa7;
        }}
    </style>
</head>
<body>
    <h1>A股指数快照（自动更新）</h1>
    <p>更新时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    {verify_code}
    <pre style="line-height: 1.6">{html_table}</pre>
</body>
</html>
"""

# 写入 index.html（GitHub Pages 使用）
with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)
