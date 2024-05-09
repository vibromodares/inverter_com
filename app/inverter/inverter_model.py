from app.serial_com.serial_com_model import SerialModel


class InverterBaseModel:
    def __init__(self):
        self.serial = SerialModel('COM11')

    def set_serial_com(self, com):
        self.serial.ser.port = com

    def start(self):
        self.serial.open()
