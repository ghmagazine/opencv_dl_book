import cv2
import argparse

# コマンドライン引数パーサーのインスタンス生成
parser = argparse.ArgumentParser(
        description='This sample shows how to define custom OpenCV deep learning layers in Python. '
                    'Holistically-Nested Edge Detection (https://arxiv.org/abs/1504.06375) neural network '
                    'is used as an example model. Find a pre-trained model at https://github.com/s9xie/hed.')

# コマンドライン引数から入力画像、動画ファイル、カメラデバイスのファイルパスを指定する
parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')

# コマンドライン引数からprototxtのファイルパスを指定する
parser.add_argument('--prototxt', help='Path to deploy.prototxt', required=True)

# コマンドライン引数からCaffeモデルのファイルパスを指定する
parser.add_argument('--caffemodel', help='Path to hed_pretrained_bsds.caffemodel', required=True)
args = parser.parse_args()

# カスタムレイヤの実装
class CropLayer(object):
    def __init__(self, params, blobs):
        self.xstart = 0
        self.xend = 0
        self.ystart = 0
        self.yend = 0

    # 出力の形状を定義
    def getMemoryShapes(self, inputs):
        inputShape, targetShape = inputs[0], inputs[1]
        batchSize, numChannels = inputShape[0], inputShape[1]
        height, width = targetShape[2], targetShape[3]

        self.ystart = (inputShape[2] - targetShape[2]) // 2
        self.xstart = (inputShape[3] - targetShape[3]) // 2
        self.yend = self.ystart + height
        self.xend = self.xstart + width

        return [[batchSize, numChannels, height, width]]

    # レイヤの内部処理を実装
    def forward(self, inputs):
        return [inputs[0][:,:,self.ystart:self.yend,self.xstart:self.xend]]


# カスタムレイヤの登録
cv2.dnn_registerLayer('Crop', CropLayer)

# 学習済みモデルの読み込み
net = cv2.dnn.readNet(model=args.caffemodel, config=args.prototxt)

# ウィンドウ作成
cv2.namedWindow('Input', cv2.WINDOW_NORMAL)
cv2.namedWindow('Holistically-Nested Edge Detection', cv2.WINDOW_NORMAL)

# 動画ファイル、もしくはカメラを開く
cap = cv2.VideoCapture(args.input if args.input else 0)
while cv2.waitKey(1) < 0:
    # 動画ファイル、カメラ画像をキャプチャする
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv2.waitKey()
        break

    # 入力パラメーターから画像をブロブに変換する
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1.0, 
                               mean=(104.00698793, 116.66876762, 122.67891434),
                               swapRB=False, crop=False)

    # ネットワークの入力レイヤにブロブを設定する
    net.setInput(blob)

    # ネットワークを順伝搬して推論結果を取得する  
    out = net.forward()
    out = out[0, 0]
    out = cv2.resize(out, (frame.shape[1], frame.shape[0]))

    # 入力画像、出力画像をウィンドウ表示する
    cv2.imshow('Input', frame)
    cv2.imshow('Holistically-Nested Edge Detection', out)
