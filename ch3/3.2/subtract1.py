import numpy as np
import cv2

x = np.uint8([10])
y = np.uint8([5])
z = cv2.subtract(x, y) # 10 - 5 = 5
print(f'z = {z}')
