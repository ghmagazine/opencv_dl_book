import numpy as np
import cv2

# 画像ファイルをカラーで読み込み
src1 = cv2.imread('yorkie.png', cv2.IMREAD_COLOR)

# マスク画像を生成する
height, width, channels = src1.shape[:3]
src2 = np.zeros((height, width, channels), np.uint8)
cv2.rectangle(src2, (150, 135), (290, 315), (255, 255, 255), thickness=-1)

# ピクセルごとにAND演算を行う
dst = cv2.bitwise_and(src1, src2)

# 画像をウィンドウ表示する
cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
