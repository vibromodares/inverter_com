from time import time_ns
from typing import Union

import serial

from app.serial_com.serial_com_model import SerialModel


class InverterBaseModel:
    start_char = ENQ = chr(5)
    end_char = EOT = chr(4)
    normal_response_char = ACK = chr(6)
    bad_response_char = NAK = chr(21)
    connect_flag: bool = False

    def __init__(self):
        self.serial = SerialModel()

    def set_serial_com(self, com) -> None:
        self.serial.ser.port = com

    def start_com(self) -> bool:
        try:
            flag = self.serial.open()
            if flag:
                self.connect_flag = True
                return True
            self.connect_flag = False
            return False
        except serial.SerialException as e:
            self.connect_flag = False
            return False
        except:
            self.connect_flag = False
            return False
        self.connect_flag = True
        return True

    def stop_com(self) -> bool:
        try:
            flag = self.serial.close()
            if flag:
                self.connect_flag = False
                return True
            return False
        except serial.SerialException as e:
            print(e)
            return False
        except:
            return False

    def code_data(self, data) -> str:
        return 'should imp'

    def readSerial(self, address: str):
        # TODO:in bayad doros she bug ziad dare aval inke bayad time out dashte bashe baadam bayad yekisho tasmim begirim bezarim
        byte = self.code_data(address)

        self.serial.ser.write(byte)
        # bstr = ''
        sstr = ''

        flag = False
        start_time = time_ns()

        while True:
            mHex = self.serial.ser.read()

            if len(mHex) != 0:
                flag = True
                # bstr += binascii.hexlify(bytearray(mHex)).decode("utf-8")
                # bstr += " "
                sstr += mHex.decode("utf-8")

            if len(mHex) == 0 and time_ns() - start_time > self.serial.read_timeout * 10 ^ 9:
                break

            # if time_ns() - start_time > self.serial.read_timeout*2 * 10 ^ 9:
            #     break

            if len(mHex) == 0 and flag:
                break

        # TODO:bayad vase tak tak ina handle bezarim k age errori dadi befahmim

        response_data, response_flag = self.decode_data(sstr)
        return response_data, response_flag
        # id, RW, data, total = self.extract_data(response_data)
        # id, RW, address_data, total, length = self.extract_address(address)
        #
        # self.convert_response_data('0x' + address_data, '0x' + data)

        # return self.convert_response_data('0x' + address_data, '0x' + data)

    def decode_data(self, data: str) -> tuple[str, bool]:
        if self.normal_response_char in data:
            flag = True
        elif self.bad_response_char in data:
            flag = False
        else:
            print('inverte model decode', data)
            flag = False
            # raise  # TODO:bayad raise ro doros konam k y error doros bede

        data = (data.replace(self.start_char, '').replace(self.end_char, '').
                replace(self.normal_response_char, '').replace(self.bad_response_char, ''))
        return data, flag

    def test_com(self):
        if self.serial.ser.port == '':
            self.connect_flag = False
            return False

        if not self.connect_flag:
            return False
        else:
            try:
                self.readSerial('01R00001A4')
                return True
            except:
                self.connect_flag = False
                return False

    def convert_str_to_ascii(self, char: Union[str, list['str']]) -> list[str]:
        list_return = []
        for char1 in char:
            for char2 in char1:
                list_return.append(hex(ord(char2)).split('x')[-1])
        return list_return

    def add_hex(self, hex_nums: list[str]):
        out = 0
        for hex_num in hex_nums:
            out += int(hex_num, 16)

        return hex(out).split('x')[-1]

    def get_num_4_sum(self, hex_in: str) -> str:
        return hex_in[-2:].upper()
