import numpy as np
import cv2

x = np.uint8([250])
y = np.uint8([10])
z = cv2.add(x, y) # 250 + 10 = 260 => 255
print(f'z = {z}')
