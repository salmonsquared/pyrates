"""This file holds the main functionality for PyRates."""

import sys
import os
import requests
import webbrowser
import csv
import submenu

from ctypes import windll
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QTableWidget,
    QMenuBar,
    QAction
)


windll.shcore.SetProcessDpiAwareness(1)  # Fixes blurry text on W11
movie_api = "http://www.omdbapi.com/?apikey=7c6a9526&"
placeholder_poster = "placeholderposter.png"  # Used for testing


def fetch_image(url):
    """Take an image URL and return a QPixmap of the image.

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
        """Create a MyTableWidget."""
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
        for n in range(2, 6):
            item = QtWidgets.QTableWidgetItem()
            self.setHorizontalHeaderItem(n, item)
        # Finish Creating Table
        self.horizontalHeader().setDefaultSectionSize(200)
        self.verticalHeader().setDefaultSectionSize(160)
        self.horizontalHeader().setVisible(True)
        self.verticalHeader().setVisible(False)

    def keyPressEvent(self, event):
        """Check if keypress was enter, and if so grab info from the API."""
        key = event.key()
        if key == 16777220 and \
            str(type(self.currentItem()) == "<class 'PyQt5.QtWidgets.QTableWidgetItem'>"):
            current_row = self.currentRow()
            current_column = self.currentColumn()
            if current_column == 1:
                search_title = self.item(current_row, current_column).text()
                search_parameters = {'t': search_title}
                movie_data = requests.get(movie_api, params=search_parameters).json()
                print(movie_data)
                if movie_data['Response'] == 'True':
                    movie_title = movie_data['Title']
                    print(movie_title)
                    self.currentItem().setText(movie_title)
                    if ('Poster' in movie_data and
                        movie_data['Poster'] != 'N/A'):
                        movie_poster_url = movie_data['Poster']  # Fetch Poster
                        movie_poster = fetch_image(movie_poster_url)
                    else:
                        movie_poster_url = "placeholderposter.png"
                        movie_poster = "placeholderposter.png"
                    poster_label = QtWidgets.QLabel(self)  # Image
                    pixmap = QPixmap(movie_poster)
                    poster_label.setPixmap(pixmap)
                    poster_label.setScaledContents(True)
                    self.setItem(current_row, 0,
                                 QtWidgets.QTableWidgetItem(str(movie_poster_url)))
                    self.setCellWidget(current_row, 0, poster_label)
                else:
                    self.currentItem().setText("Movie not found!")
        else:
            super(MyTableWidget, self).keyPressEvent(event)


# Initalize Windows
class MainWindow(QMainWindow):
    """Represents the main window the PyRates user sees."""

    def __init__(self, parent=None):
        """Create Main Window."""
        super(MainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.resize(1050, 1000)
        self.setWindowTitle("PyRates")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        # Setup Menu Bar
        self._create_actions()
        self._create_menu_bar()
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
        self.tableWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                       QtWidgets.QSizePolicy.Expanding)
        self.centralwidget.layout().addWidget(self.tableWidget)
        # Buttons
        self.button_holder = QtWidgets.QWidget()
        self.button_holder.setLayout(QtWidgets.QHBoxLayout())
        self.deleteRowButton = QtWidgets.QPushButton("-")
        self.newRowButton = QtWidgets.QPushButton("+")
        self.button_holder.layout().addWidget(self.deleteRowButton)
        self.button_holder.layout().addWidget(self.newRowButton)
        self.centralwidget.layout().addWidget(self.button_holder,
                                              alignment=QtCore.Qt.AlignCenter)
        # Finalization
        self.setCentralWidget(self.centralwidget)
        self.deleteRowButton.clicked.connect(self.delete_row)
        self.newRowButton.clicked.connect(self.add_row)

    def _create_actions(self):
        self.newAction = QAction("&New Table", self)
        self.saveAction = QAction("&Save as CSV", self)
        self.exportAction = QAction("&Export as HTML", self)
        self.openAction = QAction("&Open...", self)
        self.aboutAction = QAction("&About", self)
        self.githubAction = QAction("&GitHub", self)
        self.aboutAction.triggered.connect(self.open_about)
        self.githubAction.triggered.connect(self.open_github)
        self.newAction.triggered.connect(self.new_file)
        self.saveAction.triggered.connect(self.save_file)
        self.exportAction.triggered.connect(self.export_file)
        self.openAction.triggered.connect(self.open_file)

    def _create_menu_bar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        file_menu = menu_bar.addMenu("&File")
        help_menu = menu_bar.addMenu("&Help")
        file_menu.addAction(self.newAction)
        file_menu.addAction(self.saveAction)
        file_menu.addAction(self.exportAction)
        file_menu.addAction(self.openAction)
        help_menu.addAction(self.aboutAction)
        help_menu.addAction(self.githubAction)

    def open_about(self, s):
        """Open the about infobox."""
        self.about = submenu.AboutMenu()
        self.about.show()
  
    def open_github(self, s):
        """Open the PyRates GitHub."""
        webbrowser.open("https://github.com/salmonsquared/pyrates")

    def add_row(self):
        """Add a row to the table."""
        last_row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(last_row)

    def delete_row(self):
        """Delete a row from the table."""
        last_row = self.tableWidget.rowCount()
        self.tableWidget.removeRow(last_row-1)
  
    # Saving and Exporting
    def save_file(self, s):
        """Save file to CSV."""
        file = QFileDialog.getSaveFileName(self, "Save CSV File",
                                           "", "CSV (*.csv)")
        writer = csv.writer(open(file[0], "w", newline=''),
                            delimiter=',', quotechar='|')
        for r in range(self.tableWidget.rowCount()):
            row_items = []
            for c in range(self.tableWidget.columnCount()):
                if self.tableWidget.item(r, c) is not None:
                    row_items.append(self.tableWidget.item(r, c).text())
                else:
                    row_items.append("")
            writer.writerow(row_items)
        print("File saved to " + file[0])

    # Opening
    def open_file(self, s):
        """Open table from CSV file."""
        file = QFileDialog.getOpenFileName(self, "Open CSV File",
                                           "", "CSV (*.csv)")
        reader = csv.reader(open(file[0], 'r',), delimiter=',', quotechar='|')
        loaded_rows = 0
        self.tableWidget.setRowCount(loaded_rows)
        for row in reader:
            loaded_rows += 1
            self.tableWidget.setRowCount(loaded_rows)
            for c in range(5):
                self.tableWidget.setItem((loaded_rows - 1), c, QtWidgets.QTableWidgetItem(str(row[c])))
        print("File opened at " + file[0])

    # Exporting to HTML
    def export_file(self, s):
        """Export table contents to HTML."""
        file = QFileDialog.getSaveFileName(self, "Save HTML File",
                                           "", "Hyper Text Markup Language file (*.html)")
        html_file = open(file[0], 'w')
        html_file.write("<table>\n  <tr>")
        for h in range(self.tableWidget.columnCount()):
            html_file.write("       <th>" 
                            + self.tableWidget.horizontalHeaderItem(h).text() 
                            + "</th>")
        html_file.write("   </tr>")
        for r in range(self.tableWidget.rowCount()):
            html_file.write("   <tr>")
            for c in range(self.tableWidget.columnCount()):
                if self.tableWidget.item(r, c) is not None:
                    if c == 0:
                        html_file.write("       <td><img src="
                                        + self.tableWidget.item(r, c).text()
                                        + "></td>")
                    else:
                        html_file.write("       <td>"
                                        + self.tableWidget.item(r, c).text()
                                        + "</td>")
                else:
                    html_file.write("      <td></td>")
            html_file.write("   </tr>")
        html_file.write("</table>")
        
    def new_file(self, s):
        """Restart program"""
        os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
