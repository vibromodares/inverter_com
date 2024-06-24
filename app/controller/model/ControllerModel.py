from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QGridLayout

from core.theme.style.style import inverter_unknown_stylesheet, inverter_connect_stylesheet


class ControllerModel:
    ui_pb: QPushButton

    def __init__(self):
        self.popup_ui = PopupControllerModel()

    def mouseDoubleClickEventChanged(self, QMouseEvent):
        self.popup_ui.display_info()
        self.ui_pb.setStyleSheet(inverter_connect_stylesheet)

    def ui_setter(self, ui_pb: QPushButton):
        self.ui_pb = ui_pb
        self.ui_pb.mouseDoubleClickEvent = self.mouseDoubleClickEventChanged
        self.ui_pb.setStyleSheet(inverter_unknown_stylesheet)

    def start(self):
        self.ui_pb.setStyleSheet(inverter_connect_stylesheet)

class PopupControllerModel(QWidget):
    name: str
    k_coe: int = 10
    name_label: QLabel
    name_label: int

    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setFixedHeight(100)

        self.name = 'P controller'
        self.setWindowTitle('GNDCenter ' + self.name)
        main_layout = QGridLayout()

        self.name_label = QLabel(self.name)
        main_layout.addWidget(QLabel('Name: '), 0, 0)
        main_layout.addWidget(self.name_label, 0, 1)

        main_layout.addWidget(QLabel('P : '), 1, 0)
        main_layout.addWidget(QLabel(str(self.k_coe)), 1, 1)

        self.close_pb = QPushButton('Close')
        self.close_pb.clicked.connect(self.close)
        main_layout.addWidget(self.close_pb, 3, 0, 1, 2)

        self.setLayout(main_layout)

    def display_info(self):
        self.show()
