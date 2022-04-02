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


# テキストを認識するクラス
class text_recognizer:
    _model = None
    _require_gray = False

    # コンストラクタ
    def __init__(self):
        self._init_model()

    # モデルを準備する
    def _init_model(self):
        # モデルを読み込む
        directory = os.path.dirname(__file__)
        weights = os.path.join(directory, "DenseNet_CTC.onnx")  # 英語, 数字
        self._model = cv2.dnn_TextRecognitionModel(weights)

        # モデルの推論に使用するエンジンとデバイスを設定する
        self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # グレースケール画像を要求する（DenseNet_CTC）
        self._require_gray = False
        if "DenseNet_CTC.onnx" in weights:
            self._require_gray = True

        # モデルの入力パラメーターを設定する
        scale = 1.0 / 127.5           # スケールファクター
        size = (100, 32)              # 入力サイズ
        mean = (127.5, 127.5, 127.5)  # 差し引かれる平均値
        swap = True                   # チャンネルの順番（True: RGB、False: BGR）
        crop = False                  # クロップ
        self._model.setInputParams(scale, size, mean, swap, crop)

        # デコードタイプを設定する
        type = "CTC-greedy"               # 貪欲法
        # tpye = "CTC-prefix-beam-search" # ビーム探索
        self._model.setDecodeType(type)

        # 語彙リストを設定する
        vocabulary_file = os.path.join(directory, "alphabet_36.txt")  # 英語, 数字
        vocabularies = self._read_vocabularies(vocabulary_file)
        self._model.setVocabulary(vocabularies)

    # ファイルから語彙リストを読み込む
    def _read_vocabularies(self, file):
        vocabularies = None
        with open(file, mode='r', encoding="utf-8") as f:
            vocabularies = f.read().splitlines()
        return vocabularies

    # 画像からテキストを認識する
    def recognize(self, image):
        if self._model is None:
            raise IOError("failed model has not been created!")

        if image is None:
            raise IOError("failed image is empty!")

        # グレースケール画像に変換する
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        if self._require_gray and channels != 1:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # テキストを認識する
        text = self._model.recognize(image)
        return text


# 画像とテキスト領域の座標リストからテキスト領域の画像を切り出す関数
def get_text_images(image, vertices):
    text_images = []
    size = (100, 32)
    for vertex in vertices:
        source_poins = np.array(vertex, dtype=np.float32)
        target_poins = np.array([[0, size[1]], [0, 0], [size[0], 0], [size[0], size[1]]], dtype=np.float32)
        transform_matrix = cv2.getPerspectiveTransform(source_poins, target_poins)
        text_image = cv2.warpPerspective(image, transform_matrix, size)
        text_images.append(text_image)
    return text_images


def main():
    # キャプチャを開く
    directory = os.path.dirname(__file__)
    capture = cv2.VideoCapture(os.path.join(directory, "text.jpg"))  # 画像ファイル
    # capture = cv2.VideoCapture(0)  # カメラ
    if not capture.isOpened():
        raise IOError("can't open capture!")

    # テキスト検出器の生成
    detector = text_detector()

    # テキスト認識器の生成
    recognizer = text_recognizer()

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

        # テキストを検出する
        vertices, _ = detector.detect_vertices(image)

        # テキスト領域の画像を切り出す
        text_images = get_text_images(image, vertices)

        # テキスト領域の画像を保存する
        # for i, text_image in enumerate(text_images):
        #     file_name = "text_{0}.jpg".format(str(i).zfill(3))
        #     cv2.imwrite(os.path.join(directory, file_name), text_image)

        # テキストを認識する
        texts = []
        for text_image in text_images:
            text = recognizer.recognize(text_image)
            texts.append(text)

        # テキスト検出の結果を描画する
        for vertex in vertices:
            vertex = np.array(vertex)
            close = True
            color = (0, 255, 0)
            thickness = 2
            cv2.polylines(image, [vertex], close, color, thickness, cv2.LINE_AA)

        # テキスト認識の結果を描画する
        for text, vertex in zip(texts, vertices):
            position = vertex[1] - (0, 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 1.0
            color = (0, 0, 255)
            cv2.putText(image, text, position, font, scale, color, thickness, cv2.LINE_AA)

            # OpenCVのcv2.putText()では中国語（漢字）は描画できないので標準出力に表示する
            print(text)

        # 画像を表示する
        cv2.imshow("text recognition", image)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
