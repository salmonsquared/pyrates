from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QTableWidget, QMenuBar, QAction)
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

import sys

class AboutMenu(QtWidgets.QWidget):
    """This class creates a window that displays information about PyRates."""
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel(
            """PyRates is a simple software that allows a user to quickly create tables of
            movie ratings in a similar fashion to Letterboxd. These tables then can be
            exported to HTML or XML for personal use.
            \n
            Made using PyQt5.""", self)