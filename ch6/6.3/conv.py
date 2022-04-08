import cv2
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(20,10))

src_img = cv2.imread('test.png', cv2.IMREAD_GRAYSCALE)
plt.subplot(1,3,1)
plt.imshow(src_img, cmap='gray')

# 縦線を抽出するフィルタ
filter_vertical = [[-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1]]

dst_img = cv2.filter2D(src_img, ddepth=-1, kernel=np.array(filter_vertical))
plt.subplot(1,3,2)
plt.imshow(cv2.convertScaleAbs(dst_img), cmap='gray')

# 横線を抽出するフィルタ
filter_horizontal = [[-1, -2, -1],
                [0, 0, 0],
                [1, 2, 1]]

dst_img = cv2.filter2D(src_img, ddepth=-1, kernel=np.array(filter_horizontal))
plt.subplot(1,3,3)
plt.imshow(cv2.convertScaleAbs(dst_img), cmap='gray')
plt.show()
