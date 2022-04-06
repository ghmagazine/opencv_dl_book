import sys
import numpy as np
import cv2

# ファイル名
filename = 'output.xml'

# 書き込みモードでファイルを開く
fs = cv2.FileStorage(filename, cv2.FileStorage_WRITE)

## 以下のような書き方でもよい
## fs = cv2.FileStorage()
## fs.open(filename, cv2.FileStorage_WRITE)

# ファイルのオープンに失敗したらエラーとして終了
if fs.isOpened() is False:
    print('Failed to load XML file.')
    sys.exit(1)

# 書き出したいデータを定義
R = np.eye(3, 3)
T = np.zeros((3, 1))

# 書き出し
fs.write('R_MAT', R)
fs.write('T_MAT', T)

# コメント追記
fs.writeComment('This is comment')

# ファイルのクローズ、バッファの解放
fs.release()
