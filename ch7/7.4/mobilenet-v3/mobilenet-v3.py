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
    weights = os.path.join(directory, "v3-large_224_1.0_float.pb")  # Large
    # weights = os.path.join(directory, "v3-small_224_1.0_float.pb")  # Small
    model = cv2.dnn_ClassificationModel(weights)

    # モデルの推論に使用するエンジンとデバイスを設定する
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # モデルの入力パラメーターを設定する
    scale = 1.0 / 127.5           # スケールファクター
    size = (224, 224)             # 入力サイズ
    mean = (127.5, 127.5, 127.5)  # 差し引かれる平均値
    swap = True                   # チャンネルの順番（True: RGB、False: BGR）
    crop = True                   # クロップ
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
        label = classes[class_id - 1]  # クラスIDの範囲は[1, 1001]なので1を引く
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
        # ここで扱うMobileNet v3の学習済みモデルにはSoftMaxレイヤーが含まれるため不要
        # confidences = softmax(confidences)

        # 信頼度が上位5個のクラスを取得する
        # top_n = 5
        # class_ids = np.argsort(-confidences)[:top_n:]

        # 信頼度が上位5個のクラスを表示する
        # for i, class_id in enumerate(class_ids):
        #     label = classes[class_id - 1]
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
