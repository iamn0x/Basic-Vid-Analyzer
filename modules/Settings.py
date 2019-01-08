import jsonpickle

class Settings():
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Settings.__instance == None:
            Settings()
        return Settings.__instance

    def __init__(self):
        if Settings.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Settings.__instance = self

        ### camera options ###
        self.cameraNumber = None
        self.cameraWidth = None
        self.cameraHeight = None
        self.cameraBrightness = None
        self.cameraContrast = None
        self.cameraSaturation = None
        self.cameraGain = None
        self.cameraWhiteBalance = None

        ### make data options ###
        # making data time methods #
        self.countOfPhoto = None

        self.countOfTimeH = None
        self.countOfTimeM = None
        self.countOfTimeS = None

        # making one photo methods #
        self.countOfFrames = None
        #self.countOfTimeBetweenPhotos = None

        ### area options ###
        self.left = None
        self.upper = None
        self.right = None
        self.lower = None
        self.areasList = []
        self.countOfAreas = None

        ### port name ###
        self.portName = None

    def setCamProperties(self, cameraObj):
        cameraObj.setProperty(3, self.cameraWidth)
        cameraObj.setProperty(4, self.cameraHeight)
        cameraObj.setProperty(10, self.cameraBrightness)
        cameraObj.setProperty(11, self.cameraContrast)
        cameraObj.setProperty(12, self.cameraSaturation)
        cameraObj.setProperty(14, self.cameraGain)
        return cameraObj

    @staticmethod
    def settingsDict():
        return jsonpickle.encode(Settings.__instance)

    @staticmethod
    def saveJSON(pathToFile):
        file = open(pathToFile, "w+")
        file.write(Settings.settingsDict())
        file.close()

    @staticmethod
    def loadJSON(fileName):
        Settings.__instance = jsonpickle.decode(open(fileName).read())


