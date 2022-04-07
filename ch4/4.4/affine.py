import cv2
import numpy as np
from matplotlib import pyplot as plt

# 100*100[px]のカラー画像を生成
width, height = 100, 100
src_img = np.full((width, height, 3), 128, dtype=np.uint8)
cv2.rectangle(src_img, (10,10), (width-10, height-10), (255,255,255), -1) #枠をつける
# 文字を描画する
cv2.putText(src_img, 'CV', (30,60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 4, cv2.LINE_4)

plt.imshow(src_img, 'gray')
plt.show()

#
# 平行移動
# 画像を+x, +y方向に移動する
#
x = 50
y = -10
M_shift = [[1, 0, x],
           [0, 1, y]]
M_shift = np.array(M_shift, dtype=np.float32)
sheer_img = cv2.warpAffine(src_img, M_shift, dsize=(width,height))
plt.imshow(sheer_img, 'gray')
plt.show()

#
# 回転
# 画像をcenterを中心にangle度回転させる
#
angle = 45
# 回転はやや煩雑だが、getRotationMatrix2Dを使うと変換行列を求めてくれる
M_rotate = cv2.getRotationMatrix2D(center=(width//2, height//2), angle=angle, scale=1.0)
rotation_img = cv2.warpAffine(src_img, M_rotate, dsize=(width,height))
plt.imshow(rotation_img, 'gray')
plt.show()

#
# せん断(シアー)
#
a = 0.2
b = 0.0
M_shear = [[1, a, 0],
           [b, 1, 0]]
M_shear = np.array(M_shear, dtype=np.float32)
shear_img = cv2.warpAffine(src_img, M_shear, dsize=(width,height))
plt.imshow(shear_img, 'gray')
plt.show()

