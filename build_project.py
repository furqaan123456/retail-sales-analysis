"""Retail Sales Analysis: data generation, pandas analysis, dashboard export.
Run: python build_project.py   ->  retail_sales.csv + dashboard.html
Swap the generated CSV for a real dataset (e.g. Superstore) with the same columns."""
import json, numpy as np, pandas as pd

rng = np.random.default_rng(42)
N = 6000
CATALOG = [  # category, product, unit price (INR), cost ratio
    ("Furniture", "Office Chair", 7500, .70), ("Furniture", "Bookcase", 9800, .74),
    ("Furniture", "Standing Desk", 21000, .78), ("Technology", "Wireless Mouse", 900, .55),
    ("Technology", "Laptop Stand", 2200, .60), ("Technology", "Monitor 24in", 11500, .82),
    ("Technology", "Headphones", 3900, .62), ("Office Supplies", "Notebook Pack", 350, .45),
    ("Office Supplies", "Printer Paper", 520, .60), ("Office Supplies", "Marker Set", 280, .40),
]
REGIONS = ["North", "South", "East", "West", "Central"]

pool = pd.date_range("2022-01-01", "2025-12-31")
w = np.asarray((1 + .6 * (pool.month >= 10) + .25 * (pool.month == 3)) * (1 + .15 * (pool.year - 2022)), dtype=float)
dates = rng.choice(pool, N, p=w / w.sum())
pick = rng.integers(0, len(CATALOG), N)
df = pd.DataFrame({
    "order_id": [f"ORD-{100000 + i}" for i in range(N)],
    "order_date": dates,
    "customer_id": [f"C{c:04d}" for c in rng.integers(1, 1201, N)],
    "region": rng.choice(REGIONS, N, p=[.18, .27, .15, .25, .15]),
    "category": [CATALOG[i][0] for i in pick],
    "product": [CATALOG[i][1] for i in pick],
    "quantity": rng.integers(1, 6, N),
    "discount": rng.choice([0, .05, .1, .2, .3], N, p=[.4, .2, .2, .12, .08]),
})
price = np.array([CATALOG[i][2] for i in pick]); cost = np.array([CATALOG[i][3] for i in pick])
df["sales"] = (df.quantity * price * (1 - df.discount)).round(2)
df["profit"] = (df.sales - df.quantity * price * cost).round(2)
df.to_csv("retail_sales.csv", index=False)

# ---- analysis ----
df["month"] = df.order_date.dt.to_period("M").astype(str)
monthly = df.groupby("month")[["sales", "profit"]].sum().round(0).reset_index()
region = df.groupby("region")[["sales", "profit"]].sum().round(0).sort_values("sales", ascending=False).reset_index()
prod = df.groupby("product")[["sales", "profit"]].sum().round(0).sort_values("sales", ascending=False).head(8).reset_index()
cat = df.groupby("category")[["sales", "profit"]].sum().round(0).reset_index()
disc = df.groupby("discount").profit.sum().round(0)
yearly = df.groupby(df.order_date.dt.year).sales.sum()
q4 = df[df.order_date.dt.month >= 10].sales.sum() / df.sales.sum()
tot_s, tot_p = df.sales.sum(), df.profit.sum()
rep = df.groupby("customer_id").order_id.count()
insights = [
    f"{region.region[0]} is the top region with {region.sales[0] / tot_s:.0%} of sales; {region.region.iloc[-1]} is the smallest.",
    f"{prod['product'][0]} is the best-selling product by revenue.",
    f"October to December brings {q4:.0%} of annual sales, and sales grew {yearly.iloc[-1] / yearly.iloc[0] - 1:.0%} from 2022 to 2025.",
    f"Orders with a 30% discount made {disc[.3]:,.0f} in profit versus {disc[0]:,.0f} at no discount, so deep discounts are eroding margin.",
]
data = dict(kpi=dict(sales=tot_s, profit=tot_p, orders=len(df), customers=int(df.customer_id.nunique()),
                     margin=tot_p / tot_s, repeat=float((rep > 1).mean())),
            monthly=monthly.to_dict("list"), region=region.to_dict("list"),
            prod=prod.to_dict("list"), cat=cat.to_dict("list"), insights=insights)

HTML = open("dashboard_template.html").read().replace("__DATA__", json.dumps(data))
open("dashboard.html", "w").write(HTML)
print("\n".join(insights))
