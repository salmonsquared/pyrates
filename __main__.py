import utils # Local Package
import tkinter as tk
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1) # Fixes blurry text on W11

# Initalize Windows
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, width=800, height=500)
        self.parent = parent

        graph_label = tk.Label(parent, text="Graph")

        c1 = tk.Label(parent, text = "Empty", background = 'yellow')
        graph = tk.DisplayedGrid(parent)
        c2 = tk.Label(parent, text = "Empty", background = 'yellow')


        graph_label.grid(row=0, column=1, sticky='ns', pady=2)
        c1.grid(row=1, column=0)
        graph.grid(row=1, column=1, sticky = 'ns', pady = 2)
        c2.grid(row=1, column=2)

class DisplayedGrid(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, borderwidth=1)
        self.parent = parent
        title = tk.Label(parent, text = "Cell", background = 'blue')

        for x in range(5):
            for y in range(5):
                title.grid(row=x, column=y)

if __name__ == "__main__":
    root = tk.Tk()

    menubar = tk.Menu(root)      
    file = tk.Menu(menubar, tearoff = 0)
    menubar.add_cascade(label ='File', menu = file)
    file.add_command(label = "New Table...")
    file.add_command(label = "Save")
    file.add_command(label = "Open...")

    help = tk.Menu(menubar, tearoff = 0)
    menubar.add_cascade(label ='Help', menu = help)
    help.add_command(label = "Help")
    help.add_command(label = "Github")
    help.add_command(label = "About")

    root.title('PyRates')
    root.config(menu = menubar)
    MainApplication(root).grid(row = 1, column = 1)
    root.mainloop()