import os
import timeit

import cv2
import numpy as np


class text_detector:
    def __init__(self):
        self._init_model()

    def _init_model(self):
        directory = os.path.dirname(__file__)
        weights = os.path.join(directory, "db/DB_IC15_resnet50.onnx")
        self._model = cv2.dnn_TextDetectionModel_DB(weights)

        self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        scale = 1.0 / 255.0
        size = (736, 1280)
        mean = (122.67891434, 116.66876762, 104.00698793)
        swap = False
        crop = False
        self._model.setInputParams(scale, size, mean, swap, crop)

        binary_threshold = 0.3
        polygon_threshold = 0.5
        max_candidates = 200
        unclip_ratio = 2.0
        self._model.setBinaryThreshold(binary_threshold)
        self._model.setPolygonThreshold(polygon_threshold)
        self._model.setMaxCandidates(max_candidates)
        self._model.setUnclipRatio(unclip_ratio)

    def detect_vertices(self, image):
        if self._model is None:
            raise IOError("failed model has not been created!")

        if image is None:
            raise IOError("failed image is empty!")

        vertices, confidences = self._model.detect(image)

        return vertices, confidences

    def detect_rotated_rectangles(self, image):
        if self._model is None:
            raise IOError("failed model has not been created!")

        if image is None:
            raise IOError("failed image is empty!")

        rotated_rectangles, confidences = self._model.detectTextRectangles(image)

        return rotated_rectangles, confidences


class text_recognizer:
    def __init__(self, model_file):
        self._init_model(model_file)

    def _init_model(self, model_file):
        directory = os.path.dirname(__file__)
        weights = os.path.join(directory, model_file)
        self._model = cv2.dnn_TextRecognitionModel(weights)

        self._model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self._model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        self._require_gray = False
        if "crnn.onnx" in weights:
            self._require_gray = True
        if "DenseNet_CTC.onnx" in weights:
            self._require_gray = True

        scale = 1.0 / 127.5
        size = (100, 32)
        mean = (127.5, 127.5, 127.5)
        swap = True
        crop = False
        self._model.setInputParams(scale, size, mean, swap, crop)

        type = "CTC-greedy"
        self._model.setDecodeType(type)

        if "crnn.onnx" in weights:
            vocabulary_file = os.path.join(directory, "crnn-ctc/alphabet_36.txt")
        if "crnn_cs.onnx" in weights:
            vocabulary_file = os.path.join(directory, "crnn-ctc/alphabet_94.txt")
        if "DenseNet_CTC.onnx" in weights:
            vocabulary_file = os.path.join(directory, "densenet-ctc/alphabet_36.txt")
        vocabularies = self._read_vocabularies(vocabulary_file)
        self._model.setVocabulary(vocabularies)

    def _read_vocabularies(self, file):
        vocabularies = None
        with open(file, mode='r', encoding="utf-8") as f:
            vocabularies = f.read().splitlines()
        return vocabularies

    def recognize(self, image):
        if self._model is None:
            raise IOError("failed model has not been created!")

        if image is None:
            raise IOError("failed image is empty!")

        channels = 1 if len(image.shape) == 2 else image.shape[2]
        if self._require_gray and channels != 1:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        text = self._model.recognize(image)
        return text


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


def draw_results(image, detector, recognizer):
    result_image = image.copy()

    vertices, _ = detector.detect_vertices(image)
    text_images = get_text_images(image, vertices)

    for vertex in vertices:
        vertex = np.array(vertex)
        close = True
        color = (0, 255, 0)
        thickness = 2
        cv2.polylines(result_image, [vertex], close, color, thickness, cv2.LINE_AA)

    texts = []
    for text_image in text_images:
        text = recognizer.recognize(text_image)
        texts.append(text)

    for text, vertex in zip(texts, vertices):
        position = vertex[1] - (0, 10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1.0
        color = (0, 0, 255)
        cv2.putText(result_image, text, position, font, scale, color, thickness, cv2.LINE_AA)

    return result_image


def main():
    loop = 100

    directory = os.path.dirname(__file__)
    image = cv2.imread(os.path.join(directory, "db/text.jpg"))
    if image is None:
        exit()

    channels = 1 if len(image.shape) == 2 else image.shape[2]
    if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    detector = text_detector()

    vertices, _ = detector.detect_vertices(image)
    text_images = get_text_images(image, vertices)
    text_image = text_images[0]

    # CRNN
    recognizer = text_recognizer("crnn-ctc/crnn.onnx")
    crnn_image = draw_results(image, detector, recognizer)
    time = timeit.timeit(lambda: recognizer.recognize(text_image), globals=globals(), number=loop)
    time = (time / loop) * 1000
    print("CRNN : {0}[ms]".format(time))

    # CRNN_CS
    recognizer = text_recognizer("crnn-ctc/crnn_cs.onnx")
    crnn_cs_image = draw_results(image, detector, recognizer)
    time = timeit.timeit(lambda: recognizer.recognize(text_image), globals=globals(), number=loop)
    time = (time / loop) * 1000
    print("CRNN_CS : {0}[ms]".format(time))

    # DenseNet_CTC
    recognizer = text_recognizer("densenet-ctc/DenseNet_CTC.onnx")
    densenet_ctc_image = draw_results(image, detector, recognizer)
    time = timeit.timeit(lambda: recognizer.recognize(text_image), globals=globals(), number=loop)
    time = (time / loop) * 1000
    print("DenseNet_CTC : {0}[ms]".format(time))

    cv2.imshow("text recognition (crnn)", crnn_image)
    cv2.imshow("text recognition (crnn_cs)", crnn_cs_image)
    cv2.imshow("text recognition (densenet_ctc)", densenet_ctc_image)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
