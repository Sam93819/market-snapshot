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

def get_index_price(code):
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        res = requests.get(url, timeout=10)
        raw = res.text.split('~')
        name = raw[1]
        price = raw[3]
        change = raw[4]
        pct = raw[5]
        return f"{price}（{pct}%）"
    except:
        return "获取失败"

lines = []
lines.append(f"# A股指数快照（自动更新）\n")
lines.append(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
lines.append("\n| 指数 | 当前点位 |\n|------|-----------|")

for name, code in indices.items():
    val = get_index_price(code)
    lines.append(f"| {name} | {val} |")

# 输出到 README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write('\n'.join(lines))
