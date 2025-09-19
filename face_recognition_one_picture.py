import face_recognition

img = face_recognition.load_image_file("faces/user1/user11.jpg")

# 找臉
locs = face_recognition.face_locations(img)
print("找到臉位置:", locs)

# 算 encoding
encs = face_recognition.face_encodings(img, locs)
print("編碼數量:", len(encs))
