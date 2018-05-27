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
import ecdsa
import ecdsa.der
import ecdsa.util
import hashlib
import struct
from PIL.ImageQt import ImageQt
import qrcode
import qrtools
from transactions import Transactions
import cv2
import base58
import binascii
import bitcoin


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
Qrshowspeed= float(configParser.get('DSG-CONFIG', 'Qrshowspeed'))
Qrmoviesplit= int(configParser.get('DSG-CONFIG', 'Qrmoviesplit'))




global publickey
global deleteorsavemassage




class Btcpaperwallet(QtGui.QMainWindow):
    def __init__(self, passwdsend=None):
        super(Btcpaperwallet, self).__init__()
        global passwd
        passwd=passwdsend

        self.setGeometry(0, 0, 480, 800)
        self.setWindowTitle("BTC Paper Wallet")
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


        # creae btc address
        extractAction11 = QtGui.QAction(LANG_SHOW_QR_BTC_ADDRESS, self)
        extractAction11.triggered.connect(self.showqrgeneratebtcaddress)
        self.toolbarshowqrgeneratebtcaddress = self.addToolBar("Extraction")
        self.toolbarshowqrgeneratebtcaddress.addAction(extractAction11)


        self.addToolBarBreak()

        # recreate keys
        extractAction12 = QtGui.QAction(LANG_BTC_RECREATE_ADDRESS, self)
        extractAction12.triggered.connect(self.generatebtcaddress)
        self.toolbarshowrecreate = self.addToolBar("Extraction")
        self.toolbarshowrecreate.addAction(extractAction12)

        self.addToolBarBreak()

        # rescan keys
        extractAction13 = QtGui.QAction(LANG_BTC_RESCAN_ADDRESS, self)
        extractAction13.triggered.connect(self.importprivatekeybtc)
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
        #extractAction16 = QtGui.QAction(LANG_SHOW_RAW_SIGNED, self)
        #extractAction16.triggered.connect(self.showtransactionrawtext)
        #self.toolBartransactionraw = self.addToolBar("Extraction")
        #self.toolBartransactionraw.addAction(extractAction16)


        self.addToolBarBreak()

        # sign transaction
        extractAction14 = QtGui.QAction(LANG_BTC_SIGN, self)
        extractAction14.triggered.connect(self.signatransaction)
        self.toolbarsign = self.addToolBar("Extraction")
        self.toolbarsign.addAction(extractAction14)


        self.addToolBarBreak()

        # text raw transaction
        #extractAction17 = QtGui.QAction(LANG_SHOW_QR_SIGNED, self)
        #extractAction17.triggered.connect(self.showtransactionqrcode)
        #self.toolBartransactionqrcode = self.addToolBar("Extraction")
        #self.toolBartransactionqrcode.addAction(extractAction17)




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


       

    def base_encode(self,v):
        chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$*+-./:'
        bingevonden= binascii.unhexlify(v)

        long_value = 0L
        for (i, c) in enumerate(bingevonden[::-1]):
            long_value += (256**i) * ord(c)
        result = ''
        while long_value >= 43:
            div, mod = divmod(long_value, 43)
            result = chars[mod] + result
            long_value = div
        result = chars[long_value] + result
        nPad = 0
        for c in bingevonden:
            if c == '\0': nPad += 1
            else: break
        return (chars[0]*nPad) + result



    def base_decode(self,v):
        chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$*+-./:'

        long_value = 0L
        for (i, c) in enumerate(v[::-1]):
            long_value += chars.find(c) * (43**i)
        result = ''
        while long_value >= 256:
            div, mod = divmod(long_value, 256)
            result = chr(mod) + result
            long_value = div
        result = chr(long_value) + result
        nPad = 0
        for c in v:
            if c == chars[0]: nPad += 1
            else: break
        result = chr(0)*nPad + result
        #return result
        return binascii.hexlify(result)







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
        self.toolbarshowqrgeneratebtcaddress.hide()
        self.toolbarshowrecreate.hide()
        self.toolbarshowrescan.hide()
        self.toolbarsign.hide()
        self.toolBarqrpublicenprivatearchive.hide()
        self.msgallround.hide()



        self.statusBar().showMessage("")

        self.lanchkeyboardhide()


        #self.toolBartransactionraw.hide()
        #self.toolBartransactionqrcode.hide()

        self.messageboard.clear()
        self.imglogo.hide()

        QtGui.QApplication.processEvents()








    def createwalletbuttons(self):
        self.btn10 = QtGui.QPushButton(LANG_BTC_CREATE_ADDRESS, self)
        self.btn10.setGeometry(0, 50, 480, 50)
        self.btn10.clicked.connect(self.generatebtcaddress)
        self.btn10.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn10.setIcon(QtGui.QIcon(dir_mainpath+'/img/plus.png'))


        self.btn11 = QtGui.QPushButton(LANG_BTC_IMPORT_ADDRESS, self)
        self.btn11.setGeometry(0, 100, 480, 50)
        self.btn11.clicked.connect(self.importprivatekeybtc)
        self.btn11.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn11.setIcon(QtGui.QIcon(dir_mainpath+'/img/qr.png'))


        self.btn13 = QtGui.QPushButton(LANG_BTC_SIGN_ADDRESS, self)
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

        self.listcontactskey = glob.glob(dir_coin+"/BTC/*")
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
                
                privatekeyorg = self.WifToPrivateKey(privateaddresis)
                publicaddresis = self.keyToAddr(privatekeyorg)

                #print publicaddresis

                self.comboBoxmsg.addItem(publicaddresis,item)



            self.comboBoxmsg.setEnabled(True)
            self.statusBar().showMessage("")
            QtGui.QApplication.processEvents()




    def midfunction1(self,index):
        itemnow = self.comboBoxmsg.itemData(index).toPyObject()
        if itemnow == "NIKS2":
            pass
        else:
            self.msg_unencrypte(itemnow)
                





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
        privatekeyorg = self.WifToPrivateKey(privatekeyusetosignnowarchive)
        publickeyusetosignnowarchive = self.keyToAddr(privatekeyorg)


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

        #global tx_signed
        tx_signed=""

        self.clearscreen()
        self.toolBar7.show()
        self.toolbarsign.show()

        #foundkeyfromqrcode=self.camscanner()
        foundkeyfromqrcode1=self.camscannermd5()
        foundkeyfromqrcode2=foundkeyfromqrcode1.split(",")[0]
        unsignedmsgnow=foundkeyfromqrcode2.split(":")[1]
        sendedcmdtocheck=foundkeyfromqrcode2.split(":")[0]

       

        foundkeyfromqrcodenow = str(unsignedmsgnow.strip())
        privatekeyusetosignnow = str(privatekeyusetosignnowarchive.strip())

    
        self.clearscreen()
        self.toolBar7.show()
        self.toolbarsign.show()




        transactions = Transactions(testnet=True)
        tx_signed=""


        if sendedcmdtocheck == 'signbtc':

            try:
                tx_signed = transactions.sign(foundkeyfromqrcodenow, privatekeyusetosignnow)
                #print tx_signed
            except:
                pass
                tx_signed=""
                #print "No RAW transactions, try base43 for electrum"

            if tx_signed =="":

                try:
                    rawis=self.base_decode(foundkeyfromqrcodenow);
                    tx_signed = transactions.sign(rawis, privatekeyusetosignnow)
                    #print tx_signed
                except:
                    pass
                    tx_signed=""
                    #print "Was no base43 either"
        


        self.clearscreen()
        self.toolBar7.show()

        if tx_signed !="":

            #self.showtransactionqrcode()

            tx_signed='btcbroadcast:'+tx_signed



            msgnow='Plase scan this QR to broadcast your transaction.'
            self.msgallround.show()
            self.allroundmsg(17,530,446,270,msgnow)

            self.showqrmovie(tx_signed,0,50,480,480)  #text, positie x,y,w,h 






        else:
            self.statusBar().showMessage("ERROR!!! I Cant sign the transaction.")
            self.toolbarsign.show()



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



    def split(self,s, n):
      new_list = []
      for i in range(0, len(s), n):
        new_list.append(s[i:i+n])
      return new_list




#    def showtransactionqrcode(self):
#        global tx_signed
#        self.clearscreen()
#        self.toolBar7.show()
#        self.toolBartransactionraw.show()
#        self.setCode("qrboardleft",17,50,350,350,tx_signed)

#        electrumversion=self.base_encode(tx_signed)
#        self.setCode("qrboardright",17,440,350,350,electrumversion)





#        self.messageboardprivatepublickey1.setText(LANG_RAW_VERSION)
#        self.messageboardprivatepublickey2.setText(LANG_ELEC_VERSION)

#        self.messageboardprivatepublickey1.show()
#        self.messageboardprivatepublickey2.show()
        


#    def showtransactionrawtext(self):
#        global tx_signed
#        self.clearscreen()
#        self.toolBar7.show()
#        self.toolBartransactionqrcode.show()

#        self.editor()
#        self.textEdit.setReadOnly(True)
#        self.textEdit.setHtml(tx_signed)



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



        stopcam="no"
        foundkeyfromqrcode="NULL"
 
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













    def camscannermd5(self):
        global stopcam
        stopcam="yes"
        imagetoshow=dir_coin+"/TEMP/cam.jpg"
        cam = cv2.VideoCapture(0)

        width = self.geometry().width()
        height = self.geometry().height()-80
        self.messageboard.setGeometry(0, 80, width, height)
        self.messageboard.setScaledContents(True);
        self.messageboard.show()



        stopcam="no"
        foundkeyfromqrcode="NULL"
        checklistarray="NULL"
 
        while stopcam =="no":
           
            s, im = cam.read() # captures image
            cv2.imwrite(imagetoshow,im) # writes image test.bmp to disk


            self.messageboard.setPixmap(QtGui.QPixmap(imagetoshow))  
            QtGui.QApplication.processEvents()
            qr = qrtools.QR()
            qr.decode(imagetoshow)
            foundkeyfromqrcode= qr.data.encode('ascii')

            if foundkeyfromqrcode !="NULL":



                tempfoundkeyfromqrcode=foundkeyfromqrcode


                try:
                    maxqrcodescounts=int(tempfoundkeyfromqrcode.split(",")[0].split(":")[1])
                    currentqrnumber=int(tempfoundkeyfromqrcode.split(",")[0].split(":")[0])


                    #one time creation
                    if checklistarray =="NULL":
                        checklistarray = ['THISISEMPTY'] * maxqrcodescounts



                    #currentdatais=tempfoundkeyfromqrcode.split(",").encode("ascii")
                    

                    if currentqrnumber == maxqrcodescounts:
                        

                        lengttotalarray=int(len(tempfoundkeyfromqrcode.split(",")))
                        md5is=tempfoundkeyfromqrcode.split(",")[ lengttotalarray - 2]
                        #print md5is

                        md5total=tempfoundkeyfromqrcode.split(",")[ lengttotalarray - 1]
                        #print md5total

                        #remove what not needed.
                        currentdatais=tempfoundkeyfromqrcode.split(",")
                        currentdatais.remove(currentdatais[0])
                        currentdatais.remove(currentdatais[-1])
                        currentdatais.remove(currentdatais[-1])

                        #print currentdatais


                    else:


                        lengttotalarray=int(len(tempfoundkeyfromqrcode.split(",")))
                        md5is=tempfoundkeyfromqrcode.split(",")[ lengttotalarray - 1]
                        #print md5is

                        currentdatais=tempfoundkeyfromqrcode.split(",")
                        currentdatais.remove(currentdatais[0])
                        currentdatais.remove(currentdatais[-1])

                        #print currentdatais




                    #currentdatais = ','.join(currentdatais).encode("ascii")
                    currentdatais = ','.join(currentdatais)

                    #print '================'
                    #print currentdatais
                    #print md5is
                    #print '================'



                    #check if md5 is correct
                    if hashlib.md5(currentdatais).hexdigest() == md5is:


                        #add data to our final array
                        checklistarray[int(currentqrnumber)-1]= currentdatais





                    #print checklistarray
                    if 'THISISEMPTY' not in checklistarray:
                        stopcam="yes"


                except:
                    pass
                    #print 'error scanning'



        #finaldatafromqris = ''.join(checklistarray).encode("ascii")
        finaldatafromqris = ''.join(checklistarray)
        #print finaldatafromqris


        cam.release()
        del cam
        #print "Cam stoped"
        os.remove(imagetoshow)
        return finaldatafromqris









    def importprivatekeybtc(self):
        self.clearscreen()
        self.toolBar7.show()
        self.toolbarshowrescan.show()

        foundkeyfromqrcode=self.camscanner()


        self.clearscreen()
        self.toolBar7.show()
        self.toolbarshowrescan.show()

        #print foundkeyfromqrcode
        #self.checkprivatepublicbtc(foundkeyfromqrcode)

        try:
            self.checkprivatepublicbtc(foundkeyfromqrcode)
        except:
            pass
            self.statusBar().showMessage("ERROR!!! Wrong privatekey.")






        

    def checkprivatepublicbtc(self,foundkeyfromqrcode):
        wiffoundkeyfromqrcode=self.WifToPrivateKey(foundkeyfromqrcode)
        publickeygevonden1=self.privateKeyToPublicKey(wiffoundkeyfromqrcode)
        publickeygevonden=self.pubKeyToAddr(publickeygevonden1)
        
        #print foundkeyfromqrcode # private
        #print publickeygevonden #public


        global privatekeygenerated
        global publickeygenerated


        self.clearscreen()
        self.toolBar7.show()
        self.toolbarshowrescan.show()
        self.toolbarshowqrgeneratebtcaddress.show()

        privatekeygenerated = foundkeyfromqrcode
        publickeygenerated = publickeygevonden


        msgshowkeys ="<b>Private Key:</b><br>"+privatekeygenerated+"<br><b>Public Address:</b><br>"+publickeygenerated+""
        self.editor()
        self.textEdit.setReadOnly(True)
        self.textEdit.setHtml(msgshowkeys)

        








   






    def generatebtcaddress(self):
        

        global privatekeygenerated
        global publickeygenerated


        self.clearscreen()
        self.toolBar7.show()

        # Generate a random private key
        private_key = os.urandom(32).encode('hex')
        privatekeygenerated = self.privateKeyToWif(private_key)
        publickeygenerated = self.keyToAddr(private_key)


        #print private_key
        #print privatekeygenerated
        #print publickeygenerated

        msgshowkeys ="<b>Private Key:</b><br>"+privatekeygenerated+"<br><b>Public Address:</b><br>"+publickeygenerated+""
        self.editor()
        self.textEdit.setReadOnly(True)
        self.textEdit.setHtml(msgshowkeys)

        self.toolbarshowqrgeneratebtcaddress.show()
        self.toolbarshowrecreate.show()







    def showqrgeneratebtcaddress(self):


        global publickey
        publickey = "MYOWN_PUBLIC_ID.pem.pub"
        self.textEdit.setReadOnly(True)
        self.textEdit.setText(privatekeygenerated)

        text = self.textEdit.toPlainText()

        randomnaamwordt=''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(100))
        self.writeenctextfile(dir_coin+"/BTC/"+randomnaamwordt,text)


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






        









    