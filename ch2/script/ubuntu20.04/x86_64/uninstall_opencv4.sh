#!/bin/bash

OPENCV_INSTALL_PATH=/usr/local
PYTHON_VERSION=3.8

sudo rm -rf ${OPENCV_INSTALL_PATH}/include/opencv4
sudo rm -rf ${OPENCV_INSTALL_PATH}/lib/python${PYTHON_VERSION}/dist-packages/cv2
sudo rm -rf ${OPENCV_INSTALL_PATH}/lib/cmake/opencv4
sudo rm ${OPENCV_INSTALL_PATH}/lib/libopencv_*
sudo rm ${OPENCV_INSTALL_PATH}/bin/opencv_*
sudo rm ${OPENCV_INSTALL_PATH}/bin/setup_vars_opencv4.sh
sudo rm -rf ${OPENCV_INSTALL_PATH}/share/licenses/opencv4
sudo rm -rf ${OPENCV_INSTALL_PATH}/share/opencv4
