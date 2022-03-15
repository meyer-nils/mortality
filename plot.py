import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

files = [
    "sonderauswertung-sterbefaelle.xlsx",
    "sonderauswertung-sterbefaelle-endgueltige-daten.xlsx",
]
sheets = ["D_2016_2022_Tage", "D_2000_2015_Tage"]

# Read dataframes from file
dfs = []
for file, sheet in zip(files, sheets):
    dfs.append(
        pd.read_excel(
            file,
            sheet_name=sheet,
            skiprows=8,
            index_col=0,
            header=0,
            dtype=float,
            usecols=lambda x: "29.02." not in x,
        )
    )

# Combine and clean dataframes
df = pd.concat(dfs)
df = df.T
df.drop(df.tail(1).index, inplace=True)
df.reset_index(inplace=True)

# Compute radians for polar plot
df["angle"] = df.index * 2 * np.pi / 365.0

# Plot
ax = plt.subplot(111, projection="polar")
for year in range(2000, 2019):
    brightness = 0.5 * (year - 2000) / 20
    ax.plot(df["angle"], df[year], "-", color=str(brightness))
for year in [2019, 2020, 2021, 2022]:
    ax.plot(df["angle"], df[year], linewidth=3, label=year)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_rlabel_position(200)
ax.set_xticks(np.linspace(0, 2 * np.pi, 13))
ax.set_xticklabels([f"01.{month}." for month in range(1, 13)] + [""])
ax.set_title("Daily mortality in Germany")
ax.legend(bbox_to_anchor=(1.1, 1.1))
plt.savefig("mortality.png")
