import numpy as np
import cv2

width = 200
height = 100
value = 128

# width=200、height=100、画素値0で埋めたグレースケール画像を生成
img1 = np.zeros((height, width), np.uint8)

# width=200、height=100、画素値128で埋めたグレースケール画像を生成
img2 = np.full((height, width), value, np.uint8)

# 画像をウィンドウ表示する
cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
