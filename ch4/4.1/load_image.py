import cv2

# 画像を読み込む
img = cv2.imread('test.jpg')

# 画像を表示する
cv2.imshow('image', img)

# waitKey()を使って待たないとウィンドウがすぐ閉じてしまう
cv2.waitKey(0)

