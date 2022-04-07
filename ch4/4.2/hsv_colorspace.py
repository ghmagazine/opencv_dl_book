import cv2
import numpy as np
import matplotlib.pyplot as plt

# グラフを大きめに表示する
fig, ax = plt.subplots(figsize=(10, 10))

# 256px * 180px のまっさらな画像を用意する
img_hsv = np.zeros((180, 256, 3), np.uint8)

# Hを0〜179, Sを0〜255まで変化させながら画素を埋めていく
for y, h in enumerate(range(0, 180)):
    for x, s in enumerate(range(0, 256)):
        img_hsv[y, x, :] = (h, s, 255)

# 可視化のため、HSVからRGBに変換する
img_rgb = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
# 画像のタイトル
ax.set_title("HSV Color Space (V=255)", size='x-large')
# X軸のタイトル
ax.set_xlabel('Saturation', size='x-large')
# Y軸のタイトル
ax.set_ylabel('Hue', size='x-large')

# 画像(グラフ)を表示
plt.imshow(img_rgb)
plt.show()
