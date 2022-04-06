import sys
import numpy as np
import cv2

# ファイル名
filename = 'input.xml'

# 読み込みモードでファイルを開く
fs = cv2.FileStorage(filename, cv2.FileStorage_READ)

## 以下のような書き方でもよい
## fs = cv2.FileStorage()
## fs.open(filename, cv2.FileStorage_READ)

# ファイルのオープンに失敗したらエラーとして終了
if fs.isOpened() is False:
    print('Failed to load XML file.')
    sys.exit(1)

# 要素の読み込み
R = fs.getNode('R_MAT').mat()
T = fs.getNode('T_MAT').mat()

print(R)
print(T)

# ファイルのクローズ、バッファの解放
fs.release()
