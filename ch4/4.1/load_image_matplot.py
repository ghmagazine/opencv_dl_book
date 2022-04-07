import cv2
import matplotlib.pyplot as plt # Matplotlibをimport

# 適当な画像を読み込む
img = cv2.imread('test.jpg')

# BGR → RGB に変換する
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Matplotlibで画像を表示する
plt.imshow(img)
plt.show()
