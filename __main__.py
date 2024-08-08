import utils # Local Package
import tkinter as tk
import requests
import json
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1) # Fixes blurry text on W11
movie_api = "http://www.omdbapi.com/?apikey=7c6a9526&"

# Initalize Windows
class MainApplication(tk.Frame): #Whole UI 
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(1, weight=1)

        graph_label = tk.Label(parent, text="Graph", borderwidth=1, relief='solid')

        graph_label.grid(row=0, column=1, sticky='nswe', pady=2)
        DisplayedGrid(self).grid(row=1, column=1, sticky = 'nswe', pady = 2, padx = 50)

class DisplayedGrid(tk.Frame): #Inner Displayed Rating Graph
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        for x in range(5):
            parent.columnconfigure(x, weight=1, minsize=200)
            parent.rowconfigure(x, weight=1, minsize=150)
            header = tk.Label(text="Header")
            for y in range(5):
                title = PosterCell(parent)
                title.grid(row=x, column=y, sticky = 'nswe')

class PosterCell(tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent)
        self.parent = parent

        def enter_pressed(x):
            movie_title = self.get()
            print(movie_title)
            search_parameters = {'t': movie_title}
            movie_data = requests.get(movie_api, params = search_parameters).json()
            print(movie_data)
            movie_poster = movie_data['Poster']
            print(movie_poster)
        self.bind("<Return>", enter_pressed)

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