import cv2

model_dir = 'face-detection-adas-0001'
precision = 'FP32'
weights_file = 'face-detection-adas-0001.bin'
config_file = 'face-detection-adas-0001.xml'

weights_path = model_dir + '/' + precision + '/' + weights_file
config_path = model_dir + '/' + precision + '/' + config_file

# モデルを読み込む
model = cv2.dnn_DetectionModel(weights_path, config_path)

# モデルの推論に使用するエンジンとデバイスを設定する
model.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# モデルの入力パラメーターを設定する
scale = 1.0                  # スケールファクター
size = (672, 384)            # 入力サイズ
model.setInputParams(scale, size)

# 画像ファイルをカラーで読み込み
frame = cv2.imread('img_233.jpg', cv2.IMREAD_COLOR)

# 顔を検出する
confidence_threshold = 0.3
nms_threshold = 0.4
_, _, boxes = model.detect(frame, confidence_threshold, nms_threshold)

# 検出した顔のバウンディングボックスを描画する
for box in boxes:
    cv2.rectangle(frame, box, (0, 0, 255), 2, cv2.LINE_AA)
