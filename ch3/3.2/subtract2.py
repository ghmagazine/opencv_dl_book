import numpy as np
import cv2

x = np.uint8([10])
y = np.uint8([20])
z = cv2.subtract(x, y) # 10 - 20 = -10 => 0
print(f'z = {z}')
