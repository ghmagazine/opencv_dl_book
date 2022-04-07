import cv2
import numpy as np
from matplotlib import pyplot as plt

# 元の画像
img = cv2.cvtColor(cv2.imread('drivecam.jpg'), cv2.COLOR_BGR2GRAY)
cv2.imshow('1. original', img)

# パラメータ
block_size = 15
c = 25

# 画像をぼかす
blur_img = cv2.GaussianBlur(img, (block_size, block_size), 0)
cv2.imshow('2. blur', blur_img)

# ぼかした画像とぼかす前の画像の差分をとる
diff_img = blur_img - img
cv2.imshow('3. diff', diff_img)

# 差がcより大きいか否かで白か黒かを決める
result_img = np.where(blur_img - c > img, 0, 255)
cv2.imshow('4. result', result_img.astype(np.uint8))

cv2.waitKey(0)
