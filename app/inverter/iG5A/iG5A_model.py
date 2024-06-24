from typing import Union, Optional

from PyQt5.QtWidgets import QVBoxLayout

from app.database.api.api import get_module_by_id
from app.database.model.inverter_model import InverterModel
from app.inverter.inverter_model import InverterBaseModel
from app.inverter.ui.iG5A_ui_model import iG5A_UI
from app.inverter.ui.iG5A_setup_ui_model import SetupUI

# TODO: change bein adi v rs485

class iG5AModel(InverterBaseModel):
    start_char = ENQ = chr(5)
    end_char = EOT = chr(4)
    normal_response_char = ACK = chr(6)
    bad_response_char = NAK = chr(21)

    setup_flag: bool = False
    connect_flag: bool = False
    ui_need_update: bool = False
    ui_layout: Optional[QVBoxLayout] = None
    inverter_id: int
    model_id: int
    name: str
    default_com_port: str
    inverter: InverterModel
    start_flag: bool = False

    def __init__(self, config: dict) -> None:
        super(iG5AModel, self).__init__()

        self.inverter_id = config['inverter_id']
        self.model_id = config['model_id']
        self.drive_number = config['drive_number']
        self.name = config['name']
        self.default_com_port = config['com_port']

        self.inverter = get_module_by_id(self.inverter_id)

        self.model = 'iG5A'
        self.ui_layout = None
        self.setup_flag = False
        self.ui_need_update = False

        self.ui = iG5A_UI()
        self.setup_ui = SetupUI()
        self.setup_ui.parent_com_changed = self.com_changed
        self.setup_ui.default_com_port = self.default_com_port
        self.setup_ui.inverter = self.inverter
        self.init_serial()

    def get_ui(self) -> Union[iG5A_UI, SetupUI]:
        if self.setup_flag:
            return self.ui.get_ui()
        else:
            return self.setup_ui.get_ui()

    def update_ui(self) -> None:
        # item = self.ui_layout.itemAt(self.inverter_id)
        #
        # if item is not None:
        #     widget = item.widget()
        #     # self.ui_layout.replaceWidget(widget, self.get_ui)
        #     self.ui_layout.removeWidget(widget)
        #
        # self.ui_layout.insertWidget(self.inverter_id, self.get_ui())
        # # TODO:nemidonam in daghighan doros kar mikone ya na,natonestam checkesh konam
        pass

    def com_changed(self, com: str) -> None:
        self.set_serial_com(com)
        self.connect_flag = self.test_com()  # TODO:inja bayad bebine age vasl mishe sabz kone v ghabol kone az baghie ham pak kone
        # TODO:age ghabol shod v sabz shod to db update kone
        if self.connect_flag:
            self.setup_flag = True
            self.update_ui()

    def init_serial(self) -> None:
        self.serial.start_char = self.start_char
        self.serial.end_char = self.end_char

    # def start(self):
    #     pass
    #     # TODO:vaghti start zade mishe nabayad hame chi deactive beshe bayad
    #     #  bar asas driveview bebinim kodomaro mishe avaz kard kodomaro nemishe
    #     #  betor mesal freq acc dec jahat
    #     #  reverse ham malom beshe to code
