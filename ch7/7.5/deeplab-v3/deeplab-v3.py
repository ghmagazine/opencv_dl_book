import os

import cv2
import numpy as np


# ファイルからクラスの名前のリストを読み込む関数
def read_classes(file):
    classes = None
    with open(file, mode='r', encoding="utf-8") as f:
        classes = f.read().splitlines()
    return classes


# クラスの数だけカラーテーブルを生成する関数
def get_colors(num):
    colors = []
    np.random.seed(0)
    for i in range(num):
        color = np.random.randint(0, 256, [3]).astype(np.uint8)
        colors.append(color.tolist())
    return colors


def main():
    # キャプチャを開く
    directory = os.path.dirname(__file__)
    capture = cv2.VideoCapture(os.path.join(directory, "bicycle.jpg"))  # 画像ファイル（自転車）
    # capture = cv2.VideoCapture(os.path.join(directory, "city.jpg"))  # 画像ファイル（道路）
    # capture = cv2.VideoCapture(0)  # カメラ
    if not capture.isOpened():
        raise IOError("can't open capture!")

    # モデルを読み込む
    weights = os.path.join(directory, "optimized_graph_voc.pb")
    # weights = os.path.join(directory, "optimized_graph_cityscapes.pb")
    model = cv2.dnn_SegmentationModel(weights)

    # モデルの推論に使用するエンジンとデバイスを設定する
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # モデルの入力パラメーターを設定する
    scale = 1.0 / 127.5           # スケールファクター
    size = (513, 513)             # 入力サイズ（VOC）
    # size = (2049, 1025)         # 入力サイズ（CityScapes）
    mean = (127.5, 127.5, 127.5)  # 差し引かれる平均値
    swap = True                   # チャンネルの順番（True: RGB、False: BGR）
    crop = False                  # クロップ
    model.setInputParams(scale, size, mean, swap, crop)

    # クラスリストとカラーテーブルを取得する
    names = os.path.join(directory, "voc.names")  # VOC
    # names = os.path.join(directory, "cityscapes.names")  # CityScapes
    classes = read_classes(names)
    colors = get_colors(len(classes))
    if "voc.names" in names:
        colors[0] = (0, 0, 0)

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

        # セグメンテーションしてマスクを取得する
        mask = model.segment(image)

        # カラーテーブルを参照してマスクに色を付ける
        color_mask = np.array(colors, dtype=np.uint8)[mask]

        # マスクを入力画像と同じサイズに拡大する
        height, width, _ = image.shape
        color_mask = cv2.resize(color_mask, (width, height), cv2.INTER_NEAREST)

        # 画像とマスクをアルファブレンドする
        alpha = 0.5
        beta = 1.0 - alpha
        cv2.addWeighted(image, alpha, color_mask, beta, 0.0, image)

        # 画像とマスクを表示する
        cv2.imshow("segmentation", image)
        cv2.imshow("mask", color_mask)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
