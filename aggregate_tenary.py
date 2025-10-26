# aggregate_ternary.py
# Aggregates Supabase CSV -> combined ternary plot + Excel copy

import pandas as pd
import plotly.express as px

# 1) Load your exported CSV
df = pd.read_csv("responses.csv")  # rename if needed

# 2) Basic cleaning/validation
req_cols = {"plot_type","a","b","c"}
assert req_cols.issubset(df.columns), f"CSV missing columns: {req_cols - set(df.columns)}"
df = df[df["plot_type"].isin(["present","2075"])].copy()

# 3) Build a single ternary scatter with color by period
fig = px.scatter_ternary(
    df,
    a="a", b="b", c="c",
    color="plot_type",
    symbol="plot_type",
    hover_data={"a":":.0f","b":":.0f","c":":.0f","plot_type":True},
    labels={"a":"Public Safety","b":"Civil Liberties","c":"Accountability & Transparency","plot_type":""},
    title="Veritas AI Values — Present vs 2075 (All Responses)"
)

# 4) Save figure and an Excel copy of the dataset
fig.write_image("aggregated_plot.png", scale=2)  # needs kaleido: pip install -U kaleido
fig.write_html("aggregated_plot.html", include_plotlyjs="cdn")  # handy for your report appendix
df.to_excel("responses.xlsx", index=False)

print("Done: aggregated_plot.png, aggregated_plot.html, responses.xlsx")
