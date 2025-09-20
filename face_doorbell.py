import cv2
import face_recognition
import os

# Step 1: 載入已知人臉
known_encodings = []
known_names = []

faces_dir = "faces"

for name in os.listdir(faces_dir):
    person_dir = os.path.join(faces_dir, name)
    if not os.path.isdir(person_dir):
        continue
    for file in os.listdir(person_dir):
        img_path = os.path.join(person_dir, file)
        img = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(img)
        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(name)

print("已載入人臉數量:", len(known_encodings))

# Step 2: 開啟攝影機
cap = cv2.VideoCapture(0)
print("[INFO] 開始辨識，按 q 離開...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] 攝影機讀取失敗")
        break

    # 縮小影像加速
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = small_frame[:, :, ::-1]  # BGR → RGB

    # Step 3: 偵測人臉
    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(
        rgb_small.astype("uint8"),  # 確保型態正確
        face_locations,
        num_jitters=1
    )

    # Step 4: 比對
    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
        if True in matches:
            matched_idx = matches.index(True)
            name = known_names[matched_idx]
            print(f"成功辨識：{name}")
        else:
            print("辨識失敗：未知訪客")

cap.release()
cv2.destroyAllWindows()
