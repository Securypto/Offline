
import sys
from PyQt4 import QtGui, QtCore
import glob
import os
import shutil



#settings
dir_mainpath = os.path.dirname(os.path.realpath(__file__))+"/.."
dir_coin = dir_mainpath+"/coins"
import ConfigParser
configParser = ConfigParser.RawConfigParser()   
configFilePath = r''+dir_mainpath+'/settings.txt'
configParser.read(configFilePath)
Backupdironusb = configParser.get('DSG-CONFIG', 'Backupdironusb')
Qrshowspeed= float(configParser.get('DSG-CONFIG', 'Qrshowspeed'))
Qrmoviesplit= int(configParser.get('DSG-CONFIG', 'Qrmoviesplit'))


class BTCHDwallet(QtGui.QMainWindow):
    def __init__(self, passwdsend=None):
        super(BTCHDwallet, self).__init__()
        global passwd
        passwd=passwdsend

        self.setGeometry(0, 0, 480, 800)
        self.setWindowTitle("BTC HD Wallet")
        #disable right click
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setStyleSheet('font-size: 18pt; font-family: Courier;')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)



        #disable mouse pointer at DSG
        if (QtGui.QApplication.desktop().screenGeometry().width() < 500):
            self.setCursor(QtCore.Qt.BlankCursor)



        self.statusBar().showMessage('')

        self.btnclose = QtGui.QPushButton('', self)
        self.btnclose.clicked.connect(self.close_application)
        self.btnclose.resize(30,30)
        self.btnclose.setIcon(QtGui.QIcon(dir_mainpath+'/img/close.png'))
        self.btnclose.setIconSize(QtCore.QSize(24,24))
        self.btnclose.move(440,5)
        self.btnclose.show()


      #logo
        self.imglogo = QtGui.QLabel(self)
        self.imglogo.setGeometry(0,0,185,50)
        self.pixmaplogo = QtGui.QPixmap(dir_mainpath+"/img/logo50x185.png")
        self.imglogo.setPixmap(self.pixmaplogo)
        self.imglogo.show()



    def lanchkeyboardshow(self):
        command = "florence show" 
        proc = Popen([command], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        command = "florence move  0,490"
        proc = Popen([command], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        self.setGeometry(0, 0, 480, 490)


    def lanchkeyboardhide(self):
        command = "florence hide" 
        proc = Popen([command], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        self.setGeometry(0, 0, 480, 800)



    def close_application(self):
        self.close()



