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

with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
