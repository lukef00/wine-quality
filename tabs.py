import tkinter as tk
import re
from functools import partial
from idlelib import window
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.filedialog import asksaveasfile

import label as label
import pandas as pd
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
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

class Correlation(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.df = None
        self.frame = ttk.Frame.__init__(self, master)
        tk.Label(self, text="Correlation", font=('bold')).pack()
    def set_data_frame(self, df):
        self.df = df
        self.column_names = df.columns.values.tolist()
        self.prepare_correlation_table()
        tk.Button(self, text="Open correlation heatmap in new window", command=lambda: self.createHeatmap()).pack(pady=1)

    def createHeatmap(self):
        data = self.df.corr(method='pearson')
        sns.set()
        ax = sns.heatmap(data,annot=True, vmin=(-1), vmax=1)
        plt.show()

    def prepare_correlation_table(self):
        self.table_frame = Frame(self)
        columns =("column","fix_acid","vol_acid","cit_acid","res_sugar","chlorides","fsd","tsd","dens","pH","sulp","alco","score")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text = col)
            self.tree.column(col, width = 80, anchor = 'e')

        self.tree.column('column', width = 150, anchor = 'w')


        self.tree.column('score', width = 150)

        self.tree.pack()

        data = self.df.corr(method='pearson')

        print(data)
        print(data.iloc[0,0])
        column_headers = list(data.columns.values)
        print(column_headers)
        for i in range(12):
            self.tree.insert("", 'end',values=(column_headers[i], "{:.3f}".format(data.iloc[i,0]),"{:.3f}".format(data.iloc[i,1]),"{:.3f}".format(data.iloc[i,2]),"{:.3f}".format(data.iloc[i,3]),"{:.3f}".format(data.iloc[i,4]),"{:.3f}".format(data.iloc[i,5]),"{:.3f}".format(data.iloc[i,6]),"{:.3f}".format(data.iloc[i,7]),"{:.3f}".format(data.iloc[i,8]),"{:.3f}".format(data.iloc[i,9]),"{:.3f}".format(data.iloc[i,10]),"{:.3f}".format(data.iloc[i,11])         ))





class Plots(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.canvas= None
        self.df = None
        self.frame = ttk.Frame.__init__(self, master)




    def set_data_frame(self, df):
        self.df = df
        self.column_names = df.columns.values.tolist()
        self.create_plot()
    def create_plot(self):


        def show():
            label.config(text=clicked.get())

        options = [
                "fix_acid",
                "vol_acid",
                "cit_acid",
                "res_sugar",
                "chlorides",
                "fsd",
                "tsd",
                "dens",
                "pH",
                "sulp",
                "alco"
                ]
        clicked = StringVar()
        clicked.set("fix_acid")
        clicked2 = StringVar()
        clicked2.set("pH")


        xname=clicked.get()
        yname=clicked2.get()

        #  tk.Label(self, text="wykres "+xname +" od "+yname, font=('bold')).pack()
        fig = Figure(figsize=(6, 6), dpi=100)

        x = [x for x in self.df.loc[:, xname]]
        y = [x for x in self.df.loc[:, yname]]
        plot1 = fig.add_subplot(111)
        plot1.scatter(x,y)
        plot1.set_ylabel(yname)
        plot1.set_xlabel(xname)
        plot1.set_title("graph showing the dependence  of "+xname +" on "+yname)

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas.get_tk_widget().pack()


        def clearPlot(self,plot1):
            xname = clicked.get()
            yname = clicked2.get()

            x = [x for x in self.df.loc[:, xname]]
            y = [x for x in self.df.loc[:, yname]]
            plot1.clear()
            plot1.set_title("graph showing the dependence  of " + xname + " on " + yname)
            plot1.scatter(x,y)
            plot1.set_ylabel(yname)
            plot1.set_xlabel(xname)

            self.canvas.draw()

        drop = OptionMenu(self, clicked, *options)
        drop.pack()
        drop2 = OptionMenu(self, clicked2, *options)
        drop2.pack();

        ttk.Button(self, text="Change Plot", command= lambda: clearPlot(self,plot1) ).pack(pady=1)



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
        grid_frame = tk.Frame(self)
        grid_frame.pack()
        for i, col in enumerate(self.column_names):
            self.boxes[col] = tk.IntVar()
            self.boxes[col].set(1)
            ttk.Checkbutton(grid_frame,
                            text=col,
                            command=None,
                            variable=self.boxes[col],
                            ).grid(row = i // 3, column= i % 3, sticky= 'w', padx=10, pady=10)

        self.regex_box = tk.Entry(self)
        self.regex_box.pack()
        tk.Button(self, text="Export", command=self.exportData).pack()

    def exportData(self):
        files = [('CSV', '*.csv')]
        file = asksaveasfile(filetypes = files, defaultextension = files)
        items = self.regex_box.get().split(" ")
        rows = []
        if len(items) > 0:
            for item in items:
                if re.match('^\d+-\d+$', item):
                    # range
                    temp = [int(x) for x in item.split('-')]
                    for x in list(range(temp[0], temp[1] + 1)):
                        rows.append(x)
                elif re.match('^\d+$', item):
                    rows.append(int(item))


        columns_to_drop = []
        for key in self.boxes.keys():
            if self.boxes[key].get() == 0:
                columns_to_drop.append(key)

        new_df = self.df.drop(columns=columns_to_drop)
        if len(rows):
            print(rows)
            new_df = new_df.iloc[rows]
        new_df.to_csv(file, index = False, mode = 'w+')
