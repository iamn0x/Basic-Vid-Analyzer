import cv2

class Camera():
    def __init__(self, deviceNumber):
        self.camera = cv2.VideoCapture(deviceNumber)

    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()

    def release(self):
        self.camera.release()

    def getProperty(self, number):
        '''
        3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
        4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
        10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
        11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
        12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
        14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
        17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
        '''
        return self.camera.get(number)

    def setProperty(self, propId, val):
        '''
        3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
        4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
        10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
        11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
        12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
        14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
        17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
        '''
        return self.camera.set(propId, val)


    def getFrame(self):
        ret, self.frame = self.camera.read()
        return ret,self.frame

    def testIfExists(self):
            if self.camera is None or not self.camera.isOpened():
                return False
            return True
