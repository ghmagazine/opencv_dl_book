import os
import timeit

import cv2
import numpy as np


class cascade_classfication:
    def __init__(self):
        directory = os.path.dirname(__file__)
        self.init_image(directory)
        self.init_model(directory)

    def init_image(self, directory):
        self._image = cv2.imread(os.path.join(directory, "haarcascade/face.jpg"))
        if self._image is None:
            raise IOError("failed read image!")

    def init_model(self, directory):
        cascade = os.path.join(directory, "haarcascade/haarcascade_frontalface_default.xml")
        if not os.path.exists(cascade):
            raise IOError("failed read cascade!")
        self._cascade = cv2.CascadeClassifier(cascade)
        height, width, _ = self._image.shape
        self._offset = (width / 300.0, height / 300.0,
                        width / 300.0, height / 300.0)

    def detect(self):
        image = cv2.resize(self._image, (300, 300))
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        boxes = self._cascade.detectMultiScale(gray_image)
        boxes = (boxes * self._offset).astype(np.uint8)


class deep_learning_float32:
    def __init__(self):
        directory = os.path.dirname(__file__)
        self.init_image(directory)
        self.init_model(directory)

    def init_image(self, directory):
        self._image = cv2.imread(os.path.join(directory, "opencv_face_detector/face.jpg"))
        if self._image is None:
            raise IOError("failed read image!")

    def init_model(self, directory):
        weights = os.path.join(directory, "opencv_face_detector/opencv_face_detector.caffemodel")
        config = os.path.join(directory, "opencv_face_detector/opencv_face_detector.prototxt")
        self._model = cv2.dnn_DetectionModel(weights, config)
        if self._model is None:
            raise IOError("failed read model!")

        scale = 1.0
        size = (300, 300)
        mean = (104.0, 177.0, 123.0)
        swap = False
        crop = False
        self._model.setInputParams(scale, size, mean, swap, crop)

    def detect(self):
        confidence_threshold = 0.3
        nms_threshold = 0.4
        _, _, boxes = self._model.detect(self._image, confidence_threshold, nms_threshold)


class deep_learning_float16:
    def __init__(self):
        directory = os.path.dirname(__file__)
        self.init_image(directory)
        self.init_model(directory)

    def init_image(self, directory):
        self._image = cv2.imread(os.path.join(directory, "opencv_face_detector/face.jpg"))
        if self._image is None:
            raise IOError("failed read image!")

    def init_model(self, directory):
        weights = os.path.join(directory, "opencv_face_detector/opencv_face_detector_fp16.caffemodel")
        config = os.path.join(directory, "opencv_face_detector/opencv_face_detector_fp16.prototxt")
        self._model = cv2.dnn_DetectionModel(weights, config)
        if self._model is None:
            raise IOError("failed read model!")

        scale = 1.0
        size = (300, 300)
        mean = (104.0, 177.0, 123.0)
        swap = False
        crop = False
        self._model.setInputParams(scale, size, mean, swap, crop)

    def detect(self):
        confidence_threshold = 0.3
        nms_threshold = 0.4
        _, _, boxes = self._model.detect(self._image, confidence_threshold, nms_threshold)


class deep_learning_uint8:
    def __init__(self):
        directory = os.path.dirname(__file__)
        self.init_image(directory)
        self.init_model(directory)

    def init_image(self, directory):
        self._image = cv2.imread(os.path.join(directory, "opencv_face_detector/face.jpg"))
        if self._image is None:
            raise IOError("failed read image!")

    def init_model(self, directory):
        weights = os.path.join(directory, "opencv_face_detector/opencv_face_detector_uint8.pb")
        config = os.path.join(directory, "opencv_face_detector/opencv_face_detector_uint8.pbtxt")
        self._model = cv2.dnn_DetectionModel(weights, config)
        if self._model is None:
            raise IOError("failed read model!")

        scale = 1.0
        size = (300, 300)
        mean = (104.0, 177.0, 123.0)
        swap = False
        crop = False
        self._model.setInputParams(scale, size, mean, swap, crop)

    def detect(self):
        confidence_threshold = 0.3
        nms_threshold = 0.4
        _, _, boxes = self._model.detect(self._image, confidence_threshold, nms_threshold)


def main():
    loop = 100

    # カスケード型の識別機
    detector = cascade_classfication()
    detector.detect()  # 初回の実行は計測しない
    time = timeit.timeit(lambda: detector.detect(), globals=globals(), number=loop)
    time = (time / loop) * 1000
    print("cascade classfication : {0}[ms]".format(time))

    #　ディープラーニング
    detector = deep_learning_float32()
    detector.detect()  # 初回の実行は計測しない
    time = timeit.timeit(lambda: detector.detect(), globals=globals(), number=loop)
    time = (time / loop) * 1000
    print("deep learning (float32) : {0}[ms]".format(time))

    #　ディープラーニング
    detector = deep_learning_float16()
    detector.detect()  # 初回の実行は計測しない
    time = timeit.timeit(lambda: detector.detect(), globals=globals(), number=loop)
    time = (time / loop) * 1000
    print("deep learning (float16) : {0}[ms]".format(time))

    #　ディープラーニング
    detector = deep_learning_uint8()
    detector.detect()  # 初回の実行は計測しない
    time = timeit.timeit(lambda: detector.detect(), globals=globals(), number=loop)
    time = (time / loop) * 1000
    print("deep learning (uint8) : {0}[ms]".format(time))


if __name__ == '__main__':
    main()
