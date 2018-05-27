#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
import glob
import os
import shutil
import tarfile
import time
import subprocess
from subprocess import Popen
from zipfile import ZipFile
import random
import string
from threading import Thread
import threading
import re
import cv2
from PIL.ImageQt import ImageQt
import qrcode
import qrtools

import base58
import binascii
import ecdsa
import ecdsa.der
import ecdsa.util
import hashlib

#tijdelijk uit
#from ethereum import utils

import dsgclass
from dsglanguages.english import *


#settings
dir_mainpath = os.path.dirname(os.path.realpath(__file__))
dir_coin = dir_mainpath+"/coins"
import ConfigParser
configParser = ConfigParser.RawConfigParser()   
configFilePath = r''+dir_mainpath+'/settings.txt'
configParser.read(configFilePath)
Backupdironusb = configParser.get('DSG-CONFIG', 'Backupdironusb')
Qrshowspeed= float(configParser.get('DSG-CONFIG', 'Qrshowspeed'))
Qrmoviesplit= int(configParser.get('DSG-CONFIG', 'Qrmoviesplit'))




class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(0, 0, 480, 800)
        self.setWindowTitle("DigiSaveBox")
        self.numberwronglogin = 0
        #disable right click
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.setStyleSheet('font-size: 18pt; font-family: Courier; background-image: url(img/logo100x370.png); background-repeat: no-repeat;')
        self.setStyleSheet('font-size: 18pt; font-family: Courier;')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)


        #disable mouse pointer at DSG
        if (QtGui.QApplication.desktop().screenGeometry().width() < 500):
            self.setCursor(QtCore.Qt.BlankCursor)





        #login box
        self.loginbox = QtGui.QLineEdit(LANG_PASSWORD,self)
        self.loginbox.setGeometry(0,50,480,50)
        self.loginbox.setAlignment(QtCore.Qt.AlignCenter)
        self.loginbox.setEchoMode(QtGui.QLineEdit.Password)
        regex=QtCore.QRegExp("[a-z-A-Z-0-9-!@#%_]+")
        validator = QtGui.QRegExpValidator(regex)
        self.loginbox.setValidator(validator)


        self.btnchecklogin = QtGui.QPushButton(LANG_LOGIN, self)
        self.btnchecklogin.clicked.connect(self.logintest)
        self.btnchecklogin.setGeometry(0,100,480,50)


        self.btnreset = QtGui.QPushButton(LANG_RESET, self)
        self.btnreset.clicked.connect(self.resetask)
        self.btnreset.setGeometry(0,150,480,50)


        self.mainmessageboard = QtGui.QLabel('Info:', self)
        self.mainmessageboard.setGeometry(0,200,480,290)
        self.mainmessageboard.setStyleSheet("QLabel { text-align: left; padding-left: 15px; padding-right: 15px;}")
        self.mainmessageboard.setWordWrap(True);

     


        self.qrboardleft = QtGui.QLabel("", self)
        self.qrboardright = QtGui.QLabel("", self)

        self.msgallround = QtGui.QLabel('', self)
        self.msgallround.setGeometry(466,80,350,350)
        self.msgallround.setWordWrap(True);



        self.statusBar().showMessage('')


        #shutdown icon
        self.btnshutdown = QtGui.QPushButton('', self)
        self.btnshutdown.clicked.connect(self.shutdown)
        self.btnshutdown.setIcon(QtGui.QIcon(dir_mainpath+'/img/shutdown.png'))
        self.btnshutdown.setIconSize(QtCore.QSize(50,50))
        self.btnshutdown.setGeometry(375,0,100,50)



        #menu icon
        self.btnmenu = QtGui.QPushButton('', self)
        self.btnmenu.clicked.connect(self.menushow)
        self.btnmenu.setIcon(QtGui.QIcon(dir_mainpath+'/img/menuicon.png'))
        self.btnmenu.setIconSize(QtCore.QSize(50,50))
        self.btnmenu.setGeometry(430,0,50,50)




      #logo
        self.imglogo = QtGui.QLabel(self)
        self.imglogo.setGeometry(0,0,185,50)
        self.pixmaplogo = QtGui.QPixmap(dir_mainpath+"/img/logo50x185.png")
        self.imglogo.setPixmap(self.pixmaplogo)
        self.imglogo.show()




        self.editor()
        self.home()
        self.statusBar()


        self.show()





    def createwalletbuttons(self):
        self.btn10 = QtGui.QPushButton(LANG_MESSAGING, self)
        self.btn10.setGeometry(0, 50, 480, 50)
        self.btn10.clicked.connect(self.windowmsg)
        self.btn10.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn10.setIcon(QtGui.QIcon(dir_mainpath+'/img/Messaging.png'))

        self.btn11 = QtGui.QPushButton(LANG_BTC_PAPER_WALLET, self)
        self.btn11.setGeometry(0,100, 480, 50)
        self.btn11.clicked.connect(self.windowbtcpaperwallet)
        self.btn11.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn11.setIcon(QtGui.QIcon(dir_mainpath+'/img/coinimages/btc.png'))


        self.btn22 = QtGui.QPushButton(LANG_BTC_HD_WALLET, self)
        self.btn22.setGeometry(0, 150, 480, 50)
        self.btn22.clicked.connect(self.windowbtchdwallet)
        self.btn22.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn22.setIcon(QtGui.QIcon(dir_mainpath+'/img/coinimages/btc.png'))


        self.btn16 = QtGui.QPushButton('ETH Wallet', self)
        self.btn16.setGeometry(0, 200, 480, 50)
        self.btn16.clicked.connect(self.windowethpaperwallet)
        self.btn16.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn16.setIcon(QtGui.QIcon(dir_mainpath+'/img/coinimages/eth.png'))


        self.btn12 = QtGui.QPushButton(LANG_MONERO_WALLET, self)
        self.btn12.setGeometry(0, 250, 480, 50)
        self.btn12.clicked.connect(self.windowmonero)
        self.btn12.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn12.setIcon(QtGui.QIcon(dir_mainpath+'/img/coinimages/xmr.png'))

        self.btn13 = QtGui.QPushButton('Komodo Wallet', self)
        self.btn13.setGeometry(0, 300, 480, 50)
        self.btn13.clicked.connect(self.windowmonero)
        self.btn13.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn13.setIcon(QtGui.QIcon(dir_mainpath+'/img/coinimages/kmd.png'))


        self.btn20 = QtGui.QPushButton('Zcash Wallet', self)
        self.btn20.setGeometry(0, 350, 480, 50)
        self.btn20.clicked.connect(self.windowmonero)
        self.btn20.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn20.setIcon(QtGui.QIcon(dir_mainpath+'/img/coinimages/zec.png'))

        self.btn21 = QtGui.QPushButton('Sia Wallet', self)
        self.btn21.setGeometry(0, 400, 480, 50)
        self.btn21.clicked.connect(self.windowmonero)
        self.btn21.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn21.setIcon(QtGui.QIcon(dir_mainpath+'/img/coinimages/sc.png'))


        self.btn14 = QtGui.QPushButton(LANG_CREATE_BACKUP, self)
        self.btn14.setGeometry(0, 700, 240, 50)
        self.btn14.clicked.connect(self.backup)


        self.btn15 = QtGui.QPushButton(LANG_CREATE_BACKUP_RESTORE, self)
        self.btn15.setGeometry(240, 700, 240, 50)
        self.btn15.clicked.connect(self.backuprestore)



        self.btn17 = QtGui.QPushButton(LANG_SHUTDOWN, self)
        self.btn17.setGeometry(0, 750, 160, 50)
        self.btn17.clicked.connect(self.shutdown)

        self.btn18 = QtGui.QPushButton(LANG_REBOOT, self)
        self.btn18.setGeometry(160, 750, 160, 50)
        self.btn18.clicked.connect(self.rebootsystem)

        self.btn19 = QtGui.QPushButton(LANG_LOGOUT, self)
        self.btn19.setGeometry(320, 750, 160, 50)
        self.btn19.clicked.connect(self.logout)


    def showwelcombuttons(self):

        self.btnmenu.show()

        self.btn10.show()
        self.btn11.show()
        self.btn12.show()
        self.btn13.show()

        self.btn14.show()
        self.btn15.show()
        self.btn17.show()
        self.btn18.show()
        self.btn19.show()

        self.btn16.show()
        self.btn20.show()
        self.btn21.show()
        self.btn22.show()

















    def hidewelcombuttons(self):


        self.btnmenu.hide()
        

        self.btn10.hide()
        self.btn11.hide()
        self.btn12.hide()
        self.btn13.hide()
        self.btn14.hide()
        self.btn15.hide()
        self.btn16.hide()
        self.btn17.hide()
        self.btn18.hide()
        self.btn19.hide()
        self.btn20.hide()
        self.btn21.hide()
        self.btn22.hide()
        self.mainmessageboard.hide()



    def home(self):
        self.createwalletbuttons()
        self.loginpage()
        self.lanchkeyboardshow()





    def loginpage(self):
        global passwd
        self.clearscreen()



        self.loginbox.show()
        self.btnchecklogin.show()
        self.btnreset.show()
        self.btnshutdown.show()
        self.btnmenu.hide()

        self.mainmessageboard.show()
        self.mainmessageboard.setText(LANG_STRONG_PASSWD)


        self.lanchkeyboardshow()


    def logintest(self):


        passwd = self.loginbox.text() 

        command = "openssl rsa -in "+dir_coin+"/MY-OWN-PRIVATE-KEY/MYOWN_id_rsa -check -passin pass:"+passwd
        resultcommand = os.popen(str(command)).read()
        #print resultcommand



        if "BEGIN RSA PRIVATE KEY" in resultcommand:

            self.lanchkeyboardhide()
            self.clearscreen()
            #self.createwalletbuttons()
            self.showwelcombuttons()
            #self.statusBar().showMessage(LANG_WELCOME_BACK, 2000)



        else:
                

            self.numberwronglogin += 1
            msgwronglogin = str(self.numberwronglogin)+"x "+LANG_WRONG_PASSWD
            #self.statusBar().showMessage(msgwronglogin, 2000)
            self.mainmessageboard.setText(msgwronglogin)
            if self.numberwronglogin > 3:
                command = "sudo reboot"
                resultcommand = os.popen(str(command)).read()



    def reset(self):


        self.clearscreen()
        self.loadingbegin()
        QtGui.QApplication.processEvents()


        treset = Thread(target=self.resetthread)
        treset.start()


        while treset.is_alive():
            self.loadingloop()
            QtGui.QApplication.processEvents()
            time.sleep(0.2)
                    

        self.loadingend(LANG_DEVICES_RESET_FINISH)
        QtGui.QApplication.processEvents()
        self.loginpage()





    def resetthread(self):

        passwd = self.loginbox.text() 


        #replace or create if needed
        if os.path.isdir(dir_coin):
            shutil.rmtree(dir_coin)
            os.mkdir(dir_coin)
        else:
            os.mkdir(dir_coin)

        
        #replace or create if needed
        myownprivatekeydir=dir_coin+"/MY-OWN-PRIVATE-KEY"
        if os.path.isdir(myownprivatekeydir):
            shutil.rmtree(myownprivatekeydir)
            os.mkdir(myownprivatekeydir)
        else:
            os.mkdir(myownprivatekeydir)


        tempdir=dir_coin+"/TEMP"
        if os.path.isdir(tempdir):
            shutil.rmtree(tempdir)
            os.mkdir(tempdir)
        else:
            os.mkdir(tempdir)


        sendmsgdir=dir_coin+"/CONTACTS-PUBLIC-KEYS"
        if os.path.isdir(sendmsgdir):
            shutil.rmtree(sendmsgdir)
            os.mkdir(sendmsgdir)
        else:
            os.mkdir(sendmsgdir)


        tempdir=dir_coin+"/TEMP"
        if os.path.isdir(tempdir):
            shutil.rmtree(tempdir)
            os.mkdir(tempdir)
        else:
            os.mkdir(tempdir)


        tempdir=dir_coin+"/BTC"
        if os.path.isdir(tempdir):
            shutil.rmtree(tempdir)
            os.mkdir(tempdir)
        else:
            os.mkdir(tempdir)




        tempdir=dir_coin+"/ETH"
        if os.path.isdir(tempdir):
            shutil.rmtree(tempdir)
            os.mkdir(tempdir)
        else:
            os.mkdir(tempdir)



     


        command = "ssh-keygen -t rsa -b 4096 -f '"+dir_coin+"/MY-OWN-PRIVATE-KEY/MYOWN_id_rsa' -N "+passwd
        resultcommand = os.popen(str(command)).read()
        #print resultcommand

        command = "openssl rsa -in '"+dir_coin+"/MY-OWN-PRIVATE-KEY/MYOWN_id_rsa'  -passin pass:"+passwd+" -pubout > '"+dir_coin+"/CONTACTS-PUBLIC-KEYS/MYOWN_PUBLIC_ID.pem.pub'"
        resultcommand = os.popen(str(command)).read()
        #print resultcommand


        filetormnu=dir_coin+"/MY-OWN-PRIVATE-KEY/MYOWN_id_rsa.pub"
        if os.path.exists(filetormnu):
            os.remove(filetormnu)


        #create dsgid
        enctextmsg=''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(100))
        enctextfile=dir_coin+"/dsgid"
        self.writeenctextfile(enctextfile,enctextmsg)


        self.loginbox.setText(LANG_PASSWORD)




    def resetask(self):

        passwd = self.loginbox.text() 




        if passwd == LANG_PASSWORD or len(passwd) < 10 :
            choice = QtGui.QMessageBox.warning(self, LANG_PASSWORD_ERROR,""+LANG_PASSWORD_CHOOSE_STRONG+"",QtGui.QMessageBox.Ok)


        else:

            choice = QtGui.QMessageBox.question(self, LANG_RESET_CONFIRM,LANG_RESET_CONFIRM1,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:
                self.resetask2()
            else:
                pass



    def resetask2(self):

        choice = QtGui.QMessageBox.question(self, LANG_RESET_CONFIRM,LANG_SURE+"\n"+LANG_DELETE_CONFIRM,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            self.reset()
        else:
            pass



    def clearscreen(self):

        self.qrboardleft.hide()
        self.qrboardright.hide()
        self.msgallround.hide()

        self.textEdit.hide()
        self.loginbox.hide()
        self.btnreset.hide()
        self.btnshutdown.hide()
        self.btnchecklogin.hide()
        self.hidewelcombuttons()
        self.statusBar().showMessage("")
        self.lanchkeyboardhide()
        QtGui.QApplication.processEvents()



    def getDigiSaveBoxPathUSB(self):
        
        command ="lsblk -o MOUNTPOINT"
        pathDigiSaveBox = os.popen(str(command)).read()
        for line in pathDigiSaveBox.splitlines():
            finddir= line+"/"+Backupdironusb
            if os.path.isdir(finddir):
                break
            else:
                finddir=""
        #print finddir
        return finddir
 


    def logout(self):
        global passwd
        self.loginbox.setText(LANG_PASSWORD)
        passwd=LANG_PASSWORD
        self.loginpage()







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










    def backup(self):

        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if Backupdironusb not in pathDigiSaveBoxUSB:
            #print LANG_USB_MISSING
            #self.statusBar().showMessage(LANG_USB_MISSING)
            self.loadingend(LANG_USB_MISSING)
        else:

            choice = QtGui.QMessageBox.question(self, LANG_SURE_CREATE_BACKUP,LANG_SURE_CREATE_BACKUP,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:


                self.loadingbegin()
                QtGui.QApplication.processEvents()


                tbackup = Thread(target=self.create_backup)
                tbackup.start()


                while tbackup.is_alive():
                    self.loadingloop()
                    QtGui.QApplication.processEvents()
                    time.sleep(0.2)
                    
                self.loadingend(LANG_BACKUP_FINISHED)
                QtGui.QApplication.processEvents()
                self.clearscreen()
                self.showwelcombuttons()

            else:
                pass
    







    def create_backup(self):

        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if Backupdironusb not in pathDigiSaveBoxUSB:
            #print LANG_USB_MISSING
            #self.statusBar().showMessage(LANG_USB_MISSING)
            self.loadingend(LANG_USB_MISSING)
        else:


            def exclude_files(filename):
                return filename.endswith('.py') 

            #tar to send
            file=pathDigiSaveBoxUSB+"/backup-device-digisavebox.tar.gz"
            tar3 = tarfile.open(file, "w:gz")
            tar3.add(dir_mainpath, arcname='', exclude=exclude_files)
            tar3.close()



    def backuprestore(self):

        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if Backupdironusb not in pathDigiSaveBoxUSB:
            #print LANG_USB_MISSING
            #self.statusBar().showMessage(LANG_USB_MISSING)
            self.loadingend(LANG_USB_MISSING)
        else:


            choice = QtGui.QMessageBox.question(self, LANG_SURE_RESTORE_BACKUP,LANG_SURE_RESTORE_BACKUP,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:
            
                if os.path.exists(pathDigiSaveBoxUSB+"/backup-device-digisavebox.tar.gz"):

                    self.loadingbegin()
                    QtGui.QApplication.processEvents()


                    tbackupres = Thread(target=self.restore_backup)
                    tbackupres.start()


                    while tbackupres.is_alive():
                        self.loadingloop()
                        QtGui.QApplication.processEvents()
                        time.sleep(0.2)
                        

                    self.loadingend(LANG_BACKUP_RESTORED)
                    QtGui.QApplication.processEvents()
                    self.logout()
                else:
                    choice = QtGui.QMessageBox.warning(self, LANG_BACKUP_HEADER,""+LANG_BACKUP_MISSING+"",QtGui.QMessageBox.Ok)

            else:
                pass
    






    def restore_backup(self):

        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if Backupdironusb not in pathDigiSaveBoxUSB:
            #print LANG_USB_MISSING
            #self.statusBar().showMessage(LANG_USB_MISSING)
            self.loadingend(LANG_USB_MISSING)
        else:



            tempdir=dir_coin
            if os.path.isdir(tempdir):
                shutil.rmtree(tempdir)




            tempdir=dir_coin+"/TEMP"
            if os.path.isdir(tempdir):
                shutil.rmtree(tempdir)

            tempdir=dir_coin+"/BTC"
            if os.path.isdir(tempdir):
                shutil.rmtree(tempdir)



            tempdir=dir_coin+"/ETH"
            if os.path.isdir(tempdir):
                shutil.rmtree(tempdir)



            tempdir=dir_coin+"/MY-OWN-PRIVATE-KEY"
            if os.path.isdir(tempdir):
                shutil.rmtree(tempdir)


            tempdir=dir_coin+"/TEMP"
            if os.path.isdir(tempdir):
                shutil.rmtree(tempdir)




            tempdir=dir_coin+"/CONTACTS-PUBLIC-KEYS"
            if os.path.isdir(tempdir):
                shutil.rmtree(tempdir)


            #untar to read
            file=pathDigiSaveBoxUSB+"/backup-device-digisavebox.tar.gz"
            tar = tarfile.open(file) 
            tar.extractall(dir_mainpath) # untar file into same directory
            tar.close()





    def setCode(self,position,x,y,w,h,text=""):        
            self.text = text      
            qrImg = qrcode.make(text)
            imgQt = ImageQt(qrImg.convert("RGB"))   # keep a reference!
            pixm = QtGui.QPixmap.fromImage(imgQt)
            if position == "qrboardleft":
                self.qrboardleft.setGeometry(x, y, w, h)
                self.qrboardleft.setPixmap(pixm.scaled(w,h,QtCore.Qt.KeepAspectRatio))
                self.qrboardleft.show()
            if position == "qrboardright":
                self.qrboardright.setGeometry(x, y, w, h)
                self.qrboardright.setPixmap(pixm.scaled(w,h,QtCore.Qt.KeepAspectRatio))
                self.qrboardright.show()






      


    def showqrmovie(self,textforqrmovie,x,y,w,h):


        arrayqrdatatoshow=self.split(textforqrmovie, Qrmoviesplit)
        totalqrcodes=len(arrayqrdatatoshow)

        #print totalqrcodes
        #print textforqrmovie
        md5checktotal=hashlib.md5(textforqrmovie).hexdigest()

        teller=0
        tellerplus=0
        self.qrboardleft.show()
        while teller < totalqrcodes and self.qrboardleft.isVisible() == True:
            tellerplus=teller+1
            #print tellerplus
            #print str(tellerplus)+"/"+str(totalqrcodes)

            dataforqrnow=arrayqrdatatoshow[teller]
            md5check=hashlib.md5(dataforqrnow).hexdigest()
            #print md5check

            #qrcodetextnow= str(tellerplus)+"|"+str(totalqrcodes)+","+dataforqrnow+",MD5:"+md5check
            qrcodetextnow= str(tellerplus)+":"+str(totalqrcodes)+","+dataforqrnow+","+md5check
            teller=teller+1

            if(tellerplus == totalqrcodes):
                teller=0
                #qrcodetextnow= qrcodetextnow+",MD5TOTAL:"+md5checktotal
                qrcodetextnow= qrcodetextnow+","+md5checktotal
            #
            #print qrcodetextnow

            self.setCode("qrboardleft",x,y,w,h,qrcodetextnow)
            time.sleep(Qrshowspeed)
            QtGui.QApplication.processEvents()


    


    def readenctextfile(self,enctextfile):
        passwd = self.loginbox.text()
        command = "cat '"+enctextfile+"' | base64 --decode | openssl rsautl -decrypt -inkey '"+dir_coin+"/MY-OWN-PRIVATE-KEY/MYOWN_id_rsa' -passin pass:"+passwd+""                      
        resultcommand = os.popen(str(command)).read()
        return resultcommand.strip()


    def writeenctextfile(self,enctextfile,enctextmsg):
        command = "echo "+enctextmsg+" | openssl  rsautl -encrypt -pubin -inkey '"+dir_coin+"/CONTACTS-PUBLIC-KEYS/MYOWN_PUBLIC_ID.pem.pub' | base64 > "+enctextfile+""
        resultcommand = os.popen(str(command)).read()





    def split(self,s, n):
      new_list = []
      for i in range(0, len(s), n):
        new_list.append(s[i:i+n])
      return new_list

    

    def allroundmsg(self,x,y,w,h,text=""):  
            self.msgallround.show()      
            self.msgallround.setWordWrap(True);
            self.msgallround.setGeometry(x,y,w,h)
            self.msgallround.setText(str(text))





    def getlistoffallpubaddressforqrsync(self):   

        global unenctextis             

        dsgid=self.readenctextfile(dir_coin+"/dsgid")
        unenctextis="DIGISAFEGUARDID:"+dsgid

        listaddres = glob.glob(dir_coin+"/BTC/*")
        for item in listaddres:
            privateaddresis=self.readenctextfile(item)
            privatekeyorg = self.WifToPrivateKey(privateaddresis)
            publicaddresis = self.keyToAddr(privatekeyorg)
            unenctextis=unenctextis+",BTC:"+publicaddresis
            

        listaddres = glob.glob(dir_coin+"/ETH/*")
        for item in listaddres:


            privateaddresis=self.readenctextfile(item)
            publicaddresis = utils.checksum_encode(utils.privtoaddr(privateaddresis))
            unenctextis=unenctextis+",ETH:"+publicaddresis





    def menushow(self):

        if (self.qrboardleft.isVisible() == False):

            self.loadingbegin()
            QtGui.QApplication.processEvents()

            tgetlistoffallpubaddressforqrsync = Thread(target=self.getlistoffallpubaddressforqrsync)
            tgetlistoffallpubaddressforqrsync.start()


            while tgetlistoffallpubaddressforqrsync.is_alive():
                self.loadingloop()
                QtGui.QApplication.processEvents()
                time.sleep(0.2)
                
            QtGui.QApplication.processEvents()
            self.clearscreen()
 




            self.hidewelcombuttons()
            self.btnmenu.show()

            self.msgallround.show()
            self.allroundmsg(17,530,446,270,INFO_ABOUT_QR_WALLET_SYNC)
            self.showqrmovie(unenctextis,0,50,480,480)  #text, positie x,y,w,h 
       




        else:

            self.showwelcombuttons()
            self.btnmenu.show()

            self.qrboardleft.hide()
            self.msgallround.hide()







    def base58encode(self,n):
        b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        result = ''
        while n > 0:
            result = b58[n%58] + result
            n /= 58
        return result

    def base256decode(self,s):
        result = 0
        for c in s:
            result = result * 256 + ord(c)
        return result

    def countLeadingChars(self,s, ch):
        count = 0
        for c in s:
            if c == ch:
                count += 1
            else:
                break
        return count

    def base58CheckEncode(self,version, payload):
        s = chr(version) + payload
        checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]
        result = s + checksum
        leadingZeros = self.countLeadingChars(result, '\0')
        return '1' * leadingZeros + self.base58encode(self.base256decode(result))

    def privateKeyToWif(self,key_hex):    
        return self.base58CheckEncode(0x80, key_hex.decode('hex'))
        
    def privateKeyToPublicKey(self,s):
        sk = ecdsa.SigningKey.from_string(s.decode('hex'), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        return ('\04' + sk.verifying_key.to_string()).encode('hex')


        
    def pubKeyToAddr(self,s):
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(s.decode('hex')).digest())
        return self.base58CheckEncode(0, ripemd160.digest())

    def keyToAddr(self,s):
        return self.pubKeyToAddr(self.privateKeyToPublicKey(s))



    def WifToPrivateKey(self,wif):
        first_encode = base58.b58decode(wif)
        private_key_full = binascii.hexlify(first_encode)
        private_key = private_key_full[2:-8]
        return private_key.upper()





    def shutdown(self):
        command = "sudo shutdown now -h"
        resultcommand = os.popen(str(command)).read()


    def rebootsystem(self):
        command = "sudo reboot"
        resultcommand = os.popen(str(command)).read()







    def editor(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)



    def loadingbegin(self):
        self.clearscreen()
        loadingtext="Progress"
        self.editor()
        self.textEdit.setReadOnly(True)
        self.textEdit.setHtml(loadingtext)
        #self.statusBar().showMessage(loadingtext)
        #QtGui.QApplication.processEvents()



    def loadingloop(self):  
        
        loadingtext = self.textEdit.toPlainText()
        if loadingtext.count('.') > 500:
            loadingtext="Progress"
        loadingtext=loadingtext+"."
        self.textEdit.setHtml(loadingtext)
        #self.statusBar().showMessage(loadingtext)
        #QtGui.QApplication.processEvents()
                


    def loadingend(self,loadingtext):  
        #self.textEdit.setHtml(loadingtext)  
        choice = QtGui.QMessageBox.information(self, LANG_INFO,loadingtext,QtGui.QMessageBox.Ok)
        #self.statusBar().showMessage(loadingtext)
        #QtGui.QApplication.processEvents()



    def windowbtcpaperwallet(self):
        passwd = self.loginbox.text() 
        self.dialog=dsgclass.digisaveboxbtcpaperwallet.Btcpaperwallet(passwdsend=passwd)
        self.dialog.show()


    def windowbtchdwallet(self):
        passwd = self.loginbox.text() 
        self.dialog=dsgclass.digisaveboxbtchdwallet.BTCHDwallet(passwdsend=passwd)
        self.dialog.show()


    def windowethpaperwallet(self):
        passwd = self.loginbox.text() 
        self.dialog=dsgclass.digisaveboxethpaperwallet.ETHpaperwallet(passwdsend=passwd)
        self.dialog.show()


    def windowmsg(self):
        passwd = self.loginbox.text() 
        self.dialog=dsgclass.digisaveboxmsg.msgpage(passwdsend=passwd)
        self.dialog.show()


###TODO

    def windowmonero(self):
        passwd = self.loginbox.text() 
        self.dialog=dsgclass.digisaveboxmonero.Monero(passwdsend=passwd)
        self.dialog.show()

        



   





        
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()






    
