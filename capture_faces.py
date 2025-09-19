import cv2
import os

# 輸入名稱 (例如 alice, bob)
name = input("請輸入名字: ").strip()

# 設定存檔資料夾
save_dir = f"faces/{name}"
os.makedirs(save_dir, exist_ok=True)

# 開啟攝影機 (改成正確的 /dev/videoX)
cap = cv2.VideoCapture("/dev/video0")

if not cap.isOpened():
    print("❌ 無法開啟攝影機")
    exit()

count = 0
while count < 10:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ 無法讀取影像")
        break

    filename = os.path.join(save_dir, f"{name}{count+1}.jpg")
    cv2.imwrite(filename, frame)
    print(f"✅ 已存檔: {filename}")
    count += 1

    # 每次拍照間隔一秒
    cv2.waitKey(2000)

cap.release()
print("📸 拍攝完成！")
