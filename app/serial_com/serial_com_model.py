import serial
import binascii
from time import sleep, time, time_ns


start_char = ENQ = chr(5)
end_char = EOT = chr(4)
normal_response_char = ACK = chr(6)
bad_response_char = NAK = chr(21)


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
        self.read_timeout = 1
        self.start_char = start_char  # TODO: in bayad bere dakhele plc k azesh ino seda mizane
        self.end_char = end_char  # TODO: in bayad bere dakhele plc k azesh ino seda mizane
        # self.open()  # TODO: in bayad bere dakhele plc k azesh ino seda mizane

    def open(self) -> None:
        self.ser.open()

    def readSerial(self, address: str):
        # TODO:in bayad doros she bug ziad dare aval inke bayad time out dashte bashe baadam bayad yekisho tasmim begirim bezarim
        byte = self.code_data(address)

        self.ser.write(byte)
        # bstr = ''
        sstr = ''

        flag = False
        start_time = time_ns()

        while True:
            mHex = self.ser.read()

            if len(mHex) != 0:
                flag = True
                # bstr += binascii.hexlify(bytearray(mHex)).decode("utf-8")
                # bstr += " "
                sstr += mHex.decode("utf-8")

            if len(mHex) == 0 and time_ns() - start_time > self.read_timeout * 10 ^ 9:
                break

            if len(mHex) == 0 and flag:
                break

        # TODO:bayad vase tak tak ina handle bezarim k age errori dadi befahmim

        response_data, response_flag = self.decode_data(sstr)
        id, RW, data, total = self.extract_data(response_data)
        id, RW, address_data, total, length = self.extract_address(address)

        self.convert_response_data('0x' + address_data, '0x' + data)

        return self.convert_response_data('0x' + address_data, '0x' + data)

    def code_data(self, data):
        # TODO:inam fekr konam bayad bere az plc k azesh mikhonim biad
        return bytes(self.start_char + data + self.end_char, 'utf-8')

    def decode_data(self, data: str) -> tuple[str, bool]:
        if normal_response_char in data:
            flag = True
        elif bad_response_char in data:
            flag = False
        else:
            raise  # TODO:bayad raise ro doros konam k y error doros bede

        data = data.replace(start_char, '').replace(end_char, '').replace(normal_response_char, '').replace(
            bad_response_char, '')
        return data, flag

    def convert_response_data(self, address: str, byte: str) -> str:
        pass
        # return db.get_response(address, byte)['discreption']

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
