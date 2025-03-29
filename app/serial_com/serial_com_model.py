import serial
import binascii
from time import sleep, time, time_ns
from MainCode import logging_system


class SerialModel:
    def __init__(self, port: str = '') -> None:
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = port
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.bytesize = 8
        self.ser.parity = serial.PARITY_NONE
        self.ser.rtscts = 0
        self.ser.timeout = 0.05  # momkene to baghie system haw fargh dashte bashe bayad y hodod barash peida konim
        self.read_timeout = 0.5
        # self.open()  # TODO: in bayad bere dakhele plc k azesh ino seda mizane

    def open(self) -> bool:
        if self.ser.is_open:
            logging_system.insert(2, "open serial com", description="should not come here")
            return True

        try:
            logging_system.insert(0, "trying open serial com " + str(self.ser.port))
            self.ser.open()
            return True
        except Exception as e:
            logging_system.insert(2, "error in trying open serial com " + str(self.ser.port), error=str(e))
            return False

    def close(self) -> bool:
        logging_system.insert(0, "trying closing serial com " + str(self.ser.port))
        self.ser.close()
        return True

    def extract_data(self, response_data):
        id = response_data[0:2]
        RW = response_data[2]
        data = response_data[3:7]
        total = response_data[7:]
        return id, RW, data, total

    def extract_address(self, address):
        id = address[0:2]
        RW = address[2]
        data = address[3:7]
        length = address[7]
        total = address[8:]
        return id, RW, data, length, total
