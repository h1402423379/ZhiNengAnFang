import socket
import struct
import sys
import threading

import cv2
import numpy
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QApplication, QDialog
from PyQt5.uic import loadUi
from widget import Ui_Widget
from login import Ui_login
from mainwindow import Ui_MainWindow

class MyLoginClass(QDialog,Ui_login):
    def __init__(self):
        #super(MyLoginClass, self).__init__(parent)
        #self.setupUi(self)
        #self.lg_Button.clicked.connect(self.end_event)
        #self.ex_Button.clicked.connect(self.close)
        super().__init__()
        self.resize(500,500)
        self.move(400,200)
        self.set_ui()
        self.setWindowTitle('登录窗口')
        #self.lineEdit_2.setEchoMode(QlineEdit.password)
    def set_ui(self):
        loadUi("./login.ui", self)
        print(dir(self))
        self.pushButton.clicked.connect(self.login_btn_hand)
        self.pushButton_2.clicked.connect(self.quit)
    def quit(self):
        sys.exit()
    def login_btn_hand(self):
        if self.lineEdit.text()=="":
            QMessageBox.about(self,'提示','请输入用户名')
        elif self.lineEdit_2.text()=="":
            QMessageBox.about(self, '提示', '请输入密码')
        elif self.lineEdit.text()=="Hou" and self.lineEdit_2.text()=="123456":
            QMessageBox.about(self,'登陆成功','欢迎使用本系统!')
            self.shop = MyMainClass()

            self.shop.show()

        else:
            QMessageBox.about(self, '提示', '用户名或密码输入错误')





class MyMainClass(QtWidgets.QWidget,Ui_Widget):
    def __init__(self,parent=None):

        super(MyMainClass, self).__init__(parent)

        self.setupUi(self)

        self.timer = QTimer(self)

        #self.timer.timeout.connect(self.showTime)
        #self.timer.start(1000)


        self.resolution = [640,480]
        self.addr_port = ("192.168.137.176",8880)
        self.src = 888+15
        self.interval = 0
        self.img_fps = 100

        self.button_exit.clicked.connect(self.quit)
        self.button_open.clicked.connect(self.button_2_clicked)
        self.button_local.clicked.connect(self.get_local)
        print('MyMainClass init Finished')
        #self.Socket_Connect()

    def get_local(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        self.local_ip.setText(hostname)
        self.local_port.setText(ip)
    def quit(self):
        sys.exit()

    def button_2_clicked(self):
        print('ip', self.serverip.text())
        print('port', self.addr_port[1])
        self.Socket_Connect()
        self.Get_Data(self.interval)

    def showTime(self):
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.label1.setText(timeDisplay)

    def Set_socket(self):

        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    def Socket_Connect(self):
        print("IP is %s:%d" % (self.addr_port[0], self.addr_port[1]))
        self.Set_socket()
        print('port is :', self.addr_port)

        print('Error', self.client.connect_ex(self.addr_port))


    def Get_Data(self,interval):
        print('Get_Data')
        self.socket_client()
        self.showThread= threading.Thread(target=self.socket_client)
        self.showThread.start()
    def socket_client(self):
        print('socket_client')
        self.client.send(struct.pack("lhh",self.src,self.resolution[0],self.resolution[1]))
        print(123123)
        width = self.label_4.width()
        height = self.label_4.height()
        while 1:
            print(self.client.getsockname())
            print(123123)
            info = struct.unpack('lhh',self.client.recv(8))
            print(123)
            buf_size = info[0]
            if buf_size:
                try:
                    self.buf = b""
                    while (buf_size):
                        print('buf_size:',buf_size)
                        temp_buf = self.client.recv(buf_size)
                        buf_size -= len(temp_buf)
                        self.buf +=temp_buf
                        data = numpy.frombuffer(self.buf,dtype='uint8')
                        self.image = cv2.imdecode(data,1)
                        filename = 'image.jpg'
                        cv2.imwrite(filename,self.image)
                        print('width:',self.label_4.width())
                        openJpg = QPixmap(filename).scaled(width, height)
                        self.label_4.setPixmap(openJpg)
                except:
                    pass
                    print('except')
                finally:
                    if(cv2.waitKey(10)==27):
                        self.client.close()
                        cv2.destroyAllWindows()
                        break
                    print('finally')




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyLoginClass()
    window.show()
    sys.exit(app.exec_())

