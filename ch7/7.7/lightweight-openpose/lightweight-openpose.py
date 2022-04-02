import enum
import math
import os

import cv2
import numpy as np


# ジョイントタイプ（関節の名前）
class joints(enum.IntEnum):
    NOSE = 0
    SPINE_SHOULDER = enum.auto()  # 1
    SHOULDER_RIGHT = enum.auto()  # 2
    ELBOW_RIGHT = enum.auto()     # 3
    HAND_RIGHT = enum.auto()      # 4
    SHOULDER_LEFT = enum.auto()   # 5
    ELBOW_LEFT = enum.auto()      # 6
    HAND_LEFT = enum.auto()       # 7
    HIP_RIGHT = enum.auto()       # 8
    KNEE_RIGHT = enum.auto()      # 9
    FOOT_RIGHT = enum.auto()      # 10
    HIP_LEFT = enum.auto()        # 11
    KNEE_LEFT = enum.auto()       # 12
    FOOT_LEFT = enum.auto()       # 13
    EYE_RIGHT = enum.auto()       # 14
    EYE_LEFT = enum.auto()        # 15
    EAR_RIGHT = enum.auto()       # 16
    EAR_LEFT = enum.auto()        # 17


# ボーンリスト（関節の接続関係）
bones = [
    (joints.SPINE_SHOULDER, joints.SHOULDER_RIGHT),
    (joints.SPINE_SHOULDER, joints.SHOULDER_LEFT),
    (joints.SHOULDER_RIGHT, joints.ELBOW_RIGHT),
    (joints.ELBOW_RIGHT,    joints.HAND_RIGHT),
    (joints.SHOULDER_LEFT,  joints.ELBOW_LEFT),
    (joints.ELBOW_LEFT,     joints.HAND_LEFT),
    (joints.SPINE_SHOULDER, joints.HIP_RIGHT),
    (joints.HIP_RIGHT,      joints.KNEE_RIGHT),
    (joints.KNEE_RIGHT,     joints.FOOT_RIGHT),
    (joints.SPINE_SHOULDER, joints.HIP_LEFT),
    (joints.HIP_LEFT,       joints.KNEE_LEFT),
    (joints.KNEE_LEFT,      joints.FOOT_LEFT),
    (joints.SPINE_SHOULDER, joints.NOSE),
    (joints.NOSE,           joints.EYE_RIGHT),
    (joints.EYE_RIGHT,      joints.EAR_RIGHT),
    (joints.NOSE,           joints.EYE_LEFT),
    (joints.EYE_LEFT,       joints.EAR_LEFT)
]


# カラーテーブルを生成する関数
def get_colors():
    colors = [(255, 0, 0), (255, 85, 0), (255, 170, 0), (255, 255, 0), (170, 255, 0),
              (85, 255, 0), (0, 255, 0), (0, 255, 85), (0, 255, 170), (0, 255, 255),
              (0, 170, 255), (0, 85, 255), (0, 0, 255), (85, 0, 255), (170, 0, 255),
              (255, 0, 255), (255, 0, 170), (255, 0, 85)]
    return colors


# ボーンを描画する関数
def draw_bone(image, start_point, end_point, color, thickness=4):
    mean_x = int((start_point[0] + end_point[0]) / 2.0)
    mean_y = int((start_point[1] + end_point[1]) / 2.0)
    center = (mean_x, mean_y)
    diff = start_point - end_point
    length = math.sqrt(diff[0] * diff[0] + diff[1] * diff[1])
    axes = (int(length / 2.0), thickness)
    angle = int(math.degrees(math.atan2(diff[1], diff[0])))
    polygon = cv2.ellipse2Poly(center, axes, angle, 0, 360, 1)
    cv2.fillConvexPoly(image, polygon, color, cv2.LINE_AA)


def main():
    # キャプチャを開く
    directory = os.path.dirname(__file__)
    capture = cv2.VideoCapture(os.path.join(directory, "pose.jpg"))  # 画像ファイル
    # capture = cv2.VideoCapture(0)  # カメラ
    if not capture.isOpened():
        raise IOError("can't open capture!")

    # モデルを読み込む
    weights = os.path.join(directory, "human-pose-estimation.onnx")
    model = cv2.dnn_KeypointsModel(weights)

    # モデルの推論に使用するエンジンとデバイスを設定する
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # モデルの入力パラメーターを設定する
    scale = 1.0 / 255.0           # スケールファクター
    size = (256, 456)             # 入力サイズ（仮）
    mean = (128.0, 128.0, 128.0)  # 差し引かれる平均値
    swap = False                  # チャンネルの順番（True: RGB、False: BGR）
    crop = False                  # クロップ
    model.setInputParams(scale, size, mean, swap, crop)

    # カラーテーブルを取得する
    colors = get_colors()

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

        # モデルの入力サイズを設定する
        rows, cols, _ = image.shape
        size = (256, int((256 / cols) * rows))  # アスペクト比を保持する
        model.setInputSize(size)

        # キーポイントを検出する
        confidence_threshold = 0.6
        keypoints = model.estimate(image, confidence_threshold)

        # キーポイントを描画する
        for index, keypoint in enumerate(keypoints):
            point = tuple(map(int, keypoint.tolist()))
            radius = 5
            color = colors[index]
            thickness = -1
            cv2.circle(image, point, radius, color, thickness, cv2.LINE_AA)

        # ボーンを描画する
        for bone in bones:
            point1 = keypoints[bone[0]]
            point2 = keypoints[bone[1]]
            if (point1 == [-1, -1]).all() or (point2 == [-1, -1]).all():
                continue
            draw_bone(image, point1, point2, colors[bone[1]])

        # ヒートマップ画像を取得する
        # heatmaps = model.predict(image)
        # heatmaps = np.squeeze(np.array(heatmaps))  # (19, 58, 46)
        # heatmap = cv2.resize(heatmaps[-1], (cols, rows))
        # heatmap = cv2.applyColorMap(np.uint8(255. * (1.0 - heatmap)), cv2.COLORMAP_JET)

        # ヒートマップをアルファブレンドで可視化する
        # alpha = 0.5
        # beta  = 1.0 - alpha
        # blend = np.zeros(image.shape, np.uint8)
        # cv2.addWeighted(image, alpha, heatmap, beta, 0.0, blend)

        # 画像を表示する
        cv2.imshow("keypoint estimation", image)
        # cv2.imshow("heatmap", blend)
        key = cv2.waitKey(10)
        if key == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
