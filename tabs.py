import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd


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

        self.df = None
        self.frame = ttk.Frame.__init__(self, master)
        tk.Label(self, text="Plots", font=('bold')).pack()

    def set_data_frame(self, df):
        if not self.df:
            self.table_frame.pack()

        self.df = df
        self.column_names = df.columns.values.tolist()


