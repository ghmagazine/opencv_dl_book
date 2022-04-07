import cv2
import numpy as np
from matplotlib import pyplot as plt

# 20*20[px]のカラー画像を生成
width, height = 20, 20
src_img = np.full((width, height, 3), 128, dtype=np.uint8)
cv2.rectangle(src_img, (5,5), (14, 14), (255,255,255), -1) #白い四角を書く

# 30度回転して0.6倍するアフィン変換の変換行列を求める
angle = 30
M_rotate = cv2.getRotationMatrix2D(center=(width//2, height//2), angle=angle, scale=0.6)

flags = [cv2.INTER_NEAREST, cv2.INTER_LINEAR, cv2.INTER_CUBIC, cv2.INTER_AREA, cv2.INTER_LANCZOS4]
flags_name = ['NEAREST', 'LINEAR', 'CUBIC', 'AREA', 'LANCZOS4']

fig = plt.figure(figsize=(15,3))
ax = fig.add_subplot(1,len(flags)+1,1)
ax.title.set_text('original')
ax.imshow(src_img, 'gray')

for index, (flag, name) in enumerate(zip(flags, flags_name)):
    rotation_img = cv2.warpAffine(src_img, M_rotate, dsize=(width,height), flags=flag)
    ax = fig.add_subplot(1,len(flags)+1,index+2)
    ax.title.set_text(name)
    ax.imshow(rotation_img, 'gray')

