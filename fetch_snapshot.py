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
        price = raw[3]
        pct_chg = raw[5]
        if not pct_chg.startswith("-"):
            pct_chg = f"+{pct_chg}"
        return price, pct_chg
    except:
        return "获取失败", "--"

# 生成 Markdown
lines = []
lines.append("# A股指数快照（自动更新）\n")
lines.append(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
lines.append("\n| 指数 | 当前点位 | 涨跌幅 |")
lines.append("|------|-----------|--------|")

for name, code in indices.items():
    price, change = fetch_index(code)
    lines.append(f"| {name} | {price} | {change}% |")

with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
