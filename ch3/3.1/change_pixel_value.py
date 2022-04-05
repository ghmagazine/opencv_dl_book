import cv2

# 画像ファイルをカラーで読み込み
img = cv2.imread('yorkie.png', cv2.IMREAD_COLOR)
x = 200
y = 100
channel = 0

print(f'before: bgr_val({x}, {y}) = {img[y, x]}')

# (x, y) = (200, 100)の画素値を代入（Blue、Green、Redチャンネル）
img[y, x] = [255, 255, 255]
print(f'after: bgr_val({x}, {y}) = {img[y, x]}')

print(f'before: b_val({x}, {y}) = {img[y, x, channel]}')

# 0番目のチャンネル（＝Blueチャンネル）の(x, y) = (200, 100)の画素値を代入
img[y, x, channel] = 0
print(f'after: b_val({x}, {y}) = {img[y, x, channel]}')
