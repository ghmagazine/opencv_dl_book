# Ubuntu 22.04

## 1. opencv_contribなし

### 1.1 依存パッケージインストール

以下のスクリプトを実行して依存パッケージをインストールします。

```
./install_dependency_package.sh
```

### 1.2 OpenCV 4.5.5インストール（opencv_contribなし）

以下のスクリプトを実行してopencv_contribなしのOpenCV 4.5.5をインストールします。

```
./opencv4.5.5_build-ubuntu22.04.sh
```

## 2. opencv_contribあり

### 2.1 依存パッケージインストール

以下のスクリプトを実行して依存パッケージをインストールします。

```
./install_dependency_package.sh
```

### 2.2 OpenCV 4.5.5インストール（opencv_contribあり）

以下のスクリプトを実行してopencv_contribありのOpenCV 4.5.5をインストールします。

```
./opencv4.5.5_contrib_build-ubuntu22.04.sh
```

## 3. OpenCVアンインストール

以下のスクリプトを実行してOpenCVをアンインストールします。このスクリプトではOpenCVは`/usr/local`以下にインストールされていることを想定しています。

```
./uninstall_opencv4.sh
```
