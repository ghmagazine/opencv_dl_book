import numpy as np
import cv2

# 画像ファイルをカラーで読み込み
org_img = cv2.imread('yorkie.png', cv2.IMREAD_COLOR)

# cv2.copyToでコピーする
mask = np.full(org_img.shape, 255, np.uint8)
cv_copy_img = cv2.copyTo(org_img, mask)

# numpy.ndarray.copyでコピーする
numpy_copy_img = org_img.copy()

# shallow copyでコピーする
shallow_copy_img = org_img

# コピー元（img1）の左上を矩形で塗りつぶす
cv2.rectangle(org_img, (0, 0), (100, 100), (255, 255, 255), thickness=-1)

# 画像をウィンドウ表示する
cv2.imshow('cv_copy_img', cv_copy_img)
cv2.imshow('numpy_copy_img', numpy_copy_img)
cv2.imshow('shallow_copy_img', shallow_copy_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
