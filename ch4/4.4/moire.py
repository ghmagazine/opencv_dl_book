import cv2
import numpy as np
import matplotlib.pyplot as plt

# モアレが発生しやすそうな画像を作る
x = np.linspace(0, 16, 3000)
y = np.linspace(0, 16, 3000)
xx, yy = np.meshgrid(x, y)
z = np.sin(xx**2 + yy**2)
fig = plt.figure(figsize=(10,10))
fig.gca().set_aspect('equal')
plt.contourf(x, y, z, cmap='gray')

# Matplotlib で描画したものを OpenCV の画像に変換するテクニック
fig.canvas.draw()
img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
plt.show()

# 画像を縮小して表示する(INTER_LINEAR)
img_linear = cv2.resize(img, (200,200), interpolation=cv2.INTER_LINEAR)
plt.imshow(img_linear)
plt.show()

# 画像を縮小して表示する(INTER_AREA)
img_area = cv2.resize(img, (200,200), interpolation=cv2.INTER_AREA)
plt.imshow(img_area)
plt.show()
