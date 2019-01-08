import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from modules.Camera import Camera
from modules.Settings import Settings
from modules.MakeData import MakeData
from modules.MouseCropper import MouseCropper
from modules.TempReader import TempReader
import time
import cv2
import os
import asyncio
import threading

class Make(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        settings = Settings.getInstance()
        self.camera = Camera(settings.cameraNumber)
        self.camera = settings.setCamProperties(self.camera)
        self.makeDataList = []
        self.TempReader = TempReader()
        self.do_temp = False
        self.temperaturePort = settings.portName

        ############  LEFT  ###############
        ################ MAKE DATA OPTIONS ###################

        self.makeDataContainer = tk.Frame(self)
        self.makeDataContainer.grid(row=0, column=0, sticky='N', columnspan=2)

        self.label11 = ttk.Label(self.makeDataContainer, text='Make Data Settings', font='Helvetica 10 bold')
        self.label11.grid(row=0, column=0, columnspan=3)

        self.label12 = ttk.Label(self.makeDataContainer, text='Making Data Time method: ')
        self.label12.grid(row=1, column=0)
        self.makeDataTimeList = ['Count of Photos', 'Count of Time']
        self.makeDataTimeList.insert(0, self.makeDataTimeList[0])
        self.variable4 = tk.StringVar(self.makeDataContainer)
        self.variable4.set(self.makeDataTimeList[0])
        self.dropdownmenu4 = ttk.OptionMenu(self.makeDataContainer, self.variable4, *self.makeDataTimeList,
                                            command=self.makeDataTimeMethodInterfaceUpdate)
        self.dropdownmenu4.grid(row=1, column=1, sticky='news')

        self.label13 = ttk.Label(self.makeDataContainer, text='Making Data Photo method: ')
        self.label13.grid(row=2, column=0)
        self.makeDataPhotoList = ['Count of Frames']
        self.makeDataPhotoList.insert(0, self.makeDataPhotoList[0])
        self.variable5 = tk.StringVar(self.makeDataContainer)
        self.variable5.set(self.makeDataPhotoList[0])
        self.dropdownmenu5 = ttk.OptionMenu(self.makeDataContainer, self.variable5, *self.makeDataPhotoList, command='')
        self.dropdownmenu5.grid(row=2, column=1, sticky='news')

        self.makeDataFramesContainer = tk.Frame(self.makeDataContainer)
        self.makeDataFramesContainer.grid(row=2, column=2)
        self.makeDataFramesSpinboxVar = tk.StringVar(self.makeDataFramesContainer)
        self.makeDataCountOfFramesSpinbox = tk.Spinbox(self.makeDataFramesContainer, from_=0, to=144,
                                                           textvariable=self.makeDataFramesSpinboxVar,
                                                           width=21, command=self.makeDataUpdateCountOfFrames)
        self.makeDataCountOfFramesSpinbox.grid(row=0, column=0)


        ############ AREA #################
        areaContainer = tk.Frame(self)
        areaContainer.grid(row=1, column=0, sticky='N', columnspan=2)

        self.label10 = ttk.Label(areaContainer, text='Area Settings', font='Helvetica 10 bold')
        self.label10.grid(row=0, column=0, columnspan=2)

        self.scrollbar = ttk.Scrollbar(areaContainer, orient='vertical')
        self.scrollbar.grid(row=1, column=2, sticky='WNS')
        self.listbox = tk.Listbox(areaContainer, selectmode='EXTENDED')
        self.listbox.grid(row=1, column=0, sticky='WE', columnspan=2)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.addareabutton = ttk.Button(areaContainer, text='Add', command=self.addAreaFunc)
        self.addareabutton.grid(row=2, column=0, sticky='W')
        self.deletebutton = ttk.Button(areaContainer, text='Delete', command=self.deleteSelection)
        self.deletebutton.grid(row=2, column=1, sticky='W')

        ################# START/CANCEL ##################
        self.async_loop = asyncio.get_event_loop()
        startstopContainer = tk.Frame(self)
        startstopContainer.grid(row=3, column=0, sticky='N', columnspan=2)
        self.startButton = ttk.Button(startstopContainer, text='Start', command=lambda: self.do_tasks(self.async_loop))
        self.startButton.grid(row=1, column=0, sticky='W')
        self.stopButton = ttk.Button(startstopContainer, text='Cancel', command=self.cancel)
        self.stopButton.grid(row=1, column=1, sticky='W')




        ############  RIGHT  ###############
        cameraCheckContainer = tk.Frame(self)
        cameraCheckContainer.grid(row=0, column=2, rowspan=2, sticky='N')

        ### CAMERA PREVIEW CHECK ###
        self.checkVar = tk.IntVar()
        self.checkbutton = tk.Checkbutton(cameraCheckContainer, variable=self.checkVar, text='Camera Preview',
                                          command=self.checkClick)
        self.checkbutton.grid(row=0, column=0, sticky='W')

        cameraContainer = tk.Frame(cameraCheckContainer)
        cameraContainer.grid(row=1, column=0, rowspan=2, sticky='N')
        ### CAMERA PREVIEW ###
        self.cameraWindow = tk.Canvas(cameraContainer, width=640, height=480)
        self.cameraWindow.grid(row=0, column=0, columnspan=2)


        ### PROGRESS BAR ###
        self.progressBarContainer = tk.Frame(self)
        self.progressBarContainer.grid(row=4, column=0, columnspan=4)
        self.progressBar = ttk.Progressbar(self.progressBarContainer, orient='horizontal', length=1050)
        self.progressBar.grid(row=0, column=0, sticky='EW')
        self.progressBar.config(maximum=150, value=0)

        self.delayOptions = 2000
        self.delay = 18
        self.updateCameraParameters()
        self.update()
        self.makeDataTimeMethodInterfaceUpdate('')
        self.updateAreasFromOptions()
        self.makeDataFramesSetFromOptions()
        self.updateOptions()
        #self.temperatureGetter()

    def temperatureGetter(self):
        self.currentTemp = self.TempReader.readTemp(self.temperaturePort)
        try:
            for i in self.makeDataList:
                i.currentTemp = self.currentTemp

        except:
            pass

        if self.do_temp:
            self.after(1000, self.temperatureGetter)

    def _asyncio_thread(self, async_loop):
        async_loop.run_until_complete(self.makeData())

    def do_tasks(self, async_loop):
        """ Button-Event-Handler starting the asyncio part. """

        threading.Thread(target=self._asyncio_thread, args=(async_loop,)).start()

    def makingData(self, makeDataObj):
            makeDataObj.camera = self.camera
            if self.variable4.get() == 'Count of Photos':
                makeDataObj.makingData(countOfPhoto=int(self.makeDataTimeCountOfPhotosSpinboxVar.get()),
                                    countOfFramesToAverage=int(self.makeDataFramesSpinboxVar.get()))

            if self.variable4.get() == 'Count of Time':
                makeDataObj.makingData(timeToExecute=[int(self.makeDataTimeCountOfTimeHoursSpinboxVar.get()),
                                                   int(self.makeDataTimeCountOfTimeMinutesSpinboxVar.get()),
                                                   int(self.makeDataTimeCountOfTimeSecondsSpinboxVar.get())],
                                    countOfFramesToAverage=int(self.makeDataFramesSpinboxVar.get()))


    async def makeData(self):
        #self.progressBar.start()
        settings = Settings.getInstance()
        self.do_temp = True
        self.temperatureGetter()

        self.countOfProcess = len(settings.areasList) - 1
        threads = []
        for i in range(self.countOfProcess):
            self.makeDataList.append(MakeData(settings.areasList[i+1]))
            t = threading.Thread(target=self.makingData, args=(self.makeDataList[i],))
            threads.append(t)

        time.sleep(1)
        for i in threads:
            i.start()

        for i in threads:
            i.join()

        self.do_temp = False
        #self.progressBar.stop()

        for i in self.makeDataList:
            i.camera.release()

    def cancel(self):
        for i in self.makeDataList:
            i.do = False
        self.progressBar.stop()

    def updateMakeDataSettings(self):
        self.makeDataUpdateCountOfFrames()

        if self.variable4.get() == 'Count of Photos':
            self.makeDataTimeUpdateCountOfPhoto()

        if self.variable4.get() == 'Count of Time':
            self.makeDataTimeUpdateCountOfTimeH()
            self.makeDataTimeUpdateCountOfTimeM()
            self.makeDataTimeUpdateCountOfTimeS()

    def updateOptions(self):
        self.updateMakeDataSettings()

        self.after(self.delayOptions, self.updateOptions)

    def makeDataFramesSetFromOptions(self):
        settings = Settings.getInstance()
        if settings.countOfFrames != None:
            self.makeDataFramesSpinboxVar.set(str(settings.countOfFrames))

    def makeDataUpdateCountOfFrames(self):
        settings = Settings.getInstance()
        settings.countOfFrames = int(self.makeDataFramesSpinboxVar.get())

    def makeDataTimeUpdateCountOfPhoto(self):
        settings = Settings.getInstance()
        settings.countOfPhoto = int(self.makeDataTimeCountOfPhotosSpinboxVar.get())

    def makeDataTimeUpdateCountOfTimeH(self):
        settings = Settings.getInstance()
        settings.countOfTimeH = int(self.makeDataTimeCountOfTimeHoursSpinboxVar.get())

    def makeDataTimeUpdateCountOfTimeM(self):
        settings = Settings.getInstance()
        settings.countOfTimeM = int(self.makeDataTimeCountOfTimeMinutesSpinboxVar.get())

    def makeDataTimeUpdateCountOfTimeS(self):
        settings = Settings.getInstance()
        settings.countOfTimeS = int(self.makeDataTimeCountOfTimeSecondsSpinboxVar.get())

    def makeDataTimeSetFromOptions(self):
        settings = Settings.getInstance()

        if self.variable4.get() == 'Count of Photos':
            if settings.countOfPhoto != None:
                self.makeDataTimeCountOfPhotosSpinboxVar.set(str(settings.countOfPhoto))

        if self.variable4.get() == 'Count of Time':
            if settings.countOfTimeH != None:
                self.makeDataTimeCountOfTimeHoursSpinboxVar.set(str(settings.countOfTimeH))
            if settings.countOfTimeM != None:
                self.makeDataTimeCountOfTimeMinutesSpinboxVar.set(str(settings.countOfTimeM))
            if settings.countOfTimeS != None:
                self.makeDataTimeCountOfTimeSecondsSpinboxVar.set(str(settings.countOfTimeS))

    def makeDataTimeMethodInterfaceUpdate(self,option):
        if self.variable4.get() == 'Count of Photos':
            try:
                self.makeDataTimeCountOfTimeContainer.grid_forget()
            except:
                None

            self.makeDataTimeCountOfPhotosContainer = tk.Frame(self.makeDataContainer)
            self.makeDataTimeCountOfPhotosContainer.grid(row=1, column=2)
            self.makeDataTimeCountOfPhotosSpinboxVar = tk.StringVar(self.makeDataTimeCountOfPhotosContainer)
            self.makeDataTimeSetFromOptions()
            self.makeDataTimeCountOfPhotosSpinbox = tk.Spinbox(self.makeDataTimeCountOfPhotosContainer, from_=0,
                                                               to=10000,
                                                               textvariable=self.makeDataTimeCountOfPhotosSpinboxVar,
                                                               width=21, command=self.makeDataTimeUpdateCountOfPhoto)
            self.makeDataTimeCountOfPhotosSpinbox.grid(row=0, column=0)

        if self.variable4.get() == 'Count of Time':
            try:
                self.makeDataTimeCountOfPhotosContainer.grid_forget()
            except:
                None

            self.makeDataTimeCountOfTimeContainer = tk.Frame(self.makeDataContainer)
            self.makeDataTimeCountOfTimeContainer.grid(row=1, column=2)
            self.makeDataTimeCountOfTimeHoursSpinboxVar = tk.StringVar(self.makeDataTimeCountOfTimeContainer)
            self.makeDataTimeCountOfTimeMinutesSpinboxVar = tk.StringVar(self.makeDataTimeCountOfTimeContainer)
            self.makeDataTimeCountOfTimeSecondsSpinboxVar = tk.StringVar(self.makeDataTimeCountOfTimeContainer)
            self.makeDataTimeSetFromOptions()
            self.makeDataTimeCountOfTimeHoursLabel = ttk.Label(self.makeDataTimeCountOfTimeContainer, text='h')
            self.makeDataTimeCountOfTimeHoursLabel.grid(row=0, column=1)
            self.makeDataTimeCountOfTimeHoursSpinbox = tk.Spinbox(self.makeDataTimeCountOfTimeContainer, from_=0, to=12,
                                                                  textvariable=self.makeDataTimeCountOfTimeHoursSpinboxVar,
                                                                  width=5, command=self.makeDataTimeUpdateCountOfTimeH)
            self.makeDataTimeCountOfTimeHoursSpinbox.grid(row=0, column=0)
            self.makeDataTimeCountOfTimeMinutesLabel = ttk.Label(self.makeDataTimeCountOfTimeContainer, text='m')
            self.makeDataTimeCountOfTimeMinutesLabel.grid(row=0, column=3)
            self.makeDataTimeCountOfTimeMinutesSpinbox = tk.Spinbox(self.makeDataTimeCountOfTimeContainer, from_=0,
                                                                    to=59, textvariable=self.makeDataTimeCountOfTimeMinutesSpinboxVar,
                                                                    width=5, command=self.makeDataTimeUpdateCountOfTimeM)
            self.makeDataTimeCountOfTimeMinutesSpinbox.grid(row=0, column=2)
            self.makeDataTimeCountOfTimeSecondsLabel = tk.Label(self.makeDataTimeCountOfTimeContainer, text='s')
            self.makeDataTimeCountOfTimeSecondsLabel.grid(row=0, column=5)
            self.makeDataTimeCountOfTimeSecondsSpinbox = tk.Spinbox(self.makeDataTimeCountOfTimeContainer, from_=0, to=59,
                                                                    textvariable=self.makeDataTimeCountOfTimeSecondsSpinboxVar,
                                                                    width=5, command=self.makeDataTimeUpdateCountOfTimeS)
            self.makeDataTimeCountOfTimeSecondsSpinbox.grid(row=0, column=4)

    def addAreaFunc(self):
        start = time.time()
        while int(time.time() - start) < 2:
            ret, frame = self.camera.getFrame()
        cv2.imwrite('configure.png', frame)

        mouseCropper = MouseCropper()
        mouseCropper.configure('configure.png')
        self.left = mouseCropper.left
        self.upper = mouseCropper.upper
        self.right = mouseCropper.right
        self.lower = mouseCropper.lower
        os.remove('configure.png')

        self.listbox.insert('end','{}, {}, {}, {}'.format(self.left, self.upper, self.right, self.lower))
        self.updateSettings()

    def updateSettings(self):
        settings = Settings.getInstance()
        settings.left = self.left
        settings.upper = self.upper
        settings.right = self.right
        settings.lower = self.lower

        if (self.left, self.upper, self.right, self.lower) not in settings.areasList:
            settings.areasList.append((self.left, self.upper, self.right, self.lower))

        settings.countOfAreas = len(settings.areasList)


    def updateAreasFromOptions(self):
        settings = Settings.getInstance()
        for i in range(1,len(settings.areasList)):
            self.listbox.insert('end', '{}, {}, {}, {}'.format(settings.areasList[i][0], settings.areasList[i][1],
                                                               settings.areasList[i][2], settings.areasList[i][3]))


    def updateCameraParameters(self):
        # self.updateSettings()
        settings = Settings.getInstance()
        self.camera.setProperty(3, settings.cameraWidth)
        self.camera.setProperty(4, settings.cameraHeight)
        self.camera.setProperty(10, settings.cameraBrightness)
        self.camera.setProperty(11, settings.cameraContrast)
        self.camera.setProperty(12, settings.cameraSaturation)
        self.camera.setProperty(14, settings.cameraGain)
        #self.camera.setProperty(17, settings.cameraWhiteBalance)

    def checkClick(self):
        if self.checkVar.get() == 0:
            self.checkVar.set(1)
        else:
            self.checkVar.set(0)

    def update(self):
        settings = Settings.getInstance()
        if self.checkVar.get():
            ret, frame = self.camera.getFrame()
            if ret:
                for i in range(len(settings.areasList)):
                    try:
                        cv2.rectangle(frame,
                                      (settings.areasList[i][0], settings.areasList[i][1]),
                                      (settings.areasList[i][2], settings.areasList[i][3]),
                                      (0, 255, 0), 1)
                    except:
                        pass
                self.img = ImageTk.PhotoImage(master=self.cameraWindow, image=Image.fromarray(frame).resize((640, 480)))
                self.cameraWindow.create_image(0, 0, image=self.img, anchor='nw')

        if self.checkVar.get() == 0:
            self.cameraWindow.delete("all")

        self.after(self.delay, self.update)


    def deleteSelection(self):
        items = self.listbox.curselection()
        itemToDel = self.listbox.get(self.listbox.curselection())
        itemToDel = tuple(map(int,itemToDel.replace(" ", "").split(',')))

        pos = 0
        for i in items:
            idx = int(i) - pos
            self.listbox.delete(idx, idx)
            pos = pos + 1

        settings = Settings.getInstance()
        try:
            settings.areasList.remove(itemToDel)
        except:
            None
