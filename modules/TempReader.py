import serial
import time
#import random

class TempReader():
    def testPort(self, port):
        try:
            serialPort = serial.Serial()
            serialPort.port = port
            serialPort.baudrate = 9600
            serialPort.rtscts = True
            serialPort.timeout = 2
            serialPort.open()
            if serialPort.isOpen():
                serialPort.close()
                return True
        except:
            return False


    def readTemp(self, port):
        #return random.randint(1, 38)

        serialPort = serial.Serial()
        serialPort.port = port
        serialPort.baudrate = 9600
        serialPort.rtscts = True
        serialPort.timeout = 2
        temperature = -1000
 
        try:
            serialPort.open()
        except:
            print('Serial Port opening problems')

        if serialPort.isOpen():
            ans=b''
            while len(ans) == 0:
                serialPort.write(b'?')
                time.sleep(0.1)
                ans = serialPort.readline()
            try:
                temperature = int(ans)
            except:
                temperature = -1000

        serialPort.close()
        del serialPort
        return temperature
