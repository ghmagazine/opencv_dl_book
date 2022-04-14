# Ubuntu 20.04

## 1. opencv_contribなし

### 1.1 依存パッケージインストール

以下のスクリプトを実行して依存パッケージをインストールします。

```
./install_dependency_package.sh
```

### 1.2 OpenCV 4.5.5インストール（opencv_contribなし）

以下のスクリプトを実行してopencv_contribなしのOpenCV 4.5.5をインストールします。

```
./opencv4.5.5_build-ubuntu20.04.sh
```

## 2. opencv_contribなし、WITH_INF_ENGINE=ON

以下のスクリプトを実行して依存パッケージをインストールします。

### 2.1 依存パッケージインストール

```
./install_dependency_package.sh
```

### 2.2 Intel OpenVINO Toolkitインストール

以下のスクリプトを実行してIntel OpenVINO Toolkitをインストールします。

```
./install_openvino.sh
```

### 2.3 OpenCV 4.5.5インストール（opencv_contribなし、WITH_INF_ENGINE=ON）

以下のスクリプトを実行してWITH_INF_ENGINE=ONのOpenCV 4.5.5をインストールします。

```
./opencv4.5.5_ie_build-ubuntu20.04.sh
```

## 3. opencv_contribあり

### 3.1 依存パッケージインストール

以下のスクリプトを実行して依存パッケージをインストールします。

```
./install_dependency_package.sh
```

### 3.2 OpenCV 4.5.5インストール（opencv_contribあり）

以下のスクリプトを実行してopencv_contribありのOpenCV 4.5.5をインストールします。

```
./opencv4.5.5_contrib_build-ubuntu20.04.sh
```

## 4. opencv_contribあり、WITH_CUDA=ON

### 4.1 CUDA、cuDNNインストール

OpenCVでCUDA、cuDNNを使った実装を有効化するためにCUDA Toolkit、cuDNNをインストールします。  
ここではCUDA、cuDNNのインストール手順は割愛します。

- CUDA Toolkit：<https://developer.nvidia.com/cuda-toolkit>
- cuDNN：<https://developer.nvidia.com/cudnn>

### 4.2 依存パッケージインストール

以下のスクリプトを実行して依存パッケージをインストールします。

```
./install_dependency_package.sh
```

### 4.3 OpenCV 4.5.5インストール（opencv_contribあり、WITH_CUDA=ON）

以下のスクリプトを実行してopencv_contribあり、WITH_CUDA=ONのOpenCV 4.5.5をインストールします。

- 以下のスクリプトではビルド時間を短縮するため、`CUDA_ARCH_BIN`には動作環境のNVIDIA GPUに対応したCompute Capabilityを指定しています
  - 以下のスクリプトではサンプルとして`CUDA_ARCH_BIN="7.5"`となっているため環境に応じて書き換えてください
  - NVIDIA GPUに対応したCompute Capabilityは<https://developer.nvidia.com/cuda-gpus>から調べることができます

```
./opencv4.5.5_contrib_cuda_build-ubuntu20.04.sh
```

## 5. OpenCVアンインストール

以下のスクリプトをOpenCVをアンインストールします。このスクリプトではOpenCVは`/usr/local`以下にインストールされていることを想定しています。

```
./uninstall_opencv4.sh
```
