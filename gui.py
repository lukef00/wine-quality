import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd

import tabs

DATASET = None

class StatusBar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self)
        self.label.pack(side=tk.LEFT)
        self.pack(side=tk.BOTTOM, fill=tk.X)

    def set(self, newText, color):
        self.label.config(text=newText, fg=color)

    def clear(self):
        self.label.config(text="")


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.create_menu(master)
        self.create_status_bar(master)
        self.create_tabs(master)

        self.add_keybinds(master)
        self.pack()


    def create_menu(self, master):
        self.menu = Menu(master)
        file_menu = Menu(self.menu, tearoff = 0)
        file_menu.add_command(label = "Load dataset", command=self.load_dataset)
        file_menu.add_separator()
        file_menu.add_command(label = "Exit", command = master.destroy)
        self.menu.add_cascade(label = "File", menu = file_menu)
        self.master.config(menu = self.menu)


    def create_status_bar(self, master):
        self.status = StatusBar(master)
        self.status.set("Dataset not loaded", '#ff0000')


    def create_tabs(self, master):
        self.tabController = ttk.Notebook(master)
        self.statistics = tabs.StatsTab(self.tabController)
        self.plots = tabs.Plots(self.tabController)
        self.export = tabs.ExportTab(self.tabController)
        # TODO: change lines below into classes and place them in tabs.py,

        self.tabController.add(self.statistics, text="Statistical data")
        self.tabController.add(self.plots, text="Plots")
        self.tabController.add(self.export, text="Export")

        self.tabController.pack(expand = 1, fill='both')


    def add_keybinds(self, master):
        master.bind('<Control-o>', self.load_dataset)


    def load_dataset(self, event = None):
        filetypes = (
                ('csv', '*.csv'),
                ('text files', '*.txt'),
                ('All files', '*.*')
                )

        filename = filedialog.askopenfilename(
                title='Open a file',
                filetypes=filetypes)

        DATASET = pd.read_csv(filename, sep=";")
        self.status.set("Dataset loaded", '#00ff00')
        self.statistics.set_data_frame(DATASET)
        self.plots.set_data_frame(DATASET)
        self.export.set_data_frame(DATASET)



root = tk.Tk()
root.geometry("800x600")
myapp = App(root)
myapp.mainloop()
