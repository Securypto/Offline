## Use this file to quickly install all required dependencies on a Linux machine, tested mint and ubuntu 16.0.4.2

export DSG_ROOT=$PWD

sudo apt-get update && sudo apt-get install -y \
python python-setuptools python-dev build-essential  python-qt4 python-setuptools  libjpeg62 \
libjpeg62-dev ipython python-opencv python-scipy python-numpy \
python-pygame python-setuptools python-pip git python-pil \
python-qrtools libgtk-3-dev python-gtk2-dev libssl-dev build-essential \
automake pkg-config libtool libffi-dev libgmp-dev python-setuptools

cd $DSG_ROOT && pip install -r requirements.txt


# pyethereum
git clone https://github.com/ethereum/pyethereum/ $HOME/pyethereum && \
cd $HOME/pyethereum && \
sudo python setup.py install

