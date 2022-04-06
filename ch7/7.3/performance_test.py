import os
import timeit

import cv2
import numpy as np


class yolov4:
    def __init__(self, size=416, use_gpu=False):
        directory = os.path.dirname(__file__)
        if size != 320 and size != 416 and size != 512 and size != 608:
            raise IOError("failed input size!")
        self.init_image(directory)
        self.init_model(directory, size, use_gpu)

    def init_image(self, directory):
        self._image = cv2.imread(os.path.join(directory, "yolov4/dog.jpg"))
        if self._image is None:
            raise IOError("failed read image!")

    def init_model(self, directory, size, use_gpu):
        weights = os.path.join(directory, "yolov4/yolov4.weights")
        config = os.path.join(directory, "yolov4/yolov4.cfg")
        self._model = cv2.dnn_DetectionModel(weights, config)

        if use_gpu is True:
            self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        else:
            self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        scale = 1.0 / 255.0
        size = (size, size)
        mean = (0.0, 0.0, 0.0)
        swap = True
        crop = False
        self._model.setInputParams(scale, size, mean, swap, crop)

        self._model.setNmsAcrossClasses(False)

    def detect(self):
        confidence_threshold = 0.5
        nms_threshold = 0.4
        class_ids, confidences, boxes = self._model.detect(self._image, confidence_threshold, nms_threshold)


class scaled_yolov4:
    def __init__(self, model, size=512, use_gpu=False):
        directory = os.path.dirname(__file__)
        if size != 512 and size != 640 and size != 896 and size != 1280:
            raise IOError("failed input size!")
        self.init_image(directory)
        self.init_model(directory, model, size, use_gpu)

    def init_image(self, directory):
        self._image = cv2.imread(os.path.join(directory, "scaled-yolov4/dog.jpg"))
        if self._image is None:
            raise IOError("failed read image!")

    def init_model(self, directory, model, size, use_gpu):
        weights = os.path.join(directory, "scaled-yolov4/{0}.weights".format(model))
        config = os.path.join(directory, "scaled-yolov4/{0}.cfg".format(model))
        self._model = cv2.dnn_DetectionModel(weights, config)

        if use_gpu is True:
            self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        else:
            self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        scale = 1.0 / 255.0
        size = (size, size)
        mean = (0.0, 0.0, 0.0)
        swap = True
        crop = False
        self._model.setInputParams(scale, size, mean, swap, crop)

        self._model.setNmsAcrossClasses(False)

    def detect(self):
        confidence_threshold = 0.5
        nms_threshold = 0.4
        class_ids, confidences, boxes = self._model.detect(self._image, confidence_threshold, nms_threshold)


class yolov4_tiny:
    def __init__(self, size=416):
        directory = os.path.dirname(__file__)
        if size != 320 and size != 416 and size != 512 and size != 608:
            raise IOError("failed input size!")
        self.init_image(directory)
        self.init_model(directory, size)

    def init_image(self, directory):
        self._image = cv2.imread(os.path.join(directory, "yolov4-tiny/dog.jpg"))
        if self._image is None:
            raise IOError("failed read image!")

    def init_model(self, directory, size):
        weights = os.path.join(directory, "yolov4-tiny/yolov4-tiny.weights")
        config = os.path.join(directory, "yolov4-tiny/yolov4-tiny.cfg")
        self._model = cv2.dnn_DetectionModel(weights, config)

        self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        scale = 1.0 / 255.0
        size = (size, size)
        mean = (0.0, 0.0, 0.0)
        swap = True
        crop = False
        self._model.setInputParams(scale, size, mean, swap, crop)

        self._model.setNmsAcrossClasses(False)

    def detect(self):
        confidence_threshold = 0.5
        nms_threshold = 0.4
        class_ids, confidences, boxes = self._model.detect(self._image, confidence_threshold, nms_threshold)


def main():
    loop = 100
    sizes = [320, 416, 512, 608]

    # 精度重視のオブジェクト検出（YOLOv4）
    for size in sizes:
        use_gpu = False
        detector = yolov4(size, use_gpu)
        detector.detect()  # 初回の実行は計測しない
        time = timeit.timeit(lambda: detector.detect(), globals=globals(), number=loop)
        time = (time / loop) * 1000
        print("YOLOv4 ({0}x{0}) : {1}[ms]".format(size, time))

    # さらに精度重視のオブジェクト検出（Scaled-YOLOv4）
    patterns = [
        ("yolov4-csp", 512),
        ("yolov4-csp", 640),
        ("yolov4x-mish", 640),
        ("yolov4-p5", 896),
        ("yolov4-p6", 1280)
    ]
    for model, size in patterns:
        use_gpu = False
        detector = scaled_yolov4(model, size, use_gpu)
        detector.detect()  # 初回の実行は計測しない
        time = timeit.timeit(lambda: detector.detect(), globals=globals(), number=loop)
        time = (time / loop) * 1000
        print("Scaled-YOLOv4 {0} ({1}x{1}) : {2}[ms]".format(model, size, time))

    # 処理速度重視のオブジェクト検出（YOLOv4-tiny）
    for size in sizes:
        detector = yolov4_tiny(size)
        detector.detect()  # 初回の実行は計測しない
        time = timeit.timeit(lambda: detector.detect(), globals=globals(), number=loop)
        time = (time / loop) * 1000
        print("YOLOv4-tiny ({0}x{0}) : {1}[ms]".format(size, time))


if __name__ == '__main__':
    main()
