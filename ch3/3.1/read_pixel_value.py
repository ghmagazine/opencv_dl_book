import numpy as np
import cv2

# 画像ファイルをカラーで読み込み
img = cv2.imread('yorkie.png', cv2.IMREAD_COLOR)

x = 200
y = 100
channel = 0

# 座標値(x, y) = (200, 100)の画素値を参照（Blue、Green、Red）
# 座標値指定がy、xの順になっている点に注意
bgr_val = img[y, x]
print(f'bgr_val({x}, {y}) = {bgr_val}')

# 0番目のチャンネル（＝Blue）の(x, y) = (200, 100)の画素値を参照
# 座標値指定がy、xの順になっている点に注意
b_val = img[y, x, channel]
print(f'b_val({x}, {y}) = {b_val}')
