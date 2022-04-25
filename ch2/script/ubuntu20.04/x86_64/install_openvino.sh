#!/bin/bash

OPENVINO_VERSION=2022.1.0

# please refer to https://docs.openvino.ai/2022.1/openvino_docs_install_guides_installing_openvino_apt.html

# Install the GPG key for the repository
wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
sudo apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
echo "deb https://apt.repos.intel.com/openvino/2022 focal main" | sudo tee /etc/apt/sources.list.d/intel-openvino-2022.list
sudo apt update

# Install OpenVINO Runtime Using the APT Package Manager
sudo apt -y install openvino-${OPENVINO_VERSION}
sudo ln -s /opt/intel/openvino_2022 /opt/intel/openvino
source /opt/intel/openvino/setupvars.sh
echo "source /opt/intel/openvino/setupvars.sh" >> $HOME/.bashrc
