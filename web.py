import streamlit as st
import pandas as pd
import os
file_path = "養蟲組.xlsx"
# 1. 讀取資料
df = pd.read_excel(file_path)

st.title("蚊蟲實驗自動化查詢系統")

# 2. 建立側邊欄篩選器 (自動生成下拉選單)
year = st.sidebar.selectbox("請選擇年度", df["年度"].unique())
city = st.sidebar.selectbox("請選擇縣市", df["縣市"].unique())

# 3. 套用你原本寫的篩選邏輯
result = df[(df["年"] == year) & (df["縣市"] == city)]

# 4. 顯示結果
st.write(f"篩選出 {year} 年，{city} 的實驗紀錄：")
st.dataframe(result)

