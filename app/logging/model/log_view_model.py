from PyQt5.QtWidgets import QTableWidget, QComboBox, QHeaderView, QTableWidgetItem
from MainCode import logging_system


class LogViewModel:
    log_tableWidget: QTableWidget
    log_tableWidget: QComboBox

    def __init__(self, log_tableWidget: QTableWidget, type_comboBox: QComboBox):
        self.log_tableWidget = log_tableWidget
        self.type_comboBox = type_comboBox

        self.type_comboBox.currentIndexChanged.connect(self.change_filter)

        self.change_filter(1)

    def change_filter(self, index: int):
        self.log_tableWidget.clear()

        data = []

        if index == 0:
            data = logging_system.get_log()
        elif index == 1:
            data = logging_system.get_log(2)
        elif index == 2:
            data = logging_system.get_log(1)
        elif index == 3:
            data = logging_system.get_log(0)

        row_count = len(data)
        if row_count == 0:
            self.log_tableWidget.setColumnCount(1)
            self.log_tableWidget.setRowCount(1)
            self.log_tableWidget.setItem(0, 0, QTableWidgetItem("no data"))
            return

        if row_count > 100:
            data = data[-100:]
            row_count = len(data)
        # TODO:inja data khondan ro bayad doros konam k dakhele queue bere
        self.log_tableWidget.setColumnCount(7)
        self.log_tableWidget.setRowCount(row_count)

        self.log_tableWidget.setItem(0, 0, QTableWidgetItem("place"))
        self.log_tableWidget.setItem(0, 1, QTableWidgetItem("code"))
        self.log_tableWidget.setItem(0, 2, QTableWidgetItem("send address"))
        self.log_tableWidget.setItem(0, 3, QTableWidgetItem("receive address"))
        self.log_tableWidget.setItem(0, 4, QTableWidgetItem("error"))
        self.log_tableWidget.setItem(0, 5, QTableWidgetItem("description"))
        self.log_tableWidget.setItem(0, 6, QTableWidgetItem("time"))

        for index, row in enumerate(data):
            self.log_tableWidget.setItem(index + 1, 0, QTableWidgetItem(row["place"]))
            self.log_tableWidget.setItem(index + 1, 1, QTableWidgetItem(row["code"]))
            self.log_tableWidget.setItem(index + 1, 2, QTableWidgetItem(row["send_address"]))
            self.log_tableWidget.setItem(index + 1, 3, QTableWidgetItem(row["receive_address"]))
            self.log_tableWidget.setItem(index + 1, 4, QTableWidgetItem(row["error"]))
            self.log_tableWidget.setItem(index + 1, 5, QTableWidgetItem(row["description"]))
            self.log_tableWidget.setItem(index + 1, 6, QTableWidgetItem(row["time"]))

        self.log_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.log_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        header = self.log_tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        # self.log_tableWidget.verticalHeader().setVisible(False)
