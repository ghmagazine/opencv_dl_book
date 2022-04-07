import cv2
import matplotlib.pyplot as plt
import numpy as np

img_bgr = cv2.imread('chocolates.jpg')
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

h, s, v = cv2.split(img_hsv)

# 画像を大きめに表示する
plt.figure(figsize=(15,10))

# 2x3の領域に区切って合計6枚の画像をまとめて表示する
plt.subplot(2,3,1)
plt.title('Original (RGB)')
plt.imshow(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))

plt.subplot(2,3,2)
plt.title('Hue (H)')
plt.imshow(h, cmap='gray')

plt.subplot(2,3,3)
plt.title('Saturation (S)')
plt.imshow(s, cmap='gray')

plt.subplot(2,3,4)
plt.title('Value, Brightness (V)')
plt.imshow(v, cmap='gray')

# マスク画像(抜き出す部分が1, それ以外が0の画像）を作ります
# ここでは Hue が 80〜140かつ、Saturation が 70を超える部分を指定しています
mask = np.zeros(h.shape, dtype=np.uint8)
mask[(h > 80) & (h < 140) & (s > 70)] = 255

# そのままではマスク画像に穴が開くので closing 処理をすると綺麗なマスクになります
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((41,41),np.uint8))

# maskが1チャンネル, img_bgrが3チャンネルのためそのままでは AND が計算できません
# そのため cvtColor() でmask側を3チャンネルに変換しています。
mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

# bitwise_and() で AND をとり、MASKが0の部分が真っ黒になっている画像を出力します
result_img = cv2.bitwise_and(img_bgr, mask_3ch)

# マスク画像を表示
plt.subplot(2,3,5)
plt.title('mask')
plt.imshow(mask, cmap='gray')

# 最終的な出力を表示
plt.subplot(2,3,6)
plt.title('result')
plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))

plt.show()
