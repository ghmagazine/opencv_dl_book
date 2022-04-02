import os
import timeit

import cv2
import numpy as np


class efficientnet:
    def __init__(self, model_scale=7, use_gpu=False):
        directory = os.path.dirname(__file__)
        self.init_image(directory)
        self.init_model(directory, model_scale, use_gpu)

    def init_image(self, directory):
        self._image = cv2.imread(os.path.join(directory, "efficientnet/yorkie.jpg"))
        if self._image is None:
            raise IOError("failed read image!")

    def init_model(self, directory, model_scale, use_gpu):
        model_name = "efficientnet/efficientnet-b{0}.onnx".format(model_scale)
        weights = os.path.join(directory, model_name)
        self._model = cv2.dnn_ClassificationModel(weights)

        if use_gpu is True:
            self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        else:
            self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        size_list = [(224, 224), (240, 240), (260, 260), (300, 300),
                     (380, 380), (456, 456), (528, 528), (600, 600)]

        scale = 1.0 / 255.0
        size = size_list[model_scale]
        mean = (123.675, 116.28, 103.53)
        swap = True
        crop = True
        self._model.setInputParams(scale, size, mean, swap, crop)

    def classify(self):
        class_id, confidence = self._model.classify(self._image)


class mobilenet_v3:
    def __init__(self, use_large=True, use_gpu=False):
        directory = os.path.dirname(__file__)
        self.init_image(directory)
        self.init_model(directory, use_large)

    def init_image(self, directory):
        self._image = cv2.imread(os.path.join(directory, "mobilenet-v3/yorkie.jpg"))
        if self._image is None:
            raise IOError("failed read image!")

    def init_model(self, directory, use_large):
        if use_large is True:
            weights = os.path.join(directory, "mobilenet-v3/v3-large_224_1.0_float.pb")
        else:
            weights = os.path.join(directory, "mobilenet-v3/v3-small_224_1.0_float.pb")
        self._model = cv2.dnn_ClassificationModel(weights)

        self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        scale = 1.0 / 127.5
        size = (224, 224)
        mean = (127.5, 127.5, 127.5)
        swap = True
        crop = True
        self._model.setInputParams(scale, size, mean, swap, crop)

    def classify(self):
        class_id, confidence = self._model.classify(self._image)


def main():
    loop = 100

    # 精度重視のクラス分類（EfficientNet）
    for model_scale in range(8):
        use_gpu = False
        classifier = efficientnet(model_scale, use_gpu)
        classifier.classify()  # 初回の実行は計測しない
        time = timeit.timeit(lambda: classifier.classify(), globals=globals(), number=loop)
        time = (time / loop) * 1000
        print("EfficientNet (b{0}) : {1}[ms]".format(model_scale, time))

    # 処理速度重視のクラス分類（MobileNet v3）
    use_large = True
    classifier = mobilenet_v3(use_large)
    classifier.classify()  # 初回の実行は計測しない
    time = timeit.timeit(lambda: classifier.classify(), globals=globals(), number=loop)
    time = (time / loop) * 1000
    print("MobileNet v3 (Large) : {0}[ms]".format(time))

    use_large = False
    classifier = mobilenet_v3(use_large)
    classifier.classify()  # 初回の実行は計測しない
    time = timeit.timeit(lambda: classifier.classify(), globals=globals(), number=loop)
    time = (time / loop) * 1000
    print("MobileNet v3 (Smale) : {0}[ms]".format(time))


if __name__ == '__main__':
    main()
