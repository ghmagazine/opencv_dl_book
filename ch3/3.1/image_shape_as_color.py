import cv2

# 画像ファイルをカラーで読み込み
img = cv2.imread('yorkie.png', cv2.IMREAD_COLOR)

# shape（ndarrayの形状）、dtype（画素のデータ型）を表示する
print(f'shape = {img.shape}')
print(f'dtype = {img.dtype}')
