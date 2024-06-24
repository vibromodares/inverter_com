from PyQt5 import uic
from PyQt5.QtCore import Qt, QDateTime, QTimer, QObject, pyqtSignal, QEvent
from PyQt5.QtWidgets import QComboBox, QLabel, QCheckBox, QHBoxLayout, QGridLayout, QGroupBox, QRadioButton, \
    QVBoxLayout, QPushButton, QTabWidget, QSizePolicy, QWidget, QTableWidget, QTextEdit, QLineEdit, QSpinBox, \
    QDateTimeEdit, QSlider, QScrollBar, QDial, QProgressBar, QFrame, QMainWindow

import serial.tools.list_ports

from MainCode import path
from app.database.model.inverter_model import InverterModel


class SetupUI(QFrame):
    com_label: QLabel
    com_combo_box: QComboBox
    default_com_port: str = None
    inverter: InverterModel

    def __init__(self):
        super(SetupUI, self).__init__()
        uic.loadUi(path + "core/theme/ui/setup.ui", self)

        self.main_file_path = "core/theme/pic/"
        # self.main_family_file_path = "iG5A/"
        # self.model = "iG5A_0.4kw"
        self.width = 400
        self.height = 400
        self.parent_com_changed = None

        # stylesheet = ("QWidget {"
        #               "border: none;"
        #               "border-image-slice: fill;"
        #               "background: transparent;"
        #               "border-image: url(" + path + self.main_file_path + self.main_family_file_path + self.model + ".png) 0 0 0 0 stretch stretch;"
        #               "border-image-repeat: stretch;"
        #               "}")
        # "border-image-repeat: stretch;"
        stylesheet = ("QFrame>QWidget{background-color: rgb(255, 50, 50);}"
                      "QFrame{background-color: rgb(255, 255, 255);}")
        self.central_widget = self.findChild(QWidget, "central_widget")

        self.setStyleSheet(stylesheet)
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        # self.setContentsMargins(0,0,0,0)

        self.com_combo_box = self.findChild(QComboBox, "com_combo_box")

        self.com_label = self.findChild(QLabel, "com_label")
        self.com_label.setStyleSheet("background: transparent;")

    def get_ui(self):
        self.com_combo_box.clear() #TODO:check konim bebinim in clear kar mikone ya na

        combo_items, current_index = self.get_combo_list_current()

        # TODO:inja har bar k ro dokme mizane bayad refresh beshe v update kone list ro

        self.com_combo_box.addItems(combo_items)
        self.com_combo_box.adjustSize()
        self.com_combo_box.textActivated.connect(self.change_com)

        self.com_combo_box.setCurrentIndex(current_index)

        # combo box set text center
        # self.com_combo_box.setEditable(True)
        # ledit = self.com_combo_box.lineEdit()
        # ledit.setAlignment(Qt.AlignCenter)
        # ledit.setReadOnly(True)
        #
        # self.clickable(self.com_combo_box).connect(self.com_combo_box.showPopup)
        # self.clickable(ledit).connect(self.com_combo_box.showPopup)
        # combo box set text center

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)
        # topLayout.addWidget(self.useStylePaletteCheckBox)
        # topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        # mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        # mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        # mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        # mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        # mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        # mainLayout.setRowStretch(1, 1)
        # mainLayout.setRowStretch(2, 1)
        # mainLayout.setColumnStretch(0, 1)
        # mainLayout.setColumnStretch(1, 1)

        # self.setLayout(mainLayout)
        return self

    def change_com(self, text: str):
        com = text.split(':')[0]
        self.parent_com_changed(com)
        # current_index = self.balance_comboBox.currentIndex()

    def clickable(self, widget):
        """ class taken from
        https://wiki.python.org/moin/PyQt/Making%20non-clickable%20widgets%20clickable """

        class Filter(QObject):
            clicked = pyqtSignal()

            def eventFilter(self, obj, event):
                if obj == widget:
                    if event.type() == QEvent.MouseButtonRelease:
                        if obj.rect().contains(event.pos()):
                            self.clicked.emit()
                            # The developer can opt for .emit(obj) to get the object within the slot.
                            return True
                return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

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
