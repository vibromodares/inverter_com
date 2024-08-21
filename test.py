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
# from time import sleep
#
# from time import sleep
#
# from app.database.api.api import get_device_by_id
# from app.inverter.iG5A.iG5AModel_new import iG5AModel
# from app.inverter.inverter_model import InverterBaseModel
# from files.data.make_db import make_tinydb_from_excel, handle_db
# handle_db()
# from app.database.model.database_model import DataBaseModel
#
# # TODO:bayad check kone data on model inverter ra dare ya na dl kone v check kone bebine aslan in model inverter to model haye ma hast ya na


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


# from app.inverter.iG5A.communication_response_model import CommunicationResponse
# from files.data.make_db import get_db_time, handle_db
from files.logs.plot_figure import plot_figure

# from app.logging.model.log_model import LoggingModel

# import sys
# # from datetime import time
# # from time import sleep
# #
# from PyQt5.QtWidgets import QApplication
#
# from app.database.api.api import get_device_by_id
#
# app = QApplication(sys.argv)
# # from core.app_provider.admin.main import Main
#
# # main = Main()
#
# asd = get_device_by_id(1)
# asd.set_serial_com('COM12')
# print(asd.start_com())
# print(asd.read_serial('0380', cmd_in='W', data_in="EA38"))
#
# # print(asd.read_serial('0311', cmd_in='R')[1][0].true_value)
# # print(asd.read_serial('000A', cmd_in='R')[1][0].true_value)
#
# # asd.start_command()
# # print(asd.readSerial('01W038010C8BA1')) #'01W0C8BA5'
# # print(asd.readSerial('01Z03801EA60A3')) #'01W0C8BA5'
#
# # print(asd.readSerial('01W03821000177')) #'01W000179'
# # sleep(2)
# # print(asd.readSerial('01W03821000076')) #'01W000078'
# sys.exit(app.exec_())
# import subprocess
# subprocess.Popen(r'explorer /select,"D:\project\avidMechanic\project\vibromodares\code\main\files\data\iG5A_data.xlsx"')
# import sys
# import random
# import matplotlib
#
# matplotlib.use('Qt5Agg')
#
# from PyQt5 import QtCore, QtWidgets
#
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
#
#
# class MplCanvas(FigureCanvas):
#
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         super(MplCanvas, self).__init__(fig)
#
#
# class MainWindow(QtWidgets.QMainWindow):
#
#     def __init__(self, *args, **kwargs):
#         super(MainWindow, self).__init__(*args, **kwargs)
#
#         self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
#         self.setCentralWidget(self.canvas)
#
#         n_data = 50
#         self.xdata = list(range(n_data))
#         self.ydata = [random.randint(0, 10) for i in range(n_data)]
#
#         # We need to store a reference to the plotted line
#         # somewhere, so we can apply the new data to it.
#         self._plot_ref = None
#         self.update_plot()
#
#         self.show()
#
#         # Setup a timer to trigger the redraw by calling update_plot.
#         self.timer = QtCore.QTimer()
#         self.timer.setInterval(100)
#         self.timer.timeout.connect(self.update_plot)
#         self.timer.start()
#
#     def update_plot(self):
#         # Drop off the first y element, append a new one.
#         self.ydata = self.ydata[1:] + [random.randint(0, 10)]
#
#         # Note: we no longer need to clear the axis.
#         if self._plot_ref is None:
#             # First time we have no plot reference, so do a normal plot.
#             # .plot returns a list of line <reference>s, as we're
#             # only getting one we can take the first element.
#             plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'r')
#             self._plot_ref = plot_refs[0]
#         else:
#             # We have a reference, we can use it to update the data for that line.
#             self._plot_ref.set_ydata(self.ydata)
#
#         # Trigger the canvas to update and redraw.
#         self.canvas.draw()
#
#
# app = QtWidgets.QApplication(sys.argv)
# w = MainWindow()
# app.exec_()
# from datetime import datetime
# dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
# time123 = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S:%f')
# print(time123.timestamp()*1000000)
# print(time123.timestamp())
# print(dt)

plot_figure()