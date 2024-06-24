import os
import sys
from datetime import time
from time import sleep

from PyQt5.QtWidgets import QApplication


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


path = resource_path("")
path = path.replace(path[2], "/")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    from core.app_provider.admin.main import Main

    main = Main()
    sys.exit(app.exec_())

    # start_time = time()
    # print(serial.readSerial('01R00001A4'))
    # print(time() - start_time)
    # start_time = time()
    # print(serial.readSerial('01R03001A7'))
    # print(time() - start_time)
    # print(serial.readSerial('01R03011A8'))
    # print(serial.readSerial('01W0380101F48F'))
    # print(serial.readSerial('01W03821000177'))

    # import serial
    # import binascii
    # from time import sleep
    #
    #
    # def initSerial(serial_in):
    #     serial_in.baudrate = 9600
    #     serial_in.port = 'COM12'
    #     serial_in.stopbits = serial.STOPBITS_ONE
    #     serial_in.bytesize = 8
    #     serial_in.parity = serial.PARITY_NONE
    #     serial_in.rtscts = 0
    #     serial_in.timeout = 1
    #
    #
    # def readSerial(data):
    #     ser = serial.Serial()
    #     initSerial(ser)
    #     ser.open()
    #
    #     ENQ = chr(5)
    #     EOT = chr(4)
    #
    #     byte = bytes(ENQ + data + EOT, 'utf-8')
    #     ser.write(byte)
    #
    #     bstr = ''
    #     sstr = ''
    #     flag = False
    #     while True:
    #         mHex = ser.read()
    #         if len(mHex) != 0:
    #             flag = True
    #             bstr += binascii.hexlify(bytearray(mHex)).decode("utf-8")
    #             bstr += " "
    #             sstr += mHex.decode("utf-8")
    #
    #         sleep(0.1)
    #         if len(mHex) == 0 and flag:
    #             break
    #     return bstr, sstr
    #
    #
    # if __name__ == "__main__":
    #     print(readSerial('01R03001A7'))
    #     print(readSerial('01R03011A8'))
    #     print(readSerial('01W0380101F48F'))
    #     print(readSerial('01W03821000177'))
    #
    #     sleep(5)
    #     print(readSerial('01R030D1A8'))
    #     sleep(10)
    #     print(readSerial('01W03821000076'))
    #
    # sleep(2)
    # print(serial.readSerial('01R030D1A8'))
    # sleep(2)
    # print(serial.readSerial('01W03821000076'))
