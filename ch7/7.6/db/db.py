import os

import cv2
import numpy as np


# テキストを検出するクラス
class text_detector:
    # コンストラクタ
    def __init__(self):
        self._init_model()

    # モデルを準備する
    def _init_model(self):
        # モデルを読み込む
        directory = os.path.dirname(__file__)
        # weights = os.path.join(directory, "DB_TD500_resnet50.onnx")  # 英語, 中国語, 数字
        # weights = os.path.join(directory, "DB_TD500_resnet18.onnx")  # 英語, 中国語, 数字
        weights = os.path.join(directory, "DB_IC15_resnet50.onnx")     # 英語, 数字
        # weights = os.path.join(directory, "DB_IC15_resnet18.onnx")   # 英語, 数字
        self._model = cv2.dnn_TextDetectionModel_DB(weights)

        # モデルの推論に使用するエンジンとデバイスを設定する
        self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # モデルの入力パラメーターを設定する
        scale = 1.0 / 255.0                                # スケールファクター
        # size = (736, 736)                                # 入力サイズ（MSRA-TD500）
        size = (736, 1280)                                 # 入力サイズ（ICDAR2015）
        mean = (122.67891434, 116.66876762, 104.00698793)  # 差し引かれる平均値
        swap = False                                       # チャンネルの順番（True: RGB、False: BGR）
        crop = False                                       # クロップ
        self._model.setInputParams(scale, size, mean, swap, crop)

        # テキスト検出のパラメーターを設定する
        binary_threshold = 0.3   # 二値化の閾値
        polygon_threshold = 0.5  # テキスト輪郭スコアの閾値
        max_candidates = 200     # テキスト候補領域の上限値
        unclip_ratio = 2.0       # アンクリップ率
        self._model.setBinaryThreshold(binary_threshold)
        self._model.setPolygonThreshold(polygon_threshold)
        self._model.setMaxCandidates(max_candidates)
        self._model.setUnclipRatio(unclip_ratio)

    # 画像からテキストを検出する（座標）
    def detect_vertices(self, image):
        if self._model is None:
            raise IOError("failed model has not been created!")

        if image is None:
            raise IOError("failed image is empty!")

        # テキストを検出する（座標）
        vertices, confidences = self._model.detect(image)

        return vertices, confidences

    # 画像からテキストを検出する（中心座標、領域サイズ、回転角度）
    def detect_rotated_rectangles(self, image):
        if self._model is None:
            raise IOError("failed model has not been created!")

        if image is None:
            raise IOError("failed image is empty!")

        # テキストを検出する（中心座標、領域サイズ、回転角度）
        rotated_rectangles, confidences = self._model.detectTextRectangles(image)

        return rotated_rectangles, confidences


# 回転矩形から矩形四隅の頂点座標（左下から時計回り）を取得する
def get_vertices(rotated_rectangles):
    vertices = []
    for rotated_rectangle in rotated_rectangles:
        points = cv2.boxPoints(rotated_rectangle)
        bl = tuple(map(int, points[0]))  # 左下
        tl = tuple(map(int, points[1]))  # 左上
        tr = tuple(map(int, points[2]))  # 右上
        br = tuple(map(int, points[3]))  # 右下
        vertices.append([bl, tl, tr, br])
    return vertices


def main():
    # キャプチャを開く
    directory = os.path.dirname(__file__)
    capture = cv2.VideoCapture(os.path.join(directory, "text.jpg"))  # 画像ファイル
    # capture = cv2.VideoCapture(0)  # カメラ
    if not capture.isOpened():
        raise IOError("can't open capture!")

    # テキスト検出器の生成
    detector = text_detector()

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

        # テキスト検出（座標）
        vertices, _ = detector.detect_vertices(image)

        # テキスト検出（中心座標、領域サイズ、回転角度）
        # rotated_rectangles, _ = detector.detect_rotated_rectangles(image)
        # vertices = get_vertices(rotated_rectangles)  # テキスト検出（座標）と同じ

        # 検出したテキスト領域の矩形を描画する
        for vertex in vertices:
            vertex = np.array(vertex)
            close = True
            color = (0, 255, 0)
            thickness = 2
            cv2.polylines(image, [vertex], close, color, thickness, cv2.LINE_AA)

        # 画像を表示する
        cv2.imshow("text detection", image)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
