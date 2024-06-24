# db = DataBaseModel(file_name='device_models.json')
# db.insert_data({
#     'model_id': 1,
#     'name': 'iG5A',
#     'com_disc': 'USB-SERIAL CH340',
# })
# db.insert_data({
#     'model_id': 2,
#     'name': 'PLC',
#     'com_disc': 'USB-SERIAL CH340'
# })
from time import sleep

from app.database.api.api import get_device_by_id
from app.inverter.iG5A.iG5AModel_new import iG5AModel
from app.inverter.inverter_model import InverterBaseModel

# from app.database.model.database_model import DataBaseModel
#
# # TODO:bayad check kone data on model inverter ra dare ya na dl kone v check kone bebine aslan in model inverter to model haye ma hast ya na
#
#
# db = DataBaseModel(file_name='device_list.json')
# db.insert_data({
#     'inverter_id': 1,
#     'model_id': 1,
#     'name': 'main',
#     'com_port': 'COM11',
# })
#
# db.insert_data({
#     'inverter_id': 2,
#     'model_id': 1,
#     'name': 'test',
#     'com_port': 'COM12',
# })

# db.insert_data({
#     'address': '0x0000',
#     'byte': '0x000A',
#     'discreption': 'Ig5a'
# })
# db.insert_data({
#     'address': '0x0301',
#     'byte': '0x0019',
#     'discreption': '0.4kW'
# })
# db.insert_data({
#     'address': '0x0301',
#     'byte': '0x3200',
#     'discreption': '0.75kW'
# })
# db.insert_data({
#     'address': '0x0301',
#     'byte': '0x4015',
#     'discreption': '1.5kW'
# })
# db.insert_data({
#     'address': '0x0301',
#     'byte': '0x4022',
#     'discreption': '2.2kW'
# })

# import serial.tools.list_ports
# ports = serial.tools.list_ports.comports()
#
# for port, desc, hwid in sorted(ports):
#         print("{}: {} ".format(port, desc))


# asd = InverterBaseModel()
# asd.set_serial_com('COM10')
# print(asd.test_com())
# asd = InverterBaseModel()
# asd.set_serial_com('COM10')
# print(asd.start())


# print(serial.readSerial('01R00001A4'))
# print(time() - start_time)
# start_time = time()
# print(serial.readSerial('01R03001A7'))
# print(time() - start_time)
# print(serial.readSerial('01R03011A8'))
# print(serial.readSerial('01W0380101F48F'))
# print(serial.readSerial('01W03821000177'))

# sleep(2)
# print(serial.readSerial('01R030D1A8'))
# sleep(2)
# print(serial.readSerial('01W03821000076'))
# import os
# import sys
# from datetime import time
# from time import sleep
#
# from PyQt5.QtWidgets import QApplication
#
# app = QApplication(sys.argv)
# from core.app_provider.admin.main import Main
#
# # main = Main()
#
# asd = get_device_by_id(1)
# asd.start_com()
# print('frq',asd.read_frq())
# asd.set_frq_ui(4.82)
#
# print(asd.read_name())
# print(asd.read_capacity())
# print(asd.read_acc_time())
# print(asd.read_deacc_time())
# print('op',asd.read_operating_status())
#
# asd.set_acc_time_ui(250)
# asd.set_deacc_time_ui(25)
# asd.start()
# sleep(2)
# print('frq',asd.read_frq())
# print('op',asd.read_operating_status())
# sleep(20)
# print('frq',asd.read_frq())
# print('op',asd.read_operating_status())
# asd.stop()
# print('frq',asd.read_frq())
# print('op',asd.read_operating_status())
# sleep(5)
# print('frq',asd.read_frq())
# print('op',asd.read_operating_status())
# sys.exit(app.exec_())
# print(asd2)