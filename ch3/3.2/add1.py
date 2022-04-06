import numpy as np
import cv2

x = np.uint8([250])
y = np.uint8([5])
z = cv2.add(x, y) # 250 + 5 = 255
print(f'z = {z}')
