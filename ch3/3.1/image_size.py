import cv2

# 画像ファイルをカラーで読み込み
img = cv2.imread('yorkie.png', cv2.IMREAD_COLOR)

if len(img.shape) == 3:
    # カラー画像
    height, width, channels = img.shape[:3]
else:
    # グレースケール画像
    height, width = img.shape[:2]
    channels = 1

# width、height、チャンネル数を表示する
print(f'width = {width}')
print(f'height = {height}')
print(f'channels = {channels}')
