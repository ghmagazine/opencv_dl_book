# Dockerfile

## 動作確認環境

以下の環境で動作確認を行いました。

### 環境(1)

- マシン: Raspberry Pi 4 Model B
- OS: Ubuntu MATE 20.04 64bit
- Docker: Docker CE

### 環境(2)

- マシン: Raspberry Pi 4 Model B
- OS: Raspberry Pi OS(Bullseye)
- Docker: Docker CE

### 環境(3)

- マシン: M1 MacBook Air
- OS: macOS Big Sur
- Docker: Docker Desktop

## 動作確認OpenCVバージョン

| 環境構築方法 | 動作確認OpenCVバージョン |
|---|---|
| pip | 4.5.5 |
| Miniconda | 4.5.5 |
| Jupyter Notebook | 4.5.5 |

## 使い方

### pip

#### Dockerイメージ生成

以下のコマンドを実行してDockerイメージを生成します。

```shell
docker build -t pip/opencv:4.5.5 -f Dockerfile.pip .
```

#### Dockerコンテナ起動

以下のコマンドを実行してDockerコンテナを起動します。

```shell
docker run -it --rm -v $HOME:$HOME pip/opencv:4.5.5 bash
```

### Miniconda

#### Dockerイメージ生成

以下のコマンドを実行してDockerイメージを生成します。

```shell
docker build -t conda/opencv:4.5.5 -f Dockerfile.conda .
```

#### Dockerコンテナ起動

以下のコマンドを実行してDockerコンテナを起動します。

```shell
docker run -it --rm -v $HOME:$HOME conda/opencv:4.5.5 bash
```

### Jupyter Notebook

#### Dockerイメージ生成

以下のコマンドを実行してDockerイメージを生成します。

```shell
docker build -t conda-notebook/opencv:4.5.5 -f Dockerfile.notebook .
```

#### Dockerコンテナ起動

以下のコマンドを実行してDockerコンテナを起動します。

```shell
docker run -it --rm -v $HOME:$HOME -p 8888:8888 conda-notebook/opencv:4.5.5 bash
```

#### Jupyter Notebook起動

Dockerコンテナ上で以下のコマンドを実行してJupyter Notebookを起動します。

```shell
jupyter notebook --ip 0.0.0.0
```
