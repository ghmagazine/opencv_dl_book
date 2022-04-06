import numpy as np
import cv2

# ファイルからクラスの名前のリストを読み込む関数
def read_classes(file):
    classes = None
    with open(file, mode='r', encoding='utf-8') as f:
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

    # モデルを読み込む
    weights = 'yolov4.weights'
    config = 'yolov4.cfg'
    model = cv2.dnn_DetectionModel(weights, config)

    # モデルの推論に使用するエンジンとデバイスを設定する
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # モデルの入力パラメーターを設定する
    scale = 1.0 / 255.0    # スケールファクター
    size = (416, 416)      # 入力サイズ
    mean = (0.0, 0.0, 0.0) # 差し引かれる平均値
    swap = True            # チャンネルの順番（True: RGB、False: BGR）
    crop = False           # クロップ
    model.setInputParams(scale, size, mean, swap, crop)

    # NMS（Non-Maximum Suppression）をクラスごとに処理する
    model.setNmsAcrossClasses(False) # （True: 全体、False: クラスごと）

    # クラスリストとカラーテーブルを取得する
    names = 'coco.names'
    classes = read_classes(names)
    colors = get_colors(len(classes))

    image = cv2.imread('dog.jpg')

    # オブジェクトを検出する
    confidence_threshold = 0.5
    nms_threshold = 0.4
    class_ids, confidences, boxes = model.detect(image, confidence_threshold, nms_threshold)

    # 2次元配列(n, 1)から1次元配列(n, )に変換
    class_ids = np.array(class_ids).flatten()
    confidences = np.array(confidences).flatten()

    # 検出されたオブジェクトを描画する
    for class_id, confidence, box in zip(class_ids, confidences, boxes):
        class_name = classes[class_id]
        color = colors[class_id]
        thickness = 2
        cv2.rectangle(image, box, color, thickness, cv2.LINE_AA)

        result = '{0} ({1:.3f})'.format(class_name, confidence)
        point = (box[0], box[1] - 5)
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.5
        cv2.putText(image, result, point, font, scale, color, thickness, cv2.LINE_AA)

    # 画像を出力する
    cv2.imwrite('object_detection.png', image)

if __name__ == '__main__':
    main()
