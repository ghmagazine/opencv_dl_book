#!/bin/bash

sudo apt update

# development tools
sudo apt -y install \
  git \
  build-essential \
  cmake \
  curl \
  wget \
  gnupg \
  libpython3-dev \
  python3-setuptools \
  python3-numpy

# linear algebra
sudo apt -y install \
  libeigen3-dev \
  libatlas-base-dev \
  liblapacke-dev

# GUI toolkit
sudo apt -y install \
  libgtk-3-dev \
  qt5-default \
  libvtk7-qt-dev \
  freeglut3-dev

# image format library
sudo apt -y install \
  libjpeg-dev \
  libopenjp2-7-dev \
  libpng++-dev \
  libtiff-dev \
  libopenexr-dev \
  libwebp-dev

# video library
sudo apt -y install \
  libavcodec-dev \
  libavformat-dev \
  libavutil-dev \
  libswscale-dev \
  libavresample-dev \
  libgstreamer1.0-dev \
  libgstreamer-plugins-base1.0-dev \
  libhdf5-dev

