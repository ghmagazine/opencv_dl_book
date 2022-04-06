import numpy as np
import cv2

# 画像ファイルをカラーで読み込み
img1 = cv2.imread('yorkie.png', cv2.IMREAD_COLOR)
img2 = cv2.imread('yorkie_flip_0.png', cv2.IMREAD_COLOR)

# 画像を垂直方向に連結
vconcat_img = cv2.vconcat([img1, img2])

cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.imshow('vconcat_img', vconcat_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
