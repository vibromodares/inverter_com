from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QGridLayout

from core.theme.style.style import inverter_unknown_stylesheet, inverter_connect_stylesheet


class MotorModel:
    ui_pb: QPushButton

    def __init__(self):
        self.popup_ui = PopupMotorModel()

    def mouseDoubleClickEventChanged(self, QMouseEvent):
        self.popup_ui.display_info()
        self.ui_pb.setStyleSheet(inverter_connect_stylesheet)

    def ui_setter(self, ui_pb: QPushButton):
        self.ui_pb = ui_pb
        self.ui_pb.mouseDoubleClickEvent = self.mouseDoubleClickEventChanged
        self.ui_pb.setStyleSheet(inverter_unknown_stylesheet)

    def start(self):
        self.ui_pb.setStyleSheet(inverter_connect_stylesheet)
class PopupMotorModel(QWidget):
    name: str
    name_label: QLabel

    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setFixedHeight(100)

        self.name = '2'
        self.setWindowTitle('motor ' + self.name)
        main_layout = QGridLayout()

        self.name_label = QLabel(self.name)
        main_layout.addWidget(QLabel('Name: '), 0, 0)
        main_layout.addWidget(self.name_label, 0, 1)

        self.close_pb = QPushButton('Close')
        self.close_pb.clicked.connect(self.close)
        main_layout.addWidget(self.close_pb, 2, 0, 1, 2)

        self.setLayout(main_layout)

    def display_info(self):
        self.show()
