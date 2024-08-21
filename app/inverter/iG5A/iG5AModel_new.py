from datetime import datetime
from queue import Queue, Empty
from threading import Thread
from time import sleep
from typing import Callable, Union, Optional

import serial.tools.list_ports
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QCloseEvent, QMouseEvent
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QGridLayout, QComboBox, QLineEdit, QSpinBox, \
    QDoubleSpinBox

from MainCode import logging_system
from app.database.api.api import get_module_by_id, get_db_by_model_id
from app.database.model.database_model import DataModel
from app.inverter.iG5A.communication_response_model import CommunicationResponse
from app.inverter.inverter_model import InverterBaseModel
from app.logging.model.data_log_model import DataLoggingModel
from core.theme.style.style import inverter_unknown_stylesheet, inverter_connect_stylesheet, \
    inverter_disconnect_stylesheet, no_error_label, yes_error_label, stop_inverter_pb_style, start_inverter_pb_style


class PopupiG5ARowModel(QWidget):
    label: QLabel
    config: dict
    could_update: bool = True
    description_ui: Union[QLabel, QDoubleSpinBox]
    send_queue: Queue
    data_logger: Optional[DataLoggingModel]

    def __init__(self, config: dict, send_queue: Queue):
        super().__init__()
        self.config = config
        self.parent_id = config['parent_id']
        self.address = config['address']
        self.code = self.address.split('x')[-1]
        self.parameter = config['parameter']
        self.allotment_for_bits = config['allotment_for_bits']
        self.description = config['description']
        self.scale = config['scale']
        self.unit = config['unit']
        self.RW = config['RW']
        self.range = config['range']
        self.important = config['important']
        self.show = config['show']
        self.need_update = config['need_update']
        self.min = config['min']
        self.max = config['max']
        self.step = config['step']
        self.decimal = config['decimal']
        self.function = config['function']
        self.refresh_rate = config['refresh_rate']
        self.logging_flag = config['logging']
        self.editable = config['editable']

        self.last_update = datetime.now()

        if self.logging_flag == 1:
            self.data_logger = DataLoggingModel(self.parameter)
            self.data_logger.start_thread()
        else:
            self.data_logger = None

        self.send_queue = send_queue

        self.label = QLabel(self.parameter)

        if self.editable == 0:
            # self.description_ui = QLabel(self.send_queue(self.code, cmd_in='R')[1])
            self.description_ui = QLabel('0')
        else:
            self.description_ui = QDoubleSpinBox()
            if self.max != self.min:
                self.description_ui.setRange(self.min, self.max)

            self.description_ui.setDecimals(self.decimal)
            self.description_ui.setSingleStep(self.step)
            self.description_ui.setValue((self.min + self.max) / 2)

            self.description_ui.installEventFilter(self)

        self.label.setFixedHeight(30)
        self.description_ui.setFixedHeight(30)

    def update_ui(self, force: bool = False) -> None:
        if self.could_update:
            if not force:
                if self.need_update:
                    if self.refresh_rate != -1:
                        if (datetime.now() - self.last_update).total_seconds() > self.refresh_rate:
                            self.update_func()
            else:
                if self.important:
                    self.update_func()

    def update_func(self) -> None:
        self.send_queue.put(
            {'code': self.code, 'data_in': None, 'cmd_in': 'R', 'callback_func': self.update_description_ui,
             'time': datetime.now()})

        self.last_update = datetime.now()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            self.could_update = False
        elif event.type() == QEvent.FocusOut:
            self.could_update = True
        elif event.type() == QEvent.KeyRelease and event.key() == Qt.Key_Enter:
            data_in = self.description_ui.value()
            data_in = int(data_in / self.scale)
            data_in = hex(data_in).split('x')[-1]
            data_in = self.fix_data(data_in)
            self.send_queue.put(
                {'code': self.code, 'data_in': data_in, 'cmd_in': 'W', 'callback_func': None, 'time': datetime.now()})

        return super(PopupiG5ARowModel, self).eventFilter(obj, event)

    def fix_data(self, data_in):
        data_in = data_in.upper()
        if len(data_in) == 1:
            return '000' + data_in
        if len(data_in) == 2:
            return '00' + data_in
        if len(data_in) == 3:
            return '0' + data_in
        return data_in

    def update_description_ui(self, temp_re: list[CommunicationResponse]) -> None:
        if self.scale == -1:
            if self.function == 'operating_status':
                temp_data = temp_re[2].description + ' ' + temp_re[3].description
            else:
                descriptions = []
                for item in temp_re:
                    descriptions.append(item.description)

                temp_data = ' '.join(descriptions)
        else:
            temp_data = round(temp_re[0].true_value, 2)

        if self.editable == 0:
            self.description_ui.setText(str(temp_data))
        else:
            self.description_ui.setValue(temp_data)

        if self.logging_flag:
            self.data_logger.insert(temp_data)

    def close_thread(self):
        if self.logging_flag:
            self.data_logger.stop_thread()


class PopupAdvancediG5AModel(QWidget):
    name: str
    show_flag: bool = False
    parameters_ui: list[PopupiG5ARowModel]

    def __init__(self, parameters_ui: list[PopupiG5ARowModel]):
        super().__init__()

        self.setFixedWidth(500 * 4)

        self.parameters_ui = parameters_ui

        self.name = '_advanced'
        self.setWindowTitle('iG5A ' + self.name)
        main_layout = QGridLayout()

        n_show = len(self.parameters_ui)

        self.setFixedHeight((int(n_show / 4) + 1) * 50)

        for index, ui in enumerate(self.parameters_ui):
            main_layout.addWidget(ui.label, int(index / 4), index % 4 * 2 + 0)
            main_layout.addWidget(ui.description_ui, int(index / 4), index % 4 * 2 + 1)

        self.close_pb = QPushButton('Close')
        self.close_pb.clicked.connect(self.close)
        main_layout.addWidget(self.close_pb, index + 1, 1, 1, 1)

        self.setLayout(main_layout)

    def close(self):
        logging_system.insert(0, "iG5A advanced pop up ui close ui", description="show_flag : " + str(self.show_flag))
        if self.show_flag:
            logging_system.insert(0, "iG5A advanced pop up ui close closing ui")
            super().close()

        self.show_flag = False

    def display_info(self):
        logging_system.insert(0, "iG5A advanced pop up ui display_info",
                              description="show_flag : " + str(self.show_flag))
        if not self.show_flag:
            logging_system.insert(0, "iG5A advanced pop up ui display_info showing ui")
            self.show()
        else:
            self.raise_()

        self.show_flag = True

    def closeEvent(self, event):
        self.close()


class PopupiG5AModel(QWidget):
    """

    """
    name: str
    show_flag: bool = False
    data: dict
    parameters_ui: list[PopupiG5ARowModel]
    error_label: QLabel

    def __init__(self, disconnect_com, start, stop, data: dict, send_queue: Queue):
        super().__init__()

        self.data = data
        self.setFixedWidth(500)

        self.disconnect_com = disconnect_com
        self.start = start
        self.stop = stop
        self.parameters_ui = []
        self.show_ui = []

        self.error_label: QLabel = QLabel('No error')
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet(no_error_label)
        self.error_label.setFixedHeight(30)

        self.name = '1'
        self.setWindowTitle(self.name)
        main_layout = QGridLayout()

        temp_parent_id = []

        for data_temp in self.data:
            if data_temp['parent_id'] not in temp_parent_id:
                temp_parent_id.append(data_temp['parent_id'])
                self.parameters_ui.append(PopupiG5ARowModel(data_temp, send_queue))

        self.advanced_pop_up = PopupAdvancediG5AModel(self.parameters_ui)

        for ui in self.parameters_ui:
            if ui.show == 1:
                self.show_ui.append(ui)

        n_show = len(self.show_ui)

        self.setFixedHeight((n_show + 4 + 2) * 50)

        main_layout.addWidget(self.error_label, 0, 0, 1, 2)

        index = 1
        for ui in self.parameters_ui:
            if ui.function == 'model_name':
                main_layout.addWidget(ui.description_ui, index + 1, 0)
            if ui.function == 'capacity':
                main_layout.addWidget(ui.description_ui, index + 1, 1)
            if ui.function == 'operating_status':
                main_layout.addWidget(ui.label, index, 0)
                main_layout.addWidget(ui.description_ui, index, 1)

        index = index + 3
        for ui in self.show_ui:
            main_layout.addWidget(ui.label, index, 0)
            main_layout.addWidget(ui.description_ui, index, 1)
            index = index + 1

        self.disconnect_pb = QPushButton('disconnect')
        self.disconnect_pb.clicked.connect(self.disconnect_com)
        main_layout.addWidget(self.disconnect_pb, index + 1, 0, 1, 1)

        # self.close_pb = QPushButton('Close')
        # self.close_pb.clicked.connect(self.close)
        # main_layout.addWidget(self.close_pb, index + 1, 1, 1, 1)

        self.advanced_pb = QPushButton('Advanced')
        self.advanced_pb.clicked.connect(self.show_advanced)
        main_layout.addWidget(self.advanced_pb, index + 1, 1, 1, 1)

        self.stop_pb = QPushButton('stop')
        self.stop_pb.clicked.connect(self.stop)
        self.stop_pb.setStyleSheet(stop_inverter_pb_style)
        main_layout.addWidget(self.stop_pb, index + 2, 0, 1, 1)

        self.start_pb = QPushButton('start')
        self.start_pb.clicked.connect(self.start)
        self.start_pb.setStyleSheet(start_inverter_pb_style)
        main_layout.addWidget(self.start_pb, index + 2, 1, 1, 1)

        self.setLayout(main_layout)

    def close(self):
        logging_system.insert(0, "iG5A pop up ui close ui", description="show_flag : " + str(self.show_flag))
        if self.show_flag:
            logging_system.insert(0, "iG5A pop up ui close closing ui")
            super().close()

        self.show_flag = False

    def display_info(self):
        logging_system.insert(0, "iG5A pop up ui display_info", description="show_flag : " + str(self.show_flag))
        if not self.show_flag:
            logging_system.insert(0, "iG5A pop up ui display_info showing ui")
            self.show()
        else:
            self.raise_()

        self.show_flag = True

    def closeEvent(self, event):
        self.close()

    def show_advanced(self):
        self.advanced_pop_up.display_info()

    def close_all(self):
        for ui in self.parameters_ui:
            ui.close_thread()

    def restart_loggers(self):
        for ui in self.parameters_ui:
            if ui.logging_flag:
                ui.data_logger.restart_thread()


class PopupiG5ASetupModel(QWidget):
    name: str
    name_label: QLabel
    com_combo_box: QComboBox
    show_flag: bool = False

    def __init__(self):
        super().__init__()
        self.default_com_port = None
        self.inverter = None
        self.setFixedWidth(500)
        self.setFixedHeight(100)

        self.parent_com_changed = None

        self.name = '1'
        self.setWindowTitle('inverter setup ' + self.name)
        main_layout = QGridLayout()

        self.com_combo_box = QComboBox()

        main_layout.addWidget(QLabel('Com Port: '), 0, 0)
        main_layout.addWidget(self.com_combo_box, 0, 1)

        self.apply_pb = QPushButton('Apply')
        self.apply_pb.clicked.connect(self.apply_func)
        main_layout.addWidget(self.apply_pb, 2, 1, 1, 1)

        self.setLayout(main_layout)

    def display_info(self):
        logging_system.insert(0, "iG5A setup ui display_info", description="show_flag : " + str(self.show_flag))

        if not self.show_flag:
            logging_system.insert(0, "iG5A setup ui display_info showing ui")
            self.com_combo_box.clear()
            combo_items, current_index = self.get_combo_list_current()

            self.com_combo_box.addItems(combo_items)
            self.com_combo_box.adjustSize()
            self.com_combo_box.textActivated.connect(self.change_com)

            self.com_combo_box.setCurrentIndex(current_index)

            self.show()
        else:
            self.raise_()

        self.show_flag = True

    def change_com(self, text: str):
        com = text.split(':')[0]
        # self.parent_com_changed(com)

    def apply_func(self):
        text = self.com_combo_box.currentText()
        com = text.split(':')[0]
        self.parent_com_changed(com)

    def get_combo_list_current(self):
        ports = serial.tools.list_ports.comports()
        disc_port_id = None
        default_port_id = None
        current_index = 0

        combo_items = []

        for id, (port, desc, hwid) in enumerate(sorted(ports)):
            if self.inverter.com_disc in desc:
                disc_port_id = id
            if port == self.default_com_port:
                default_port_id = id

            combo_items.append("{}: {} ".format(port, desc))

        if default_port_id is None and disc_port_id is None:
            combo_items.insert(0, 'none')
            current_index = 0

        elif disc_port_id is not None:
            current_index = disc_port_id
        elif default_port_id is not None:
            current_index = default_port_id

        return combo_items, current_index

    def close(self):
        logging_system.insert(0, "iG5A setup ui close ui", description="show_flag : " + str(self.show_flag))
        if self.show_flag:
            logging_system.insert(0, "iG5A setup ui close closing ui")
            super().close()

        self.show_flag = False

    def closeEvent(self, event):
        self.close()


class iG5AModel(InverterBaseModel):
    start_char = ENQ = chr(5)
    end_char = EOT = chr(4)
    normal_response_char = ACK = chr(6)
    bad_response_char = NAK = chr(21)

    db: DataModel
    send_queue: Queue
    ui_pb: QPushButton

    popup_ui: PopupiG5AModel
    setup_ui: PopupiG5ASetupModel
    error_time: datetime
    error_shade_time: int

    def __init__(self, config: dict) -> None:
        super(iG5AModel, self).__init__()
        self.error_shade_time = 5
        self.error_time = datetime.now()
        self.inverter_id = config['inverter_id']
        self.model_id = config['model_id']
        self.drive_number = config['drive_number']
        self.name = config['name']
        self.default_com_port = config['com_port']
        self.set_serial_com(self.default_com_port)

        self.stop_thread = False

        self.Thread = Thread(target=self.main_thread, args=(lambda: self.stop_thread,))

        self.inverter = get_module_by_id(self.model_id)

        self.db = get_db_by_model_id(self.model_id)

        self.last_update = datetime.now()
        self.refresh_rate = 0.1

        self.send_queue = Queue()

        self.model = 'iG5A'
        self.ui_layout = None
        self.setup_flag = False
        self.ui_need_update = False
        self.popup_ui = PopupiG5AModel(self.disconnect_com, self.start, self.stop, self.db.get_all_data(),
                                       self.send_queue)
        self.popup_ui.name = self.model + str(self.inverter_id)
        self.popup_ui.setWindowTitle(self.popup_ui.name)
        self.setup_ui = PopupiG5ASetupModel()

        self.setup_ui.parent_com_changed = self.com_changed
        self.setup_ui.default_com_port = self.default_com_port
        self.setup_ui.inverter = self.inverter

    def mouseDoubleClickEventChanged(self, q_mouse_event: QMouseEvent) -> None:
        logging_system.insert(0, "iG5A mouse double click", description="setup flag : " + str(self.setup_flag))
        try:
            if self.setup_flag:
                return self.popup_ui.display_info()
            else:
                return self.setup_ui.display_info()
        except Exception as error:
            print("iG5ANew_mouseDoubleClickEventChanged", error)
            logging_system.insert(2, "iG5ANew_mouseDoubleClickEventChanged", error=error)

    def com_changed(self, com: str) -> None:
        logging_system.insert(0, 'iG5A_new com changed', description="com change to " + com)
        if self.Thread.is_alive():
            # TODO: bara in test nanveshtam bayad check beshe
            logging_system.insert(2, "com change", description="thread is alive")

            self.stop_thread = True
            self.Thread.join()
            self.Thread = Thread(target=self.main_thread, args=(lambda: self.stop_thread,))

        self.set_serial_com(com)

        self.stop_thread = False

        self.start_com()
        self.check_com()

        # print("khar nafahm")
        # TODO:bayad check konim k tartib ina doroste ya na

        if self.connect_flag:
            self.setup_ui.close()

            self.popup_ui.display_info()
            self.toggle_popup_ui(True)

            sleep(2)

            if not self.Thread.is_alive():
                self.Thread = Thread(target=self.main_thread, args=(lambda: self.stop_thread,))
                self.Thread.start()

            self.popup_ui.restart_loggers()

    def ui_setter(self, ui_pb: QPushButton):
        self.ui_pb = ui_pb
        self.ui_pb.mouseDoubleClickEvent = self.mouseDoubleClickEventChanged
        self.ui_pb.setStyleSheet(inverter_unknown_stylesheet)

    def disconnect_com(self):
        print("press disconnect")

        self.popup_ui.close()

        self.connect_flag = False
        self.setup_flag = False
        self.stop_thread = True

        self.stop_command()
        self.Thread.join()

        self.popup_ui.close_all()

        self.ui_pb.setStyleSheet(inverter_unknown_stylesheet)

    def start(self):
        self.stop_thread = False

        if not self.Thread.is_alive():
            self.Thread = Thread(target=self.main_thread, args=(lambda: self.stop_thread,))
            self.Thread.start()

        if not self.connect_flag:
            self.start_com()

        if self.connect_flag:
            self.start_command()

    def stop(self):
        # self.stop_thread = True
        self.stop_command()
        # self.Thread.join()

    def start_command(self):
        start_code = '0382'
        forward_code = '0001'

        self.send_queue.put(
            {'code': start_code, 'data_in': forward_code, 'cmd_in': 'W', 'callback_func': None, 'time': datetime.now()})

    def stop_command(self):
        start_code = '0382'
        reverse_code = '0000'

        self.send_queue.put(
            {'code': start_code, 'data_in': reverse_code, 'cmd_in': 'W', 'callback_func': None, 'time': datetime.now()})

    def extract_data(self, response_data):
        # TODO:in ghalate dg in bayad doros she

        id = response_data[0:2]
        RW = response_data[2]
        data = response_data[3:7]
        total = response_data[7:]
        return id, RW, data, total

    def code_data(self, data) -> bytes:
        return bytes(self.start_char + data + self.end_char, 'utf-8')

    def cal_sum(self, code: str, cmd: str, data: str = None) -> str:
        num_byte = self.get_byte(code)
        device_num = self.get_drive_number()
        if data is None:
            return self.get_num_4_sum(self.add_hex(self.convert_str_to_ascii(device_num + cmd + code + num_byte)))
        else:
            return self.get_num_4_sum(
                self.add_hex(self.convert_str_to_ascii(device_num + cmd + code + num_byte + data)))

    def get_drive_number(self) -> str:
        if self.drive_number > 100:
            raise
        elif self.drive_number > 10:
            return str(self.drive_number)

        return '0' + str(self.drive_number)

    def __repr__(self):
        return f"iG5AModel({self.inverter_id}, {self.drive_number}, {self.model})"

    def get_cmd(self, code: str) -> str:
        if code in ['0382', '0380', '0383', '0384']:
            return 'W'
        else:
            return 'R'

    def get_byte(self, code) -> str:
        return '1'

    def check_id(self, response_id: str):
        if response_id == self.get_drive_number():
            return True
        return False

    def check_data_in(self, data_in, data):
        return data_in == data

    def read_serial(self, code: str, data_in: str = None, cmd_in: str = None) -> (bool, list[CommunicationResponse]):
        # TODO:Error code haie k dakhele manual has ro k momkene inja bede ro check nakardim

        if cmd_in is None:
            cmd = self.get_cmd(code)
        else:
            cmd = cmd_in

        sum = self.cal_sum(code, cmd, data_in)
        num_byte = self.get_byte(code)
        device_num = self.get_drive_number()
        if data_in is None:
            final_address = device_num + cmd + code + num_byte + sum
        else:
            final_address = device_num + cmd + code + num_byte + data_in + sum

        try:
            logging_system.insert(0, "read serial", send_address=final_address)
            response_data_read, flag = self.readSerial(final_address)
            logging_system.insert(0, "read serial response", send_address=final_address,
                                  receive_address=response_data_read,
                                  description="flag is : " + str(flag))

        except Exception as e:
            print("read serial except ", e, "send_address = ", final_address)
            logging_system.insert(2, "read serial except", send_address=final_address, error=str(e))
            # self.connect_flag = False
            return False, [CommunicationResponse(code, '0000', '', None)]

        if not flag:
            if len(response_data_read) == 7:
                error_id = response_data_read[3:5]
                if error_id == "IF":
                    self.set_error_ui("master is sending codes other than Function code (R, W, X, Y).")
                if error_id == "IA":
                    self.set_error_ui("parameter address does not exist")
                if error_id == "ID":
                    self.set_error_ui("Data value exceeds its permissible range during ‘W’ (Write).")
                if error_id == "WM":
                    self.set_error_ui("the specific parameters cannot be written during ‘W’ (Write).")
                if error_id == "FE":
                    self.set_error_ui("frame size of specific function is not correct and Checksum field is wrong")

            logging_system.insert(2, 'bad request sent!!', code, final_address, response_data_read)
            print('bad request sent!!', code, final_address, response_data_read)
            return False, [CommunicationResponse(code, '0000', '', None)]

        response_id, RW, response_data, total = self.extract_data(response_data_read)
        if not self.check_id(response_id):
            self.set_error_ui('bad id response')
            print('bad id response', final_address, response_data_read, response_data, response_id,
                  self.get_drive_number())
            logging_system.insert(2, "bad id response", final_address, response_data_read, error="bad id response",
                                  description="response id = " + str(response_id) + " response data = " + str(
                                      response_data))
            return False, [CommunicationResponse(code, '0000', response_data, None)]

        if data_in is not None:
            # TODO:rabt b scale dastgah dare havasemon bashe
            if not self.check_data_in(response_data, data_in):
                self.set_error_ui('bad data response')
                print('bad data response', response_data, data_in, final_address, response_data_read)
                logging_system.insert(2, "bad data response", final_address, response_data_read,
                                      error="bad data response",
                                      description="response id = " + str(response_id) + " response data = " + str(
                                          response_data))
                return False, [CommunicationResponse(code, '0000', response_data, None)]

        responses = self.db.get_responses('0x' + code)

        have_allotment = True
        if len(responses) == 1 and responses[0]['allotment_for_bits'] == '':
            have_allotment = False

        if have_allotment:
            c_rs = []
            ranges = []
            for response in responses:
                temp_range = response['range']
                if temp_range not in ranges:
                    ranges.append(temp_range)
                    c_rs.append(CommunicationResponse(code, temp_range, response_data, self.db))
                    # TODO:inja bayad moshakhas beshe k str pass bede mese baghie moghe ha ya baghie ro bokonim list

            return True, c_rs

        else:
            response = responses[0]
            return True, [CommunicationResponse(code, response['range'], response_data, self.db, have_allotment,
                                                response['scale'], response['unit'])]

    def fix_data(self, data_in):
        data_in = data_in.upper()
        if len(data_in) == 1:
            return '000' + data_in
        if len(data_in) == 2:
            return '00' + data_in
        if len(data_in) == 3:
            return '0' + data_in
        return data_in

    def main_thread(self, stop_thread: Callable[[], bool]) -> None:
        while True:
            try:
                send_object = self.send_queue.get(block=False)

                code = send_object['code']
                data_in = send_object['data_in']
                cmd_in = send_object['cmd_in']
                callback_func = send_object['callback_func']
                time = send_object['time']  # TODO:

                if data_in is None:
                    temp_re = self.read_serial(code, cmd_in=cmd_in)
                else:
                    temp_re = self.read_serial(code, data_in, cmd_in=cmd_in)

                if callback_func is not None:
                    temp_re = temp_re[1]
                    callback_func(temp_re)

                self.send_queue.task_done()

            except Empty:
                if stop_thread():
                    print("stop iG5A model main thread")
                    break
            except Exception as error:
                print(error)

            else:
                pass
                # try:
                #     self.check_com()  # TODO: in nemishe har 0.1 check beshe bayad 2 sanie beshe
                #
                # except Exception as e:
                #     # TODO:in error ro mide inja 'cannot join current thread' bayad befahmam yani chi
                #     print('ig5a new', e)
                #     pass
                #
                # if stop_thread():
                #     break
                # sleep(0.1)

            if self.popup_ui.error_label.text() != "no error":
                if (datetime.now() - self.error_time).total_seconds() > self.error_shade_time:
                    self.set_error_ui("")

            if (datetime.now() - self.last_update).total_seconds() > self.refresh_rate:
                self.toggle_popup_ui()
                self.last_update = datetime.now()

    def check_com(self):
        self.test_com()  # TODO:inja bayad bebine age vasl mishe sabz kone v ghabol kone az baghie ham pak kone

        # TODO:age ghabol shod v sabz shod to db update kone
        if self.connect_flag:
            self.setup_flag = True
            self.ui_pb.setStyleSheet(inverter_connect_stylesheet)

        else:
            logging_system.insert(2, "check com thread", error="connect flag : " + str(self.connect_flag))
            # self.setup_flag = False
            # self.popup_ui.close()
            # self.ui_pb.setStyleSheet(inverter_disconnect_stylesheet)
            # self.stop_thread = True

    def toggle_popup_ui(self, force: bool = False):
        if self.popup_ui.show_flag:
            for ui in self.popup_ui.parameters_ui:
                ui.update_ui(force)

    def set_error_ui(self, text: str = ""):
        self.error_time = datetime.now()

        if text == "":
            self.popup_ui.error_label.setStyleSheet(no_error_label)
            text = "no error"
        else:
            self.popup_ui.error_label.setStyleSheet(yes_error_label)

        self.popup_ui.error_label.setText(text)
