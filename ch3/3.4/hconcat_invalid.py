import numpy as np
import cv2

# width=200、height=100、画素値0で埋めたグレースケール画像を生成
width1 = 200
height1 = 100
img1 = np.zeros((height1, width1), np.uint8)

# 画像を水平方向に連結（画像1と画像2の高さが同じなので正常に結合できる）
concat1 = cv2.hconcat([img1, img1])
print(f'concat1.shape = {concat1.shape}')

# width=200、height=200、画素値0で埋めたグレースケール画像を生成
width2 = 200
height2 = 200
img2 = np.zeros((height2, width2), np.uint8)

# 画像を水平方向に連結（画像1と画像2の高さが異なるのでエラーになる）
concat2 = cv2.hconcat([img1, img2])
print(f'concat2.shape = {concat2.shape}')
