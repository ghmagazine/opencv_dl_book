import cv2

# 画像ファイルをカラーで読み込み
img = cv2.imread('yorkie.png', cv2.IMREAD_COLOR)

# ROI[top:bottom, left:right]を使って画像データを切り出す
img_roi = img[135:320, 150:290]

# 画像をウィンドウ表示する
cv2.imshow('img', img)
cv2.imshow('img_roi', img_roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
