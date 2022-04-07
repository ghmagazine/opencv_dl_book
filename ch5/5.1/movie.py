import cv2

cap = cv2.VideoCapture('test.mp4')

# 総フレーム数
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

while True:
    ret, frame = cap.read()

    # 今のフレーム数
    current_frames = cap.get(cv2.CAP_PROP_POS_FRAMES)

    # 総フレーム数以上読み込んだら終了
    if current_frames >= total_frames:
        break

    # 読み込みに失敗したらスキップする
    if (not ret) or (frame is None):
        continue

    # 画像の表示
    cv2.imshow('frame', frame)
    cv2.waitKey(1) # 1ミリ秒待つ
