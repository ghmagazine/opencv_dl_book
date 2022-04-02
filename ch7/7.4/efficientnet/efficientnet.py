import os

import cv2
import numpy as np


# ファイルからクラスの名前のリストを読み込む関数
def read_classes(file):
    classes = None
    with open(file, mode='r', encoding="utf-8") as f:
        classes = f.read().splitlines()
    return classes


# 入力配列を[0.0-1.0]の範囲に変換する関数（SoftMax関数）
def softmax(confidences):
    exp = np.exp(confidences - np.max(confidences))
    return exp / np.sum(exp)


def main():
    # キャプチャを開く
    directory = os.path.dirname(__file__)
    capture = cv2.VideoCapture(os.path.join(directory, "yorkie.jpg"))  # 画像ファイル
    # capture = cv2.VideoCapture(0)  # カメラ
    if not capture.isOpened():
        raise IOError("can't open capture!")

    # モデルを読み込む
    # weights = os.path.join(directory, "efficientnet-b0.onnx")
    # weights = os.path.join(directory, "efficientnet-b1.onnx")
    # weights = os.path.join(directory, "efficientnet-b2.onnx")
    # weights = os.path.join(directory, "efficientnet-b3.onnx")
    # weights = os.path.join(directory, "efficientnet-b4.onnx")
    # weights = os.path.join(directory, "efficientnet-b5.onnx")
    # weights = os.path.join(directory, "efficientnet-b6.onnx")
    weights = os.path.join(directory, "efficientnet-b7.onnx")
    model = cv2.dnn_ClassificationModel(weights)

    # モデルの推論に使用するエンジンとデバイスを設定する
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # モデルの入力パラメーターを設定する
    scale = 1.0 / 255.0               # スケールファクター
    # size = (224, 224)               # 入力サイズ (b0)
    # size = (240, 240)               # 入力サイズ (b1)
    # size = (260, 260)               # 入力サイズ (b2)
    # size = (300, 300)               # 入力サイズ (b3)
    # size = (380, 380)               # 入力サイズ (b4)
    # size = (456, 456)               # 入力サイズ (b5)
    # size = (528, 528)               # 入力サイズ (b6)
    size = (600, 600)                 # 入力サイズ (b7)
    mean = (123.675, 116.28, 103.53)  # 差し引かれる平均値
    swap = True                       # チャンネルの順番（True: RGB、False: BGR）
    crop = True                       # クロップ
    model.setInputParams(scale, size, mean, swap, crop)

    # クラスリストを取得する
    names = os.path.join(directory, "imagenet.names")
    classes = read_classes(names)

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

        # クラスに分類して信頼度が最も高いクラスを取得する
        class_id, confidence = model.classify(image)

        # 信頼度が最も高いクラスを描画する
        label = classes[class_id]
        result = "{0} ({1:.3f})".format(label, confidence)
        point = (30, 30)
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.5
        color = (255, 255, 255)
        thickness = 1
        cv2.putText(image, result, point, font, scale, color, thickness, cv2.LINE_AA)

        # 推論結果を取得する
        # confidences = model.predict(image)
        # confidences = np.squeeze(confidences)

        # 必要な場合はSoftMax関数で信頼度を[0.0-1.0]の範囲に変換する
        # ここで扱うEfficientNetの学習済みモデルにはSoftMaxレイヤーが含まれないため必要
        # confidences = softmax(confidences)

        # 信頼度が上位5個のクラスを取得する
        # top_n = 5
        # class_ids = np.argsort(-confidences)[:top_n:]

        # 信頼度が上位5個のクラスを表示する
        # for i, class_id in enumerate(class_ids):
        #     label = classes[class_id]
        #     confidence = confidences[class_id]
        #     result = "top-{0} {1} ({2:.3f})".format(i + 1, label, confidence)
        #     print(result)

        # 画像を表示する
        cv2.imshow("classfication", image)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
