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

    # モデルを読み込む
    # weights = os.path.join(directory, "opencv_face_detector.caffemodel")  # float32
    # config = os.path.join(directory, "opencv_face_detector.prototxt")
    weights = os.path.join(directory, "opencv_face_detector_fp16.caffemodel")  # float16
    config = os.path.join(directory, "opencv_face_detector_fp16.prototxt")
    # weights = os.path.join(directory, "opencv_face_detector_uint8.pb")  # uint8
    # config = os.path.join(directory, "opencv_face_detector_uint8.pbtxt")
    model = cv2.dnn_DetectionModel(weights, config)

    # モデルの推論に使用するエンジンとデバイスを設定する
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # モデルの入力パラメーターを設定する
    scale = 1.0                   # スケールファクター
    size = (300, 300)             # 入力サイズ
    mean = (104.0, 177.0, 123.0)  # 差し引かれる平均値
    swap = False                  # チャンネルの順番（True: RGB、False: BGR）
    crop = False                  # クロップ
    model.setInputParams(scale, size, mean, swap, crop)

    while True:
        # フレームをキャプチャして画像を読み込む
        result, image = capture.read()
        if result is False:
            cv2.waitKey(0)
            break

        # 画像が3チャンネル以外の場合は3チャンネルに変換する
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        if channels == 1:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        if channels == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        # 顔を検出する
        confidence_threshold = 0.6
        nms_threshold = 0.4
        _, _, boxes = model.detect(image, confidence_threshold, nms_threshold)

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
