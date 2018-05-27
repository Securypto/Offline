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
import base64


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
global dirpathtoread







class msgpage(QtGui.QMainWindow):
    def __init__(self, passwdsend=None):
        super(msgpage, self).__init__()
        global passwd
        passwd=passwdsend

        self.setGeometry(0, 0, 480, 800)
        self.setWindowTitle("Messaging")
        #disable right click
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setStyleSheet('font-size: 18pt; font-family: Courier;')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)


        #disable mouse pointer at DSG
        if (QtGui.QApplication.desktop().screenGeometry().width() < 500):
            self.setCursor(QtCore.Qt.BlankCursor)

        # Read a message
        extractAction1 = QtGui.QAction(LANG_KEEP_IN_ARCHIVE, self)
        extractAction1.triggered.connect(self.messagingpage)
        self.toolbarmessaging = self.addToolBar("Extraction")
        self.toolbarmessaging.addAction(extractAction1)
        

        self.addToolBarBreak()


        # msg encrypte short
        extractAction4 = QtGui.QAction(LANG_ENCRYPTE_SHORT, self)
        extractAction4.triggered.connect(self.msg_encrypte_short)
        self.toolBar40 = self.addToolBar("Extraction")
        self.toolBar40.addAction(extractAction4)

        self.addToolBarBreak()



        # msg encrypte short
        extractAction5 = QtGui.QAction(LANG_ENCRYPTE_PICTURES, self)
        extractAction5.triggered.connect(self.enc_msg_take_picture)
        self.toolBar51 = self.addToolBar("Extraction")
        self.toolBar51.addAction(extractAction5)

        self.addToolBarBreak()



        # take picture
        extractAction52 = QtGui.QAction(LANG_TAKE_PICTURES, self)
        extractAction52.triggered.connect(self.take_picture)
        self.toolBar52 = self.addToolBar("Extraction")
        self.toolBar52.addAction(extractAction52)

        self.addToolBarBreak()

        # take another picture
        extractAction53 = QtGui.QAction(LANG_TAKE_ANOTHER_PICTURES, self)
        extractAction53.triggered.connect(self.start_cam_take_picture)
        self.toolBar53 = self.addToolBar("Extraction")
        self.toolBar53.addAction(extractAction53)

        self.addToolBarBreak()


        # Import an contact
        extractActionimportcontact = QtGui.QAction(LANG_CONTACTS_IMPORT, self)
        extractActionimportcontact.triggered.connect(self.importcontact)
        self.toolbarimportcontact = self.addToolBar("Extraction")
        self.toolbarimportcontact.addAction(extractActionimportcontact)

        self.addToolBarBreak()

        # manage an contact
        extractActionmanageyourcontact = QtGui.QAction(LANG_CONTACTS_MANAGER, self)
        extractActionmanageyourcontact.triggered.connect(self.manageyourcontact)
        self.toolbarmnageyourcontact = self.addToolBar("Extraction")
        self.toolbarmnageyourcontact.addAction(extractActionmanageyourcontact)




        #Default messageboard
        self.messageboard = QtGui.QLabel("", self)
        self.messageboard.move(10,150)


        self.qrboardleft = QtGui.QLabel("", self)
        self.qrboardright = QtGui.QLabel("", self)


        self.msgallround = QtGui.QLabel(INFO_ABOUT_PUBLIC_KEY_FOR_MESSAGING, self)
        self.msgallround.setGeometry(466,80,350,350)
        self.msgallround.setWordWrap(True);


        self.messageboardprivatepublickey1 = QtGui.QLabel(LANG_PRIVATE_KEY, self)
        self.messageboardprivatepublickey1.setGeometry(50,80,250,40)
        self.messageboardprivatepublickey2 = QtGui.QLabel(LANG_PUBLIC_KEY, self)
        self.messageboardprivatepublickey2.setGeometry(466,80,250,40)



        self.btndeltecontact = QtGui.QPushButton(LANG_DELETE_MESSAGE,self)
        self.btndeltecontact.setGeometry(0,300,480,40)
        self.btndeltecontact.clicked.connect(self.selectedcontactverwijderen)
        self.btndeltecontact.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btndeltecontact.setIcon(QtGui.QIcon(dir_mainpath+'/img/close.png'))







        

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

        self.dropdowncontactmanager()
        self.dropdowncontact()
        self.dropdownmsg()
        self.dropdownfiles()
        self.createwelcomebuttons()
        self.clearscreen()
        self.messagingpage()




    def messagingpage(self):

        self.clearscreen()
        self.btn20.show() #read message short
        self.btn21.show() #write message short
        self.btn1.show() #read message
        self.btn3.show() #send a file
        self.btn5.show() #manage contacts
        self.btn6.show() #manage contacts
        self.imglogo.show()
        #self.toolbarmessaging.show()







    def clearscreen(self):


        global stopcam
        stopcam="yes"

        self.textEdit.hide()
       
        self.comboBoxcontactmanager.deleteLater()
        self.dropdowncontactmanager()
        self.comboBoxcontactmanager.hide()


        self.comboBox.deleteLater()
        self.dropdowncontact()
        self.comboBox.hide()

        self.comboBoxmsg.deleteLater()
        self.dropdownmsg()
        self.comboBoxmsg.hide()


        self.comboBoxfiles.deleteLater()
        self.dropdownfiles()
        self.comboBoxfiles.hide()
       
        self.messageboard.hide()
        self.qrboardleft.hide()
        self.qrboardright.hide()

        self.messageboardprivatepublickey1.hide()
        self.messageboardprivatepublickey2.hide()

        self.hidewelcomebuttons()
     
        self.toolBar40.hide() #encrypte button short

        self.toolBar51.hide() #encrypte button foto
        self.toolBar52.hide() #take button foto
        self.toolBar53.hide() #take another button foto


        self.toolbarmessaging.hide() #btc wallet



        self.toolbarimportcontact.hide()
        self.msgallround.hide()
        self.toolbarmnageyourcontact.hide()
        self.btndeltecontact.hide()


        self.statusBar().showMessage("")

        self.lanchkeyboardhide()


        self.messageboard.clear()

        self.imglogo.hide()

        QtGui.QApplication.processEvents()









    def createwelcomebuttons(self):




        self.btn5 = QtGui.QPushButton(LANG_CONTACTS, self)
        self.btn5.setGeometry(0, 50, 480, 50)
        self.btn5.clicked.connect(self.contactsmanager)
        self.btn5.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn5.setIcon(QtGui.QIcon(dir_mainpath+'/img/Messaging.png'))



        self.btn20 = QtGui.QPushButton(LANG_READ_MESSAGE_SHORT, self)
        self.btn20.setGeometry(0, 150, 480, 50)
        self.btn20.clicked.connect(self.readashortqrmessage)
        self.btn20.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn20.setIcon(QtGui.QIcon(dir_mainpath+'/img/Messaging.png'))

        self.btn21 = QtGui.QPushButton(LANG_WRITE_MESSAGE_SHORT, self)
        self.btn21.setGeometry(0, 200, 480, 50)
        self.btn21.clicked.connect(self.selectcontactshort)
        self.btn21.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn21.setIcon(QtGui.QIcon(dir_mainpath+'/img/Messaging.png'))




        self.btn6 = QtGui.QPushButton(LANG_TAKE_AND_SEND_PICTURE, self)
        self.btn6.setGeometry(0, 300, 480, 50)
        self.btn6.clicked.connect(self.takeandsendpicture)
        self.btn6.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn6.setIcon(QtGui.QIcon(dir_mainpath+'/img/Messaging.png'))

        self.btn3 = QtGui.QPushButton(LANG_OPEN_FILE, self)
        self.btn3.setGeometry(0, 350, 480, 50)
        self.btn3.clicked.connect(self.file_open)
        self.btn3.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn3.setIcon(QtGui.QIcon(dir_mainpath+'/img/Messaging.png'))

        self.btn1 = QtGui.QPushButton(LANG_READ_MESSAGE, self)
        self.btn1.setGeometry(0, 400, 480, 50)
        self.btn1.clicked.connect(self.selectdirpatforreaadincomming)
        self.btn1.setStyleSheet("QPushButton { text-align: left; padding-left: 15px; }")
        self.btn1.setIcon(QtGui.QIcon(dir_mainpath+'/img/Messaging.png'))













    def hidewelcomebuttons(self):
        self.btn20.hide()
        self.btn21.hide()
        self.btn1.hide()
        self.btn3.hide()
        self.btn5.hide()
        self.btn6.hide()
        self.imglogo.hide()




    def editor(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)





    def dropdowncontactmanager(self):

        self.comboBoxcontactmanager = QtGui.QComboBox(self)
        self.comboBoxcontactmanager.setGeometry(0, 120,480,30)


    def dropdowncontact(self):

        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.setGeometry(0, 50,480,30)


    def dropdownmsg(self):

        self.comboBoxmsg = QtGui.QComboBox(self)
        self.comboBoxmsg.setGeometry(0, 50,480,30) 


    def dropdownfiles(self):

        self.comboBoxfiles = QtGui.QComboBox(self)
        self.comboBoxfiles.setGeometry(0, 50,480,30)



    def allroundmsg(self,x,y,w,h,text=""):  
            self.msgallround.show()      
            self.msgallround.setWordWrap(True);
            self.msgallround.setGeometry(x,y,w,h)
            self.msgallround.setText(str(text))






    def manageyourcontact(self):

        self.clearscreen()
        self.toolbarmessaging.show()
        self.toolbarimportcontact.show()
        self.toolbarmnageyourcontact.show()
        self.comboBoxcontactmanager.clear()
        self.comboBoxcontactmanager.show()


        self.listcontacts = glob.glob(dir_coin+"/CONTACTS-PUBLIC-KEYS/*.pem.pub")

        

        if len(self.listcontacts) < 2:
            self.statusBar().showMessage(LANG_NO_MESSAGE)
            self.comboBoxcontactmanager.hide()
            #print "geen contacts"
        else:

            self.comboBoxcontactmanager.addItem(LANG_DROP_DOWN_SELECT_CONTACT_MANAGER)

            for item in self.listcontacts:
                itemnu = (item.replace(dir_coin+"/CONTACTS-PUBLIC-KEYS/", ""))
                if itemnu !="MYOWN_PUBLIC_ID.pem.pub" and "pem.pub" in itemnu and itemnu != LANG_DROP_DOWN_SELECT_CONTACT_MANAGER:
                    itemnu = (itemnu.replace(".pem.pub", ""))
                    self.comboBoxcontactmanager.addItem(itemnu)
                    #print itemnu

            self.comboBoxcontactmanager.activated[str].connect(self.manageyourcontactselected)




    def manageyourcontactselected(self,selectedcontact):


        if selectedcontact != LANG_DROP_DOWN_SELECT_CONTACT_MANAGER:


            #selectedcontact= str.replace("", ".pem.pub")

            global deletecontactpersoon
            deletecontactpersoon=selectedcontact
            self.btndeltecontact.show()


            file = open(dir_coin+"/CONTACTS-PUBLIC-KEYS/"+selectedcontact+".pem.pub", "r") 
            pubselected= file.read() 
            file.close() 

            #self.allroundmsg(17,150,446,40,str(selectedcontact))
            self.setCode("qrboardleft",17,350,446,446,pubselected)





        else:
            self.qrboardleft.hide()
            self.qrboardright.hide()
            self.msgallround.hide()
            self.btndeltecontact.hide()
            pass




    def selectedcontactverwijderen(self):



        global deletecontactpersoon
        #if "pem.pub" in deletecontactpersoon and deletecontactpersoon != LANG_DROP_DOWN_SELECT_CONTACT_MANAGER:
        if deletecontactpersoon != LANG_DROP_DOWN_SELECT_CONTACT_MANAGER:    
            
            #print deletecontactpersoon
            #print "ok"


            choice = QtGui.QMessageBox.question(self, LANG_DELETE_MESSAGE,LANG_SURE,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:

                choice = QtGui.QMessageBox.question(self, LANG_DELETE_MESSAGE,LANG_SURE2,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if choice == QtGui.QMessageBox.Yes:

                    todeletepath=dir_coin+"/CONTACTS-PUBLIC-KEYS/"+deletecontactpersoon+".pem.pub"

                    #print todeletepath

                    if os.path.isfile(todeletepath):
                        os.remove(todeletepath)
                        self.manageyourcontact()


                    else:
                        pass

            else:
                pass


        else:
            pass


                        

            






    def importcontact(self):

        self.clearscreen()
        self.toolbarmessaging.show()
        self.toolbarimportcontact.show()
        self.toolbarmnageyourcontact.show()



        foundkeyfromqrcode=self.camscanner()

        #print foundkeyfromqrcode
        #command = "echo '"+foundkeyfromqrcode+"' | openssl rsa -inform PEM -pubin -noout"
        #resultcommand = os.popen(str(command)).read()
        #print resultcommand
        
        if "BEGIN PUBLIC KEY" in foundkeyfromqrcode:
 

            #self.editor()
            #self.textEdit.setReadOnly(True)
            #self.textEdit.setText(foundkeyfromqrcode)


            self.lanchkeyboardshow()
               
            text, ok = QtGui.QInputDialog.getText(self, LANG_CHOOSE_A_NAME, LANG_SAVE_AS)

            if ok and text != '' and bool(re.match("^[a-zA-Z0-9_-]+([\s][a-zA-Z0-9_-]+)*$", str(text))):
                    opslaanals=dir_coin+"/CONTACTS-PUBLIC-KEYS/"+str(text)+".pem.pub"
                    filet = open(opslaanals,"w") 
                    filet.write(str(foundkeyfromqrcode)) 
                    filet.close() 

            self.clearscreen()
            self.toolbarmessaging.show()
            self.toolbarimportcontact.show()
            self.toolbarmnageyourcontact.show()



            self.setCode("qrboardleft",17,350,446,446,foundkeyfromqrcode)
            self.allroundmsg(17,150,446,40,str(text))


        else:
            print LANG_WRONG_PUBLIC_KEY_IMPORTED
            self.clearscreen()
            self.toolbarmessaging.show()
            self.toolbarimportcontact.show()
            self.toolbarmnageyourcontact.show()
            self.allroundmsg(17,150,446,40,str(LANG_WRONG_PUBLIC_KEY_IMPORTED))








    def contactsmanager(self):

        self.clearscreen()
        self.toolbarmessaging.show()
        self.toolbarimportcontact.show()
        self.toolbarmnageyourcontact.show()
        self.msgallround.show()

        file = open(dir_coin+"/CONTACTS-PUBLIC-KEYS/MYOWN_PUBLIC_ID.pem.pub", "r") 
        myownpublic= file.read() 
        file.close() 


        #self.setCode("qrboardleft",17,150,350,350,myownpublic)
        #self.allroundmsg(17,500,446,300,INFO_ABOUT_PUBLIC_KEY_FOR_MESSAGING)

        self.setCode("qrboardleft",5,125,470,470,myownpublic)
        self.allroundmsg(17,595,446,205,INFO_ABOUT_PUBLIC_KEY_FOR_MESSAGING)


        #self.setCode("qrboardleft",5,50,470,470,resultcommand)
        #self.allroundmsg(17,530,446,270,str(LANG_MESSAGE_SHORT_READY))



    def contactsshort(self,text):
        global publickey
        publickey = text

        if "pem.pub" in publickey:
            self.clearscreen()
            self.lanchkeyboardshow()
            self.editor()
            self.toolBar40.show()
            QtGui.QApplication.processEvents()


    def contactsendpicture(self,text):
        global publickey
        publickey = text

        if "pem.pub" in publickey:
            self.clearscreen()
            QtGui.QApplication.processEvents()
            self.start_cam_take_picture()




    def setpublickkey(self,text):
        global publickey
        publickey = text

        if "pem.pub" in publickey:
            self.file_open2()





    def getpublickeys(self):


        self.comboBox.clear()
        self.comboBox.show()
        self.listcontacts = glob.glob(dir_coin+"/CONTACTS-PUBLIC-KEYS/*.pub")

        self.comboBox.addItem(LANG_DROP_DOWN_SELECT_PUBLIC_KEY)

        for item in self.listcontacts:
            itemnu = (item.replace(dir_coin+"/CONTACTS-PUBLIC-KEYS/", ""))
            self.comboBox.addItem(itemnu)
            #print itemnu





    def selectdirpatforreaadincomming(self):
        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if Backupdironusb not in pathDigiSaveBoxUSB:
            self.statusBar().showMessage(LANG_USB_MISSING)
        else:
            global dirpathtoread
            dirpathtoread ="USB"
            global mainpath
            mainpath =pathDigiSaveBoxUSB
            self.readmessages("USB")





    def readmessages(self,forswitchtemp):


        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if dirpathtoread == "USB" and Backupdironusb not in pathDigiSaveBoxUSB:
            self.statusBar().showMessage(LANG_USB_MISSING)
        else:

            self.clearscreen()
            
            self.listcontactskey = glob.glob(pathDigiSaveBoxUSB+"/*.tar.gz")
            self.toolbarmessaging.show()


            if len(self.listcontactskey) < 1:
                self.statusBar().showMessage(LANG_NO_MESSAGE)
                self.comboBoxmsg.hide()
            else:

                self.comboBoxmsg.show()
                self.comboBoxmsg.clear()

                self.comboBoxmsg.activated[str].connect(self.msg_unencrypte)    

                loadingtext="Loading"
                self.comboBoxmsg.setEnabled(False)

                for item in self.listcontactskey:
                    

                    if loadingtext.count('.') > 5:
                        loadingtext="Loading"
                    loadingtext=loadingtext+"."
                    self.statusBar().showMessage(loadingtext)
                    QtGui.QApplication.processEvents()

                    if ".tar.gz" in item:

                        itemnu = (item.replace(mainpath+"/"+dirpathtoread+"/", ""))
                        itemnu = (item.replace(mainpath+"/", ""))

                        self.comboBoxmsg.addItem(itemnu)

                self.comboBoxmsg.setEnabled(True)
                self.statusBar().showMessage("")
                QtGui.QApplication.processEvents()





    def takeandsendpicture(self):

        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if Backupdironusb not in pathDigiSaveBoxUSB:
            self.statusBar().showMessage(LANG_USB_MISSING)
        else:

            self.getpublickeys()
            self.textEdit.hide()
            self.hidewelcomebuttons()
            self.toolbarmessaging.show()
            self.comboBox.show()
            self.comboBox.activated[str].connect(self.contactsendpicture)






    def selectcontact(self):

        self.getpublickeys()
        self.textEdit.hide()
        self.hidewelcomebuttons()
        self.toolbarmessaging.show()
        self.comboBox.show()
        self.comboBox.activated[str].connect(self.contacts)




    def selectcontactshort(self):


        self.getpublickeys()
        self.textEdit.hide()
        self.hidewelcomebuttons()
        self.toolbarmessaging.show()
        self.comboBox.show()
        self.comboBox.activated[str].connect(self.contactsshort)



    def readashortqrmessage(self):



        self.clearscreen()
        self.toolbarmessaging.show()

        foundkeyfromqrcode=self.camscanner()

        command = "echo '"+foundkeyfromqrcode+"' | base64 --decode | openssl rsautl -decrypt -inkey '"+dir_coin+"/MY-OWN-PRIVATE-KEY/MYOWN_id_rsa' -passin pass:"+passwd+""
        resultcommand = os.popen(str(command)).read()


        self.editor()
        self.textEdit.setReadOnly(True)
        self.textEdit.setText(resultcommand)






    def file_open(self):

        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if Backupdironusb not in pathDigiSaveBoxUSB:
            self.statusBar().showMessage(LANG_USB_MISSING)
        else:


            self.getpublickeys()
            self.textEdit.hide()
            self.hidewelcomebuttons()
            self.toolbarmessaging.show()
            self.comboBox.show()
            self.comboBox.activated[str].connect(self.setpublickkey)



    def file_open2(self):
 


        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if Backupdironusb not in pathDigiSaveBoxUSB:
            self.statusBar().showMessage(LANG_USB_MISSING)
        else:

            self.clearscreen()
            self.toolbarmessaging.show()
            self.comboBoxfiles.clear()
            self.comboBoxfiles.show()
            self.listfiles = glob.glob(pathDigiSaveBoxUSB+"/*")



            if len(self.listfiles) < 1:
                self.statusBar().showMessage(LANG_NO_FILES)
                self.comboBoxfiles.hide()
            else:


                self.comboBoxfiles.addItem(LANG_DROP_DOWN_SELECT_FILES)



                for item in self.listfiles:
                    itemnu = (item.replace(pathDigiSaveBoxUSB+"/", ""))
                    self.comboBoxfiles.addItem(itemnu)



                self.comboBoxfiles.activated[str].connect(self.file_open3)




    def file_open3(self,fileoftext):
        fileplainnaam = str(fileoftext)

        if fileplainnaam != LANG_DROP_DOWN_SELECT_FILES:
            self.msg_encrypteexternal(fileplainnaam)




        

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







        

        self.messagingpage()









    def msg_unencrypte_usb(self,msgtoreadfile):

        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if Backupdironusb not in pathDigiSaveBoxUSB:
            self.statusBar().showMessage(LANG_USB_MISSING)
        else:




            
            msgtoreadfile=str(msgtoreadfile)



            dirnametosave="decrypt-"+(time.strftime("%Y-%m-%d-%H-%M-%S"))
            os.mkdir(pathDigiSaveBoxUSB+"/"+dirnametosave)
            os.mkdir(pathDigiSaveBoxUSB+"/"+dirnametosave+"/TEMPDIGISAVEBOX")


            
            #untar to read
            tar = tarfile.open(pathDigiSaveBoxUSB+"/"+msgtoreadfile) 
            tar.extractall(pathDigiSaveBoxUSB+"/"+dirnametosave+"/TEMPDIGISAVEBOX") # untar file into same directory
            tar.close()


            command = "openssl rsautl -decrypt  -inkey '"+dir_coin+"/MY-OWN-PRIVATE-KEY/MYOWN_id_rsa' -passin pass:"+passwd+" -in '"+pathDigiSaveBoxUSB+"/"+dirnametosave+"/TEMPDIGISAVEBOX/TEMPtempkey.bin.enc' -out '"+pathDigiSaveBoxUSB+"/"+dirnametosave+"/TEMPDIGISAVEBOX/keyforthisfile.bin'"
            resultcommand = os.popen(str(command)).read()

            
            command = "openssl enc -d -aes-256-cbc -md sha256 -in '"+pathDigiSaveBoxUSB+"/"+dirnametosave+"/TEMPDIGISAVEBOX/TEMPmsgfile.enc' -out '"+pathDigiSaveBoxUSB+"/"+dirnametosave+"/TEMPDIGISAVEBOX/msgfile' -pass file:'"+pathDigiSaveBoxUSB+"/"+dirnametosave+"/TEMPDIGISAVEBOX/keyforthisfile.bin'"
            resultcommand = os.popen(str(command)).read()


            tar2 = tarfile.open(pathDigiSaveBoxUSB+"/"+dirnametosave+"/TEMPDIGISAVEBOX/msgfile") 
            tar2.extractall(pathDigiSaveBoxUSB+"/"+dirnametosave) # untar file into same directory
            tar2.close()

            tempdir=pathDigiSaveBoxUSB+"/"+dirnametosave+"/TEMPDIGISAVEBOX"
            if os.path.isdir(tempdir):
                shutil.rmtree(tempdir)







    def msg_unencrypte(self,msgtoreadfile):

        global dirpathtoread


        if dirpathtoread == "USB":

            self.loadingbegin()
            QtGui.QApplication.processEvents()

            tunencrypteexternal = threading.Thread(target=self.msg_unencrypte_usb, args=(msgtoreadfile,))
            tunencrypteexternal.start()

            while tunencrypteexternal.is_alive():
                self.loadingloop()
                QtGui.QApplication.processEvents()
                time.sleep(0.2)


                    


            self.loadingend(LANG_DECRYPTE_WAS_SUCCES_NEW)
            QtGui.QApplication.processEvents()
            self.clearscreen()
            self.messagingpage()








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
        #print "Cam stoped"
        os.remove(imagetoshow)
        return foundkeyfromqrcode




    def take_picture(self):
        #stop  start_cam_take_picture en neem foto
        imagetoshow=dir_coin+"/TEMP/cam.jpg"
        global stopcam
        stopcam="yes"
        self.clearscreen()

        self.comboBox.deleteLater()
        self.dropdowncontact()
        self.comboBox.hide()

        QtGui.QApplication.processEvents()
        self.toolBar51.show()
        self.toolBar53.show()

        self.messageboard.setGeometry(0, 320, 480, 360)
        self.messageboard.setScaledContents(True);
        self.messageboard.show()
        self.messageboard.setPixmap(QtGui.QPixmap(imagetoshow))  




    def start_cam_take_picture(self):
        global stopcam
        stopcam="yes"

        self.clearscreen()
        QtGui.QApplication.processEvents()
        self.toolBar52.show()
        

        imagetoshow=dir_coin+"/TEMP/cam.jpg"

        cam = cv2.VideoCapture(0)

        self.messageboard.setGeometry(0, 320, 480, 360)
        self.messageboard.setScaledContents(True);
        self.messageboard.show()

        stopcam="no"
        while stopcam =="no":

            s, im = cam.read() # captures image
            cv2.imwrite(imagetoshow,im) # writes image test.bmp to disk
            self.messageboard.setPixmap(QtGui.QPixmap(imagetoshow))  
            QtGui.QApplication.processEvents()
            

        cam.release()
        del cam
        print "Cam stoped"
        #os.remove(imagetoshow)
        #return foundkeyfromqrcode

        




    def enc_msg_take_picture(self):

        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if Backupdironusb not in pathDigiSaveBoxUSB:
            self.statusBar().showMessage(LANG_USB_MISSING)
        else:



            savename, ok = QtGui.QInputDialog.getText(self, LANG_CHOOSE_A_NAME, LANG_SAVE_AS)
            if ok and savename != '' and bool(re.match("^[a-zA-Z0-9_-]+([\s][a-zA-Z0-9_-]+)*$", str(savename))):
                self.clearscreen()
                print "we gaan encrypten"


                fileplain = dir_coin+"/TEMP/cam.jpg"
                fileplainnaam = "cam.jpg"


                file=dir_coin+"/TEMP"+"/TEMPzipfile.tar"
                fileplain = dir_coin+"/TEMP/cam.jpg"
                fileplainnaam = "cam.jpg"

                #tar to send
                tar3 = tarfile.open(file, "w")
                tar3.add(fileplain, arcname=fileplainnaam)
                tar3.close()


              
                command ="openssl rand -base64 32 > '"+dir_coin+"/TEMP"+"/TEMPtempkey.bin'"
                resultcommand = os.popen(str(command)).read()
                #print resultcommand
                command = "openssl rsautl -encrypt -inkey '"+dir_coin+"/CONTACTS-PUBLIC-KEYS/"+publickey+"' -pubin -in '"+dir_coin+"/TEMP"+"/TEMPtempkey.bin' -out '"+dir_coin+"/TEMP"+"/TEMPtempkey.bin.enc'"
                resultcommand = os.popen(str(command)).read()
                #print resultcommand
                command = "openssl enc -e -aes-256-cbc -md sha256 -in '"+file+"' -out '"+dir_coin+"/TEMP"+"/TEMPmsgfile.enc' -pass file:'"+dir_coin+"/TEMP"+"/TEMPtempkey.bin'"
                resultcommand = os.popen(str(command)).read()
                #print resultcommand


                #check if it was created, maybe wrong key?
                filetormnu=dir_coin+"/TEMP"+"/TEMPtempkey.bin.enc"
                if os.path.exists(filetormnu):
                #tar to send
                    #tar = tarfile.open(dir_coin+"/TEMP"+"/encrypted-"+fileplainnaam+".tar.gz", "w:gz")
                    datesave=(time.strftime("%Y-%m-%d-%H-%M-%S"))
                    tar = tarfile.open(pathDigiSaveBoxUSB+"/encrypted-"+str(savename)+"-"+datesave+".tar.gz", "w:gz")
                    for name in ["TEMPmsgfile.enc", "TEMPtempkey.bin.enc"]:
                        tar.add(dir_coin+"/TEMP"+"/"+name, arcname=name)
                    tar.close()


                filetormnu=dir_coin+"/TEMP"+"/TEMPmsgfile.enc"
                if os.path.exists(filetormnu):
                    os.remove(filetormnu)

                filetormnu=dir_coin+"/TEMP"+"/TEMPtempkey.bin"
                if os.path.exists(filetormnu):
                    os.remove(filetormnu)

                filetormnu=dir_coin+"/TEMP"+"/TEMPtempkey.bin.enc"
                if os.path.exists(filetormnu):
                    os.remove(filetormnu)

                filetormnu=dir_coin+"/TEMP"+"/TEMPzipfile.tar"
                if os.path.exists(filetormnu):
                    os.remove(filetormnu)

                filetormnu=dir_coin+"/TEMP"+"/cam.jpg"
                if os.path.exists(filetormnu):
                    os.remove(filetormnu)

                printmessagetouser=LANG_PIC_ENC_SAVED
                self.toolbarmessaging.show()
                self.editor()
                self.textEdit.setReadOnly(True)
                self.textEdit.setText(printmessagetouser)


        '''
        image_file = dir_coin+"/TEMP"+"/encrypted-cam.jpg.tar.gz"

        image = open(image_file, 'rb') #open binary file in read mode
        image_read = image.read()
        image_64_encode = base64.encodestring(image_read)
        #print image_64_encode

        count=2000
        chunks= [''.join(x) for x in zip(*[list(image_64_encode[z::count]) for z in range(count)])]
        #print chunks
        total=len(chunks)
        
        global stopqrdance
        stopqrdance="no"
        while stopqrdance =="no":

            teller=0
            for chunk in chunks:

                teller=teller+1
                msgprint="("+str(teller)+"/"+str(total)+")"
                chunk=msgprint+chunk
                
                self.setCode("qrboardleft",5,50,470,470,chunk)
                self.allroundmsg(17,530,446,270,str(msgprint))
                #time.sleep(0.1)
                QtGui.QApplication.processEvents()




                # STITCH IMAGE BACK TOGETHER
                # Normally this will be in another location to stitch it back together
                #read_file = open('chunkfile.txt', 'rb')

                # Create the jpg file
                #with open('images/stitched_together.jpg', 'wb') as image:
                #    for f in read_file:
                #        image.write(f)

        '''








    def msg_encrypte_short(self,fileoftext):


        text = self.textEdit.toPlainText()
        text= str(text)
        command = "echo '"+text+"' | openssl  rsautl -encrypt -pubin -inkey '"+dir_coin+"/CONTACTS-PUBLIC-KEYS/"+publickey+"' | base64"
        resultcommand = os.popen(str(command)).read()
        resultcommand=str(resultcommand)


        self.clearscreen()
        self.toolbarmessaging.show()

        self.setCode("qrboardleft",5,50,470,470,resultcommand)
        self.allroundmsg(17,530,446,270,str(LANG_MESSAGE_SHORT_READY))



    def msg_encrypteexternal(self,fileoftext):


        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if Backupdironusb not in pathDigiSaveBoxUSB:
            self.statusBar().showMessage(LANG_USB_MISSING)
        else:


            self.loadingbegin()
            QtGui.QApplication.processEvents()
            
            
            tencrypteexternal = threading.Thread(target=self.tencrypteexternalfunction, args=(fileoftext,))
            tencrypteexternal.start()



            while tencrypteexternal.is_alive():
                self.loadingloop()
                QtGui.QApplication.processEvents()
                time.sleep(0.2)




            filetormnu=pathDigiSaveBoxUSB+"/encrypted-"+str(fileoftext)+".tar.gz"
            if os.path.exists(filetormnu):
                printmessagetouser= LANG_ENCRYPTE_WAS_SUCCES
            else:
                printmessagetouser= LANG_WRONG_ENC_FILE_DIR


            self.loadingend(printmessagetouser)
            QtGui.QApplication.processEvents()
            self.clearscreen()
            self.messagingpage()





    def tencrypteexternalfunction(self,fileoftext):

        pathDigiSaveBoxUSB = self.getDigiSaveBoxPathUSB()
        if Backupdironusb not in pathDigiSaveBoxUSB:
            self.statusBar().showMessage(LANG_USB_MISSING)
        else:


            fileplain = pathDigiSaveBoxUSB+"/"+str(fileoftext)
            fileplainnaam = str(fileoftext)


            file=pathDigiSaveBoxUSB+"/TEMPzipfile.tar"
            fileplainnaam=str(fileoftext)
            fileplain = pathDigiSaveBoxUSB+"/"+str(fileoftext)

            #tar to send
            tar3 = tarfile.open(file, "w")
            tar3.add(fileplain, arcname=fileplainnaam)
            tar3.close()


          
            command ="openssl rand -base64 32 > '"+pathDigiSaveBoxUSB+"/TEMPtempkey.bin'"
            resultcommand = os.popen(str(command)).read()
            #print resultcommand
            command = "openssl rsautl -encrypt -inkey '"+dir_coin+"/CONTACTS-PUBLIC-KEYS/"+publickey+"' -pubin -in '"+pathDigiSaveBoxUSB+"/TEMPtempkey.bin' -out '"+pathDigiSaveBoxUSB+"/TEMPtempkey.bin.enc'"
            resultcommand = os.popen(str(command)).read()
            #print resultcommand
            command = "openssl enc -e -aes-256-cbc -md sha256 -in '"+file+"' -out '"+pathDigiSaveBoxUSB+"/TEMPmsgfile.enc' -pass file:'"+pathDigiSaveBoxUSB+"/TEMPtempkey.bin'"
            resultcommand = os.popen(str(command)).read()
            #print resultcommand


            #check if it was created, maybe wrong key?
            filetormnu=pathDigiSaveBoxUSB+"/TEMPtempkey.bin.enc"
            if os.path.exists(filetormnu):
            #tar to send
                tar = tarfile.open(pathDigiSaveBoxUSB+"/encrypted-"+fileplainnaam+".tar.gz", "w:gz")
                for name in ["TEMPmsgfile.enc", "TEMPtempkey.bin.enc"]:
                    tar.add(pathDigiSaveBoxUSB+"/"+name, arcname=name)
                tar.close()


            filetormnu=pathDigiSaveBoxUSB+"/TEMPmsgfile.enc"
            if os.path.exists(filetormnu):
                os.remove(filetormnu)

            filetormnu=pathDigiSaveBoxUSB+"/TEMPtempkey.bin"
            if os.path.exists(filetormnu):
                os.remove(filetormnu)

            filetormnu=pathDigiSaveBoxUSB+"/TEMPtempkey.bin.enc"
            if os.path.exists(filetormnu):
                os.remove(filetormnu)

            filetormnu=pathDigiSaveBoxUSB+"/TEMPzipfile.tar"
            if os.path.exists(filetormnu):
                os.remove(filetormnu)














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

            








    def close_application(self):
        global stopcam
        stopcam="yes"
        self.close()

        







    