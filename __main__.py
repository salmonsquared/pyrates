import sys
import requests
from ctypes import windll

from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QTableWidget, QMenuBar, QAction)
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

from main_ui import Ui_MainWindow

windll.shcore.SetProcessDpiAwareness(1)  #Fixes blurry text on W11
movie_api = "http://www.omdbapi.com/?apikey=7c6a9526&"
placeholder_poster = "placeholderposter.png"  #Used for testing


def fetch_image(url):
    """This function takes an Image URL and returns a QPixmap of the image. 

    Args:
        url (str): Image URL

    Returns:
        pixmap (QPixmap): Image Pixmap
    """
    response = requests.get(url)
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(response.content)
    return pixmap


class MyTableWidget(QTableWidget):
    """Class where table and all its functions are contained."""
    def __init__(self, parent):
        super(MyTableWidget, self).__init__(parent)
        self.setEnabled(True)
        # self.setGeometry(QtCore.QRect(32, 40, 1005, 900))
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
        """Checks if keypress was enter on a TableWidgetItem, and if so grabs info from the API to use."""
        key = event.key()
        if key == 16777220 and str(type(self.currentItem())) == "<class 'PyQt5.QtWidgets.QTableWidgetItem'>": 
            current_row = self.currentRow()
            current_column = self.currentColumn()
            if current_column == 1:
                search_title = self.item(current_row, current_column).text()
                search_parameters = {'t': search_title}
                movie_data = requests.get(movie_api, params = search_parameters).json()
                print(movie_data)
                movie_title = movie_data['Title']
                print(movie_title)
                self.currentItem().setText(movie_title) 
                movie_poster_url = movie_data['Poster'] #Fetch Poster
                movie_poster = fetch_image(movie_poster_url)
                poster_label = QtWidgets.QLabel(self) #Image
                pixmap = QPixmap(movie_poster)
                poster_label.setPixmap(pixmap)
                poster_label.setScaledContents(True)
                self.setCellWidget(current_row,0, poster_label)
        else:
            super(MyTableWidget, self).keyPressEvent(event)


# Initalize Windows
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.resize(446, 338)
        self.setWindowTitle("PyRates")
        # Setup Menu Bar
        self._createActions()
        self._createMenuBar()
        # Setup Widgets 
        self.centralwidget = QtWidgets.QWidget()
        self.tableWidget = MyTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(100, 100, 300, 300))
        self.tableWidget(QtCore.Qt.AlignCenter)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 10, 361, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("New Table")
        self.setCentralWidget(self.tableWidget)
        
        
    def _createActions(self):
        self.newAction = QAction("&New Table", self)
        self.saveAction = QAction("&Save", self)
        self.openAction = QAction("&Open...", self)
        self.githubAction = QAction("&GitHub", self)
        self.aboutAction = QAction("&About", self)
        
    def _createMenuBar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        fileMenu = menuBar.addMenu("&File")
        helpMenu = menuBar.addMenu("&Help")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.openAction)
        helpMenu.addAction(self.githubAction)
        helpMenu.addAction(self.aboutAction)
        
        # self.actionNew_Table = QtWidgets.QAction()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
