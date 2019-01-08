from os import listdir
from os.path import isfile, join
from PIL import Image
import numpy as np
import math

class DataAnalyzer():
    def __init__(self, directoryPath):
        self.directoryPath = directoryPath


    def getFilesList(self):
        filesList = [f for f in listdir(self.directoryPath) if isfile(join(self.directoryPath, f))]
        try:
            filesList.remove('log.txt')
        except:
            pass
        try:
            filesList.remove('analysis.txt')
        except:
            pass
        try:
            filesList.remove('Thumbs.db')
        except:
            pass

        return filesList

    def createFileTempTime(self):
        f = open(self.directoryPath + '/' + 'log.txt', 'r')
        lines = f.readlines()
        dictFileTempTime = {}

        for i in lines:
            splitted = i.rstrip().split(' ')
            name = splitted[0] + " " + splitted[1]
            val = splitted[2]
            time = splitted[3]

            if val == 'None':
                dictFileTempTime[name] = {'temp': None, 'time': time}
            else:
                dictFileTempTime[name] = {'temp': float(val), 'time': time}

        return dictFileTempTime

    def analyseData(self):
        data = {}
        dictFileTempTime = self.createFileTempTime()
        files = self.getFilesList()
        count = len(files)

        for i in files:
            im = Image.open(self.directoryPath + '/' + i)
            arrayImage = np.asarray(im)
            arrayImage = arrayImage.flat
            redPixSum = sum(arrayImage[::3]) / (len(arrayImage) / 3)
            greenPixSum = sum(arrayImage[1::3]) / (len(arrayImage) / 3)
            bluePixSum = sum(arrayImage[2::3]) / (len(arrayImage) / 3)
            data[i] = {'time': dictFileTempTime[i]['time'],
                       'temperature': dictFileTempTime[i]['temp'],
                       'red': redPixSum,
                       'green': greenPixSum,
                       'blue': bluePixSum}

        avgR = 0
        avgG = 0
        avgB = 0
        for i in files:
            avgR += data[i]['red']
            avgG += data[i]['green']
            avgB += data[i]['blue']

        avgR = avgR / count
        avgG = avgG / count
        avgB = avgB / count

        variancyR = 0
        variancyG = 0
        variancyB = 0
        for i in files:
            variancyR += (data[i]['red'] - avgR) * (data[i]['red'] - avgR)
            variancyG += (data[i]['green'] - avgG) * (data[i]['green'] - avgG)
            variancyB += (data[i]['blue'] - avgB) * (data[i]['blue'] - avgB)

        variancyR = variancyR / count
        variancyG = variancyG / count
        variancyB = variancyB / count

        stdDevR = math.sqrt(variancyR)
        stdDevG = math.sqrt(variancyG)
        stdDevB = math.sqrt(variancyB)

        self.data = data
        self.avgR = avgR
        self.avgG = avgG
        self.avgB = avgB
        self.stdDevR = stdDevR
        self.stdDevG = stdDevG
        self.stdDevB = stdDevB

        avg = [self.avgR, self.avgG, self.avgB]
        stdDev = [self.stdDevR, self.stdDevG, self.stdDevB]

        analysisFile = open(self.directoryPath + '/' + 'analysis.txt', 'w')

        for i in data:
            analysisFile.write('{}: t: {}, T: {}, Rav: {}, Gav: {}, Bav: {}\n\n'
                               .format(i,
                                       data[i]['time'],
                                       data[i]['temperature'],
                                       data[i]['red'],
                                       data[i]['green'],
                                       data[i]['blue'],))

        analysisFile.write('average of red: {}, average of green: {}, average of blue: {}\n\n'
                           .format(avg[0],
                                   avg[1],
                                   avg[2]))

        analysisFile.write('standard deviation for red: {}, standard deviation for green: {}, standard deviation for blue: {}'
                           .format(stdDev[0],
                                   stdDev[1],
                                   stdDev[2]))

        return self.data