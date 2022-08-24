import numpy as np
from scipy.fft import fft, fftfreq
import sys
import glob
import serial
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import json

result = {
    "Sequence_number" : [],
    "AcX":[],
    "AcY":[],
    "AcZ":[],
    "GyX":[],
    "GyY":[],
    "GyZ":[],
}

class Arm:

    def __init__(self,port):
        self.results = {}
        self.line = None
        self.port = port
        self.results = {
            "Sequence_number" : [],
            "AcX":[],
            "AcY":[],
            "AcZ":[],
            "GyX":[],
            "GyY":[],
            "GyZ":[],
                }
        self.open_line()
    def open_line(self):
        self.line = serial.Serial(self.port,57600)
    def read_data(self):



        while True:
                serial_line = self.line.readline().decode("utf-8")
                x = 0
                first_char = serial_line[0]
                if first_char == ">":
                    #mpu status
                    serial_line = serial_line[1:-2]
                    x = serial_line.find(">")
                    serial_line = serial_line.replace(">","")

                    data = serial_line.split(",")

                    data = [int(i,16) for i in data]

                    self.results["Sequence_number"].append(data[0])
                    self.results["AcX"].append(data[1])
                    self.results["AcY"].append( data[2])
                    self.results["AcZ"].append(data[3])
                    self.results["GyX"].append(data[4])
                    self.results["GyY"].append(data[5])
                    self.results["GyZ"].append(data[6])
                if(x != -1):
                    break



def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    N = 1500
    x = serial_ports()
    arm = Arm(x[0])
    for i in range(20):
        for i in range(N):
            arm.read_data()
        data = arm.results["AcY"][-N:]
        w = savgol_filter(data, 101, 2)
        plt.plot(arm.results["Sequence_number"][-N:],w)
        #plt.show()
    with open('json_data_medium.json', 'w') as outfile:
        json.dump(arm.results, outfile)
