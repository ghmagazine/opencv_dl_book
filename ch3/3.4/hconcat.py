import cv2

# 画像ファイルをカラーで読み込み
img1 = cv2.imread('yorkie.png', cv2.IMREAD_COLOR)
img2 = cv2.imread('yorkie_flip_0.png', cv2.IMREAD_COLOR)

# 画像を水平方向に連結
hconcat_img = cv2.hconcat([img1, img2])

# 画像をウィンドウ表示する
cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.imshow('hconcat_img', hconcat_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
