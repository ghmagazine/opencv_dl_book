import cv2

# 画像ファイルをカラーで読み込み
src = cv2.imread('yorkie.png', cv2.IMREAD_COLOR)

# X軸を中心に反転
dst = cv2.flip(src, 0)

# 画像をウィンドウ表示する
cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
