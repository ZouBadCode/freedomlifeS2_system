from datetime import datetime

# 假設您有一個日期時間字符串
date_str = "2023-03-04 12:00:00"

# 將字符串轉換為 datetime 對象
date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

# 現在您可以與另一個 datetime 對象進行比較了
other_date_obj = datetime(2023, 3, 4, 13, 0, 0)

# 進行比較
if date_obj <= other_date_obj:
    print(date_obj,other_date_obj)
    print("date_obj 是在 other_date_obj 之前或相同的時間")
else:
    print("date_obj 是在 other_date_obj 之後的時間")
    print(date_obj,other_date_obj)
