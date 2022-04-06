# Dockerfile

## 動作確認環境

以下の環境で動作確認を行いました。

- CPU: Intel Core i7-9800X CPU @ 3.80GHz
- OS: Ubuntu 20.04 64bit
- Docker: Docker CE 20.10.9

## 動作確認OpenCVバージョン

| 環境構築方法 | 動作確認OpenCVバージョン |
|---|---|
| pip | 4.5.5 |
| Miniconda | 4.5.5 |
| Jupyter Notebook | 4.5.5 |
| Intel Inference Engine | 4.5.3 |

## 使い方

### pip

#### Dockerイメージ生成

以下のコマンドを実行してDockerイメージを生成します。  
ここで、`--build-arg`オプションでホストPCのアカウントのUID、GIDをDockerイメージ内のアカウントのUID、GIDと同じになるようにしています。

```shell
docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t pip/opencv:4.5.5 -f Dockerfile.pip .
```

#### Dockerコンテナ起動

以下のコマンドを実行してDockerコンテナを起動します。

```shell
docker run -it --rm -v $HOME:$HOME pip/opencv:4.5.5 bash
```

### Miniconda

#### Dockerイメージ生成

以下のコマンドを実行してDockerイメージを生成します。  
ここで、`--build-arg`オプションでホストPCのアカウントのUID、GIDをDockerイメージ内のアカウントのUID、GIDと同じになるようにしています。

```shell
docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t conda/opencv:4.5.5 -f Dockerfile.conda .
```

#### Dockerコンテナ起動

以下のコマンドを実行してDockerコンテナを起動します。

```shell
docker run -it --rm -v $HOME:$HOME conda/opencv:4.5.5 bash
```

### Jupyter Notebook

#### Dockerイメージ生成

以下のコマンドを実行してDockerイメージを生成します。  
ここで、`--build-arg`オプションでホストPCのアカウントのUID、GIDをDockerイメージ内のアカウントのUID、GIDと同じになるようにしています。

```shell
docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t conda-notebook/opencv:4.5.5 -f Dockerfile.notebook .
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

### Intel Inference Engine

#### Dockerイメージ生成

以下のコマンドを実行してDockerイメージを生成します。  
ここで、`--build-arg`オプションでホストPCのアカウントのUID、GIDをDockerイメージ内のアカウントのUID、GIDと同じになるようにしています。

```shell
docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t ie/opencv:4.5.3 -f Dockerfile.ie .
```

#### Dockerコンテナ起動

以下のコマンドを実行してDockerコンテナを起動します。

```shell
docker run -it --rm --device /dev/dri:/dev/dri -v $HOME:$HOME ie/opencv:4.5.3 bash
```
