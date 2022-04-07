import cv2

# test.png を読み込む
img_bgr = cv2.imread('veggie.png')

# グレイスケールの画像に変換する
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# 画像の表示
cv2.imshow('BGR', img_bgr)
cv2.imshow('GRAY', img_gray)

# BGRからHSVへの変換
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
cv2.imshow('HSV', img_hsv)


# HSVの3チャンネル画像をH,S,Vの3枚の画像に分解する
h, s, v = cv2.split(img_hsv)

# 3枚を横に連結して表示
cv2.imshow('H,S,V', cv2.hconcat([h, s, v]))
cv2.waitKey(0)
