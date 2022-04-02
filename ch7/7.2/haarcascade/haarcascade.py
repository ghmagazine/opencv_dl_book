import os

import cv2
import numpy as np


def main():
    # キャプチャを開く
    directory = os.path.dirname(__file__)
    capture = cv2.VideoCapture(os.path.join(directory, "face.jpg"))  # 画像ファイル
    # capture = cv2.VideoCapture(0)  # カメラ
    if not capture.isOpened():
        raise IOError("can't open capture!")

    # 分類器を読み込む
    path = os.path.join(directory, "haarcascade_frontalface_default.xml")
    cascade = cv2.CascadeClassifier(path)
    if cascade is None:
        raise IOError("can't read cascade!")

    while True:
        # フレームをキャプチャして画像を読み込む
        result, image = capture.read()
        if result is False:
            cv2.waitKey(0)
            break

        # グレースケールに変換する
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 顔を検出する
        height, width = gray_image.shape
        min_size = (int(width / 10), int(height / 10))
        boxes = cascade.detectMultiScale(gray_image, minSize=min_size)

        # 検出した顔のバウンディングボックスを描画する
        for box in boxes:
            color = (0, 0, 255)
            thickness = 2
            cv2.rectangle(image, box, color, thickness, cv2.LINE_AA)

        # 画像を表示する
        cv2.imshow("face detection", image)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
