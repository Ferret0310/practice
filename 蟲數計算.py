import pandas as pd

# 1. 讀取 Excel 檔案
# 記得把檔案放在跟程式碼同一個資料夾
df = pd.read_excel(r"C:\Users\nmbdcrc\Desktop\養蟲組.xlsx")

def data_check(year,city):
    result = df[(df["年"] == year) & (df["縣市"] == city)]
    return result
my_data = data_check(2020,"台南")
print(my_data)



