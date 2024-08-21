from datetime import datetime
from queue import Queue, Empty
from threading import Thread
from typing import Callable

from tinydb import TinyDB
from MainCode import log_path

from matplotlib import pyplot as plt


class DataLoggingModel:
    queue: Queue
    stop_thread_flag: bool = False
    insert_thread: Thread

    def __init__(self, variable_name: str, log_path_in: str = None) -> None:
        self.database_file_name = variable_name + '.json'
        self.log_table_name = variable_name
        self.variable_name = variable_name
        self.time_format = '%Y-%m-%d %H:%M:%S:%f'

        self.queue = Queue()

        if log_path_in is None:
            self.log_path = log_path
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
            self.insert_thread.start()

    def start_thread(self) -> None:
        self.insert_thread.start()

    def stop_thread(self) -> None:
        self.stop_thread_flag = True
        self.insert_thread.join()

    def insert_database(self, text: dict) -> None:
        data = {
            'value': text['value'],
            'time': text['time']
        }

        self.log_table.insert(data)

    def insert_database_thread(self, stop_thread_flag: Callable[[], bool]) -> None:
        while True:
            try:
                text = self.queue.get(timeout=1)
                self.insert_database(text)
                self.queue.task_done()
            except Empty:
                if stop_thread_flag():
                    print("stop logging " + self.variable_name)
                    break
            except Exception as error:
                print(error)

            if stop_thread_flag():
                print(self.stop_thread_flag)
                print("stop logging " + self.variable_name)
                break

    def insert(self, value: float) -> None:

        # type 0: logging, 1: warning,2:error

        data = {
            'value': value,
            'time': datetime.now().strftime(self.time_format)
        }
        self.queue.put(data)

    def get_log(self) -> list[dict]:
        return self.log_table.all()

    def plot_figure(self):
        logs = self.get_log()
        start_time = datetime.strptime(logs[0]['time'], self.time_format)
        start_timestamp = start_time.timestamp() * 1000000
        times = []
        values = []
        plt.clf()
        for log in logs:
            temp_time = datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S:%f')
            times.append(int((temp_time.timestamp() * 1000000 - start_timestamp) / 1000000))
            values.append(log['value'])
        plt.step(times, values)
        plt.xlabel('time')
        plt.ylabel(self.variable_name)
        plt.title(self.variable_name)

        plt.savefig(self.log_path + self.variable_name + '.png')