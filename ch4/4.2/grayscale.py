import cv2

# test.png を読み込む
img_bgr = cv2.imread('veggie.png')

# グレースケールの画像に変換する
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# 画像の表示
cv2.imshow('BGR', img_bgr)
cv2.imshow('GRAY', img_gray)
cv2.waitKey(0)
