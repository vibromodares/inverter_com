import os
from datetime import datetime
from time import sleep

from PyQt5 import uic
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QLabel, QPushButton, QDesktopWidget, QVBoxLayout, QComboBox, QWidget, QFrame, QRadioButton, \
    QTableWidget

from MainCode import path
from app.acc_meter.model.AccMeterModel import AccMeterModel
from app.controller.model.ControllerModel import ControllerModel
from app.database.api.api import get_module_model, get_device_by_id
from app.gnd_center.model.GNDCenterModel import GNDCenterModel
from app.inverter.iG5A.iG5AModel_new import iG5AModel
from app.logging.model.log_view_model import LogViewModel
from app.motor.model.MotorModel import MotorModel
from app.plant.model.PlantModel import PlantModel
from app.speed_meter.model.SpeedMeterModel import SpeedMeterModel
from core.model.SplashScreen import SplashScreen
from core.theme.style.style import close_pb_style


class MainUi(QFrame):
    onlyInt: QIntValidator = QIntValidator(1, 100)
    tab_main: QWidget

    start_service_pb: QPushButton
    stop_service_pb: QPushButton
    close_pb: QPushButton

    main_logo_label: QLabel
    setting_logo_label: QLabel

    gnd_inv_line: QFrame
    inv_motor_line: QFrame
    motor_plan_line: QFrame
    plan_acc_line: QFrame
    acc_cnt_line: QFrame
    acc_cnt_2_line: QFrame
    spd_cnt_line: QFrame
    motor_spd_line: QFrame
    inv_cnt_2_line: QFrame
    inv_cnt_line: QFrame

    gnd_center_ui_pb: QPushButton
    inverter_ui_pb: QPushButton
    motor_ui_pb: QPushButton
    plan_ui_pb: QPushButton
    acc_meter_ui_pb: QPushButton
    spd_meter_ui_pb: QPushButton
    controller_ui_pb: QPushButton

    help_ui_pb: QPushButton
    user_manual_pb: QPushButton

    motor: MotorModel
    gnd_center: GNDCenterModel
    plant: PlantModel
    acc_meter: AccMeterModel
    speed_meter: SpeedMeterModel
    controller: ControllerModel

    module: iG5AModel

    verticalLayout_inverter: QVBoxLayout

    log_tableWidget: QTableWidget
    log_view_model:LogViewModel
    type_comboBox: QComboBox


    def __init__(self):
        super(MainUi, self).__init__()

        uic.loadUi(path + "core/theme/ui/main.ui", self)

        self.setWindowTitle("vibro modaress")
        self.setWindowIcon(QIcon(path + "core/theme/icons/logo.ico"))
        self.setFrameShape(QFrame.StyledPanel)

        self.setMouseTracking(True)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.init_ui()

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        self.LoginNow = datetime.now()

    def init_ui(self):
        from core.theme.pic import Pics

        self.tab_main = self.findChild(QWidget, "Main")
        self.start_service_pb = self.findChild(QPushButton, "start_service_pb")
        self.stop_service_pb = self.findChild(QPushButton, "stop_service_pb")

        self.main_logo_label = self.findChild(QLabel, "main_logo_label")
        self.setting_logo_label = self.findChild(QLabel, "setting_logo_label")

        self.gnd_inv_line = self.findChild(QFrame, "gnd_inv_line")
        self.inv_motor_line = self.findChild(QFrame, "inv_motor_line")
        self.motor_plan_line = self.findChild(QFrame, "motor_plan_line")
        self.plan_acc_line = self.findChild(QFrame, "plan_acc_line")
        self.acc_cnt_line = self.findChild(QFrame, "acc_cnt_line")
        self.acc_cnt_2_line = self.findChild(QFrame, "acc_cnt_2_line")
        self.spd_cnt_line = self.findChild(QFrame, "spd_cnt_line")
        self.motor_spd_line = self.findChild(QFrame, "motor_spd_line")
        self.inv_cnt_2_line = self.findChild(QFrame, "inv_cnt_2_line")
        self.inv_cnt_line = self.findChild(QFrame, "inv_cnt_line")

        self.gnd_center_ui_pb = self.findChild(QPushButton, "gnd_center_ui_pb")
        self.inverter_ui_pb = self.findChild(QPushButton, "inverter_ui_pb")
        self.motor_ui_pb = self.findChild(QPushButton, "motor_ui_pb")
        self.plan_ui_pb = self.findChild(QPushButton, "plan_ui_pb")
        self.acc_meter_ui_pb = self.findChild(QPushButton, "acc_meter_ui_pb")
        self.spd_meter_ui_pb = self.findChild(QPushButton, "spd_meter_ui_pb")
        self.controller_ui_pb = self.findChild(QPushButton, "controller_ui_pb")

        self.verticalLayout_inverter: QVBoxLayout = self.findChild(QVBoxLayout, "verticalLayout_inverter")

        self.log_tableWidget: QTableWidget = self.findChild(QTableWidget, "log_tableWidget")
        self.type_comboBox: QComboBox = self.findChild(QComboBox, "type_comboBox")

        self.user_manual_pb = self.findChild(QPushButton, "user_manual_pb")
        self.user_manual_pb.clicked.connect(self.open_user_manual)

        self.help_ui_pb = self.findChild(QPushButton, "help_ui_pb")
        self.help_ui_pb.clicked.connect(self.open_help_ui)

        self.log_view_model = LogViewModel(self.log_tableWidget, self.type_comboBox)

        self.motor = MotorModel()
        self.gnd_center = GNDCenterModel()
        self.plant = PlantModel()
        self.acc_meter = AccMeterModel()
        self.speed_meter = SpeedMeterModel()
        self.controller = ControllerModel()

        #   Start Colors
        from core.theme.color.color import tab_selected_bg_color, tab_selected_text_color

        from core.theme.style.style import ui_line_style, start_service_pb_style, stop_service_pb_style

        # stylesheet = "QTabBar::tab:selected {background-color: " + tab_selected_bg_color + ";" + \
        #              "color: " + tab_selected_text_color + ";font-size: 8pt;}" + \
        #              "QTabWidget>QWidget>QWidget{background-image: url(" + path + \
        #              "core/theme/pic/pic/Main.jpg);background-repeat: no-repeat;background-position:center;}" + \
        #              "MainUi { background-image: url(" + path + "core/theme/pic/pic/Main.jpg);" + \
        #              "background-repeat: no-repeat;background-position:center;} "
        stylesheet = "QTabBar::tab:selected {background-color: " + tab_selected_bg_color + ";" + \
                     "color: " + tab_selected_text_color + ";font-size: 10pt;}" + \
                     "QTabWidget>QWidget>QWidget{border-image: url(" + path + \
                     "core/theme/pic/pic/Main.jpg);background-repeat: no-repeat;background-position:center;}" + \
                     "MainUi { border-image: url(" + path + "core/theme/pic/pic/Main.jpg);" + \
                     "background-repeat: no-repeat;background-position:center;} "
        self.setStyleSheet(stylesheet)

        qt_rectangle = self.frameGeometry()
        qt_rectangle.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qt_rectangle.topLeft())

        #   End Colors

        # modules = get_all_module()
        self.module = get_device_by_id(1)
        # trades.remove(get_trading(12))
        # trades = [get_trading(11)]

        # self.add_module_to_threads(modules)

        # # self.start_trade_threads()
        #
        # self.main_trading_thread = MainTradingThreadModel(self.trade_threads)

        self.setting_logo_label.setPixmap(Pics.Logo)
        self.main_logo_label.setPixmap(Pics.Logo)

        # self.open_trade_window_pb = self.findChild(QPushButton, "open_trade_window_pb")
        # data_connector = DataConnector()
        # self.open_trade_window_pb.clicked.connect(lambda: data_connector.open_trade_window())
        #
        # self.open_trade_window_pb.setStyleSheet(active_pb_style)

        self.close_pb = self.findChild(QPushButton, "close_pb")
        self.close_pb.setStyleSheet(close_pb_style)

        # self.go_to_account_pb = self.findChild(QPushButton, "go_to_account_pb")
        # self.go_to_account_pb.setStyleSheet(active_pb_style)
        #
        # self.open_instructions_pb = self.findChild(QPushButton, "open_instructions_pb")
        # self.open_instructions_pb.setStyleSheet(active_pb_style)
        # self.open_instructions_pb.clicked.connect(self.open_instructions)
        #
        # self.open_instructions_label = self.findChild(QLabel, "open_instructions_label")
        # self.open_instructions_label.setStyleSheet(label_style)

        self.start_service_pb.setStyleSheet(start_service_pb_style)
        self.start_service_pb.clicked.connect(self.main_service_start_thread)

        self.stop_service_pb.setStyleSheet(stop_service_pb_style)
        # self.stop_service_pb.hide()
        self.stop_service_pb.clicked.connect(self.main_service_stop_thread)

        self.gnd_inv_line.setStyleSheet(ui_line_style)
        self.inv_motor_line.setStyleSheet(ui_line_style)
        self.motor_plan_line.setStyleSheet(ui_line_style)
        self.plan_acc_line.setStyleSheet(ui_line_style)
        self.acc_cnt_line.setStyleSheet(ui_line_style)
        self.acc_cnt_2_line.setStyleSheet(ui_line_style)
        self.spd_cnt_line.setStyleSheet(ui_line_style)
        self.motor_spd_line.setStyleSheet(ui_line_style)
        self.inv_cnt_2_line.setStyleSheet(ui_line_style)
        self.inv_cnt_line.setStyleSheet(ui_line_style)

        self.motor.ui_setter(self.motor_ui_pb)
        self.gnd_center.ui_setter(self.gnd_center_ui_pb)
        self.plant.ui_setter(self.plan_ui_pb)
        self.acc_meter.ui_setter(self.acc_meter_ui_pb)
        self.speed_meter.ui_setter(self.spd_meter_ui_pb)
        self.controller.ui_setter(self.controller_ui_pb)
        self.module.ui_setter(self.inverter_ui_pb)

        # self.balance_comboBox = self.findChild(QComboBox, "balance_comboBox")
        # self.balance_comboBox.setStyleSheet(line_edit_style)
        # self.balance_comboBox.setCurrentIndex(1)
        # self.balance_comboBox.currentIndexChanged.connect(self.balance_comboBox_change)
        #
        # self.balance_value_label = self.findChild(QLabel, "balance_value_label")
        # self.balance_value_label.setStyleSheet(balance_label_style)
        #
        # self.amount_label = self.findChild(QLabel, "amount_label")
        # self.amount_label.setStyleSheet(label_style)
        #
        # self.time_label = self.findChild(QLabel, "time_label")
        # self.time_label.setStyleSheet(label_style)
        #
        # self.trading_asset_label = self.findChild(QLabel, "trading_asset_label")
        # self.trading_asset_label.setStyleSheet(label_style)
        #
        # self.trading_asset_value_label = self.findChild(QLabel, "trading_asset_value_label")
        # self.trading_asset_value_label.setStyleSheet(line_edit_style)
        #
        # self.trading_asset_prop_label = self.findChild(QLabel, "trading_asset_prop_label")
        # self.trading_asset_prop_label.setStyleSheet(line_edit_prop_style)
        #
        # self.amount_spinBox = self.findChild(QSpinBox, "amount_spinBox")
        # self.amount_spinBox.setStyleSheet(line_edit_style)
        #
        # self.time_comboBox = self.findChild(QComboBox, "time_comboBox")
        # self.time_comboBox.setStyleSheet(line_edit_style)
        # self.time_comboBox.setCurrentIndex(0)
        #
        # self.optimal_strategy_radioButton = self.findChild(QRadioButton, "optimal_strategy_radioButton")
        # self.optimal_strategy_radioButton.setStyleSheet(optimal_strategy_rb_style)
        #
        # self.optimal_strategy_label = self.findChild(QLabel, "optimal_strategy_label")
        # self.optimal_strategy_label.setStyleSheet(optimal_strategy_label_style)
        #
        # self.activate_label_4 = self.findChild(QLabel, "activate_label_4")
        # self.activate_label_4.setStyleSheet(
        #     "border-image: url(" + path + "core/theme/pic/pic/flags.png);background-repeat: "
        #                                   "no-repeat;background-position:center;")
        # self.activate_label_5 = self.findChild(QLabel, "activate_label_5")
        # self.activate_label_5.setStyleSheet(
        #     "border-image: url(" + path + "core/theme/pic/pic/sound.png);background-repeat: "
        #                                   "no-repeat;background-position:center;")
        #
        # self.question_label = self.findChild(QLabel, "question_label")
        # self.question_label.setStyleSheet(
        #     "border-image: url(" + path + "core/theme/pic/pic/question_mark.png);background-repeat: "
        #                                   "no-repeat;background-position:center;")
        #
        # self.question_label_2 = self.findChild(QLabel, "question_label_2")
        # self.question_label_2.setStyleSheet(
        #     "border-image: url(" + path + "core/theme/pic/pic/question_mark.png);background-repeat: "
        #                                   "no-repeat;background-position:center;")
        #
        # self.activate_label_main = self.findChild(QLabel, "activate_label_main")
        # self.activate_label_main.setStyleSheet(label_style)
        #
        # self.quotex_username_label = self.findChild(QLabel, "quotex_username_label")
        # self.quotex_username_label.setStyleSheet(label_style)
        #
        # self.quotex_password_label = self.findChild(QLabel, "quotex_password_label")
        # self.quotex_password_label.setStyleSheet(label_style)
        #
        # self.quotex_username_lineEdit = self.findChild(QLineEdit, "quotex_username_lineEdit")
        # self.quotex_username_lineEdit.setStyleSheet(label_style)
        #
        # self.quotex_password_lineEdit = self.findChild(QLineEdit, "quotex_password_lineEdit")
        # self.quotex_password_lineEdit.setStyleSheet(label_style)
        #
        # self.show_user_pass_from_config()
        #
        # self.set_profile_pb = self.findChild(QPushButton, "set_profile_pb")
        # self.set_profile_pb.setStyleSheet(active_pb_style)
        # self.set_profile_pb.clicked.connect(self.set_profile_to_config)
        #
        # self.activate_account_pb = self.findChild(QPushButton, "activate_account_pb")
        # # self.activate_pb.clicked.connect(lambda: data_connector.open_trade_window())
        #
        # self.activate_account_pb.setStyleSheet(activate_account_pb_style)
        #
        # # self.aggressive_strategy_radioButton = self.findChild(QRadioButton, "aggressive_strategy_radioButton")
        # # self.aggressive_strategy_radioButton.setStyleSheet(line_edit_style)
        #
        # self.main_trading_thread.max_trading_label = self.trading_asset_value_label
        # self.main_trading_thread.max_trading_value_label = self.trading_asset_prop_label
        # self.main_trading_thread.balance_value_label = self.balance_value_label
        # self.balance_value_label.setText("$" + str(data_connector.get_balance()))
        # self.Setting.DebugPrintFlag = self.findChild(QCheckBox, "DebugPrintFlag")

        # self.Setting.TestSensor_lineEdit = self.findChild(QLineEdit, "TestSensor_lineEdit")
        #
        # self.Sensor_Status.Sensor_Submit_pb = self.Sensor_Status.findChild(QPushButton, "Sensor_Submit_pb")

    def add_module_to_ui(self, module: dict) -> None:
        """
        add trade QH to vertical layout
        :param name: name
        :param value: value
        :return:
        """
        pass
        # verticalLayout_trade.insertWidget()

        # for i in reversed(range(verticalLayout_trade.count())):
        #     widget = verticalLayout_trade.itemAt(i).widget()
        #     verticalLayout_trade.removeWidget(widget)

        # h1 = QHBoxLayout()
        # # h1 = QVBoxLayout()
        #
        # from core.theme.style.style import label_style
        #
        # q_label_name = QLabel(name)
        # q_label_value = QLabel(value)
        # q_label_accuracy = QLabel("0")
        # q_label_predict = QLabel("Neutral")
        #
        # q_label_name.setAlignment(Qt.AlignCenter)
        # q_label_value.setAlignment(Qt.AlignCenter)
        # q_label_accuracy.setAlignment(Qt.AlignCenter)
        # q_label_predict.setAlignment(Qt.AlignCenter)
        #
        # q_label_name.setFont(QFont('Times New Roman', 12))
        # q_label_value.setFont(QFont('Times New Roman', 12))
        # q_label_accuracy.setFont(QFont('Times New Roman', 12))
        # q_label_predict.setFont(QFont('Times New Roman', 12))
        #
        # q_label_name.setStyleSheet(label_style)
        # q_label_value.setStyleSheet(label_style)
        # q_label_accuracy.setStyleSheet(label_style)
        # q_label_predict.setStyleSheet(label_style)
        #
        #
        # h1.addWidget(q_label_name)
        # h1.addWidget(q_label_value)
        # h1.addWidget(q_label_accuracy)
        # h1.addWidget(q_label_predict)
        #
        # i = verticalLayout_trade.count()
        # verticalLayout_trade.insertLayout(i - 2, h1)
        # return {"q_label_name": q_label_name,
        #         "q_label_value": q_label_value,
        #         "q_label_accuracy": q_label_accuracy,
        #         "q_label_predict": q_label_predict}

    def main_service_start_thread(self):
        """
            starting the main trade thread
        """
        # self.start_service_pb.hide()
        # self.start_service_pb.setEnabled(False)
        if not self.module.connect_flag:
            self.module.start_com()
        # self.module.start_com()
        self.module.start()
        self.motor.start()
        self.gnd_center.start()
        self.plant.start()
        self.acc_meter.start()
        self.speed_meter.start()
        self.controller.start()
        # if self.module.connect_flag:
        # # self.stop_service_pb.show()
        #     self.stop_service_pb.setEnabled(True)
        # else:
        #     self.stop_service_pb.setEnabled(False)
        #     self.start_service_pb.setEnabled(True)

    def main_service_stop_thread(self):
        """
            starting the main trade thread
        """
        self.module.stop()

        # self.module.stop_com()
        # self.start_service_pb.setEnabled(True)

        # self.start_service_pb.show()
        # self.amount_spinBox.setEnabled(1)
        # self.time_comboBox.setEnabled(1)
        # self.balance_comboBox.setEnabled(1)
        # self.quotex_password_lineEdit.setEnabled(1)
        # self.quotex_username_lineEdit.setEnabled(1)
        # self.set_profile_pb.setEnabled(1)

    def add_module_to_threads(self, modules):
        """
            add trade to self-trade threads
        :param trades: list[TradingModel]
        """
        self.module_threads = []

        for module in modules:
            model = get_module_model(module['model_id'])
            inv_model = model(module)
            inv_model.ui_layout = self.verticalLayout_inverter
            inv_model.update_ui()
            index = self.add_module_to_ui(module)

            self.module_threads.append(inv_model)

        # verticalLayout_trade.insertWidget(i, mainLayout)

        # # widget.setParent(None)

    def start_trade_threads(self):
        for trade in self.trade_threads:
            trade.start_thread()

    def stop_trade_threads(self, splash_screen: SplashScreen):
        self.main_service_stop_thread()

        for trade in self.trade_threads:
            splash_screen.show_message("closing trade " + trade.trade.currency_disp())
            trade.thread.join()
            splash_screen.add_saved_text("trade " + trade.trade.currency_disp() + " closed!")

    def open_user_manual(self):
        file_name = "files/help/user_manual.pdf"
        file_name = os.path.join(path, file_name)
        try:
            os.startfile(file_name)
        except Exception as e:
            print(e)

    def open_help_ui(self):
        file_name = "files/help/user_manual.pdf"
        file_name = os.path.join(path, file_name)
        try:
            os.startfile(file_name)
        except Exception as e:
            print(e)
