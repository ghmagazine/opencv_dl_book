import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('drivecam.jpg')

src_pts = np.array([(670, 680), (1130, 680), (130, 800), (1600, 800)], dtype=np.float32)
dst_pts = np.array([(0, 0), (500, 0), (0, 500), (500, 500)], dtype=np.float32)

M = cv2.getPerspectiveTransform(src_pts, dst_pts)

dst_img = cv2.warpPerspective(img, M, (500, 500))

cv2.drawMarker(img, (670, 680), (0,0,255), cv2.MARKER_TILTED_CROSS, markerSize=50, thickness=10)
cv2.drawMarker(img, (1130, 680), (0,0,255), cv2.MARKER_TILTED_CROSS, markerSize=50, thickness=10)
cv2.drawMarker(img, (130, 800), (0,0,255), cv2.MARKER_TILTED_CROSS, markerSize=50, thickness=10)
cv2.drawMarker(img, (1600, 800), (0,0,255), cv2.MARKER_TILTED_CROSS, markerSize=50, thickness=10)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()

plt.imshow(cv2.cvtColor(dst_img, cv2.COLOR_BGR2RGB))
plt.show()
