import cv2
import os

cap = cv2.VideoCapture(os.path.join('frames', f'%08d.jpg'), cv2.CAP_IMAGES)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('frame', frame)
    cv2.waitKey(1) # 1ミリ秒待つ
