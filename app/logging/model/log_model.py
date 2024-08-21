from datetime import datetime
from queue import Queue, Empty
from threading import Thread
from time import sleep
from typing import Callable

from tinydb import TinyDB, Query

from core.config.MakeConfig import time_format


class LoggingModel:
    queue: Queue
    stop_thread_flag: bool = False
    insert_thread: Thread
    database_db_path = 'files/database/'
    database_file_name = 'log.json'
    log_table_name = 'log'
    error_table_name = 'error'

    def __init__(self, log_path: str = database_db_path) -> None:
        self.queue = Queue()
        self.log_path = log_path
        self.stop_thread_flag = False
        self.insert_thread = Thread(target=self.insert_database_thread, args=(lambda: self.stop_thread_flag,))
        self.db = TinyDB(self.log_path + self.database_file_name)
        self.log_table = self.db.table(self.log_table_name)
        self.error_table = self.db.table(self.error_table_name)

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
        data = {'type': text['type'],
                'place': text['place'],
                'code': text['code'],
                'send_address': text['send_address'],
                'receive_address': text['receive_address'],
                'error': text['error'],
                'description': text['description'],
                'time': text['time']
                }

        if data['send_address'] != "":
            temp_data = ""
            for char in data['send_address']:
                temp_data += hex(ord(char)).split('x')[-1]

            data['send_address'] += " hex : "
            data['send_address'] += temp_data

        if data['receive_address'] != "":
            temp_data = ""
            for char in data['receive_address']:
                temp_data += hex(ord(char)).split('x')[-1]

            data['receive_address'] += " hex : "
            data['receive_address'] += temp_data

        # if data['error'] == "":
        #     self.log_table.insert(data)
        # else:
        #     self.error_table.insert(data)
        # type 0: logging, 1: warning,2:error

        if data['type'] == 0:
            self.log_table.insert(data)
        elif data['type'] == 1:
            self.log_table.insert(data)
        elif data['type'] == 2:
            self.error_table.insert(data)

    def insert_database_thread(self, stop_thread_flag: Callable[[], bool]) -> None:
        while True:
            try:
                text = self.queue.get(timeout=1)
                self.insert_database(text)
                self.queue.task_done()
            except Empty:
                if stop_thread_flag():
                    print("stop logging")
                    break
                sleep(1)
            except Exception as error:
                print(error)

            if stop_thread_flag():
                print(self.stop_thread_flag)
                print("stop logging")
                break

    def insert(self, type: int, place: str, code: str = "", send_address: str = "", receive_address: str = "",
               error: str = "", description: str = "") -> None:

        # type 0: logging, 1: warning,2:error

        data = {'type': type,
                'place': place,
                'code': code,
                'send_address': send_address,
                'receive_address': receive_address,
                'error': error,
                'description': description,
                'time': datetime.now().strftime(time_format)
                }
        self.queue.put(data)

    def get_log(self, type_in: int = -1) -> list[dict]:
        query = Query()

        if type_in == -1:
            log_data = self.log_table.all()
            error_data = self.error_table.all()
            return log_data + error_data
        elif type_in == 0:
            return self.log_table.search(query.type == 0)
        elif type_in == 1:
            return self.log_table.search(query.type == 1)
        elif type_in == 2:
            return self.error_table.search(query.type == 2)
