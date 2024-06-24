import utils # Local Package
import tkinter as tk
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1) # Fixes blurry text on W11

cookies = 0

def when_clicked():
    global cookies
    cookies += 1
    cookie_text.set(str(cookies))

# Initalize Windows
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, width=800, height=500)
        self.parent = parent

if __name__ == "__main__":
    root = tk.Tk()
    root.title('PyRates')
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()