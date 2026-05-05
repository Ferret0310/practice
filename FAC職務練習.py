import pandas as pd

data = {
    'Status': ['Run', 'Run', 'Run', 'Idle'],
    'Pressure': [3.5, 4.2, 3.8, 5.0],
    'Vibration': [0.5, 0.9, 0.9, 1.2]
}
df = pd.DataFrame(data)

def check_machine (s,p,v):
    if s == "Idle":
        return f"機台待機中，無需監控"
    if p > 4.0 and v > 0.8:
        return f"緊急停機：請立刻檢查！"
    elif p > 4.0 or v >0.8:
        return f"預警：數值偏高"
    else:
        return f"運作正常"
df["回報"] = df.apply(lambda row:check_machine(s = row["Status"],p = row["Pressure"],v = row["Vibration"]),axis=1)
print(df["回報"])