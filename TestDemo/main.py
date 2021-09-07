# from demo1 import myclass
# import cv2
# import threading
# import pyqt5_tools
# x=myclass(cv2.VideoCapture(0))
# thread= threading.Thread(target=x.capture(),name='thread-1')
# thread.start()
# thread.join()

import sys
import widget
import login
from PyQt5.QtWidgets import QApplication, QMainWindow

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = login.Ui_login()#类名
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())