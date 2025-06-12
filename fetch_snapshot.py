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

lines = []
lines.append("# A股指数快照（自动更新）\n")
lines.append(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
lines.append("\n| 指数 | 当前点位 | 涨跌幅 |\n|------|-----------|--------|")

for name, code in indices.items():
    price, pct = fetch_index(code)
    print(f"{name}: {price} / {pct}")
    lines.append(f"| {name} | {price} | {pct} |")

from datetime import datetime

# 假设你已经生成了 data 表格 markdown 形式，如 final_md

# 生成 HTML 页面内容（index.html）
final_html = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A股指数快照</title>
    <style>
        body {{
            font-family: "SF Pro SC", "Segoe UI", sans-serif;
            background-color: #f7f9fa;
            color: #333;
            padding: 2em;
        }}
        h1 {{
            color: #005aa7;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 1em;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 0.5em 1em;
            text-align: center;
        }}
        th {{
            background-color: #eaeaea;
        }}
    </style>
</head>
<body>
    <h1>A股指数快照（自动更新）</h1>
    <p>更新时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    {final_md.replace('\n', '<br>')}
</body>
</html>
"""

# 写入 index.html（供 GitHub Pages 展示）
with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)
