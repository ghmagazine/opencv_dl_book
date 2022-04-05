import cv2

# 画像ファイルをカラーで読み込み
img = cv2.imread('yorkie.jpg', cv2.IMREAD_COLOR)

# cv2.TickMeterクラスのインスタンスを生成
timer = cv2.TickMeter()

for i in range(5):
    # タイマーをリセット
    timer.reset()

    # 処理時間計測開始
    timer.start()

    # 計測したい処理（グレースケール変換）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 処理時間計測終了
    timer.stop()

    # 計測結果をミリ秒単位にして取得
    measurement_time = timer.getTimeMilli()
    print(f"measurement_time = {measurement_time:.3f}[ms]")
