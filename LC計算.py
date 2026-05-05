import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# 【步驟 A】定義分析機器
def calculate_lc_probit(file_path):
    xl = pd.ExcelFile(file_path)
    all_sheet = xl.sheet_names
    summary_list = []
    for name in all_sheet:
        try:
            # 1. 讀取與清理 (確保資料是乾淨的)
            df = pd.read_excel(file_path, sheet_name=name)
            df = df.dropna(subset=['Dose', 'Alive', 'Dead'])
            
            # 2. 數據換算 (同步 R 語言邏輯)
            df['Conc'] = 1 / df['Dose']           # 轉濃度
            df['Log_Conc'] = np.log10(df['Conc']) # 取對數
            
            # 3. 建立矩陣 (這是為了把「權重」放進去)
            # 把死掉跟活著的並排，告訴電腦：總數 = Dead + Alive
            y = np.column_stack((df['Dead'], df['Alive']))
            x = sm.add_constant(df['Log_Conc']) 
            
            # 4. 核心運算 (Probit 迴歸)
            model = sm.GLM(y, x, family=sm.families.Binomial(sm.families.links.probit()))
            result = model.fit()
            
            # 5. 提取計算結果
            intercept, slope = result.params
            lc50_log = -intercept / slope
            lc50_conc = 10**lc50_log
            
            # 6. 計算 LC95 (常態分佈 z-score 為 1.645)
            lc95_log = (1.64485 - intercept) / slope
            lc95_conc = 10**lc95_log

            # --- 輸出結果到螢幕 ---
            print(f"✅ 分析成功！")
            print(f"LC50 (濃度): {lc50_conc:.6f}")
            print(f"LC50 (稀釋倍數): {1/lc50_conc:.2f}")
            print(f"LC95 (濃度): {lc95_conc:.6f}")
            print(f"LC95(稀釋倍數): {1/lc95_conc:.2f}")

            # 7. 自動存檔報告 (工程師的自動化精神)
            today = pd.Timestamp.now().strftime('%Y-%m-%d')
            summary_list.append({
                '地區': name,                  # 這是分頁名稱
                'LC50_濃度': lc50_conc,        # 第一個數值結果
                'LC95_濃度': lc95_conc,        # 第二個數值結果
                'LC50_倍數': 1/lc50_conc,      # 第三個數值結果
                'LC95_倍數': 1/lc95_conc,      # 第四個數值結果
                '分析日期': today
            })
        except Exception as e:
            # 【步驟 B】防錯機制：如果出錯，告訴我原因
            print(f"❌ 發生錯誤了！請檢查：{e}")
    # 2. 【核心重點】這個存檔動作必須在 for 迴圈外面 (縮排跟 for 一樣)
    if summary_list:
        output_df = pd.DataFrame(summary_list)
        output_name = file_path.replace('.xlsx', '_全分頁匯總結果.xlsx')
        output_df.to_excel(output_name, index=False)
        print(f"📂 匯總完畢！共處理 {len(summary_list)} 個分頁。")

# 【步驟 C】設定路徑與啟動
target_file = r"C:\Users\nmbdcrc\Desktop\藥效分析專案\data\中西區LC50.xlsx"
calculate_lc_probit(target_file)