import os
import time
import datetime
import cv2
import numpy as np
from threading import Lock
from PIL import Image
from modules.Settings import Settings
from modules.TempReader import TempReader

lock = Lock()

class RealTime():
    def __init__(self, area):
        self.area = area
        self.frames = None
        self.count = 0
        self.do = True

        self.avR = []
        self.avG = []
        self.avB = []
        self.tempList = []
        self.timeList = []

        self.currentTemp = 0


    def createDirectoryForData(self):
        lock.acquire()
        currentDate = datetime.date.today()
        currentPath = os.getcwd()
        countOfCurrentData = 0
        folderName = "RTdata-{}".format(str(currentDate))
        self.directoryPath = os.path.join(currentPath ,"DATA",folderName)

        if not os.path.exists(self.directoryPath):
            os.makedirs(self.directoryPath)
        else:
            while(True):
                if os.path.exists(self.directoryPath):
                    if ("_" in self.directoryPath) == True:
                        countOfCurrentData += 1
                        self.directoryPath = self.directoryPath[:self.directoryPath.find("_")] + "_{}".format(str(countOfCurrentData))

                    else:
                        self.directoryPath += "_{}".format(countOfCurrentData)

                else:
                    os.makedirs(self.directoryPath)
                    break
        print("Folder {} was created in directory : {}".format(folderName, self.directoryPath))
        lock.release()
        return self.directoryPath

    def currentDataTime(self):
        # return time.strftime("%H:%M:%S", time.gmtime(time.time() - self.startTime))
        return time.time()

    def timePast(self):
        return time.time() - self.startTime

    def createLogFile(self):
        self.logFile = open(self.directoryPath + '/' + 'log.txt', 'w')

    def createAnalysisFile(self):
        self.analysisFile = open(self.directoryPath + '/' + 'analysis.txt', 'w')

    def logFileWrite(self):
        self.logFile.write('{} {} {}\n'.format(self.imageNameFormat[1:], str(self.currentTemp), self.currentDataTime()))

    def analysisFileWrite(self):
        self.analysisFile.write('{}: t: {}, T: {}, Rav: {}, Gav: {}, Bav: {}\n\n'
                           .format(self.imageNameFormat[1:len(self.imageNameFormat)],
                                   self.currentTime,
                                   self.currentTemp,
                                   self.redPixAvg,
                                   self.greenPixAvg,
                                   self.bluePixAvg))

    def convertTimeToSeconds(self, time):
        if type(time) == list:
            time = time[0] * 3600 + time[1] * 60 + time[2]
        return time

    def makePhoto(self):
        cameraWidth = int(self.camera.getProperty(3))
        cameraHeight = int(self.camera.getProperty(4))
        averagedArray = np.zeros((cameraHeight, cameraWidth, 3), np.float)
        countOfFramesDone = 0
        currentDate = datetime.date.today()

        while countOfFramesDone < self.frames:
            ret, frame = self.camera.getFrame()
            arrayFromFrame = np.array(frame, dtype=np.float)
            averagedArray = np.add(averagedArray, arrayFromFrame, casting='unsafe')
            countOfFramesDone += 1

        self.currentTime = self.currentDataTime()
        self.tempList.append(self.currentTemp)
        self.timeList.append(self.currentDataTime())

        self.averagedArray_ready = np.divide(averagedArray, self.frames, casting='unsafe')
        image = np.array(np.round(self.averagedArray_ready), dtype=np.uint8)
        self.imageNameFormat = "image{}{}{}{}{}".format(" ", str(currentDate), "_", str(self.count),
                                                    ".png")
        self.count += 1
        self.fileNameAndDirectory = os.path.join(self.directoryPath,self.imageNameFormat)
        cv2.imwrite(self.fileNameAndDirectory, image)

    def cropPhoto(self):
        im = Image.open(self.fileNameAndDirectory)
        im = im.crop((self.area))
        im.save(self.fileNameAndDirectory)

    def analysePhoto(self):
        im = Image.open(self.fileNameAndDirectory)
        arrayImage = np.asarray(im)
        arrayImage = arrayImage.flat
        self.redPixAvg = sum(arrayImage[::3]) / (len(arrayImage) / 3)
        self.greenPixAvg = sum(arrayImage[1::3]) / (len(arrayImage) / 3)
        self.bluePixAvg = sum(arrayImage[2::3]) / (len(arrayImage) / 3)

        self.avR.append(self.redPixAvg)
        self.avG.append(self.greenPixAvg)
        self.avB.append(self.bluePixAvg)

    def before(self):
        ''' run this method before you use run() method. '''
        self.startTime = time.time()
        self.createDirectoryForData()
        self.createLogFile()
        self.createAnalysisFile()

    def run(self):
        ''' before you run this method make sure that you set startTime, directory, log and analysis files by before() method. '''
        self.makePhoto()
        self.cropPhoto()
        self.logFileWrite()
        self.analysePhoto()
        self.analysisFileWrite()


