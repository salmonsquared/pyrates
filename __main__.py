import utils
import tkinter as tk
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1) # Fixes blurry text on W11

window = tk.Tk()
greeting = tk.Label(text="Hello World")
greeting.pack()
window.mainloop()