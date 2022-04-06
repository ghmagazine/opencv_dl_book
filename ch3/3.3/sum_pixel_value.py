import numpy as np
import cv2

img = np.array([[1, 2, 3, 4, 5]])

# 画像データ中の画素値の総和を計算
sum = img.sum()

print(f'sum = {sum}')