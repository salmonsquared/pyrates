import utils # Local Package
import sys
import requests
import json
from ctypes import windll
from io import BytesIO

from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QTableWidget)
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

from main_ui import Ui_MainWindow

windll.shcore.SetProcessDpiAwareness(1) # Fixes blurry text on W11
movie_api = "http://www.omdbapi.com/?apikey=7c6a9526&"
placeholder_poster = "placeholderposter.png"

def fetch_image(url):
    response = requests.get(url)
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(response.content)
    return pixmap

class MyTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(MyTableWidget, self).__init__(parent)
        self.setEnabled(True)
        self.setGeometry(QtCore.QRect(32, 40, 1005, 900))
        self.setAutoFillBackground(False)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.setGridStyle(QtCore.Qt.SolidLine)
        self.setRowCount(5)
        self.setColumnCount(5)
        self.setObjectName("tableWidget")
        for n in range(4):
            item = QtWidgets.QTableWidgetItem()
            self.setHorizontalHeaderItem(n, item)
        self.horizontalHeader().setVisible(True)
        self.horizontalHeader().setDefaultSectionSize(200)
        self.verticalHeader().setDefaultSectionSize(160)
        self.verticalHeader().setVisible(False)

    def keyPressEvent(self, event):
        key = event.key()
        if key == 16777220:
            search_title = self.currentItem().text() # bug where text box has to be blue, not just hilighted
            search_parameters = {'t': search_title}
            movie_data = requests.get(movie_api, params = search_parameters).json()
            print(movie_data)
            movie_title = movie_data['Title']
            print(movie_title)
            self.currentItem().setText(movie_title) 
            #Fetch Poster 
            movie_poster_url = movie_data['Poster']
            movie_poster = fetch_image(movie_poster_url)
            #Image
            poster_label = QtWidgets.QLabel(self)
            pixmap = QPixmap(movie_poster)
            poster_label.setPixmap(pixmap)
            self.setCellWidget(0,0, poster_label)
            

            
        else:
            super(MyTableWidget, self).keyPressEvent(event)




# Initalize Windows
class MainWindow(QMainWindow, Ui_MainWindow): #Whole UI 
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

app = QApplication(sys.argv)

window = MyTableWidget()
window.show()
app.exec()