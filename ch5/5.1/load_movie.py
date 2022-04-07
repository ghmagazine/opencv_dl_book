import cv2

cap = cv2.VideoCapture('test.mp4')
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('frame', frame)
    cv2.waitKey(1) # 1ミリ秒待つ
