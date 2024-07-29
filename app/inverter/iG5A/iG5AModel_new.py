from threading import Thread
from time import sleep
from typing import Callable

import serial.tools.list_ports
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QGridLayout, QComboBox, QLineEdit, QSpinBox, \
    QDoubleSpinBox

from app.database.api.api import get_module_by_id, get_db_by_model_id
from app.database.model.database_model import DataModel
from app.inverter.iG5A.communication_response_model import CommunicationResponse
from app.inverter.inverter_model import InverterBaseModel
from core.theme.style.style import inverter_unknown_stylesheet, inverter_connect_stylesheet, \
    inverter_disconnect_stylesheet


class iG5AModel(InverterBaseModel):
    start_char = ENQ = chr(5)
    end_char = EOT = chr(4)
    normal_response_char = ACK = chr(6)
    bad_response_char = NAK = chr(21)

    db: DataModel

    ui_pb: QPushButton

    def __init__(self, config: dict) -> None:
        super(iG5AModel, self).__init__()
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

        self.model = 'iG5A'
        self.ui_layout = None
        self.setup_flag = False
        self.ui_need_update = False
        self.popup_ui = PopupiG5AModel(self.disconnect_com, self.start, self.stop, self.db.get_all_data(),
                                       self.read_serial)
        self.setup_ui = PopupiG5ASetupModel()

        self.setup_ui.parent_com_changed = self.com_changed
        self.setup_ui.default_com_port = self.default_com_port
        self.setup_ui.inverter = self.inverter

        self.popup_ui.set_deacc_time = self.set_deacc_time_ui
        self.popup_ui.set_acc_time = self.set_acc_time_ui
        self.popup_ui.set_frq = self.set_frq_ui

    def mouseDoubleClickEventChanged(self, QMouseEvent):
        if self.setup_flag:
            self.popup_ui.frq_sp.setValue(self.read_frq())
            self.popup_ui.acc_time_sp.setValue(self.read_acc_time())
            self.popup_ui.deacc_time_sp.setValue(self.read_deacc_time())
            return self.popup_ui.display_info()
        else:
            return self.setup_ui.display_info()

    def com_changed(self, com: str) -> None:
        self.set_serial_com(com)
        self.stop_thread = False

        if not self.Thread.is_alive():
            self.Thread = Thread(target=self.main_thread, args=(lambda: self.stop_thread,))
            self.Thread.start()

        self.start_com()
        self.check_com()
        # print("khar nafahm")
        # TODO:bayad check konim

        if self.connect_flag:
            self.setup_ui.close()

            self.popup_ui.display_info()
            self.update_popup_ui(True)

    def ui_setter(self, ui_pb: QPushButton):
        self.ui_pb = ui_pb
        self.ui_pb.mouseDoubleClickEvent = self.mouseDoubleClickEventChanged
        self.ui_pb.setStyleSheet(inverter_unknown_stylesheet)

    def disconnect_com(self):
        self.popup_ui.close()

        self.connect_flag = False
        self.setup_flag = False
        self.stop_thread = True

        self.stop_command()
        self.Thread.join()

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

        self.read_serial(start_code, forward_code)

    def stop_command(self):
        start_code = '0382'
        reverse_code = '0000'

        self.read_serial(start_code, reverse_code)

    def read_frq(self):
        frq_code = '0005'
        flag, response_data = self.read_serial(frq_code)
        return float(response_data / 100)

    def read_test(self):
        frq_code = '0302'
        flag, response_data = self.read_serial(frq_code)
        if flag:
            return response_data
        else:
            return 0

    def set_frq(self, data_in):
        # data_in='05DC' 15
        frq_code = '0380'
        self.read_serial(frq_code, data_in)

    def set_frq_ui(self, data_in: float):
        data_in = int(data_in * 100)
        data_in = hex(data_in).split('x')[-1]
        data_in = self.fix_data(data_in)
        self.set_frq(data_in)

    def read_name(self):
        name_code = '0300'
        flag, response_data = self.read_serial(name_code)
        if flag:
            return response_data
        else:
            return 0

    def read_capacity(self):
        capacity_code = '0301'
        flag, response_data = self.read_serial(capacity_code)
        if flag:
            return response_data
        else:
            return 0

    def read_power(self):
        power_code = '0316'
        flag, response_data = self.read_serial(power_code)
        if flag:
            return response_data
        else:
            return 0

    def read_acc_time(self):
        # acc_code = '0383'
        acc_code = '0007'
        flag, response_data = self.read_serial(acc_code)
        return response_data

    def set_acc_time(self, data_in):
        acc_code = '0383'
        self.read_serial(acc_code, data_in)

    def set_acc_time_ui(self, data_in: float):
        data_in = int(data_in * 10)
        data_in = hex(data_in).split('x')[-1]
        data_in = self.fix_data(data_in)
        self.set_acc_time(data_in)

    def read_deacc_time(self):
        # deacc_code = '0384'
        deacc_code = '0008'
        flag, response_data = self.read_serial(deacc_code)
        return int(response_data / 10)

    def set_deacc_time(self, data_in):
        deacc_code = '0384'
        self.read_serial(deacc_code, data_in)

    def set_deacc_time_ui(self, data_in: float):
        data_in = int(data_in * 10)
        data_in = hex(data_in).split('x')[-1]
        data_in = self.fix_data(data_in)
        self.set_deacc_time(data_in)

    def read_operating_status(self):
        operating_code = '0305'
        # operating_code = '000E'
        flag, response_data = self.read_serial(operating_code)
        # TODO:in bayad to ui hamishe hei namayesh dade beshe
        return response_data

    def extract_data(self, response_data):
        id = response_data[0:2]
        RW = response_data[2]
        data = response_data[3:7]
        total = response_data[7:]
        return id, RW, data, total

    def code_data(self, data) -> bytes:
        return bytes(self.start_char + data + self.end_char, 'utf-8')

    def cal_sum(self, code: str, data: str = None) -> str:
        num_byte = self.get_byte(code)
        cmd = self.get_cmd(code)
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

    def read_serial(self, code: str, data_in: str = None, cmd_in: str = None) -> (bool, str):
        sum = self.cal_sum(code, data_in)
        if cmd_in is None:
            cmd = self.get_cmd(code)
        else:
            cmd = cmd_in
        num_byte = self.get_byte(code)
        device_num = self.get_drive_number()
        if data_in is None:
            final_address = device_num + cmd + code + num_byte + sum
        else:
            final_address = device_num + cmd + code + num_byte + data_in + sum

        try:
            response_data, flag = self.readSerial(final_address)
        except:
            self.connect_flag = False
            return False, '0'

        if not flag:
            print('bad request sent!!', code, final_address)
            return False, '0'
        response_id, RW, response_data, total = self.extract_data(response_data)

        if not self.check_id(response_id):
            print('bad id response')
            return False, '0'

        if data_in is not None:
            # TODO:ino check konam k bebinam chera bazi mogheha ino mide
            if not self.check_data_in(response_data, data_in):
                print('bad data response')
                return False, '0'

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
            if stop_thread():
                break
            sleep(0.1)
            try:
                self.check_com()
                self.update_popup_ui()
            except Exception as e:
                # TODO:in error ro mide inja 'cannot join current thread' bayad befahmam yani chi
                print('ig5a new', e)
                pass

    def check_com(self):
        self.test_com()  # TODO:inja bayad bebine age vasl mishe sabz kone v ghabol kone az baghie ham pak kone

        # TODO:age ghabol shod v sabz shod to db update kone
        if self.connect_flag:
            self.setup_flag = True
            self.ui_pb.setStyleSheet(inverter_connect_stylesheet)

        else:
            self.setup_flag = False
            self.popup_ui.close()
            self.ui_pb.setStyleSheet(inverter_disconnect_stylesheet)
            self.stop_thread = True
            self.Thread.join()

    def update_popup_ui(self, force: bool = False):
        if self.popup_ui.show_flag:
            for ui in self.popup_ui.parameters_ui:
                if not force:
                    if ui.need_update:
                        ui.update_ui()
                else:
                    # TODO:bayad ba hame bashe vali bug dare
                    if ui.important:
                        ui.update_ui()
            # self.popup_ui.frq_sp.setValue(self.read_frq())
            # self.popup_ui.acc_time_sp.setValue(self.read_acc_time())
            # self.popup_ui.deacc_time_sp.setValue(self.read_deacc_time())


class PopupiG5ARowModel(QWidget):
    label: QLabel
    config: dict
    should_update: bool = True

    def __init__(self, config, read_serial):
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

        self.read_serial = read_serial

        self.label = QLabel(self.parameter)

        if self.scale == -1:
            self.description_ui = QLabel(self.read_serial(self.code)[1])
        else:
            self.description_ui = QDoubleSpinBox()
            self.description_ui.setRange(self.min, self.max)
            self.description_ui.setDecimals(self.decimal)
            self.description_ui.setSingleStep(self.step)
            self.description_ui.setValue((self.min + self.max) / 2)

            self.description_ui.installEventFilter(self)

        self.label.setFixedHeight(30)
        self.description_ui.setFixedHeight(30)

    def update_ui(self):
        if self.should_update:
            try:
                if self.code == '0380':
                    code = '0005'
                elif self.code == '0383':
                    code = '0007'
                elif self.code == '0384':
                    code = '0008'
                else:
                    code = self.code

                if self.scale == -1:
                    if self.function == 'operating_status':
                        temp_re = self.read_serial(code)[1]
                        temp_data = temp_re[2].description+' ' + temp_re[3].description
                    else:
                        temp_data = self.read_serial(code)[1][0].description

                else:
                    temp_data = self.read_serial(code)[1][0].true_value

            except Exception as e:
                if self.scale == -1:
                    temp_data = ''
                else:
                    temp_data = 0

            if self.scale == -1:
                self.description_ui.setText(temp_data)
            else:
                self.description_ui.setValue(temp_data)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            self.should_update = False
            # if obj is self.LE_sample_input_01:
            #     print("LE_sample_input_01")
            # elif obj is self.LE_sample_input_02:
            #     print("LE_sample_input_02")
        elif event.type() == QEvent.FocusOut:
            self.should_update = True
            # if obj is self.deacc_time_sp:
            #     self.set_deacc_time(self.deacc_time_sp.value())
            # elif obj is self.acc_time_sp:
            #     self.set_acc_time(self.acc_time_sp.value())
            # elif obj is self.frq_sp:
            #     self.set_frq(self.frq_sp.value())
            pass
        elif event.type() == QEvent.KeyRelease and event.key() == Qt.Key_Enter:
            # if obj is self.deacc_time_sp:
            #     self.set_deacc_time(self.deacc_time_sp.value())
            # elif obj is self.acc_time_sp:
            #     self.set_acc_time(self.acc_time_sp.value())
            # elif obj is self.frq_sp:
            #     self.set_frq(self.frq_sp.value())

            data_in = self.description_ui.value()
            data_in = int(data_in / self.scale)
            data_in = hex(data_in).split('x')[-1]
            data_in = self.fix_data(data_in)
            self.read_serial(self.code,data_in)

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

class PopupiG5AModel(QWidget):
    name: str
    frq_sp: QDoubleSpinBox
    acc_time_sp: QSpinBox
    deacc_time_sp: QSpinBox
    show_flag: bool = False
    data: dict
    parameters_ui: list[PopupiG5ARowModel]

    def __init__(self, disconnect_com, start, stop, data: dict, read_serial):
        super().__init__()

        self.data = data
        self.setFixedWidth(500)

        self.set_deacc_time = None
        self.set_acc_time = None
        self.set_frq = None
        self.disconnect_com = disconnect_com
        self.start = start
        self.stop = stop
        self.parameters_ui = []
        self.show_ui = []

        self.name = '1'
        self.setWindowTitle('iG5A ' + self.name)
        main_layout = QGridLayout()

        temp_parent_id = []

        for data_temp in self.data:
            if data_temp['parent_id'] not in temp_parent_id:
                temp_parent_id.append(data_temp['parent_id'])
                self.parameters_ui.append(PopupiG5ARowModel(data_temp, read_serial))

        for ui in self.parameters_ui:
            if ui.show == 1:
                self.show_ui.append(ui)

        n_show = len(self.show_ui)

        self.setFixedHeight((n_show + 4 + 1) * 50)

        # self.frq_sp = QDoubleSpinBox()
        # self.frq_sp.setRange(0, 50)
        # self.frq_sp.setDecimals(2)
        # self.frq_sp.setSingleStep(0.01)
        # self.frq_sp.setValue(5)
        index = 0
        for ui in self.parameters_ui:
            if ui.function == 'model_name':
                main_layout.addWidget(ui.description_ui, index + 1, 0)
            if ui.function == 'capacity':
                main_layout.addWidget(ui.description_ui, index + 1, 1)
            if ui.function == 'operating_status':
                main_layout.addWidget(ui.label, index, 0)
                main_layout.addWidget(ui.description_ui, index, 1)

        index = index + 2
        for ui in self.show_ui:
            main_layout.addWidget(ui.label, index, 0)
            main_layout.addWidget(ui.description_ui, index, 1)
            index = index + 1

        # self.acc_time_sp = QSpinBox()
        # self.acc_time_sp.setRange(0, 6000)
        # self.acc_time_sp.setValue(300)
        # main_layout.addWidget(QLabel('Acceleration time: '), 1, 0)
        # main_layout.addWidget(self.acc_time_sp, 1, 1)
        #
        # self.deacc_time_sp = QSpinBox()
        # self.deacc_time_sp.setRange(0, 6000)
        # self.deacc_time_sp.setValue(30)
        # main_layout.addWidget(QLabel('Deceleration time: '), 2, 0)
        # main_layout.addWidget(self.deacc_time_sp, 2, 1)

        self.disconnect_pb = QPushButton('disconnect')
        self.disconnect_pb.clicked.connect(self.disconnect_com)
        main_layout.addWidget(self.disconnect_pb, index + 1, 0, 1, 1)

        self.close_pb = QPushButton('Close')
        self.close_pb.clicked.connect(self.close)
        main_layout.addWidget(self.close_pb, index + 1, 1, 1, 1)

        self.stop_pb = QPushButton('stop')
        self.stop_pb.clicked.connect(self.stop)
        main_layout.addWidget(self.stop_pb, index + 2, 0, 1, 1)

        self.start_pb = QPushButton('start')
        self.start_pb.clicked.connect(self.start)
        main_layout.addWidget(self.start_pb, index + 2, 1, 1, 1)

        # self.deacc_time_sp.installEventFilter(self)
        # self.acc_time_sp.installEventFilter(self)
        # self.frq_sp.installEventFilter(self)

        self.setLayout(main_layout)

    def close(self):
        if self.show_flag:
            super().close()

        self.show_flag = False

    def display_info(self):
        if not self.show_flag:
            self.show()
        self.show_flag = True


class PopupiG5ASetupModel(QWidget):
    name: str
    name_label: QLabel
    com_combo_box: QComboBox
    show_flag: bool = False

    def __init__(self):
        super().__init__()
        self.default_com_port = None
        self.inverter = None
        self.setFixedWidth(800)
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
        main_layout.addWidget(self.apply_pb, 2, 0, 1, 2)

        self.setLayout(main_layout)

    def display_info(self):
        if not self.show_flag:
            self.com_combo_box.clear()
            combo_items, current_index = self.get_combo_list_current()

            self.com_combo_box.addItems(combo_items)
            self.com_combo_box.adjustSize()
            self.com_combo_box.textActivated.connect(self.change_com)

            self.com_combo_box.setCurrentIndex(current_index)

            self.show()

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
        if self.show_flag:
            super().close()
        self.show_flag = False
