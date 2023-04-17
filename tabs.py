import tkinter as tk
from idlelib import window
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class StatsTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.df = None
        self.frame = ttk.Frame.__init__(self, master)
        tk.Label(self, text="Stats Page", font=('bold')).pack()
        self.prepare_table()


    def set_data_frame(self, df):
        if not self.df:
           self.table_frame.pack()

        self.df = df
        self.column_names = df.columns.values.tolist()
        self.calculate()


    def calculate(self):
        min_vals = self.df.min()
        max_vals = self.df.max()
        mean_vals = self.df.mean()
        median_vals = self.df.median()
        mode_vals = self.df.mode()
        std_vals = self.df.std()

        for key in min_vals.keys():
            self.tree.insert('', 
                             tk.END, 
                             values=(
                                 key,
                                 min_vals[key],
                                 max_vals[key],
                                 round(mean_vals[key], 5),
                                 median_vals[key],
                                 mode_vals[key].at[0],
                                 round(std_vals[key], 5),
                                 )
                             )


    def prepare_table(self):
        self.table_frame = Frame(self)
        scrollbar = Scrollbar(self.table_frame)
        scrollbar.pack(side = RIGHT, fill = Y)
        self.tree = ttk.Treeview(
                self.table_frame,
                yscrollcommand=scrollbar.set,
                columns = ('column', 'min', 'max', 'mean', 'median', 'mode', 'standard deviation'),
                show = 'headings'
                )

        for col in self.tree['columns']:
            self.tree.heading(col, text = col)
            self.tree.column(col, width = 80, anchor = 'e')

        self.tree.column('column', width = 150, anchor = 'w')
        self.tree.column('standard deviation', width = 150)
        scrollbar.config(command=self.tree.yview)

        self.tree.pack()




class Plots(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.canvas= None
        self.df = None
        self.frame = ttk.Frame.__init__(self, master)

         #

        #

    def set_data_frame(self, df):
        self.df = df
        self.column_names = df.columns.values.tolist()
        self.create_plot()
    def create_plot(self):
        tk.Label(self, text="Plots", font=('bold')).pack()

        fig = Figure(figsize=(6, 6), dpi=100)
        y = [self.df.loc[:, "pH"].min(), self.df.loc[:, "pH"].max()]

        x = [1, 2]


        plot1 = fig.add_subplot(111)
        plot1.plot(y)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas.get_tk_widget().pack()


class ExportTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.df = None
        self.boxes = dict()
        self.frame = ttk.Frame.__init__(self, master)
        tk.Label(self, text="Export Page", font=('bold')).pack()

    def set_data_frame(self, df):
        self.df = df
        self.column_names = df.columns.values.tolist()
        self.prepare_checkboxes()


    def prepare_checkboxes(self):
        for col in self.column_names:
            self.boxes[col] = tk.IntVar()
            self.boxes[col].set(1)
            ttk.Checkbutton(self,
                            text=col,
                            command=None,
                            variable=self.boxes[col],
                            ).pack(side = tk.LEFT)

        tk.Button(self, text="Export", command=self.exportData).pack()

    def exportData(self):
        columns_to_drop = []
        for key in self.boxes.keys():
            if self.boxes[key].get() == 0:
                columns_to_drop.append(key)

        new_df = self.df.drop(columns=columns_to_drop)
        new_df.to_csv('export.csv', index = False, mode = 'w+')