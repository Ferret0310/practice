import pandas as pd

data = {
    "區域": ["仁德區", "歸仁區", "永康區", "東區"],
    "數量": [15, 45, 120, 30],
    "陽性": ["否", "是", "是", "否"]
}
test_df = pd.DataFrame(data)
test_df["風險"] = test_df["數量"] * 10
danger_zone = test_df[test_df["風險"] > 50]
danger_zone_sort = danger_zone.sort_values(by="風險",ascending=False)
print(danger_zone_sort)
