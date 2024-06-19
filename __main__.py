import utils
import tkinter
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1) # Fixes blurry text on W11

tkinter._test()
