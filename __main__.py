import sys
import requests
from ctypes import windll
import webbrowser

from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QTableWidget, QMenuBar, QAction)
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

import submenu

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
        self.setAutoFillBackground(False)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.setGridStyle(QtCore.Qt.SolidLine)
        self.setRowCount(5)
        self.setColumnCount(5)
        self.setObjectName("tableWidget")
        # Column 0 = "Poster"
        item = QtWidgets.QTableWidgetItem()
        item.setText("Poster")
        self.setHorizontalHeaderItem(0, item)
        # Column 1 = "Title"
        item = QtWidgets.QTableWidgetItem()
        item.setText("Title")
        self.setHorizontalHeaderItem(1, item)
        # Clear Remaining Columns 
        for n in range(2,6):
            item = QtWidgets.QTableWidgetItem()
            self.setHorizontalHeaderItem(n, item) 
        # Finish Creating Table
        self.horizontalHeader().setDefaultSectionSize(200)
        self.verticalHeader().setDefaultSectionSize(160)
        self.horizontalHeader().setVisible(True)
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
                if movie_data['Response'] == 'True':
                    movie_title = movie_data['Title']
                    print(movie_title)
                    self.currentItem().setText(movie_title) 
                    if 'Poster' in movie_data and movie_data['Poster'] != 'N/A':
                        movie_poster_url = movie_data['Poster'] #Fetch Poster
                        movie_poster = fetch_image(movie_poster_url)
                    else:
                        movie_poster = "placeholderposter.png"
                    poster_label = QtWidgets.QLabel(self) #Image
                    pixmap = QPixmap(movie_poster)
                    poster_label.setPixmap(pixmap)
                    poster_label.setScaledContents(True)
                    self.setCellWidget(current_row,0, poster_label)
                else: 
                    self.currentItem().setText("Movie not found!") 
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
        self.centralwidget.setLayout(QtWidgets.QVBoxLayout())
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("New Table")
        self.centralwidget.layout().addWidget(self.label)
        self.tableWidget = MyTableWidget(self.centralwidget)
        self.tableWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.centralwidget.layout().addWidget(self.tableWidget)
        self.setCentralWidget(self.centralwidget)

    def _createActions(self):
        self.newAction = QAction("&New Table", self)
        self.saveAction = QAction("&Save", self)
        self.openAction = QAction("&Open...", self)
        self.aboutAction = QAction("&About", self)
        self.githubAction = QAction("&GitHub", self)
        
        self.aboutAction.triggered.connect(self.openAbout)
        self.githubAction.triggered.connect(self.openGithub)
        
    def _createMenuBar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        fileMenu = menuBar.addMenu("&File")
        helpMenu = menuBar.addMenu("&Help")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.openAction)
        helpMenu.addAction(self.aboutAction)    
        helpMenu.addAction(self.githubAction)
        
    def openAbout(self, s):
        print("About Window Opened")
        self.about = submenu.AboutMenu()
        self.about.show()
        
    def openGithub(self, s):
        webbrowser.open("https://github.com/salmonsquared/pyrates")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
