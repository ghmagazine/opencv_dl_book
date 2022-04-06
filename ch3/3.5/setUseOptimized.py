import cv2

print(f'before: {cv2.useOptimized()}')
cv2.setUseOptimized(False)
print(f'after: {cv2.useOptimized()}')
