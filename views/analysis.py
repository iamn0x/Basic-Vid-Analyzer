import tkinter as tk
from tkinter import ttk
from modules.DataAnalyzer import DataAnalyzer
from tkinter import filedialog
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import style
style.use('ggplot')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class Analysis(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)


        self.container = tk.Frame(self)
        self.container.grid()

        self.leftContainer = tk.Frame(self.container)
        self.leftContainer.grid(row=0 ,column=0)
        self.loadDataButton = ttk.Button(self.leftContainer, text='Load Data', command=self.loadDataFunc)
        self.loadDataButton.grid(row=0, column=0, padx=20, pady=5)
        self.startDataButton = ttk.Button(self.leftContainer, text='Start Analysis', command=self.startDataFunc)
        self.startDataButton.grid(row=1, column=0, padx=20, pady=5)

        self.rightContainer = tk.Frame(self.container)
        self.rightContainer.grid(row=0, column=1)

        self.graphOptionsContainer = tk.Frame(self.rightContainer)
        self.graphOptionsContainer.grid(row=0, column=0)

        self.makeClearGraph()

    def makeClearGraph(self):
        self.f = Figure(figsize=(8, 5), dpi=100)
        self.avg = self.f.add_subplot(111)
        self.Canvas = FigureCanvasTkAgg(self.f, master=self)
        self.Canvas.get_tk_widget().grid(row=3, column=0)
        self.toolbar_frame = tk.Frame(self.graphOptionsContainer)
        self.Toolbar = NavigationToolbar2Tk(self.Canvas, self.toolbar_frame)
        self.Toolbar.update()
        self.toolbar_frame.grid(row=2, column=0)

        # self.toolbar_frame = tk.Frame(self.graphOptionsContainer)
        # self.Myfig = plt.figure()
        # self.Canvas = FigureCanvasTkAgg(self.Myfig, master=self)
        # self.Toolbar = NavigationToolbar2Tk(self.Canvas, self.toolbar_frame)
        # self.Toolbar.update()
        # self.toolbar_frame.grid(row=2, column=0)
        # self.Canvas._tkcanvas.grid(row=3, column=0)
        # self.avg = self.Myfig.add_subplot(111)

    def drawGraph(self, folderName, x):

        self.makeClearGraph()
        currentDir = self.dictFolderDir[folderName]
        currentData = self.dictDirDataAnalyzer[currentDir].data

        xtemp = []
        xtime = []

        yred = []
        ygreen = []
        yblue = []

        for i in currentData.keys():
            if currentData[i]['temperature'] == None:
                xtemp.append(-1)
            else:
                xtemp.append(currentData[i]['temperature'])

            xtime.append(currentData[i]['time'])
            yred.append(currentData[i]['red'])
            ygreen.append(currentData[i]['green'])
            yblue.append(currentData[i]['blue'])

        osx = None
        if x == 'temperature':
            osx = xtemp
            xlabel = 'Temperature'

        if x == 'time':
            xlabel = 'Time'
            osx = xtime

        if osx != None:
            self.avg.clear()
            self.avg.plot(osx, yred, "ro", osx, ygreen, "go", osx, yblue, 'bo')
            plt.ylabel('Average of pixels')
            plt.xlabel(xlabel)
            plt.setp(self.avg.get_xticklabels(), rotation=30, horizontalalignment='right')
            self.Canvas.draw()
            # self.avgR = self.Myfig.add_subplot(111)
            # #self.avgR.plot(xtemp, yred, '-', color='red', lw=1)
            # self.avgR.scatter(xtemp, yred)
            #
            # self.avgG = self.Myfig.add_subplot(111)
            # #self.avgG.plot(xtemp, ygreen, '-', color='green', lw=1)
            # self.avgG.scatter(xtemp, ygreen)
            #
            # self.avgB = self.Myfig.add_subplot(111)
            # #self.avgB.plot(xtemp, yblue, '-', color='blue', lw=1)
            # self.avgB.scatter(xtemp, yblue)
            #
            # plt.ylabel('Average of pixels')
            # plt.xlabel('Temperature')
            # self.Canvas.draw()

        # if x == 'time':
        #     self.avgR = self.Myfig.add_subplot(111)
        #     #self.avgR.plot(xtime, yred, '-', color='red', lw=1)
        #     self.avgR.scatter(xtime, yred)
        #
        #     self.avgG = self.Myfig.add_subplot(111)
        #     #self.avgG.plot(xtime, ygreen, '-', color='green', lw=1)
        #     self.avgG.scatter(xtime, ygreen)
        #
        #     self.avgB = self.Myfig.add_subplot(111)
        #     #self.avgB.plot(xtime, yblue, '-', color='blue', lw=1)
        #     self.avgB.scatter(xtime, yblue)
        #
        #
        #     plt.ylabel('Average of pixels')
        #     plt.xlabel('Time')
        #     self.Canvas.draw()


    def loadDataFunc(self):
        dirselect = filedialog.Directory()
        self.dirsList = []
        while True:
            d = dirselect.show()
            if not d:
                break
            self.dirsList.append(d)

        self.createOptionMenu()


    def createOptionMenu(self):
        self.folderList = []
        for i in range(len(self.dirsList)):
            self.folderList.append(self.dirsList[i][len(self.dirsList[i]) - self.dirsList[i][::-1].find('/'):
                                                    len(self.dirsList[i])])

        self.dictFolderDir = {}

        for i in range(len(self.folderList)):
            self.dictFolderDir[self.folderList[i]] = self.dirsList[i]

        self.folderList.insert(0, self.folderList[0])
        self.folderListVar = tk.StringVar(self.graphOptionsContainer)
        self.folderListVar.set(self.folderList[0])

        self.graphOptionMenu = ttk.OptionMenu(self.graphOptionsContainer, self.folderListVar, *self.folderList,
                                              command=lambda x: self.drawGraph(self.folderListVar.get(), self.xListVar.get()))
        self.graphOptionMenu.grid(row=0, column=0)

        self.xList = ['temperature', 'time']
        self.xList.insert(0, self.xList[0])
        self.xListVar = tk.StringVar(self.graphOptionsContainer)
        self.xListVar.set(self.xList[0])

        self.xOptionMenu = ttk.OptionMenu(self.graphOptionsContainer, self.xListVar, *self.xList,
                                              command=lambda x: self.drawGraph(self.folderListVar.get(), self.xListVar.get()))
        self.xOptionMenu.grid(row=0, column=1)


    def startDataFunc(self):
        self.dataAnalyzerList = []
        self.dictDirDataAnalyzer = {}

        for i in range(len(self.dirsList)):
            self.dataAnalyzerList.append(DataAnalyzer(self.dirsList[i]))
            self.dictDirDataAnalyzer[self.dirsList[i]] = self.dataAnalyzerList[i]
            self.dataAnalyzerList[i].analyseData()

        self.drawGraph(self.folderListVar.get(), self.xListVar.get())