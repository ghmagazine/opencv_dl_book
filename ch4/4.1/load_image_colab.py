#
# このコードはGoogle Colab環境でのみ動作します
#
import cv2
from google.colab.patches import cv2_imshow #追加

img = cv2.imread('test.jpg')

cv2_imshow(img) # 変更
