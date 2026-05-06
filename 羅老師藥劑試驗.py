import streamlit as st
import pandas as pd
import os
file_path = "羅老師藥劑試驗.xlsx"
# 1. 讀取資料
df = pd.read_excel(file_path)

st.title("羅老師藥劑實驗查詢系統")
unique_pesticides = df["藥劑"].unique().tolist()
all_pesticides = ["全部"] + unique_pesticides
# 2. 建立側邊欄篩選器 (自動生成下拉選單)
year = st.sidebar.selectbox("請選擇年度", df["年"].unique())
pesticides = st.sidebar.selectbox("請選擇藥劑",all_pesticides)

# 3. 套用你原本寫的篩選邏輯
result = df[(df["年"] == year)]
if pesticides != "全部":
    result = result[result["藥劑"] == pesticides]

count = len(result)
# 4. 顯示結果
st.write(f"篩選出 {year} 年，所用藥劑，共{count}筆。")
st.dataframe(result.reset_index(drop=True),hide_index=True, use_container_width=True)