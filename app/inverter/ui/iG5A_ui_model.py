from PyQt5 import uic
from PyQt5.QtCore import Qt, QDateTime, QTimer, QEvent
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox, QLabel, QCheckBox, QHBoxLayout, QGridLayout, QGroupBox, QRadioButton, \
    QVBoxLayout, QPushButton, QTabWidget, QSizePolicy, QWidget, QTableWidget, QTextEdit, QLineEdit, QSpinBox, \
    QDateTimeEdit, QSlider, QScrollBar, QDial, QProgressBar, QFrame, QMainWindow

from MainCode import path


class iG5A_UI(QFrame):

    def __init__(self):
        super(iG5A_UI, self).__init__()

        uic.loadUi(path + "core/theme/ui/iG5A.ui", self)

        self.main_file_path = "core/theme/pic/"
        self.main_family_file_path = "iG5A/"
        self.model = "iG5A_0.4kw"
        self.width = 400
        self.height = 400

        # stylesheet = ("QWidget {"
        #               "border: none;"
        #               "border-image-slice: fill;"
        #               "background: transparent;"
        #               "border-image: url(" + path + self.main_file_path + self.main_family_file_path + self.model + ".png) 0 0 0 0 stretch stretch;"
        #               "border-image-repeat: stretch;"
        #               "}")
        # "border-image-repeat: stretch;"

        stylesheet = "background-color: rgb(0, 255, 255);"
        self.setStyleSheet(stylesheet)
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)

        # self.setContentsMargins(0,0,0,0)

        # TODO:bar asas dade sensor ham y control sade shayad bezarim

    def get_ui(self):
        commands = ["asd111", "asdf1123"] #TODO:bayad inaro az db nekhone shayad ya az cache
        styleComboBox = QComboBox()
        styleComboBox.addItems(["asd", "asdf1123"])

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)
        layout = QVBoxLayout()
        # topLayout.addWidget(styleLabel)
        # topLayout.addWidget(styleComboBox)
        # topLayout.addStretch(1)

        for command in commands:
            # topLayout.addWidget(self.useStylePaletteCheckBox)

            topLayout = QHBoxLayout()
            q_label_name = QLabel(command)
            q_label_value = QLabel("asd")
            q_label_accuracy = QLineEdit()
            # q_label_accuracy.installEventFilter(self)
            q_label_accuracy.editingFinished.connect(self.param_change)

            # q_label_accuracy.textChanged.connect(self.param_change)
            # q_label_accuracy.textEdited.connect(self.param_change)
            # q_label_accuracy.leaveEvent().connect(self.param_change)
            q_label_predict = QLabel("Neutral")

            q_label_name.setAlignment(Qt.AlignCenter)
            q_label_value.setAlignment(Qt.AlignCenter)
            q_label_accuracy.setAlignment(Qt.AlignCenter)
            q_label_predict.setAlignment(Qt.AlignCenter)

            # TODO:font ham bayad bere to style age beshe age na ham bayad az dakhele core theme tanzim she

            q_label_name.setFont(QFont('Times New Roman', 12))
            q_label_value.setFont(QFont('Times New Roman', 12))
            q_label_accuracy.setFont(QFont('Times New Roman', 12))
            q_label_predict.setFont(QFont('Times New Roman', 12))

            # TODO:inaro bayad y style dehi doros bokonim kolan

            # q_label_name.setStyleSheet(label_style)
            # q_label_value.setStyleSheet(label_style)
            # q_label_accuracy.setStyleSheet(label_style)
            # q_label_predict.setStyleSheet(label_style)

            topLayout.addWidget(q_label_name)
            topLayout.addWidget(q_label_value)
            topLayout.addWidget(q_label_accuracy)
            topLayout.addWidget(q_label_predict)
            topLayout.addStretch(1)
            # topLayout.
            i = layout.count()
            layout.insertLayout(i - 2, topLayout)

        mainLayout = QGridLayout()
        mainLayout.addLayout(layout, 0, 0, 1, 2)
        # mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        # mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        # mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        # mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        # mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        # mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        # mainLayout.setRowStretch(1, 1)
        # mainLayout.setRowStretch(2, 1)
        # mainLayout.setColumnStretch(0, 1)
        # mainLayout.setColumnStretch(1, 1)

        self.setLayout(mainLayout)
        return self

    def param_change(self):
        # TODO:log bardarim k che dastor haie behesh dade shode ast shayad niaz bashe
        #  y seri dade ham in bein az khode inverter bekhonim
        #  v nemodaresho bekeshim shayad
        #  check konam bebinam power ham mide ya na
        #  frequency dade khani ham tosh tarif beshe
        print("asd")

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            print("FocusIn")
            print(obj)
            # if obj is self.LE_sample_input_01:
            #     print("LE_sample_input_01")
            # elif obj is self.LE_sample_input_02:
            #     print("LE_sample_input_02")
        elif event.type() == QEvent.FocusOut:
            print("FocusOut")
            print(obj)
            # if obj is self.LE_sample_input_01:
            #     print("LE_sample_input_01")
            # elif obj is self.LE_sample_input_02:
            #     print("LE_sample_input_02")
        return super(iG5A_UI, self).eventFilter(obj, event)