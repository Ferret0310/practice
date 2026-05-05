# 1. 第一行輸入：告訴電腦總共要做幾次 (範例輸入的 3)
n = int(input()) 

# 2. 準備一個空盒子 (戶口名簿)
household_register = []

# 3. 開始跑迴圈，跑 n 次
for _ in range(n):
    # 讀取輸入。範例中每一筆前面有個 1 (代表新增動作)
    # 我們用 split() 把那一長串字拆開
    data = input().split() 
    
    # 檢查是不是要「新增」(如果第一個數字是 1)
    if data[0] == "1":
        # 抓出後面的名字、編號、顏色
        name = data[1]
        id_num = data[2]
        color = data[3]
        
        # 存進盒子裡 (就像你存 LC50 一樣)
        household_register.append({
            "Name": name,
            "ID": id_num,
            "Color": color
        })

# 4. 最後印出來檢查看看
print("目前的戶口名簿內容：")
for person in household_register:
    print(person)