import serial
import binascii
from time import sleep


def initSerial(serial_in):
    serial_in.baudrate = 9600
    serial_in.port = 'COM12'
    serial_in.stopbits = serial.STOPBITS_ONE
    serial_in.bytesize = 8
    serial_in.parity = serial.PARITY_NONE
    serial_in.rtscts = 0
    serial_in.timeout = 1


def readSerial(data):
    ser = serial.Serial()
    initSerial(ser)
    ser.open()

    ENQ = chr(5)
    EOT = chr(4)

    byte = bytes(ENQ + data + EOT, 'utf-8')
    ser.write(byte)

    bstr = ''
    sstr = ''
    flag = False
    while True:
        mHex = ser.read()
        if len(mHex) != 0:
            flag = True
            bstr += binascii.hexlify(bytearray(mHex)).decode("utf-8")
            bstr += " "
            sstr += mHex.decode("utf-8")

        sleep(0.1)
        if len(mHex) == 0 and flag:
            break
    return bstr, sstr


if __name__ == "__main__":
    print(readSerial('01R03001A7'))
    print(readSerial('01R03011A8'))
    print(readSerial('01W0380101F48F'))
    print(readSerial('01W03821000177'))

    sleep(5)
    print(readSerial('01R030D1A8'))
    sleep(10)
    print(readSerial('01W03821000076'))
