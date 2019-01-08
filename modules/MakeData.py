import cv2
import time
import datetime
import os
import numpy as np
from PIL import Image
from modules.Settings import Settings
from threading import Lock

lock = Lock()

class MakeData():
    def __init__(self,area):
        self.left = area[0]
        self.upper = area[1]
        self.right = area[2]
        self.lower = area[3]
        self.do = True
        self.currentTemp = 0

    def createDirectoryForData(self):
        lock.acquire()
        currentDate = datetime.date.today()
        currentPath = os.getcwd()
        countOfCurrentData = 0
        folderName = "data-{}".format(str(currentDate))
        directoryPath = currentPath + "/DATA/" + folderName

        if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)

        else:
            while (True):
                if os.path.exists(directoryPath):
                    if ("_" in directoryPath) == True:
                        countOfCurrentData += 1
                        directoryPath = directoryPath[:directoryPath.find("_")] + "_{}".format(str(countOfCurrentData))

                    else:
                        directoryPath += "_{}".format(countOfCurrentData)

                else:
                    os.makedirs(directoryPath)
                    break

        print("Folder {} was created in directory : {}".format(folderName, directoryPath))
        lock.release()
        return directoryPath

    def convertListToSeconds(self,listOfTimeValuesHMS):
        countOfSeconds = listOfTimeValuesHMS[0] * 3600 + listOfTimeValuesHMS[1] * 60 + listOfTimeValuesHMS[2]
        return countOfSeconds

    def makingData(self, countOfPhoto=None, timeToExecute=None, countOfFramesToAverage=None, *args, **kwargs):
        try:
            settings = Settings.getInstance()


            # time count to execute by program
            if timeToExecute != None:
                if type(timeToExecute) == list:
                    timeToExecute = self.convertListToSeconds(timeToExecute)
                else:
                    timeToExecute = timeToExecute


            # camera
            #self.camera = cv2.VideoCapture(settings.cameraNumber)
            cameraWidth = int(self.camera.getProperty(3))
            cameraHeight = int(self.camera.getProperty(4))

            # array shape
            averagedArray = np.zeros((cameraHeight, cameraWidth, 3), np.float)

            # variables
            countOfPhotoDone = 0
            countOfFramesToAverageDone = 0
            currentDate = datetime.date.today()

            # creating directory
            if not self.do:
                return

            directoryPath = self.createDirectoryForData()

            # creating log.txt
            logFile = open(directoryPath + '/' + 'log.txt', 'w')
            dataTime = time.time()

            if (countOfPhoto and countOfFramesToAverage) != None:

                while (self.do):
                    ret, frame = self.camera.getFrame()
                    arrayFromFrame = np.array(frame, dtype=np.float)
                    averagedArray = np.add(averagedArray, arrayFromFrame, casting='unsafe')
                    countOfFramesToAverageDone += 1

                    if countOfFramesToAverageDone >= countOfFramesToAverage:
                        averagedArray = np.divide(averagedArray, countOfFramesToAverage, casting='unsafe')
                        photoToSave = np.array(np.round(averagedArray), dtype=np.uint8)
                        imageNameFormat = "\image{}{}{}{}{}".format(" ", str(currentDate), "_", str(countOfPhotoDone),
                                                                    ".png")
                        fileNameAndDirectory = directoryPath + imageNameFormat
                        cv2.imwrite(fileNameAndDirectory, photoToSave)
                        im = Image.open(fileNameAndDirectory)
                        im = im.crop((self.left, self.upper, self.right, self.lower))
                        im.save(fileNameAndDirectory)
                        logFile.write('{} {} {}\n'.format(imageNameFormat[1:], str(self.currentTemp),
                                                          time.time()))
                        averagedArray = np.zeros((cameraHeight, cameraWidth, 3), np.float)
                        countOfPhotoDone += 1
                        countOfFramesToAverageDone = 0
                        continue

                    if countOfPhotoDone >= countOfPhoto:
                        break

            elif (timeToExecute and countOfFramesToAverage) != None:

                startingProgramTime = time.time()

                while (self.do):

                    ProgramTimePast = time.time() - startingProgramTime
                    ret, frame = self.camera.getFrame()
                    arrayFromFrame = np.array(frame, dtype=np.float)
                    averagedArray = np.add(averagedArray, arrayFromFrame, casting='unsafe')
                    countOfFramesToAverageDone += 1

                    if countOfFramesToAverageDone >= countOfFramesToAverage:
                        averagedArray = np.divide(averagedArray, countOfFramesToAverage, casting='unsafe')
                        photoToSave = np.array(np.round(averagedArray), dtype=np.uint8)
                        imageNameFormat = "\image{}{}{}{}{}".format(" ", str(currentDate), "_", str(countOfPhotoDone),
                                                                    ".png")
                        fileNameAndDirectory = directoryPath + imageNameFormat
                        cv2.imwrite(fileNameAndDirectory, photoToSave)
                        logFile.write('{} {} {}\n'.format(imageNameFormat[1:], str(self.currentTemp),
                                                          time.time()))
                        im = Image.open(fileNameAndDirectory)
                        im = im.crop((self.left, self.upper, self.right, self.lower))
                        im.save(fileNameAndDirectory)
                        averagedArray = np.zeros((cameraHeight, cameraWidth, 3), np.float)
                        countOfPhotoDone += 1
                        countOfFramesToAverageDone = 0
                        continue

                    if int(ProgramTimePast) >= timeToExecute:
                        break

            logFile.close()
            #self.camera.release()
            print("Making data ends successfully, made {} frames".format(countOfPhotoDone))
        except Exception as e:
            print(e)
        return


