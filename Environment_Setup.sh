#!/bin/bash

# Download and install setuptools
if [ ! -f "setuptools-19.6.tar.gz" ]; then
    wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-19.6.tar.gz
fi

if [ ! -d "setuptools-19.6" ]; then
    tar -zxvf setuptools-19.6.tar.gz
    cd setuptools-19.6
    python3 setup.py build
    sudo python3 setup.py install
    cd ..
fi

# Download and install pip
if [ ! -f "pip-10.0.1.tar.gz" ]; then
    wget --no-check-certificate https://pypi.python.org/packages/source/p/pip/pip-10.0.1.tar.gz
fi

if [ ! -d "pip-10.0.1" ]; then
    tar -zvxf pip-10.0.1.tar.gz
    cd pip-10.0.1
    python3 setup.py build
    sudo python3 setup.py install
    cd ..
fi

# Upgrade pip
sudo pip install --upgrade pip
pip3 install testresources
sudo pip3 install --upgrade setuptools
sudo pip3 install --upgrade pip


sudo apt-get install python3-pip libopenblas-base libopenmpi-dev libomp-dev
pip3 install Cython
cd ./resources/wheel
cat torch-1.11.0-cp38-cp38-linux_aarch64.part.* > torch-1.11.0-cp38-cp38-linux_aarch64.tar.gz
tar -xzvf torch-1.11.0-cp38-cp38-linux_aarch64.tar.gz
cd ../../
pip3 install numpy ./resources/wheel/torch-1.11.0-cp38-cp38-linux_aarch64.whl
sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libopenblas-dev libavcodec-dev libavformat-dev libswscale-dev
git clone --branch release/0.12 https://github.com/pytorch/vision torchvision
cd torchvision
export BUILD_VERSION=0.12.0
python3 setup.py install --user
pip3 install numpy==1.23.5 protobuf==4.25.1 natsort==8.4.0 onnx==1.15.0 open3d==0.16.0 onnxruntime==1.12.0   pycuda==2021.1
pip3 install ultralytics
sudo apt-get install python3-pyqt5
pip3 install qimage2ndarray
pip3 uninstall opencv-python
pip3 install ../resources/wheel/PyGs-0.1-py3-none-any.whl
sudo apt-get install v4l-utils
