import numpy as np
import cv2

img = np.array([[1, 2, 3, 4, 5]])

# 画像データ中の画素値の平均値を求める
mean = img.mean()

# (1.0 + 2.0 + 3.0 + 4.0 + 5.0) / 5 = 3.0

print(f'mean = {mean}')
