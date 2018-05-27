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
import struct
from PIL.ImageQt import ImageQt
import qrcode
import qrtools
import cv2
import base58
import binascii

#tijdelijk uit
#from ethereum import utils
#from ethereum import transactions
#import rlp


#import languages
from dsglanguages.english import *

#settings
dir_mainpath = os.path.dirname(os.path.realpath(__file__))+"/.."
dir_coin = dir_mainpath+"/coins"
import ConfigParser
configParser = ConfigParser.RawConfigParser()   
configFilePath = r''+dir_mainpath+'/settings.txt'
configParser.read(configFilePath)
Backupdironusb = configParser.get('DSG-CONFIG', 'Backupdironusb')






global publickey
global deleteorsavemassage





class ETHpaperwallet(QtGui.QMainWindow):
    def __init__(self, passwdsend=None):
        super(ETHpaperwallet, self).__init__()
        global passwd
        passwd=passwdsend

        self.setGeometry(0, 0, 480, 800)
        self.setWindowTitle("ETH Paper Wallet")
        #disable right click
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setStyleSheet('font-size: 18pt; font-family: Courier;')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)



        #disable mouse pointer at DSG
        if (QtGui.QApplication.desktop().screenGeometry().width() < 500):
            self.setCursor(QtCore.Qt.BlankCursor)



        # msg keep in archive
        extractAction7 = QtGui.QAction(LANG_KEEP_IN_ARCHIVE, self)
        extractAction7.triggered.connect(self.recreatetemp)
        self.toolBar7 = self.addToolBar("Extraction")
        self.toolBar7.addAction(extractAction7)


        self.addToolBarBreak()

        # msg delete
        extractAction5 = QtGui.QAction(LANG_DELETE_MESSAGE, self)
        extractAction5.triggered.connect(self.msg_delete)
        self.toolBar5 = self.addToolBar("Extraction")
        self.toolBar5.addAction(extractAction5)

        self.addToolBarBreak()


        # creae eth address
        extractAction11 = QtGui.QAction(LANG_SHOW_QR_BTC_ADDRESS, self)
        extractAction11.triggered.connect(self.showqrgenerateethaddress)
        self.toolbarshowqrgenerateethaddress = self.addToolBar("Extraction")
        self.toolbarshowqrgenerateethaddress.addAction(extractAction11)


        self.addToolBarBreak()

        # recreate keys
        extractAction12 = QtGui.QAction(LANG_BTC_RECREATE_ADDRESS, self)
        extractAction12.triggered.connect(self.generateethaddress)
        self.toolbarshowrecreate = self.addToolBar("Extraction")
        self.toolbarshowrecreate.addAction(extractAction12)

        self.addToolBarBreak()

        # rescan keys
        extractAction13 = QtGui.QAction(LANG_BTC_RESCAN_ADDRESS, self)
        extractAction13.triggered.connect(self.importprivatekeyeth)
        self.toolbarshowrescan = self.addToolBar("Extraction")
        self.toolbarshowrescan.addAction(extractAction13)



        self.addToolBarBreak()


        # qrcode pub e private show
        extractAction15 = QtGui.QAction(LANG_KEEP_SHOW_QR_FROM_ARCHIVE, self)
        extractAction15.triggered.connect(self.qrcodepubenprivateshowarchive)
        self.toolBarqrpublicenprivatearchive = self.addToolBar("Extraction")
        self.toolBarqrpublicenprivatearchive.addAction(extractAction15)

        self.addToolBarBreak()

        # qrcode raw transaction
        extractAction16 = QtGui.QAction(LANG_SHOW_RAW_SIGNED, self)
        extractAction16.triggered.connect(self.showtransactionrawtext)
        self.toolBartransactionraw = self.addToolBar("Extraction")
        self.toolBartransactionraw.addAction(extractAction16)


        self.addToolBarBreak()

        # sign transaction
        extractAction14 = QtGui.QAction(LANG_BTC_SIGN, self)
        extractAction14.triggered.connect(self.signatransaction)
        self.toolbarsign = self.addToolBar("Extraction")
        self.toolbarsign.addAction(extractAction14)


        self.addToolBarBreak()

        # text raw transaction
        extractAction17 = QtGui.QAction(LANG_SHOW_QR_SIGNED, self)
        extractAction17.triggered.connect(self.showtransactionqrcode)
        self.toolBartransactionqrcode = self.addToolBar("Extraction")
        self.toolBartransactionqrcode.addAction(extractAction17)




        #Default messageboard
        self.messageboard = QtGui.QLabel("", self)
        self.messageboard.move(10,150)


        self.qrboardleft = QtGui.QLabel("", self)
        self.qrboardright = QtGui.QLabel("", self)


        self.msgallround = QtGui.QLabel(INFO_ABOUT_PUBLIC_KEY_FOR_MESSAGING, self)
        self.msgallround.setGeometry(17,440,350,350)
        self.msgallround.setWordWrap(True);


        self.messageboardprivatepublickey1 = QtGui.QLabel(LANG_PRIVATE_KEY, self)
        self.messageboardprivatepublickey1.setGeometry(370,50,110,350)
        self.messageboardprivatepublickey2 = QtGui.QLabel(LANG_PUBLIC_KEY, self)
        self.messageboardprivatepublickey2.setGeometry(370,440,110,350)

        self.messageboardprivatepublickey1.setStyleSheet('color: red; font-weight: bold;')
        self.messageboardprivatepublickey2.setStyleSheet('color: green; font-weight: bold;')




        

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



        self.editor()
        self.home()
        self.statusBar()

        self.show()


    def home(self):



        self.dropdownmsg()
        self.createwalletbuttons()
        self.clearscreen()
        self.walletpage()
        #self.lanchkeyboardshow()



    def walletpage(self):
        self.clearscreen()
        self.showwalletbuttons()


       



    def clearscreen(self):


        global stopcam
        stopcam="yes"

        self.textEdit.hide()
       



        self.comboBoxmsg.deleteLater()
        self.dropdownmsg()
        self.comboBoxmsg.hide()


       
        self.messageboard.hide()
        self.qrboardleft.hide()
        self.qrboardright.hide()
        self.messageboardprivatepublickey1.hide()
        self.messageboardprivatepublickey2.hide()

        self.hidewalletbuttons()
        self.toolBar5.hide() #delte button
        self.toolBar7.hide() #keep in archive button
        self.toolbarshowqrgenerateethaddress.hide()
        self.toolbarshowrecreate.hide()
        self.toolbarshowrescan.hide()
        self.toolbarsign.hide()
        self.toolBarqrpublicenprivatearchive.hide()
        self.msgallround.hide()



        self.statusBar().showMessage("")

        self.lanchkeyboardhide()


        self.toolBartransactionraw.hide()
        self.toolBartransactionqrcode.hide()

        self.messageboard.clear()

        self.imglogo.hide()


        QtGui.QApplication.processEvents()








    def createwalletbuttons(self):
        self.btn10 = QtGui.QPushButton(LANG_ETH_CREATE_ADDRESS, self)
        self.btn10.setGeometry(0, 50, 480, 50)
        self.btn10.clicked.connect(self.generateethaddress)
        self.btn10.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn10.setIcon(QtGui.QIcon(dir_mainpath+'/img/plus.png'))


        self.btn11 = QtGui.QPushButton(LANG_ETH_IMPORT_ADDRESS, self)
        self.btn11.setGeometry(0, 100, 480, 50)
        self.btn11.clicked.connect(self.importprivatekeyeth)
        self.btn11.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn11.setIcon(QtGui.QIcon(dir_mainpath+'/img/qr.png'))


        self.btn13 = QtGui.QPushButton(LANG_ETH_SIGN_ADDRESS, self)
        self.btn13.setGeometry(0, 150, 480, 50)
        self.btn13.clicked.connect(self.readmessages)
        self.btn13.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn13.setIcon(QtGui.QIcon(dir_mainpath+'/img/archive.png'))


    def hidewalletbuttons(self):
        self.btn10.hide()
        self.btn11.hide()
        self.btn13.hide()
        self.imglogo.hide()


    def showwalletbuttons(self):
        self.btn10.show()
        self.btn11.show()
        self.btn13.show()
        self.imglogo.show()



    def editor(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)










    def dropdownmsg(self):

        self.comboBoxmsg = QtGui.QComboBox(self)
        self.comboBoxmsg.move(5, 50)
        self.comboBoxmsg.resize(700,30)  




    def allroundmsg(self,x,y,w,h,text=""):  
            self.msgallround.show()      
            self.msgallround.setWordWrap(True);
            self.msgallround.setGeometry(x,y,w,h)
            self.msgallround.setText(str(text))







    def readmessages(self):



        self.clearscreen()

        self.listcontactskey = glob.glob(dir_coin+"/ETH/*")
        self.toolBar7.show()


        if len(self.listcontactskey) < 1:
            self.statusBar().showMessage(LANG_NO_MESSAGE)
            self.comboBoxmsg.hide()
        else:



            self.comboBoxmsg.show()
            self.comboBoxmsg.clear()


            self.comboBoxmsg.currentIndexChanged.connect(self.midfunction1)



            self.comboBoxmsg.addItem(LANG_SELECT_FROM_BTC_KEYS,"NIKS2")

            loadingtext="Loading"
            self.comboBoxmsg.setEnabled(False)

            for item in self.listcontactskey:
                

                if loadingtext.count('.') > 5:
                    loadingtext="Loading"
                loadingtext=loadingtext+"."
                self.statusBar().showMessage(loadingtext)
                QtGui.QApplication.processEvents()



                privateaddresis=self.readenctextfile(item)
                #print privateaddresis

                
                publicaddresis = utils.checksum_encode(utils.privtoaddr(privateaddresis))

                #print publicaddresis

                self.comboBoxmsg.addItem(publicaddresis,item)



            self.comboBoxmsg.setEnabled(True)
            self.statusBar().showMessage("")
            QtGui.QApplication.processEvents()





    def midfunction1(self,index):
        method = self.comboBoxmsg.itemData(index).toPyObject()
        if method == "NIKS2":
            pass
        else:
            self.msg_unencrypte(method)
                








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





    def loadingbegin(self):
        self.clearscreen()
        loadingtext="Progress"
        self.editor()
        self.textEdit.setReadOnly(True)
        self.textEdit.setHtml(loadingtext)
        #self.statusBar().showMessage(loadingtext)
        QtGui.QApplication.processEvents()



    def loadingloop(self):  
        
        loadingtext = self.textEdit.toPlainText()
        if loadingtext.count('.') > 500:
            loadingtext="Progress"  
        loadingtext=loadingtext+"."
        self.textEdit.setHtml(loadingtext)
        #self.statusBar().showMessage(loadingtext)
        QtGui.QApplication.processEvents()
                

    def loadingend(self,loadingtext):  
        #self.textEdit.setHtml(loadingtext)  
        choice = QtGui.QMessageBox.information(self, LANG_INFO,loadingtext,QtGui.QMessageBox.Ok)
        #self.statusBar().showMessage(loadingtext)
        #QtGui.QApplication.processEvents()



    










    def msg_delete(self):




        choice = QtGui.QMessageBox.question(self, LANG_DELETE_MESSAGE,LANG_SURE,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:

            choice = QtGui.QMessageBox.question(self, LANG_DELETE_MESSAGE,LANG_SURE2,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:


                urlpriv = str(deleteorsavemassage)

                if os.path.exists(urlpriv):
                    os.remove(urlpriv)



                self.walletpage()
           


            else:
                pass


        else:
            pass









    def recreatetemp(self):

        global stopcam
        stopcam="yes"
        self.walletpage()



    def msg_unencrypte(self,msgtoreadfile):

      
        urlpriv = str(msgtoreadfile)

        global deleteorsavemassage
        deleteorsavemassage=urlpriv

        global privatekeyusetosignnowarchive
        privatekeyusetosignnowarchive = self.readenctextfile(urlpriv)

        global publickeyusetosignnowarchive
        publickeyusetosignnowarchive = utils.checksum_encode(utils.privtoaddr(privatekeyusetosignnowarchive))



        self.clearscreen()
        self.toolBar5.show()
        self.toolbarsign.show()
        self.toolBar7.show()
        self.toolBarqrpublicenprivatearchive.show()



        msgshowkeys ="<hr><b><font color='green'>Public Address:</font></b><br>"+publickeyusetosignnowarchive+"<br><hr><b><font color='red'>Private Key:</font></b><br>"+privatekeyusetosignnowarchive+"<br><hr>"
        self.editor()
        self.textEdit.setReadOnly(True)
        self.textEdit.setHtml(msgshowkeys)   
 







    def signatransaction(self):

        global tx_signed
        global to
        global nonce
        global amount

        tx_signed=""

        self.clearscreen()
        self.toolBar7.show()
        self.toolbarsign.show()

        foundkeyfromqrcode=self.camscanner()


        foundkeyfromqrcodenow = str(foundkeyfromqrcode.strip())
        privatekeyusetosignnow = str(privatekeyusetosignnowarchive.strip())

    
        self.clearscreen()
        self.toolBar7.show()
        self.toolbarsign.show()


        qrsplit = foundkeyfromqrcodenow.split("|")


        to=str(qrsplit[0])
        nonce=int(qrsplit[1])
        amount=float(qrsplit[2])
        

        #print to
        #print amount
        #print nonce

        if to !="" and amount !="" and nonce!="":

            amounttosend=amount*1000000000000000000
            #nonce, gasprice, startgas, to, value, data, v, r, s 
            #tx = transactions.Transaction(0, 21000000000, 21000, to, 1000000000, "").sign(frompaperprivte).to_dict()
            tx = transactions.Transaction(nonce, 21000000000, 21000, to, int(amounttosend), "").sign(privatekeyusetosignnow)
            tx_signed= rlp.encode(tx).encode('hex')

        


        self.clearscreen()
        self.toolBar7.show()

        if tx_signed !="":

            self.showtransactionqrcode()


        else:
            self.statusBar().showMessage("ERROR!!! I Cant sign the transaction.")
            self.toolbarsign.show()









    def showtransactionqrcode(self):
        global tx_signed
        self.clearscreen()
        self.toolBar7.show()
        self.toolBartransactionraw.show()
        self.setCode("qrboardleft",17,100,350,350,tx_signed)



        msgshowsigned="Sending:"+str(amount)+" ETH to:"+str(to)
        self.allroundmsg(0,450,480,350,msgshowsigned)





    def showtransactionrawtext(self):
        global tx_signed
        self.clearscreen()
        self.toolBar7.show()
        self.toolBartransactionqrcode.show()

        self.editor()
        self.textEdit.setReadOnly(True)
        self.textEdit.setHtml(tx_signed)



    def camscanner(self):

        global stopcam
        stopcam="yes"
        imagetoshow=dir_coin+"/TEMP/cam.jpg"
        cam = cv2.VideoCapture(0)

        width = self.geometry().width()
        height = self.geometry().height()-80
        self.messageboard.setGeometry(0, 80, width, height)
        self.messageboard.setScaledContents(True);
        self.messageboard.show()

        foundkeyfromqrcode="NULL"
 
        stopcam="no"
        while stopcam =="no":
           
            s, im = cam.read() # captures image
            cv2.imwrite(imagetoshow,im) # writes image test.bmp to disk


            self.messageboard.setPixmap(QtGui.QPixmap(imagetoshow))  
            QtGui.QApplication.processEvents()
            qr = qrtools.QR()
            qr.decode(imagetoshow)
            foundkeyfromqrcode= qr.data.encode('ascii')

            if foundkeyfromqrcode !="NULL":
                stopcam="yes"

        
        cam.release()
        del cam
        print "Cam stoped"
        os.remove(imagetoshow)
        return foundkeyfromqrcode



    def importprivatekeyeth(self):   
        self.clearscreen()
        self.toolBar7.show()
        self.toolbarshowrescan.show()

        foundkeyfromqrcode=self.camscanner()


        self.clearscreen()
        self.toolBar7.show()
        self.toolbarshowrescan.show()



        try:
            self.checkprivatepubliceth(foundkeyfromqrcode)
        except:
            pass
            self.statusBar().showMessage("ERROR!!! Wrong privatekey.")






        

    def checkprivatepubliceth(self,foundkeyfromqrcode):

        publickeygevonden = utils.checksum_encode(utils.privtoaddr(foundkeyfromqrcode))

        print publickeygevonden


        global privatekeygenerated
        global publickeygenerated


        self.clearscreen()
        self.toolBar7.show()
        self.toolbarshowrescan.show()
        self.toolbarshowqrgenerateethaddress.show()

        privatekeygenerated = foundkeyfromqrcode
        publickeygenerated = publickeygevonden


        msgshowkeys ="<b>Private Key:</b><br>"+privatekeygenerated+"<br><b>Public Address:</b><br>"+publickeygenerated+""
        self.editor()
        self.textEdit.setReadOnly(True)
        self.textEdit.setHtml(msgshowkeys)

        



  
    def generateethaddress(self):
        

        global privatekeygenerated
        global publickeygenerated


        self.clearscreen()
        self.toolBar7.show()

        # Generate a random private key
        private_key_raw = utils.sha3(os.urandom(4096))
        publickeygenerated = utils.checksum_encode(utils.privtoaddr(private_key_raw))
        privatekeygenerated=utils.encode_hex(private_key_raw)


        #print private_key
        #print privatekeygenerated
        #print publickeygenerated

        msgshowkeys ="<b>Private Key:</b><br>"+privatekeygenerated+"<br><b>Public Address:</b><br>"+publickeygenerated+""
        self.editor()
        self.textEdit.setReadOnly(True)
        self.textEdit.setHtml(msgshowkeys)

        self.toolbarshowqrgenerateethaddress.show()
        self.toolbarshowrecreate.show()





    def showqrgenerateethaddress(self):


        global publickey
        publickey = "MYOWN_PUBLIC_ID.pem.pub"
        self.textEdit.setReadOnly(True)
        self.textEdit.setText(privatekeygenerated)

        text = self.textEdit.toPlainText()

        randomnaamwordt=''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(100))
        self.writeenctextfile(dir_coin+"/ETH/"+randomnaamwordt,text)

        self.loadingend(LANG_SAVED_BUT_WARN_BACKUP)
        QtGui.QApplication.processEvents()
        



        self.clearscreen()
        self.toolBar7.show()
        qrcodeprivate=self.setCode("qrboardleft",17,50,350,350,privatekeygenerated)
        qrcodepublic=self.setCode("qrboardright",17,440,350,350,publickeygenerated)


        self.messageboardprivatepublickey1.setText(LANG_PRIVATE_KEY)
        self.messageboardprivatepublickey2.setText(LANG_PUBLIC_KEY)

        self.messageboardprivatepublickey1.show()
        self.messageboardprivatepublickey2.show()






    def qrcodepubenprivateshowarchive(self):
        global privatekeyusetosignnowarchive
        global publickeyusetosignnowarchive


        self.clearscreen()
        self.toolBar7.show()
        qrcodeprivate=self.setCode("qrboardleft",17,50,350,350,privatekeyusetosignnowarchive)
        qrcodepublic=self.setCode("qrboardright",17,440,350,350,publickeyusetosignnowarchive)


        self.messageboardprivatepublickey1.setText(LANG_PRIVATE_KEY)
        self.messageboardprivatepublickey2.setText(LANG_PUBLIC_KEY)

        self.messageboardprivatepublickey1.show()
        self.messageboardprivatepublickey2.show()










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

            

    def readenctextfile(self,enctextfile):
        command = "cat '"+enctextfile+"' | base64 --decode | openssl rsautl -decrypt -inkey '"+dir_coin+"/MY-OWN-PRIVATE-KEY/MYOWN_id_rsa' -passin pass:"+passwd+""                      
        resultcommand = os.popen(str(command)).read()
        return resultcommand.strip()


    def writeenctextfile(self,enctextfile,enctextmsg):
        command = "echo "+enctextmsg+" | openssl  rsautl -encrypt -pubin -inkey '"+dir_coin+"/CONTACTS-PUBLIC-KEYS/MYOWN_PUBLIC_ID.pem.pub' | base64 > "+enctextfile+""
        resultcommand = os.popen(str(command)).read()






    def close_application(self):
        global stopcam
        stopcam="yes"
        self.close()






        









    