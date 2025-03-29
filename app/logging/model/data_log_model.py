from datetime import datetime
from queue import Queue, Empty
from threading import Thread
from time import sleep
from typing import Callable

from app.ResourcePath.app_provider.admin.main import resource_path

import numpy as np
from tinydb import TinyDB
from MainCode import log_path

from matplotlib import pyplot as plt


class DataLoggingModel:
    queue: Queue
    stop_thread_flag: bool = False
    insert_thread: Thread
    ax: plt.Axes
    Figure: plt.Figure

    def __init__(self, variable_name: str, log_path_in: str = None, logging_plot_type: int = 0) -> None:
        """

        :param variable_name: variable_name
        :param log_path_in: log_path_in
        :param logging_plot_type:  0 :step, 1:normal plot
        """
        self.database_file_name = variable_name + '.json'
        self.log_table_name = variable_name
        self.variable_name = variable_name
        self.logging_plot_type = logging_plot_type
        self.time_format = '%Y-%m-%d %H:%M:%S:%f'

        self.queue = Queue()

        plt.ion()
        self.fig = plt.figure()
        self.fig.set_visible(False)
        self.fig.canvas.draw_idle()
        self.fig.canvas.manager.set_window_title(self.variable_name)

        self.mngr = plt.get_current_fig_manager()
        self.mngr.window.setGeometry(50, 50 + (self.fig.number - 1) * 500, 500, 500)
        # TODO:alan moshkel ineke hamashon ro ham mioftan bayad bar asas tedad bechinameshon
        self.ax = self.fig.add_subplot(111)

        self.data = []
        self.data_time = []

        self.start_timestamp = datetime.now().timestamp() * 1000000

        # self.line, = self.ax.plot(self.data)
        if logging_plot_type:
            self.line, = self.ax.plot(self.data)
        else:
            self.line, = self.ax.step(np.arange(len(self.data)), self.data)

        # self.ax.set_xlim([0, len(self.data)])
        self.ax.set_xlim([-5, 100])

        # self.line.set_xdata(np.arange(len(self.data)))
        # self.line.set_xdata(np.arange(100))

        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Data')
        self.ax.set_title('Real time Data ' + variable_name)
        self.ax.legend(['Data'], loc='upper right')

        if log_path_in is None:
            self.log_path = resource_path(log_path)
        else:
            self.log_path = log_path_in

        self.stop_thread_flag = False
        self.insert_thread = Thread(target=self.insert_database_thread, args=(lambda: self.stop_thread_flag,))
        self.db = TinyDB(self.log_path + self.database_file_name)

        self.log_table = self.db.table(self.log_table_name)

    def restart_thread(self) -> None:
        self.stop_thread_flag = False
        if not (self.insert_thread.is_alive()):
            self.insert_thread = Thread(target=self.insert_database_thread, args=(lambda: self.stop_thread_flag,))
            self.start_thread()

    def start_thread(self) -> None:
        self.insert_thread.start()

    def stop_thread(self) -> None:
        self.stop_thread_flag = True
        self.insert_thread.join()
        self.plot_figure()

    def insert_database(self, text: dict) -> None:
        data = {
            'value': text['value'],
            'time_send': text['time_send'],
            'time_receive': text['time_receive'],
            'time_insert': text['time_insert']
        }

        self.log_table.insert(data)

    def insert_database_thread(self, stop_thread_flag: Callable[[], bool]) -> None:
        while True:
            try:
                text = self.queue.get(timeout=1)
                self.data.append(text['value'])

                if len(self.data_time) == 0:
                    self.start_timestamp = datetime.now().timestamp() * 1000000
                    self.fig.set_visible(True)

                temp_time = datetime.strptime(text['time_receive'], '%Y-%m-%d %H:%M:%S:%f')
                self.data_time.append((temp_time.timestamp() * 1000000 - self.start_timestamp) / 1000000)

                if len(self.data) > 100:
                    self.data = self.data[-100:]
                    self.data_time = self.data_time[-100:]
                    self.ax.set_xlim([min(self.data_time) * 0.9, max(self.data_time) * 1.1])
                else:
                    self.ax.set_xlim([-max(self.data_time) * 0.05, max(self.data_time) * 1.1])

                self.line.set_xdata(self.data_time)
                self.ax.set_ylim([-max(self.data) * 0.05, max(self.data) * 1.1])
                self.line.set_ydata(self.data)
                self.fig.canvas.draw_idle()

                self.insert_database(text)
                self.queue.task_done()
            except Empty:
                if stop_thread_flag():
                    print("data empty " + self.variable_name)
                    print("stop logging " + self.variable_name)
                    break

            except Exception as error:
                print(error)

            # if stop_thread_flag():
            #     print(self.stop_thread_flag)
            #     print("stop logging " + self.variable_name)
            #     break

    def insert(self, value: float, time_send, time_receive) -> None:
        data = {
            'value': value,
            'time_send': time_send.strftime(self.time_format),
            'time_receive': time_receive.strftime(self.time_format),
            'time_insert': datetime.now().strftime(self.time_format)
        }
        self.queue.put(data)

    def get_log(self) -> list[dict]:
        return self.log_table.all()

    def plot_figure(self):
        logs = self.get_log()

        start_time = datetime.strptime(logs[0]['time_receive'], self.time_format)
        start_timestamp = start_time.timestamp() * 1000000
        times = []
        values = []
        plt.clf()
        self.fig.set_visible(True)
        for log in logs:
            temp_time = datetime.strptime(log['time_receive'], '%Y-%m-%d %H:%M:%S:%f')
            times.append((temp_time.timestamp() * 1000000 - start_timestamp) / 1000000)
            values.append(log['value'])
        if self.logging_plot_type:
            plt.plot(times, values)
        else:
            plt.step(times, values)

        plt.xlabel('time')
        plt.ylabel(self.variable_name)
        plt.title(self.variable_name)

        plt.savefig(self.log_path + self.variable_name + '.png')
