import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def calculate_lc_probit(file_path):
    xl = pd.ExcelFile(file_path)
    all_sheet = xl.sheet_names
    summary_list = []

    for name in all_sheet:
        try:
            print(f"\n📊 正在分析：{name}")

            # 1️⃣ 讀資料
            df = pd.read_excel(file_path, sheet_name=name)
            df = df.dropna(subset=['Dose', 'Alive', 'Dead'])

            # 2️⃣ 資料轉換
            df['Conc'] = 1 / df['Dose']
            df['Log_Conc'] = np.log10(df['Conc'])
            df['Mortality'] = df['Dead'] / (df['Dead'] + df['Alive'])

            # 3️⃣ 建立模型
            y = np.column_stack((df['Dead'], df['Alive']))
            x = sm.add_constant(df['Log_Conc'])

            model = sm.GLM(y, x, family=sm.families.Binomial(sm.families.links.probit()))
            result = model.fit()

            # 4️⃣ 計算 LC50 / LC95
            intercept, slope = result.params
            lc50_log = -intercept / slope
            lc50 = 10**lc50_log

            lc95_log = (1.64485 - intercept) / slope
            lc95 = 10**lc95_log

            print(f"LC50: {lc50:.6f}")
            print(f"LC95: {lc95:.6f}")

            # 5️⃣ 畫圖（升級重點🔥）
            plt.figure()

            # 原始資料點
            plt.scatter(df['Log_Conc'], df['Mortality'], label='Observed')

            # 模型預測線
            x_range = np.linspace(df['Log_Conc'].min(), df['Log_Conc'].max(), 100)
            x_pred = sm.add_constant(x_range)
            y_pred = result.predict(x_pred)

            plt.plot(x_range, y_pred, color='red', label='Probit Fit')

            # LC50線
            plt.axhline(0.5, linestyle='--', label='LC50')
            plt.axvline(lc50_log, linestyle='--')

            plt.xlabel('Log Concentration')
            plt.ylabel('Mortality')
            plt.title(f'{name} Dose-Response')
            plt.legend()
            plt.show()

            # 6️⃣ AI簡單預測（升級🔥）
            if 'Year' in df.columns:
                model_ml = LinearRegression()
                X = df[['Year']]
                y_ml = df['Log_Conc']

                model_ml.fit(X, y_ml)

                future_year = np.array([[2026]])
                pred = model_ml.predict(future_year)

                print(f"📈 預測2026抗藥性(log): {pred[0]:.4f}")

            # 7️⃣ 存結果
            summary_list.append({
                '地區': name,
                'LC50': lc50,
                'LC95': lc95
            })

        except Exception as e:
            print(f"❌ 錯誤：{e}")

    # 8️⃣ 匯總輸出
    if summary_list:
        output_df = pd.DataFrame(summary_list)
        output_df.to_excel('summary.xlsx', index=False)
        print("\n📂 已輸出 summary.xlsx")

# 啟動
file_path = input("請輸入Excel檔案路徑：")
calculate_lc_probit(file_path)