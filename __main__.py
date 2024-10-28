import sys
import requests
import webbrowser
import csv
from ctypes import windll


from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QMainWindow, QMessageBox, QTableWidget, QMenuBar, QAction)
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
                        movie_poster_url = "placeholderposter.png"
                        movie_poster = "placeholderposter.png"
                    poster_label = QtWidgets.QLabel(self) #Image
                    pixmap = QPixmap(movie_poster)
                    poster_label.setPixmap(pixmap)
                    poster_label.setScaledContents(True)
                    self.setItem(current_row, 0, QtWidgets.QTableWidgetItem(str(movie_poster_url)))
                    self.setCellWidget(current_row, 0, poster_label)
                else: 
                    self.currentItem().setText("Movie not found!") 
        else:
            super(MyTableWidget, self).keyPressEvent(event)


# Initalize Windows
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.resize(1050, 1000)
        self.setWindowTitle("PyRates")
        # Setup Menu Bar
        self._createActions()
        self._createMenuBar()
        # Setup Widgets 
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setLayout(QtWidgets.QVBoxLayout())
        # Heading Label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("New Table")
        self.centralwidget.layout().addWidget(self.label)
        # Table Widget
        self.tableWidget = MyTableWidget(self.centralwidget)
        self.tableWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.centralwidget.layout().addWidget(self.tableWidget)
        # Buttons
        self.button_holder = QtWidgets.QWidget()
        self.button_holder.setLayout(QtWidgets.QHBoxLayout())
        self.deleteRowButton = QtWidgets.QPushButton("-")
        self.newRowButton = QtWidgets.QPushButton("+")
        self.button_holder.layout().addWidget(self.deleteRowButton)
        self.button_holder.layout().addWidget(self.newRowButton)
        self.centralwidget.layout().addWidget(self.button_holder, alignment=QtCore.Qt.AlignCenter)
        # Finalization
        self.setCentralWidget(self.centralwidget)
        self.deleteRowButton.clicked.connect(self.deleteRow)
        self.newRowButton.clicked.connect(self.addRow)

    def _createActions(self):
        self.newAction = QAction("&New Table", self)
        self.saveAction = QAction("&Save as CSV", self)
        self.exportAction = QAction("&Export as HTML", self)
        self.openAction = QAction("&Open...", self)
        self.aboutAction = QAction("&About", self)
        self.githubAction = QAction("&GitHub", self)
        
        self.aboutAction.triggered.connect(self.openAbout)
        self.githubAction.triggered.connect(self.openGithub)
        self.saveAction.triggered.connect(self.saveFile)
        self.openAction.triggered.connect(self.openFile)
        
    def _createMenuBar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        fileMenu = menuBar.addMenu("&File")
        helpMenu = menuBar.addMenu("&Help")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exportAction)
        fileMenu.addAction(self.openAction)
        helpMenu.addAction(self.aboutAction)        
        helpMenu.addAction(self.githubAction)
        
    def openAbout(self, s):
        self.about = submenu.AboutMenu()
        self.about.show()
        
    def openGithub(self, s):
        webbrowser.open("https://github.com/salmonsquared/pyrates")
        
    def addRow(self):
        lastRow = self.tableWidget.rowCount()
        self.tableWidget.insertRow(lastRow) 

    def deleteRow(self):
        lastRow = self.tableWidget.rowCount()
        self.tableWidget.removeRow(lastRow-1)
        
    #Saving and Exporting
    def saveFile(self, s):
        file = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV (*.csv)")
        writer = csv.writer(open(file[0], "x", newline=''), delimiter=',', quotechar='|') # Talk about how needed to use open() to ensure file was created
        for r in range(self.tableWidget.rowCount()):
            row_items = []
            for c in range(self.tableWidget.columnCount()):
                if self.tableWidget.item(r, c) is not None:
                    row_items.append(self.tableWidget.item(r, c).text())
                else:
                    row_items.append("")
            writer.writerow(row_items)
        print("File saved to " + file[0])
        
    #Opening
    def openFile(self, s):
        file = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV (*.csv)")
        reader = csv.reader(open(file[0], 'r',), delimiter=',', quotechar='|') # Talk about how needed to use open() to ensure file was created
        loaded_rows = 0
        self.tableWidget.setRowCount(loaded_rows) #Talk about how using row in reader twice didnt work initially, but looking into it the pointer was at the end and needed to be reset
        for row in reader:
            loaded_rows += 1
            self.tableWidget.setRowCount(loaded_rows)
            for c in range(5):
                self.tableWidget.setItem((loaded_rows - 1), c, QtWidgets.QTableWidgetItem(str(row[c])))
        print("File opened at " + file[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
