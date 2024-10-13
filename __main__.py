import utils # Local Package
import sys
import requests
import json
from ctypes import windll
from io import BytesIO

from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QTableWidget)
from PyQt5.uic import loadUi

from main_ui import Ui_MainWindow

windll.shcore.SetProcessDpiAwareness(1) # Fixes blurry text on W11
movie_api = "http://www.omdbapi.com/?apikey=7c6a9526&"

def fetch_image(url):
    response = requests.get(url)
    image_data = Image.open(BytesIO(response.content))
    return ImageTk.PhotoImage(image_data)

class MyTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(MyTableWidget, self).__init__(parent)
        self.setEnabled(True)
        self.setGeometry(QtCore.QRect(32, 40, 381, 221))
        self.setAutoFillBackground(False)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.setGridStyle(QtCore.Qt.SolidLine)
        self.setRowCount(5)
        self.setColumnCount(5)
        self.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(4, item)
        self.horizontalHeader().setVisible(True)
        self.horizontalHeader().setDefaultSectionSize(60)
        self.verticalHeader().setVisible(False)

    def keyPressEvent(self, event):
        key = event.key()
        if key == 16777220:
            print("vvvvvvvv")
            print(self.currentItem())
            print(search_title)
            search_parameters = {'t': search_title}
            movie_data = requests.get(movie_api, params = search_parameters).json()
            print(movie_data)
            movie_title = movie_data['Title']
            print(movie_title)
            self.delete(0, tk.END)
            self.insert(0, movie_title)
            #Poster 
            movie_poster_url = movie_data['Poster']
            movie_poster = fetch_image(movie_poster_url)
            
            poster_label = tk.Label(root, image=movie_poster)
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