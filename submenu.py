from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QTableWidget, QMenuBar, QAction)
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

import sys

class AboutMenu(QMessageBox):
    """This class creates a window that displays information about PyRates."""
    def __init__(self):
        super().__init__()
        self.setText("PyRates is a simple software that allows a user to quickly create tables of movie ratings in a similar fashion to Letterboxd. These tables then can be exported to HTML or XML for personal use.\n\nTo begin, type the title of the movie you wish to rate in a cell in the Title column and hilight it. Press enter to search IMDB for the movie, and the poster will automatically be put in the first column.\n\nMade in PyQt5 by Jay.")
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle("PyRates Help")