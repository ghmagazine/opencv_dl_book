import cv2

# 画像ファイルをカラーで読み込み
src1 = cv2.imread('aloeL.png', cv2.IMREAD_COLOR)
src2 = cv2.imread('aloeR.png', cv2.IMREAD_COLOR)

alpha = 0.5
beta = 0.5
gamma = 0.0

# ピクセルごとに重み付け合成を行う
dst = cv2.addWeighted(src1, alpha, src2, beta, gamma)

# 画像をウィンドウ表示する
cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
