# db = DataBaseModel(file_name='inverter_models.json')
# db.insert_data({
#     'model_id': '1',
#     'name': 'iG5A',
#     'com_disc': 'USB-SERIAL CH340',
# })
# db.insert_data({
#     'model_id': '2',
#     'name': 'PLC',
#     'com_disc': 'USB-SERIAL CH340'
# })
from app.database.api.api import get_all_module

# TODO:bayad check kone data on model inverter ra dare ya na dl kone v check kone bebine aslan in model inverter to model haye ma hast ya na


# db = DataBaseModel(file_name='inverter_list.json')
# db.insert_data({
#     'inverter_id': '1',
#     'model_id': '1',
#     'name': 'main',
#     'com_port': 'COM11',
# })
#
# db.insert_data({
#     'inverter_id': '2',
#     'model_id': '1',
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
