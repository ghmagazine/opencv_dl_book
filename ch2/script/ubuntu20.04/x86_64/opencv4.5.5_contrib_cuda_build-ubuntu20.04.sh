#!/bin/bash

GENERATOR_NAME="Unix Makefiles"
OPENCV_VERSION=4.5.5
PYTHON_VERSION=3.8
CUDA_ARCH_BIN="7.5"

# building
git clone https://github.com/opencv/opencv.git -b ${OPENCV_VERSION}
git clone https://github.com/opencv/opencv_contrib.git -b ${OPENCV_VERSION}
cd opencv
cmake \
-G "${GENERATOR_NAME}" \
-B build \
-D BUILD_CUDA_STUBS=OFF \
-D BUILD_DOCS=OFF \
-D BUILD_EXAMPLES=OFF \
-D BUILD_JASPER=OFF \
-D BUILD_JPEG=OFF \
-D BUILD_OPENEXR=OFF \
-D BUILD_PACKAGE=ON \
-D BUILD_PERF_TESTS=OFF \
-D BUILD_PNG=OFF \
-D BUILD_SHARED_LIBS=ON \
-D BUILD_TBB=OFF \
-D BUILD_TESTS=OFF \
-D BUILD_TIFF=OFF \
-D BUILD_WITH_DEBUG_INFO=ON \
-D BUILD_ZLIB=OFF \
-D BUILD_WEBP=OFF \
-D BUILD_opencv_apps=ON \
-D BUILD_opencv_calib3d=ON \
-D BUILD_opencv_core=ON \
-D BUILD_opencv_cudaarithm=ON \
-D BUILD_opencv_cudabgsegm=ON \
-D BUILD_opencv_cudacodec=OFF \
-D BUILD_opencv_cudafeatures2d=ON \
-D BUILD_opencv_cudafilters=ON \
-D BUILD_opencv_cudaimgproc=ON \
-D BUILD_opencv_cudalegacy=ON \
-D BUILD_opencv_cudaobjdetect=ON \
-D BUILD_opencv_cudaoptflow=ON \
-D BUILD_opencv_cudastereo=ON \
-D BUILD_opencv_cudawarping=ON \
-D BUILD_opencv_cudev=ON \
-D BUILD_opencv_dnn=ON \
-D BUILD_opencv_features2d=ON \
-D BUILD_opencv_flann=ON \
-D BUILD_opencv_gapi=ON \
-D BUILD_opencv_highgui=ON \
-D BUILD_opencv_imgcodecs=ON \
-D BUILD_opencv_imgproc=ON \
-D BUILD_opencv_java=OFF \
-D BUILD_opencv_js=OFF \
-D BUILD_opencv_ml=ON \
-D BUILD_opencv_objdetect=ON \
-D BUILD_opencv_photo=ON \
-D BUILD_opencv_python2=OFF \
-D BUILD_opencv_python3=ON \
-D BUILD_opencv_stitching=ON \
-D BUILD_opencv_ts=ON \
-D BUILD_opencv_video=ON \
-D BUILD_opencv_videoio=ON \
-D BUILD_opencv_world=OFF \
-D CMAKE_BUILD_TYPE=Release \
-D CUDA_ARCH_BIN=${CUDA_ARCH_BIN} \
-D CUDA_ARCH_PTX="" \
-D OPENCV_DNN_CUDA=ON \
-D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules \
-D OPENCV_PYTHON_INSTALL_PATH=/usr/local/lib/python${PYTHON_VERSION}/dist-packages \
-D WITH_1394=OFF \
-D WITH_CUBLAS=ON \
-D WITH_CUDA=ON \
-D WITH_CUFFT=ON \
-D WITH_CUDNN=ON \
-D WITH_EIGEN=ON \
-D WITH_FFMPEG=ON \
-D WITH_GDAL=OFF \
-D WITH_GPHOTO2=OFF \
-D WITH_GIGEAPI=OFF \
-D WITH_GSTREAMER=ON \
-D WITH_GTK=OFF \
-D WITH_INTELPERC=OFF \
-D WITH_IPP=ON \
-D WITH_IPP_A=OFF \
-D WITH_JASPER=ON \
-D WITH_JPEG=ON \
-D WITH_LAPACK=ON \
-D WITH_LIBV4L=ON \
-D WITH_OPENCL=OFF \
-D WITH_OPENCLAMDBLAS=OFF \
-D WITH_OPENCLAMDFFT=OFF \
-D WITH_OPENCL_SVM=OFF \
-D WITH_OPENEXR=ON \
-D WITH_OPENGL=ON \
-D WITH_OPENJPEG=ON \
-D WITH_OPENMP=OFF \
-D WITH_OPENNI=OFF \
-D WITH_PNG=ON \
-D WITH_PTHREADS_PF=ON \
-D WITH_PVAPI=OFF \
-D WITH_QT=ON \
-D WITH_TBB=OFF \
-D WITH_TIFF=ON \
-D WITH_UNICAP=OFF \
-D WITH_V4L=ON \
-D WITH_VTK=ON \
-D WITH_WEBP=ON \
-D WITH_XIMEA=OFF \
-D WITH_XINE=OFF \
.

cd build
make -j
sudo make install 
sudo ldconfig
