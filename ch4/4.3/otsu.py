import cv2
import numpy as np
from matplotlib import pyplot as plt

# 100*500[px]のカラー画像を生成し、白(255,255,255)で初期化する
src_img = np.full((100,500,3), 255, dtype=np.uint8)

# 適当にいくつかの色を生成
v = (50, 200)
colors = [(b,g,r) for b in v for g in v for r in v]
for i, color in enumerate(colors):
    cv2.circle(src_img, (i*60+40,50), 30, color, -1)

# threshold() に渡すためにグレイスケールに変換
gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

# しきい値処理(THRESH_OTSUを指定)
ret, img_otsu = cv2.threshold(gray_img,127,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print('大津の方法でのしきい値:', ret)

# しきい値処理(THRESH_TRIANGLEを指定)
ret, img_triangle = cv2.threshold(gray_img,127,255,cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
print('トライアングル法でのしきい値:', ret)

titles = ['Original', 'Gray', 'THRESH_OTSU','THRESH_TRIANGLE']
images = [src_img, gray_img, img_otsu, img_triangle]

plt.figure(figsize=(20,15))

# オリジナル、グレイスケール、大津の方法、トライアングルアルゴリズムそれぞれの画像を出力
for i, (title, img) in enumerate(zip(titles, images)):
    plt.subplot(4,1,i+1)
    plt.imshow(img, 'gray', vmin=0, vmax=255)
    plt.title(title)
plt.show()
