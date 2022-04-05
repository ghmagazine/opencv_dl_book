# OpenCVセットアップ：ソースコード（Ubuntu 20.04：opencv_contribあり）

Ubuntu 20.04上にソースコードからOpenCVをopencv_contrib[^1]を含めてインストールする方法を紹介します。
以下の環境で動作確認を行いました。

- CPU：Intel Core i7-9800X CPU @ 3.80GHz
- OS：Ubuntu 20.04 64bit
- OpenCV：4.5.5

## 1. 依存パッケージインストール

本章ではOpenCVをビルド、インストールするために必要なパッケージのインストール手順を記載します。

### 1.1 開発ツール

以下のコマンドを実行して開発ツールのパッケージをインストールします。

```shell
sudo apt -y install build-essential
sudo apt -y install cmake
sudo apt -y install libpython3-dev
sudo apt -y install python3-numpy
```

### 1.2 行列演算

以下のコマンドを実行して行列演算のパッケージをインストールします。

```shell
sudo apt -y install libeigen3-dev
```

### 1.3 GUIフレームワーク

以下のコマンドを実行してGUIフレームワークのパッケージをインストールします。

```shell
sudo apt -y install libgtk-3-dev
```

### 1.4 画像フォーマット関連

以下のコマンドを実行して画像フォーマット関連パッケージをインストールします。

```shell
sudo apt -y install libjpeg-dev
sudo apt -y install libopenjp2-7-dev
sudo apt -y install libpng++-dev
sudo apt -y install libtiff-dev
sudo apt -y install libopenexr-dev
sudo apt -y install libwebp-dev
```

### 1.5 動画像関連

以下のコマンドを実行して動画像関連パッケージをインストールします。

```shell
sudo apt -y install libavcodec-dev
sudo apt -y install libavformat-dev
sudo apt -y install libavutil-dev
sudo apt -y install libswscale-dev
sudo apt -y install libavresample-dev
sudo apt -y install libgstreamer1.0-dev
sudo apt -y install libgstreamer-plugins-base1.0-dev
```

### 1.6 その他

以下のコマンドを実行してその他パッケージをインストールします。

```shell
sudo apt -y install libhdf5-dev
```

## 2. ビルド、インストール

以下のURLからopencv-4.5.5.tar.gzをダウンロードします。

Release OpenCV 4.5.5 · opencv/opencv：<https://github.com/opencv/opencv/releases/tag/4.5.5>

その後、以下のコマンドを実行して展開します。

```shell
tar xfvz opencv-4.5.5.tar.gz
```

opencv_contribを含める場合、以下のURLからopencv_contrib-4.5.5.tar.gzをダウンロードします。

Release 4.5.5 · opencv/opencv_contrib：<https://github.com/opencv/opencv_contrib/releases/tag/4.5.5>

その後、以下のコマンドを実行して展開します。

```shell
tar xfvz opencv_contrib-4.5.5.tar.gz
```

展開後、以下のコマンドを実行し、CMakeを使ってMakefileを生成します。  

```shell
cd opencv-4.5.5
mkdir -p build
cd build
cmake -D CMAKE_BUILD_TYPE=Release -D BUILD_TESTS=OFF -D BUILD_PERF_TESTS=OFF -D OPENCV_PYTHON_INSTALL_PATH=/usr/local/lib/python3.8/dist-packages -D OPENCV_EXTRA_MODULES_PATH=/path/to/opencv_contrib-4.5.5/modules ..
```

上記の例ではCMakeオプションを以下のように指定しています。

- `CMAKE_BUILD_TYPE`オプションを`Release`に指定することでリリースビルドとしている
- `BUILD_TESTS`オプションを`OFF`に指定することでテストプログラムのビルドを無効化している
- `BUILD_PERF_TESTS`オプションを`OFF`に指定することでパフォーマンステストプログラムのビルドを無効化している
- `OPENCV_PYTHON_INSTALL_PATH`オプションで`/usr/local/lib/python3.8/dist-packages`を指定している
  - Ubuntu 20.04では、aptでインストールされるPython 3.8の場合のパスであるため、お使いの環境によって必要に応じて書き換える
- `OPENCV_EXTRA_MODULES_PATH`オプションでopencv_contribのモジュールディレクトリのパスを指定している
  - `/path/to/opencv_contrib-4.5.5/modules`となっている箇所はお使いの環境に応じて書き換える

Makefile生成後、以下のコマンドを実行して、OpenCVをビルド、インストールします。メモリ搭載量が少ないマシン環境では`make -j`とすると、コンパイル時にメモリ不足で失敗することがあるため、`make -j`となっているところを`make`として、並列度を下げてください。

```shell
make -j
sudo make install
sudo ldconfig
```

## 3. 動作確認

以下のコマンドを実行してパッケージが正常にインストールできているかを確認します。

```python
python3
Python 3.8.10 (default, Nov 26 2021, 20:14:08)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> print(cv2.__version__)
4.5.5
```

確認するポイントは以下の通りです。

- `import cv2`を実行してcv2パッケージがインポートできること
- `print(cv2.__version__)`を実行してインストールしたOpenCVバージョンが表示されること
  - OpenCV 4.5.5をインストールしているため、`4.5.5`が表示される

[^1]: Repository for OpenCV's extra modules：<https://github.com/opencv/opencv_contrib>  
