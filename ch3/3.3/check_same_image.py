import numpy as np
import cv2

# 画像データの内容が同一かをチェックする
def is_same_image(img1, img2):
    # 差分の絶対値を計算する
    diff = cv2.absdiff(img1, img2)
    # 画素値が非ゼロの画素数をカウントして、0ならTrue、そうでなければFalseを返す
    return (cv2.countNonZero(diff) == 0)

width = 200
height = 100
value1 = 128
value2 = 255

# img1は画素値として128を持ち、img2は画素値として255を持つ
img1 = np.full((height, width), value1, np.uint8)
img2 = np.full((height, width), value2, np.uint8)

# 画像データの内容が同一であるため、Trueとなる
print(is_same_image(img1, img1))

# 画像データの内容が異なるため、Falseとなる
print(is_same_image(img1, img2))
