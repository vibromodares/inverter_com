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
import time

from app.database.api.api import get_all_module
from app.inverter.iG5A.iG5AModel_new import iG5AModel
# from app.inverter.inverter_model import InverterBaseModel
# from files.data.make_db import make_tinydb_from_excel, handle_db
# handle_db()
# from app.database.model.database_model import DataBaseModel
#
# # TODO:bayad check kone data on model inverter ra dare ya na dl kone v check kone bebine aslan in model inverter to model haye ma hast ya na
import os
import sys

# from core.theme.style.style import progress_bar_style
# from files.data.make_db import MakeDBUIModel
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
# from files.logs.plot_figure import plot_figure
# plot_figure()
# from app.logging.model.log_model import LoggingModel

# import sys
# # from datetime import time
# # from time import sleep
# #
from PyQt5.QtWidgets import QApplication

from app.database.api.api import get_device_by_id

app = QApplication(sys.argv)
from core.app_provider.admin.main import Main

main = Main()

asd = get_device_by_id(1)
asd.set_serial_com('COM5')

print(asd.start_com())

time.sleep(1)
# print(asd.read_serial('0380', cmd_in='W', data_in="EA38"))

# print(asd.read_serial('0323', cmd_in='R'))
# print(asd.read_serial('A103', cmd_in='R'))
print(asd.read_serial('A103', cmd_in='W', data_in="0003"))
# print(asd.read_serial('A104', cmd_in='W', data_in="0007"))

# print(asd.read_serial('0006', cmd_in='R'))
# print(asd.read_serial('0306', cmd_in='R'))
#
print(asd.stop_com())
#
# sys.exit(app.exec_())
# print(asd.read_serial('0311', cmd_in='R')[1][0].true_value)
# print(asd.read_serial('000A', cmd_in='R')[1][0].true_value)

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

# if os.path.exists("files/data/database.json"):
#   os.remove("files/data/database.json")
#
# app = QtWidgets.QApplication(sys.argv)
# # w = MainWindow()
# # main = Main()
# try:
#     db_ui = MakeDBUIModel()
#     db_ui.handle_db()
# except Exception as e:
#     print(e)
# app.exec_()
# sys.exit(app.exec())
# from datetime import datetime
# dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
# time123 = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S:%f')
# print(time123.timestamp()*1000000)
# print(time123.timestamp())
# print(dt)


# from random import randint
# import sys
# from PyQt5.QtCore import QTimer
# from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QProgressBar
#
#
#
# class ProgressBar(QProgressBar):
#
#     def __init__(self, *args, **kwargs):
#         super(ProgressBar, self).__init__(*args, **kwargs)
#         self.setValue(0)
#         if self.minimum() != self.maximum():
#             self.timer = QTimer(self, timeout=self.onTimeout)
#             self.timer.start(randint(1, 3) * 1000)
#
#     def onTimeout(self):
#         if self.value() >= 100:
#             self.timer.stop()
#             self.timer.deleteLater()
#             del self.timer
#             return
#         self.setValue(self.value() + 1)
#
#
# class Window(QWidget):
#
#     def __init__(self, *args, **kwargs):
#         super(Window, self).__init__(*args, **kwargs)
#         self.resize(800, 600)
#         layout = QVBoxLayout(self)
#         layout.addWidget(
#             ProgressBar(self, minimum=0, maximum=100, objectName="RedProgressBar"))
#
#         layout.addWidget(
#             ProgressBar(self, minimum=0, maximum=0, objectName="RedProgressBar"))
#
#         layout.addWidget(
#             ProgressBar(self, minimum=0, maximum=100, textVisible=False,
#                         objectName="GreenProgressBar"))
#         layout.addWidget(
#             ProgressBar(self, minimum=0, maximum=0, textVisible=False,
#                         objectName="GreenProgressBar"))
#
#         layout.addWidget(
#             ProgressBar(self, minimum=0, maximum=100, textVisible=False,
#                         objectName="BlueProgressBar"))
#         layout.addWidget(
#             ProgressBar(self, minimum=0, maximum=0, textVisible=False,
#                         objectName="BlueProgressBar"))
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyleSheet(StyleSheet)
#     w = Window()
#     w.show()
#     sys.exit(app.exec_())
# import sys
# import time
# from PyQt5.QtCore import QThread, pyqtSignal
# from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QVBoxLayout, QApplication
#
#
# class Thread(QThread):
#     _signal = pyqtSignal(int)
#
#     def __init__(self):
#         super(Thread, self).__init__()
#
#     def __del__(self):
#         self.wait()
#
#     def run(self):
#         for i in range(100):
#             time.sleep(0.1)
#             self._signal.emit(i)
#
#
# class Example(QWidget):
#     def __init__(self):
#         super(Example, self).__init__()
#         self.setWindowTitle('QProgressBar')
#         self.btn = QPushButton('Click me')
#         self.btn.clicked.connect(self.btnFunc)
#         self.pbar = QProgressBar(self)
#         self.pbar.setValue(0)
#         self.resize(300, 100)
#         self.vbox = QVBoxLayout()
#         self.vbox.addWidget(self.pbar)
#         self.vbox.addWidget(self.btn)
#         self.setLayout(self.vbox)
#         self.show()
#
#     def btnFunc(self):
#         self.thread = Thread()
#         self.thread._signal.connect(self.signal_accept)
#         self.thread.start()
#         self.btn.setEnabled(False)
#
#     def signal_accept(self, msg):
#         self.pbar.setValue(int(msg))
#         if self.pbar.value() == 99:
#             self.pbar.setValue(0)
#             self.btn.setEnabled(True)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ex = Example()
#     ex.show()
#     sys.exit(app.exec_())

