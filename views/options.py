import tkinter as tk
import tkinter.simpledialog as tksd
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from modules.Camera import Camera
from modules.Settings import Settings
from modules.MouseCropper import MouseCropper
import time
import cv2
import os

class Options(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.settings = Settings.getInstance()

        ###AREA###
        self.left = None
        self.upper = None
        self.right = None
        self.lower = None

        ############  LEFT  ###############
        optionsContainer = tk.Frame(self)
        optionsContainer.grid(row=0, column=0, sticky='N', columnspan=2)

        self.label9 = ttk.Label(optionsContainer, text='Camera Options', font='Helvetica 10 bold')
        self.label9.grid(row=0, column=0, columnspan=2)

        ### DEVICE NUMBER ###
        self.label1 = ttk.Label(optionsContainer, text='Device Number: ')
        self.label1.grid(row=1, column=0)
        self.devicelist = self.getDeviceList()
        self.devicelist.insert(0, self.devicelist[0])
        self.variable1 = tk.StringVar(optionsContainer)
        self.variable1.set(self.devicelist[0])
        self.dropdownmenu1 = ttk.OptionMenu(optionsContainer, self.variable1, *self.devicelist, command=self.changeCamera)
        self.dropdownmenu1.grid(row=1, column=1, sticky ='news')

        #set camera
        self.camera = Camera(int(self.variable1.get()))

        ### RESOLUTION ###
        self.label2 = ttk.Label(optionsContainer, text='Resolution:')
        self.label2.grid(row=2, column=0)
        self.resolutionlist = ["640x480","800x600", "1280x960", "1920x1080"]
        self.resolutionlist.insert(0, self.resolutionlist[0])
        self.variable2 = tk.StringVar(optionsContainer)
        self.variable2.set(str(self.camera.getProperty(3))+"x"+str(self.camera.getProperty(4)))
        self.dropdownmenu2 = ttk.OptionMenu(optionsContainer, self.variable2, *self.resolutionlist, command=self.changeResolution)
        self.dropdownmenu2.grid(row=2, column=1, sticky ='news')

        # ### WHITE BALANCE ###
        #         # self.label3 = ttk.Label(optionsContainer, text='White Balance:')
        #         # self.label3.grid(row=3, column=0)
        #         # self.whitebalancelist = ['on','off']
        #         # self.whitebalancelist.insert(0,self.whitebalancelist[0])
        #         # self.variable3 = tk.StringVar(optionsContainer)
        #         # self.variable3.set(self.camera.getProperty(17))
        #         # self.dropdownmenu3 = ttk.OptionMenu(optionsContainer, self.variable3, *self.whitebalancelist, command=self.changeWhiteBalance)
        #         # self.dropdownmenu3.grid(row=3, column=1, sticky='news')

        ### BRIGHTNESS ###
        self.label4 = ttk.Label(optionsContainer, text='Brightness:')
        self.label4.grid(row=4, column=0)
        self.defaultBrightnessVar = tk.StringVar(optionsContainer)
        self.defaultBrightnessVar.set(self.camera.getProperty(10))
        self.spinbox1 = tk.Spinbox(optionsContainer, textvariable=self.defaultBrightnessVar, command=self.updateCameraParameters)
        self.spinbox1.grid(row=4, column=1)
        self.spinbox1.config(from_=0, to=10000, justify='right')

        ### CONTRAST ###
        self.label5 = tk.Label(optionsContainer, text='Contrast:')
        self.label5.grid(row=5, column=0)
        self.defaultContrastVar = tk.StringVar(optionsContainer)
        self.defaultContrastVar.set(self.camera.getProperty(11))
        self.spinbox2 = tk.Spinbox(optionsContainer, textvariable=self.defaultContrastVar, command=self.updateCameraParameters)
        self.spinbox2.grid(row=5, column=1)
        self.spinbox2.config(from_=0, to=10000, justify='right')

        ### SATURATION ###
        self.label6 = tk.Label(optionsContainer, text='Saturation:')
        self.label6.grid(row=6, column=0)
        self.defaultSaturationVar = tk.StringVar(optionsContainer)
        self.defaultSaturationVar.set(self.camera.getProperty(12))
        self.spinbox3 = tk.Spinbox(optionsContainer, textvariable=self.defaultSaturationVar, command=self.updateCameraParameters)
        self.spinbox3.grid(row=6, column=1)
        self.spinbox3.config(from_=0, to=10000, justify='right')

        ### GAIN ###
        self.label7 = ttk.Label(optionsContainer, text='Gain:')
        self.label7.grid(row=7, column=0)
        self.defaultGainVar = tk.StringVar(optionsContainer)
        self.defaultGainVar.set(self.camera.getProperty(14)/10000000)
        self.spinbox4 = tk.Spinbox(optionsContainer, textvariable=self.defaultGainVar, command=self.updateCameraParameters)
        self.spinbox4.grid(row=7, column=1)
        self.spinbox4.config(from_=0, to=100, justify='right')


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

        ################ MAKE DATA OPTIONS ###################

        self.makeDataContainer = tk.Frame(self)
        self.makeDataContainer.grid(row=2, column=0, sticky='N', columnspan=2)

        self.label11 = ttk.Label(self.makeDataContainer, text='Make Data Settings', font='Helvetica 10 bold')
        self.label11.grid(row=0, column=0, columnspan=3)

        self.label12 = ttk.Label(self.makeDataContainer, text='Making Data Time method: ')
        self.label12.grid(row=1, column=0)
        self.makeDataTimeList = ['Count of Photos', 'Count of Time']
        self.makeDataTimeList.insert(0, self.makeDataTimeList[0])
        self.variable4 = tk.StringVar(self.makeDataContainer)
        self.variable4.set(self.makeDataTimeList[0])
        self.dropdownmenu4 = ttk.OptionMenu(self.makeDataContainer, self.variable4, *self.makeDataTimeList, command=self.makeDataTimeMethodInterfaceUpdate)
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


        ################# LOAD/SAVE ##################
        loadsaveContainer = tk.Frame(self)
        loadsaveContainer.grid(row=3, column=0, sticky='N', columnspan=2)
        self.loadButton = ttk.Button(loadsaveContainer, text='Load Config', command=self.loadConfig)
        self.loadButton.grid(row=1, column=0, sticky='W', pady=5)
        self.saveButton = ttk.Button(loadsaveContainer, text='Save Config', command=self.saveConfig)
        self.saveButton.grid(row=1, column=1, sticky='W', pady=5)

        ############# PORT #################
        self.portName = ''
        portContainer = tk.Frame(self)
        portContainer.grid(row=4, column=0, sticky='N', columnspan=2)
        self.label12 = ttk.Label(portContainer, text='Port Settings', font='Helvetica 10 bold')
        self.label12.grid(row=0, column=0, columnspan=3)
        self.portLabel = ttk.Label(portContainer, text=str(self.settings.portName))
        self.portLabel.grid(row=1, column=1, sticky='W', pady=5)
        self.portEntry = ttk.Button(portContainer, text="Enter Port Name:", command=self.portEntryMethod)
        self.portEntry.grid(row=1, column=0, sticky='W', pady=5)

        ############  RIGHT  ###############
        cameraCheckContainer = tk.Frame(self)
        cameraCheckContainer.grid(row=0, column=2, rowspan=2, sticky='N')

        ### CAMERA PREVIEW CHECK ###
        self.checkVar = tk.IntVar()
        self.checkbutton = tk.Checkbutton(cameraCheckContainer, variable=self.checkVar, text='Camera Preview', command=self.checkClick)
        self.checkbutton.grid(row=0, column=0, sticky='W')

        cameraContainer = tk.Frame(cameraCheckContainer)
        cameraContainer.grid(row=1, column=0, rowspan=2, sticky='N')
        ### CAMERA PREVIEW ###
        self.cameraWindow = tk.Canvas(cameraContainer, width=640, height=480)
        self.cameraWindow.grid(row=0, column=0, columnspan=2)


        self.delayOptions = 2000
        self.delay = 18
        self.updateCameraParameters()
        self.update()
        self.makeDataTimeMethodInterfaceUpdate('')
        self.updateAreasFromOptions()
        self.makeDataFramesSetFromOptions()
        self.updateOptions()

    def portEntryMethod(self):
        self.settings.portName = tksd.askstring('Port name','Enter serial port',initialvalue=str( self.settings.portName))
        self.portLabel.config(text=str(self.settings.portName))

    def updateMakeDataSettings(self):
        self.makeDataUpdateCountOfFrames()

        if self.variable4.get() == 'Count of Photos':
            self.makeDataTimeUpdateCountOfPhoto()

        if self.variable4.get() == 'Count of Time':
            self.makeDataTimeUpdateCountOfTimeH()
            self.makeDataTimeUpdateCountOfTimeM()
            self.makeDataTimeUpdateCountOfTimeS()

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
            self.makeDataTimeCountOfPhotosSpinbox = tk.Spinbox(self.makeDataTimeCountOfPhotosContainer, from_=0, to=10000, textvariable=self.makeDataTimeCountOfPhotosSpinboxVar, width=21, command=self.makeDataTimeUpdateCountOfPhoto)
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
            self.makeDataTimeCountOfTimeHoursSpinbox = tk.Spinbox(self.makeDataTimeCountOfTimeContainer, from_=0, to=12, textvariable=self.makeDataTimeCountOfTimeHoursSpinboxVar, width=5, command=self.makeDataTimeUpdateCountOfTimeH)
            self.makeDataTimeCountOfTimeHoursSpinbox.grid(row=0, column=0)
            self.makeDataTimeCountOfTimeMinutesLabel = ttk.Label(self.makeDataTimeCountOfTimeContainer, text='m')
            self.makeDataTimeCountOfTimeMinutesLabel.grid(row=0, column=3)
            self.makeDataTimeCountOfTimeMinutesSpinbox = tk.Spinbox(self.makeDataTimeCountOfTimeContainer, from_=0, to=59, textvariable=self.makeDataTimeCountOfTimeMinutesSpinboxVar, width=5, command=self.makeDataTimeUpdateCountOfTimeM)
            self.makeDataTimeCountOfTimeMinutesSpinbox.grid(row=0, column=2)
            self.makeDataTimeCountOfTimeSecondsLabel = tk.Label(self.makeDataTimeCountOfTimeContainer, text='s')
            self.makeDataTimeCountOfTimeSecondsLabel.grid(row=0, column=5)
            self.makeDataTimeCountOfTimeSecondsSpinbox = tk.Spinbox(self.makeDataTimeCountOfTimeContainer, from_=0, to=59, textvariable=self.makeDataTimeCountOfTimeSecondsSpinboxVar, width=5, command=self.makeDataTimeUpdateCountOfTimeS)
            self.makeDataTimeCountOfTimeSecondsSpinbox.grid(row=0, column=4)


    def updateAreasFromOptions(self):
        settings = Settings.getInstance()
        for i in range(1,len(settings.areasList)):
            self.listbox.insert('end', '{}, {}, {}, {}'.format(settings.areasList[i][0], settings.areasList[i][1], settings.areasList[i][2], settings.areasList[i][3]))

    def changeResolution(self, something):
        self.updateCameraParameters()

    def changeWhiteBalance(self, something):
        self.updateCameraParameters()

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

        self.listbox.insert('end', '{}, {}, {}, {}'.format(self.left, self.upper, self.right, self.lower))
        self.updateSettings()


    def changeCamera(self, x):
        self.camera.__del__()
        self.camera = Camera(self.variable1.get())
        self.updateCameraParameters()

    def updateSettings(self):
        settings = Settings.getInstance()
        settings.cameraNumber = int(self.variable1.get())
        settings.cameraWidth = int(self.variable2.get().split('x')[0])
        settings.cameraHeight = int(self.variable2.get().split('x')[1])
        settings.cameraBrightness = int(self.defaultBrightnessVar.get())
        settings.cameraContrast = int(self.defaultContrastVar.get())
        settings.cameraSaturation = int(self.defaultSaturationVar.get())
        settings.cameraGain = int(self.defaultGainVar.get()) * 10000000
        # if self.variable3.get() == 'on':
        #     settings.cameraWhiteBalance = 1
        # else:
        #     settings.cameraWhiteBalance = 0

        settings.left = self.left
        settings.upper = self.upper
        settings.right = self.right
        settings.lower = self.lower

        if (self.left, self.upper, self.right, self.lower) not in settings.areasList:
            settings.areasList.append((self.left, self.upper, self.right, self.lower))

        settings.countOfAreas = len(settings.areasList)


    def updateCameraParameters(self):
        self.updateSettings()
        settings = Settings.getInstance()
        self.camera.setProperty(3, settings.cameraWidth)
        self.camera.setProperty(4, settings.cameraHeight)
        self.camera.setProperty(10, settings.cameraBrightness)
        self.camera.setProperty(11, settings.cameraContrast)
        self.camera.setProperty(12, settings.cameraSaturation)
        self.camera.setProperty(14, settings.cameraGain)
        # self.camera.setProperty(17, settings.cameraWhiteBalance)

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


    def updateOptions(self):
        self.updateCameraParameters()
        self.updateMakeDataSettings()


        self.after(self.delayOptions, self.updateOptions)


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

    def getDeviceList(self):
        list = []
        for i in range(5):
            if Camera(i).testIfExists() == True:
                list.append(i)
        return list

    def loadConfig(self):
        Settings.loadJSON(filedialog.askopenfilename())
        self.updateAreasFromOptions()
        self.makeDataFramesSetFromOptions()

    def saveConfig(self):
        self.updateSettings()
        Settings.saveJSON(filedialog.asksaveasfilename(defaultextension=".ini"))

