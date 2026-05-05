import pandas as pd
df = pd.read_excel("2022各區LC50.xlsx")
# 看前幾筆資料
print(df.head())

# 看欄位名稱
print(df.columns)

# 基本統計
print(df.describe())

df["concentration"] = 1 / df["Dose"]
df_group = df.groupby("Dose").sum()
df_group["Total"] = df_group["Alive"] + df_group["Dead"]
df_group["死亡率"] = df_group["Dead"] / df_group["Total"]
df_group = df_group.sort_values(by="死亡率")
print(df_group)
import matplotlib.pyplot as plt
df_group = df_group.sort_values(by="concentration")
# 用 concentration 當 x（比較合理）
x = df_group["concentration"]
y = df_group["死亡率"]

plt.scatter(x, y)
plt.plot(x, y)

plt.xlabel("concentration")
plt.ylabel("Mortality")
plt.title("Dose-Response Curve")

plt.show()
