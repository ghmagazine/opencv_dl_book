import cv2
import numpy as np

cap = cv2.VideoCapture('movie.mp4') # 入力ファイル名

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# VideoWriterのインスタンスを作る
# width, heightは正確に指定しないと書き込まれないことに注意
fourcc = cv2.VideoWriter_fourcc(*'MP4V') # コーデック
#writer = cv2.VideoWriter('output.mp4', fourcc=fourcc, fps=fps, frameSize=(width, height))
writer = cv2.VideoWriter('output_%05d.jpg', fourcc=0, fps=0, frameSize=(width, height))

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        frame = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)
        # もとのフルカラーの画像と分解した1チャンネルの画像はそのままでは連結できないので
        # cvtColorでグレイスケール→BGRに変換している
        b, g, r = map(lambda x: cv2.cvtColor(x, cv2.COLOR_GRAY2BGR), cv2.split(frame))
        concat_frame = cv2.vconcat([cv2.hconcat([frame, r]), cv2.hconcat([g, b])])
        writer.write(concat_frame)
    else:
        break

cap.release()
writer.release()
