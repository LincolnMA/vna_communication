import serial
import time

class positioner:
    
    connection = None


    def __init__(self) -> None:
        pass
    def connect(self,porta,b = 9600):
        self.connection = serial.Serial(port=porta,baudrate=b)
        time.sleep(1)
        print("home achivied!")
    def small_step_foward(self):
        self.connection.write(b'd')

    def big_step_foward(self):
        self.connection.write(b'f')

    def small_step_back(self):
        self.connection.write(b's')

    def big_step_back(self):
        self.connection.write(b'a')

    def disconnect(self):
        self.connection.close()

