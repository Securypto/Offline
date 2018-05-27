## Use this file to quickly install all required dependencies on a Debian Linux machine

export DSG_ROOT=$PWD

sudo apt-get update && sudo apt-get install -y \
	libssl-dev build-essential automake pkg-config libtool libffi-dev libgmp-dev \
	libgtk-3-dev libjpeg-dev libjpeg8-dev libjpeg62 libjpeg62-dev libopencv-dev libffi-dev libzbar-dev \
	git vlc xpdf python-pip python-gtk2-dev \
	python-setuptools ipython \
	python-opencv python-scipy python-numpy \
	python-pygame python-setuptools python-pil \
	python-qt4 python-qrtools && \
	apt install webkit-image-qt libqt4-dev


sudo pip install https://github.com/sightmachine/SimpleCV/zipball/develop
	
# pyethereum install might fail. in that case installing the requirements and then running the install script works
git clone https://github.com/ethereum/pyethereum/ $HOME/pyethereum && \
	cd $HOME/pyethereum && \
	pip install -r requirements.txt && \
	python setup.py install





git clone https://github.com/opencv/opencv.git $HOME/OpenCV/opencv && \
	cd $HOME/OpenCV/opencv && git checkout 3.3.1 &&
	git clone https://github.com/opencv/opencv_contrib.git $HOME/OpenCV/opencv_contrib && \
	cd $HOME/OpenCV/opencv_contrib && git checkout 3.3.1 && cd $HOME/OpenCV/opencv && \
	mkdir build && cd build && \
	cmake -D CMAKE_BUILD_TYPE=RELEASE \
	      -D CMAKE_INSTALL_PREFIX=/usr/local \
	      -D INSTALL_C_EXAMPLES=ON \
	      -D INSTALL_PYTHON_EXAMPLES=ON \
	      -D WITH_TBB=ON \
	      -D WITH_V4L=ON \
	      -D WITH_QT=ON \
	      -D WITH_OPENGL=ON \
	      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
	      -D BUILD_EXAMPLES=ON ..

make -j$(nproc) && \
	sudo make install && \
	sudo sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf' && \
	sudo ldconfig && sudo apt-get update

cd $DSG_ROOT && pip install -r requirements.txt


echo "Successfully installed all dependencies"
