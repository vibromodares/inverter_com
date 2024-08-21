from time import time_ns
from typing import Union

import serial

from MainCode import logging_system
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
            logging_system.insert(0, "start serial com inverter " + self.serial.ser.port)
            flag = self.serial.open()

            logging_system.insert(0, "start serial com inverter after " + self.serial.ser.port,
                                  description="connect flag : " + str(flag))
            if flag:
                self.connect_flag = True
                return True
            self.connect_flag = False
            return False
        except serial.SerialException as e:
            logging_system.insert(2, "start serial com inverter serial except" + self.serial.ser.port, error=str(e))
            self.connect_flag = False
            return False
        except Exception as e:
            logging_system.insert(2, "start serial com inverter except" + self.serial.ser.port, error=str(e))
            self.connect_flag = False
            return False

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
        logging_system.insert(0, "read serial inverter ", send_address=address)
        byte = self.code_data(address)

        self.serial.ser.write(byte)
        # bstr = ''
        sstr = ''

        flag = False
        start_time = time_ns()

        while True:
            mHex = self.serial.ser.read()

            if sstr == '':
                if mHex not in [bytes(self.normal_response_char, 'utf-8'), bytes(self.bad_response_char, 'utf-8')]:
                    print("khar miad inja123")
                    print("mHex = " + str(mHex))
                    logging_system.insert(2, "read serial check NRC BRC", send_address=address,
                                          description="mHex = " + str(mHex) + " sstr = " + sstr,
                                          error="start with bad char")
                    break

            if len(mHex) != 0:
                flag = True

                try:
                    sstr += mHex.decode("utf-8")
                except Exception as e:
                    print("inverter model read serial decode to utf-8 ", e, "sstr = ", sstr, "mHex = ", mHex)
                    logging_system.insert(2, "inverter model read serial decode to utf-8 ",
                                          description="sstr = " + sstr, error=str(e))

            if mHex == bytes(self.end_char, 'utf-8'):
                break

            if len(mHex) == 0 and time_ns() - start_time > self.serial.read_timeout * 10 ** 9:
                break

            if time_ns() - start_time > self.serial.read_timeout * 2 * 10 ** 9:
                break

            if len(mHex) == 0 and flag:
                break
        # print(sstr)

        # TODO:age 6 ta bod yani errore v error handle konim
        # TODO:bayad vase tak tak ina handle bezarim k age errori dadi befahmim
        logging_system.insert(0, "read serial inverter ", send_address=address, receive_address=sstr)
        response_data, response_flag = self.decode_data(sstr, address)
        return response_data, response_flag
        # id, RW, data, total = self.extract_data(response_data)
        # id, RW, address_data, total, length = self.extract_address(address)
        #
        # self.convert_response_data('0x' + address_data, '0x' + data)

        # return self.convert_response_data('0x' + address_data, '0x' + data)

    def decode_data(self, data: str, address: str) -> tuple[str, bool]:
        if self.normal_response_char in data:
            flag = True
        elif self.bad_response_char in data:
            flag = False
        else:
            print('inverter model decode', data, address)
            flag = False
            logging_system.insert(2, 'inverter model decode', send_address=address, receive_address=data)
            # raise  # TODO:bayad raise ro doros konam k y error doros bede

        data = (data.replace(self.start_char, '').replace(self.end_char, '').
                replace(self.normal_response_char, '').replace(self.bad_response_char, ''))
        return data, flag

    def test_com(self):
        if self.serial.ser.port == '':
            logging_system.insert(2, "test com ", error="serial com not set")
            self.connect_flag = False
            return False

        if not self.connect_flag:
            return False
        else:
            try:
                # TODO:rah eftezah cherti baraye check kardam com darim
                self.readSerial('01R00001A4')
                return True
            except Exception as e:
                logging_system.insert(2, "test com try open com", error=str(e))
                print("test com try open com", str(e))
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
