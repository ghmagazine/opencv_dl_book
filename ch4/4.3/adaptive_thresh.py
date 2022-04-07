import cv2
import numpy as np
from matplotlib import pyplot as plt

img_bgr = cv2.imread('drivecam.jpg')
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

for thresh in range(30, 150, 30):
    ret, th = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)
    print(f'threshold={thresh}')
    cv2.imshow(f'thresh={thresh}', th)

ret, th = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imshow(f'Otsu (threshold={ret})', th)

th = cv2.adaptiveThreshold(img_gray, 255, \
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 4)
cv2.imshow(f'adaptiveThreshold', th)

cv2.waitKey(0)
